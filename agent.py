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

    def process_input(self, user_input: str, user_role: str = "guest", user_name: str = "Guest") -> str:
        if not self.model:
            return "⚠️ AI Agent is offline (Missing API Key). Please configure GEMINI_API_KEY."

        # 1. Gather Context
        today = date.today()
        tomorrow = today + timedelta(days=1)
        
        # Basic availability check for context (simplified)
        available_rooms = self.system.check_availability(today, tomorrow)
        room_context = "\n".join([f"- {r.type.value} Room: ₹{r.price_per_night}" for r in available_rooms[:5]])
        
        # 2. Construct Prompt
        prompt = f"""
        You are the concierge at a luxury hotel.
        Current Date: {today}
        User: {user_name} ({user_role})
        
        Available Rooms for Tonight:
        {room_context}
        
        Hotel Info:
        - Check-in: 2 PM, Check-out: 11 AM
        - Amenities: Pool, Gym, Spa, Free Wi-Fi
        - Prices are in INR (₹).
        
        User Query: "{user_input}"
        
        Instructions:
        - Be polite, professional, and helpful.
        - If the user asks to book, guide them to use the booking form on the right.
        - Keep responses concise (max 3 sentences).
        - If you don't know, say so politely.
        """
        
        # 3. Call LLM
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"I apologize, I'm having trouble connecting to my brain right now. ({str(e)})"

    def _handle_staff_intent(self, text: str) -> str:
        # Deprecated, now handled by LLM or specific tools if we add function calling later
        return "Staff mode is currently being upgraded."
