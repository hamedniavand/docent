import aiosmtplib
from typing import Optional
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

async def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None
):
    """
    Send email via SMTP
    """
    try:
        message = MIMEMultipart("alternative")
        message["From"] = settings.EMAIL_FROM
        message["To"] = to_email
        message["Subject"] = subject
        
        # Add text version
        if text_content:
            part1 = MIMEText(text_content, "plain")
            message.attach(part1)
        
        # Add HTML version
        part2 = MIMEText(html_content, "html")
        message.attach(part2)
        
        # Send email
        await aiosmtplib.send(
            message,
            hostname=settings.SMTP_HOST,
            port=settings.SMTP_PORT,
            username=settings.SMTP_USER,
            password=settings.SMTP_PASSWORD,
            use_tls=True
        )
        
        logger.info(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        logger.error(f"Failed to send email to {to_email}: {e}")
        return False

async def send_invite_email(
    to_email: str,
    to_name: str,
    company_name: str,
    invite_token: str,
    custom_message: Optional[str] = None
):
    """
    Send user invitation email
    """
    invite_link = f"{settings.BASE_URL}/auth/accept-invite?token={invite_token}"
    
    subject = f"You're invited to join {company_name} on Docent"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .header {{
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 30px;
                text-align: center;
                border-radius: 8px 8px 0 0;
            }}
            .content {{
                background: #f9f9f9;
                padding: 30px;
                border-radius: 0 0 8px 8px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 30px;
                background: #667eea;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                margin: 20px 0;
            }}
            .footer {{
                text-align: center;
                margin-top: 20px;
                color: #666;
                font-size: 12px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🎓 Welcome to Docent</h1>
            </div>
            <div class="content">
                <p>Hi {to_name},</p>
                
                <p>You've been invited to join <strong>{company_name}</strong> on Docent - our knowledge retention platform.</p>
                
                {f'<p><em>{custom_message}</em></p>' if custom_message else ''}
                
                <p>Click the button below to accept the invitation and set up your account:</p>
                
                <center>
                    <a href="{invite_link}" class="button">Accept Invitation</a>
                </center>
                
                <p style="margin-top: 20px; color: #666; font-size: 14px;">
                    Or copy this link: <br>
                    <code>{invite_link}</code>
                </p>
                
                <p style="margin-top: 30px;">
                    Best regards,<br>
                    The Docent Team
                </p>
            </div>
            <div class="footer">
                <p>This invitation will expire in 7 days.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    text_content = f"""
    Hi {to_name},
    
    You've been invited to join {company_name} on Docent.
    
    Accept your invitation here: {invite_link}
    
    This invitation will expire in 7 days.
    
    Best regards,
    The Docent Team
    """
    
    return await send_email(to_email, subject, html_content, text_content)

async def send_password_reset_email(
    to_email: str,
    to_name: str,
    reset_token: str
):
    """
    Send password reset email
    """
    reset_link = f"{settings.BASE_URL}/auth/reset-password?token={reset_token}"
    
    subject = "Reset your Docent password"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{
                font-family: Arial, sans-serif;
                line-height: 1.6;
                color: #333;
            }}
            .container {{
                max-width: 600px;
                margin: 0 auto;
                padding: 20px;
            }}
            .button {{
                display: inline-block;
                padding: 12px 30px;
                background: #e74c3c;
                color: white;
                text-decoration: none;
                border-radius: 6px;
                margin: 20px 0;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>Password Reset Request</h2>
            
            <p>Hi {to_name},</p>
            
            <p>We received a request to reset your password. Click the button below to set a new password:</p>
            
            <center>
                <a href="{reset_link}" class="button">Reset Password</a>
            </center>
            
            <p style="color: #666; font-size: 14px;">
                If you didn't request this, please ignore this email.
            </p>
            
            <p style="margin-top: 20px; color: #999; font-size: 12px;">
                This link will expire in 1 hour.
            </p>
        </div>
    </body>
    </html>
    """
    
    return await send_email(to_email, subject, html_content)