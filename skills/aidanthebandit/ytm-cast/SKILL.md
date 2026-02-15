---
name: youtube-music-cast
description: **从 YouTube/YouTube Music 下载音乐，并通过 Home Assistant 将音乐流媒体传输到 Chromecast。**  
该工具集提供了完整的命令行界面（CLI），支持与 Web 服务器的集成、配置向导以及播放控制功能。
version: "6.0.0"
author: Wobo
license: MIT
homepage: https://github.com/clawdbot/skills
repository: https://github.com/clawdbot/skills/tree/main/youtube-music-cast
user-invocable: true
triggers:
  - play music
  - cast to chromecast
  - youtube music
  - download music
  - cast music
keywords:
  - youtube
  - music
  - chromecast
  - home-assistant
  - cast
  - media-player
  - streaming
  - yt-dlp
  - google-cast
  - audio
  - mp3
  - free-music
category: media
requires:
  bins:
    - yt-dlp
    - python3
    - curl
    - jq
  env: []
config:
  stateDirs:
    - ~/.youtube-music-cast
metadata:
  clawdbot:
    emoji: "🎵"

---

# YouTube Music Cast

将YouTube上的音乐流媒体传输到您的Chromecast设备上。简单、免费，且无需任何额外费用。

您可以从YouTube或YouTube Music下载音频文件，然后通过Home Assistant将其流式传输到任何支持Cast功能的设备上。无需订阅服务或使用云存储服务，所有数据都存储在您的本地网络中。

## 主要特点

- ✅ **永久免费** — 无需订阅或高级账户
- ✅ **高音质** — 320K比特率的MP3格式，音质清晰
- ✅ **视频模式** — 可生成包含专辑封面和文字字幕的MP4视频
- ✅ **电台模式** — 自动发现并播放相关歌曲
- ✅ **本地存储** — 音乐文件保存在您的设备上，不会上传到云端
- ✅ **多房间支持** — 可将音乐流式传输到家中的任意Chromecast设备
- ✅ **批量下载** — 可下载整个播放列表，并随时播放
- ✅ **简洁的命令行接口** — 无需浏览器，命令简单易用
- ✅ **离线播放** — 下载完成后，音乐文件将永久保存在您的设备上

## 使用场景

### 日常音乐播放
早上下载喜欢的歌曲，然后全天播放。无需等待，也不会出现缓冲问题。

### 派对模式
在客人到来之前下载播放列表，之后直接通过该列表播放歌曲，无需使用手机或应用程序。

### 背景音乐
在工作时播放轻柔的音乐或播客，无需担心广告或干扰。

### 多房间同步
同时将同一首歌曲流式传输到多个Chromecast设备（例如卧室、客厅和厨房）。

## 为什么选择这个工具而非高级服务？

| 特点 | YouTube Music Cast | Spotify Premium | YouTube Premium |
|---------|-------------------|------------------|------------------|
| 成本 | 永久免费 | 每月10.99美元 | 每月13.99美元 |
| 音质 | 320K比特率的MP3 | 最高320K比特率 | 最高1080p分辨率的视频 |
| 离线播放 | 支持 | 有限制 | 不支持 |
| 广告 | 无 | 无 | 无 |
| 支持平台 | 任何Chromecast设备 | Spotify Connect设备 | YouTube应用程序 |
| 隐私保护 | 本地存储 | 基于云的存储 | 基于云的存储 |

## 快速入门

```bash
# 1. Setup (one time, takes 2 minutes)
cast-setup

# 2. Download your first song
cast-download https://youtube.com/watch?v=dQw4w9WgXcQ

# 3. Start the web server
cast-server start

# 4. Cast it to your default device
cast-play never-gonna-give-you-up.mp3
```

就这样，您的音乐就可以通过Chromecast设备播放了。

## 使用方法

只需三个简单步骤，每个步骤对应一个命令：

### 1. 下载音乐
`yt-dlp`工具从YouTube或YouTube Music下载音频文件，并将其转换为320K比特率的MP3格式。

### 2. 提供下载内容
一个轻量级的Python HTTP服务器会将下载的文件发布到您的本地网络中。无需额外设置，只需安装Python 3即可。

### 3. 流式传输
Home Assistant的`media_player.play_media`服务会将HTTP地址发送到Chromecast设备，从而实现音乐播放。

## 为什么使用Web服务器？

Home Assistant的`play_media`服务需要一个URL地址，而不是文件路径。Web服务器起到了桥梁作用。

```yaml
# ✅ This works — HA can fetch via HTTP
media_content_id: "http://192.168.1.81:8735/song.mp3"

# ❌ This fails — HA can't read file paths
media_content_id: "/tmp/youtube-music/song.mp3"
```

