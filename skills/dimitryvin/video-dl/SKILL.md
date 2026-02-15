---
name: video-dl
description: 使用 yt-dlp 从 YouTube、Reddit、Twitter/X、TikTok、Instagram 以及 1000 多个其他网站下载视频。当用户提供视频链接并希望下载该视频时，可以使用此工具。
---

# 视频下载工具

使用 `yt-dlp` 可以从几乎所有网站下载视频。

## 支持的网站

YouTube、Reddit、Twitter/X、TikTok、Instagram、Vimeo、Facebook、Twitch 以及 1000 多个其他网站。完整列表：  
https://github.com/yt-dlp/yt-dlp/blob/master/supportedsites.md

## 使用方法

### 快速下载（最佳质量）

```bash
{baseDir}/scripts/download.sh "URL"
```

视频将被下载到 `~/Downloads/videos/` 目录中，且采用最佳质量。

### 带参数的下载

```bash
{baseDir}/scripts/download.sh "URL" [OPTIONS]
```

**常用参数：**
- `--audio-only` 仅提取音频（格式：mp3）
- `--720p` 最大分辨率限制为 720p
- `--1080p` 最大分辨率限制为 1080p
- `--output DIR` 自定义输出目录
- `--filename NAME` 自定义文件名（不包含扩展名）

### 使用示例

```bash
# Download YouTube video (best quality)
{baseDir}/scripts/download.sh "https://www.youtube.com/watch?v=dQw4w9WgXcQ"

# Download Reddit video
{baseDir}/scripts/download.sh "https://www.reddit.com/r/videos/comments/abc123/cool_video/"

# Extract audio only
{baseDir}/scripts/download.sh "https://www.youtube.com/watch?v=dQw4w9WgXcQ" --audio-only

# Download to specific folder
{baseDir}/scripts/download.sh "URL" --output ~/Videos/projects

# Custom filename
{baseDir}/scripts/download.sh "URL" --filename "my-video"
```

## 下载结果

- 默认保存路径：`~/Downloads/videos/`
- 文件名格式：`{title}-{id}.{ext}`
- 成功下载后，会返回文件的完整路径

## 注意事项

- Reddit 上的视频需要合并视频和音频文件（该过程会自动完成）
- 受年龄限制的 YouTube 视频可能需要使用 Cookie（当前未配置）
- 非常长的视频下载可能需要较长时间；脚本会显示下载进度
- 如果下载失败，请检查目标网站是否受支持，或者视频是否被设置为私密或已删除

## 发送到 Telegram

由于 Telegram 的文件大小限制为 16MB，较大的视频需要先进行压缩。对于较长的视频，请按照以下步骤操作：

1. 先正常下载视频。
2. 在后台运行压缩工具：
   ```bash
   nohup {baseDir}/scripts/compress-and-send.sh "/path/to/video.mp4" "CHAT_ID" > /tmp/compress.log 2>&1 &
   ```
3. 等待压缩完成（压缩时间约为视频时长除以 4）。
4. 然后将压缩后的文件（格式：`-telegram.mp4`）发送到 Telegram。

这样可以避免在聊天中频繁发送进度更新信息。

## 直接使用 `yt-dlp`

如需高级使用，`yt-dlp` 可以通过 `~/.local/bin/yt-dlp`（已更新版本）或 `/usr/bin/yt-dlp` 进行访问。使用 `yt-dlp --help` 可查看所有参数和选项。