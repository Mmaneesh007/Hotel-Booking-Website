import os
import google.generativeai as genai
from datetime import date, timedelta
from typing import Optional
from system import HotelSystem
from models import RoomType

class HospitalityAI:
    def __init__(self, system: HotelSystem, api_key: Optional[str] = None):
        self.system = system
        self.api_key = api_key
        if self.api_key:
            genai.configure(api_key=self.api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            self.model = None

    def parse_date(self, date_str: str) -> date:
        # Very basic parser for demo purposes
        today = date.today()
        if "tomorrow" in date_str.lower():
            return today + timedelta(days=1)
        if "today" in date_str.lower():
            return today
        try:
            return datetime.strptime(date_str, "%Y-%m-%d").date()
        except ValueError:
            return today # Fallback

    def process_input(self, user_input: str, history: list = [], user_role: str = "guest", user_name: str = "Guest") -> str:
        if not self.model:
            return "⚠️ AI Agent is offline (Missing API Key). Please configure GEMINI_API_KEY."

        # 1. Gather Context
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        # Basic availability check for context
        available_rooms = self.system.check_availability(today, tomorrow)
        room_context = "\n".join([f"- {r.type.value}: ₹{r.price_per_night}/night" for r in available_rooms[:5]])
        
        # 2. Format History for Context
        conversation_history = "\n".join([f"{msg['role']}: {msg['content']}" for msg in history[-10:]]) # Last 10 messages

        # 3. Construct Conversational Prompt
        prompt = f"""You are an expert hotel concierge at a luxury 5-star hotel. You are warm, professional, and genuinely helpful.

CURRENT CONTEXT:
- Date: {today.strftime('%B %d, %Y')}
- Guest: {user_name}
- Role: {user_role}

HOTEL INFORMATION:
- Room Types Available Tonight:
{room_context if room_context else "  (Checking availability...)"}

- Check-in: 2:00 PM
- Check-out: 11:00 AM
- Amenities: 
  • Rooftop infinity pool (6 AM - 10 PM)
  • 24/7 fitness center with personal trainers
  • Full-service spa
  • Fine dining restaurant
  • Free high-speed Wi-Fi throughout
  • Business center
  • Concierge services

CONVERSATION HISTORY:
{conversation_history if conversation_history else "(New conversation)"}

GUEST'S QUESTION:
"{user_input}"

YOUR ROLE:
- Be conversational and natural, like a real person
- Remember details from the conversation history
- Provide thoughtful, complete answers
- If asked about booking, guide them to use the booking form on the right side
- Suggest upgrades or add-ons when relevant (spa packages, room service, etc.)
- Answer questions about local attractions, restaurants, or activities
- Be proactive in anticipating guest needs

IMPORTANT: Respond naturally. Don't limit yourself to short answers. Be helpful and engaging, just like ChatGPT would be.
"""
        
        # 4. Call LLM
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, I'm having trouble connecting right now. Please try again in a moment. (Error: {str(e)})"

    def _handle_staff_intent(self, text: str) -> str:
        # Deprecated, now handled by LLM or specific tools if we add function calling later
        return "Staff mode is currently being upgraded."
