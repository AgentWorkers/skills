---
name: tiktok-scraping-yt-dlp
description: 用于TikTok的爬取、内容检索和分析。
---

# 使用 yt-dlp 抓取 TikTok 视频

yt-dlp 是一个命令行工具（CLI），用于从 TikTok 以及 [许多其他网站](https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md) 下载视频和音频。

## 设置

```bash
# macOS
brew install yt-dlp ffmpeg

# pip (any platform)
pip install yt-dlp
# Also install ffmpeg separately for merging/post-processing
```

---

## 下载模式

### 单个视频

```bash
yt-dlp "https://www.tiktok.com/@handle/video/1234567890"
```

### 整个用户资料

```bash
yt-dlp "https://www.tiktok.com/@handle" \
  -P "./tiktok/data" \
  -o "%(uploader)s/%(upload_date)s-%(id)s/video.%(ext)s" \
  --write-info-json
```

### 多个用户资料

```bash
for handle in handle1 handle2 handle3; do
  yt-dlp "https://www.tiktok.com/@$handle" \
    -P "./tiktok/data" \
    -o "%(uploader)s/%(upload_date)s-%(id)s/video.%(ext)s" \
    --write-info-json \
    --download-archive "./tiktok/downloaded.txt"
done
```

### 搜索、标签和音频

```bash
# Search by keyword
yt-dlp "tiktoksearch:cooking recipes" --playlist-end 20

# Hashtag page
yt-dlp "https://www.tiktok.com/tag/booktok" --playlist-end 50

# Videos using a specific sound
yt-dlp "https://www.tiktok.com/music/original-sound-1234567890" --playlist-end 30
```

### 格式选择

```bash
# List available formats
yt-dlp -F "https://www.tiktok.com/@handle/video/1234567890"

# Download specific format (e.g., best video without watermark if available)
yt-dlp -f "best" "https://www.tiktok.com/@handle/video/1234567890"
```

---

## 过滤

### 按日期

```bash
# On or after a date
--dateafter 20260215

# Before a date
--datebefore 20260220

# Exact date
--date 20260215

# Date range
--dateafter 20260210 --datebefore 20260220

# Relative dates (macOS / Linux)
--dateafter "$(date -u -v-7d +%Y%m%d)"           # macOS: last 7 days
--dateafter "$(date -u -d '7 days ago' +%Y%m%d)" # Linux: last 7 days
```

### 按指标和内容

```bash
# 100k+ views
--match-filters "view_count >= 100000"

# Duration between 30-60 seconds
--match-filters "duration >= 30 & duration <= 60"

# Title contains "recipe" (case-insensitive)
--match-filters "title ~= (?i)recipe"

# Combine: 50k+ views from Feb 2026
yt-dlp "https://www.tiktok.com/@handle" \
  --match-filters "view_count >= 50000" \
  --dateafter 20260201
```

---

## 仅获取元数据（不下载）

### 预览要下载的内容

```bash
yt-dlp "https://www.tiktok.com/@handle" \
  --simulate \
  --print "%(upload_date)s | %(view_count)s views | %(title)s"
```

### 导出为 JSON

```bash
# Single JSON array
yt-dlp "https://www.tiktok.com/@handle" --simulate --dump-json > handle_videos.json

# JSONL (one object per line, better for large datasets)
yt-dlp "https://www.tiktok.com/@handle" --simulate -j > handle_videos.jsonl
```

### 导出为 CSV

```bash
yt-dlp "https://www.tiktok.com/@handle" \
  --simulate \
  --print-to-file "%(uploader)s,%(id)s,%(upload_date)s,%(view_count)s,%(like_count)s,%(webpage_url)s" \
  "./tiktok/analysis/metadata.csv"
```

### 使用 jq 进行分析

```bash
# Top 10 videos by views from downloaded .info.json files
jq -s 'sort_by(.view_count) | reverse | .[:10] | .[] | {title, view_count, url: .webpage_url}' \
  tiktok/data/*/*.info.json

# Total views across all videos
jq -s 'map(.view_count) | add' tiktok/data/*/*.info.json

# Videos grouped by upload date
jq -s 'group_by(.upload_date) | map({date: .[0].upload_date, count: length})' \
  tiktok/data/*/*.info.json
```

> **提示：** 为了进行更深入的分析和可视化，可以使用 `pandas` 将 JSONL/CSV 文件导入 Python。这有助于生成互动图表、发布频率图或比较不同创作者的指标。

---

## 持续抓取

### 归档（跳过已下载的内容）

`--download-archive` 标志用于跟踪已下载的视频，从而实现增量更新：

