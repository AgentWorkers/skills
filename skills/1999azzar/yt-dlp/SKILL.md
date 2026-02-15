---
name: yt-dlp
description: 这是一个功能强大的命令行界面（CLI）封装工具，用于通过 `yt-dlp` 下载 YouTube 及数千个其他网站的视频、播放列表和音频文件。它支持格式选择、质量控制、元数据嵌入以及基于 Cookie 的身份验证功能。
---

# yt-dlp 技能

## 概述
该技能提供了一个便捷的接口，用于调用 `yt-dlp`——一个功能强大的命令行媒体下载工具。它简化了视频下载、音频提取以及播放列表管理的流程，并支持最优的质量设置和元数据处理。

## 使用方法
- **角色**：媒体归档员。
- **触发命令**：`下载这个视频`、`从 YouTube 下载 MP3`、`归档这个频道`。
- **输出结果**：下载的媒体文件将保存在当前目录或指定的输出路径中。

## 依赖项
- `yt-dlp`：核心下载工具（必须已安装并添加到系统的 PATH 环境变量中）。
- `ffmpeg`：用于合并视频和音频流以及进行格式转换。

## 命令

### `scripts/download.sh`
该脚本是主要的入口点，它为 `yt-dlp` 提供了合理的默认配置，以实现高质量的视频归档。

**语法：**
```bash
./scripts/download.sh <URL> [OPTIONS]
```

**默认配置**：
- 合并最佳质量的视频和音频文件（`bv+ba/b`）
- 嵌入元数据、缩略图和字幕（`--embed-metadata`、`--embed-thumbnail`、`--embed-subs`）
- 输出文件格式：`Title [ID].mp4`（`%(title)s [%(id)s].%(ext)s`）

**示例**：
1. **下载单个视频（最高质量）：**
    ```bash
    scripts/download.sh "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    ```

2. **下载整个播放列表：**
    ```bash
    scripts/download.sh "https://www.youtube.com/playlist?list=PL..."
    ```

3. **提取音频（MP3 格式）：**
    ```bash
    scripts/download.sh "URL" -x --audio-format mp3
    ```

4. **下载特定分辨率的视频（例如 1080p）：**
    ```bash
    scripts/download.sh "URL" -f "bv*[height<=1080]+ba/b[height<=1080]"
    ```

5. **使用浏览器 Cookie（用于访问受限制或需要付费的内容）：**
    *注意：需要将浏览器 Cookie 导出到文件中或直接使用。*
    ```bash
    scripts/download.sh "URL" --cookies-from-browser chrome
    ```

## 安装与安全注意事项
该技能依赖于 `yt-dlp` 和 `ffmpeg` 在宿主系统上的安装。
- **仅从官方渠道安装**：通过 `pip install yt-dlp` 或相应的系统包管理器（如 `apt`、`brew`）进行安装。避免从不可信的来源运行脚本。
- **Cookie 使用**：使用 `--cookies-from-browser` 时需谨慎操作。对于自主运行的脚本，建议手动导出 `cookies.txt` 文件，以限制对当前浏览器会话的访问权限。

## 参考指南
有关高级用法，请参阅详细的 [使用指南](references/guide.md)。