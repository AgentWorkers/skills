---
name: yt-thumbnail-grabber
description: 下载 YouTube 视频的缩略图，支持多种分辨率。这些缩略图可用于获取视频预览图片、制作拼贴画或保存以供参考。
metadata: {"openclaw":{"requires":{"bins":["yt-dlp"]},"install":[{"id":"python","kind":"pip","package":"yt-dlp","bins":["yt-dlp"],"label":"Install yt-dlp (pip)"}]}}
---

# YouTube缩略图下载工具

## 设置

安装 yt-dlp：
```bash
pip install yt-dlp
```

## 下载缩略图

使用 yt-dlp：
```bash
yt-dlp --write-thumbnail --skip-download "VIDEO_URL"
```

将缩略图转换为 JPG 格式：
```bash
yt-dlp --write-thumbnail --skip-download --convert-thumbnails jpg "VIDEO_URL"
```

自定义输出路径：
```bash
yt-dlp --write-thumbnail --skip-download -o "thumbnail" "VIDEO_URL"
```

## 直接获取缩略图 URL 的方法

获取缩略图 URL：
```bash
yt-dlp --get-thumbnail "VIDEO_URL"
```

使用 curl 下载缩略图：
```bash
curl -o thumbnail.jpg "$(yt-dlp --get-thumbnail 'VIDEO_URL')"
```

## 缩略图 URL 的获取规则

对于视频 ID `VIDEO_ID`，缩略图可以在以下地址获取：
```
# Maximum resolution (may not exist for all videos)
https://img.youtube.com/vi/VIDEO_ID/maxresdefault.jpg

# High quality (480x360)
https://img.youtube.com/vi/VIDEO_ID/hqdefault.jpg

# Medium quality (320x180)
https://img.youtube.com/vi/VIDEO_ID/mqdefault.jpg

# Standard quality (640x480)
https://img.youtube.com/vi/VIDEO_ID/sddefault.jpg

# Default (120x90)
https://img.youtube.com/vi/VIDEO_ID/default.jpg
```

## 通过视频 ID 快速下载缩略图

```bash
VIDEO_ID="dQw4w9WgXcQ"

# Max resolution
curl -o "thumb_max.jpg" "https://img.youtube.com/vi/${VIDEO_ID}/maxresdefault.jpg"

# HQ
curl -o "thumb_hq.jpg" "https://img.youtube.com/vi/${VIDEO_ID}/hqdefault.jpg"
```

## 下载所有分辨率的缩略图

```bash
VIDEO_ID="dQw4w9WgXcQ"

for res in maxresdefault sddefault hqdefault mqdefault default; do
    curl -o "${VIDEO_ID}_${res}.jpg" "https://img.youtube.com/vi/${VIDEO_ID}/${res}.jpg"
done
```

## 从 URL 中提取视频 ID

```bash
# From full URL
echo "https://www.youtube.com/watch?v=dQw4w9WgXcQ" | grep -oP '(?<=v=)[^&]+'

# Or using yt-dlp
yt-dlp --get-id "VIDEO_URL"
```

## 批量下载缩略图

- 从播放列表中下载：
```bash
yt-dlp --write-thumbnail --skip-download -o "%(title)s" "PLAYLIST_URL"
```

- 从包含视频 URL 的文件中下载：
```bash
yt-dlp --write-thumbnail --skip-download -a urls.txt
```

## 下载带有元数据的缩略图

```bash
yt-dlp --dump-json "VIDEO_URL" | python3 -c "
import sys, json
d = json.load(sys.stdin)
print(f\"Title: {d['title']}\")
print(f\"Thumbnail: {d['thumbnail']}\")
for t in d.get('thumbnails', []):
    print(f\"  {t.get('width', '?')}x{t.get('height', '?')}: {t['url']}\")"
```

## 下载最佳质量的缩略图

```bash
python3 -c "
import sys
import urllib.request

video_id = sys.argv[1]
resolutions = ['maxresdefault', 'sddefault', 'hqdefault', 'mqdefault', 'default']

for res in resolutions:
    url = f'https://img.youtube.com/vi/{video_id}/{res}.jpg'
    try:
        urllib.request.urlretrieve(url, f'{video_id}.jpg')
        print(f'Downloaded: {res} ({url})')
        break
    except:
        continue
" "VIDEO_ID"
```

## 缩略图的分辨率

| 名称 | 分辨率 | 备注 |
|------|------------|-------|
| maxresdefault | 1280x720 | 不总是可用 |
| sddefault | 640x480 | 标准分辨率 |
| hqdefault | 480x360 | 高质量 |
| mqdefault | 320x180 | 中等质量 |
| default | 120x90 | 始终可用 |
| 0, 1, 2, 3 | 120x90 | 视频帧截图 |

## 备用的缩略图帧

YouTube 会存储多个视频帧的截图：
```bash
VIDEO_ID="dQw4w9WgXcQ"

# Different moments from the video
curl -o "frame0.jpg" "https://img.youtube.com/vi/${VIDEO_ID}/0.jpg"
curl -o "frame1.jpg" "https://img.youtube.com/vi/${VIDEO_ID}/1.jpg"
curl -o "frame2.jpg" "https://img.youtube.com/vi/${VIDEO_ID}/2.jpg"
curl -o "frame3.jpg" "https://img.youtube.com/vi/${VIDEO_ID}/3.jpg"
```

## 注意事项：

- `maxresdefault` 仅适用于高清视频
- 如果无法获取最高分辨率，系统会自动使用 `hqdefault`
- YouTube 会缓存缩略图
- 公共视频无需身份验证即可下载
- 可能返回 WebP 格式的缩略图；使用 `--convert-thumbnails jpg` 命令进行转换
- 缩略图帧（0-3）分别代表视频的不同时刻