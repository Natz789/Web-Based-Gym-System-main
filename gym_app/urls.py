# Replace gym_app/urls.py with this:

from django.urls import path
from . import views

urlpatterns = [
    # Public pages
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    
    # Authentication
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Dashboard (role-based)
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # Membership management
    path('plans/', views.membership_plans_view, name='membership_plans'),
    path('plans/subscribe/<int:plan_id>/', views.subscribe_plan, name='subscribe_plan'),
    
    # Walk-in management (staff/admin)
    path('walkin/', views.walkin_purchase, name='walkin_purchase'),
    path('walkin/confirm/', views.walkin_confirm, name='walkin_confirm'),
    
    # Reports & Analytics (admin)
    path('reports/', views.reports_view, name='reports'),
    path('audit-trail/', views.audit_trail_view, name='audit_trail'),
    path('manage-plans/', views.manage_plans_view, name='manage_plans'),
    
    # Member management (admin/staff)
    path('members/', views.members_list, name='members_list'),
    path('members/<int:user_id>/', views.member_detail, name='member_detail'),
    path('create-staff/', views.create_staff_view, name='create_staff'),
    
    # Kiosk (no authentication required)
    path('kiosk/', views.kiosk_login, name='kiosk_login'),
    path('kiosk/success/<str:action>/<int:duration>/<int:user_id>/', views.kiosk_success, name='kiosk_success'),
    
    # Attendance reports (staff/admin)
    path('attendance/', views.attendance_report, name='attendance_report'),
    
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
    path('api/chatbot/suggestions/', views.chatbot_suggestions, name='chatbot_suggestions'),
]