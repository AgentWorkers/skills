---
name: media-backup
description: 将 Clawdbot 的对话媒体（照片、视频）存档到本地文件夹中。该功能支持与任何同步服务（Dropbox、iCloud、Google Drive、OneDrive）配合使用。
metadata: {"clawdbot":{"env":["MEDIA_BACKUP_DEST"]}}
---

# 媒体备份

该功能用于将 Clawdbot 收到的媒体文件简单备份到本地文件夹中。无需使用任何 API 或 OAuth，仅通过文件复制实现备份。

由于备份内容仅存储在本地文件夹中，因此该功能可与任何云同步服务配合使用。

## 设置

1. 设置目标文件夹：
```bash
export MEDIA_BACKUP_DEST="$HOME/Dropbox/Clawdbot/media"
# or
export MEDIA_BACKUP_DEST="$HOME/Library/Mobile Documents/com~apple~CloudDocs/Clawdbot/media"  # iCloud
# or  
export MEDIA_BACKUP_DEST="$HOME/Google Drive/Clawdbot/media"
```

2. 或者将此设置添加到 Clawdbot 的配置文件中：
```json
{
  "skills": {
    "entries": {
      "media-backup": {
        "env": {
          "MEDIA_BACKUP_DEST": "/path/to/your/folder"
        }
      }
    }
  }
}
```

## 使用方法

```bash
# Run backup
uv run skills/media-backup/scripts/backup.py

# Dry run (preview only)
uv run skills/media-backup/scripts/backup.py --dry-run

# Custom source/destination
uv run skills/media-backup/scripts/backup.py --source ~/.clawdbot/media/inbound --dest ~/Backups/media

# Check status
uv run skills/media-backup/scripts/backup.py status
```

## 工作原理

1. 扫描 `~/.clawdbot/media/inbound/` 目录下的所有媒体文件。
2. 按日期对文件进行排序：`YYYY-MM-DD/filename.jpg`。
3. 通过文件内容哈希值来跟踪已备份的文件（确保文件不会重复）。
4. 你的云服务会自动同步该本地文件夹。

## 定时备份设置

- 每小时执行一次备份：
```
0 * * * * cd ~/clawd && uv run skills/media-backup/scripts/backup.py >> /tmp/media-backup.log 2>&1
```

- 或者通过 Clawdbot 的定时任务来执行备份：
```
Run media backup: uv run skills/media-backup/scripts/backup.py
If files archived, reply: 📸 Archived [N] media files
If none, reply: HEARTBEAT_OK
```

## 支持的文件格式

jpg, jpeg, png, gif, webp, heic, mp4, mov, m4v, webm