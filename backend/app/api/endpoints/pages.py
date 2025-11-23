from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Pages"])

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    """
    Simple dashboard page (protected by frontend)
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docent - Dashboard</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: #f5f7fa;
            }
            .header {
                background: white;
                padding: 20px 40px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .header h1 {
                color: #2c3e50;
                font-size: 24px;
            }
            .user-info {
                display: flex;
                align-items: center;
                gap: 20px;
            }
            .container {
                max-width: 1200px;
                margin: 40px auto;
                padding: 0 20px;
            }
            .welcome-card {
                background: white;
                padding: 40px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }
            .welcome-card h2 {
                color: #2c3e50;
                margin-bottom: 10px;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
            }
            .stat-card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            .stat-card h3 {
                color: #7f8c8d;
                font-size: 14px;
                margin-bottom: 10px;
                text-transform: uppercase;
            }
            .stat-card .value {
                color: #2c3e50;
                font-size: 32px;
                font-weight: bold;
            }
            .btn {
                padding: 10px 20px;
                background: #e74c3c;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
            }
            .btn:hover {
                background: #c0392b;
            }
            .loading {
                text-align: center;
                padding: 40px;
                color: #7f8c8d;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎓 Docent</h1>
            <div class="user-info">
                <span id="userName">Loading...</span>
                <button class="btn" onclick="logout()">Logout</button>
            </div>
        </div>
        
        <div class="container">
            <div class="welcome-card">
                <h2>Welcome to Docent!</h2>
                <p id="welcomeMessage">Loading your dashboard...</p>
            </div>
            
            <div class="stats">
                <div class="stat-card">
                    <h3>Documents</h3>
                    <div class="value">0</div>
                </div>
                <div class="stat-card">
                    <h3>Searches</h3>
                    <div class="value">0</div>
                </div>
                <div class="stat-card">
                    <h3>Users</h3>
                    <div class="value">1</div>
                </div>
                <div class="stat-card">
                    <h3>Templates</h3>
                    <div class="value">3</div>
                </div>
            </div>
        </div>
        
        <script>
            // Check if logged in
            const token = localStorage.getItem('access_token');
            if (!token) {
                window.location.href = '/auth/login-page';
            }
            
            // Load user info
            async function loadUserInfo() {
                try {
                    const response = await fetch('/auth/me', {
                        headers: {
                            'Authorization': `Bearer ${token}`
                        }
                    });
                    
                    if (response.ok) {
                        const user = await response.json();
                        document.getElementById('userName').textContent = user.name;
                        document.getElementById('welcomeMessage').textContent = 
                            `You're logged in as ${user.email}. User type: ${user.type}`;
                    } else {
                        // Token invalid, redirect to login
                        localStorage.removeItem('access_token');
                        window.location.href = '/auth/login-page';
                    }
                } catch (error) {
                    console.error('Error loading user info:', error);
                }
            }
            
            function logout() {
                localStorage.removeItem('access_token');
                localStorage.removeItem('user');
                window.location.href = '/auth/login-page';
            }
            
            // Load user info on page load
            loadUserInfo();
        </script>
    </body>
    </html>
    """

@router.get("/login", response_class=HTMLResponse)
def login_redirect():
    """Redirect /login to /auth/login-page"""
    return """
    <script>window.location.href = '/auth/login-page';</script>
    """