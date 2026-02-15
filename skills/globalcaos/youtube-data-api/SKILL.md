---
name: youtube
description: YouTube 数据 API 集成用于搜索视频、查看订阅信息、播放列表以及获取视频详情。当用户需要搜索 YouTube 内容、查看自己的订阅列表、浏览播放列表、获取视频信息或列出自己喜欢的视频时，可以使用该 API。
homepage: https://developers.google.com/youtube/v3
metadata:
  {
    "openclaw":
      {
        "emoji": "📺",
        "requires": { "bins": ["uv"] },
        "install":
          [
            {
              "id": "uv-brew",
              "kind": "brew",
              "formula": "uv",
              "bins": ["uv"],
              "label": "Install uv (brew)",
            },
          ],
      },
  }
---

# YouTube

您可以使用提供的脚本访问 YouTube 数据 API。此操作需要先完成 OAuth 设置（只需完成一次）。

## 首次设置

1. 从 [Google Cloud Console](https://console.cloud.google.com/apis/credentials) 获取 OAuth 凭据。
2. 创建 OAuth 2.0 客户端 ID（适用于桌面应用程序）。
3. 下载 JSON 文件并将其保存到 `~/.config/youtube-skill/credentials.json`。
4. 运行 `auth` 命令（该命令会打开浏览器）：

```bash
uv run {baseDir}/scripts/youtube.py auth
```

注意：如果您已经使用了 `gog`（gogcli），则凭据会自动共享。

## 命令

### 搜索视频

```bash
uv run {baseDir}/scripts/youtube.py search "AI news 2026"
uv run {baseDir}/scripts/youtube.py search "python tutorial" -l 20
```

### 获取视频详情

```bash
uv run {baseDir}/scripts/youtube.py video VIDEO_ID
uv run {baseDir}/scripts/youtube.py video dQw4w9WgXcQ -v
```

### 列出订阅的频道

```bash
uv run {baseDir}/scripts/youtube.py subscriptions
uv run {baseDir}/scripts/youtube.py subs -l 50
```

### 列出播放列表

```bash
uv run {baseDir}/scripts/youtube.py playlists
uv run {baseDir}/scripts/youtube.py pl -l 10
```

### 列出播放列表中的视频

```bash
uv run {baseDir}/scripts/youtube.py playlist-items PLAYLIST_ID
uv run {baseDir}/scripts/youtube.py pli PLxxxxxx -l 25
```

### 列出可用的字幕

```bash
uv run {baseDir}/scripts/youtube.py captions VIDEO_ID
```

### 列出用户喜欢的视频

```bash
uv run {baseDir}/scripts/youtube.py liked
uv run {baseDir}/scripts/youtube.py liked -l 50
```

### 获取频道信息

```bash
uv run {baseDir}/scripts/youtube.py channel
uv run {baseDir}/scripts/youtube.py channel CHANNEL_ID -v
```

## 多账户支持

使用 `-a` 标志来切换不同的账户：

```bash
uv run {baseDir}/scripts/youtube.py -a work subscriptions
uv run {baseDir}/scripts/youtube.py -a personal liked
```

## 与 yt-dlp 结合使用

若需下载视频，请使用单独的工具 `yt-dlp`：

```bash
yt-dlp "https://youtube.com/watch?v=VIDEO_ID"
yt-dlp --write-auto-subs --skip-download "https://youtube.com/watch?v=VIDEO_ID"
yt-dlp -x --audio-format mp3 "https://youtube.com/watch?v=VIDEO_ID"
```