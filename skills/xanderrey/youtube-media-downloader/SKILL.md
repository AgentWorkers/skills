---
name: youtube-downloader
description: 从 YouTube URL 下载音频（MP3）和视频（MP4）文件。适用于用户需要将 YouTube 视频转换为文件、提取音乐/歌曲、下载视频以供离线观看、保存教育资源或处理播放列表的场景。支持单个视频、播放列表以及批量下载，并提供多种质量选项。
---
# YouTube 媒体下载工具

从 YouTube 下载高质量的音频和视频文件，适用于离线使用、音乐转换和内容归档。

## 概述

该工具提供了全面的 YouTube 下载功能，包括质量控制、批量处理和多种格式选择，非常适合用于音乐提取、视频归档、教育内容处理以及播放列表管理。

## 快速入门

### 单个视频/音频下载
```bash
# Download as MP3 (default)
scripts/download_media.sh "https://www.youtube.com/watch?v=VIDEO_ID"

# Download as MP4 video
scripts/download_media.sh -v "https://www.youtube.com/watch?v=VIDEO_ID"

# Custom filename and directory
scripts/download_media.sh -o ~/Downloads "https://www.youtube.com/watch?v=VIDEO_ID" "my_song"
```

### 播放列表/批量下载
```bash
# Entire playlist as MP3
scripts/batch_download.sh "https://www.youtube.com/playlist?list=PLAYLIST_ID"

# Playlist items 5-10 as 720p video
scripts/batch_download.sh -v -q 720p -s 5 -e 10 "PLAYLIST_URL"

# From file list of URLs
scripts/batch_download.sh -f urls.txt
```

## 核心功能

### 音频提取
- **格式**：高质量 MP3
- **质量**：自动选择最佳质量的音频
- **适用场景**：音乐、播客、讲座、采访
- **命令**：默认行为（无需额外参数）

### 视频下载
- **格式**：MP4（最高兼容性）
- **质量选项**：最佳质量、720p、480p、360p、最低质量
- **适用场景**：离线观看、内容归档、教育用途
- **命令**：使用 `-v/--video` 参数

### 批量处理
- **播放列表**：支持整个播放列表的下载，并可指定下载范围
- **URL 文件**：可以处理包含多个 URL 的文本文件
- **文件命名**：播放列表文件会自动编号
- **控制选项**：可以设置下载的起始和结束位置，以及最大下载数量

## 质量选择指南

### 音频（MP3）
- **最佳质量**：自动从源视频中选择最高质量的音频
- **文件大小**：每首歌曲约 3-10MB
- **兼容性**：支持所有主流音频格式

### 视频质量选项
- **最佳质量**：最高质量的视频（1080p+，文件较大）
- **720p**：高清质量，文件大小适中（约 50-200MB）
- **480p**：标清质量，适合移动设备（约 20-80MB）
- **360p**：较低质量，文件较小（约 10-30MB）

## 高级用法

### 文件组织选项
```bash
# Specific output directory
-o ~/Downloads/Music

# Date-based folders
-o ~/Downloads/$(date +%Y-%m-%d)
```

### 播放列表范围控制
```bash
# Specific range (items 10-20)
-s 10 -e 20

# From specific item to end
-s 25

# Limit total downloads
-m 50
```

### 文件输入格式
创建一个 `urls.txt` 文件，每行包含一个 YouTube 链接：
```
https://www.youtube.com/watch?v=video1
https://www.youtube.com/watch?v=video2
```
然后运行：`batch_download.sh -f urls.txt`

## 脚本参考

### download_media.sh
**用途**：单个视频/音频下载
**关键参数**：
- `-a/--audio`：仅下载音频（默认）
- `-v/--video`：下载视频（MP4 格式）
- `-q/--quality`：选择视频质量
- `-o/--output`：指定输出目录

### batch_download.sh
**用途**：批量下载播放列表中的视频
**关键参数**：
- `-s/--start`：指定下载范围的起始位置
- `-e/--end`：指定下载范围的结束位置
- `-m/--max-downloads`：限制最大下载数量
- `-f/--file`：指定包含下载链接的文件
- 支持所有单个下载相关的参数

## 最佳实践与使用技巧

有关详细的用法指南、质量设置建议和故障排除方法，请参阅 [download-patterns.md](references/download-patterns.md)。

## 技术说明

- **自动安装**：根据需要，脚本会自动安装 `yt-dlp` 和 `ffmpeg` 工具。
- **便携式设置**：下载的程序为便携版本，无需系统管理员权限。
- **下载中断恢复**：即使部分下载失败，整个流程仍会继续。
- **错误处理**：批量下载过程中遇到问题时，其他任务会继续执行。
- **格式优先级**：优先尝试下载 MP4 格式的视频文件，MP3 格式的音频文件。
- **文件命名**：文件名会自动根据视频标题生成（除非另有指定）。

## 法律与道德使用规范

- **个人用途**：仅限个人离线观看。
- **尊重版权**：严禁传播受版权保护的内容。
- **遵守服务条款**：请遵守 YouTube 的服务条款。
- **合理使用**：在教育用途下，请遵循合理的版权使用准则。