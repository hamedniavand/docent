
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
        <p style="margin: 30px 0;">Day 7/30 Complete • 23% Progress</p>
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
                </div>
            </div>
            
            <!-- Quick Actions -->
            <div class="quick-actions">
                <h3>Quick Actions</h3>
                <div class="action-buttons">
                    <a href="/documents-management" class="action-btn">📤 Upload Documents</a>
                    <a href="/search-page" class="action-btn">🔍 Advanced Search</a>
                    <a href="/users-management" class="action-btn">👥 Manage Users</a>
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