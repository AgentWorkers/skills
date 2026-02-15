# Spotify CLI

这是一个简单的命令行接口，用于通过 Raspberry Pi（或任何 Linux 系统）控制 Spotify 的播放功能。

## 所需条件

- Python 3
- Spotify Premium 账户
- `spotipy` Python 库
- 在另一台设备（手机、电脑或网页播放器）上打开 Spotify 应用

## 安装

### 1. 安装依赖项

```bash
pip3 install spotipy --break-system-packages
```

### 2. 创建 Spotify 开发者应用

1. 访问 https://developer.spotify.com/dashboard
2. 登录并点击“创建应用”
3. 将重定向 URI 设置为 `http://127.0.0.1:8888/callback`
4. 复制 **客户端 ID** 和 **客户端密钥**

### 3. 创建配置文件

```bash
mkdir -p ~/.config/spotify-cli
cat << EOF > ~/.config/spotify-cli/config
SPOTIPY_CLIENT_ID=your_client_id
SPOTIPY_CLIENT_SECRET=your_client_secret
SPOTIPY_REDIRECT_URI=http://127.0.0.1:8888/callback
EOF
```

脚本会自动从 `~/.config/spotify-cli/config` 文件中加载凭证。

### 4. 安装脚本

```bash
sudo cp spotify /usr/local/bin/spotify
sudo chmod +x /usr/local/bin/spotify
```

### 5. 进行身份验证

运行任何命令（例如 `spotify status`）。首次运行时，系统会提供一个需要在浏览器中打开的 URL。授权后，按照提示复制该重定向 URL 并粘贴即可。

## 命令

| 命令 | 描述 |
|---------|-------------|
| `spotify search <查询>` | 搜索歌曲（显示前 5 个结果） |
| `spotify play <歌曲名>` | 搜索并播放指定的歌曲 |
| `spotify pause` | 暂停播放 |
| `spotify resume` | 恢复播放 |
| `spotify next` | 跳到下一首歌 |
| `spotify prev` | 返回上一首歌 |
| `spotify status` | 显示当前正在播放的歌曲 |
| `spotify devices` | 列出可用的 Spotify 设备 |

## 示例

```bash
# Search for a song
spotify search "stairway to heaven"

# Play a song (tip: include artist for better results)
spotify play "stairway to heaven led zeppelin"

# Check what's playing
spotify status

# Control playback
spotify pause
spotify resume
spotify next
```

## 最佳实践（针对 AI 代理）

在代表用户使用此工具时，请遵循以下规则：

1. **先搜索再播放**：使用 `spotify search <查询>` 查看搜索结果。
2. **确认匹配结果**：与用户确认搜索结果是否符合他们的需求。
3. **再开始播放**：确认无误后，使用 `spotify play <歌曲名艺术家>` 命令播放搜索结果中的正确歌曲。

这样可以避免因 Spotify 的模糊搜索功能而播放错误的歌曲。

**示例工作流程：**
```bash
# User asks: "play voice actor u projected 2"

# Step 1: Search first
spotify search "voice actor u projected 2"
# Results show: "U Projected 2 - Voice Actor, Yarrow.co"

# Step 2: Confirm with user that this is the right song

# Step 3: Play with exact match
spotify play "U Projected 2 Voice Actor"
```

## 注意事项

- 该 CLI 需要在现有的 Spotify 会话中进行控制。请确保在另一台设备上（手机、电脑或 https://open.spotify.com）打开 Spotify。
- CLI 向该设备发送播放指令，音频将在该设备上播放，而非 Raspberry Pi 上。
- 控制播放功能需要 Spotify Premium 账户。

## 故障排除

### “未找到活跃设备”
在您的手机或电脑上打开 Spotify 并播放一首歌曲，然后重新尝试。

### “未找到设备”
确保至少有一台设备上打开了 Spotify 并且使用了相同的账号登录。

### 认证令牌过期
删除 `~/.cache-*` 文件并重新进行身份验证。