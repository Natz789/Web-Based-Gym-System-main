from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date, timedelta
from decimal import Decimal


class User(AbstractUser):
    """Custom User model with role-based access and demographics"""
    
    ROLE_CHOICES = [
        ('admin', 'Admin'),
        ('staff', 'Staff'),
        ('member', 'Member'),
    ]
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='member')
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)
    birthdate = models.DateField(blank=True, null=True)
    age = models.IntegerField(blank=True, null=True)
    

    kiosk_pin = models.CharField(
        max_length=6, 
        blank=True, 
        null=True, 
        unique=True,
        help_text="6-digit PIN for kiosk check-in/out",
        verbose_name="Kiosk PIN"
    )
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def save(self, *args, **kwargs):
        """Auto-calculate age from birthdate before saving"""
        # Auto-assign admin role to superusers
        if self.is_superuser and self.role != 'admin':
            self.role = 'admin'
        
        # Auto-assign staff role to staff users (if not already admin)
        if self.is_staff and self.role == 'member' and not self.is_superuser:
            self.role = 'staff'
        
        if self.birthdate:
            # Handle both date objects and string inputs
            if isinstance(self.birthdate, str):
                from datetime import datetime
                try:
                    self.birthdate = datetime.strptime(self.birthdate, '%Y-%m-%d').date()
                except ValueError:
                    self.birthdate = None
            
            if self.birthdate:
                today = date.today()
                self.age = today.year - self.birthdate.year - (
                    (today.month, today.day) < (self.birthdate.month, self.birthdate.day)
                )
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.role})"
    
    def is_admin(self):
        """Check if user is admin (includes superusers)"""
        return self.role == 'admin' or self.is_superuser
    
    def is_staff_or_admin(self):
        """Check if user is staff or admin"""
        return self.role in ['admin', 'staff'] or self.is_superuser or self.is_staff
      # NEW METHOD - Add this method
    def generate_kiosk_pin(self):
        """Generate a unique 6-digit PIN for kiosk access"""
        import random
        while True:
            pin = ''.join([str(random.randint(0, 9)) for _ in range(6)])
            if not User.objects.filter(kiosk_pin=pin).exists():
                self.kiosk_pin = pin
                self.save()
                return pin
    
    # NEW METHOD - Add this method
    def has_kiosk_access(self):
        """Check if user has kiosk access (active membership)"""
        if self.role != 'member':
            return False
        
        active_membership = UserMembership.objects.filter(
            user=self,
            status='active',
            end_date__gte=date.today()
        ).first()
        
        return active_membership is not None

class MembershipPlan(models.Model):
    """Permanent membership plans (monthly, yearly, etc.)"""
    
    name = models.CharField(max_length=100)
    duration_days = models.IntegerField(help_text="Duration in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'membership_plans'
        verbose_name = 'Membership Plan'
        verbose_name_plural = 'Membership Plans'
        ordering = ['price']
    
    def __str__(self):
        return f"{self.name} - ₱{self.price} ({self.duration_days} days)"


class FlexibleAccess(models.Model):
    """Walk-in passes (1-day, 3-day, weekly, etc.)"""
    
    name = models.CharField(max_length=100)
    duration_days = models.IntegerField(help_text="Validity in days")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'flexible_access'
        verbose_name = 'Flexible Access Pass'
        verbose_name_plural = 'Flexible Access Passes'
        ordering = ['duration_days']
    
    def __str__(self):
        return f"{self.name} - ₱{self.price} ({self.duration_days} days)"


class UserMembership(models.Model):
    """Tracks member subscriptions to plans"""
    
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('cancelled', 'Cancelled'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='memberships')
    plan = models.ForeignKey(MembershipPlan, on_delete=models.PROTECT, related_name='subscriptions')
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'user_memberships'
        verbose_name = 'User Membership'
        verbose_name_plural = 'User Memberships'
        ordering = ['-start_date']
    
    def save(self, *args, **kwargs):
        """Auto-calculate end_date based on plan duration"""
        if not self.end_date and self.start_date and self.plan:
            self.end_date = self.start_date + timedelta(days=self.plan.duration_days)
        
        # Auto-update status based on dates
        if self.end_date < date.today():
            self.status = 'expired'
        
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.plan.name} ({self.status})"
    
    def is_active(self):
        """Check if membership is currently active"""
        return self.status == 'active' and self.end_date >= date.today()
    
    def days_remaining(self):
        """Calculate days remaining in membership"""
        if self.end_date >= date.today():
            return (self.end_date - date.today()).days
        return 0


