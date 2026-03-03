---
name: download
description: 将 YouTube 视频下载到 `~/Downloads` 目录中。适用于用户希望将 YouTube 视频下载到自己电脑上的情况。
metadata: {"openclaw": {"emoji": "⬇️", "requires": {"bins": ["yt-dlp"]}, "install": [{"id": "brew", "kind": "brew", "formula": "yt-dlp", "bins": ["yt-dlp"], "label": "Install yt-dlp (brew)"}], "user-invocable": true}}
---
# 下载功能

使用 `yt-dlp` 将 YouTube 视频下载到您的 `~/Downloads` 文件夹中。

## 功能说明

- 接受一个 YouTube 链接作为输入
- 下载该视频的最高可用质量版本（视频和音频合并为 MP4 格式）
- 将下载后的文件保存到 `~/Downloads` 文件夹中，文件名使用视频的标题作为文件名

## 使用方法

```bash
{baseDir}/download.sh "https://youtube.com/watch?v=VIDEO_ID"
```

或者，您只需提供视频的 URL，我就会为您执行下载操作。

## 系统要求

- 必须安装 `yt-dlp`：`brew install yt-dlp`
- 首次运行时，如果系统中没有 `yt-dlp`，该工具会提示您进行安装。