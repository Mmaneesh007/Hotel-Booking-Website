import streamlit as st
from datetime import date, timedelta
from system import HotelSystem
from agent import HospitalityAI
from models import RoomType, GuestType

# Initialize System
@st.cache_resource
def get_system():
    return HotelSystem()

system = get_system()
ai = HospitalityAI(system)

st.set_page_config(page_title="HOSPITALITY-AI", page_icon="🏨", layout="wide")

st.title("🏨 HOSPITALITY-AI System")

# Sidebar for Role Selection
role = st.sidebar.selectbox("Select Role", ["Guest", "Staff", "Manager"])

if role == "Guest":
    st.header("Welcome, Guest!")
    
    # Guest Identity
    guest_name = st.sidebar.text_input("Your Name", "John Doe")
    if st.sidebar.button("Login/Register"):
        guest = system.create_guest(guest_name)
        st.sidebar.success(f"Welcome back, {guest.name}!")

    # Chat Interface
    st.subheader("Concierge Chat")
    user_input = st.text_input("Ask me anything (e.g., 'I need a room for tomorrow')")
    if user_input:
        response = ai.process_input(user_input, user_role="guest", user_name=guest_name)
        st.info(response)

    st.markdown("---")
    
    # Direct Booking Form
    st.subheader("Book a Room")
    col1, col2 = st.columns(2)
    with col1:
        check_in = st.date_input("Check-in Date", date.today() + timedelta(days=1))
    with col2:
        check_out = st.date_input("Check-out Date", date.today() + timedelta(days=2))
    
    room_type = st.selectbox("Room Type", [t.value for t in RoomType])
    
    if st.button("Check Availability"):
        available = system.check_availability(check_in, check_out, RoomType(room_type))
        if available:
            st.success(f"Found {len(available)} available {room_type} rooms!")
            for room in available:
                with st.expander(f"Room {room.number} - ₹{room.price_per_night}/night"):
                    # Image Gallery
                    img_col1, img_col2, img_col3 = st.columns(3)
                    
                    # Determine image prefix based on room type
                    img_prefix = "standard"
                    if room.type == RoomType.DELUXE:
                        img_prefix = "deluxe"
                    elif room.type == RoomType.SUITE:
                        img_prefix = "suite"
                        
                    with img_col1:
                        st.image(f"images/{img_prefix}_bedroom.png", caption="Bedroom", use_container_width=True)
                    with img_col2:
                        st.image(f"images/{img_prefix}_washroom.png", caption="Washroom", use_container_width=True)
                    with img_col3:
                        st.image(f"images/{img_prefix}_amenities.png", caption="Amenities", use_container_width=True)

                    st.write(f"Features: {room.features}")
                    if st.button(f"Book Room {room.number}", key=room.id):
                        # Need guest ID
                        guest = system.create_guest(guest_name)
                        res = system.create_reservation(guest.id, room.id, check_in, check_out)
                        st.success(f"Reservation Confirmed! ID: {res.id}")
        else:
            st.error("No rooms available for these dates.")

elif role == "Staff":
    st.header("Staff Operations Dashboard")
    
    # Stats
    occ, total = system.get_room_stats()
    st.metric("Occupancy", f"{occ}/{total}", f"{int(occ/total*100) if total else 0}%")
    
    # Chat for Ops
    st.subheader("Operational Query")
    ops_input = st.text_input("Command (e.g., 'checkouts today')")
    if ops_input:
        response = ai.process_input(ops_input, user_role="staff")
        st.warning(response)
        
    # Reservations List
    st.subheader("All Reservations")
    reservations = system.get_all_reservations()
    if reservations:
        data = []
        for r in reservations:
            data.append({
                "ID": r.id[:8],
                "Guest ID": r.guest_id[:8],
                "Room": r.room_id[:8], # In real app, would join to get number
                "Check-in": r.check_in,
                "Check-out": r.check_out,
                "Status": r.status
            })
        st.dataframe(data)
    else:
        st.info("No reservations found.")

elif role == "Manager":
    st.header("Manager Overview")
    st.write("Analytics and Reporting modules coming soon.")