class Payment(models.Model):
    """Payment records for registered members"""
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('gcash', 'GCash'),
        ('card', 'Card'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    membership = models.ForeignKey(UserMembership, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField(default=timezone.now)
    reference_no = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'payments'
        verbose_name = 'Payment'
        verbose_name_plural = 'Payments'
        ordering = ['-payment_date']
    
    def __str__(self):
        return f"{self.user.get_full_name()} - ₱{self.amount} ({self.payment_date.strftime('%Y-%m-%d')})"


class WalkInPayment(models.Model):
    """Payment records for walk-in clients (no account required)"""
    
    PAYMENT_METHOD_CHOICES = [
        ('cash', 'Cash'),
        ('gcash', 'GCash'),
        ('card', 'Card'),
    ]
    
    pass_type = models.ForeignKey(FlexibleAccess, on_delete=models.PROTECT, related_name='walk_in_sales')
    customer_name = models.CharField(max_length=100, blank=True, null=True)
    mobile_no = models.CharField(max_length=20, blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)
    payment_date = models.DateTimeField(default=timezone.now)
    reference_no = models.CharField(max_length=50, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'walk_in_payments'
        verbose_name = 'Walk-in Payment'
        verbose_name_plural = 'Walk-in Payments'
        ordering = ['-payment_date']
    
    def __str__(self):
        customer = self.customer_name if self.customer_name else "Anonymous"
        return f"{customer} - {self.pass_type.name} - ₱{self.amount}"


class Analytics(models.Model):
    """Daily/weekly aggregated data for dashboard"""
    
    date = models.DateField(unique=True)
    total_members = models.IntegerField(default=0)
    total_passes = models.IntegerField(default=0)
    total_sales = models.DecimalField(max_digits=10, decimal_places=2, default=Decimal('0.00'))
    age_group = models.CharField(max_length=20, blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'analytics'
        verbose_name = 'Analytics'
        verbose_name_plural = 'Analytics'
        ordering = ['-date']
    
    def __str__(self):
        return f"Analytics for {self.date}"
    
    @classmethod
    def generate_daily_report(cls, target_date=None):
        """Generate analytics for a specific date"""
        if target_date is None:
            target_date = date.today()
        
        # Count active memberships
        active_members = UserMembership.objects.filter(
            status='active',
            start_date__lte=target_date,
            end_date__gte=target_date
        ).count()
        
        # Count walk-in passes sold on this date
        passes_sold = WalkInPayment.objects.filter(
            payment_date__date=target_date
        ).count()
        
        # Calculate total sales
        member_sales = Payment.objects.filter(
            payment_date__date=target_date
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
        
        walkin_sales = WalkInPayment.objects.filter(
            payment_date__date=target_date
        ).aggregate(total=models.Sum('amount'))['total'] or Decimal('0.00')
        
        total_sales = member_sales + walkin_sales
        
        # Create or update analytics record
        analytics, created = cls.objects.update_or_create(
            date=target_date,
            defaults={
                'total_members': active_members,
                'total_passes': passes_sold,
                'total_sales': total_sales,
            }
        )
        
        return analytics
    
class AuditLog(models.Model):
    """Audit trail for all system activities and transactions"""
    
    ACTION_CHOICES = [
        # Authentication
        ('login', 'User Login'),
        ('logout', 'User Logout'),
        ('login_failed', 'Login Failed'),
        ('register', 'User Registration'),
        
        # User Management
        ('user_created', 'User Created'),
        ('user_updated', 'User Updated'),
        ('user_deleted', 'User Deleted'),
        ('role_changed', 'Role Changed'),
        
        # Membership
        ('membership_created', 'Membership Created'),
        ('membership_updated', 'Membership Updated'),
        ('membership_cancelled', 'Membership Cancelled'),
        ('membership_expired', 'Membership Expired'),
        
        # Payments
        ('payment_received', 'Payment Received'),
        ('walkin_sale', 'Walk-in Sale'),
        ('payment_refunded', 'Payment Refunded'),
        
        # Plans
        ('plan_created', 'Plan Created'),
        ('plan_updated', 'Plan Updated'),
        ('plan_deleted', 'Plan Deleted'),
        
        # System
        ('data_export', 'Data Exported'),
        ('report_generated', 'Report Generated'),
        ('settings_changed', 'Settings Changed'),
        
        # Security
        ('unauthorized_access', 'Unauthorized Access Attempt'),
        ('password_changed', 'Password Changed'),
        ('permission_denied', 'Permission Denied'),
    ]
    
    SEVERITY_CHOICES = [
        ('info', 'Info'),
        ('warning', 'Warning'),
        ('error', 'Error'),
        ('critical', 'Critical'),
    ]
    
    user = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='audit_logs'
    )
    action = models.CharField(max_length=50, choices=ACTION_CHOICES)
    severity = models.CharField(max_length=10, choices=SEVERITY_CHOICES, default='info')
    description = models.TextField()
    ip_address = models.GenericIPAddressField(null=True, blank=True)
    user_agent = models.TextField(blank=True, null=True)
    
    # Related objects (optional)
    model_name = models.CharField(max_length=100, blank=True, null=True)
    object_id = models.CharField(max_length=100, blank=True, null=True)
    object_repr = models.CharField(max_length=200, blank=True, null=True)
    
    # Additional data in JSON format
    extra_data = models.JSONField(default=dict, blank=True)
    
    timestamp = models.DateTimeField(auto_now_add=True, db_index=True)
    
    class Meta:
        db_table = 'audit_logs'
        verbose_name = 'Audit Log'
        verbose_name_plural = 'Audit Logs'
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['user', '-timestamp']),
            models.Index(fields=['action', '-timestamp']),
        ]
    
    def __str__(self):
        user_str = self.user.username if self.user else 'Anonymous'
        return f"{self.timestamp.strftime('%Y-%m-%d %H:%M:%S')} - {user_str} - {self.get_action_display()}"
    
    @classmethod
    def log(cls, action, user=None, description='', severity='info', 
            request=None, model_name=None, object_id=None, object_repr=None, **extra_data):
        """
        Create an audit log entry
        
        Usage:
            AuditLog.log('login', user=request.user, description='User logged in successfully')
        """
        ip_address = None
        user_agent = None
        
        if request:
            # Get IP address
            x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
            if x_forwarded_for:
                ip_address = x_forwarded_for.split(',')[0]
            else:
                ip_address = request.META.get('REMOTE_ADDR')
            
            # Get user agent
            user_agent = request.META.get('HTTP_USER_AGENT', '')
        
        return cls.objects.create(
            user=user,
            action=action,
            severity=severity,
            description=description,
            ip_address=ip_address,
            user_agent=user_agent,
            model_name=model_name,
            object_id=str(object_id) if object_id else None,
            object_repr=object_repr,
            extra_data=extra_data
        )
    
    @classmethod
    def get_user_activity(cls, user, days=30):
        """Get recent activity for a specific user"""
        from django.utils import timezone
        from datetime import timedelta
        
        start_date = timezone.now() - timedelta(days=days)
        return cls.objects.filter(
            user=user,
            timestamp__gte=start_date
        )
    
    @classmethod
    def get_security_events(cls, days=7):
        """Get recent security-related events"""
        from django.utils import timezone
        from datetime import timedelta
        
        start_date = timezone.now() - timedelta(days=days)
        security_actions = ['login_failed', 'unauthorized_access', 'permission_denied']
        return cls.objects.filter(
            action__in=security_actions,
            timestamp__gte=start_date
        )
    
    @classmethod
    def get_financial_transactions(cls, start_date=None, end_date=None):
        """Get all financial transaction logs"""
        financial_actions = ['payment_received', 'walkin_sale', 'payment_refunded']
        logs = cls.objects.filter(action__in=financial_actions)
        
        if start_date:
            logs = logs.filter(timestamp__gte=start_date)
        if end_date:
            logs = logs.filter(timestamp__lte=end_date)
        
        return logs
    



    # Add this to gym_app/models.py (at the end, before the last line)

class Attendance(models.Model):
    """Track member check-ins and check-outs"""
    
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='attendances'
    )
    check_in = models.DateTimeField(auto_now_add=True)
    check_out = models.DateTimeField(null=True, blank=True)
    duration_minutes = models.IntegerField(null=True, blank=True)
    notes = models.TextField(blank=True, null=True)
    
    class Meta:
        db_table = 'attendance'
        verbose_name = 'Attendance'
        verbose_name_plural = 'Attendance Records'
        ordering = ['-check_in']
        indexes = [
            models.Index(fields=['-check_in']),
            models.Index(fields=['user', '-check_in']),
        ]
    
    def __str__(self):
        return f"{self.user.get_full_name()} - {self.check_in.strftime('%Y-%m-%d %H:%M')}"
    
    def save(self, *args, **kwargs):
        """Calculate duration if check_out is set"""
        if self.check_out and self.check_in:
            delta = self.check_out - self.check_in
            self.duration_minutes = int(delta.total_seconds() / 60)
        super().save(*args, **kwargs)
    
    def is_checked_in(self):
        """Check if user is currently checked in"""
        return self.check_out is None
    
    def get_duration_display(self):
        """Get human-readable duration"""
        if not self.duration_minutes:
            return "In progress"
        
        hours = self.duration_minutes // 60
        minutes = self.duration_minutes % 60
        
        if hours > 0:
            return f"{hours}h {minutes}m"
        return f"{minutes}m"