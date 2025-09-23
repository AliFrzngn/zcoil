"""Email service for sending emails."""

import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
import logging
from jinja2 import Template

from backend.shared.config import settings

logger = logging.getLogger(__name__)


class EmailTemplates:
    """Email templates for various email types."""
    
    @staticmethod
    def get_verification_email_html(user_name: str, verification_url: str) -> str:
        """Get HTML content for verification email."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Verify Your Email - AliFrzngn Development</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #2c3e50;">Welcome to AliFrzngn Development!</h2>
                <p>Hello {user_name},</p>
                <p>Thank you for registering with AliFrzngn Development. Please verify your email address by clicking the button below:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{verification_url}" style="background-color: #3498db; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">Verify Email Address</a>
                </div>
                <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #666;">{verification_url}</p>
                <p>This link will expire in 24 hours.</p>
                <p>If you didn't create an account with us, please ignore this email.</p>
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="font-size: 12px; color: #666;">© 2025 AliFrzngn Development. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def get_verification_email_text(user_name: str, verification_url: str) -> str:
        """Get text content for verification email."""
        return f"""
        Welcome to AliFrzngn Development!
        
        Hello {user_name},
        
        Thank you for registering with AliFrzngn Development. Please verify your email address by visiting the following link:
        
        {verification_url}
        
        This link will expire in 24 hours.
        
        If you didn't create an account with us, please ignore this email.
        
        Best regards,
        AliFrzngn Development Team
        """
    
    @staticmethod
    def get_password_reset_email_html(user_name: str, reset_url: str) -> str:
        """Get HTML content for password reset email."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Reset Your Password - AliFrzngn Development</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #e74c3c;">Password Reset Request</h2>
                <p>Hello {user_name},</p>
                <p>We received a request to reset your password for your AliFrzngn Development account.</p>
                <p>Click the button below to reset your password:</p>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{reset_url}" style="background-color: #e74c3c; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">Reset Password</a>
                </div>
                <p>If the button doesn't work, you can copy and paste this link into your browser:</p>
                <p style="word-break: break-all; color: #666;">{reset_url}</p>
                <p>This link will expire in 1 hour for security reasons.</p>
                <p>If you didn't request a password reset, please ignore this email and your password will remain unchanged.</p>
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="font-size: 12px; color: #666;">© 2025 AliFrzngn Development. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def get_password_reset_email_text(user_name: str, reset_url: str) -> str:
        """Get text content for password reset email."""
        return f"""
        Password Reset Request
        
        Hello {user_name},
        
        We received a request to reset your password for your AliFrzngn Development account.
        
        Please visit the following link to reset your password:
        
        {reset_url}
        
        This link will expire in 1 hour for security reasons.
        
        If you didn't request a password reset, please ignore this email and your password will remain unchanged.
        
        Best regards,
        AliFrzngn Development Team
        """
    
    @staticmethod
    def get_welcome_email_html(user_name: str) -> str:
        """Get HTML content for welcome email."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>Welcome to AliFrzngn Development!</title>
        </head>
        <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
            <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                <h2 style="color: #27ae60;">Welcome to AliFrzngn Development!</h2>
                <p>Hello {user_name},</p>
                <p>Congratulations! Your email has been successfully verified and your account is now active.</p>
                <p>You can now access all features of our platform:</p>
                <ul>
                    <li>Browse our product inventory</li>
                    <li>Manage your customer profile</li>
                    <li>Access exclusive features</li>
                </ul>
                <div style="text-align: center; margin: 30px 0;">
                    <a href="{settings.frontend_url}" style="background-color: #27ae60; color: white; padding: 12px 24px; text-decoration: none; border-radius: 5px; display: inline-block;">Get Started</a>
                </div>
                <p>If you have any questions, feel free to contact our support team.</p>
                <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                <p style="font-size: 12px; color: #666;">© 2025 AliFrzngn Development. All rights reserved.</p>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def get_welcome_email_text(user_name: str) -> str:
        """Get text content for welcome email."""
        return f"""
        Welcome to AliFrzngn Development!
        
        Hello {user_name},
        
        Congratulations! Your email has been successfully verified and your account is now active.
        
        You can now access all features of our platform:
        - Browse our product inventory
        - Manage your customer profile
        - Access exclusive features
        
        Visit our platform: {settings.frontend_url}
        
        If you have any questions, feel free to contact our support team.
        
        Best regards,
        AliFrzngn Development Team
        """


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