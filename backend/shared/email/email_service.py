"""Email service for sending emails."""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
import logging
from jinja2 import Template

from ..config import settings

logger = logging.getLogger(__name__)


class EmailService:
    """Email service for sending various types of emails."""
    
    def __init__(self):
        self.smtp_server = getattr(settings, 'SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = getattr(settings, 'SMTP_PORT', 587)
        self.smtp_username = getattr(settings, 'SMTP_USERNAME', '')
        self.smtp_password = getattr(settings, 'SMTP_PASSWORD', '')
        self.from_email = getattr(settings, 'FROM_EMAIL', 'noreply@alifrzngn.dev')
        self.from_name = getattr(settings, 'FROM_NAME', 'AliFrzngn Development')
    
    def send_email(
        self,
        to_email: str,
        subject: str,
        html_content: str,
        text_content: Optional[str] = None
    ) -> bool:
        """Send an email."""
        try:
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{self.from_name} <{self.from_email}>"
            msg['To'] = to_email
            
            # Add text content
            if text_content:
                text_part = MIMEText(text_content, 'plain')
                msg.attach(text_part)
            
            # Add HTML content
            html_part = MIMEText(html_content, 'html')
            msg.attach(html_part)
            
            # Send email
            if settings.environment == 'development':
                # In development, just log the email
                logger.info(f"Email would be sent to {to_email}: {subject}")
                logger.info(f"Content: {html_content}")
                return True
            
            # In production, actually send the email
            context = ssl.create_default_context()
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            logger.info(f"Email sent successfully to {to_email}")
            return True
            
        except Exception as e:
            logger.error(f"Failed to send email to {to_email}: {str(e)}")
            return False
    
    def send_verification_email(self, to_email: str, verification_token: str, user_name: str) -> bool:
        """Send email verification email."""
        verification_url = f"{settings.FRONTEND_URL}/verify-email?token={verification_token}"
        
        subject = "Verify Your Email Address - AliFrzngn Development"
        
        html_content = EmailTemplates.get_verification_email_html(
            user_name=user_name,
            verification_url=verification_url
        )
        
        text_content = EmailTemplates.get_verification_email_text(
            user_name=user_name,
            verification_url=verification_url
        )
        
        return self.send_email(to_email, subject, html_content, text_content)
    
    def send_password_reset_email(self, to_email: str, reset_token: str, user_name: str) -> bool:
        """Send password reset email."""
        reset_url = f"{settings.FRONTEND_URL}/reset-password?token={reset_token}"
        
        subject = "Reset Your Password - AliFrzngn Development"
        
        html_content = EmailTemplates.get_password_reset_email_html(
            user_name=user_name,
            reset_url=reset_url
        )
        
        text_content = EmailTemplates.get_password_reset_email_text(
            user_name=user_name,
            reset_url=reset_url
        )
        
        return self.send_email(to_email, subject, html_content, text_content)
    
    def send_welcome_email(self, to_email: str, user_name: str) -> bool:
        """Send welcome email to new users."""
        subject = "Welcome to AliFrzngn Development!"
        
        html_content = EmailTemplates.get_welcome_email_html(user_name=user_name)
        text_content = EmailTemplates.get_welcome_email_text(user_name=user_name)
        
        return self.send_email(to_email, subject, html_content, text_content)