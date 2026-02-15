---
name: yt-api-cli
description: 通过命令行管理您的 YouTube 账户。这是一个完整的 YouTube Data API v3 命令行接口（CLI）实现，支持视频列表/搜索、上传、播放列表管理等功能。
metadata: {"clawdbot":{"emoji":"▶️","os":["darwin","linux"],"requires":{"env":["YT_API_AUTH_TYPE", "YT_API_CLIENT_ID", "YT_API_CLIENT_SECRET"]}}}
---

# yt-api-cli

这是一个用于通过终端管理您的YouTube账户的命令行工具，它是YouTube Data API v3的完整命令行接口（CLI）。

## 安装

```bash
# Using go install
go install github.com/nerveband/youtube-api-cli/cmd/yt-api@latest

# Or download from releases
curl -L -o yt-api https://github.com/nerveband/youtube-api-cli/releases/latest/download/yt-api-darwin-arm64
chmod +x yt-api
sudo mv yt-api /usr/local/bin/
```

## 设置

### 1. Google Cloud Console 设置

1. 访问 [Google Cloud Console](https://console.cloud.google.com)
2. 创建/启用YouTube Data API v3
3. 创建OAuth 2.0凭据（适用于桌面应用程序）
4. 下载客户端配置文件

### 2. 配置 yt-api

```bash
mkdir -p ~/.yt-api
cat > ~/.yt-api/config.yaml << EOF
default_auth: oauth
default_output: json
oauth:
  client_id: "YOUR_CLIENT_ID"
  client_secret: "YOUR_CLIENT_SECRET"
EOF
```

### 3. 验证身份

```bash
yt-api auth login  # Opens browser for Google login
yt-api auth status # Check auth state
```

## 命令

### 列出操作

```bash
# List your videos
yt-api list videos --mine

# List channel videos
yt-api list videos --channel-id UC_x5XG1OV2P6uZZ5FSM9Ttw

# List playlists
yt-api list playlists --mine

# List subscriptions
yt-api list subscriptions --mine
```

### 搜索

```bash
# Basic search
yt-api search --query "golang tutorial"

# With filters
yt-api search --query "music" --type video --duration medium --order viewCount
```

### 上传操作

```bash
# Upload video
yt-api upload video ./video.mp4 \
  --title "My Video" \
  --description "Description here" \
  --tags "tag1,tag2" \
  --privacy public

# Upload thumbnail
yt-api upload thumbnail ./thumb.jpg --video-id VIDEO_ID
```

### 播放列表管理

```bash
# Create playlist
yt-api insert playlist --title "My Playlist" --privacy private

# Add video to playlist
yt-api insert playlist-item --playlist-id PLxxx --video-id VIDxxx
```

### 频道操作

```bash
# Get channel info
yt-api list channels --id UCxxx --part snippet,statistics

# Update channel description
yt-api update channel --id UCxxx --description "New description"
```

## 输出格式

```bash
# JSON (default - LLM-friendly)
yt-api list videos --mine

# Table (human-readable)
yt-api list videos --mine -o table

# YAML
yt-api list videos --mine -o yaml

# CSV
yt-api list videos --mine -o csv > videos.csv
```

## 全局参数

| 参数 | 缩写 | 说明 |
|------|-------|-------------|
| `--output` | `-o` | 输出格式：json（默认），yaml，csv，table |
| `--quiet` | `-q` | 忽略stderr信息 |
| `--config` | | 配置文件路径 |
| `--auth-type` | | 认证方式：oauth（默认），service-account |

## 环境变量

| 变量 | 说明 |
|----------|-------------|
| `YT_API_AUTH_TYPE` | 认证方式：oauth或service-account |
| `YT_API_OUTPUT` | 默认输出格式 |
| `YT_API_CLIENT_ID` | OAuth客户端ID |
| `YT_API_CLIENT_SECRET` | OAuth客户端密钥 |
| `YT_API_CREDENTIALS` | 服务账户JSON文件的路径 |

## 认证方式

### OAuth 2.0（默认）
最适合交互式使用和访问您的个人YouTube账户。

```bash
yt-api auth login  # Opens browser
```

### 服务账户
最适合服务器端自动化操作。

```bash
yt-api --auth-type service-account --credentials ./key.json list videos
```

## 快速诊断命令

```bash
yt-api info                      # Full system state
yt-api info --test-connectivity  # Verify API access
yt-api info --test-permissions   # Check credential capabilities
yt-api auth status               # Authentication details
yt-api version                   # Version info
```

## 错误处理

退出代码：
- `0` - 成功
- `1` - 一般错误
- `2` - 认证错误
- `3` - API错误（配额、权限问题）
- `4` - 输入错误

## 适用于大型语言模型（LLMs）和自动化脚本

- 默认输出格式为JSON
- 错误信息以JSON对象的形式呈现
- 可使用`--quiet`模式进行解析
- `--dry-run`模式用于验证操作而不执行实际操作
- 支持通过标准输入（stdin）传递数据

## 注意事项

- 需要有效的Google Cloud凭据，并且已启用YouTube Data API v3
- OAuth令牌存储在`~/.yt-api/tokens.json`文件中（权限设置为0600）
- 默认输出格式为JSON（优化了大型语言模型的处理）
- 支持YouTube Data API v3的所有资源

## 来源

GitHub: https://github.com/nerveband/youtube-api-cli