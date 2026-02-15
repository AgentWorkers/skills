---
description: 生成针对 PostgreSQL、MySQL、SQLite 和 MongoDB 的自动备份脚本，并实现备份文件的轮换机制。
---

# 数据库备份

创建具备压缩、数据轮换和定时备份功能的自动化脚本。

## 指令

1. **向用户询问**：数据库类型、名称、连接信息、备份目录（默认：`~/backups/db/`）、保留时间（默认：7天）、备份时间（默认：每天凌晨2点）。

2. **根据数据库类型生成对应的脚本**：

### PostgreSQL
```bash
#!/bin/bash
set -euo pipefail
BACKUP_DIR="${BACKUP_DIR:-$HOME/backups/db}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
TS=$(date +%Y%m%d_%H%M%S)
DB="DATABASE_NAME"
mkdir -p "$BACKUP_DIR" && chmod 700 "$BACKUP_DIR"
pg_dump -Fc "$DB" > "$BACKUP_DIR/${DB}_${TS}.dump"
chmod 600 "$BACKUP_DIR/${DB}_${TS}.dump"
find "$BACKUP_DIR" -name "${DB}_*.dump" -mtime +$RETENTION_DAYS -delete
echo "[$(date)] ✅ Backup: ${DB}_${TS}.dump"
```

### MySQL
```bash
#!/bin/bash
set -euo pipefail
BACKUP_DIR="${BACKUP_DIR:-$HOME/backups/db}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
TS=$(date +%Y%m%d_%H%M%S)
DB="DATABASE_NAME"
mkdir -p "$BACKUP_DIR" && chmod 700 "$BACKUP_DIR"
mysqldump --single-transaction "$DB" | gzip > "$BACKUP_DIR/${DB}_${TS}.sql.gz"
chmod 600 "$BACKUP_DIR/${DB}_${TS}.sql.gz"
find "$BACKUP_DIR" -name "${DB}_*.sql.gz" -mtime +$RETENTION_DAYS -delete
echo "[$(date)] ✅ Backup: ${DB}_${TS}.sql.gz"
```

### SQLite
```bash
#!/bin/bash
set -euo pipefail
BACKUP_DIR="${BACKUP_DIR:-$HOME/backups/db}"
RETENTION_DAYS="${RETENTION_DAYS:-7}"
TS=$(date +%Y%m%d_%H%M%S)
DB_FILE="PATH_TO_DB.sqlite"
DB_NAME=$(basename "$DB_FILE" .sqlite)
mkdir -p "$BACKUP_DIR" && chmod 700 "$BACKUP_DIR"
sqlite3 "$DB_FILE" ".backup '$BACKUP_DIR/${DB_NAME}_${TS}.sqlite'"
gzip "$BACKUP_DIR/${DB_NAME}_${TS}.sqlite"
chmod 600 "$BACKUP_DIR/${DB_NAME}_${TS}.sqlite.gz"
find "$BACKUP_DIR" -name "${DB_NAME}_*.sqlite.gz" -mtime +$RETENTION_DAYS -delete
echo "[$(date)] ✅ Backup: ${DB_NAME}_${TS}.sqlite.gz"
```

3. **设置定时任务**：
   ```bash
   chmod +x backup.sh
   (crontab -l 2>/dev/null; echo "0 2 * * * /path/to/backup.sh >> /path/to/backup.log 2>&1") | crontab -
   ```

4. **验证**：手动运行一次脚本并检查输出结果。

## 安全性

- **切勿将密码硬编码**——使用 `~/.pgpass`（PostgreSQL）、`~/.my.cnf`（MySQL）或环境变量来存储密码。
- 为所有备份文件设置权限 `chmod 600`，为备份目录设置权限 `chmod 700`。
- 将备份目录添加到 `.gitignore` 文件中。
- 对于远程存储，可以使用 `aws s3 cp` 或 `rclone copy` 命令进行传输。

## 故障排除

- **“权限被拒绝”**：检查数据库用户的权限以及文件的权限设置。
- **“命令未找到”**：安装 `postgresql-client`、`mysql-client` 或 `sqlite3`。
- **磁盘空间不足**：在备份前使用 `df -h` 命令检查磁盘空间；可以在脚本中添加预检查逻辑。
- **SQLite 数据库被锁定**：确保在备份过程中没有写入操作。

## 所需工具

- 数据库客户端工具：`pg_dump`、`mysqldump`、`sqlite3` 或 `mongodump`。
- `gzip`、`find`、`crontab`（标准Unix工具）。
- 不需要API密钥。