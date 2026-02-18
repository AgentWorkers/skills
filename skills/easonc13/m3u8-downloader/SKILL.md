---
name: m3u8-downloader
description: 使用并行下载方式来下载加密的 m3u8/HLS 视频。当您获得一个 m3u8 URL 时，可以使用此方法来下载视频，尤其是那些采用 AES-128 加密方式的 HLS 流。
---
# M3U8 视频下载工具

支持并行下载多个视频片段，并自动解密 HLS/m3U8 格式的视频文件。

## 先决条件

- `aria2c`（安装方法：`brew install aria2`）
- `ffmpeg`（安装方法：`brew install ffmpeg`）

## 完整工作流程（从网页到 MP4 文件）

### 第一步：从网页中提取 m3u8 URL

如果提供的是一个网页 URL（而非直接的 m3u8 文件），请使用浏览器自动化工具来获取视频流的 URL：

```javascript
// In browser console or via browser tool evaluate
(() => {
  // Check HLS.js player instance
  if (window.hls && window.hls.url) return window.hls.url;
  if (window.player && window.player.hls && window.player.hls.url) return window.player.hls.url;
  
  // Search window objects for m3u8 URLs
  const allVars = Object.keys(window).filter(k => {
    try {
      return window[k] && typeof window[k] === 'object' && 
             window[k].url && window[k].url.includes('m3u8');
    } catch(e) { return false; }
  });
  return allVars.length > 0 ? allVars.map(k => window[k].url) : 'not found';
})()
```

建议使用 `profile=openclaw`（独立的浏览器环境）以避免浏览器历史记录的影响。

### 第二步：处理主播放列表（多画质选项）

主播放列表会列出不同的画质选项，而不是具体的视频片段：

```bash
curl -s "https://example.com/playlist.m3u8"
# Output example:
# #EXT-X-STREAM-INF:BANDWIDTH=8247061,RESOLUTION=1920x1080
# 1080p/video.m3u8
# #EXT-X-STREAM-INF:BANDWIDTH=4738061,RESOLUTION=1280x720
# 720p/video.m3u8
```

选择最高质量的视频（例如 1080p），然后获取对应的子播放列表：

```bash
BASE_URL="https://example.com"
curl -s "${BASE_URL}/1080p/video.m3u8"
```

### 第三步：提取视频片段的 URL

视频片段的扩展名可能不符合标准格式（例如使用 `.jpeg` 而不是 `.ts`）：

```bash
mkdir -p /tmp/video_download && cd /tmp/video_download

BASE_URL="https://example.com/1080p"
curl -s "${BASE_URL}/video.m3u8" | grep -E "^[^#]" | while read seg; do
  echo "${BASE_URL}/${seg}"
done > urls.txt

# Count segments
wc -l urls.txt
```

### 第四步：使用 aria2c 进行并行下载

```bash
aria2c -i urls.txt -j 16 -x 16 -s 16 --file-allocation=none -c true \
  --console-log-level=warn --summary-interval=30
```

- `-j 16`：同时进行 16 个下载任务
- `-x 16`：每个文件使用 16 个连接进行下载
- `-c true`：允许下载未完成的文件片段

### 第五步：使用 ffmpeg 合并下载的文件

```bash
# Get segment count
NUM_SEGMENTS=$(wc -l < urls.txt)

# Generate file list (adjust filename pattern as needed)
for i in $(seq 0 $((NUM_SEGMENTS-1))); do
  echo "file 'video${i}.jpeg'"  # or video${i}.ts
done > filelist.txt

# Merge (copy streams, no re-encoding)
ffmpeg -y -f concat -safe 0 -i filelist.txt -c copy ~/Downloads/output.mp4
```

### 第六步：清理临时文件

```bash
rm -rf /tmp/video_download
```

## 快速脚本使用方法

```bash
~/clawd/skills/m3u8-downloader/scripts/download.sh "https://example.com/video.m3u8" "output_name"
```

注意：该脚本可能无法处理所有特殊情况（如复杂的播放列表结构或非标准的文件扩展名）。对于复杂的视频流，请手动执行上述步骤。

## 处理加密流（AES-128 加密）

在播放列表中查找 `#EXT-X-KEY:METHOD=AES-128,URI="enc.key"` 这一行，以确定视频是否被加密：

```bash
curl -s "https://example.com/path/enc.key" -o enc.key
ffmpeg -allowed_extensions ALL -i local_playlist.m3u8 -c copy output.mp4
```

## 输出结果

最终的视频文件将保存在 `~/Downloads/<output_name>.mp4` 目录下。