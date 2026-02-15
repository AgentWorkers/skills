---
name: apple-music
description: 搜索 Apple Music、将歌曲添加到音乐库中、管理播放列表、控制播放以及使用 AirPlay 功能。
metadata: {"clawdbot":{"emoji":"🎵","os":["darwin"],"requires":{"bins":["node","curl"]}}}
---

# Apple Music

您可以通过 MusicKit API 和 AppleScript 来控制 Apple Music。路径：`~/.clawdbot/skills/apple-music/`

## 本地使用（无需额外设置）

**播放功能：**  
`./apple-music.sh player [now|play|pause|toggle|next|prev|shuffle|repeat|volume N|song "name"]`  
**AirPlay 功能：**  
`./apple-music.sh airplay [list|select N|add N|remove N]`

## API 使用（需要设置）

需要注册 Apple 开发者账户（每年费用 99 美元）并获取 MusicKit 密钥。

### 设置步骤：

1. 访问 developer.apple.com → “Keys”（密钥管理）→ 创建 MusicKit 密钥 → 下载 `.p8` 文件。
2. 记下您的密钥 ID 和团队 ID。

**然后运行设置脚本：**
```bash
./launch-setup.sh  # Opens Terminal for interactive setup
```

设置脚本会打开 Terminal.app 并执行相应的设置操作。请输入 `.p8` 文件的路径、密钥 ID 和团队 ID，然后在浏览器中完成授权并粘贴生成的令牌。

**⚠️ 注意：**  
始终使用 `./launch-setup.sh` 来启动 Terminal；不要通过聊天界面运行 `setup.sh`（该脚本需要用户交互式输入）。

### 命令列表：

- `search "query" [--type songs|albums|artists] [--limit N]`  
- `library add <song-id>`  
- `playlists [list|create "Name"|add <playlist-id> <song-id>]`

### 配置文件

`config.json` 用于存储令牌（有效期约为 6 个月）。如果授权失败，请重新运行 `./setup.sh`。

### 常见错误信息：

- 401：令牌过期，请重新设置。  
- 403：请检查您的 Apple Music 订阅状态。  
- 404：提供的 ID 无效或受地区限制。

### 设置时可能遇到的问题：

- **授权页面显示 404 错误：** 设置脚本会自动尝试通过 HTTP 服务器进行验证。  
- **浏览器无法打开设置页面：** 请手动打开生成的 URL（推荐使用 Chrome 浏览器）。