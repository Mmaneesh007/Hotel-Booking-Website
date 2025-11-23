@st.cache_resource(ttl=3600)  # Refresh cache every hour
def get_system():
    db_url = st.secrets.get("DATABASE_URL")
    try:
        return HotelSystem(db_url=db_url)
    except Exception as e:
        st.error(f"🚨 Database Connection Error: {e}")
        st.stop()

system = get_system()

# Initialize AI
api_key = st.secrets.get("GEMINI_API_KEY")
ai = HospitalityAI(system, api_key=api_key)

# Initialize Session State for Chat
if "messages" not in st.session_state:
    st.session_state.messages = []

# --- CUSTOM CSS (PREMIUM UI) ---
st.markdown("""
<style>
    /* Import Google Font */
    @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Inter:wght@300;400;600&display=swap');

    /* Global Styles */
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3 {
        font-family: 'Playfair Display', serif;
        color: #1E293B;
    }
    
    /* Hero Section */
    .hero-container {
        background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%);
        padding: 4rem 2rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .hero-title {
        font-size: 3.5rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #F8F9FA;
    }
    .hero-subtitle {
        font-size: 1.2rem;
        font-weight: 300;
        opacity: 0.9;
    }

    /* Buttons */
    .stButton > button {
        background-color: #C5A059; /* Gold */
        color: white;
        border-radius: 30px;
        border: none;
        padding: 0.5rem 2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }
    .stButton > button:hover {
        background-color: #B08D48;
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(197, 160, 89, 0.4);
    }

    /* Chat Interface */
    .stChatMessage {
        background-color: #F8F9FA;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 2px 5px rgba(0,0,0,0.05);
    }
    
    .stChatMessage p, .stChatMessage div, .stChatMessage span {
        color: #000000 !important;
    }
    
    /* Chat Input - Black text on light input */
    .stChatInput input {
        color: #000000 !important;
        background-color: #FFFFFF !important;
    }
    
    /* All Text Inputs - Black text */
    input, textarea {
        color: #000000 !important;
    }
    
    .stTextInput input, .stTextArea textarea {
        color: #000000 !important;
    }
    
    /* Placeholder text */
    input::placeholder, textarea::placeholder {
        color: #666666 !important;
    }
</style>
""", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/201/201623.png", width=80)
    st.title("HOSPITALITY-AI")
    st.markdown("---")
    
    # Check if user is logged in
    from auth import AuthManager
    
    # Auto-login from cookies if available
    AuthManager.auto_login()
    
    if AuthManager.is_logged_in():
        # Show logged-in user info
        user_data = AuthManager.get_current_user()
        st.success(f"👤 {user_data['name']}")
        st.caption(user_data['email'])
        if st.button("Logout", use_container_width=True):
            AuthManager.logout()
            st.rerun()
        st.markdown("---")
        role = st.selectbox("Select Role", ["Guest", "Manager"])
    else:
        # Show login/registration forms
        auth_tab = st.radio("", ["Login", "Register"], horizontal=True)
        
        if auth_tab == "Login":
            with st.form("login_form"):
                st.subheader("🔐 Login")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                submit = st.form_submit_button("Login", use_container_width=True)
                
                if submit:
                    try:
                        user = system.verify_login(email, password)
                        if user:
                            AuthManager.login({
                                'id': user.id,
                                'email': user.email,
                                'name': user.full_name
                            })
                            st.success("Login successful!")
                            st.rerun()
                        else:
                            st.error("Invalid email or password")
                    except ValueError as e:
                        st.error(str(e))
        
        else:  # Register
            # Show registration form
            with st.form("register_form"):
                st.subheader("📝 Register")
                full_name = st.text_input("Full Name")
                email = st.text_input("Email")
                password = st.text_input("Password", type="password")
                password_confirm = st.text_input("Confirm Password", type="password")
                submit = st.form_submit_button("Create Account", use_container_width=True)
                
                if submit:
                    if password != password_confirm:
                        st.error("Passwords do not match")
                    elif len(password) < 6:
                        st.error("Password must be at least 6 characters")
                    elif not email or not full_name:
                        st.error("Please fill in all fields")
                    else:
                        user = system.create_user(email, password, full_name)
                        if user:
                            # Auto-verify the user (email verification disabled for now)
                            system.auto_verify_user(user.id)
                            
                            # Log them in immediately
                            AuthManager.login({
                                'id': user.id,
                                'email': user.email,
                                'name': user.full_name
                            })
                            st.success("✅ Account created successfully! Welcome!")
                            st.rerun()
                        else:
                            st.error("Email already registered. Please login instead.")
        
        # Prevent access to main content if not logged in
        role = None
        st.markdown("---")
        st.info("👆 Please login or register to continue")

# --- MAIN CONTENT ---

if role == "Guest":
    # Hero Section
    st.markdown("""
    <div class="hero-container">
        <div class="hero-title">Welcome to Luxury</div>
        <div class="hero-subtitle">Experience comfort, elegance, and AI-powered hospitality.</div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([1, 1.5], gap="large")

    with col1:
        st.subheader("💬 AI Concierge")
        st.caption("Ask about rooms, amenities, or local tips.")
        
        # Display Chat History
        for msg in st.session_state.messages:
            with st.chat_message(msg["role"]):
                st.write(msg["content"])

        # Chat Input
        if prompt := st.chat_input("How can I help you today?"):
            # Add user message to history
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.write(prompt)

            # Get AI Response
            with st.chat_message("assistant"):
                with st.spinner("Thinking..."):
                    response = ai.process_input(prompt, history=st.session_state.messages, user_name=guest_name)
                    st.write(response)
            
            # Add AI response to history
            st.session_state.messages.append({"role": "assistant", "content": response})

    with col2:
        st.subheader("📅 Book Your Stay")
        with st.container(border=True):
            c1, c2 = st.columns(2)
            check_in = c1.date_input("Check-in", date.today() + timedelta(days=1))
            check_out = c2.date_input("Check-out", date.today() + timedelta(days=2))
            room_type = st.selectbox("Room Type", [t.value for t in RoomType])
            
            if st.button("Check Availability", use_container_width=True):
                # Convert the string value back to enum
                selected_room_type = next(t for t in RoomType if t.value == room_type)
                available = system.check_availability(check_in, check_out, selected_room_type)
                if available:
                    st.success(f"✨ Found {len(available)} {room_type} rooms!")
                    
                    # Store available rooms in session state for booking
                    st.session_state.available_rooms = available
                    st.session_state.booking_check_in = check_in
                    st.session_state.booking_check_out = check_out
                else:
                    st.error("No rooms available for these dates.")
            
            # Show available rooms if they exist in session
            if 'available_rooms' in st.session_state and st.session_state.available_rooms:
                st.markdown("---")
                st.markdown("### 🏨 Available Rooms")
                
                for room in st.session_state.available_rooms:
                    with st.container(border=True):
                        # Room header
                        col_a, col_b = st.columns([3, 1])
                        col_a.markdown(f"**🛏️ Room {room.number}**")
                        col_b.markdown(f"**₹{room.price_per_night}/night**")
                        
                        # Image Gallery
                        img_prefix = room.type.value.lower()
                        ic1, ic2, ic3 = st.columns(3)
                        ic1.image(f"images/{img_prefix}_bedroom.png", caption="Bedroom", use_column_width=True)
                        ic2.image(f"images/{img_prefix}_washroom.png", caption="Washroom", use_column_width=True)
                        ic3.image(f"images/{img_prefix}_amenities.png", caption="Amenities", use_column_width=True)
                        
                        # Booking button
                        if st.button(f"📅 Book Room {room.number}", key=f"book_{room.id}", use_container_width=True, type="primary"):
                            try:
                                # Get current user
                                user_data = AuthManager.get_current_user()
                                
                                # Try to find existing guest or create new one
                                from sqlmodel import Session
                                with Session(system.engine) as session:
                                    # Check if guest exists for this user
                                    guest = session.exec(select(Guest).where(Guest.user_id == user_data['id'])).first()
                                    
                                    if not guest:
                                        # Create new guest with user info
                                        g_id = str(uuid.uuid4())
                                        guest = Guest(
                                            id=g_id,
                                            user_id=user_data['id'],
                                            name=user_data['name'],
                                            email=user_data['email']
                                        )
                                        session.add(guest)
                                        session.commit()
                                        session.refresh(guest)
                                
                                # Create reservation
                                res = system.create_reservation(
                                    guest.id, 
                                    room.id, 
                                    st.session_state.booking_check_in, 
                                    st.session_state.booking_check_out
                                )
                                st.balloons()
                                st.success(f"✅ Reservation Confirmed! ID: {res.id[:8]}...")
                                st.info(f"**Room:** {room.number} | **Dates:** {st.session_state.booking_check_in} to {st.session_state.booking_check_out}")
                                
                                # Clear available rooms after booking
                                del st.session_state.available_rooms
                                st.rerun()
                            except Exception as e:
                                st.error(f"Booking failed: {str(e)}")
                                st.write("Please contact support or try again later.")

elif role == "Staff":
    st.header("🛡️ Staff Operations")
    st.info("Staff module is currently under maintenance for the upgrade.")

elif role == "Manager":
    st.header("📊 Manager Dashboard")
    
    # Metrics
    occ, total = system.get_room_stats()
    revenue = 125000 # Mocked for demo, or calculate from DB
    
    m1, m2, m3 = st.columns(3)
    occupancy_rate = int(occ/total*100) if total > 0 else 0
    m1.metric("Occupancy Rate", f"{occupancy_rate}%", f"{occ}/{total} Rooms")
    m2.metric("Total Revenue", f"₹{revenue:,}", "+12%")
    m3.metric("Check-ins Today", "8", "+2")
    
    st.markdown("### Occupancy Trends")
    # Mock Data for Chart
    chart_data = {
        "Date": [date.today() - timedelta(days=i) for i in range(6, -1, -1)],
        "Occupancy": [45, 50, 65, 70, 85, 90, 88]
    }
    st.line_chart(chart_data, x="Date", y="Occupancy", color="#C5A059")
    
    st.markdown("### Recent Reservations")
    reservations = system.get_all_reservations()
    if reservations:
        data = [{
            "ID": r.id[:8],
            "Guest": r.guest_id[:8],
            "Room": r.room_id[:8],
            "Check-in": r.check_in,
            "Status": r.status
        } for r in reservations]
        st.dataframe(data, use_container_width=True)

