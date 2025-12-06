#!/bin/bash
# Docent Monitoring Script

echo "=== Docent System Monitor ==="
echo "Time: $(date)"
echo ""

# Check services
echo "📦 Docker Containers:"
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}" | grep docent

echo ""
echo "💾 Disk Usage:"
df -h / | tail -1

echo ""
echo "🔍 Health Check:"
curl -s http://localhost:8000/health | python3 -m json.tool 2>/dev/null || echo "Backend not responding"

echo ""
echo "📊 Recent Logs (last 5 lines):"
docker logs docent-backend --tail 5 2>&1 | grep -v "INFO:"

echo ""
echo "🗄️ Database:"
docker exec docent-postgres psql -U docent_user -d docent -c "SELECT 'Users:', COUNT(*) FROM users UNION ALL SELECT 'Documents:', COUNT(*) FROM documents UNION ALL SELECT 'Chunks:', COUNT(*) FROM doc_chunks;" 2>/dev/null | tail -4
