"""Email templates for various email types."""

from typing import Dict, Any


class EmailTemplates:
    """Email templates for different types of emails."""
    
    @staticmethod
    def get_verification_email_html(user_name: str, verification_url: str) -> str:
        """Get HTML content for email verification email."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Verify Your Email</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #3b82f6; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9fafb; }}
                .button {{ display: inline-block; background-color: #3b82f6; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
                .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>AliFrzngn Development</h1>
                </div>
                <div class="content">
                    <h2>Verify Your Email Address</h2>
                    <p>Hello {user_name},</p>
                    <p>Thank you for registering with AliFrzngn Development! To complete your registration, please verify your email address by clicking the button below:</p>
                    <p style="text-align: center;">
                        <a href="{verification_url}" class="button">Verify Email Address</a>
                    </p>
                    <p>If the button doesn't work, you can also copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #3b82f6;">{verification_url}</p>
                    <p>This link will expire in 24 hours for security reasons.</p>
                    <p>If you didn't create an account with us, please ignore this email.</p>
                </div>
                <div class="footer">
                    <p>© 2024 AliFrzngn Development. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def get_verification_email_text(user_name: str, verification_url: str) -> str:
        """Get text content for email verification email."""
        return f"""
        Verify Your Email Address - AliFrzngn Development
        
        Hello {user_name},
        
        Thank you for registering with AliFrzngn Development! To complete your registration, please verify your email address by visiting the following link:
        
        {verification_url}
        
        This link will expire in 24 hours for security reasons.
        
        If you didn't create an account with us, please ignore this email.
        
        Best regards,
        The AliFrzngn Development Team
        
        © 2024 AliFrzngn Development. All rights reserved.
        """
    
    @staticmethod
    def get_password_reset_email_html(user_name: str, reset_url: str) -> str:
        """Get HTML content for password reset email."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Reset Your Password</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #dc2626; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9fafb; }}
                .button {{ display: inline-block; background-color: #dc2626; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
                .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>AliFrzngn Development</h1>
                </div>
                <div class="content">
                    <h2>Reset Your Password</h2>
                    <p>Hello {user_name},</p>
                    <p>We received a request to reset your password for your AliFrzngn Development account. Click the button below to reset your password:</p>
                    <p style="text-align: center;">
                        <a href="{reset_url}" class="button">Reset Password</a>
                    </p>
                    <p>If the button doesn't work, you can also copy and paste this link into your browser:</p>
                    <p style="word-break: break-all; color: #dc2626;">{reset_url}</p>
                    <p>This link will expire in 1 hour for security reasons.</p>
                    <p>If you didn't request a password reset, please ignore this email. Your password will remain unchanged.</p>
                </div>
                <div class="footer">
                    <p>© 2024 AliFrzngn Development. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def get_password_reset_email_text(user_name: str, reset_url: str) -> str:
        """Get text content for password reset email."""
        return f"""
        Reset Your Password - AliFrzngn Development
        
        Hello {user_name},
        
        We received a request to reset your password for your AliFrzngn Development account. Visit the following link to reset your password:
        
        {reset_url}
        
        This link will expire in 1 hour for security reasons.
        
        If you didn't request a password reset, please ignore this email. Your password will remain unchanged.
        
        Best regards,
        The AliFrzngn Development Team
        
        © 2024 AliFrzngn Development. All rights reserved.
        """
    
    @staticmethod
    def get_welcome_email_html(user_name: str) -> str:
        """Get HTML content for welcome email."""
        return f"""
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Welcome to AliFrzngn Development</title>
            <style>
                body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
                .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
                .header {{ background-color: #10b981; color: white; padding: 20px; text-align: center; }}
                .content {{ padding: 20px; background-color: #f9fafb; }}
                .button {{ display: inline-block; background-color: #10b981; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
                .footer {{ text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }}
            </style>
        </head>
        <body>
            <div class="container">
                <div class="header">
                    <h1>Welcome to AliFrzngn Development!</h1>
                </div>
                <div class="content">
                    <h2>Hello {user_name}!</h2>
                    <p>Welcome to AliFrzngn Development! We're excited to have you on board.</p>
                    <p>Your account has been successfully created and verified. You can now access all the features of our microservices platform:</p>
                    <ul>
                        <li>📦 Inventory Management</li>
                        <li>👥 Customer Relationship Management</li>
                        <li>🔐 Secure User Authentication</li>
                        <li>📊 Real-time Dashboard</li>
                    </ul>
                    <p style="text-align: center;">
                        <a href="http://localhost:3000/dashboard" class="button">Access Your Dashboard</a>
                    </p>
                    <p>If you have any questions or need assistance, please don't hesitate to contact our support team.</p>
                </div>
                <div class="footer">
                    <p>© 2024 AliFrzngn Development. All rights reserved.</p>
                </div>
            </div>
        </body>
        </html>
        """
    
    @staticmethod
    def get_welcome_email_text(user_name: str) -> str:
        """Get text content for welcome email."""
        return f"""
        Welcome to AliFrzngn Development!
        
        Hello {user_name}!
        
        Welcome to AliFrzngn Development! We're excited to have you on board.
        
        Your account has been successfully created and verified. You can now access all the features of our microservices platform:
        
        - Inventory Management
        - Customer Relationship Management
        - Secure User Authentication
        - Real-time Dashboard
        
        Access your dashboard at: http://localhost:3000/dashboard
        
        If you have any questions or need assistance, please don't hesitate to contact our support team.
        
        Best regards,
        The AliFrzngn Development Team
        
        © 2024 AliFrzngn Development. All rights reserved.
        """
