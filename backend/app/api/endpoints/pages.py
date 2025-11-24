from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter(tags=["Pages"])

@router.get("/", response_class=HTMLResponse)
def root():
    """Landing page"""
    return """
    <!DOCTYPE html>
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
            .container {
                text-align: center;
                padding: 40px;
                max-width: 800px;
            }
            h1 {
                font-size: 64px;
                margin-bottom: 20px;
                text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
            }
            .tagline {
                font-size: 24px;
                margin-bottom: 40px;
                opacity: 0.9;
            }
            .status {
                background: rgba(255,255,255,0.2);
                backdrop-filter: blur(10px);
                border-radius: 16px;
                padding: 30px;
                margin-bottom: 30px;
            }
            .status-item {
                display: flex;
                align-items: center;
                justify-content: space-between;
                padding: 12px 0;
                border-bottom: 1px solid rgba(255,255,255,0.1);
            }
            .status-item:last-child { border-bottom: none; }
            .check { color: #4ade80; font-size: 20px; }
            .btn {
                display: inline-block;
                padding: 16px 48px;
                background: white;
                color: #667eea;
                text-decoration: none;
                border-radius: 12px;
                font-size: 18px;
                font-weight: 600;
                transition: all 0.3s;
                box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            }
            .btn:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(0,0,0,0.3);
            }
            .version {
                margin-top: 40px;
                opacity: 0.7;
                font-size: 14px;
            }
            .features {
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
                gap: 20px;
                margin: 30px 0;
            }
            .feature {
                background: rgba(255,255,255,0.1);
                padding: 20px;
                border-radius: 12px;
            }
            .feature h3 {
                font-size: 18px;
                margin-bottom: 10px;
            }
            .feature p {
                font-size: 14px;
                opacity: 0.8;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🎓 Docent</h1>
            <p class="tagline">AI-Powered Knowledge Retention Platform</p>
            
            <div class="status">
                <div class="status-item">
                    <span>Infrastructure & SSL</span>
                    <span class="check">✓</span>
                </div>
                <div class="status-item">
                    <span>Database & Models</span>
                    <span class="check">✓</span>
                </div>
                <div class="status-item">
                    <span>Authentication System</span>
                    <span class="check">✓</span>
                </div>
                <div class="status-item">
                    <span>User Management</span>
                    <span class="check">✓</span>
                </div>
                <div class="status-item">
                    <span>Document Upload</span>
                    <span class="check">✓</span>
                </div>
                <div class="status-item">
                    <span>Document Processing</span>
                    <span class="check">✓</span>
                </div>
                <div class="status-item">
                    <span>AI Search</span>
                    <span style="opacity: 0.5">⏳ Coming Soon</span>
                </div>
            </div>
            
            <div class="features">
                <div class="feature">
                    <h3>📄 Smart Documents</h3>
                    <p>Upload and process company documents with AI</p>
                </div>
                <div class="feature">
                    <h3>🔍 AI Search</h3>
                    <p>Intelligent search across all documents</p>
                </div>
                <div class="feature">
                    <h3>👥 Team Management</h3>
                    <p>Role-based access control</p>
                </div>
                <div class="feature">
                    <h3>📊 Analytics</h3>
                    <p>Track knowledge usage</p>
                </div>
            </div>
            
            <a href="/auth/login-page" class="btn">Launch Dashboard →</a>
            
            <div class="version">
                <p>Version 0.7.0 (MVP Development)</p>
                <p>Day 7/30 Complete • 23% Progress</p>
                <p><a href="/docs" style="color: white; opacity: 0.8;">API Documentation</a></p>
            </div>
        </div>
    </body>
    </html>
    """

@router.get("/dashboard", response_class=HTMLResponse)
def dashboard():
    # ... rest of your existing code

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
                <div class="stat-card" onclick="window.location.href='/users-management'" style="cursor: pointer;">
                    <h3>Team Members</h3>
                    <div class="value">1</div>
                    <p style="font-size: 12px; color: #7f8c8d; margin-top: 10px;">Click to manage →</p>
                </div>
                <div class="stat-card" onclick="window.location.href='/documents-management'" style="cursor: pointer;">
                    <h3>Documents</h3>
                    <div class="value" id="docCount">0</div>
                    <p style="font-size: 12px; color: #7f8c8d; margin-top: 10px;">Click to view →</p>
                </div>
                <div class="stat-card">
                    <h3>Searches</h3>
                    <div class="value">0</div>
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

        // Load document count
            async function loadDocCount() {
                try {
                    const response = await fetch('/documents/stats/company', {
                        headers: { 'Authorization': `Bearer ${token}` }
                    });
                    if (response.ok) {
                        const stats = await response.json();
                        document.getElementById('docCount').textContent = stats.total_documents;
                    }
                } catch (error) {
                    console.error('Error loading doc count:', error);
                }
            }
            
            loadDocCount();    
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
                const response = await fetch(`/users/company/${currentUser.company_id}/roles`, {
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
                const url = `/users/?company_id=${currentUser.company_id}&search=${search}`;
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
                    alert('Invitation sent successfully!');
                    closeInviteModal();
                    loadUsers();
                } else {
                    const error = await response.json();
                    alert('Error: ' + error.detail);
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
                    <div class="value" id="statTotal">-</div>
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
            
            // Load documents
            async function loadDocuments(search = '') {
                const url = `/documents/?company_id=${currentUser.company_id}&search=${search}`;
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
                                    <button class="btn btn-secondary" style="padding: 5px 10px; font-size: 12px; margin-right: 5px;" 
                                            onclick="downloadDocument(${doc.id}, '${doc.filename}')">Download</button>
                                    <button class="btn btn-danger" style="padding: 5px 10px; font-size: 12px;" 
                                            onclick="deleteDocument(${doc.id})">Delete</button>
                                </td>
                            </tr>
                        `;
                    }).join('');
                }
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
                        alert('Upload failed. Please try again.');
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
                    alert('Failed to download file');
                }
            }
            
            // Delete document
            async function deleteDocument(docId) {
                if (!confirm('Are you sure you want to delete this document?')) return;
                
                const response = await fetch(`/documents/${docId}`, {
                    method: 'DELETE',
                    headers: {
                        'Authorization': `Bearer ${token}`
                    }
                });
                
                if (response.ok) {
                    alert('Document deleted successfully');
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