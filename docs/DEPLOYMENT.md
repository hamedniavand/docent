# Docent Deployment Guide

## Prerequisites
- Ubuntu 20.04+ server
- Docker & Docker Compose
- Domain with SSL certificate
- 2GB+ RAM, 10GB+ disk

## Quick Deploy

### 1. Clone Repository
```bash
git clone https://github.com/hamedniavand/docent.git /opt/docent
cd /opt/docent
```

### 2. Configure Environment
```bash
cp .env.example .env
nano .env
```

Required variables:
- `DATABASE_URL` - PostgreSQL connection
- `JWT_SECRET` - Random secret key
- `GEMINI_API_KEY` - Google AI key
- `SMTP_*` - Email settings

### 3. Start Services
```bash
docker-compose up -d
```

### 4. Initialize Database
```bash
docker exec docent-backend python scripts/init_data.py
```

### 5. Setup Nginx (optional)
```bash
sudo cp docs/nginx-docent.conf /etc/nginx/sites-available/docent
sudo ln -s /etc/nginx/sites-available/docent /etc/nginx/sites-enabled/
sudo certbot --nginx -d yourdomain.com
sudo systemctl reload nginx
```

## Maintenance

### View Logs
```bash
docker logs docent-backend -f
docker logs docent-postgres -f
```

### Restart Services
```bash
docker-compose restart backend
```

### Backup Database
```bash
docker exec docent-postgres pg_dump -U docent_user docent > backup.sql
```

### Update Application
```bash
git pull origin main
docker-compose build backend
docker-compose up -d
```

## Troubleshooting

### Bad Gateway
```bash
docker logs docent-backend --tail 50
docker-compose restart backend
```

### Database Connection
```bash
docker exec docent-postgres pg_isready -U docent_user
```

### Disk Space
```bash
df -h /
docker system prune -f
```
