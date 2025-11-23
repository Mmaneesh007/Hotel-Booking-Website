import smtplib
import random
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from typing import Optional
import streamlit as st

class EmailService:
    """Handles email sending for OTP verification"""
    
    @staticmethod
    def generate_otp() -> str:
        """Generate a 6-digit OTP"""
        return str(random.randint(100000, 999999))
    
    @staticmethod
    def send_otp_email(recipient_email: str, otp: str, user_name: str) -> bool:
        """Send OTP verification email via Gmail SMTP"""
        try:
            # Get email credentials from Streamlit secrets
            smtp_server = st.secrets.get("email", {}).get("smtp_server", "smtp.gmail.com")
            smtp_port = st.secrets.get("email", {}).get("smtp_port", 587)
            sender_email = st.secrets.get("email", {}).get("sender_email")
            sender_password = st.secrets.get("email", {}).get("sender_password")
            
            if not sender_email or not sender_password:
                print("Email credentials not configured in Streamlit secrets")
                return False
            
            # Create email message
            message = MIMEMultipart("alternative")
            message["Subject"] = "Verify Your Email - Hospitality AI"
            message["From"] = f"Hospitality AI <{sender_email}>"
            message["To"] = recipient_email
            
            # Email body
            html_body = f"""
            <html>
                <body style="font-family: Arial, sans-serif; background-color: #f4f4f4; padding: 20px;">
                    <div style="max-width: 600px; margin: 0 auto; background-color: white; padding: 30px; border-radius: 10px; box-shadow: 0 2px 10px rgba(0,0,0,0.1);">
                        <h2 style="color: #2C5364; margin-bottom: 20px;">Welcome to Hospitality AI!</h2>
                        <p>Hi {user_name},</p>
                        <p>Thank you for registering with Hospitality AI. To complete your registration, please verify your email address using the OTP code below:</p>
                        
                        <div style="background: linear-gradient(135deg, #0F2027 0%, #203A43 50%, #2C5364 100%); color: white; padding: 20px; border-radius: 8px; text-align: center; margin: 30px 0;">
                            <h1 style="margin: 0; font-size: 36px; letter-spacing: 8px;">{otp}</h1>
                        </div>
                        
                        <p style="color: #666;">This code will expire in <strong>10 minutes</strong>.</p>
                        <p style="color: #666;">If you didn't request this verification, please ignore this email.</p>
                        
                        <hr style="border: none; border-top: 1px solid #eee; margin: 30px 0;">
                        <p style="color: #999; font-size: 12px;">This is an automated email. Please do not reply.</p>
                    </div>
                </body>
            </html>
            """
            
            # Attach HTML body
            html_part = MIMEText(html_body, "html")
            message.attach(html_part)
            
            # Send email
            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()  # Secure connection
                server.login(sender_email, sender_password)
                server.send_message(message)
            
            return True
            
        except Exception as e:
            print(f"Error sending email: {e}")
            return False
    
    @staticmethod
    def get_otp_expiry() -> datetime:
        """Get OTP expiry time (10 minutes from now)"""
        return datetime.now() + timedelta(minutes=10)
