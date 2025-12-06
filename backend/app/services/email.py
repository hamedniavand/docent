import resend
from typing import Optional
from app.core.config import settings
import logging

logger = logging.getLogger(__name__)

# Initialize Resend
resend.api_key = settings.RESEND_API_KEY

async def send_email(
    to_email: str,
    subject: str,
    html_content: str,
    text_content: Optional[str] = None
):
    """Send email via Resend"""
    try:
        r = resend.Emails.send({
            "from": "Docent <noreply@docent.hexoplus.ir>",
            "to": to_email,
            "subject": subject,
            "html": html_content
        })
        logger.info(f"Email sent successfully to {to_email}, id: {r.get('id')}")
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
    """Send user invitation email"""
    invite_link = f"{settings.BASE_URL}/auth/accept-invite?token={invite_token}"
    
    subject = f"You're invited to join {company_name} on Docent"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 30px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
            .button {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
            .footer {{ text-align: center; margin-top: 20px; color: #666; font-size: 12px; }}
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
                <p style="margin-top: 30px;">Best regards,<br>The Docent Team</p>
            </div>
            <div class="footer">
                <p>This invitation will expire in 7 days.</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    return await send_email(to_email, subject, html_content)

async def send_password_reset_email(
    to_email: str,
    to_name: str,
    reset_token: str
):
    """Send password reset email"""
    reset_link = f"{settings.BASE_URL}/auth/reset-password?token={reset_token}"
    
    subject = "Reset your Docent password"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .button {{ display: inline-block; padding: 12px 30px; background: #e74c3c; color: white; text-decoration: none; border-radius: 6px; margin: 20px 0; }}
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
            <p style="color: #666; font-size: 14px;">If you didn't request this, please ignore this email.</p>
            <p style="margin-top: 20px; color: #999; font-size: 12px;">This link will expire in 1 hour.</p>
        </div>
    </body>
    </html>
    """
    
    return await send_email(to_email, subject, html_content)

async def send_notification_email(
    to_email: str,
    to_name: str,
    subject: str,
    message: str
):
    """Send general notification email"""
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2>🎓 Docent Notification</h2>
        <p>Hi {to_name},</p>
        <p>{message}</p>
        <p style="margin-top: 30px;">Best regards,<br>The Docent Team</p>
    </body>
    </html>
    """
    
    return await send_email(to_email, subject, html_content)

async def send_weekly_digest(
    to_email: str,
    to_name: str,
    digest_data: dict
):
    """Send weekly digest email"""
    subject = "Your Weekly Docent Digest"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2>🎓 Weekly Digest</h2>
        <p>Hi {to_name},</p>
        <p>Here's your weekly summary:</p>
        <ul>
            <li>New documents: {digest_data.get('new_docs', 0)}</li>
            <li>Searches performed: {digest_data.get('searches', 0)}</li>
            <li>Cases created: {digest_data.get('cases', 0)}</li>
        </ul>
        <p style="margin-top: 30px;">Best regards,<br>The Docent Team</p>
    </body>
    </html>
    """
    
    return await send_email(to_email, subject, html_content)

async def send_onboarding_reminder(
    to_email: str,
    to_name: str,
    path_name: str,
    progress: int
):
    """Send onboarding reminder email"""
    subject = f"Continue your onboarding: {path_name}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2>🎓 Onboarding Reminder</h2>
        <p>Hi {to_name},</p>
        <p>You're {progress}% through <strong>{path_name}</strong>. Keep going!</p>
        <p><a href="{settings.BASE_URL}/onboarding" style="display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 6px;">Continue Learning</a></p>
        <p style="margin-top: 30px;">Best regards,<br>The Docent Team</p>
    </body>
    </html>
    """
    
    return await send_email(to_email, subject, html_content)

async def send_document_processed_notification(
    to_email: str,
    to_name: str,
    document_name: str
):
    """Send notification when document is processed"""
    subject = f"Document ready: {document_name}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333; max-width: 600px; margin: 0 auto; padding: 20px;">
        <h2>📄 Document Processed</h2>
        <p>Hi {to_name},</p>
        <p>Your document <strong>{document_name}</strong> has been processed and is now searchable.</p>
        <p><a href="{settings.BASE_URL}/documents-management" style="display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 6px;">View Documents</a></p>
        <p style="margin-top: 30px;">Best regards,<br>The Docent Team</p>
    </body>
    </html>
    """
    
    return await send_email(to_email, subject, html_content)