```bash
yt-dlp "https://www.tiktok.com/@handle" \
  -P "./tiktok/data" \
  -o "%(uploader)s/%(upload_date)s-%(id)s/video.%(ext)s" \
  --write-info-json \
  --download-archive "./tiktok/downloaded.txt"
```

稍后再次运行相同的命令时，它会跳过 `downloaded.txt` 文件中已存在的视频。

### 认证（私密/受限内容）

```bash
# Use cookies from browser (recommended)
yt-dlp --cookies-from-browser chrome "https://www.tiktok.com/@handle"

# Or export cookies to a file first
yt-dlp --cookies tiktok_cookies.txt "https://www.tiktok.com/@handle"
```

### 定时抓取（Cron 任务）

```bash
# crontab -e
# Run daily at 2 AM, log output
0 2 * * * cd /path/to/project && ./scripts/scrape-tiktok.sh >> ./tiktok/logs/cron.log 2>&1
```

示例脚本 `scripts/scrape-tiktok.sh`：

```bash
#!/bin/bash
set -e

HANDLES="handle1 handle2 handle3"
DATA_DIR="./tiktok/data"
ARCHIVE="./tiktok/downloaded.txt"

for handle in $HANDLES; do
  echo "[$(date)] Scraping @$handle"
  yt-dlp "https://www.tiktok.com/@$handle" \
    -P "$DATA_DIR" \
    -o "%(uploader)s/%(upload_date)s-%(id)s/video.%(ext)s" \
    --write-info-json \
    --download-archive "$ARCHIVE" \
    --cookies-from-browser chrome \
    --dateafter "$(date -u -v-7d +%Y%m%d)" \
    --sleep-interval 2 \
    --max-sleep-interval 5
done
echo "[$(date)] Done"
```

---

## 故障排除

| 问题                                      | 解决方案                                      |
| ---------------------------------------- | --------------------------------------------------------------------------- |
| 没有找到结果/没有视频                         | 添加 `--cookies-from-browser chrome` — 解决 TikTok 对匿名请求的速率限制问题 |
| 403 禁止访问错误                         | 视频被限制访问。等待 10-15 分钟，或使用 cookies 或不同的 IP 地址           |
| “视频不可用”                             | 视频可能因地区限制而无法访问。尝试使用 `--geo-bypass` 或 VPN            |
| 视频带有水印                             | 使用 `-F` 选项查看其他格式；某些视频可能没有水印                   |
| 下载速度慢                                  | 添加 `--concurrent-fragments 4` 以加快下载速度                   |
| 用户资料中的视频数量少于预期                         | TikTok API 有下载限制。使用 `--playlist-end N` 显式指定下载范围，或尝试使用 cookies     |

### 调试模式

```bash
# Verbose output to diagnose issues
yt-dlp -v "https://www.tiktok.com/@handle" 2>&1 | tee debug.log
```

---

## 参考

### 关键选项

| 选项                        | 描述                                      |
| ----------------------------- | ------------------------------------------- |
| `-o TEMPLATE`                 | 输出文件模板                                  |
| `-P PATH`                     | 基本下载目录                                  |
| `--dateafter DATE`            | 仅在指定日期之后的视频下载                         |
| `--datebefore DATE`           | 仅在指定日期之前的视频下载                         |
| `--playlist-end N`            | 在下载 N 个视频后停止                             |
| `--match-filters EXPR`        | 根据元数据（观看次数、时长、标题等）进行过滤             |
| `--write-info-json`           | 为每个视频保存元数据 JSON 文件                         |
| `--download-archive FILE`     | 记录下载信息，跳过重复文件                         |
| `--simulate` / `-s`           | 进行模拟测试，不实际下载                             |
| `-j` / `--dump-json`          | 以 JSON 格式输出元数据                             |
| `--cookies-from-browser NAME`     | 使用浏览器中的 cookies                             |
| `--sleep-interval SEC`        | 在下载之间等待指定时间（避免速率限制）                         |

### 输出模板变量

| 变量                          | 示例输出                                        |
| ----------------------------- | --------------------------------------------------- |
| `%(id)s`          | `7331234567890`                                   |
| `%(uploader)s`    | 视频上传者名称                                   |
| `%(upload_date)s`    | 视频上传日期                                   |
| `%(title).50s`    | 标题的前 50 个字符                               |
| `%(view_count)s`    | 视频观看次数                                   |
| `%(like_count)s`    | 视频点赞次数                                   |
| `%(ext)s`         | 视频文件扩展名                                   |

[完整模板参考 →](https://github.com/yt-dlp/yt-dlp#output-template)