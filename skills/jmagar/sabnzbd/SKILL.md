---
name: sabnzbd
version: 1.0.0
description: 使用 SABnzbd 管理 Usenet 下载任务。当用户请求“检查 SABnzbd 的状态”、“列出 NZB 下载队列”、“添加 NZB 文件”、“暂停下载”、“恢复下载”、“查看 SABnzbd 的详细信息”、“查看 Usenet 下载队列”或提及 SABnzbd 以及下载管理相关功能时，可以使用该工具。
---

# SABnzbd API

通过 SABnzbd 的 REST API 管理 Usenet 下载任务。

## 设置

配置文件：`~/.clawdbot/credentials/sabnzbd/config.json`

```json
{
  "url": "http://localhost:8080",
  "apiKey": "your-api-key-from-config-general"
}
```

从 SABnzbd 的“设置” → “安全”选项中获取您的 API 密钥。

## 快速参考

### 队列状态

```bash
# Full queue
./scripts/sab-api.sh queue

# With filters
./scripts/sab-api.sh queue --limit 10 --category tv

# Specific job
./scripts/sab-api.sh queue --nzo-id SABnzbd_nzo_xxxxx
```

### 添加 NZB 文件

```bash
# By URL (indexer link)
./scripts/sab-api.sh add "https://indexer.com/get.php?guid=..."

# With options
./scripts/sab-api.sh add "URL" --name "My Download" --category movies --priority high

# By local file
./scripts/sab-api.sh add-file /path/to/file.nzb --category tv
```

优先级：`force`、`high`、`normal`、`low`、`paused`、`duplicate`

### 控制队列

```bash
./scripts/sab-api.sh pause              # Pause all
./scripts/sab-api.sh resume             # Resume all
./scripts/sab-api.sh pause-job <nzo_id>
./scripts/sab-api.sh resume-job <nzo_id>
./scripts/sab-api.sh delete <nzo_id>    # Keep files
./scripts/sab-api.sh delete <nzo_id> --files  # Delete files too
./scripts/sab-api.sh purge              # Clear queue
```

### 速度控制

```bash
./scripts/sab-api.sh speedlimit 50      # 50% of max
./scripts/sab-api.sh speedlimit 5M      # 5 MB/s
./scripts/sab-api.sh speedlimit 0       # Unlimited
```

### 历史记录

```bash
./scripts/sab-api.sh history
./scripts/sab-api.sh history --limit 20 --failed
./scripts/sab-api.sh retry <nzo_id>     # Retry failed
./scripts/sab-api.sh retry-all          # Retry all failed
./scripts/sab-api.sh delete-history <nzo_id>
```

### 分类与脚本

```bash
./scripts/sab-api.sh categories
./scripts/sab-api.sh scripts
./scripts/sab-api.sh change-category <nzo_id> movies
./scripts/sab-api.sh change-script <nzo_id> notify.py
```

### 状态与信息

```bash
./scripts/sab-api.sh status             # Full status
./scripts/sab-api.sh version
./scripts/sab-api.sh warnings
./scripts/sab-api.sh server-stats       # Download stats
```

## 响应格式

队列信息包括：
- `nzo_id`、`filename`、`status`
- `mb`、`mbleft`、`percentage`
- `timeleft`、`priority`、`cat`
- `script`、`labels`

状态值：`Downloading`、`Queued`、`Paused`、`Propagating`、`Fetching`

历史记录状态：`Completed`、`Failed`、`Queued`、`Verifying`、`Repairing`、`Extracting`