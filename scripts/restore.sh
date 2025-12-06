#!/bin/bash
# Docent Restore Script

BACKUP_DIR="/opt/docent/backups"

if [ -z "$1" ]; then
    echo "Usage: ./restore.sh <backup_date>"
    echo "Available backups:"
    ls -1 $BACKUP_DIR/db_*.sql.gz 2>/dev/null | sed 's/.*db_//' | sed 's/.sql.gz//'
    exit 1
fi

DATE=$1
DB_BACKUP="$BACKUP_DIR/db_${DATE}.sql.gz"

if [ ! -f "$DB_BACKUP" ]; then
    echo "Backup not found: $DB_BACKUP"
    exit 1
fi

echo "Restoring from $DATE..."

# Restore database
echo "Restoring database..."
gunzip -c $DB_BACKUP | docker exec -i docent-postgres psql -U docent_user -d docent

echo "Restore complete!"
