
from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Pages"])

@router.get("/", response_class=HTMLResponse)
def root():
    """Landing page"""
    html = """<!DOCTYPE html>
<html>
<head>
    <title>Docent - Knowledge Retention Platform</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body {
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
        }
        .container { text-align: center; padding: 40px; max-width: 800px; }
        h1 { font-size: 64px; margin-bottom: 20px; }
        .btn {
            display: inline-block;
            padding: 16px 48px;
            background: white;
            color: #667eea;
            text-decoration: none;
            border-radius: 12px;
            font-size: 18px;
            font-weight: 600;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>🎓 Docent</h1>
        <p>AI-Powered Knowledge Retention Platform</p>
        <p style="margin: 30px 0;">Day 30/30 Complete • 100% 🎉</p>
        <a href="/auth/login-page" class="btn">Launch Dashboard →</a>
    </div>
</body>
</html>"""
    return html

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    """
    Dashboard with search widget and stats
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docent - Dashboard</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: #f5f7fa;
            }
            /* Mobile responsive */
            @media (max-width: 768px) {
                .header { padding: 15px 20px !important; flex-direction: column; gap: 10px; }
                .header h1 { font-size: 20px !important; }
                .container { padding: 0 15px !important; margin: 20px auto !important; }
                .stats { grid-template-columns: repeat(2, 1fr) !important; }
                .stat-card { padding: 15px !important; }
                .stat-card .value { font-size: 24px !important; }
                .quick-actions { grid-template-columns: repeat(2, 1fr) !important; }
                .action-btn { padding: 15px 10px !important; font-size: 12px !important; }
                table { font-size: 12px; }
                th, td { padding: 8px !important; }
                .btn { padding: 8px 12px !important; font-size: 12px !important; }
                .modal-content { width: 95% !important; padding: 20px !important; }
                .search-box { width: 100% !important; }
                .grid-2 { grid-template-columns: 1fr !important; }
            }
            @media (max-width: 480px) {
                .stats { grid-template-columns: 1fr !important; }
                .quick-actions { grid-template-columns: 1fr !important; }
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
            
            /* Search Widget */
            .search-widget {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 40px;
                border-radius: 16px;
                margin-bottom: 30px;
                color: white;
            }
            .search-widget h2 {
                margin-bottom: 20px;
                font-size: 24px;
            }
            .search-input-container {
                display: flex;
                gap: 10px;
                max-width: 600px;
            }
            .search-input {
                flex: 1;
                padding: 15px 20px;
                border: none;
                border-radius: 8px;
                font-size: 16px;
            }
            .search-input:focus {
                outline: none;
            }
            .search-btn {
                padding: 15px 30px;
                background: white;
                color: #667eea;
                border: none;
                border-radius: 8px;
                font-size: 16px;
                font-weight: 600;
                cursor: pointer;
                transition: transform 0.2s;
            }
            .search-btn:hover {
                transform: translateY(-2px);
            }
            .search-hint {
                margin-top: 15px;
                font-size: 14px;
                opacity: 0.9;
            }
            
            /* Stats Grid */
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                cursor: pointer;
                transition: transform 0.2s, box-shadow 0.2s;
            }
            .stat-card:hover {
                transform: translateY(-3px);
                box-shadow: 0 4px 15px rgba(0,0,0,0.15);
            }
            .stat-card h3 {
                color: #7f8c8d;
                font-size: 13px;
                margin-bottom: 8px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }
            .stat-card .value {
                color: #2c3e50;
                font-size: 32px;
                font-weight: bold;
            }
            .stat-card .subtitle {
                font-size: 12px;
                color: #999;
                margin-top: 8px;
            }
            .stat-card.highlight {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .stat-card.highlight h3,
            .stat-card.highlight .value,
            .stat-card.highlight .subtitle {
                color: white;
            }
            .stat-card.highlight h3 {
                opacity: 0.9;
            }
            
            /* Quick Actions */
            .quick-actions {
                background: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }
            .quick-actions h3 {
                margin-bottom: 15px;
                color: #2c3e50;
            }
            .action-buttons {
                display: flex;
                gap: 10px;
                flex-wrap: wrap;
            }
            .action-btn {
                padding: 12px 20px;
                border: 2px solid #e0e0e0;
                background: white;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 500;
                color: #555;
                transition: all 0.2s;
                text-decoration: none;
            }
            .action-btn:hover {
                border-color: #667eea;
                color: #667eea;
            }
            
            /* Recent Activity */
            .recent-section {
                background: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }
            .recent-section h3 {
                margin-bottom: 15px;
                color: #2c3e50;
            }
            .recent-item {
                padding: 12px 0;
                border-bottom: 1px solid #eee;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .recent-item:last-child {
                border-bottom: none;
            }
            .recent-item .query {
                color: #333;
                font-weight: 500;
            }
            .recent-item .meta {
                color: #999;
                font-size: 12px;
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
            <!-- Search Widget -->
            <div class="search-widget">
                <h2>🔍 Ask anything about your documents</h2>
                <div class="search-input-container">
                    <input type="text" id="searchInput" class="search-input" 
                           placeholder="e.g., What is our remote work policy?" 
                           onkeypress="if(event.key==='Enter') quickSearch()">
                    <button class="search-btn" onclick="quickSearch()">Search</button>
                </div>
                <p class="search-hint">Try: "onboarding process", "project management", "benefits"</p>
            </div>
            
            <!-- Stats -->
            <div class="stats">
                <div class="stat-card" onclick="window.location.href='/documents-management'">
                    <h3>📄 Documents</h3>
                    <div class="value" id="docCount">-</div>
                    <div class="subtitle">Click to manage</div>
                </div>
                <div class="stat-card" onclick="window.location.href='/users-management'">
                    <h3>👥 Team Members</h3>
                    <div class="value" id="userCount">-</div>
                    <div class="subtitle">Click to manage</div>
                </div>
                <div class="stat-card">
                    <h3>🔍 Searches</h3>
                    <div class="value" id="searchCount">-</div>
                    <div class="subtitle">Total queries</div>
                </div>
                <div class="stat-card highlight" onclick="window.location.href='/search-page'">
                    <h3>✨ AI Search</h3>
                    <div class="value">→</div>
                    <div class="subtitle">Advanced search</div>
                <div class="stat-card" onclick="window.location.href='/onboarding-management'">
                    <h3>📚 Onboarding</h3>
                    <div class="value" id="onboardingCount">-</div>
                    <div class="subtitle">Active paths</div>
                </div>
                </div>
            </div>
            
            <!-- Quick Actions -->
            <div class="quick-actions">
                <h3>Quick Actions</h3>
                <div class="action-buttons">
                    <a href="/documents-management" class="action-btn">📤 Upload Documents</a>
                    <a href="/search-page" class="action-btn">🔍 Advanced Search</a>
                    <a href="/users-management" class="action-btn">👥 Manage Users</a>
                    <a href="/onboarding-management" class="action-btn">📚 Onboarding</a>
                    <a href="/cases-management" class="action-btn">📋 Case Studies</a>
                    <a href="/analytics-dashboard" class="action-btn">📊 Analytics</a>
                    <a href="/settings" class="action-btn">⚙️ Settings</a>
                    <a href="/help" class="action-btn">📚 Help</a>
                    <a href="/docs" class="action-btn" target="_blank">📚 API Docs</a>
                </div>
            </div>
            
            <!-- Recent Searches -->
            <div class="recent-section">
                <h3>Recent Searches</h3>
                <div id="recentSearches">
                    <p style="color: #999;">Loading...</p>
                </div>
            </div>
        </div>
        
        <script>
            const token = localStorage.getItem('access_token');
            // Global error handler
            window.onerror = function(msg, url, line) {
                console.error('Error:', msg, 'at', url, 'line', line);
                return false;
            };

            if (!token) {
                window.location.href = '/auth/login-page';
            }
            
            // Load user info
            async function loadUserInfo() {
                try {
                    const response = await fetch('/auth/me', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    
                    if (response.ok) {
                        const user = await response.json();
                        document.getElementById('userName').textContent = user.name;
                    } else {
                        localStorage.removeItem('access_token');
                        window.location.href = '/auth/login-page';
                    }
                } catch (error) {
                    console.error('Error loading user info:', error);
                }
            }
            
            // Load stats
            async function loadStats() {
                try {
                    // Document count
                    const docResponse = await fetch('/documents/stats/company', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (docResponse.ok) {
                        const stats = await docResponse.json();
                        document.getElementById('docCount').textContent = stats.total_documents;
                    }
                    
                    // User count
                    const userResponse = await fetch('/users/?page_size=1', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (userResponse.ok) {
                        const users = await userResponse.json();
                        document.getElementById('userCount').textContent = users.total;
                    }
                    
                    // Search history count
                    const searchResponse = await fetch('/search/history?limit=100', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (searchResponse.ok) {
                        const searches = await searchResponse.json();
                        document.getElementById('searchCount').textContent = searches.total;
                    }
                    
                    // Onboarding stats
                    const onboardingResponse = await fetch('/onboarding/stats', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (onboardingResponse.ok) {
                        const onboarding = await onboardingResponse.json();
                        document.getElementById('onboardingCount').textContent = onboarding.active_onboardings;
                    }


                } catch (error) {
                    console.error('Error loading stats:', error);
                }
            }
            
            // Load recent searches
            async function loadRecentSearches() {
                try {
                    const response = await fetch('/search/history?limit=5', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        const container = document.getElementById('recentSearches');
                        
                        if (data.history && data.history.length > 0) {
                            container.innerHTML = data.history.map(h => `
                                <div class="recent-item" onclick="searchFromHistory('${h.query}')" style="cursor: pointer;">
                                    <span class="query">"${h.query}"</span>
                                    <span class="meta">${h.results_count} results</span>
                                </div>
                            `).join('');
                        } else {
                            container.innerHTML = '<p style="color: #999;">No recent searches yet. Try searching above!</p>';
                        }
                    }
                } catch (error) {
                    console.error('Error loading recent searches:', error);
                }
            }
            
            // Quick search from dashboard
            function quickSearch() {
                const query = document.getElementById('searchInput').value.trim();
                if (query) {
                    window.location.href = `/search-page?q=${encodeURIComponent(query)}`;
                }
            }
            
            // Search from history
            function searchFromHistory(query) {
                window.location.href = `/search-page?q=${encodeURIComponent(query)}`;
            }
            
            function logout() {
                localStorage.removeItem('access_token');
                localStorage.removeItem('user');
                window.location.href = '/auth/login-page';
            }
            

            // Toast notification system
            function showToast(message, type = 'success', duration = 3000) {
                let container = document.querySelector('.toast-container');
                if (!container) {
                    container = document.createElement('div');
                    container.className = 'toast-container';
                    document.body.appendChild(container);
                }
                
                const toast = document.createElement('div');
                toast.className = 'toast ' + type;
                toast.innerHTML = (type === 'success' ? '✓ ' : type === 'error' ? '✕ ' : '⚠ ') + message;
                container.appendChild(toast);
                
                setTimeout(() => {
                    toast.style.animation = 'slideOut 0.3s ease forwards';
                    setTimeout(() => toast.remove(), 300);
                }, duration);
            }

            // Initialize
            loadUserInfo();
            loadStats();
            loadRecentSearches();
            
            // Focus search input
            document.getElementById('searchInput').focus();
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

@router.get("/users-management", response_class=HTMLResponse)
def users_management():
    """
    User management page for company admins
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docent - User Management</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            .toast-container {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
            }
            .toast {
                padding: 12px 20px;
                margin-bottom: 10px;
                border-radius: 6px;
                color: white;
                animation: slideIn 0.3s ease;
            }
            .toast.success { background: #27ae60; }
            .toast.error { background: #e74c3c; }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }

            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: #f5f7fa;
            }
            /* Mobile responsive */
            @media (max-width: 768px) {
                .header { padding: 15px 20px !important; flex-direction: column; gap: 10px; }
                .header h1 { font-size: 20px !important; }
                .container { padding: 0 15px !important; margin: 20px auto !important; }
                .stats { grid-template-columns: repeat(2, 1fr) !important; }
                .stat-card { padding: 15px !important; }
                .stat-card .value { font-size: 24px !important; }
                .quick-actions { grid-template-columns: repeat(2, 1fr) !important; }
                .action-btn { padding: 15px 10px !important; font-size: 12px !important; }
                table { font-size: 12px; }
                th, td { padding: 8px !important; }
                .btn { padding: 8px 12px !important; font-size: 12px !important; }
                .modal-content { width: 95% !important; padding: 20px !important; }
                .search-box { width: 100% !important; }
                .grid-2 { grid-template-columns: 1fr !important; }
            }
            @media (max-width: 480px) {
                .stats { grid-template-columns: 1fr !important; }
                .quick-actions { grid-template-columns: 1fr !important; }
            }
            .header {
                background: white;
                padding: 20px 40px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .header h1 { color: #2c3e50; font-size: 24px; }
            .container {
                max-width: 1200px;
                margin: 40px auto;
                padding: 0 20px;
            }
            .card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
            }
            .btn-primary {
                background: #667eea;
                color: white;
            }
            .btn-primary:hover { background: #5568d3; }
            .btn-secondary {
                background: #e0e0e0;
                color: #333;
            }
            .btn-danger {
                background: #e74c3c;
                color: white;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }
            th {
                background: #f8f9fa;
                font-weight: 600;
                color: #2c3e50;
            }
            .search-box {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                width: 300px;
                font-size: 14px;
            }
            .badge {
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
            }
            .badge-active { background: #d4edda; color: #155724; }
            .badge-inactive { background: #f8d7da; color: #721c24; }
            .modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                align-items: center;
                justify-content: center;
                z-index: 1000;
            }
            .modal-content {
                background: white;
                padding: 30px;
                border-radius: 12px;
                max-width: 500px;
                width: 90%;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-group label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #2c3e50;
            }
            .form-group input, .form-group select {
                width: 100%;
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🎓 Docent - User Management</h1>
            <button class="btn btn-secondary" onclick="window.location.href='/dashboard'">
                ← Back to Dashboard
            </button>
        </div>
        
        <div class="container">
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2>Team Members</h2>
                    <div>
                        <input type="text" id="searchBox" class="search-box" placeholder="Search users...">
                        <button class="btn btn-primary" onclick="showInviteModal()" style="margin-left: 10px;">
                            + Invite User
                        </button>
                    </div>
                </div>
                
                <table id="usersTable">
                    <thead>
                        <tr>
                            <th>Name</th>
                            <th>Email</th>
                            <th>Role</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="usersTableBody">
                        <tr><td colspan="5" style="text-align: center;">Loading...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <!-- Invite Modal -->
        <div id="inviteModal" class="modal">
            <div class="modal-content">
                <h3>Invite New User</h3>
                <form id="inviteForm">
                    <div class="form-group">
                        <label>Name</label>
                        <input type="text" id="inviteName" required>
                    </div>
                    <div class="form-group">
                        <label>Email</label>
                        <input type="email" id="inviteEmail" required>
                    </div>
                    <div class="form-group">
                        <label>Role</label>
                        <select id="inviteRole">
                            <option value="">Select role...</option>
                        </select>
                    </div>
                    <div class="form-group">
                        <label>Personal Message (Optional)</label>
                        <input type="text" id="inviteMessage" placeholder="Welcome to the team!">
                    </div>
                    <div style="display: flex; gap: 10px; justify-content: flex-end;">
                        <button type="button" class="btn btn-secondary" onclick="closeInviteModal()">Cancel</button>
                        <button type="submit" class="btn btn-primary">Send Invitation</button>
                    </div>
                </form>
            </div>
        </div>
        
        <script>
            const token = localStorage.getItem('access_token');
            let currentUser = null;
            let roles = [];
            
            if (!token) {
                window.location.href = '/auth/login-page';
            }
            
            // Toast notification
            function showToast(message, type = 'success', duration = 3000) {
                let container = document.querySelector('.toast-container');
                if (!container) {
                    container = document.createElement('div');
                    container.className = 'toast-container';
                    document.body.appendChild(container);
                }
                const toast = document.createElement('div');
                toast.className = 'toast ' + type;
                toast.textContent = message;
                container.appendChild(toast);
                setTimeout(() => toast.remove(), duration);
            }
            
            // Load current user
            async function loadCurrentUser() {
                const response = await fetch('/auth/me', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (response.ok) {
                    currentUser = await response.json();
                    loadRoles();
                    loadUsers();
                }
            }
            
            // Load roles
            async function loadRoles() {
                const companyId = currentUser.company_id || 1;
                const response = await fetch(`/users/company/${companyId}/roles`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (response.ok) {
                    roles = await response.json();
                    const select = document.getElementById('inviteRole');
                    select.innerHTML = '<option value="">No role</option>';
                    roles.forEach(role => {
                        select.innerHTML += `<option value="${role.id}">${role.name}</option>`;
                    });
                }
            }
            
            // Load users
            async function loadUsers(search = '') {
                // SystemAdmin sees all users, company users see only their company
                const companyFilter = currentUser.company_id ? `company_id=${currentUser.company_id}&` : '';
                const url = `/users/?${companyFilter}search=${search}`;
                const response = await fetch(url, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    const tbody = document.getElementById('usersTableBody');
                    
                    if (data.users.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="5" style="text-align: center;">No users found</td></tr>';
                        return;
                    }
                    
                    tbody.innerHTML = data.users.map(user => `
                        <tr>
                            <td>${user.name}</td>
                            <td>${user.email}</td>
                            <td>${user.role_name || '-'}</td>
                            <td>
                                <span class="badge ${user.is_active ? 'badge-active' : 'badge-inactive'}">
                                    ${user.is_active ? 'Active' : 'Inactive'}
                                </span>
                            </td>
                            <td>
                                <button class="btn btn-secondary" style="padding: 5px 10px; font-size: 12px;" 
                                        onclick="editUser(${user.id})">Edit</button>
                                <button class="btn btn-danger" style="padding: 5px 10px; font-size: 12px;" 
                                        onclick="toggleUserStatus(${user.id}, ${user.is_active})">
                                    ${user.is_active ? 'Deactivate' : 'Activate'}
                                </button>
                            </td>
                        </tr>
                    `).join('');
                }
            }
            
            // Search
            document.getElementById('searchBox').addEventListener('input', (e) => {
                loadUsers(e.target.value);
            });
            
            // Show invite modal
            function showInviteModal() {
            document.getElementById('inviteModal').style.display = 'flex';
            }
            
            // Close invite modal
            function closeInviteModal() {
                document.getElementById('inviteModal').style.display = 'none';
                document.getElementById('inviteForm').reset();
            }
            
            // Send invitation
            document.getElementById('inviteForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const name = document.getElementById('inviteName').value;
                const email = document.getElementById('inviteEmail').value;
                const roleId = document.getElementById('inviteRole').value;
                const message = document.getElementById('inviteMessage').value;
                
                const response = await fetch('/users/invite', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        name: name,
                        email: email,
                        role_id: roleId ? parseInt(roleId) : null,
                        message: message || null
                    })
                });
                
                if (response.ok) {
                    showToast('Invitation sent!', 'success');
                    closeInviteModal();
                    loadUsers();
                } else {
                    const error = await response.json();
                    showToast('Error: ' + (error.detail || 'Unknown error'), 'error');
                }
            });
            
            // Toggle user status
            async function toggleUserStatus(userId, isActive) {
                const action = isActive ? 'deactivate' : 'activate';
                if (!confirm(`Are you sure you want to ${action} this user?`)) return;
                
                const response = await fetch(`/users/${userId}`, {
                    method: 'PUT',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${token}`
                    },
                    body: JSON.stringify({
                        is_active: !isActive
                    })
                });
                
                if (response.ok) {
                    alert(`User ${action}d successfully!`);
                    loadUsers();
                } else {
                    alert('Error updating user status');
                }
            }
            
            // Edit user (simple version)
            function editUser(userId) {
                alert('Edit functionality - coming in next update!');
            }
            
            // Initialize
            loadCurrentUser();
        </script>
    </body>
    </html>
    """
@router.get("/documents-management", response_class=HTMLResponse)
def documents_management():
    """
    Document management page
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docent - Documents</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: #f5f7fa;
            }
            /* Mobile responsive */
            @media (max-width: 768px) {
                .header { padding: 15px 20px !important; flex-direction: column; gap: 10px; }
                .header h1 { font-size: 20px !important; }
                .container { padding: 0 15px !important; margin: 20px auto !important; }
                .stats { grid-template-columns: repeat(2, 1fr) !important; }
                .stat-card { padding: 15px !important; }
                .stat-card .value { font-size: 24px !important; }
                .quick-actions { grid-template-columns: repeat(2, 1fr) !important; }
                .action-btn { padding: 15px 10px !important; font-size: 12px !important; }
                table { font-size: 12px; }
                th, td { padding: 8px !important; }
                .btn { padding: 8px 12px !important; font-size: 12px !important; }
                .modal-content { width: 95% !important; padding: 20px !important; }
                .search-box { width: 100% !important; }
                .grid-2 { grid-template-columns: 1fr !important; }
            }
            @media (max-width: 480px) {
                .stats { grid-template-columns: 1fr !important; }
                .quick-actions { grid-template-columns: 1fr !important; }
            }
            .header {
                background: white;
                padding: 20px 40px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .header h1 { color: #2c3e50; font-size: 24px; }
            .container {
                max-width: 1200px;
                margin: 40px auto;
                padding: 0 20px;
            }
            .card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
            }
            .btn-primary {
                background: #667eea;
                color: white;
            }
            .btn-primary:hover { background: #5568d3; }
            .btn-secondary {
                background: #e0e0e0;
                color: #333;
            }
            .btn-danger {
                background: #e74c3c;
                color: white;
            }
            .upload-area {
                border: 3px dashed #ddd;
                border-radius: 12px;
                padding: 40px;
                text-align: center;
                margin-bottom: 30px;
                cursor: pointer;
                transition: all 0.3s;
            }
            .upload-area:hover {
                border-color: #667eea;
                background: #f8f9ff;
            }
            .upload-area.dragging {
                border-color: #667eea;
                background: #f0f0ff;
            }
            table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 20px;
            }
            th, td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }
            th {
                background: #f8f9fa;
                font-weight: 600;
                color: #2c3e50;
            }
            .badge {
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
                font-weight: 600;
            }
            .badge-uploaded { background: #d4edda; color: #155724; }
            .badge-processing { background: #fff3cd; color: #856404; }
            .badge-processed { background: #cce5ff; color: #004085; }
            .file-icon {
                font-size: 24px;
                margin-bottom: 10px;
            }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 12px;
            }
            .stat-card h3 {
                font-size: 14px;
                opacity: 0.9;
                margin-bottom: 10px;
            }
            .stat-card .value {
                font-size: 32px;
                font-weight: bold;
            }
            .search-box {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                width: 300px;
                font-size: 14px;
            }
            .loading {
                text-align: center;
                padding: 40px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📄 Docent - Documents</h1>
            <button class="btn btn-secondary" onclick="window.location.href='/dashboard'">
                ← Back to Dashboard
            </button>
        </div>
        
        <div class="container">
            <!-- Stats -->
            <div class="stats" id="stats">
                <div class="stat-card">
                    <h3>Total Documents</h3>
                    <div class="value" id="statTotal"><span class="loading-text">...</span></div>
                </div>
                <div class="stat-card">
                    <h3>Total Size</h3>
                    <div class="value" id="statSize">-</div>
                </div>
                <div class="stat-card">
                    <h3>Recent (7 days)</h3>
                    <div class="value" id="statRecent">-</div>
                </div>
            </div>
            
            <!-- Upload Area -->
            <div class="card">
                <div class="upload-area" id="uploadArea">
                    <div class="file-icon">📤</div>
                    <h3>Drag & Drop Files Here</h3>
                    <p style="color: #666; margin: 10px 0;">or</p>
                    <button class="btn btn-primary" onclick="document.getElementById('fileInput').click()">
                        Choose Files
                    </button>
                    <input type="file" id="fileInput" multiple style="display: none" 
                           accept=".pdf,.docx,.doc,.pptx,.ppt,.xlsx,.xls,.txt">
                    <p style="color: #999; font-size: 12px; margin-top: 15px;">
                        Supported: PDF, DOCX, PPTX, XLSX, TXT (Max 50MB each)
                    </p>
                </div>
                
                <div id="uploadProgress" style="display: none; margin-top: 20px;">
                    <p><strong>Uploading...</strong></p>
                    <div style="background: #e0e0e0; height: 8px; border-radius: 4px; margin-top: 10px;">
                        <div id="progressBar" style="background: #667eea; height: 100%; border-radius: 4px; width: 0%; transition: width 0.3s;"></div>
                    </div>
                </div>
            </div>
            
            <!-- Document List -->
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2>Your Documents</h2>
                    <input type="text" id="searchBox" class="search-box" placeholder="Search documents...">
                </div>
                
                <table>
                    <thead>
                        <tr>
                            <th>Filename</th>
                            <th>Type</th>
                            <th>Size</th>
                            <th>Uploaded By</th>
                            <th>Date</th>
                            <th>Status</th>
                            <th>Actions</th>
                        </tr>
                    </thead>
                    <tbody id="documentsTableBody">
                        <tr><td colspan="7" class="loading">Loading...</td></tr>
                    </tbody>
                </table>
            </div>
        </div>
        
        <script>
            const token = localStorage.getItem('access_token');
            let currentUser = null;
            
            if (!token) {
                window.location.href = '/auth/login-page';
            }
            
            // Load current user
            async function loadCurrentUser() {
                const response = await fetch('/auth/me', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (response.ok) {
                    currentUser = await response.json();
                    loadStats();
                    loadDocuments();
                }
            }
            
            // Load stats
            async function loadStats() {
                const response = await fetch('/documents/stats/company', {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                if (response.ok) {
                    const stats = await response.json();
                    document.getElementById('statTotal').textContent = stats.total_documents;
                    document.getElementById('statSize').textContent = stats.total_size_mb + ' MB';
                    document.getElementById('statRecent').textContent = stats.recent_uploads;
                }
            }
            
            
            // Preview document
            async function previewDocument(docId, filename) {
                document.getElementById('previewModal').style.display = 'flex';
                document.getElementById('previewTitle').textContent = filename;
                document.getElementById('previewContent').textContent = 'Loading...';
                
                try {
                    // Get document summary/text from processing status
                    const response = await fetch(`/processing/status/${docId}`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        if (data.summary) {
                            document.getElementById('previewContent').textContent = data.summary;
                        } else {
                            document.getElementById('previewContent').textContent = 'No preview available. Document may not be processed yet.';
                        }
                    } else {
                        document.getElementById('previewContent').textContent = 'Could not load preview.';
                    }
                } catch (error) {
                    document.getElementById('previewContent').textContent = 'Error loading preview: ' + error.message;
                }
            }
            
            function closePreviewModal() {
                document.getElementById('previewModal').style.display = 'none';
            }
            
// Load documents
            async function loadDocuments(search = '', page = 1) {
                currentPage = page;
                // SystemAdmin sees all documents
                const companyFilter = currentUser.company_id ? `company_id=${currentUser.company_id}&` : '';
                const url = `/documents/?${companyFilter}search=${search}&page=${page}&page_size=10`;
                const response = await fetch(url, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                
                if (response.ok) {
                    const data = await response.json();
                    const tbody = document.getElementById('documentsTableBody');
                    
                    if (data.documents.length === 0) {
                        tbody.innerHTML = '<tr><td colspan="7" style="text-align: center;">No documents found</td></tr>';
                        return;
                    }
                    
                    tbody.innerHTML = data.documents.map(doc => {
                        const date = new Date(doc.created_at).toLocaleDateString();
                        const fileExt = doc.filename.split('.').pop().toUpperCase();
                        const fileSize = doc.file_size ? formatBytes(doc.file_size) : '-';
                        
                        return `
                            <tr>
                                <td><strong>${doc.filename}</strong></td>
                                <td>${fileExt}</td>
                                <td>${fileSize}</td>
                                <td>${doc.uploader_name}</td>
                                <td>${date}</td>
                                <td><span class="badge badge-${doc.status}">${doc.status}</span></td>
                                <td>
                                    ${doc.status === 'uploaded' ? `<button class="btn btn-primary" style="padding: 5px 10px; font-size: 12px; margin-right: 5px;" onclick="processDocument(${doc.id})">Process</button>` : ''}
                                    <button class="btn btn-secondary" style="padding: 5px 10px; font-size: 12px; margin-right: 5px;" 
                                            onclick="downloadDocument(${doc.id}, '${doc.filename}')">Download</button>
                                    <button class="btn btn-danger" style="padding: 5px 10px; font-size: 12px;" 
                                            onclick="deleteDocument(${doc.id})">Delete</button>
                                </td>
                            </tr>
                        `;
                    }).join('');
                    
                    // Render pagination
                    renderPagination(data.total, data.page, data.page_size);
                }
            }
            
            function renderPagination(total, page, pageSize) {
                totalPages = Math.ceil(total / pageSize);
                const container = document.getElementById('docsPagination');
                if (totalPages <= 1) {
                    container.innerHTML = '';
                    return;
                }
                
                let html = '';
                
                // Previous button
                html += `<button class="btn btn-secondary" style="padding:5px 15px;" 
                    ${page <= 1 ? 'disabled' : ''} 
                    onclick="loadDocuments(document.getElementById('searchBox').value, ${page - 1})">← Prev</button>`;
                
                // Page numbers
                for (let i = 1; i <= totalPages && i <= 5; i++) {
                    const pageNum = totalPages <= 5 ? i : (page <= 3 ? i : page - 2 + i - 1);
                    if (pageNum > 0 && pageNum <= totalPages) {
                        html += `<button class="btn ${pageNum === page ? 'btn-primary' : 'btn-secondary'}" 
                            style="padding:5px 12px;" 
                            onclick="loadDocuments(document.getElementById('searchBox').value, ${pageNum})">${pageNum}</button>`;
                    }
                }
                
                // Next button
                html += `<button class="btn btn-secondary" style="padding:5px 15px;" 
                    ${page >= totalPages ? 'disabled' : ''} 
                    onclick="loadDocuments(document.getElementById('searchBox').value, ${page + 1})">Next →</button>`;
                
                container.innerHTML = html;
            }
            
            // Format bytes
            function formatBytes(bytes) {
                if (bytes === 0) return '0 Bytes';
                const k = 1024;
                const sizes = ['Bytes', 'KB', 'MB', 'GB'];
                const i = Math.floor(Math.log(bytes) / Math.log(k));
                return Math.round(bytes / Math.pow(k, i) * 100) / 100 + ' ' + sizes[i];
            }
            
            // Search
            let searchTimeout;
            document.getElementById('searchBox').addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => {
                    loadDocuments(e.target.value);
                }, 500);
            });
            
            // File input change
            document.getElementById('fileInput').addEventListener('change', (e) => {
                if (e.target.files.length > 0) {
                    uploadFiles(e.target.files);
                }
            });
            
            // Drag and drop
            const uploadArea = document.getElementById('uploadArea');
            
            uploadArea.addEventListener('dragover', (e) => {
                e.preventDefault();
                uploadArea.classList.add('dragging');
            });
            
            uploadArea.addEventListener('dragleave', () => {
                uploadArea.classList.remove('dragging');
            });
            
            uploadArea.addEventListener('drop', (e) => {
                e.preventDefault();
                uploadArea.classList.remove('dragging');
                
                if (e.dataTransfer.files.length > 0) {
                    uploadFiles(e.dataTransfer.files);
                }
            });
            
            // Upload files
            async function uploadFiles(files) {
                const progressDiv = document.getElementById('uploadProgress');
                const progressBar = document.getElementById('progressBar');
                
                progressDiv.style.display = 'block';
                progressBar.style.width = '0%';
                
                const formData = new FormData();
                for (let file of files) {
                    formData.append('files', file);
                }
                
                try {
                    // Simulate progress
                    let progress = 0;
                    const progressInterval = setInterval(() => {
                        progress += 10;
                        if (progress <= 90) {
                            progressBar.style.width = progress + '%';
                        }
                    }, 200);
                    
                    const response = await fetch('/documents/upload-multiple', {
                        method: 'POST',
                        headers: {
                            'Authorization': `Bearer ${token}`
                        },
                        body: formData
                    });
                    
                    clearInterval(progressInterval);
                    progressBar.style.width = '100%';
                    
                    if (response.ok) {
                        const uploaded = await response.json();
                        alert(`Successfully uploaded ${uploaded.length} file(s)`);
                        
                        // Reset
                        document.getElementById('fileInput').value = '';
                        setTimeout(() => {
                            progressDiv.style.display = 'none';
                            progressBar.style.width = '0%';
                        }, 1000);
                        
                        // Reload
                        loadStats();
                        loadDocuments();
                    } else {
                        showToast('Upload failed. Please try again.', 'error');
                        progressDiv.style.display = 'none';
                    }
                } catch (error) {
                    alert('Upload error: ' + error.message);
                    progressDiv.style.display = 'none';
                }
            }
            
            // Download document
            async function downloadDocument(docId, filename) {
                // Fetch file with token
                const response = await fetch(`/documents/${docId}/download`, {
                    headers: { 'Authorization': `Bearer ${token}` }
                });
                
                if (response.ok) {
                    // Create blob and download
                    const blob = await response.blob();
                    const url = window.URL.createObjectURL(blob);
                    const a = document.createElement('a');
                    a.href = url;
                    a.download = filename;
                    document.body.appendChild(a);
                    a.click();
                    window.URL.revokeObjectURL(url);
                    document.body.removeChild(a);
                } else {
                    showToast('Failed to download file', 'error');
                }
            }
            
            // Delete document
            // Process document
            async function processDocument(docId) {
                if (!confirm("Process this document? This will extract text and create searchable chunks.")) return;
                
                try {
                    const response = await fetch(`/processing/process/${docId}`, {
                        method: "POST",
                        headers: { "Authorization": `Bearer ${token}` }
                    });
                    
                    if (response.ok) {
                        alert("Processing started! Refresh in a few seconds to see updated status.");
                        loadDocuments();
                    } else {
                        const error = await response.json();
                        alert("Error: " + (error.detail || "Failed to start processing"));
                    }
                } catch (error) {
                    alert("Error: " + error.message);
                }
            }

            async function deleteDocument(docId) {
                if (!confirm('Are you sure you want to delete this document?')) return;
                
                const response = await fetch(`/documents/${docId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                
                if (response.ok) {
                    showToast('Document deleted successfully', 'success');
                    loadStats();
                    loadDocuments();
                } else {
                    alert('Failed to delete document');
                }
            }
            
            // Initialize
            loadCurrentUser();
        </script>
    </body>
    </html>
    """
@router.get("/search-page", response_class=HTMLResponse)
def search_page():
    """
    AI Search page
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docent - AI Search</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: #f5f7fa;
                min-height: 100vh;
            }
            .header {
                background: white;
                padding: 20px 40px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .header h1 { color: #2c3e50; font-size: 24px; }
            .container {
                max-width: 900px;
                margin: 40px auto;
                padding: 0 20px;
            }
            .search-box {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 30px;
            }
            .search-input-container {
                display: flex;
                gap: 10px;
            }
            .search-input {
                flex: 1;
                padding: 15px 20px;
                border: 2px solid #e0e0e0;
                border-radius: 8px;
                font-size: 16px;
                transition: border-color 0.3s;
            }
            .search-input:focus {
                outline: none;
                border-color: #667eea;
            }
            .btn {
                padding: 15px 30px;
                border: none;
                border-radius: 8px;
                cursor: pointer;
                font-size: 16px;
                font-weight: 600;
                transition: all 0.3s;
            }
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .btn-primary:hover {
                transform: translateY(-2px);
                box-shadow: 0 5px 20px rgba(102, 126, 234, 0.4);
            }
            .btn-secondary {
                background: #e0e0e0;
                color: #333;
            }
            .results-container {
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .results-header {
                padding: 20px;
                border-bottom: 1px solid #eee;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .results-header h2 { font-size: 18px; color: #2c3e50; }
            .results-meta { color: #7f8c8d; font-size: 14px; }
            .result-item {
                padding: 20px;
                border-bottom: 1px solid #eee;
                transition: background 0.2s;
            }
            .result-item:hover {
                background: #f8f9ff;
            }
            .result-item:last-child {
                border-bottom: none;
            }
            .result-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }
            .result-filename {
                font-weight: 600;
                color: #667eea;
                font-size: 16px;
            }
            .result-score {
                background: #e8f5e9;
                color: #2e7d32;
                padding: 4px 12px;
                border-radius: 20px;
                font-size: 12px;
                font-weight: 600;
            }
            .result-score.high { background: #e8f5e9; color: #2e7d32; }
            .result-score.medium { background: #fff3e0; color: #ef6c00; }
            .result-score.low { background: #ffebee; color: #c62828; }
            .result-text {
                color: #555;
                line-height: 1.6;
                font-size: 14px;
                max-height: 100px;
                overflow: hidden;
                position: relative;
            }
            .result-text.expanded {
                max-height: none;
            }
            .result-meta {
                margin-top: 10px;
                font-size: 12px;
                color: #999;
            }
            .expand-btn {
                color: #667eea;
                cursor: pointer;
                font-size: 12px;
                margin-top: 5px;
                display: inline-block;
            }
            .no-results {
                padding: 60px 20px;
                text-align: center;
                color: #7f8c8d;
            }
            .no-results h3 { margin-bottom: 10px; color: #2c3e50; }
            .loading {
                padding: 40px;
                text-align: center;
                color: #7f8c8d;
            }
            .search-history {
                margin-top: 20px;
            }
            .history-item {
                display: inline-block;
                padding: 6px 12px;
                background: #f0f0f0;
                border-radius: 20px;
                margin: 4px;
                font-size: 13px;
                color: #555;
                cursor: pointer;
                transition: background 0.2s;
            }
            .history-item:hover {
                background: #e0e0e0;
            }
            .highlight {
                background: #fff59d;
                padding: 1px 3px;
                border-radius: 2px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>🔍 Docent - AI Search</h1>
            <button class="btn btn-secondary" onclick="window.location.href='/dashboard'">
                ← Back to Dashboard
            </button>
        </div>
        
        <div class="container">
            <div class="search-box">
                <div class="search-input-container">
                    <input type="text" id="searchInput" class="search-input" 
                           placeholder="Ask anything about your documents..." 
                           onkeypress="if(event.key==='Enter') performSearch()">
                    <button class="btn btn-primary" onclick="performSearch()">
                        Search
                    </button>
                </div>
                
                <div class="search-history" id="searchHistory">
                    <!-- Recent searches will appear here -->
                </div>
            </div>
            
            <div class="results-container" id="resultsContainer" style="display: none;">
                <div class="results-header">
                    <h2>Search Results</h2>
                    <span class="results-meta" id="resultsMeta"></span>
                </div>
                <div id="resultsBody">
                    <!-- Results will appear here -->
                </div>
            </div>
        </div>
        
        <script>
            const token = localStorage.getItem('access_token');
            if (!token) {
                window.location.href = '/auth/login-page';
            }
            
            // Load search history on page load
            loadSearchHistory();
            
            async function performSearch() {
                const query = document.getElementById('searchInput').value.trim();
                if (!query) return;
                
                const resultsContainer = document.getElementById('resultsContainer');
                const resultsBody = document.getElementById('resultsBody');
                const resultsMeta = document.getElementById('resultsMeta');
                
                resultsContainer.style.display = 'block';
                resultsBody.innerHTML = '<div class="loading">🔍 Searching...</div>';
                
                try {
                    const response = await fetch('/search/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({
                            query: query,
                            top_k: 5
                        })
                    });
                    
                    if (!response.ok) {
                        throw new Error('Search failed');
                    }
                    
                    const data = await response.json();
                    
                    // Update meta
                    resultsMeta.textContent = `${data.total_results} results in ${data.search_time_ms}ms`;
                    
                    // Deduplicate results by document_id + chunk_index
                    const seen = new Set();
                    const uniqueResults = data.results.filter(r => {
                        const key = `${r.document_id}-${r.chunk_index}`;
                        if (seen.has(key)) return false;
                        seen.add(key);
                        return true;
                    });
                    
                    if (uniqueResults.length === 0) {
                        resultsBody.innerHTML = `
                            <div class="no-results">
                                <h3>No results found</h3>
                                <p>Try different keywords or upload more documents</p>
                            </div>
                        `;
                        return;
                    }
                    
                    // Render results
                    resultsBody.innerHTML = uniqueResults.map((result, index) => {
                        const scoreClass = result.score > 0.7 ? 'high' : (result.score > 0.4 ? 'medium' : 'low');
                        const scorePercent = Math.round(result.score * 100);
                        
                        // Highlight query terms in text
                        let displayText = result.chunk_text;
                        const queryWords = query.toLowerCase().split(' ');
                        queryWords.forEach(word => {
                            if (word.length > 2) {
                                const regex = new RegExp(`(${word})`, 'gi');
                                displayText = displayText.replace(regex, '<span class="highlight">$1</span>');
                            }
                        });
                        
                        // Truncate for display
                        const truncated = displayText.length > 300 ? displayText.substring(0, 300) + '...' : displayText;
                        
                        return `
                            <div class="result-item">
                                <div class="result-header">
                                    <span class="result-filename">📄 ${result.filename}</span>
                                    <span class="result-score ${scoreClass}">${scorePercent}% match</span>
                                </div>
                                <div class="result-text" id="text-${index}">
                                    ${truncated}
                                </div>
                                ${displayText.length > 300 ? `
                                    <span class="expand-btn" onclick="toggleExpand(${index}, \`${displayText.replace(/`/g, "'")}\`)">
                                        Show more ▼
                                    </span>
                                ` : ''}
                                <div class="result-meta">
                                    Document ID: ${result.document_id} | Chunk: ${result.chunk_index}
                                </div>
                            </div>
                        `;
                    }).join('');
                    
                    // Reload search history
                    loadSearchHistory();
                    
                } catch (error) {
                    resultsBody.innerHTML = `
                        <div class="no-results">
                            <h3>Search Error</h3>
                            <p>${error.message}</p>
                        </div>
                    `;
                }
            }
            
            function toggleExpand(index, fullText) {
                const textEl = document.getElementById(`text-${index}`);
                if (textEl.classList.contains('expanded')) {
                    textEl.classList.remove('expanded');
                    textEl.innerHTML = fullText.substring(0, 300) + '...';
                } else {
                    textEl.classList.add('expanded');
                    textEl.innerHTML = fullText;
                }
            }
            
            async function loadSearchHistory() {
                try {
                    const response = await fetch('/search/history?limit=5', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        const historyContainer = document.getElementById('searchHistory');
                        
                        if (data.history && data.history.length > 0) {
                            historyContainer.innerHTML = '<span style="color: #999; font-size: 13px;">Recent: </span>' +
                                data.history.map(h => 
                                    `<span class="history-item" onclick="searchFromHistory('${h.query}')">${h.query}</span>`
                                ).join('');
                        }
                    }
                } catch (error) {
                    console.error('Failed to load search history');
                }
            }
            
            function searchFromHistory(query) {
                document.getElementById('searchInput').value = query;
                performSearch();
            }
            
            // Focus search input on load
            // Check for query parameter and auto-search
                const urlParams = new URLSearchParams(window.location.search);
                const queryParam = urlParams.get('q');
                if (queryParam) {
                    document.getElementById('searchInput').value = queryParam;
                    performSearch();
                } else {
                    document.getElementById('searchInput').focus();
                }
        </script>
    </body>
    </html>
    """
@router.get("/onboarding-management", response_class=HTMLResponse)
def onboarding_management():
    """
    Onboarding path management page
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docent - Onboarding Management</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: #f5f7fa;
            }
            /* Mobile responsive */
            @media (max-width: 768px) {
                .header { padding: 15px 20px !important; flex-direction: column; gap: 10px; }
                .header h1 { font-size: 20px !important; }
                .container { padding: 0 15px !important; margin: 20px auto !important; }
                .stats { grid-template-columns: repeat(2, 1fr) !important; }
                .stat-card { padding: 15px !important; }
                .stat-card .value { font-size: 24px !important; }
                .quick-actions { grid-template-columns: repeat(2, 1fr) !important; }
                .action-btn { padding: 15px 10px !important; font-size: 12px !important; }
                table { font-size: 12px; }
                th, td { padding: 8px !important; }
                .btn { padding: 8px 12px !important; font-size: 12px !important; }
                .modal-content { width: 95% !important; padding: 20px !important; }
                .search-box { width: 100% !important; }
                .grid-2 { grid-template-columns: 1fr !important; }
            }
            @media (max-width: 480px) {
                .stats { grid-template-columns: 1fr !important; }
                .quick-actions { grid-template-columns: 1fr !important; }
            }
            .header {
                background: white;
                padding: 20px 40px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .header h1 { color: #2c3e50; font-size: 24px; }
            .container {
                max-width: 1200px;
                margin: 40px auto;
                padding: 0 20px;
            }
            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
                transition: all 0.2s;
            }
            .btn-primary {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
            }
            .btn-primary:hover { transform: translateY(-2px); }
            .btn-secondary {
                background: #e0e0e0;
                color: #333;
            }
            .btn-success {
                background: #27ae60;
                color: white;
            }
            .card {
                background: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .card h2 {
                color: #2c3e50;
                margin-bottom: 20px;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .path-card {
                border: 2px solid #eee;
                border-radius: 10px;
                padding: 20px;
                margin-bottom: 15px;
                transition: all 0.2s;
            }
            .path-card:hover {
                border-color: #667eea;
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.15);
            }
            .path-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 10px;
            }
            .path-name {
                font-size: 18px;
                font-weight: 600;
                color: #2c3e50;
            }
            .path-meta {
                color: #7f8c8d;
                font-size: 14px;
            }
            .steps-preview {
                display: flex;
                gap: 8px;
                margin-top: 15px;
                flex-wrap: wrap;
            }
            .step-badge {
                background: #f0f0f0;
                padding: 6px 12px;
                border-radius: 20px;
                font-size: 12px;
                color: #555;
            }
            .modal {
                display: none;
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 100%;
                background: rgba(0,0,0,0.5);
                align-items: center;
                justify-content: center;
                z-index: 1000;
            }
            .modal-content {
                background: white;
                padding: 30px;
                border-radius: 12px;
                max-width: 600px;
                width: 90%;
                max-height: 80vh;
                overflow-y: auto;
            }
            .modal-content h3 {
                margin-bottom: 20px;
                color: #2c3e50;
            }
            .form-group {
                margin-bottom: 20px;
            }
            .form-group label {
                display: block;
                margin-bottom: 8px;
                font-weight: 600;
                color: #2c3e50;
            }
            .form-group input, .form-group textarea {
                width: 100%;
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
            }
            .form-group textarea {
                min-height: 80px;
                resize: vertical;
            }
            .steps-builder {
                border: 2px dashed #e0e0e0;
                border-radius: 8px;
                padding: 15px;
                margin-top: 10px;
            }
            .step-item {
                background: #f8f9fa;
                padding: 15px;
                border-radius: 8px;
                margin-bottom: 10px;
                position: relative;
            }
            .step-item .step-number {
                position: absolute;
                left: -10px;
                top: -10px;
                background: #667eea;
                color: white;
                width: 28px;
                height: 28px;
                border-radius: 50%;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 12px;
                font-weight: bold;
            }
            .step-item input {
                margin-bottom: 8px;
            }
            .remove-step {
                position: absolute;
                right: 10px;
                top: 10px;
                background: #e74c3c;
                color: white;
                border: none;
                width: 24px;
                height: 24px;
                border-radius: 50%;
                cursor: pointer;
                font-size: 14px;
            }
            .add-step-btn {
                width: 100%;
                padding: 12px;
                border: 2px dashed #667eea;
                background: transparent;
                color: #667eea;
                border-radius: 8px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
            }
            .add-step-btn:hover {
                background: #f0f0ff;
            }
            .empty-state {
                text-align: center;
                padding: 60px 20px;
                color: #7f8c8d;
            }
            .empty-state h3 {
                margin-bottom: 10px;
                color: #2c3e50;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📚 Onboarding Management</h1>
            <button class="btn btn-secondary" onclick="window.location.href='/dashboard'">
                ← Back to Dashboard
            </button>
        </div>
        
        <div class="container">
            <div class="card">
                <h2>
                    <span>Onboarding Paths</span>
                    <button class="btn btn-primary" onclick="showCreateModal()">+ Create Path</button>
                </h2>
                
                <div id="pathsList">
                    <div class="empty-state">
                        <h3>Loading...</h3>
                    </div>
                </div>
            </div>
        </div>
        
        <!-- Create Modal -->
        <div id="createModal" class="modal">
            <div class="modal-content">
                <h3>Create Onboarding Path</h3>
                <form id="createForm" onsubmit="createPath(event)">
                    <div class="form-group">
                        <label>Path Name</label>
                        <input type="text" id="pathName" required placeholder="e.g., New Employee Onboarding">
                    </div>
                    <div class="form-group">
                        <label>Description</label>
                        <textarea id="pathDescription" placeholder="Brief description of this onboarding path"></textarea>
                    </div>
                    <div class="form-group">
                        <label>Steps</label>
                        <div class="steps-builder" id="stepsBuilder">
                            <!-- Steps will be added here -->
                        </div>
                        <button type="button" class="add-step-btn" onclick="addStep()">+ Add Step</button>
                    </div>
                    <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px;">
                        <button type="button" class="btn btn-secondary" onclick="closeCreateModal()">Cancel</button>
                        <button type="submit" class="btn btn-primary">Create Path</button>
                    </div>
                </form>
            </div>
        </div>
        
        <script>
            const token = localStorage.getItem('access_token');
            if (!token) {
                window.location.href = '/auth/login-page';
            }
            
            let stepCount = 0;
            
            // Load paths
            async function loadPaths() {
                try {
                    const response = await fetch('/onboarding/paths', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        renderPaths(data.paths);
                    }
                } catch (error) {
                    console.error('Error loading paths:', error);
                }
            }
            
            function renderPaths(paths) {
                const container = document.getElementById('pathsList');
                
                if (paths.length === 0) {
                    container.innerHTML = `
                        <div class="empty-state">
                            <h3>No onboarding paths yet</h3>
                            <p>Create your first onboarding path to get started</p>
                        </div>
                    `;
                    return;
                }
                
                container.innerHTML = paths.map(path => {
                    const steps = path.steps_json?.steps || [];
                    return `
                        <div class="path-card">
                            <div class="path-header">
                                <span class="path-name">${path.name}</span>
                                <div>
                                    <button class="btn btn-success" onclick="viewPath(${path.id})" style="margin-right: 5px;">
                                        View
                                    </button>
                                    <button class="btn btn-secondary" onclick="deletePath(${path.id})" style="padding: 8px 15px;">
                                        🗑️
                                    </button>
                                </div>
                            </div>
                            <div class="path-meta">${steps.length} steps • Created ${new Date(path.created_at).toLocaleDateString()}</div>
                            <div class="steps-preview">
                                ${steps.slice(0, 5).map((s, i) => `<span class="step-badge">${i+1}. ${s.title}</span>`).join('')}
                                ${steps.length > 5 ? `<span class="step-badge">+${steps.length - 5} more</span>` : ''}
                            </div>
                        </div>
                    `;
                }).join('');
            }
            
            function showCreateModal() {
                document.getElementById('createModal').style.display = 'flex';
                stepCount = 0;
                document.getElementById('stepsBuilder').innerHTML = '';
                addStep(); // Add first step by default
            }
            
            function closeCreateModal() {
                document.getElementById('createModal').style.display = 'none';
                document.getElementById('createForm').reset();
            }
            
            function addStep() {
                stepCount++;
                const builder = document.getElementById('stepsBuilder');
                const stepDiv = document.createElement('div');
                stepDiv.className = 'step-item';
                stepDiv.id = `step-${stepCount}`;
                stepDiv.innerHTML = `
                    <span class="step-number">${stepCount}</span>
                    <button type="button" class="remove-step" onclick="removeStep(${stepCount})">×</button>
                    <input type="text" placeholder="Step title" class="step-title" required>
                    <textarea placeholder="Step description" class="step-desc"></textarea>
                `;
                builder.appendChild(stepDiv);
            }
            
            function removeStep(num) {
                const step = document.getElementById(`step-${num}`);
                if (step) step.remove();
                renumberSteps();
            }
            
            function renumberSteps() {
                const steps = document.querySelectorAll('.step-item');
                steps.forEach((step, i) => {
                    step.querySelector('.step-number').textContent = i + 1;
                });
            }
            
            async function createPath(e) {
                e.preventDefault();
                
                const name = document.getElementById('pathName').value;
                const description = document.getElementById('pathDescription').value;
                
                const steps = [];
                document.querySelectorAll('.step-item').forEach((item, i) => {
                    const title = item.querySelector('.step-title').value;
                    const desc = item.querySelector('.step-desc').value;
                    if (title) {
                        steps.push({
                            title: title,
                            description: desc || '',
                            order: i + 1
                        });
                    }
                });
                
                if (steps.length === 0) {
                    alert('Please add at least one step');
                    return;
                }
                
                try {
                    const response = await fetch('/onboarding/paths', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({
                            name: name,
                            description: description,
                            steps: steps
                        })
                    });
                    
                    if (response.ok) {
                        alert('Onboarding path created successfully!');
                        closeCreateModal();
                        loadPaths();
                    } else {
                        const error = await response.json();
                        showToast('Error: ' + (error.detail || 'Unknown error'), 'error');
                    }
                } catch (error) {
                    alert('Error creating path: ' + error.message);
                }
            }
            
            function viewPath(pathId) {
                window.location.href = `/onboarding-view/${pathId}`;
            }
            
            async function deletePath(pathId) {
                if (!confirm('Are you sure you want to delete this onboarding path?')) return;
                
                try {
                    const response = await fetch(`/onboarding/paths/${pathId}`, {
                        method: 'DELETE',
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    
                    if (response.ok) {
                        alert('Path deleted');
                        loadPaths();
                    }
                } catch (error) {
                    alert('Error deleting path');
                }
            }
            
            // Initialize
            loadPaths();
        </script>
    </body>
    </html>
    """
@router.get("/onboarding-view/{path_id}", response_class=HTMLResponse)
def onboarding_view(path_id: int):
    """
    View and complete onboarding path
    """
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docent - Onboarding</title>
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: #f5f7fa;
                min-height: 100vh;
            }
            .header {
                background: white;
                padding: 20px 40px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .header h1 { color: #2c3e50; font-size: 24px; }
            .container {
                max-width: 900px;
                margin: 40px auto;
                padding: 0 20px;
            }
            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
            }
            .btn-secondary {
                background: #e0e0e0;
                color: #333;
            }
            .progress-header {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 30px;
                border-radius: 12px;
                color: white;
                margin-bottom: 30px;
            }
            .progress-header h2 { margin-bottom: 15px; }
            .progress-bar-container {
                background: rgba(255,255,255,0.3);
                height: 10px;
                border-radius: 5px;
                overflow: hidden;
            }
            .progress-bar {
                background: white;
                height: 100%;
                border-radius: 5px;
                transition: width 0.5s ease;
            }
            .progress-text {
                margin-top: 10px;
                font-size: 14px;
                opacity: 0.9;
            }
            .steps-container {
                background: white;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                overflow: hidden;
            }
            .step-item {
                padding: 25px;
                border-bottom: 1px solid #eee;
                display: flex;
                gap: 20px;
                transition: background 0.2s;
            }
            .step-item:last-child { border-bottom: none; }
            .step-item.active { background: #f8f9ff; }
            .step-item.completed { background: #f0fff4; }
            .step-number {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: #e0e0e0;
                display: flex;
                align-items: center;
                justify-content: center;
                font-weight: bold;
                color: #666;
                flex-shrink: 0;
            }
            .step-item.active .step-number { background: #667eea; color: white; }
            .step-item.completed .step-number { background: #27ae60; color: white; }
            .step-content { flex: 1; }
            .step-title {
                font-size: 18px;
                font-weight: 600;
                color: #2c3e50;
                margin-bottom: 8px;
            }
            .step-description {
                color: #666;
                line-height: 1.6;
                margin-bottom: 15px;
            }
            .checkbox-label {
                display: flex;
                align-items: center;
                gap: 10px;
                cursor: pointer;
                font-size: 14px;
                color: #555;
            }
            .checkbox-label input {
                width: 20px;
                height: 20px;
                cursor: pointer;
            }
            .completion-card {
                background: linear-gradient(135deg, #27ae60 0%, #2ecc71 100%);
                padding: 40px;
                border-radius: 12px;
                color: white;
                text-align: center;
                margin-top: 30px;
            }
            .loading {
                text-align: center;
                padding: 60px;
                color: #666;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📚 Onboarding</h1>
            <button class="btn btn-secondary" onclick="window.location.href='/onboarding-management'">
                ← Back to Paths
            </button>
        </div>
        <div class="container">
            <div id="content">
                <div class="loading">Loading onboarding path...</div>
            </div>
        </div>
        <script>
            const token = localStorage.getItem('access_token');
            if (!token) window.location.href = '/auth/login-page';
            
            const pathId = window.location.pathname.split('/').pop();
            let currentPath = null;
            let userProgress = null;
            
            async function loadPath() {
                try {
                    const pathResponse = await fetch('/onboarding/paths/' + pathId, {
                        headers: { 'Authorization': 'Bearer ' + token }
                    });
                    if (!pathResponse.ok) {
                        document.getElementById('content').innerHTML = '<div class="loading">Path not found</div>';
                        return;
                    }
                    currentPath = await pathResponse.json();
                    
                    const progressResponse = await fetch('/onboarding/progress/me', {
                        headers: { 'Authorization': 'Bearer ' + token }
                    });
                    if (progressResponse.ok) {
                        const progressList = await progressResponse.json();
                        userProgress = progressList.find(function(p) { return p.path_id === parseInt(pathId); });
                    }
                    
                    if (!userProgress) await startProgress();
                    renderOnboarding();
                } catch (error) {
                    console.error('Error:', error);
                    document.getElementById('content').innerHTML = '<div class="loading">Error loading onboarding</div>';
                }
            }
            
            async function startProgress() {
                try {
                    const meResponse = await fetch('/auth/me', {
                        headers: { 'Authorization': 'Bearer ' + token }
                    });
                    const me = await meResponse.json();
                    
                    const response = await fetch('/onboarding/progress/start', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + token
                        },
                        body: JSON.stringify({
                            path_id: parseInt(pathId),
                            user_id: me.id
                        })
                    });
                    if (response.ok) userProgress = await response.json();
                } catch (error) {
                    console.error('Error starting progress:', error);
                }
            }
            
            function renderOnboarding() {
                const steps = currentPath.steps_json && currentPath.steps_json.steps ? currentPath.steps_json.steps : [];
                const completedSteps = userProgress && userProgress.completed_steps ? userProgress.completed_steps : [];
                const totalSteps = steps.length;
                const completedCount = completedSteps.length;
                const percent = totalSteps > 0 ? Math.round((completedCount / totalSteps) * 100) : 0;
                const isComplete = completedCount >= totalSteps;
                
                let html = '<div class="progress-header">' +
                    '<h2>' + currentPath.name + '</h2>' +
                    '<div class="progress-bar-container"><div class="progress-bar" style="width: ' + percent + '%"></div></div>' +
                    '<div class="progress-text">' + completedCount + ' of ' + totalSteps + ' steps completed (' + percent + '%)</div>' +
                    '</div><div class="steps-container">';
                
                for (let i = 0; i < steps.length; i++) {
                    const step = steps[i];
                    const isCompleted = completedSteps.indexOf(i) !== -1;
                    const isActive = i === completedCount && !isComplete;
                    const stepClass = (isCompleted ? 'completed' : '') + ' ' + (isActive ? 'active' : '');
                    
                    html += '<div class="step-item ' + stepClass + '">' +
                        '<div class="step-number">' + (isCompleted ? '✓' : (i + 1)) + '</div>' +
                        '<div class="step-content">' +
                        '<div class="step-title">' + step.title + '</div>' +
                        '<div class="step-description">' + (step.description || 'No description') + '</div>' +
                        '<div class="step-actions"><label class="checkbox-label">' +
                        '<input type="checkbox" ' + (isCompleted ? 'checked' : '') + ' onchange="toggleStep(' + i + ', this.checked)">' +
                        ' Mark as complete</label></div></div></div>';
                }
                html += '</div>';
                
                if (isComplete) {
                    html += '<div class="completion-card"><h2>🎉 Congratulations!</h2><p>You have completed this onboarding path.</p></div>';
                }
                
                document.getElementById('content').innerHTML = html;
            }
            
            async function toggleStep(stepIndex, completed) {
                if (!userProgress) return;
                
                // Optimistic update
                var steps = userProgress.completed_steps ? userProgress.completed_steps.slice() : [];
                if (completed) {
                    if (steps.indexOf(stepIndex) === -1) {
                        steps.push(stepIndex);
                        steps.sort(function(a, b) { return a - b; });
                    }
                } else {
                    steps = steps.filter(function(s) { return s !== stepIndex; });
                }
                userProgress.completed_steps = steps;
                renderOnboarding();
                
                try {
                    const response = await fetch('/onboarding/progress/' + userProgress.id + '/step', {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': 'Bearer ' + token
                        },
                        body: JSON.stringify({
                            step_index: stepIndex,
                            completed: completed
                        })
                    });
                    
                    if (response.ok) {
                        const result = await response.json();
                        userProgress.completed_steps = result.completed_steps;
                        renderOnboarding();
                    }
                } catch (error) {
                    console.error('Error updating step:', error);
                    loadPath();
                }
            }
            
            loadPath();
        </script>
    </body>
    </html>
    """


@router.get("/cases-management", response_class=HTMLResponse)
def cases_management():
    """Case Studies Management Page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docent - Case Studies</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: #f5f7fa;
            }
            /* Mobile responsive */
            @media (max-width: 768px) {
                .header { padding: 15px 20px !important; flex-direction: column; gap: 10px; }
                .header h1 { font-size: 20px !important; }
                .container { padding: 0 15px !important; margin: 20px auto !important; }
                .stats { grid-template-columns: repeat(2, 1fr) !important; }
                .stat-card { padding: 15px !important; }
                .stat-card .value { font-size: 24px !important; }
                .quick-actions { grid-template-columns: repeat(2, 1fr) !important; }
                .action-btn { padding: 15px 10px !important; font-size: 12px !important; }
                table { font-size: 12px; }
                th, td { padding: 8px !important; }
                .btn { padding: 8px 12px !important; font-size: 12px !important; }
                .modal-content { width: 95% !important; padding: 20px !important; }
                .search-box { width: 100% !important; }
                .grid-2 { grid-template-columns: 1fr !important; }
            }
            @media (max-width: 480px) {
                .stats { grid-template-columns: 1fr !important; }
                .quick-actions { grid-template-columns: 1fr !important; }
            }
            .header {
                background: white;
                padding: 20px 40px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .header h1 { color: #2c3e50; font-size: 24px; }
            .container {
                max-width: 1200px;
                margin: 40px auto;
                padding: 0 20px;
            }
            .card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
                text-decoration: none;
                display: inline-block;
            }
            .btn-primary { background: #667eea; color: white; }
            .btn-primary:hover { background: #5568d3; }
            .btn-secondary { background: #e0e0e0; color: #333; }
            .btn-success { background: #27ae60; color: white; }
            .btn-danger { background: #e74c3c; color: white; }
            .stats {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 20px;
                border-radius: 12px;
            }
            .stat-card h3 { font-size: 14px; opacity: 0.9; margin-bottom: 10px; }
            .stat-card .value { font-size: 32px; font-weight: bold; }
            .templates-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .template-card {
                background: #f8f9fa;
                border: 2px solid #e0e0e0;
                border-radius: 12px;
                padding: 20px;
                cursor: pointer;
                transition: all 0.3s;
            }
            .template-card:hover {
                border-color: #667eea;
                transform: translateY(-2px);
            }
            .template-card.selected {
                border-color: #667eea;
                background: #f0f0ff;
            }
            .template-card h4 { color: #2c3e50; margin-bottom: 10px; }
            .template-card .sections { font-size: 12px; color: #666; }
            .template-card .badge {
                display: inline-block;
                padding: 2px 8px;
                background: #667eea;
                color: white;
                border-radius: 10px;
                font-size: 11px;
                margin-top: 10px;
            }
            table { width: 100%; border-collapse: collapse; margin-top: 20px; }
            th, td { padding: 12px; text-align: left; border-bottom: 1px solid #eee; }
            th { background: #f8f9fa; font-weight: 600; color: #2c3e50; }
            .modal {
                display: none;
                position: fixed;
                top: 0; left: 0;
                width: 100%; height: 100%;
                background: rgba(0,0,0,0.5);
                align-items: center;
                justify-content: center;
                z-index: 1000;
            }
            .modal-content {
                background: white;
                padding: 30px;
                border-radius: 12px;
                max-width: 700px;
                width: 90%;
                max-height: 85vh;
                overflow-y: auto;
            }
            .form-group { margin-bottom: 20px; }
            .form-group label { display: block; margin-bottom: 8px; font-weight: 600; color: #2c3e50; }
            .form-group input, .form-group textarea, .form-group select {
                width: 100%;
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                font-size: 14px;
            }
            .form-group textarea { min-height: 100px; resize: vertical; }
            .section-input { margin-bottom: 15px; padding: 15px; background: #f8f9fa; border-radius: 8px; }
            .section-input h5 { color: #667eea; margin-bottom: 10px; }
            .search-box {
                padding: 10px;
                border: 2px solid #e0e0e0;
                border-radius: 6px;
                width: 300px;
            }
            .empty-state {
                text-align: center;
                padding: 60px;
                color: #666;
            }
            .empty-state h3 { margin-bottom: 10px; color: #2c3e50; }
            
            /* Toast notifications */
            .toast-container {
                position: fixed;
                top: 20px;
                right: 20px;
                z-index: 9999;
            }
            .toast {
                background: #333;
                color: white;
                padding: 15px 25px;
                border-radius: 8px;
                margin-bottom: 10px;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
                animation: slideIn 0.3s ease;
                display: flex;
                align-items: center;
                gap: 10px;
            }
            .toast.success { background: #27ae60; }
            .toast.error { background: #e74c3c; }
            .toast.warning { background: #f39c12; }
            @keyframes slideIn {
                from { transform: translateX(100%); opacity: 0; }
                to { transform: translateX(0); opacity: 1; }
            }
            @keyframes slideOut {
                from { transform: translateX(0); opacity: 1; }
                to { transform: translateX(100%); opacity: 0; }
            }

        </style>
    </head>
    <body>
        <div class="header">
            <h1>📋 Case Studies</h1>
            <button class="btn btn-secondary" onclick="window.location.href='/dashboard'">← Back to Dashboard</button>
        </div>
        
        <div class="container">
            <!-- Stats -->
            <div class="stats">
                <div class="stat-card">
                    <h3>Total Cases</h3>
                    <div class="value" id="statTotal"><span class="loading-text">...</span></div>
                </div>
                <div class="stat-card">
                    <h3>This Month</h3>
                    <div class="value" id="statMonth"><span class="loading-text">...</span></div>
                </div>
            </div>
            
            <!-- Templates Section -->
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2>📝 Create New Case</h2>
                </div>
                <p style="color: #666; margin-bottom: 20px;">Select a template to start a new case study:</p>
                <div class="templates-grid" id="templatesGrid">
                    <div style="text-align: center; padding: 20px; color: #666;">Loading templates...</div>
                </div>
                <button class="btn btn-primary" id="createCaseBtn" style="display: none;" onclick="showCreateModal()">
                    Create Case Study →
                </button>
            </div>
            
            <!-- Cases List -->
            <div class="card">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 20px;">
                    <h2>📚 Your Case Studies</h2>
                    <input type="text" id="searchBox" class="search-box" placeholder="Search cases...">
                </div>
                <div id="casesContainer">
                    <table>
                        <thead>
                            <tr>
                                <th>Title</th>
                                <th>Template</th>
                                <th>Created By</th>
                                <th>Date</th>
                                <th>Actions</th>
                            </tr>
                        </thead>
                        <tbody id="casesTableBody">
                            <tr><td colspan="5" style="text-align: center;">Loading...</td></tr>
                        </tbody>
                    </table>
                </div>
            </div>
        </div>
        
        <!-- Create Case Modal -->
        <div id="createModal" class="modal">
            <div class="modal-content">
                <h3 style="margin-bottom: 20px;">📋 New Case Study</h3>
                <form id="createCaseForm">
                    <div class="form-group">
                        <label>Title</label>
                        <input type="text" id="caseTitle" required placeholder="e.g., Q4 Product Launch Review">
                    </div>
                    <div id="sectionsContainer"></div>
                    <div class="form-group">
                        <label>Link Documents (Optional)</label>
                        <select id="linkedDocs" multiple style="height: 100px;">
                        </select>
                        <small style="color: #666;">Hold Ctrl/Cmd to select multiple</small>
                    </div>
                    <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px;">
                        <button type="button" class="btn btn-secondary" onclick="closeCreateModal()">Cancel</button>
                        <button type="submit" class="btn btn-primary">Create Case</button>
                    </div>
                </form>
            </div>
        </div>
        
        <!-- View Case Modal -->
        <div id="viewModal" class="modal">
            <div class="modal-content">
                <div id="viewCaseContent"></div>
                <div style="display: flex; gap: 10px; justify-content: flex-end; margin-top: 20px;">
                    <button class="btn btn-success" onclick="generateSummary()">Generate AI Summary</button>
                    <button class="btn btn-secondary" onclick="closeViewModal()">Close</button>
                </div>
            </div>
        </div>
        
        <script>
            const token = localStorage.getItem('access_token');
            let templates = [];
            let selectedTemplate = null;
            let currentViewingCase = null;
            let documents = [];
            
            if (!token) {
                window.location.href = '/auth/login-page';
            }
            
            // Load stats
            async function loadStats() {
                try {
                    const response = await fetch('/cases/stats', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (response.ok) {
                        const stats = await response.json();
                        document.getElementById('statTotal').textContent = stats.total_cases;
                        document.getElementById('statMonth').textContent = stats.cases_this_month;
                    }
                } catch (error) {
                    console.error('Error loading stats:', error);
                }
            }
            
            // Load templates
            async function loadTemplates() {
                try {
                    const response = await fetch('/cases/templates', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (response.ok) {
                        templates = await response.json();
                        renderTemplates();
                    }
                } catch (error) {
                    console.error('Error loading templates:', error);
                }
            }
            
            function renderTemplates() {
                const grid = document.getElementById('templatesGrid');
                if (templates.length === 0) {
                    grid.innerHTML = '<div class="empty-state"><h3>No templates available</h3></div>';
                    return;
                }
                
                grid.innerHTML = templates.map(t => {
                    const sections = t.template_json.sections || [];
                    return `
                        <div class="template-card ${selectedTemplate?.id === t.id ? 'selected' : ''}" 
                             onclick="selectTemplate(${t.id})">
                            <h4>${t.name}</h4>
                            <div class="sections">${sections.length} sections: ${sections.slice(0,3).join(', ')}${sections.length > 3 ? '...' : ''}</div>
                            ${t.is_default ? '<span class="badge">Default</span>' : ''}
                        </div>
                    `;
                }).join('');
            }
            
            function selectTemplate(templateId) {
                selectedTemplate = templates.find(t => t.id === templateId);
                renderTemplates();
                document.getElementById('createCaseBtn').style.display = 'inline-block';
            }
            
            // Load documents for linking
            async function loadDocuments() {
                try {
                    const response = await fetch('/documents/?page_size=100', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (response.ok) {
                        const data = await response.json();
                        documents = data.documents.filter(d => d.status === 'processed');
                        
                        const select = document.getElementById('linkedDocs');
                        select.innerHTML = documents.map(d => 
                            `<option value="${d.id}">${d.filename}</option>`
                        ).join('');
                    }
                } catch (error) {
                    console.error('Error loading documents:', error);
                }
            }
            
            // Show create modal
            function showCreateModal() {
                if (!selectedTemplate) {
                    alert('Please select a template first');
                    return;
                }
                
                const sections = selectedTemplate.template_json.sections || [];
                const container = document.getElementById('sectionsContainer');
                container.innerHTML = sections.map((s, i) => `
                    <div class="section-input">
                        <h5>${s}</h5>
                        <textarea id="section_${i}" placeholder="Enter content for ${s}..." required></textarea>
                    </div>
                `).join('');
                
                document.getElementById('createModal').style.display = 'flex';
            }
            
            function closeCreateModal() {
                document.getElementById('createModal').style.display = 'none';
                document.getElementById('createCaseForm').reset();
            }
            
            // Create case
            document.getElementById('createCaseForm').addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const title = document.getElementById('caseTitle').value;
                const sections = selectedTemplate.template_json.sections || [];
                const sectionsData = sections.map((s, i) => ({
                    section_name: s,
                    content: document.getElementById(`section_${i}`).value
                }));
                
                const linkedDocsSelect = document.getElementById('linkedDocs');
                const linkedDocs = Array.from(linkedDocsSelect.selectedOptions).map(o => parseInt(o.value));
                
                try {
                    const response = await fetch('/cases/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({
                            template_id: selectedTemplate.id,
                            title: title,
                            sections_data: sectionsData,
                            linked_document_ids: linkedDocs
                        })
                    });
                    
                    if (response.ok) {
                        showToast('Case study created!', 'success');
                        closeCreateModal();
                        loadCases();
                        loadStats();
                        selectedTemplate = null;
                        document.getElementById('createCaseBtn').style.display = 'none';
                        renderTemplates();
                    } else {
                        const error = await response.json();
                        alert('Error: ' + (error.detail || 'Failed to create case'));
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            });
            
            // Load cases
            async function loadCases(search = '') {
                try {
                    const response = await fetch(`/cases/?search=${encodeURIComponent(search)}`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (response.ok) {
                        const data = await response.json();
                        renderCases(data.cases);
                    }
                } catch (error) {
                    console.error('Error loading cases:', error);
                }
            }
            
            function renderCases(cases) {
                const tbody = document.getElementById('casesTableBody');
                if (cases.length === 0) {
                    tbody.innerHTML = '<tr><td colspan="5" class="empty-state"><h3>No case studies yet</h3><p>Select a template above to create your first case study</p></td></tr>';
                    return;
                }
                
                tbody.innerHTML = cases.map(c => {
                    const date = new Date(c.created_at).toLocaleDateString();
                    return `
                        <tr>
                            <td><strong>${c.title}</strong></td>
                            <td>${c.template_name}</td>
                            <td>${c.creator_name}</td>
                            <td>${date}</td>
                            <td>
                                <button class="btn btn-secondary" style="padding: 5px 10px; font-size: 12px; margin-right: 5px;" 
                                        onclick="viewCase(${c.id})">View</button>
                                <button class="btn btn-danger" style="padding: 5px 10px; font-size: 12px;" 
                                        onclick="deleteCase(${c.id})">Delete</button>
                            </td>
                        </tr>
                    `;
                }).join('');
            }
            
            // Search
            let searchTimeout;
            document.getElementById('searchBox').addEventListener('input', (e) => {
                clearTimeout(searchTimeout);
                searchTimeout = setTimeout(() => loadCases(e.target.value), 500);
            });
            
            // View case
            async function viewCase(caseId) {
                try {
                    const response = await fetch(`/cases/${caseId}`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (response.ok) {
                        const caseData = await response.json();
                        currentViewingCase = caseData;
                        
                        const sections = caseData.data_json.sections || {};
                        let sectionsHtml = '';
                        for (const [name, content] of Object.entries(sections)) {
                            sectionsHtml += `
                                <div style="margin-bottom: 20px;">
                                    <h4 style="color: #667eea; margin-bottom: 8px;">${name}</h4>
                                    <p style="white-space: pre-wrap; background: #f8f9fa; padding: 15px; border-radius: 8px;">${content}</p>
                                </div>
                            `;
                        }
                        
                        document.getElementById('viewCaseContent').innerHTML = `
                            <h2 style="margin-bottom: 10px;">${caseData.title}</h2>
                            <p style="color: #666; margin-bottom: 20px;">Template: ${caseData.template_name} | By: ${caseData.creator_name} | ${new Date(caseData.created_at).toLocaleDateString()}</p>
                            ${sectionsHtml}
                            ${caseData.generated_summary ? `
                                <div style="margin-top: 20px; padding: 20px; background: #e8f5e9; border-radius: 8px;">
                                    <h4 style="color: #27ae60; margin-bottom: 10px;">📝 AI Summary</h4>
                                    <p style="white-space: pre-wrap;">${caseData.generated_summary}</p>
                                </div>
                            ` : ''}
                        `;
                        
                        document.getElementById('viewModal').style.display = 'flex';
                    }
                } catch (error) {
                    alert('Error loading case: ' + error.message);
                }
            }
            
            function closeViewModal() {
                document.getElementById('viewModal').style.display = 'none';
                currentViewingCase = null;
            }
            
            // Generate summary
            async function generateSummary() {
                if (!currentViewingCase) return;
                
                try {
                    const response = await fetch(`/cases/${currentViewingCase.id}/generate-summary`, {
                        method: 'POST',
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    
                    if (response.ok) {
                        showToast('Summary generated!', 'success');
                        viewCase(currentViewingCase.id);
                    } else {
                        showToast('Failed to generate summary', 'error');
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
            
            // Delete case
            async function deleteCase(caseId) {
                if (!confirm('Are you sure you want to delete this case study?')) return;
                
                try {
                    const response = await fetch(`/cases/${caseId}`, {
                        method: 'DELETE',
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    
                    if (response.ok) {
                        showToast('Case deleted', 'success');
                        loadCases();
                        loadStats();
                    } else {
                        showToast('Failed to delete case', 'error');
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
            
            // Initialize
            loadStats();
            loadTemplates();
            loadDocuments();
            loadCases();
        </script>
    </body>
    </html>
    """


@router.get("/analytics-dashboard", response_class=HTMLResponse)
def analytics_dashboard():
    """Analytics Dashboard Page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docent - Analytics</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: #f5f7fa;
            }
            /* Mobile responsive */
            @media (max-width: 768px) {
                .header { padding: 15px 20px !important; flex-direction: column; gap: 10px; }
                .header h1 { font-size: 20px !important; }
                .container { padding: 0 15px !important; margin: 20px auto !important; }
                .stats { grid-template-columns: repeat(2, 1fr) !important; }
                .stat-card { padding: 15px !important; }
                .stat-card .value { font-size: 24px !important; }
                .quick-actions { grid-template-columns: repeat(2, 1fr) !important; }
                .action-btn { padding: 15px 10px !important; font-size: 12px !important; }
                table { font-size: 12px; }
                th, td { padding: 8px !important; }
                .btn { padding: 8px 12px !important; font-size: 12px !important; }
                .modal-content { width: 95% !important; padding: 20px !important; }
                .search-box { width: 100% !important; }
                .grid-2 { grid-template-columns: 1fr !important; }
            }
            @media (max-width: 480px) {
                .stats { grid-template-columns: 1fr !important; }
                .quick-actions { grid-template-columns: 1fr !important; }
            }
            .header {
                background: white;
                padding: 20px 40px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .header h1 { color: #2c3e50; font-size: 24px; }
            .container {
                max-width: 1400px;
                margin: 40px auto;
                padding: 0 20px;
            }
            .stats-row {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }
            .stat-card {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                color: white;
                padding: 25px;
                border-radius: 12px;
            }
            .stat-card.blue { background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%); }
            .stat-card.green { background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%); }
            .stat-card.orange { background: linear-gradient(135deg, #fa709a 0%, #fee140 100%); }
            .stat-card.purple { background: linear-gradient(135deg, #a18cd1 0%, #fbc2eb 100%); }
            .stat-card h3 { font-size: 14px; opacity: 0.9; margin-bottom: 10px; }
            .stat-card .value { font-size: 36px; font-weight: bold; }
            .stat-card .sub { font-size: 12px; opacity: 0.8; margin-top: 5px; }
            .card {
                background: white;
                padding: 25px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .card h2 { color: #2c3e50; margin-bottom: 20px; font-size: 18px; }
            .grid-2 {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(400px, 1fr));
                gap: 20px;
            }
            .chart-container {
                height: 250px;
                display: flex;
                align-items: flex-end;
                gap: 8px;
                padding: 20px 0;
            }
            .bar {
                flex: 1;
                background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
                border-radius: 4px 4px 0 0;
                min-height: 10px;
                position: relative;
                transition: all 0.3s;
            }
            .bar:hover { opacity: 0.8; }
            .bar .tooltip {
                position: absolute;
                bottom: 100%;
                left: 50%;
                transform: translateX(-50%);
                background: #333;
                color: white;
                padding: 5px 10px;
                border-radius: 4px;
                font-size: 12px;
                white-space: nowrap;
                display: none;
            }
            .bar:hover .tooltip { display: block; }
            .list-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 12px 0;
                border-bottom: 1px solid #eee;
            }
            .list-item:last-child { border-bottom: none; }
            .list-item .query { color: #2c3e50; font-weight: 500; }
            .list-item .count {
                background: #667eea;
                color: white;
                padding: 4px 12px;
                border-radius: 12px;
                font-size: 12px;
            }
            .activity-item {
                display: flex;
                gap: 15px;
                padding: 12px 0;
                border-bottom: 1px solid #eee;
            }
            .activity-item:last-child { border-bottom: none; }
            .activity-icon {
                width: 40px;
                height: 40px;
                border-radius: 50%;
                background: #f0f0f0;
                display: flex;
                align-items: center;
                justify-content: center;
                font-size: 18px;
            }
            .activity-content { flex: 1; }
            .activity-content .action { color: #2c3e50; font-weight: 500; }
            .activity-content .meta { color: #999; font-size: 12px; margin-top: 4px; }
            .type-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(100px, 1fr));
                gap: 15px;
            }
            .type-item {
                text-align: center;
                padding: 15px;
                background: #f8f9fa;
                border-radius: 8px;
            }
            .type-item .ext { font-size: 24px; font-weight: bold; color: #667eea; }
            .type-item .count { color: #666; font-size: 14px; }
            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
            }
            .btn-secondary { background: #e0e0e0; color: #333; }
            .period-selector {
                display: flex;
                gap: 10px;
                margin-bottom: 20px;
            }
            .period-btn {
                padding: 8px 16px;
                border: 2px solid #e0e0e0;
                background: white;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
            }
            .period-btn.active {
                border-color: #667eea;
                background: #f0f0ff;
                color: #667eea;
            }
            .empty-state {
                text-align: center;
                padding: 40px;
                color: #999;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📊 Analytics Dashboard</h1>
            <button class="btn btn-secondary" onclick="window.location.href='/dashboard'">← Back to Dashboard</button>
        </div>
        
        <div class="container">
            <!-- Period Selector -->
            <div class="period-selector">
                <button class="period-btn" onclick="setPeriod(7)">7 Days</button>
                <button class="period-btn active" onclick="setPeriod(30)">30 Days</button>
                <button class="period-btn" onclick="setPeriod(90)">90 Days</button>
            </div>
            
            <!-- Summary Stats -->
            <div class="stats-row">
                <div class="stat-card">
                    <h3>🔍 Total Searches</h3>
                    <div class="value" id="totalSearches"><span class="loading-text">...</span></div>
                    <div class="sub" id="searchesToday">- today</div>
                </div>
                <div class="stat-card blue">
                    <h3>📄 Documents</h3>
                    <div class="value" id="totalDocs"><span class="loading-text">...</span></div>
                    <div class="sub" id="processedDocs">- processed</div>
                </div>
                <div class="stat-card green">
                    <h3>👥 Users</h3>
                    <div class="value" id="totalUsers"><span class="loading-text">...</span></div>
                    <div class="sub" id="activeUsers">- active this week</div>
                </div>
                <div class="stat-card orange">
                    <h3>📋 Case Studies</h3>
                    <div class="value" id="totalCases"><span class="loading-text">...</span></div>
                    <div class="sub">knowledge captured</div>
                </div>
            </div>
            
            <!-- Charts Row -->
            <div class="grid-2">
                <!-- Search Trend -->
                <div class="card">
                    <h2>📈 Search Activity</h2>
                    <div class="chart-container" id="searchChart">
                        <div class="empty-state">Loading...</div>
                    </div>
                </div>
                
                <!-- Top Queries -->
                <div class="card">
                    <h2>🔝 Top Search Queries</h2>
                    <div id="topQueries">
                        <div class="empty-state">Loading...</div>
                    </div>
                </div>
            </div>
            
            <div class="grid-2">
                <!-- Document Types -->
                <div class="card">
                    <h2>📁 Documents by Type</h2>
                    <div class="type-grid" id="docTypes">
                        <div class="empty-state">Loading...</div>
                    </div>
                </div>
                
                <!-- Upload Trend -->
                <div class="card">
                    <h2>📤 Upload Activity</h2>
                    <div class="chart-container" id="uploadChart">
                        <div class="empty-state">Loading...</div>
                    </div>
                </div>
            </div>
            
            <!-- Recent Activity -->
            <div class="card">
                <h2>🕐 Recent Activity</h2>
                <div id="recentActivity">
                    <div class="empty-state">Loading...</div>
                </div>
            </div>
        </div>
        
        <script>
            const token = localStorage.getItem('access_token');
            let currentPeriod = 30;
            // Export analytics to CSV
            function exportAnalytics() {
                if (!analyticsData) {
                    alert('No data to export');
                    return;
                }
                
                let csv = 'Analytics Report\n\n';
                csv += 'Summary\n';
                csv += 'Metric,Value\n';
                csv += `Total Searches,${analyticsData.search?.total_searches || 0}\n`;
                csv += `Searches Today,${analyticsData.search?.searches_today || 0}\n`;
                csv += `Total Documents,${analyticsData.documents?.total_documents || 0}\n`;
                csv += `Processed Documents,${analyticsData.documents?.processed_documents || 0}\n`;
                csv += `Total Users,${analyticsData.users?.total_users || 0}\n`;
                csv += `Active Users,${analyticsData.users?.active_users || 0}\n`;
                csv += '\n';
                
                if (analyticsData.search?.top_queries?.length) {
                    csv += 'Top Search Queries\n';
                    csv += 'Query,Count\n';
                    analyticsData.search.top_queries.forEach(q => {
                        csv += `"${q.query}",${q.count}\n`;
                    });
                    csv += '\n';
                }
                
                if (analyticsData.documents?.documents_by_type) {
                    csv += 'Documents by Type\n';
                    csv += 'Type,Count\n';
                    Object.entries(analyticsData.documents.documents_by_type).forEach(([type, count]) => {
                        csv += `${type},${count}\n`;
                    });
                }
                
                // Download
                const blob = new Blob([csv], { type: 'text/csv' });
                const url = window.URL.createObjectURL(blob);
                const a = document.createElement('a');
                a.href = url;
                a.download = `analytics_${new Date().toISOString().split('T')[0]}.csv`;
                document.body.appendChild(a);
                a.click();
                document.body.removeChild(a);
                window.URL.revokeObjectURL(url);
            }
            
            let analyticsData = null;

            
            if (!token) {
                window.location.href = '/auth/login-page';
            }
            
            function setPeriod(days) {
                currentPeriod = days;
                document.querySelectorAll('.period-btn').forEach(btn => btn.classList.remove('active'));
                event.target.classList.add('active');
                loadAnalytics();
            }
            
            async function loadAnalytics() {
                try {
                    const response = await fetch(`/analytics/dashboard?days=${currentPeriod}`, {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    
                    if (response.ok) {
                        const data = await response.json();
                        renderAnalytics(data);
                    }
                } catch (error) {
                    console.error('Error loading analytics:', error);
                }
                
                // Also load summary for cases
                try {
                    const response = await fetch('/analytics/summary', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (response.ok) {
                        const summary = await response.json();
                        document.getElementById('totalCases').textContent = summary.total_cases;
                    }
                } catch (error) {
                    console.error('Error loading summary:', error);
                }
            }
            
            function renderAnalytics(data) {
                // Summary stats
                document.getElementById('totalSearches').textContent = data.search.total_searches;
                document.getElementById('searchesToday').textContent = data.search.searches_today + ' today';
                document.getElementById('totalDocs').textContent = data.documents.total_documents;
                document.getElementById('processedDocs').textContent = data.documents.processed_documents + ' processed';
                document.getElementById('totalUsers').textContent = data.users.total_users;
                document.getElementById('activeUsers').textContent = data.users.active_users + ' active this week';
                
                // Search chart
                renderBarChart('searchChart', data.search.searches_by_day, 'count', 'date');
                
                // Upload chart
                renderBarChart('uploadChart', data.documents.uploads_by_day, 'count', 'date');
                
                // Top queries
                renderTopQueries(data.search.top_queries);
                
                // Document types
                renderDocTypes(data.documents.documents_by_type);
                
                // Recent activity
                renderRecentActivity(data.recent_activity);
            }
            
            function renderBarChart(containerId, data, valueKey, labelKey) {
                const container = document.getElementById(containerId);
                
                if (!data || data.length === 0) {
                    container.innerHTML = '<div class="empty-state">No data for this period</div>';
                    return;
                }
                
                const maxValue = Math.max(...data.map(d => d[valueKey]));
                
                container.innerHTML = data.map(d => {
                    const height = maxValue > 0 ? (d[valueKey] / maxValue) * 200 : 10;
                    const label = d[labelKey].split('-').slice(1).join('/');
                    return `
                        <div class="bar" style="height: ${height}px;">
                            <div class="tooltip">${label}: ${d[valueKey]}</div>
                        </div>
                    `;
                }).join('');
            }
            
            function renderTopQueries(queries) {
                const container = document.getElementById('topQueries');
                
                if (!queries || queries.length === 0) {
                    container.innerHTML = '<div class="empty-state">No searches yet</div>';
                    return;
                }
                
                container.innerHTML = queries.map(q => `
                    <div class="list-item">
                        <span class="query">"${q.query}"</span>
                        <span class="count">${q.count} searches</span>
                    </div>
                `).join('');
            }
            
            function renderDocTypes(types) {
                const container = document.getElementById('docTypes');
                
                if (!types || Object.keys(types).length === 0) {
                    container.innerHTML = '<div class="empty-state">No documents yet</div>';
                    return;
                }
                
                container.innerHTML = Object.entries(types).map(([ext, count]) => `
                    <div class="type-item">
                        <div class="ext">${ext}</div>
                        <div class="count">${count} files</div>
                    </div>
                `).join('');
            }
            
            function renderRecentActivity(activities) {
                const container = document.getElementById('recentActivity');
                
                if (!activities || activities.length === 0) {
                    container.innerHTML = '<div class="empty-state">No recent activity</div>';
                    return;
                }
                
                const icons = {
                    'search': '🔍',
                    'upload': '📤',
                    'login': '🔐',
                    'document': '📄',
                    'case': '📋',
                    'default': '📌'
                };
                
                container.innerHTML = activities.slice(0, 10).map(a => {
                    const icon = Object.entries(icons).find(([k]) => a.action.toLowerCase().includes(k))?.[1] || icons.default;
                    const time = new Date(a.timestamp).toLocaleString();
                    return `
                        <div class="activity-item">
                            <div class="activity-icon">${icon}</div>
                            <div class="activity-content">
                                <div class="action">${a.action}</div>
                                <div class="meta">${a.user_name || 'System'} • ${time}</div>
                            </div>
                        </div>
                    `;
                }).join('');
            }
            
            // Initialize
            loadAnalytics();
        </script>
    </body>
    </html>
    """


@router.get("/settings", response_class=HTMLResponse)
def settings_page():
    """User Settings Page with Notification Preferences"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docent - Settings</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: #f5f7fa;
            }
            /* Mobile responsive */
            @media (max-width: 768px) {
                .header { padding: 15px 20px !important; flex-direction: column; gap: 10px; }
                .header h1 { font-size: 20px !important; }
                .container { padding: 0 15px !important; margin: 20px auto !important; }
                .stats { grid-template-columns: repeat(2, 1fr) !important; }
                .stat-card { padding: 15px !important; }
                .stat-card .value { font-size: 24px !important; }
                .quick-actions { grid-template-columns: repeat(2, 1fr) !important; }
                .action-btn { padding: 15px 10px !important; font-size: 12px !important; }
                table { font-size: 12px; }
                th, td { padding: 8px !important; }
                .btn { padding: 8px 12px !important; font-size: 12px !important; }
                .modal-content { width: 95% !important; padding: 20px !important; }
                .search-box { width: 100% !important; }
                .grid-2 { grid-template-columns: 1fr !important; }
            }
            @media (max-width: 480px) {
                .stats { grid-template-columns: 1fr !important; }
                .quick-actions { grid-template-columns: 1fr !important; }
            }
            .header {
                background: white;
                padding: 20px 40px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .header h1 { color: #2c3e50; font-size: 24px; }
            .container {
                max-width: 800px;
                margin: 40px auto;
                padding: 0 20px;
            }
            .card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .card h2 { color: #2c3e50; margin-bottom: 20px; font-size: 18px; }
            .setting-item {
                display: flex;
                justify-content: space-between;
                align-items: center;
                padding: 15px 0;
                border-bottom: 1px solid #eee;
            }
            .setting-item:last-child { border-bottom: none; }
            .setting-info h4 { color: #2c3e50; margin-bottom: 5px; }
            .setting-info p { color: #666; font-size: 14px; }
            .toggle {
                position: relative;
                width: 50px;
                height: 26px;
            }
            .toggle input {
                opacity: 0;
                width: 0;
                height: 0;
            }
            .toggle-slider {
                position: absolute;
                cursor: pointer;
                top: 0; left: 0; right: 0; bottom: 0;
                background-color: #ccc;
                transition: .3s;
                border-radius: 26px;
            }
            .toggle-slider:before {
                position: absolute;
                content: "";
                height: 20px;
                width: 20px;
                left: 3px;
                bottom: 3px;
                background-color: white;
                transition: .3s;
                border-radius: 50%;
            }
            .toggle input:checked + .toggle-slider {
                background-color: #667eea;
            }
            .toggle input:checked + .toggle-slider:before {
                transform: translateX(24px);
            }
            .btn {
                padding: 10px 20px;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                font-size: 14px;
                font-weight: 600;
            }
            .btn-primary { background: #667eea; color: white; }
            .btn-secondary { background: #e0e0e0; color: #333; }
            .btn-success { background: #27ae60; color: white; }
            .user-info {
                display: flex;
                align-items: center;
                gap: 20px;
                padding: 20px;
                background: #f8f9fa;
                border-radius: 8px;
                margin-bottom: 20px;
            }
            .user-avatar {
                width: 60px;
                height: 60px;
                border-radius: 50%;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                display: flex;
                align-items: center;
                justify-content: center;
                color: white;
                font-size: 24px;
                font-weight: bold;
            }
            .user-details h3 { color: #2c3e50; }
            .user-details p { color: #666; font-size: 14px; }
            .actions { margin-top: 20px; display: flex; gap: 10px; }
            .success-msg {
                background: #d4edda;
                color: #155724;
                padding: 10px 15px;
                border-radius: 6px;
                margin-bottom: 20px;
                display: none;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>⚙️ Settings</h1>
            <button class="btn btn-secondary" onclick="window.location.href='/dashboard'">← Back to Dashboard</button>
        </div>
        
        <div class="container">
            <div id="successMsg" class="success-msg">Settings saved successfully!</div>
            
            <!-- User Profile -->
            <div class="card">
                <h2>👤 Profile</h2>
                <div class="user-info">
                    <div class="user-avatar" id="userAvatar">?</div>
                    <div class="user-details">
                        <h3 id="userName">Loading...</h3>
                        <p id="userEmail">Loading...</p>
                        <p id="userCompany" style="color: #667eea;"></p>
                    </div>
                </div>
            </div>
            
            <!-- Notification Preferences -->
            <div class="card">
                <h2>🔔 Email Notifications</h2>
                
                <div class="setting-item">
                    <div class="setting-info">
                        <h4>Document Processing</h4>
                        <p>Get notified when your documents are processed</p>
                    </div>
                    <label class="toggle">
                        <input type="checkbox" id="pref_document" onchange="savePreferences()">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
                
                <div class="setting-item">
                    <div class="setting-info">
                        <h4>New Case Studies</h4>
                        <p>Get notified when new case studies are added</p>
                    </div>
                    <label class="toggle">
                        <input type="checkbox" id="pref_case" onchange="savePreferences()">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
                
                <div class="setting-item">
                    <div class="setting-info">
                        <h4>Weekly Digest</h4>
                        <p>Receive a weekly summary of activity</p>
                    </div>
                    <label class="toggle">
                        <input type="checkbox" id="pref_digest" onchange="savePreferences()">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
                
                <div class="setting-item">
                    <div class="setting-info">
                        <h4>Onboarding Reminders</h4>
                        <p>Get reminders about incomplete onboarding</p>
                    </div>
                    <label class="toggle">
                        <input type="checkbox" id="pref_onboarding" onchange="savePreferences()">
                        <span class="toggle-slider"></span>
                    </label>
                </div>
            </div>
            
            <!-- Test Actions -->
            <div class="card">
                <h2>🧪 Test Notifications</h2>
                <p style="color: #666; margin-bottom: 20px;">Send test emails to verify your notification settings.</p>
                <div class="actions">
                    <button class="btn btn-primary" onclick="sendTestEmail()">Send Test Email</button>
                    <button class="btn btn-success" onclick="sendDigest()">Send Weekly Digest</button>
                </div>
            </div>
        </div>
        
        <script>
            const token = localStorage.getItem('access_token');
            
            if (!token) {
                window.location.href = '/auth/login-page';
            }
            
            // Load user info
            async function loadUserInfo() {
                try {
                    const response = await fetch('/auth/me', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (response.ok) {
                        const user = await response.json();
                        document.getElementById('userName').textContent = user.name;
                        document.getElementById('userEmail').textContent = user.email;
                        document.getElementById('userAvatar').textContent = user.name.charAt(0).toUpperCase();
                        if (user.company_id) {
                            document.getElementById('userCompany').textContent = 'Company ID: ' + user.company_id;
                        }
                    }
                } catch (error) {
                    console.error('Error loading user:', error);
                }
            }
            
            // Load preferences
            async function loadPreferences() {
                try {
                    const response = await fetch('/notifications/preferences', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (response.ok) {
                        const prefs = await response.json();
                        document.getElementById('pref_document').checked = prefs.email_on_document_processed;
                        document.getElementById('pref_case').checked = prefs.email_on_new_case;
                        document.getElementById('pref_digest').checked = prefs.email_weekly_digest;
                        document.getElementById('pref_onboarding').checked = prefs.email_onboarding_reminders;
                    }
                } catch (error) {
                    console.error('Error loading preferences:', error);
                }
            }
            
            // Save preferences
            async function savePreferences() {
                try {
                    const response = await fetch('/notifications/preferences', {
                        method: 'PUT',
                        headers: {
                            'Content-Type': 'application/json',
                            'Authorization': `Bearer ${token}`
                        },
                        body: JSON.stringify({
                            email_on_document_processed: document.getElementById('pref_document').checked,
                            email_on_new_case: document.getElementById('pref_case').checked,
                            email_weekly_digest: document.getElementById('pref_digest').checked,
                            email_onboarding_reminders: document.getElementById('pref_onboarding').checked
                        })
                    });
                    
                    if (response.ok) {
                        showSuccess();
                    }
                } catch (error) {
                    console.error('Error saving preferences:', error);
                }
            }
            
            function showSuccess() {
                const msg = document.getElementById('successMsg');
                msg.style.display = 'block';
                setTimeout(() => { msg.style.display = 'none'; }, 3000);
            }
            
            // Send test email
            async function sendTestEmail() {
                try {
                    const response = await fetch('/notifications/test-email', {
                        method: 'POST',
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (response.ok) {
                        showToast('Test email sent!', 'success');
                    } else {
                        showToast('Failed to send test email', 'error');
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
            
            // Send weekly digest
            async function sendDigest() {
                try {
                    const response = await fetch('/notifications/send-digest', {
                        method: 'POST',
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (response.ok) {
                        const data = await response.json();
                        showToast('Weekly digest sent!', 'success');
                    } else {
                        showToast('Failed to send digest', 'error');
                    }
                } catch (error) {
                    alert('Error: ' + error.message);
                }
            }
            
            // Initialize
            loadUserInfo();
            loadPreferences();
        </script>
    </body>
    </html>
    """

@router.get("/help", response_class=HTMLResponse)
def help_page():
    """Help and documentation page"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Docent - Help & Documentation</title>
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; }
            body {
                font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Arial, sans-serif;
                background: #f5f7fa;
                line-height: 1.6;
            }
            .header {
                background: white;
                padding: 20px 40px;
                box-shadow: 0 2px 4px rgba(0,0,0,0.1);
                display: flex;
                justify-content: space-between;
                align-items: center;
            }
            .header h1 { color: #2c3e50; font-size: 24px; }
            .container {
                max-width: 900px;
                margin: 40px auto;
                padding: 0 20px;
            }
            .card {
                background: white;
                padding: 30px;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
                margin-bottom: 20px;
            }
            .card h2 {
                color: #2c3e50;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 2px solid #667eea;
            }
            .card h3 {
                color: #34495e;
                margin: 20px 0 10px;
            }
            .feature-grid {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-top: 20px;
            }
            .feature-item {
                background: #f8f9fa;
                padding: 20px;
                border-radius: 8px;
                border-left: 4px solid #667eea;
            }
            .feature-item h4 {
                color: #667eea;
                margin-bottom: 10px;
            }
            .shortcut-table {
                width: 100%;
                border-collapse: collapse;
                margin-top: 15px;
            }
            .shortcut-table th, .shortcut-table td {
                padding: 12px;
                text-align: left;
                border-bottom: 1px solid #eee;
            }
            .shortcut-table th {
                background: #f8f9fa;
                font-weight: 600;
            }
            kbd {
                background: #eee;
                padding: 3px 8px;
                border-radius: 4px;
                font-family: monospace;
                border: 1px solid #ccc;
            }
            .btn {
                padding: 10px 20px;
                background: #667eea;
                color: white;
                border: none;
                border-radius: 6px;
                cursor: pointer;
                text-decoration: none;
                display: inline-block;
            }
            .faq-item {
                margin-bottom: 15px;
            }
            .faq-item strong {
                color: #2c3e50;
            }
            .version-info {
                text-align: center;
                color: #999;
                margin-top: 30px;
                padding: 20px;
            }
        </style>
    </head>
    <body>
        <div class="header">
            <h1>📚 Help & Documentation</h1>
            <a href="/dashboard" class="btn">← Back to Dashboard</a>
        </div>
        
        <div class="container">
            <!-- Getting Started -->
            <div class="card">
                <h2>🚀 Getting Started</h2>
                <p>Welcome to Docent - your AI-powered knowledge retention platform. Here's how to get started:</p>
                
                <div class="feature-grid">
                    <div class="feature-item">
                        <h4>1. Upload Documents</h4>
                        <p>Go to Documents and upload PDF, DOCX, PPTX, XLSX, or TXT files. Max 50MB each.</p>
                    </div>
                    <div class="feature-item">
                        <h4>2. Process Documents</h4>
                        <p>Click "Process" to extract text and create searchable embeddings.</p>
                    </div>
                    <div class="feature-item">
                        <h4>3. Search Knowledge</h4>
                        <p>Use AI-powered semantic search to find relevant information instantly.</p>
                    </div>
                    <div class="feature-item">
                        <h4>4. Create Case Studies</h4>
                        <p>Document important projects using templates and link related documents.</p>
                    </div>
                </div>
            </div>
            
            <!-- Features -->
            <div class="card">
                <h2>✨ Features</h2>
                
                <h3>📄 Document Management</h3>
                <p>Upload and organize documents. Supported formats: PDF, DOCX, PPTX, XLSX, TXT.</p>
                
                <h3>�� AI Search</h3>
                <p>Semantic search finds relevant content even with different wording. Results are ranked by relevance.</p>
                
                <h3>📋 Case Studies</h3>
                <p>Create structured case studies using templates. Link documents and generate AI summaries.</p>
                
                <h3>�� Onboarding</h3>
                <p>Create learning paths for new employees with step-by-step progress tracking.</p>
                
                <h3>📊 Analytics</h3>
                <p>Track search trends, document usage, and user engagement. Export reports to CSV.</p>
                
                <h3>👥 User Management</h3>
                <p>Invite team members, assign roles, and manage permissions.</p>
            </div>
            
            <!-- Keyboard Shortcuts -->
            <div class="card">
                <h2>⌨️ Keyboard Shortcuts</h2>
                <table class="shortcut-table">
                    <tr><th>Shortcut</th><th>Action</th></tr>
                    <tr><td><kbd>Ctrl</kbd> + <kbd>K</kbd></td><td>Open search</td></tr>
                    <tr><td><kbd>Ctrl</kbd> + <kbd>U</kbd></td><td>Upload document</td></tr>
                    <tr><td><kbd>Esc</kbd></td><td>Close modal</td></tr>
                    <tr><td><kbd>Enter</kbd></td><td>Submit form</td></tr>
                </table>
            </div>
            
            <!-- FAQ -->
            <div class="card">
                <h2>❓ FAQ</h2>
                
                <div class="faq-item">
                    <strong>Q: How long does document processing take?</strong>
                    <p>A: Most documents process in under 30 seconds. Larger files may take a few minutes.</p>
                </div>
                
                <div class="faq-item">
                    <strong>Q: What file size is supported?</strong>
                    <p>A: Maximum 50MB per file. For larger files, consider splitting them.</p>
                </div>
                
                <div class="faq-item">
                    <strong>Q: How does AI search work?</strong>
                    <p>A: Documents are converted to embeddings. Search queries are matched semantically, not just by keywords.</p>
                </div>
                
                <div class="faq-item">
                    <strong>Q: Can I delete processed documents?</strong>
                    <p>A: Yes, deleting a document removes it and all associated search data.</p>
                </div>
                
                <div class="faq-item">
                    <strong>Q: How do I invite team members?</strong>
                    <p>A: Go to Users, click "Invite User", enter their email. They'll receive an invitation.</p>
                </div>
            </div>
            
            <!-- Contact -->
            <div class="card">
                <h2>📧 Support</h2>
                <p>Need help? Contact your administrator or reach out to support.</p>
                <p style="margin-top: 15px;">
                    <strong>Email:</strong> support@docent.com<br>
                    <strong>Documentation:</strong> <a href="https://github.com/hamedniavand/docent" target="_blank">GitHub Repository</a>
                </p>
            </div>
            
            <div class="version-info">
                <p>Docent v1.0 • Day 20/30 • 67% Complete</p>
            </div>
        </div>
    </body>
    </html>
    """
