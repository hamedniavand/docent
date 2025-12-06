#!/bin/bash
# Docent Backup Script

BACKUP_DIR="/opt/docent/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

echo "Starting backup..."

# Database backup
echo "Backing up database..."
docker exec docent-postgres pg_dump -U docent_user docent > $BACKUP_DIR/db_$DATE.sql
gzip $BACKUP_DIR/db_$DATE.sql

# Storage backup (documents)
echo "Backing up storage..."
tar -czf $BACKUP_DIR/storage_$DATE.tar.gz -C /opt/docent/data storage 2>/dev/null || true

# Keep only last 7 backups
echo "Cleaning old backups..."
ls -t $BACKUP_DIR/db_*.sql.gz 2>/dev/null | tail -n +8 | xargs rm -f 2>/dev/null
ls -t $BACKUP_DIR/storage_*.tar.gz 2>/dev/null | tail -n +8 | xargs rm -f 2>/dev/null

echo "Backup complete!"
ls -lh $BACKUP_DIR/
