---
name: youtube-playlists
description: 创建和管理 YouTube 播放列表。适用于用户需要创建播放列表、向播放列表中添加视频或管理现有 YouTube 播放列表的场景。
metadata: {"openclaw":{"emoji":"📋","requires":{"bins":["python3"]}}}
---

# YouTube 播放列表

通过 OAuth 功能创建和管理 YouTube 播放列表。

## 命令

```bash
# Authenticate (first time only)
python3 {baseDir}/scripts/yt_playlist.py auth

# Create empty playlist
python3 {baseDir}/scripts/yt_playlist.py create "Playlist Name"

# Add video to existing playlist  
python3 {baseDir}/scripts/yt_playlist.py add <playlist_id> <video_id_or_url>

# Create playlist with multiple videos (best for agent use)
python3 {baseDir}/scripts/yt_playlist.py bulk-create "Playlist Name" <video1> <video2> ...

# List your playlists
python3 {baseDir}/scripts/yt_playlist.py list
```

## 示例

创建一个 Zwift 观看列表：
```bash
python3 {baseDir}/scripts/yt_playlist.py bulk-create "Zwift Feb 3" \
  l3u_FAv33G0 \
  MY5omSLtAvk \
  VdaZqfEKv38 \
  Wq16lyNpmYs \
  SE7d4eaOJv4
```

## 注意事项：
- 首次运行时需要浏览器身份验证（会自动弹出认证窗口）
- 生成的访问令牌会保存在 `token.pickle` 文件中
- 可以使用视频 ID 或完整的 YouTube URL 来创建播放列表
- 批量创建播放列表时，默认隐私设置为“未公开”；单次创建时，默认隐私设置为“私密”。