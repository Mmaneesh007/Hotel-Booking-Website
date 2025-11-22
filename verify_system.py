from system import HotelSystem
from agent import HospitalityAI
from models import GuestType

def verify():
    print("Initializing System...")
    system = HotelSystem()
    ai = HospitalityAI(system)
    
    # Helper to print safely on Windows
    def safe_print(text):
        try:
            print(text)
        except UnicodeEncodeError:
            # Replace the problematic symbol for console output
            clean_text = text.replace('\u20b9', 'INR ')
            print(clean_text.encode('ascii', errors='replace').decode('ascii'))

    # Scenario 1: Guest Interaction
    print("\n--- Scenario 1: Guest Booking ---")
    guest_name = "John Doe"
    system.create_guest(guest_name, GuestType.VIP)
    
    input_text = "I want to book a room for tomorrow"
    print(f"Guest Input: {input_text}")
    response = ai.process_input(input_text, user_role="guest", user_name=guest_name)
    safe_print(f"AI Response: {response}")
    
    input_text = "What amenities do you have?"
    print(f"Guest Input: {input_text}")
    response = ai.process_input(input_text, user_role="guest", user_name=guest_name)
    safe_print(f"AI Response: {response}")

    # Scenario 2: Staff Interaction
    print("\n--- Scenario 2: Staff Operations ---")
    input_text = "Show me checkouts for today"
    print(f"Staff Input: {input_text}")
    response = ai.process_input(input_text, user_role="staff")
    safe_print(f"AI Response: {response}")

    input_text = "What is the occupancy status?"
    print(f"Staff Input: {input_text}")
    response = ai.process_input(input_text, user_role="staff")
    safe_print(f"AI Response: {response}")

    # Verify Room Counts
    print("\n--- Verifying Room Counts ---")
    occupied, total = system.get_room_stats()
    print(f"Total Rooms in System: {total}")
    # We can also query directly if we want, but total count is a good proxy for now (8+6+4=18)

if __name__ == "__main__":
    verify()
