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
                <div class="stat-card" onclick="window.location.href='/users-management'" style="cursor: pointer;">
                    <h3>Team Members</h3>
                    <div class="value">1</div>
                    <p style="font-size: 12px; color: #7f8c8d; margin-top: 10px;">Click to manage →</p>
                </div>
                <div class="stat-card">
                    <h3>Documents</h3>
                    <div class="value">0</div>
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
    