---
name: youtube
description: 使用 YouTube Data API v3（通过 MCP 服务器或 yt-dlp 备选方案），搜索 YouTube 视频、获取频道信息、提取视频详情以及字幕。
metadata: {"clawdbot":{"emoji":"📹","requires":{"bins":["yt-dlp"],"npm":["zubeid-youtube-mcp-server"]},"primaryEnv":"YOUTUBE_API_KEY"}}
---

# YouTube研究与转录

使用YouTube Data API v3搜索YouTube视频，获取视频/频道信息，并提取字幕。

## 功能

- 📹 视频详情（标题、描述、统计数据、发布日期）
- 📝 带时间戳的字幕
- 📺 频道信息及最新视频
- 🔍 在YouTube内搜索
- 🎬 播放列表信息

## 设置

### 1. 安装依赖项

**MCP服务器（推荐方法）：**
```bash
npm install -g zubeid-youtube-mcp-server
```

**备用工具（如果MCP失败时使用）：**
```bash
# yt-dlp for transcript extraction
pip install yt-dlp
```

### 2. 获取YouTube API密钥

1. 访问[Google Cloud Console](https://console.cloud.google.com)
2. 创建/选择一个项目（例如：“YouTube Research”）
3. 启用API：
   - 菜单 → “APIs & Services” → “Library”
   - 搜索：“YouTube Data API v3”
   - 点击“Enable”
4. 创建凭证：
   - “APIs & Services” → “Credentials”
   - “Create Credentials” → “API Key”
   - 复制密钥
5. 可选 - 限制使用范围：
   - 点击创建的密钥
   - “API restrictions” → 仅选择“YouTube Data API v3”
   - 保存设置

### 3. 配置API密钥

**选项A：Clawdbot配置**（推荐）
将密钥添加到`~/.clawdbot/clawdbot.json`文件中：
```json
{
  "skills": {
    "entries": {
      "youtube": {
        "apiKey": "AIzaSy..."
      }
    }
  }
}
```

**选项B：环境变量**
```bash
export YOUTUBE_API_KEY="AIzaSy..."
```

### 4. 设置MCP服务器

该技能将使用`mcporter`来调用YouTube MCP服务器：
```bash
# Build from source (if installed package has issues)
cd /tmp
git clone https://github.com/ZubeidHendricks/youtube-mcp-server
cd youtube-mcp-server
npm install
npm run build
```

## 使用方法

### 搜索视频

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  search_videos query="ClawdBot AI" maxResults:5
```

返回视频ID、标题、描述和频道信息。

### 获取频道信息

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  channels_info channelId="UCSHZKyawb77ixDdsGog4iWA"
```

### 列出频道的最新视频

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  channels_listVideos channelId="UCSHZKyawb77ixDdsGog4iWA" maxResults:5
```

### 获取视频详情

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  videos_details videoId="Z-FRe5AKmCU"
```

### 获取字幕（主要方法）

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  transcripts_getTranscript videoId="Z-FRe5AKmCU"
```

### 使用yt-dlp获取字幕（备用方法）

如果MCP无法获取字幕（字幕为空或不可用），可以使用`yt-dlp`：
```bash
yt-dlp --skip-download --write-auto-sub --sub-lang en --sub-format vtt \
  --output "/tmp/%(id)s.%(ext)s" \
  "https://youtube.com/watch?v=Z-FRe5AKmCU"
```

然后从`/tmp/`目录读取`.vtt`文件。

**或直接获取字幕：**
```bash
yt-dlp --skip-download --write-auto-sub --sub-lang en --print "%(subtitles)s" \
  "https://youtube.com/watch?v=VIDEO_ID" 2>&1 | grep -A1000 "WEBVTT"
```

## 常见工作流程

### 1. 查找播客的最新剧集

**示例：Lex Fridman Podcast**

```bash
# Get channel ID (Lex Fridman: UCSHZKyawb77ixDdsGog4iWA)
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  channels_listVideos channelId="UCSHZKyawb77ixDdsGog4iWA" maxResults:1
```

返回最新视频的标题、ID和发布日期。

### 2. 获取研究用字幕

```bash
# Step 1: Get video ID from search or channel listing
# Step 2: Try MCP transcript first
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  transcripts_getTranscript videoId="VIDEO_ID"

# Step 3: If empty, fallback to yt-dlp
yt-dlp --skip-download --write-auto-sub --sub-lang en \
  --output "/tmp/%(id)s.%(ext)s" \
  "https://youtube.com/watch?v=VIDEO_ID"

cat /tmp/VIDEO_ID.en.vtt
```

### 3. 搜索主题

```bash
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  search_videos query="Laravel AI productivity 2025" maxResults:10
```

筛选相关频道或日期的结果。

## 频道ID参考

将常用频道信息保存在此处以便快速访问：

- **Lex Fridman Podcast：**`UCSHZKyawb77ixDdsGog4iWA`
- **Indie Hackers：**（根据需要添加）
- **Laravel：**（根据需要添加）

获取频道ID的方法：
1. 访问频道页面
2. 查看页面源代码
3. 搜索`"channelId":`或`"externalId"`
   或通过搜索并从结果中提取。

## API配额限制

YouTube Data API v3有每日配额限制：
- 默认：每天10,000次请求
- 搜索：每次请求100次
- 视频详情：每次请求1次
- 字幕：0次（使用单独的配额机制）

**提示：**可以自由使用字幕功能（无配额限制），但搜索请求请谨慎使用。

## 故障排除

### MCP服务器无法使用

**症状：**出现“Connection closed”或“需要设置YOUTUBE_API_KEY环境变量”

**解决方法：**从源代码编译MCP服务器：
```bash
cd /tmp
git clone https://github.com/ZubeidHendricks/youtube-mcp-server
cd youtube-mcp-server
npm install
npm run build

# Test
YOUTUBE_API_KEY="your_key" node dist/cli.js
```

### 字幕为空

**症状：**虽然返回了字幕文件，但内容为空

**原因：**视频可能没有字幕，或者MCP无法获取字幕

**解决方法：**使用`yt-dlp`作为备用方案（见上文）。

### 无法找到yt-dlp

```bash
pip install --user yt-dlp
# or
pipx install yt-dlp
```

## 安全注意事项

使用此MCP服务器时，YouTube API密钥是安全的：
- ✅ 密钥仅用于与官方YouTube Data API进行身份验证
- ✅ 不涉及任何第三方服务器
- ✅ 所有网络请求都发送到`googleapis.com`
- ✅ 代码已过审查（无数据泄露风险）

不过：
- 🔒 将密钥保存在Clawdbot配置文件中（不要放在代码或脚本中）
- 🔒 仅将密钥用于YouTube Data API v3
- 🔒 不要将密钥提交到Git仓库

## 示例

### 为LinkedIn文章寻找相关播客内容

```bash
# 1. Find latest Lex Fridman episode
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  channels_listVideos channelId="UCSHZKyawb77ixDdsGog4iWA" maxResults:1

# 2. Get video details
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  videos_details videoId="Z-FRe5AKmCU"

# 3. Get transcript
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  transcripts_getTranscript videoId="Z-FRe5AKmCU"

# If transcript empty, use yt-dlp
yt-dlp --skip-download --write-auto-sub --sub-lang en \
  --output "/tmp/%(id)s.%(ext)s" \
  "https://youtube.com/watch?v=Z-FRe5AKmCU"

# 4. Analyze transcript for interesting topics
# (read /tmp/Z-FRe5AKmCU.en.vtt and extract key themes)
```

### 查找关于热门话题的视频

```bash
# Search for recent videos
mcporter call --stdio "node /tmp/youtube-mcp-server/dist/cli.js" \
  search_videos query="ClawdBot security concerns" maxResults:10

# Pick relevant ones, get transcripts
# Analyze sentiment and technical claims
```

## 注意事项

- MCP服务器路径：`/tmp/youtube-mcp-server/dist/cli.js`
- 始终通过环境变量传递API密钥：`YOUTUBE_API_KEY="key" node ...`
- 或在shell/Clawdbot配置文件中全局设置
- 字幕可能是自动生成的（请核对引用的准确性）
- 如果需要，`yt-dlp`也可以下载音频（使用`--extract-audio --audio-format mp3`选项）