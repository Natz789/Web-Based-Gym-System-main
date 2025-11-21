"""
Enhanced AI Chatbot Engine for Rhose Gym
Supports dynamic model switching, conversation persistence, and streaming responses
Optimized for E595 ThinkPad (8-16GB RAM)
Performance optimized with caching for faster response times
"""

import ollama
import uuid
import time
from django.conf import settings
from django.core.cache import cache
from .models import (
    User, MembershipPlan, FlexibleAccess, UserMembership, Payment, Attendance,
    ChatbotConfig, Conversation, ConversationMessage
)
from datetime import date, timedelta
import json


class GymChatbot:
    """AI-powered chatbot for gym assistance with dynamic configuration"""

    def __init__(self, user=None, conversation_id=None, session_key=None):
        self.user = user
        self.session_key = session_key
        self.config = ChatbotConfig.get_config()
        self.model = self.config.active_model
        self.conversation = None
        self.conversation_history = []

        # Load or create conversation
        if conversation_id:
            self._load_conversation(conversation_id)
        elif self.config.enable_persistence:
            self._create_conversation()

    def _load_conversation(self, conversation_id):
        """Load existing conversation from database"""
        try:
            if self.user and self.user.is_authenticated:
                self.conversation = Conversation.objects.get(
                    conversation_id=conversation_id,
                    user=self.user
                )
            else:
                self.conversation = Conversation.objects.get(
                    conversation_id=conversation_id,
                    session_key=self.session_key
                )

            # Load message history
            messages = self.conversation.messages.all()
            for msg in messages:
                if msg.role != 'system':  # Skip system messages
                    self.conversation_history.append({
                        'role': msg.role,
                        'content': msg.content
                    })
        except Conversation.DoesNotExist:
            self._create_conversation()

    def _create_conversation(self):
        """Create a new conversation"""
        conversation_id = str(uuid.uuid4())
        self.conversation = Conversation.objects.create(
            user=self.user if self.user and self.user.is_authenticated else None,
            conversation_id=conversation_id,
            model_used=self.model,
            session_key=self.session_key if not (self.user and self.user.is_authenticated) else None
        )

    def _save_message(self, role, content, response_time_ms=None):
        """Save message to database if persistence is enabled"""
        if self.config.enable_persistence and self.conversation:
            ConversationMessage.objects.create(
                conversation=self.conversation,
                role=role,
                content=content,
                response_time_ms=response_time_ms
            )

            # Generate title from first user message
            if role == 'user' and not self.conversation.title:
                self.conversation.generate_title()

    @staticmethod
    def _get_static_base_context():
        """
        Get cached static base context that rarely changes.
        Cached for 1 hour to improve performance.
        """
        cache_key = 'chatbot_static_base_context'
        cached_context = cache.get(cache_key)

        if cached_context:
            return cached_context

        # Base gym information (static)
        context = """You are FitBot, an AI customer service assistant for Rhose Gym, a modern fitness center.
Your primary role is to provide excellent customer service and answer frequently asked questions about:

1. MEMBERSHIPS & PRICING
   - Explain membership plans, pricing, and benefits
   - Help members understand their subscription status and expiration dates
   - Guide users through the membership purchase process
   - Explain walk-in passes and day passes

2. PAYMENTS & TRANSACTIONS
   - Answer questions about payment methods (Cash, GCash)
   - Explain payment status and history
   - Help with pending payments and payment confirmation
   - Provide information about payment references and receipts

3. CUSTOMER SERVICE & SUPPORT
   - Answer common questions about gym policies
   - Assist with account-related inquiries
   - Help troubleshoot common issues
   - Guide users on how to use the kiosk system
   - Provide information about gym hours and facilities

4. GYM FACILITIES & USAGE
   - Explain available equipment and facilities
   - Provide basic workout guidance
   - Share gym etiquette and safety rules

Always be friendly, professional, helpful, and empathetic. Prioritize customer satisfaction.
Keep your responses concise, clear, and action-oriented. When discussing the gym system, use the data provided.
If you don't know something specific, politely direct the user to contact the gym staff directly.
"""

        # Add static gym information
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

        context += "\n\nCOMMON FAQS - QUICK ANSWERS:\n"
        context += "Q: How do I pay for membership?\n"
        context += "A: We accept Cash and GCash. You can subscribe to a plan from the Membership Plans page.\n\n"
        context += "Q: How do I check my payment history?\n"
        context += "A: Login to your dashboard to view your complete payment history and transaction details.\n\n"
        context += "Q: What if my payment is pending?\n"
        context += "A: Pending payments need to be confirmed by staff. Check your dashboard or contact us for status.\n\n"
        context += "Q: How do I use my kiosk PIN?\n"
        context += "A: Enter your 6-digit PIN at the kiosk to check in when you arrive and check out when you leave.\n\n"
        context += "Q: Can I renew my membership?\n"
        context += "A: Yes! You can purchase a new membership plan from the Membership Plans page before or after your current one expires.\n\n"
        context += "Q: What's the difference between membership and walk-in pass?\n"
        context += "A: Memberships provide longer-term access (30-365 days), while walk-in passes are for single-day or short-term visits.\n\n"
        context += "Q: How do I register for the gym?\n"
        context += "A: Click 'Join Now' or 'Register' on the homepage, fill out your details, choose a membership plan, and complete payment.\n\n"

        # Cache for 1 hour
        cache.set(cache_key, context, 3600)
        return context

    @staticmethod
    def _get_cached_membership_plans():
        """Get cached membership plans. Cached for 10 minutes."""
        cache_key = 'chatbot_membership_plans'
        cached_plans = cache.get(cache_key)

        if cached_plans:
            return cached_plans

        active_plans = MembershipPlan.objects.filter(is_active=True)
        plans_text = ""

        if active_plans.exists():
            plans_text = "\n\nAVAILABLE MEMBERSHIP PLANS:\n"
            for plan in active_plans:
                plans_text += f"- {plan.name}: ₱{plan.price} for {plan.duration_days} days\n"
                if plan.description:
                    plans_text += f"  Description: {plan.description}\n"

        # Cache for 10 minutes
        cache.set(cache_key, plans_text, 600)
        return plans_text

    @staticmethod
    def _get_cached_walkin_passes():
        """Get cached walk-in passes. Cached for 10 minutes."""
        cache_key = 'chatbot_walkin_passes'
        cached_passes = cache.get(cache_key)

        if cached_passes:
            return cached_passes

        walk_in_passes = FlexibleAccess.objects.filter(is_active=True)
        passes_text = ""

        if walk_in_passes.exists():
            passes_text = "\n\nWALK-IN PASSES:\n"
            for pass_obj in walk_in_passes:
                passes_text += f"- {pass_obj.name}: ₱{pass_obj.price} for {pass_obj.duration_days} day(s)\n"

        # Cache for 10 minutes
        cache.set(cache_key, passes_text, 600)
        return passes_text

    def get_system_context(self):
        """
        Generate system context based on user role and gym data.
        Optimized with caching for faster performance.
        """
        # Start with cached static base context
        context = self._get_static_base_context()

        # Add cached membership plans and walk-in passes
        context += self._get_cached_membership_plans()
        context += self._get_cached_walkin_passes()

        # Add user-specific context (not cached as it's frequently changing)
        if self.user and self.user.is_authenticated:
            context += f"\n\nCURRENT USER: {self.user.get_full_name()} ({self.user.role})\n"

            if self.user.role == 'member':
                # Get member's active membership with optimized query
                active_membership = UserMembership.objects.filter(
                    user=self.user,
                    status='active',
                    end_date__gte=date.today()
                ).select_related('plan').first()

                if active_membership:
                    context += f"Active Membership: {active_membership.plan.name}\n"
                    context += f"Days Remaining: {active_membership.days_remaining()}\n"
                    context += f"Expires: {active_membership.end_date}\n"

                    # Get kiosk PIN
                    if self.user.kiosk_pin:
                        context += f"Kiosk PIN: {self.user.kiosk_pin}\n"
                else:
                    context += "No active membership\n"

                # Get recent attendance count (optimized - only count, no full data)
                recent_count = Attendance.objects.filter(
                    user=self.user
                ).count()

                if recent_count > 0:
                    context += f"\nRECENT GYM VISITS: {recent_count} visits logged\n"

            elif self.user.role in ['admin', 'staff']:
                # Cache staff stats for 2 minutes (frequently accessed)
                cache_key = f'chatbot_staff_stats_{date.today()}'
                cached_stats = cache.get(cache_key)

                if cached_stats:
                    context += cached_stats
                else:
                    # Get today's stats for staff/admin
                    today = date.today()
                    today_checkins = Attendance.objects.filter(
                        check_in__date=today
                    ).count()
                    currently_in = Attendance.objects.filter(
                        check_out__isnull=True
                    ).count()

                    stats_text = f"\nTODAY'S STATS:\n"
                    stats_text += f"- Check-ins today: {today_checkins}\n"
                    stats_text += f"- Currently in gym: {currently_in}\n"

                    # Cache for 2 minutes
                    cache.set(cache_key, stats_text, 120)
                    context += stats_text

        return context

    @staticmethod
    def get_fitness_knowledge():
        """
        General fitness and gym culture knowledge.
        Cached for 1 hour as it's completely static.
        """
        cache_key = 'chatbot_fitness_knowledge'
        cached_knowledge = cache.get(cache_key)

        if cached_knowledge:
            return cached_knowledge

        knowledge = """
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
        # Cache for 1 hour
        cache.set(cache_key, knowledge, 3600)
        return knowledge

    def chat(self, user_message):
        """
        Process user message and generate AI response
        """
        start_time = time.time()

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

        # Add conversation history (keep last N messages based on config)
        context_window = self.config.context_window
        if len(self.conversation_history) > 0:
            messages.extend(self.conversation_history[-context_window:])

        # Add current user message
        messages.append({
            "role": "user",
            "content": user_message
        })

        try:
            # Call Ollama API with configured settings
            ollama_options = self.config.get_ollama_options()

            if self.config.enable_streaming:
                # Streaming response (for future frontend implementation)
                return self._chat_stream(messages, user_message, start_time)
            else:
                # Standard response
                response = ollama.chat(
                    model=self.model,
                    messages=messages,
                    options=ollama_options
                )

                assistant_message = response['message']['content']

                # Calculate response time
                response_time_ms = int((time.time() - start_time) * 1000)

                # Update conversation history
                self.conversation_history.append({
                    "role": "user",
                    "content": user_message
                })
                self.conversation_history.append({
                    "role": "assistant",
                    "content": assistant_message
                })

                # Save messages to database
                self._save_message("user", user_message)
                self._save_message("assistant", assistant_message, response_time_ms)

                return {
                    "success": True,
                    "response": assistant_message,
                    "conversation_id": self.conversation.conversation_id if self.conversation else None,
                    "model": self.model,
                    "response_time_ms": response_time_ms
                }

        except Exception as e:
            error_msg = str(e)
            if "connection" in error_msg.lower():
                friendly_error = f"Cannot connect to Ollama. Please ensure:\n1. Ollama is installed\n2. Run 'ollama serve' in terminal\n3. Model '{self.model}' is pulled: 'ollama pull {self.model}'"
            else:
                friendly_error = f"Chatbot error: {error_msg}"

            return {
                "success": False,
                "error": friendly_error,
                "response": "I'm having trouble connecting right now. Please check that Ollama is running and the model is available."
            }

    def _chat_stream(self, messages, user_message, start_time):
        """Handle streaming responses (for future implementation)"""
        # This is a placeholder for streaming support
        # Frontend would need to be updated to handle Server-Sent Events (SSE)
        try:
            full_response = ""
            stream = ollama.chat(
                model=self.model,
                messages=messages,
                options=self.config.get_ollama_options(),
                stream=True
            )

            for chunk in stream:
                if 'message' in chunk and 'content' in chunk['message']:
                    full_response += chunk['message']['content']

            response_time_ms = int((time.time() - start_time) * 1000)

            # Update history
            self.conversation_history.append({"role": "user", "content": user_message})
            self.conversation_history.append({"role": "assistant", "content": full_response})

            # Save to database
            self._save_message("user", user_message)
            self._save_message("assistant", full_response, response_time_ms)

            return {
                "success": True,
                "response": full_response,
                "conversation_id": self.conversation.conversation_id if self.conversation else None,
                "model": self.model,
                "response_time_ms": response_time_ms,
                "streaming": True
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "response": "Streaming error occurred."
            }

    def get_quick_suggestions(self):
        """Get context-aware quick reply suggestions"""
        suggestions = []

        if self.user and self.user.is_authenticated:
            if self.user.role == 'member':
                suggestions = [
                    "What's my membership status?",
                    "How do I check my payment history?",
                    "How do I use my kiosk PIN?",
                    "How can I renew my membership?",
                    "What payment methods are accepted?",
                    "What are the gym hours?"
                ]
            elif self.user.role in ['admin', 'staff']:
                suggestions = [
                    "How many people are in the gym?",
                    "Today's check-in statistics",
                    "How to process walk-in sales?",
                    "How to confirm pending payments?",
                    "Common member questions"
                ]
        else:
            suggestions = [
                "What membership plans do you offer?",
                "How much are walk-in passes?",
                "How do I register for the gym?",
                "What payment methods do you accept?",
                "How do I check in at the gym?",
                "What's the difference between membership and walk-in pass?"
            ]

        return suggestions

    @staticmethod
    def get_available_models():
        """Get list of available Ollama models on the system"""
        try:
            models = ollama.list()
            available = []
            for model in models.get('models', []):
                model_name = model.get('name', '')
                if model_name:
                    available.append(model_name)
            return available
        except Exception as e:
            return []

    @staticmethod
    def check_ollama_status():
        """Check if Ollama service is running"""
        try:
            ollama.list()
            return {
                "status": "running",
                "message": "Ollama is running successfully"
            }
        except Exception as e:
            return {
                "status": "error",
                "message": f"Ollama is not running: {str(e)}"
            }

    @staticmethod
    def clear_cache():
        """
        Clear all chatbot-related cache.
        Should be called when gym data (plans, passes) is updated.
        """
        cache_keys = [
            'chatbot_static_base_context',
            'chatbot_membership_plans',
            'chatbot_walkin_passes',
            'chatbot_fitness_knowledge',
        ]

        for key in cache_keys:
            cache.delete(key)

        # Clear staff stats cache (varies by date)
        # This is a wildcard delete - in production, use cache.delete_pattern if available
        today = date.today()
        cache.delete(f'chatbot_staff_stats_{today}')


# Legacy compatibility function
def get_database_context(query):
    """
    Query-specific database context retrieval
    (Maintained for backward compatibility)
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
