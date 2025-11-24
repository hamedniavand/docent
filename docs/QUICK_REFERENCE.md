# Docent - Quick Reference Card

## URLs
- Live: https://docent.hexoplus.ir
- Login: admin@democorp.com / admin123

## Key Commands
```bash
# Start
cd /opt/docent && docker-compose up -d

# Logs
docker logs docent-backend -f

# Restart
docker-compose restart backend

# Database
docker exec -it docent-postgres psql -U docent_user -d docent
```

## File Locations
- Code: /opt/docent/backend/app/
- Storage: /opt/docent/data/storage/
- Vectors: /opt/docent/data/chroma/
- Logs: docker logs docent-backend

## API Test
```bash
TOKEN=$(curl -s -X POST https://docent.hexoplus.ir/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@democorp.com","password":"admin123"}' \
  | python3 -c "import sys, json; print(json.load(sys.stdin)['access_token'])")

curl -H "Authorization: Bearer $TOKEN" https://docent.hexoplus.ir/auth/me
```

## Current State
- 7/30 days complete (23%)
- 20 API endpoints
- 3 documents uploaded
- 1 document processed
- 7 users, 3 roles
