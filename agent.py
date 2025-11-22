from datetime import date, datetime, timedelta
from typing import Optional
from system import HotelSystem
from models import GuestType, RoomType

class HospitalityAI:
    def __init__(self, system: HotelSystem):
        self.system = system
        self.context = {} # Simple context memory

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
        user_input = user_input.lower()
        
        if user_role == "staff":
            return self._handle_staff_intent(user_input)
        else:
            return self._handle_guest_intent(user_input, user_name)

    def _handle_guest_intent(self, text: str, user_name: str) -> str:
        # 1. Booking Intent
        if "book" in text or "reservation" in text or "room" in text:
            # Simple extraction logic
            check_in = self.parse_date("tomorrow") # Default
            check_out = check_in + timedelta(days=1)
            
            # Check availability
            available = self.system.check_availability(check_in, check_out)
            if not available:
                return "I apologize, but we don't have any rooms available for those dates."
            
            # Suggest rooms (Upselling)
            response = f"Certainly, {user_name}! For tomorrow, we have the following availability:\n"
            for room in available:
                response += f"- {room.type.value} Room at ₹{room.price_per_night}/night\n"
            
            response += "\nWould you like to proceed with a booking? I can recommend the Suite for a truly luxurious experience."
            return response

        # 2. Info Intent
        if "amenities" in text or "pool" in text or "wifi" in text:
            return "We offer free high-speed Wi-Fi, a 24/7 fitness center, and a rooftop infinity pool open from 6 AM to 10 PM."

        # Default
        return f"Welcome to our hotel, {user_name}. How may I assist you today? I can help with reservations, amenities, or local recommendations."

    def _handle_staff_intent(self, text: str) -> str:
        if "checkout" in text or "departing" in text:
            today = date.today()
            checkouts = self.system.get_checkouts(today)
            if not checkouts:
                return "There are no scheduled checkouts for today."
            return f"Found {len(checkouts)} checkouts for today. Would you like the detailed list?"
        
        if "status" in text or "occupancy" in text:
            occupied, total = self.system.get_room_stats()
            return f"Current Occupancy: {occupied}/{total} rooms."

        return "Staff Mode Active. Ready for operational commands (e.g., 'checkouts today', 'occupancy status')."
