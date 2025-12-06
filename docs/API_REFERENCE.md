# Docent API Reference

## Base URL
```
https://docent.hexoplus.ir
```

## Authentication
All protected endpoints require a Bearer token in the Authorization header:
```
Authorization: Bearer <access_token>
```

### Get Token
```http
POST /auth/login
Content-Type: application/json

{
  "email": "user@company.com",
  "password": "password123"
}
```

Response:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer",
  "user": {
    "id": 1,
    "email": "user@company.com",
    "name": "User Name",
    "type": "company_user"
  }
}
```

---

## Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/auth/login` | User login |
| GET | `/auth/me` | Get current user |
| POST | `/auth/logout` | Logout |

### Users
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/users/` | List users |
| POST | `/users/` | Create user |
| GET | `/users/{id}` | Get user |
| PUT | `/users/{id}` | Update user |
| DELETE | `/users/{id}` | Deactivate user |
| POST | `/users/invite` | Invite user |

### Documents
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/documents/` | List documents |
| POST | `/documents/upload` | Upload document |
| POST | `/documents/upload-multiple` | Upload multiple |
| GET | `/documents/{id}` | Get document |
| GET | `/documents/{id}/download` | Download file |
| DELETE | `/documents/{id}` | Delete document |
| GET | `/documents/stats/company` | Get statistics |

### Document Processing
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/processing/process/{id}` | Process document |
| POST | `/processing/process-all` | Process all |
| GET | `/processing/status/{id}` | Get status |

### Search
| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/search/` | Semantic search |
| GET | `/search/history` | Search history |

### Case Studies
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/cases/` | List cases |
| POST | `/cases/` | Create case |
| GET | `/cases/{id}` | Get case |
| PUT | `/cases/{id}` | Update case |
| DELETE | `/cases/{id}` | Delete case |
| GET | `/cases/templates` | List templates |
| POST | `/cases/templates` | Create template |

### Onboarding
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/onboarding/paths` | List paths |
| POST | `/onboarding/paths` | Create path |
| GET | `/onboarding/paths/{id}` | Get path |
| POST | `/onboarding/paths/{id}/start` | Start path |
| POST | `/onboarding/progress` | Update progress |

### Analytics
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/analytics/summary` | Quick stats |
| GET | `/analytics/dashboard` | Full dashboard |
| GET | `/analytics/search` | Search analytics |
| GET | `/analytics/documents` | Document stats |
| GET | `/analytics/users` | User analytics |
| GET | `/analytics/activity` | Activity logs |

### Notifications
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/notifications/preferences` | Get preferences |
| PUT | `/notifications/preferences` | Update preferences |
| POST | `/notifications/test-email` | Send test email |

---

## Error Responses
```json
{
  "error": true,
  "message": "Error description",
  "status_code": 400
}
```

### Status Codes
- `200` - Success
- `201` - Created
- `400` - Bad Request
- `401` - Unauthorized
- `403` - Forbidden
- `404` - Not Found
- `422` - Validation Error
- `429` - Too Many Requests
- `500` - Server Error

---

## Rate Limits
- Login: 5 attempts per minute per IP
- API: 100 requests per minute per user

