---
name: YT Meta - YouTube Metadata Extractor
description: 提取YouTube视频信息、频道统计数据、播放列表以及评论。无需API密钥。这是一个免费的命令行工具（CLI），适用于内容研究和分析。
---

# YT Meta

无需API密钥即可提取YouTube元数据，包括视频、频道、播放列表和评论信息。

## 安装

```bash
npm install -g yt-meta-cli
```

## 命令

### 视频元数据

```bash
yt-meta video dQw4w9WgXcQ
yt-meta video https://youtu.be/dQw4w9WgXcQ
yt-meta video "https://youtube.com/watch?v=VIDEO_ID"
```

返回内容：标题、描述、观看次数、点赞数、时长、上传日期、标签和缩略图。

### 频道信息

```bash
yt-meta channel @mkbhd
yt-meta channel @channel --videos           # Include recent videos
yt-meta channel @channel --videos --limit 100
```

### 播放列表

```bash
yt-meta playlist PLrAXtmErZgOei...
yt-meta playlist PLxxx --all               # Entire playlist
```

### 搜索

```bash
yt-meta search "react hooks tutorial"
yt-meta search "javascript" --limit 50
yt-meta search "gaming" --sort views
```

### 评论

```bash
yt-meta comments dQw4w9WgXcQ
yt-meta comments VIDEO_ID --limit 500
yt-meta comments VIDEO_ID --sort top
```

## 输出格式

```bash
yt-meta video ID                 # JSON (default)
yt-meta playlist ID -o jsonl     # One per line
yt-meta search "query" -o csv    # Spreadsheet
yt-meta video ID -o table        # Terminal
yt-meta channel @x --save out.json
```

## 示例输出

```json
{
  "id": "dQw4w9WgXcQ",
  "title": "Rick Astley - Never Gonna Give You Up",
  "channel": "Rick Astley",
  "views": 1400000000,
  "likes": 15000000,
  "duration": "3:33",
  "uploadDate": "2009-10-25",
  "tags": ["rick astley", "never gonna give you up"]
}
```

## 常见使用场景

- **分析视频表现**：
```bash
yt-meta video VIDEO_ID -o json
```

- **导出频道的视频**：
```bash
yt-meta channel @mkbhd --videos --limit 500 > videos.json
```

- **研究热门话题**：
```bash
yt-meta search "ai tools 2024" --sort views -o csv
```

---

**由 [LXGIC Studios](https://lxgicstudios.com) 开发**

🔗 [GitHub](https://github.com/lxgicstudios/yt-meta) · [Twitter](https://x.com/lxgicstudios)