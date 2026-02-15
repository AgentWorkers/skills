---
name: mediaproc
description: 通过一个经过安全配置的 SSH 容器（使用 ffmpeg、sox 和 imagemagick 工具），处理媒体文件（视频、音频、图片）。
homepage: https://github.com/psyb0t/docker-mediaproc
user-invocable: true
metadata:
  {
    "openclaw":
      {
        "emoji": "🎬",
        "primaryEnv": "MEDIAPROC_HOST",
        "always": true,
      },
  }
---

# mediaproc

## 必需的设置

使用此技能需要设置 `MEDIAPROC_HOST` 和 `MEDIAPROC_PORT` 环境变量，这些变量应指向正在运行的 mediaproc 实例。

**配置 OpenClaw**（文件：`~/.openclaw/openclaw.json`）：

```json
{
  "skills": {
    "entries": {
      "mediaproc": {
        "env": {
          "MEDIAPROC_HOST": "localhost",
          "MEDIAPROC_PORT": "2222"
        }
      }
    }
  }
}
```

或者直接设置环境变量：

```bash
export MEDIAPROC_HOST=localhost
export MEDIAPROC_PORT=2222
```

---

通过 SSH 进行安全的媒体处理。该系统使用 Python 封装层来限制可执行的命令，仅允许预定义的命令；禁止访问 shell、防止代码注入等安全风险。

## 首次连接

在运行任何命令之前，您必须接受目标主机的密钥，以便将其添加到 `known_hosts` 文件中。运行 `ls` 命令并接受显示的主机密钥指纹：

```bash
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "ls"
```

如果这是首次连接，SSH 会提示您验证主机密钥。输入 `yes` 即可完成验证。每个主机只需执行此操作一次。如果跳过此步骤，后续的 SSH 命令将会因密钥验证失败而失败。

## 工作原理

所有命令都是通过 SSH 传递给 mediaproc 容器执行的。该容器强制所有连接都必须通过一个 Python 封装层，该层仅允许执行预定义的命令。所有文件路径都被限制在容器内的 `/work` 目录内。

**SSH 命令格式：**

```bash
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "<command> [args]"
```

## 媒体处理工具

| 命令            | 可执行文件                | 功能描述                                      |
| ------------------------- | ---------------------- | -------------------------------------------- |
| `ffmpeg`       | `/usr/bin/ffmpeg`         | 视频/音频编码、转码、过滤                     |
| `ffprobe`      | `/usr/bin/ffprobe`         | 媒体文件分析                                    |
| `sox`         | `/usr/bin/sox`          | 音频处理                                    |
| `soxi`         | `/usr/bin/soxi`          | 音频文件信息获取                              |
| `convert`      | `/usr/bin/convert`         | 图像转换/处理（使用 ImageMagick）                |
| `identify`     | `/usr/bin/identify`        | 图像文件信息获取（使用 ImageMagick）                |
| `magick`       | `/usr/bin/magick`         | ImageMagick 命令行工具                        |

## 文件操作

所有文件路径都是相对于 `/work` 目录的。尝试访问其他目录会被阻止；绝对路径会被重定向到 `/work` 目录下。

| 命令            | 功能描述                                      | 示例                                        |
| ------------------------- | ------------------------------------------------- | ------------------------------------------ |
| `ls`          | 列出 `/work` 目录或其子目录                        | `ls` 或 `ls --json subdir`                        |
| `put`          | 从标准输入（stdin）上传文件                         | `put video.mp4`                                   |
| `get`          | 将文件下载到标准输出（stdout）                         | `get output.mp4`                                   |
| `rm`          | 删除文件（不支持删除目录）                          | `rm old.mp4`                                   |
| `mkdir`        | 创建目录（支持递归）                              | `mkdir project1`                                |
| `rmdir`        | 删除空目录                                  | `rmdir project1`                                |
| `rrmdir`       | 递归删除目录及其所有内容                          | `rrmdir project1`                                |

## 使用示例

### 上传并处理文件

```bash
# Upload
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "put input.mp4" < input.mp4

# Transcode
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "ffmpeg -i /work/input.mp4 -c:v libx264 /work/output.mp4"

# Download result
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "get output.mp4" > output.mp4

# Clean up
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "rm input.mp4"
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "rm output.mp4"
```

### 视频操作

```bash
# Get video info as JSON
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "ffprobe -v quiet -print_format json -show_format -show_streams /work/video.mp4"

# Apply frei0r glow effect
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "ffmpeg -i /work/in.mp4 -vf frei0r=glow:0.5 /work/out.mp4"

# Extract audio from video
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "ffmpeg -i /work/video.mp4 -vn -acodec libmp3lame /work/audio.mp3"

# Create thumbnail from video
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "ffmpeg -i /work/video.mp4 -ss 00:00:05 -vframes 1 /work/thumb.jpg"
```

### 音频操作

```bash
# Convert audio format
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "sox /work/input.wav /work/output.mp3"

# Get audio info
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "soxi /work/audio.wav"

# Normalize audio
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "sox /work/input.wav /work/output.wav norm"
```

### 图像操作

```bash
# Resize image
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "convert /work/input.png -resize 50% /work/output.png"

# Create thumbnail
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "convert /work/input.jpg -thumbnail 200x200 /work/thumb.jpg"

# Get image info
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "identify /work/image.png"
```

### 文件管理

```bash
# List files (ls -alph style, no . and ..)
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "ls"
# drwxrwxr-x   2 mediaproc mediaproc     4096 Jan 25 14:30 project1/
# -rw-rw-r--   1 mediaproc mediaproc  1048576 Jan 25 14:32 video.mp4

# List files as JSON (use --json flag)
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "ls --json"
# [{"name": "video.mp4", "size": 1048576, "modified": 1706140800, "isDir": false, "mode": "rw-rw-r--", "owner": "mediaproc", "group": "mediaproc", "links": 1}, ...]

# List subdirectory
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "ls project1"

# Create subdirectory
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "mkdir project1"

# Remove directory recursively
ssh -p $MEDIAPROC_PORT mediaproc@$MEDIAPROC_HOST "rrmdir project1"
```

## 可用的插件

- **frei0r** - 视频效果插件（通过 `-vf frei0r=...` 使用）  
- **LADSPA** - 音频效果插件（支持 SWH、TAP、CMT 等效果，通过 `-af ladspa=...` 使用）  
- **LV2** - 音频插件（通过 `-af lv2=...` 使用）  

## 字体

系统内置了 2200 多种字体，支持emoji、CJK、阿拉伯文、泰文、印度文等多种文字类型。自定义字体可以安装到 `/usr/sharefonts/custom` 目录下。

## 安全注意事项

- 禁止访问 shell：所有命令都必须通过 Python 封装层执行  
- 仅允许预定义的命令：未列出的命令将被拒绝  
- 防止代码注入：`&&`、`;`、`|`、`$()` 等符号被视为普通参数，不会被解释为 shell 命令  
- 仅使用 SSH 密钥认证：不支持密码输入  
- 禁止所有数据转发功能  
- 所有文件路径都被限制在 `/work` 目录内