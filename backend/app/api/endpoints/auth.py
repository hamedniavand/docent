from fastapi import APIRouter, Depends, HTTPException, status, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.core.database import get_db
from app.core.security import verify_password, create_access_token
from app.core.config import settings
from app.models.models import SystemAdmin, User, ActivityLog
from app.schemas.auth import LoginRequest, LoginResponse, SystemAdminResponse, UserResponse
from app.api.deps.auth import get_current_user, require_active_user
from typing import Union

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=LoginResponse)
def login(
    login_data: LoginRequest,
    db: Session = Depends(get_db)
):
    """
    Login endpoint - returns JWT token
    """
    # Try system admin first
    admin = db.query(SystemAdmin).filter(SystemAdmin.email == login_data.email).first()
    if admin and verify_password(login_data.password, admin.hashed_password):
        if not admin.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        # Create access token
        access_token = create_access_token(
            data={
                "email": admin.email,
                "user_id": admin.id,
                "user_type": "system_admin"
            }
        )
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user={
                "id": admin.id,
                "email": admin.email,
                "name": admin.name,
                "type": "system_admin"
            }
        )
    
    # Try company user
    user = db.query(User).filter(User.email == login_data.email).first()
    if user and user.hashed_password and verify_password(login_data.password, user.hashed_password):
        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Account is inactive"
            )
        
        # Create access token
        access_token = create_access_token(
            data={
                "email": user.email,
                "user_id": user.id,
                "user_type": "company_user",
                "company_id": user.company_id
            }
        )
        
        # Update last login
        user.last_login = datetime.utcnow()
        
        # Log activity
        activity = ActivityLog(
            user_id=user.id,
            company_id=user.company_id,
            action="User Login",
            details={"email": user.email}
        )
        db.add(activity)
        db.commit()
        
        return LoginResponse(
            access_token=access_token,
            token_type="bearer",
            user={
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "company_id": user.company_id,
                "type": "company_user"
            }
        )
    
    # Invalid credentials
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect email or password"
    )

@router.get("/me")
def get_current_user_info(
    current_user: Union[SystemAdmin, User] = Depends(require_active_user),
    db: Session = Depends(get_db)
):
    """
    Get current authenticated user information
    """
    if isinstance(current_user, SystemAdmin):
        return {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "type": "system_admin",
            "is_active": current_user.is_active
        }
    else:
        return {
            "id": current_user.id,
            "email": current_user.email,
            "name": current_user.name,
            "company_id": current_user.company_id,
            "role_id": current_user.role_id,
            "type": "company_user",
            "is_active": current_user.is_active
        }

@router.post("/logout")
def logout(current_user: Union[SystemAdmin, User] = Depends(require_active_user)):
    """
    Logout endpoint (client should discard token)
    """
    return {"message": "Logged out successfully"}

# HTML Login Form
@router.get("/login-page", response_class=HTMLResponse)
def login_page():
    """
    Simple HTML login page
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docent - Login</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
                padding: 20px;
            }
            .login-container {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 10px 40px rgba(0,0,0,0.2);
                width: 100%;
                max-width: 400px;
            }
            h1 {
                color: #2c3e50;
                margin-bottom: 10px;
                font-size: 28px;
            }
            .subtitle {
                color: #7f8c8d;
                margin-bottom: 30px;
                font-size: 14px;
            }
            .form-group {
                margin-bottom: 20px;
            }
            label {
                display: block;
                margin-bottom: 8px;
                color: #2c3e50;
                font-weight: 500;
                font-size: 14px;
            }
            input {
                width: 100%;
                padding: 12px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
                transition: border-color 0.3s;
            }
            input:focus {
                outline: none;
                border-color: #667eea;
            }
            button {
                width: 100%;
                padding: 14px;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                border: none;
                border-radius: 6px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            button:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            }
            button:active {
                transform: translateY(0);
            }
            .error {
                background: #fee;
                color: #c33;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 20px;
                display: none;
                font-size: 14px;
            }
            .success {
                background: #efe;
                color: #3c3;
                padding: 12px;
                border-radius: 6px;
                margin-bottom: 20px;
                display: none;
                font-size: 14px;
            }
            .demo-creds {
                margin-top: 20px;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 6px;
                font-size: 12px;
                color: #666;
            }
            .demo-creds strong {
                color: #2c3e50;
            }
        </style>
    </head>
    <body>
        <div class="login-container">
            <h1>🎓 Docent</h1>
            <p class="subtitle">Knowledge Retention Platform</p>
            
            <div id="error" class="error"></div>
            <div id="success" class="success"></div>
            
            <form id="loginForm">
                <div class="form-group">
                    <label for="email">Email</label>
                    <input type="email" id="email" name="email" required 
                           placeholder="your.email@company.com">
                </div>
                
                <div class="form-group">
                    <label for="password">Password</label>
                    <input type="password" id="password" name="password" required
                           placeholder="Enter your password">
                </div>
                
                <button type="submit">Sign In</button>
            </form>
            
            <div class="demo-creds">
                <strong>Demo Credentials:</strong><br>
                Email: hamed.niavand@gmail.com<br>
                Password: admin123
            </div>
        </div>
        
        <script>
            const form = document.getElementById('loginForm');
            const errorDiv = document.getElementById('error');
            const successDiv = document.getElementById('success');
            
            form.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                errorDiv.style.display = 'none';
                successDiv.style.display = 'none';
                
                const email = document.getElementById('email').value;
                const password = document.getElementById('password').value;
                
                try {
                    const response = await fetch('/auth/login', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                        },
                        body: JSON.stringify({ email, password })
                    });
                    
                    const data = await response.json();
                    
                    if (response.ok) {
                        // Store token
                        localStorage.setItem('access_token', data.access_token);
                        localStorage.setItem('user', JSON.stringify(data.user));
                        
                        successDiv.textContent = 'Login successful! Redirecting...';
                        successDiv.style.display = 'block';
                        
                        // Redirect to dashboard
                        setTimeout(() => {
                            window.location.href = '/dashboard';
                        }, 1000);
                    } else {
                        errorDiv.textContent = data.detail || 'Login failed';
                        errorDiv.style.display = 'block';
                    }
                } catch (error) {
                    errorDiv.textContent = 'Network error. Please try again.';
                    errorDiv.style.display = 'block';
                }
            });
        </script>
    </body>
    </html>
    """