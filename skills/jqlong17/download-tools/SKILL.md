---
name: download-tools
description: 用于 YouTube 和 WeChat 的 CLI 下载工具
metadata:
  {
    "openclaw": {
      "requires": { "bins": ["curl", "yt-dlp"] },
      "install": [
        { "id": "yt-dlp", "kind": "brew", "package": "yt-dlp" },
        { "id": "ffmpeg", "kind": "brew", "package": "ffmpeg" }
      ]
    }
  }
---
# 下载工具

这是一组用于下载 YouTube 和微信文章的命令行工具（CLI）集合。

## 工具

### wechat-dl.sh
将微信文章下载为 TXT 格式。

```bash
./wechat-dl.sh "https://mp.weixin.qq.com/s/xxx" [output_name]
```

### yt-audio.sh
将 YouTube 视频下载为 MP3 格式。

```bash
./yt-audio.sh "https://youtube.com/watch?v=xxx" [output_name]
```

## 安装

```bash
brew install yt-dlp ffmpeg
```