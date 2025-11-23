import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
import streamlit as st

class AuthManager:
    """Handles user authentication and session management"""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using SHA-256 with salt"""
        salt = secrets.token_hex(16)
        pwd_hash = hashlib.sha256((password + salt).encode()).hexdigest()
        return f"{salt}${pwd_hash}"
    
    @staticmethod
    def verify_password(password: str, stored_hash: str) -> bool:
        """Verify a password against stored hash"""
        try:
            salt, pwd_hash = stored_hash.split('$')
            test_hash = hashlib.sha256((password + salt).encode()).hexdigest()
            return test_hash == pwd_hash
        except:
            return False
    
    @staticmethod
    def create_session_token() -> str:
        """Generate a secure session token"""
        return secrets.token_urlsafe(32)
    
    @staticmethod
    def is_logged_in() -> bool:
        """Check if user is logged in"""
        return 'user_id' in st.session_state and st.session_state.user_id is not None
    
    @staticmethod
    def get_current_user():
        """Get current logged-in user data"""
        if not AuthManager.is_logged_in():
            return None
        return {
            'id': st.session_state.get('user_id'),
            'email': st.session_state.get('user_email'),
            'name': st.session_state.get('user_name')
        }
    
    @staticmethod
    def login(user_data: dict):
        """Set user session data"""
        st.session_state.user_id = user_data['id']
        st.session_state.user_email = user_data['email']
        st.session_state.user_name = user_data['name']
    
    @staticmethod
    def logout():
        """Clear user session"""
        if 'user_id' in st.session_state:
            del st.session_state.user_id
        if 'user_email' in st.session_state:
            del st.session_state.user_email
        if 'user_name' in st.session_state:
            del st.session_state.user_name
