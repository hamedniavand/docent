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

async def send_document_processed_notification(
    to_email: str,
    to_name: str,
    document_name: str,
    status: str,
    chunks_count: int = 0
):
    """
    Send notification when document processing completes
    """
    subject = f"Document Processed: {document_name}"
    
    if status == "processed":
        status_icon = "✅"
        status_text = "successfully processed"
        details = f"<p>Your document has been indexed with <strong>{chunks_count} searchable chunks</strong>. You can now search for content within this document.</p>"
    else:
        status_icon = "❌"
        status_text = "failed to process"
        details = "<p>There was an issue processing your document. Please try re-uploading or contact support.</p>"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
            .status {{ font-size: 18px; margin: 20px 0; }}
            .btn {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 6px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>{status_icon} Document Processing Complete</h1>
            </div>
            <div class="content">
                <p>Hi {to_name},</p>
                <p class="status">Your document <strong>"{document_name}"</strong> has been {status_text}.</p>
                {details}
                <center>
                    <a href="{settings.BASE_URL}/documents-management" class="btn">View Documents</a>
                </center>
            </div>
        </div>
    </body>
    </html>
    """
    
    return await send_email(to_email, subject, html_content)


async def send_weekly_digest(
    to_email: str,
    to_name: str,
    company_name: str,
    stats: dict
):
    """
    Send weekly activity digest
    """
    subject = f"Weekly Digest - {company_name} | Docent"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
            .stat-grid {{ display: grid; grid-template-columns: repeat(2, 1fr); gap: 15px; margin: 20px 0; }}
            .stat-box {{ background: white; padding: 20px; border-radius: 8px; text-align: center; }}
            .stat-value {{ font-size: 32px; font-weight: bold; color: #667eea; }}
            .stat-label {{ color: #666; font-size: 14px; }}
            .btn {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 6px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 Weekly Digest</h1>
                <p>{company_name}</p>
            </div>
            <div class="content">
                <p>Hi {to_name},</p>
                <p>Here's your weekly activity summary:</p>
                
                <div class="stat-grid">
                    <div class="stat-box">
                        <div class="stat-value">{stats.get('searches', 0)}</div>
                        <div class="stat-label">Searches</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{stats.get('documents', 0)}</div>
                        <div class="stat-label">Documents Uploaded</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{stats.get('cases', 0)}</div>
                        <div class="stat-label">Case Studies</div>
                    </div>
                    <div class="stat-box">
                        <div class="stat-value">{stats.get('active_users', 0)}</div>
                        <div class="stat-label">Active Users</div>
                    </div>
                </div>
                
                <h3>Top Searches This Week</h3>
                <ul>
                    {"".join(f"<li>{q}</li>" for q in stats.get('top_queries', ['No searches yet']))}
                </ul>
                
                <center style="margin-top: 30px;">
                    <a href="{settings.BASE_URL}/analytics-dashboard" class="btn">View Full Analytics</a>
                </center>
            </div>
        </div>
    </body>
    </html>
    """
    
    return await send_email(to_email, subject, html_content)


async def send_onboarding_reminder(
    to_email: str,
    to_name: str,
    path_name: str,
    current_step: int,
    total_steps: int,
    path_id: int
):
    """
    Send reminder for incomplete onboarding
    """
    progress_pct = int((current_step / total_steps) * 100) if total_steps > 0 else 0
    remaining = total_steps - current_step
    
    subject = f"Continue Your Onboarding - {remaining} steps remaining"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
            .progress-bar {{ background: #e0e0e0; height: 20px; border-radius: 10px; overflow: hidden; margin: 20px 0; }}
            .progress-fill {{ background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); height: 100%; width: {progress_pct}%; }}
            .btn {{ display: inline-block; padding: 12px 30px; background: #43e97b; color: white; text-decoration: none; border-radius: 6px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📚 Keep Going!</h1>
            </div>
            <div class="content">
                <p>Hi {to_name},</p>
                <p>You're making great progress on <strong>{path_name}</strong>!</p>
                
                <div class="progress-bar">
                    <div class="progress-fill"></div>
                </div>
                <p style="text-align: center; color: #666;">{progress_pct}% complete - {remaining} steps remaining</p>
                
                <p>Take a few minutes to continue your onboarding journey.</p>
                
                <center style="margin-top: 20px;">
                    <a href="{settings.BASE_URL}/onboarding-view/{path_id}" class="btn">Continue Onboarding</a>
                </center>
            </div>
        </div>
    </body>
    </html>
    """
    
    return await send_email(to_email, subject, html_content)


async def send_new_case_notification(
    to_email: str,
    to_name: str,
    case_title: str,
    template_name: str,
    creator_name: str
):
    """
    Notify team about new case study
    """
    subject = f"New Case Study: {case_title}"
    
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <style>
            body {{ font-family: Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; padding: 20px; }}
            .header {{ background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: white; padding: 20px; text-align: center; border-radius: 8px 8px 0 0; }}
            .content {{ background: #f9f9f9; padding: 30px; border-radius: 0 0 8px 8px; }}
            .btn {{ display: inline-block; padding: 12px 30px; background: #667eea; color: white; text-decoration: none; border-radius: 6px; }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📋 New Case Study</h1>
            </div>
            <div class="content">
                <p>Hi {to_name},</p>
                <p>A new case study has been added to your knowledge base:</p>
                
                <div style="background: white; padding: 20px; border-radius: 8px; margin: 20px 0;">
                    <h3 style="margin: 0; color: #667eea;">{case_title}</h3>
                    <p style="margin: 10px 0 0; color: #666;">Template: {template_name}<br>Created by: {creator_name}</p>
                </div>
                
                <center>
                    <a href="{settings.BASE_URL}/cases-management" class="btn">View Case Studies</a>
                </center>
            </div>
        </div>
    </body>
    </html>
    """
    
    return await send_email(to_email, subject, html_content)
