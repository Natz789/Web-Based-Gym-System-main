# AI Chatbot Setup & Configuration Guide

## Overview

Your gym management system now includes an enhanced AI chatbot powered by Ollama with the following improvements:

### New Features
✅ **Dynamic Model Switching** - Switch between different Ollama models optimized for your E595 ThinkPad
✅ **Conversation Persistence** - All chat history is saved to the database
✅ **Streaming Support** - Option to enable word-by-word response streaming
✅ **Admin Configuration Panel** - Web interface to manage chatbot settings
✅ **Model Management API** - REST endpoints to manage models and settings
✅ **Performance Tracking** - Track response times and token usage

## Setup Instructions

### 1. Install Ollama

First, install Ollama on your E595 ThinkPad:

```bash
# Linux installation
curl -fsSL https://ollama.com/install.sh | sh

# Start Ollama service
ollama serve
```

### 2. Pull Recommended Models

For your E595 ThinkPad (8-16GB RAM), pull these recommended models:

```bash
# Fastest - Best for 8GB RAM
ollama pull llama3.2:1b

# Balanced - Good for 12GB RAM
ollama pull llama3.2:3b

# Alternative - Fast and efficient
ollama pull gemma2:2b

# Optional - If you have 16GB RAM
ollama pull mistral:7b
```

### 3. Apply Database Migrations

Run these commands to create the new database tables:

```bash
# Activate your virtual environment first (if using one)
source venv/bin/activate  # or 'venv\Scripts\activate' on Windows

# Create migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate
```

### 4. Create Initial Configuration

After migrating, the chatbot configuration will be automatically created with default settings.

### 5. Configure the Chatbot

**Option 1: Django Admin Interface**
1. Log in to Django admin: http://localhost:8000/admin
2. Navigate to "Chatbot Configuration"
3. Adjust settings as needed

**Option 2: Web Configuration Page (Recommended)**
1. Log in as admin
2. Visit: http://localhost:8000/chatbot/config/
3. Configure your preferred model and settings

## Recommended Settings for E595 ThinkPad

### For 8GB RAM:
```
Model: llama3.2:1b or gemma2:2b
Temperature: 0.7
Max Tokens: 512
Context Window: 6
```

### For 12GB RAM:
```
Model: llama3.2:3b
Temperature: 0.7
Max Tokens: 512
Context Window: 8
```

### For 16GB RAM:
```
Model: mistral:7b
Temperature: 0.7
Max Tokens: 768
Context Window: 10
```

## Model Comparison

| Model | RAM Required | Speed | Quality | Best For |
|-------|-------------|-------|---------|----------|
| llama3.2:1b | 8GB | ⚡⚡⚡ | ⭐⭐ | Quick responses, low RAM |
| gemma2:2b | 8GB | ⚡⚡⚡ | ⭐⭐⭐ | Balanced performance |
| llama3.2:3b | 12GB | ⚡⚡ | ⭐⭐⭐⭐ | Best balance |
| phi3:3.8b | 12GB | ⚡⚡ | ⭐⭐⭐⭐ | Efficient and accurate |
| mistral:7b | 16GB | ⚡ | ⭐⭐⭐⭐⭐ | Highest quality |

## New API Endpoints

### Chat API
```
POST /api/chatbot/
Body: {
  "message": "User message",
  "conversation_id": "optional-uuid"
}
```

### Configuration Management
```
GET /api/chatbot/models/              - List available models
POST /api/chatbot/models/switch/      - Switch active model
GET /api/chatbot/conversations/       - List conversations
POST /api/chatbot/config/update/      - Update configuration
```

## Admin Pages

- **Chatbot Configuration**: `/chatbot/config/`
- **Django Admin**: `/admin/gym_app/chatbotconfig/`
- **Conversations History**: `/admin/gym_app/conversation/`
- **Message Logs**: `/admin/gym_app/conversationmessage/`

## Troubleshooting

### Ollama Not Running
```bash
# Start Ollama service
ollama serve

# Check if running
curl http://localhost:11434/api/tags
```

### Model Not Found
```bash
# List installed models
ollama list

# Pull missing model
ollama pull llama3.2:1b
```

### Performance Issues
1. Use smaller models (1b or 2b) for faster responses
2. Reduce `max_tokens` to 256-512
3. Reduce `context_window` to 4-6
4. Close other applications to free RAM

### Database Errors
```bash
# Reset migrations if needed
python manage.py migrate gym_app zero
python manage.py migrate
```

## Configuration Parameters

### Temperature (0.0 - 1.0)
- **0.0-0.3**: Very focused, deterministic responses
- **0.4-0.7**: Balanced (recommended)
- **0.8-1.0**: Creative, varied responses

### Top P (0.0 - 1.0)
- Controls response diversity
- **0.9**: Recommended for most use cases

### Max Tokens
- **256**: Very short responses, fastest
- **512**: Standard responses (recommended)
- **1024+**: Long, detailed responses, slower

### Context Window
- Number of previous messages to remember
- **4-6**: Recommended for performance
- **8-12**: Better context understanding
- **Higher**: More RAM usage

## Features

### Conversation Persistence
All conversations are saved to the database with:
- User/anonymous tracking
- Message history
- Response time metrics
- Model used for each conversation

### Role-Based Responses
The chatbot provides contextual responses based on user role:
- **Members**: Membership status, workout advice, check-in info
- **Staff/Admin**: Statistics, operations, management help
- **Anonymous**: General info, plans, facilities

### Quick Suggestions
Context-aware suggestion chips based on user role

## Testing the Chatbot

1. Start Ollama: `ollama serve`
2. Start Django: `python manage.py runserver`
3. Visit: http://localhost:8000/chatbot/
4. Or use the floating chat widget on any page

## Monitoring

Check chatbot performance in Django Admin:
- Response times
- Model usage
- Conversation statistics
- Error logs

## Need Help?

If you encounter issues:
1. Check Ollama is running: `ollama list`
2. Verify model is pulled: `ollama list`
3. Check Django logs for errors
4. Review chatbot configuration in admin

## Updating Models

To update to a newer model version:

```bash
# Pull latest version
ollama pull llama3.2:1b

# Update in admin panel
# Visit /chatbot/config/ and select the new model
```

---

**Optimized for E595 ThinkPad** | Powered by Ollama | Django Integration
