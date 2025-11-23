import hashlib
import secrets
from datetime import datetime, timedelta
from typing import Optional
import streamlit as st
import extra_streamlit_components as stx

class AuthManager:
    """Handles user authentication and session management"""
    
    @staticmethod
    def get_cookie_manager():
        """Get cookie manager instance"""
        return stx.CookieManager()
    
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
    def login(user_data: dict, remember_me: bool = True):
        """Set user session data and optionally save to cookies"""
        st.session_state.user_id = user_data['id']
        st.session_state.user_email = user_data['email']
        st.session_state.user_name = user_data['name']
        
        if remember_me:
            # Save to cookies for persistent login
            try:
                cookies = AuthManager.get_cookie_manager()
                token = AuthManager.create_session_token()
                
                # Store user data in cookies (encrypted via token)
                cookies['auth_token'] = token
                cookies['user_id'] = user_data['id']
                cookies['user_email'] = user_data['email']
                cookies['user_name'] = user_data['name']
            except:
                pass  # Cookies not available in some environments
    
    @staticmethod
    def auto_login():
        """Check cookies and auto-login if valid session exists"""
        if AuthManager.is_logged_in():
            return True  # Already logged in
        
        try:
            cookies = AuthManager.get_cookie_manager()
            
            if cookies.get('auth_token') and cookies.get('user_id'):
                # Restore session from cookies
                st.session_state.user_id = cookies.get('user_id')
                st.session_state.user_email = cookies.get('user_email')
                st.session_state.user_name = cookies.get('user_name')
                return True
        except:
            pass
        
        return False
    
    @staticmethod
    def logout():
        """Clear user session and cookies"""
        # Clear session state
        if 'user_id' in st.session_state:
            del st.session_state.user_id
        if 'user_email' in st.session_state:
            del st.session_state.user_email
        if 'user_name' in st.session_state:
            del st.session_state.user_name
        
        # Clear cookies
        try:
            cookies = AuthManager.get_cookie_manager()
            cookies['auth_token'] = ''
            cookies['user_id'] = ''
            cookies['user_email'] = ''
            cookies['user_name'] = ''
        except:
            pass
