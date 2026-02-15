---
name: jellyfin-control
description: 控制 Jellyfin 媒体服务器：搜索内容、在远程设备（如电视）上恢复播放，并管理播放会话。智能的“恢复播放”功能能够自动找到电视节目中尚未播放的下一集。
metadata: {"version": "1.0.0", "author": "Francis via OpenClaw", "openclaw": {"requires": {"env": ["JF_URL", "JF_API_KEY", "JF_USER"]}}}
---

# Jellyfin 控制工具

这是一个功能强大、具备容错能力的工具，可通过命令行（CLI）来控制 Jellyfin 的播放功能。

## 主要特性

- **智能续播**：自动查找系列剧中的下一集未播放的部分。
- **续播位置**：能够精确地从上次暂停的位置继续播放电影或剧集（在 LG WebOS/Tizen 设备上可使用 `Seek` 命令作为备用方式）。
- **设备检测**：自动识别可控制的设备（电视、手机、网页端）。
- **内容搜索**：可以查找内容 ID 及相关详细信息。

## 配置方法

请在 `.env` 或 `SECRETOS.md` 文件中设置相应的环境变量：

```bash
JF_URL=http://your-jellyfin-ip:8096
JF_API_KEY=your_api_key_here
JF_USER=your_username
```

## 使用方法

### 智能续播/播放
该工具会自动查找与 “Breaking Bad” 相关的下一集未播放的内容，确定当前连接的电视设备，并开始播放。

```bash
node skills/jellyfin-control/cli.js resume "Breaking Bad"
```

### 定位特定设备
（支持模糊匹配）：
```bash
node skills/jellyfin-control/cli.js resume "Matrix" --device "Chromecast"
```

### 搜索内容
```bash
node skills/jellyfin-control/cli.js search "Star Wars"
```

## 架构

- `lib/jellyfin.js`：核心 API 逻辑（包括认证、搜索、会话管理以及播放/暂停功能）。
- `cli.js`：用户友好的命令行接口。