---
name: mediaproc
description: 通过一个经过安全加固的 SSH 容器（使用 ffmpeg、sox 和 imagemagick 工具），处理媒体文件（视频、音频、图片）。当用户需要转码视频、处理音频、修改图片或操作媒体文件时，可以使用此方法。
compatibility: Requires ssh and a running mediaproc instance. MEDIAPROC_HOST and MEDIAPROC_PORT env vars must be set.
metadata:
  author: psyb0t
  homepage: https://github.com/psyb0t/docker-mediaproc
---
# mediaproc

这是一个通过 SSH 进行媒体处理的工具。它基于 [lockbox](https://github.com/psyb0t/docker-lockbox) 构建，确保没有 shell 访问权限，防止任何恶意代码的注入或攻击。

有关安装和部署的详细信息，请参阅 [references/setup.md](references/setup.md)。

## SSH 封装层

所有命令都通过 `scripts/mediaproc.sh` 脚本执行。该脚本通过 `MEDIAPROC_HOST` 和 `MEDIAPROC_PORT` 环境变量来配置主机地址和端口，并处理主机密钥的验证。

```bash
scripts/mediaproc.sh <command> [args]
scripts/mediaproc.sh <command> < input_file
scripts/mediaproc.sh <command> > output_file
```

## 媒体处理工具

| 命令            | 功能描述                                      |
| ---------------------------- | ------------------------------------------------------ |
| `ffmpeg`         | 视频/音频编码、转码、过滤                            |
| `ffprobe`        | 媒体文件分析                                    |
| `sox`           | 音频处理                                    |
| `soxi`          | 音频文件信息获取                                |
| `convert`        | 图像转换/处理（使用 ImageMagick 工具）                     |
| `identify`       | 图像文件信息获取（使用 ImageMagick 工具）                   |
| `magick`         | ImageMagick 的命令行界面                            |

## 上传、处理、下载

```bash
# Upload
scripts/mediaproc.sh "put input.mp4" < input.mp4

# Transcode
scripts/mediaproc.sh "ffmpeg -i /work/input.mp4 -c:v libx264 /work/output.mp4"

# Download result
scripts/mediaproc.sh "get output.mp4" > output.mp4

# Clean up
scripts/mediaproc.sh "remove-file input.mp4"
scripts/mediaproc.sh "remove-file output.mp4"
```

## 视频操作

```bash
# Get video info as JSON
scripts/mediaproc.sh "ffprobe -v quiet -print_format json -show_format -show_streams /work/video.mp4"

# Apply frei0r glow effect
scripts/mediaproc.sh "ffmpeg -i /work/in.mp4 -vf frei0r=glow:0.5 /work/out.mp4"

# Extract audio from video
scripts/mediaproc.sh "ffmpeg -i /work/video.mp4 -vn -acodec libmp3lame /work/audio.mp3"

# Create thumbnail from video
scripts/mediaproc.sh "ffmpeg -i /work/video.mp4 -ss 00:00:05 -vframes 1 /work/thumb.jpg"
```

## 音频操作

```bash
# Convert audio format
scripts/mediaproc.sh "sox /work/input.wav /work/output.mp3"

# Get audio info
scripts/mediaproc.sh "soxi /work/audio.wav"

# Normalize audio
scripts/mediaproc.sh "sox /work/input.wav /work/output.wav norm"
```

## 图像操作

```bash
# Resize image
scripts/mediaproc.sh "convert /work/input.png -resize 50% /work/output.png"

# Create thumbnail
scripts/mediaproc.sh "convert /work/input.jpg -thumbnail 200x200 /work/thumb.jpg"

# Get image info
scripts/mediaproc.sh "identify /work/image.png"
```

## 文件操作

所有文件路径都是相对于工作目录的。禁止直接访问这些文件。

| 命令                | 功能描述                                      |
| ---------------------- | ------------------------------------------------------ |
| `put <path>`        | 从标准输入（stdin）上传文件                         |
| `get <path>`        | 将文件下载到标准输出（stdout）                         |
| `list-files [--json]`     | 列出目录中的文件                                |
| `remove-file <path>`     | 删除文件                                    |
| `create-dir <path>`      | 创建目录                                    |
| `remove-dir <path>`      | 删除空目录                                    |
| `remove-dir-recursive <path>` | 递归删除目录                                |
| `move-file <src> <dst>`    | 移动或重命名文件                                |
| `copy-file <src> <dst>`    | 复制文件                                    |
| `file-info <path>`     | 获取文件的元数据（以 JSON 格式）                         |
| `file-exists <path>`     | 检查文件是否存在（返回 true/false）                     |
| `file-hash <path>`     | 获取文件的 SHA256 哈希值                             |
| `disk-usage <path>`     | 获取文件占用的磁盘空间（以字节为单位）                   |
| `search-files <glob>`     | 使用通配符搜索文件                                |
| `append-file <path>`     | 将标准输入的内容追加到文件中                         |

```bash
# List files
scripts/mediaproc.sh "list-files"

# List as JSON (size, modified, isDir, permissions)
scripts/mediaproc.sh "list-files --json"

# List subdirectory
scripts/mediaproc.sh "list-files project1"

# File operations
scripts/mediaproc.sh "create-dir project1"
scripts/mediaproc.sh "move-file old.mp4 new.mp4"
scripts/mediaproc.sh "copy-file input.mp4 backup.mp4"
scripts/mediaproc.sh "file-info video.mp4"
scripts/mediaproc.sh "file-exists video.mp4"
scripts/mediaproc.sh "file-hash video.mp4"
scripts/mediaproc.sh "search-files '*.mp4'"
scripts/mediaproc.sh "disk-usage"
scripts/mediaproc.sh "remove-dir-recursive project1"
```

## 插件

- **frei0r**      | 视频效果插件（通过 `-vf frei0r=...` 使用）                   |
- **LADSPA**      | 音频效果插件（支持 SWH、TAP、CMT 格式，通过 `-af ladspa=...` 使用）     |
- **LV2**        | 音频效果插件（通过 `-af lv2=...` 使用）                     |

## 字体

系统内置了 2200 多种字体，支持emoji、中文（CJK）、阿拉伯文、泰文、印度文字等多种字符集。用户可以将自定义字体安装到 `/usr/share/fonts/custom` 目录中。