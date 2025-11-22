import os
import google.generativeai as genai
from datetime import date, datetime, timedelta
from typing import Optional
from system import HotelSystem
from models import RoomType

class HospitalityAI:
    def __init__(self, system: HotelSystem, api_key: Optional[str] = None):
        self.system = system
        self.api_key = api_key
        if self.api_key:
            try:
                genai.configure(api_key=self.api_key)
                # Use gemini-1.5-flash (works with free Google AI Studio keys)
                self.model = genai.GenerativeModel('gemini-1.5-flash')
            except Exception as e:
                print(f"AI Model initialization error: {e}")
                self.model = None
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
        # Temporarily disabled due to API compatibility issues
        return """👋 Hello! I'm your AI concierge assistant.

I'm currently experiencing some technical difficulties with my AI brain, but I'm still here to help!

In the meantime, you can:
✅ **Browse available rooms** using the booking form on the right
✅ **Check room prices** - Standard (₹800), Deluxe (₹1200), Suite (₹2000)
✅ **Make reservations** for your stay
✅ **View hotel amenities** - Pool, Spa, Gym, Restaurant

For complex questions, please contact our front desk directly. We're working on restoring full AI functionality soon! 🏨"""

    def _handle_staff_intent(self, text: str) -> str:
        # Deprecated, now handled by LLM or specific tools if we add function calling later
        return "Staff mode is currently being upgraded."
