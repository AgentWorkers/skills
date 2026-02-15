---
name: qbittorrent
version: 1.0.0
description: 使用 qBittorrent 管理种子文件。当用户需要执行以下操作时，请使用该工具：  
- 列出所有种子文件  
- 添加新的种子文件  
- 暂停正在下载的种子文件  
- 继续下载被暂停的种子文件  
- 删除某个种子文件  
- 查看种子的下载进度  
- 获取种子的下载速度信息  
- 查看 qBittorrent 的运行状态或相关统计数据  

（注：若用户仅提及“qBittorrent”或“种子文件管理”，也可使用该工具进行相应操作。）
---

# qBittorrent WebUI API

通过 qBittorrent 的 WebUI API（版本 4.1 及以上）来管理种子文件。

## 设置

配置文件：`~/.clawdbot/credentials/qbittorrent/config.json`

```json
{
  "url": "http://localhost:8080",
  "username": "admin",
  "password": "adminadmin"
}
```

## 快速参考

### 列出种子文件

```bash
# All torrents
./scripts/qbit-api.sh list

# Filter by status
./scripts/qbit-api.sh list --filter downloading
./scripts/qbit-api.sh list --filter seeding
./scripts/qbit-api.sh list --filter paused

# Filter by category
./scripts/qbit-api.sh list --category movies
```

筛选条件：`all`、`downloading`、`seeding`、`completed`、`paused`、`active`、`inactive`、`stalled`、`errored`

### 获取种子文件信息

```bash
./scripts/qbit-api.sh info <hash>
./scripts/qbit-api.sh files <hash>
./scripts/qbit-api.sh trackers <hash>
```

### 添加种子文件

```bash
# By magnet or URL
./scripts/qbit-api.sh add "magnet:?xt=..." --category movies

# By file
./scripts/qbit-api.sh add-file /path/to/file.torrent --paused
```

### 控制种子文件的状态

```bash
./scripts/qbit-api.sh pause <hash>         # or "all"
./scripts/qbit-api.sh resume <hash>        # or "all"
./scripts/qbit-api.sh delete <hash>        # keep files
./scripts/qbit-api.sh delete <hash> --files  # delete files too
./scripts/qbit-api.sh recheck <hash>
```

### 分类与标签

```bash
./scripts/qbit-api.sh categories
./scripts/qbit-api.sh tags
./scripts/qbit-api.sh set-category <hash> movies
./scripts/qbit-api.sh add-tags <hash> "important,archive"
```

### 传输信息

```bash
./scripts/qbit-api.sh transfer   # global speed/stats
./scripts/qbit-api.sh speedlimit # current limits
./scripts/qbit-api.sh set-speedlimit --down 5M --up 1M
```

### 应用程序信息

```bash
./scripts/qbit-api.sh version
./scripts/qbit-api.sh preferences
```

## 响应格式

种子文件对象包含以下字段：
- `hash`、`name`、`state`、`progress`
- `dlspeed`（下载速度）、`upspeed`（上传速度）、`eta`（预计完成时间）
- `size`（文件大小）、`downloaded`（已下载量）、`uploaded`（已上传量）
- `category`（分类）、`tags`（标签）、`save_path`（保存路径）

种子文件的状态：`downloading`（下载中）、`stalledDL`（下载暂停）、`uploading`（上传中）、`stalledUP`（上传暂停）、`pausedDL`（下载暂停）、`queuedDL`（排队下载）、`queuedUP`（排队上传）、`checkingDL`（检查状态）、`checkingUP`（检查上传状态）、`error`（出错）、`missingFiles`（缺少文件）