"""
AI Chatbot Engine for Rhose Gym
Uses Ollama with llama3.2:3b model for 8GB RAM optimization
"""

import ollama
from django.conf import settings
from .models import User, MembershipPlan, FlexibleAccess, UserMembership, Payment, Attendance
from datetime import date, timedelta
import json


class GymChatbot:
    """AI-powered chatbot for gym assistance"""
    
    def __init__(self, user=None):
        self.user = user
        self.model = self.model = "llama3.2:1b"
  # Optimized for 8GB RAM
        self.conversation_history = []
        
    def get_system_context(self):
        """Generate system context based on user role and gym data"""
        
        # Base gym information
        context = """You are FitBot, an AI assistant for Rhose Gym, a modern fitness center. 
Your role is to help members, staff, and admins with:
1. Gym membership information and management
2. Fitness and workout advice
3. Gym policies and procedures
4. Equipment usage and safety
5. Nutrition and health tips

Always be friendly, professional, and encouraging. When discussing the gym system, use the data provided.
"""
        
        # Add gym data context
        active_plans = MembershipPlan.objects.filter(is_active=True)
        if active_plans.exists():
            context += "\n\nAVAILABLE MEMBERSHIP PLANS:\n"
            for plan in active_plans:
                context += f"- {plan.name}: ₱{plan.price} for {plan.duration_days} days\n"
                if plan.description:
                    context += f"  Description: {plan.description}\n"
        
        walk_in_passes = FlexibleAccess.objects.filter(is_active=True)
        if walk_in_passes.exists():
            context += "\n\nWALK-IN PASSES:\n"
            for pass_obj in walk_in_passes:
                context += f"- {pass_obj.name}: ₱{pass_obj.price} for {pass_obj.duration_days} day(s)\n"
        
        # Add user-specific context
        if self.user and self.user.is_authenticated:
            context += f"\n\nCURRENT USER: {self.user.get_full_name()} ({self.user.role})\n"
            
            if self.user.role == 'member':
                # Get member's active membership
                active_membership = UserMembership.objects.filter(
                    user=self.user,
                    status='active',
                    end_date__gte=date.today()
                ).first()
                
                if active_membership:
                    context += f"Active Membership: {active_membership.plan.name}\n"
                    context += f"Days Remaining: {active_membership.days_remaining()}\n"
                    context += f"Expires: {active_membership.end_date}\n"
                    
                    # Get kiosk PIN
                    if self.user.kiosk_pin:
                        context += f"Kiosk PIN: {self.user.kiosk_pin}\n"
                else:
                    context += "No active membership\n"
                
                # Get recent attendance
                recent_attendance = Attendance.objects.filter(
                    user=self.user
                ).order_by('-check_in')[:5]
                
                if recent_attendance.exists():
                    context += f"\nRECENT GYM VISITS: {recent_attendance.count()} visits logged\n"
            
            elif self.user.role in ['admin', 'staff']:
                # Get today's stats for staff/admin
                today = date.today()
                today_checkins = Attendance.objects.filter(
                    check_in__date=today
                ).count()
                currently_in = Attendance.objects.filter(
                    check_out__isnull=True
                ).count()
                
                context += f"\nTODAY'S STATS:\n"
                context += f"- Check-ins today: {today_checkins}\n"
                context += f"- Currently in gym: {currently_in}\n"
        
        context += "\n\nGYM FACILITIES:\n"
        context += "- Cardio equipment (treadmills, bikes, ellipticals)\n"
        context += "- Strength training (free weights, machines)\n"
        context += "- Group fitness classes\n"
        context += "- Locker rooms and showers\n"
        
        context += "\n\nGYM POLICIES:\n"
        context += "- Members must check in/out using kiosk PIN\n"
        context += "- Proper gym attire required\n"
        context += "- Clean equipment after use\n"
        context += "- Memberships expire on end date\n"
        
        return context
    
    def get_fitness_knowledge(self):
        """General fitness and gym culture knowledge"""
        return """
WORKOUT TIPS:
- Warm up 5-10 minutes before exercise
- Progressive overload: gradually increase weight/reps
- Rest 48 hours between training same muscle groups
- Mix cardio and strength training
- Stay hydrated (drink water before, during, after)

BEGINNER ROUTINE (3 days/week):
- Day 1: Upper body (push-ups, rows, shoulder press)
- Day 2: Lower body (squats, lunges, leg press)
- Day 3: Full body circuit with cardio

NUTRITION BASICS:
- Protein: 1.6-2.2g per kg body weight for muscle building
- Eat whole foods, avoid processed foods
- Pre-workout: carbs + protein 1-2 hours before
- Post-workout: protein within 30-60 minutes
- Stay hydrated: 2-3 liters water daily

GYM ETIQUETTE:
- Wipe down equipment after use
- Re-rack weights properly
- Share equipment, don't hog machines
- Use headphones for music
- Respect personal space

COMMON MISTAKES:
- Skipping warm-up and cool-down
- Poor form (risking injury)
- Not tracking progress
- Inconsistent training
- Overtraining without rest
"""
    
    def chat(self, user_message, conversation_id=None):
        """
        Process user message and generate AI response
        """
        
        # Build full context
        system_context = self.get_system_context()
        fitness_knowledge = self.get_fitness_knowledge()
        
        # Prepare messages for Ollama
        messages = [
            {
                "role": "system",
                "content": system_context + fitness_knowledge
            }
        ]
        
        # Add conversation history (keep last 6 messages for context)
        if len(self.conversation_history) > 0:
            messages.extend(self.conversation_history[-6:])
        
        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })
        
        try:
            # Call Ollama API
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    "temperature": 0.7,  # Balanced creativity
                    "top_p": 0.9,
                    "num_predict": 512,  # Max tokens (shorter for speed)
                }
            )
            
            assistant_message = response['message']['content']
            
            # Update conversation history
            self.conversation_history.append({
                "role": "user",
                "content": user_message
            })
            self.conversation_history.append({
                "role": "assistant",
                "content": assistant_message
            })
            
            return {
                "success": True,
                "response": assistant_message,
                "conversation_id": conversation_id
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": f"Chatbot error: {str(e)}",
                "response": "I'm having trouble connecting right now. Please make sure Ollama is running with: ollama serve"
            }
    
    def get_quick_suggestions(self):
        """Get context-aware quick reply suggestions"""
        suggestions = []
        
        if self.user and self.user.is_authenticated:
            if self.user.role == 'member':
                suggestions = [
                    "What's my membership status?",
                    "How do I check in at the gym?",
                    "Give me a beginner workout plan",
                    "What are your membership plans?",
                    "Nutrition tips for muscle gain"
                ]
            elif self.user.role in ['admin', 'staff']:
                suggestions = [
                    "How many people are in the gym?",
                    "Today's check-in statistics",
                    "How to process walk-in sales?",
                    "Best practices for gym management",
                    "How to renew member subscriptions?"
                ]
        else:
            suggestions = [
                "What membership plans do you offer?",
                "How much are walk-in passes?",
                "What equipment do you have?",
                "Tips for starting at the gym",
                "How do I sign up?"
            ]
        
        return suggestions


def get_database_context(query):
    """
    Query-specific database context retrieval
    """
    query_lower = query.lower()
    context = {}
    
    # Membership-related queries
    if any(word in query_lower for word in ['membership', 'plan', 'price', 'cost', 'subscribe']):
        plans = MembershipPlan.objects.filter(is_active=True)
        context['plans'] = [
            {
                'name': p.name,
                'price': float(p.price),
                'days': p.duration_days,
                'description': p.description
            } for p in plans
        ]
    
    # Walk-in queries
    if any(word in query_lower for word in ['walk-in', 'day pass', 'visitor', 'guest']):
        passes = FlexibleAccess.objects.filter(is_active=True)
        context['passes'] = [
            {
                'name': p.name,
                'price': float(p.price),
                'days': p.duration_days
            } for p in passes
        ]
    
    # Statistics queries
    if any(word in query_lower for word in ['stats', 'statistics', 'how many', 'count']):
        context['stats'] = {
            'total_members': User.objects.filter(role='member').count(),
            'active_memberships': UserMembership.objects.filter(
                status='active',
                end_date__gte=date.today()
            ).count(),
            'checked_in_now': Attendance.objects.filter(
                check_out__isnull=True
            ).count()
        }
    
    return context