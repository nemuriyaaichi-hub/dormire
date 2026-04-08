#!/bin/bash

# === 設定 ===
DB_NAME="dormire"
DB_USER="nemuriya"
PGPASSWORD="BnaeEp02ndwuJlBSCFc2"

# S3設定
S3_BUCKET="dormire-db-backup"
S3_ENDPOINT="https://s3.isk01.sakurastorage.jp"
AWS_ACCESS_KEY_ID="NBYOEBU1O41R2B8HSVAE"
AWS_SECRET_ACCESS_KEY="vM03ttCZRdCGv6A9VDobExOIqrj0qBzkdd00o=3W"

# 保存設定
BACKUP_DIR="/var/backups/postgresql"
DATE=$(date +"%Y%m%d_%H%M%S")
FILENAME="${DB_NAME}_${DATE}.dump"
DUMP_PATH="${BACKUP_DIR}/${FILENAME}"

# 7日間保持
RETENTION_DAYS=7

# === バックアップ ===
mkdir -p "$BACKUP_DIR"
export PGPASSWORD
pg_dump -U "$DB_USER" -Fc "$DB_NAME" -f "$DUMP_PATH"

if [ $? -ne 0 ]; then
    echo "❌ pg_dump failed"
    exit 1
fi

echo "✅ Dump created: $DUMP_PATH"

# === さくらのオブジェクトストレージへアップロード ===
export AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY

aws --endpoint-url "$S3_ENDPOINT" s3 cp "$DUMP_PATH" "s3://${S3_BUCKET}/${FILENAME}"

if [ $? -ne 0 ]; then
    echo "❌ Upload to S3 failed"
    exit 1
fi

echo "📤 Uploaded to S3: s3://${S3_BUCKET}/${FILENAME}"

# === ローカルの古いバックアップを削除 ===
find "$BACKUP_DIR" -type f -name "${DB_NAME}_*.dump" -mtime +$RETENTION_DAYS -exec rm -f {} \;

# === S3の古いバックアップを削除 ===
aws --endpoint-url "$S3_ENDPOINT" s3 ls "s3://${S3_BUCKET}/" | while read -r line; do
  FILE_DATE=$(echo "$line" | awk '{print $1}')
  FILE_NAME=$(echo "$line" | awk '{print $4}')

  if [[ "$FILE_NAME" == dormire_*.dump ]]; then
    FILE_DATE_EPOCH=$(date -d "$FILE_DATE" +%s)
    THIRTY_DAYS_AGO=$(date -d "-30 days" +%s)

    if (( FILE_DATE_EPOCH < THIRTY_DAYS_AGO )); then
      echo "🗑 Deleting old file: $FILE_NAME"
      aws --endpoint-url "$S3_ENDPOINT" s3 rm "s3://${S3_BUCKET}/${FILE_NAME}"
    fi
  fi
done