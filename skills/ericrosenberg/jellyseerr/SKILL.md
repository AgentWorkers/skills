---
name: jellyseerr
description: 通过Jellyseerr请求电影和电视剧。当用户希望将媒体添加到他们的Plex/Jellyfin服务器中、搜索内容的可用性或管理媒体请求时，可以使用该功能。
---

# Jellyseerr

通过Jellyseerr服务器请求电影和电视节目，并实现自动下载到Plex/Jellyfin中。

## 设置

配置您的Jellyseerr服务器：

```bash
scripts/setup.sh
```

您需要以下信息：
- Jellyseerr服务器的URL
- API密钥（在Jellyseerr设置 > 通用选项中获取）

## 使用方法

请求电影：
```bash
scripts/request_movie.py "Movie Name"
```

请求电视节目：
```bash
scripts/request_tv.py "TV Show Name"
```

搜索内容：
```bash
scripts/search.py "Content Name"
```

## 示例

请求一部电影：
```bash
scripts/request_movie.py "The Matrix"
```

请求一整部电视节目：
```bash
scripts/request_tv.py "Breaking Bad"
```

请求特定的电视季：
```bash
scripts/request_tv.py "Breaking Bad" --season 1
```

## 自动内容可用性通知

当您请求的内容可用时，会收到通知。

### Webhook（推荐）

为了实现即时通知，请设置Webhook集成。请参阅[references/WEBHOOK_SETUP.md](references/WEBHOOK_SETUP.md)以获取完整指南。

快速设置：
```bash
scripts/install_service.sh  # Run with sudo
```

然后配置Jellyseerr，使其将Webhook发送到`http://YOUR_IP:8384/`

### 轮询（替代方案）

在无法使用Webhook的环境中，可以使用基于cron的轮询机制：

```bash
crontab -l > /tmp/cron_backup.txt
echo "* * * * * $(pwd)/scripts/auto_monitor.sh" >> /tmp/cron_backup.txt
crontab /tmp/cron_backup.txt
```

检查待处理的请求：
```bash
scripts/track_requests.py
```

## 配置

编辑`~/.config/jellyseerr/config.json`文件：
```json
{
  "server_url": "https://jellyseerr.yourdomain.com",
  "api_key": "your-api-key",
  "auto_approve": true
}
```

## API参考

有关Jellyseerr API的详细信息，请参阅[references/api.md](references/api.md)。