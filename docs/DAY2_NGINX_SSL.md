# Day 2: SSL & nginx Setup

## SSL Certificate
- Domain: docent.hexoplus.ir
- Certificate: Let's Encrypt (valid 89 days)
- Auto-renewal: Enabled via certbot

## nginx Configuration
- Reverse proxy to FastAPI (localhost:8000)
- HTTP → HTTPS redirect
- Max upload: 50MB
- Security headers enabled

## URLs
- Application: https://docent.hexoplus.ir
- OAuth Callback: https://docent.hexoplus.ir/auth/google/callback

## Google OAuth
- Client ID: 715314900634-mirba75d1a5ngtkbrspt4dvdfirg44cl.apps.googleusercontent.com
- Redirect: HTTPS only