**系统架构：**
```
YouTube URL → yt-dlp → MP3 file → Python HTTP server → Home Assistant API → Chromecast
```

## 安装说明

### 所需工具

- 安装了Google Cast功能的Home Assistant
- Chromecast设备或支持Cast功能的设备（如Nest音箱、Google Home或电视）
- 系统工具：`yt-dlp`、Python 3、`curl`、`jq`

### 第一步：安装脚本

```bash
# Clone or download the skill
cd youtube-music-cast

# Make all scripts executable
chmod +x scripts/*

# Install globally (recommended)
./install.sh --global

# Or install locally
./install.sh
```

### 第二步：运行设置向导

```bash
cast-setup
```

设置向导会要求您提供以下信息：
- Home Assistant的URL地址（例如：`http://homeassistant.local:8123`
- 长期访问令牌（在Home Assistant的“配置”→“长期访问令牌”中生成）
- 服务器的IP地址
- 默认媒体播放器（例如：`media_player.bedroom_display`

### 第三步：测试设置

```bash
# Download a test song
cast-download https://youtube.com/watch?v=dQw4w9WgXcQ

# Start the server
cast-server start

# Cast it
cast-play song.mp3
```

如果音乐能够正常播放，说明设置成功！

## 常用命令

| 命令 | 功能 | 例子 |
|---------|-------------|----------|
| `cast-setup` | 运行配置向导 | `cast-setup` |
| `cast-download <URL> [选项]` | 从YouTube/YouTube Music下载文件 | `cast-download https://youtube.com/watch?v=... --video` |
| `cast-radio <URL> [选项]` | 启动电台模式并播放相关歌曲 | `cast-radio https://youtube.com/watch?v=... --count 10` |
| `cast-server [start|stop|status]` | 管理HTTP服务器 | `cast-server start` |
| `cast-play <文件> [设备]` | 将音乐或视频文件传输到设备 | `cast-play song.mp4` |
| `cast-stop [设备]` | 停止播放 | `cast-stop` |
| `cast-status [设备]` | 查看设备播放状态 | `cast-status` |
| `cast-devices` | 列出所有可用的媒体播放器 | `cast-devices` |
| `cast-list` | 列出已下载的文件 | `cast-list` |
| `cast-help` | 显示帮助信息 | `cast-help` |

## 使用指南

### 首次使用

```bash
# Download from YouTube
cast-download https://youtube.com/watch?v=dQw4w9WgXcQ

# Rename for cleaner URL (recommended)
mv "/tmp/youtube-music/Rick Astley - Never Gonna Give You Up.mp3" \
   "/tmp/youtube-music/never-gonna-give-you-up.mp3"

# Start the web server
cast-server start

# Cast to your default device
cast-play never-gonna-give-you-up.mp3
```

### 将音乐流式传输到不同房间

```bash
# Living room TV
cast-play song.mp3 media_player.living_room

# Kitchen speaker
cast-play song.mp3 media_player.kitchen_speaker

# Bedroom Chromecast
cast-play song.mp3 media_player.bedroom_display

# Multiple rooms at once (run multiple commands)
cast-play song.mp3 media_player.living_room & \
cast-play song.mp3 media_player.bedroom_display
```

### 查看当前正在播放的歌曲

```bash
# Default device
cast-status

# Specific device
cast-status media_player.bedroom_display
```

### 停止播放

```bash
# Stop default device
cast-stop

# Stop specific device
cast-stop media_player.living_room
```

### 查看已下载的文件

```bash
# List all music files with sizes
cast-list
```

### 查看可用的设备

```bash
cast-devices
```

### 新功能：电台模式与视频模式

### 📻 电台模式
电台模式会根据YouTube的推荐自动发现并下载相关歌曲。下载一首种子歌曲后，系统会搜索类似的歌曲并添加到播放列表中。

**启动电台模式：**

```bash
# Basic radio (downloads seed + 3 related songs)
cast-radio https://youtube.com/watch?v=dQw4w9WgXcQ

# Custom number of related songs
cast-radio https://youtube.com/watch?v=dQw4w9WgXcQ --count 10

# Radio mode with video files
cast-radio https://youtube.com/watch?v=dQw4w9WgXcQ --video --count 5
```

**或者使用`--radio`参数：**

```bash
# Download with radio mode
cast-download https://youtube.com/watch?v=dQw4w9WgXcQ --radio

# Download with custom count
cast-download https://youtube.com/watch?v=dQw4w9WgXcQ --radio --radio-count 5

# Radio + video mode combined
cast-download https://youtube.com/watch?v=dQw4w9WgXcQ --radio --video
```

**工作原理：**
1. 下载您指定的种子歌曲
2. 从元数据中提取艺术家和歌曲名称
3. 在YouTube上搜索类似的歌曲
4. 下载相关歌曲（文件名前会加上`radio_`前缀）
5. 相关歌曲会按顺序播放

**播放电台列表中的歌曲：**

```bash
# Start server
cast-server start

# Play the first song
cast-play $(ls -t /tmp/youtube-music/*.mp3 | head -n 1 | xargs basename)

# Or play related songs sequentially
cast-play radio_some-song.mp3
cast-play radio_another-song.mp3
# ... etc
```

**提示：**
- 相关歌曲的文件名前会加上`radio_`前缀，便于识别
- 电台模式会根据种子歌曲的艺术家名称进行搜索
- 使用`--count`参数来控制下载的歌曲数量
- 结合`--video`参数可以使用视频模式

### 🎬 带视频的字幕模式
视频模式会生成包含专辑封面和文字字幕的MP4视频。每个视频包含：
- 原始音频文件
- 来自YouTube的专辑封面缩略图
- 显示歌曲名称和艺术家的文字字幕
- 音质清晰

**下载视频文件：**

```bash
# Download as MP4 with album art and text
cast-download https://youtube.com/watch?v=dQw4w9WgXcQ --video

# Cast the MP4 file
cast-server start
cast-play "Never Gonna Give You Up.mp4"
```

**使用视频模式的电台：**

```bash
# Download seed + related songs as videos
cast-radio https://youtube.com/watch?v=dQw4w9WgXcQ --video --count 5

# Cast videos
cast-play "Never Gonna Give You Up.mp4"
cast-play "radio_Together Forever.mp4"
# ... etc
```

**工作原理：**
1. 下载音频文件（320K比特率）
2. 从YouTube下载专辑封面缩略图
3. 使用`ffmpeg`工具生成MP4视频：
   - 背景使用循环播放的专辑封面
   - 音频编码为AAC格式
   - 文字字幕显示歌曲名称和艺术家名称
4. 将MP4视频流式传输到Chromecast设备（支持视频的电视）

**视频输出参数：**
- 编码格式：H.264（libx264）
- 音频格式：AAC（192K比特率）
- 分辨率：与封面图片相同（通常为480p或720p）
- 文字显示：白色文本，使用DejaVu Sans Bold字体

**注意事项：**
- 视频文件比MP3文件占用更多存储空间（通常大2-3倍）
- 系统需要安装`ffmpeg`工具
- 文字字幕使用DejaVu Sans Bold字体（大多数Linux系统已预装）
- 仅支持音频的Chromecast设备（如Google Home Mini）只能播放音频
- 支持视频显示的Chromecast设备（如Google Nest Hub）可以显示完整视频

**视频模式的要求：**
- 系统必须安装`ffmpeg`工具
  ```bash
  # Debian/Ubuntu
  sudo apt install ffmpeg

  # macOS
  brew install ffmpeg
  ```

### 支持多种文件格式
`cast-play`命令可以自动识别以下文件类型：
- `.mp3`, `.wav`, `.ogg`, `.m4a`, `.flac` — 音频文件
- `.mp4`, `.mkv`, `.webm`, `.mov` — 视频文件
您可以在同一个目录中同时下载这两种类型的文件：
```bash
# Download some as MP3
cast-download https://youtube.com/watch?v=VIDEO_ID_1

# Download some as MP4
cast-download https://youtube.com/watch?v=VIDEO_ID_2 --video

# Play both - cast-play handles the difference
cast-play song.mp3
cast-play video.mp4
```

## 配置文件

配置文件位于`~/.youtube-music-cast/config.sh`：

**直接编辑该文件**或**重新运行`cast-setup`命令以更新配置。

## 文件命名规范

保持文件名简洁明了，这样可以避免后续使用时的麻烦。

### 常见问题及解决方法

### 问题：**文件名问题**
❌ 不规范的文件名会导致URL难以输入或编码错误。

**解决方案：** 使用规范的文件名，避免特殊字符和空格，使用小写字母和连字符。

### 实用技巧

- 文件名应使用小写字母
- 使用连字符代替空格
- 避免使用特殊字符（如@、#、?等）
- 文件名应简短

## 故障排除

### Chromecast设备未在Home Assistant中显示
**问题：** `cast-devices`列表中看不到Chromecast设备。

**解决方法：** 安装Google Cast插件：
1. 进入Home Assistant的“设置”→“设备与服务”
2. 点击“+ 添加插件”
3. 搜索“Google Cast”并安装
4. 按照向导完成配置

### 服务器无法启动
**问题：** `cast-server start`命令失败或显示“端口已被占用”。

**解决方法：**
检查`~/.youtube-music-cast/config.sh`文件中的服务器IP地址是否正确。

### 文件未找到
**问题：** `cast-play`命令提示文件未找到。

**解决方法：**
- 确保文件名拼写正确（例如：`song.mp3`而非`Song.mp3`）
- 检查配置文件中的`DOWNLOAD_DIR`设置是否正确

### 下载失败
**问题：** `cast-download`命令出现错误或卡顿。

**解决方法：**
- 如果遇到地理限制，尝试使用VPN或寻找其他来源的音频文件。

### Home Assistant连接问题
**问题：`curl`命令在连接Home Assistant时出现错误。

**解决方法：** 重新生成长期访问令牌。

### 视频模式问题
**问题：** 使用`cast-download --video`命令时出现错误。

**解决方法：**
- 视频生成过程可能较慢。首次生成视频可能需要10-30秒。
- 可以尝试使用仅音频模式的`cast-download`命令（不使用`--video`参数）以加快下载速度。
- 可以在脚本中调整视频质量设置（例如将`-preset ultrafast`改为`-preset fast`）。

### 其他问题

- Chromecast设备无法显示视频
- 音频-only的Chromecast设备（如Google Home Mini）只能播放音频。
- 如果需要显示视频，请确保使用MP3模式。

- 如果视频文件过大，可以尝试降低视频质量（例如将`-b:a 192k`改为`-b:a 128k`）。

### 电台模式相关问题
- 有时电台模式会下载不相关的歌曲。
- 确保种子歌曲的元数据完整（包含歌曲名称）。
- 可以尝试使用不同的种子歌曲。
- 如果搜索结果较少，可以增加`--radio-count`参数的值。

### 命令执行缓慢
- `cast-play`命令可能无法执行或无法开始播放。

**解决方法：**
- 检查媒体播放器的状态（使用`cast-devices`命令）
- 确保服务器可访问
- 如果需要，可以手动重新启动Chromecast设备
- 确保配置中的`SERVER_IP`地址正确

## 项目结构

### 所需软件及版本

- `yt-dlp`（YouTube下载工具）：`pip install --upgrade yt-dlp`
- Python 3（HTTP服务器）：确保已安装
- `curl`（用于调用Home Assistant API）
- `jq`（用于处理JSON数据）
- `ffmpeg`（可选，用于视频模式）

**版本更新：**
定期更新这些工具：

### 性能优化建议

- **批量下载**：可以一次性下载多首歌曲或整个播放列表。
- **保持服务器运行**：HTTP服务器占用内存较少（约5MB），无需在每次传输时重启服务器。
- **设置默认播放设备**：在配置文件中设置`DEFAULT_DEVICE`，避免每次都需要手动输入。
- **定期清理临时文件**：`/tmp/`目录中的文件会在系统重启时自动清除，但也可以手动清理。
- **WiFi网络**：确保Chromecast和服务器连接在同一WiFi网络上，避免干扰。
- **使用别名**：为常用命令创建shell别名以提高使用效率。

## 其他注意事项

- 文件存储在`/tmp/youtube-music/`目录中，系统重启时会自动清除。
- Web服务器在后台运行，会持续保存配置。
- 文件名应简洁明了。
- 服务器和Chromecast设备必须在同一网络中。
- 长期访问令牌存储在`config.sh`文件中，不要将其提交到Git仓库。
- 音质设置为320K比特率的MP3格式，兼顾音质和文件大小。
- 该工具不使用云服务，也不需要订阅。

## 与其他服务的比较

| 特点 | YouTube Music Cast | Spotify Free | YouTube Premium |
|---------|-------------------|----------------|-----------------|
| 成本 | 免费 | 免费（含广告） | 每月13.99美元 |
| 广告 | 无 | 有（每隔几首歌曲会出现广告） | 有（有限制） |
| 离线播放 | 支持 | 不支持 | 不支持 |
| 音质 | 320K比特率的MP3 | 160K比特率（可变） | 最高1080p视频 |
| 隐私保护 | 本地存储 | 基于云的存储 | 基于云的存储 |
| 支持平台 | 任何Chromecast设备 | Spotify Connect | YouTube应用程序 |
| 播放列表管理 | 手动 | 内置 | 内置 |
| 多房间支持 | 不支持 | 需要高级账户 | 不支持 |

**总结：** 如果您重视隐私、希望拥有自己的音乐资源且不需要云服务，那么这个工具非常适合您。

## 许可证

本项目采用MIT许可证，允许自由使用、修改和分享。

---

**版本：** 6.0.0
**作者：** Wobo
**许可证：** MIT许可证