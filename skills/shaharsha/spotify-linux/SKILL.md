---
name: spogo-linux
description: 适用于无头 Linux 服务器的 Spotify CLI（命令行工具）。通过终端使用 cookie 认证来控制 Spotify 播放（无需 OAuth 回调），非常适合无法访问本地主机的远程服务器。
homepage: https://github.com/steipete/spogo
metadata: {"openclaw":{"emoji":"🎵","requires":{"anyBins":["spogo"]},"install":[{"id":"go","kind":"shell","command":"go install github.com/steipete/spogo/cmd/spogo@latest","bins":["spogo"],"label":"Install spogo (go)"}]}}
---

# Spogo – 适用于 Linux 服务器的 Spotify 命令行工具

通过基于 Cookie 的身份验证机制，您可以在无界面的 Linux 服务器上控制 Spotify。无需 OAuth 回调，非常适合远程服务器使用。

## 为什么需要这个工具？

ClawHub 上的 `steipete` 开发的原始 `spotify-player` 工具依赖于本地浏览器来导入 Cookie（使用命令 `spogo auth import --browser chrome`）。在没有本地浏览器的无界面 Linux 服务器上，这个方法无法使用。

本工具提供了基于 Cookie 的解决方案：只需复制两个浏览器 Cookie 即可。无需 OAuth，也无需访问本地主机。

## 使用要求
- 拥有 Spotify Premium 账户
- 安装了 Go 1.21 或更高版本
- 用户的 Spotify 浏览器 Cookie

## 安装（Linux）

### 1. 安装 Go（如果尚未安装）

```bash
# Ubuntu/Debian
sudo apt update && sudo apt install -y golang-go

# Or download latest from https://go.dev/dl/
wget https://go.dev/dl/go1.23.4.linux-amd64.tar.gz
sudo tar -C /usr/local -xzf go1.23.4.linux-amd64.tar.gz
echo 'export PATH=$PATH:/usr/local/go/bin:~/go/bin' >> ~/.bashrc
source ~/.bashrc
```

### 2. 安装 spogo

```bash
go install github.com/steipete/spogo/cmd/spogo@latest
```

安装完成后，程序会保存在 `~/go/bin/spogo` 目录下。如有需要，请将其添加到系统的 PATH 环境变量中：
```bash
sudo ln -s ~/go/bin/spogo /usr/local/bin/spogo
```

### 3. 验证安装是否成功

```bash
spogo --version
# spogo v0.2.0
```

## 设置（基于 Cookie 的身份验证）

由于 OAuth 需要访问本地主机（在远程服务器上无法实现），因此我们改用基于 Cookie 的身份验证方式。

### 1. 从浏览器中获取 Cookie

让用户打开浏览器的开发者工具（DevTools），选择“应用程序”（Application）→“Cookies”，然后找到 `open.spotify.com` 的 Cookie：
- `sp_dc`：主要认证令牌（长字符串，必需）
- `sp_t`：设备 ID（UUID 格式，用于播放）

### 2. 创建配置文件

创建 `~/.config/spogo/config.toml` 文件：
```toml
default_profile = "default"

[profile.default]
cookie_path = "/root/.config/spogo/cookies/default.json"
market = "IL"
language = "en"
```

### 3. 创建 Cookie 文件

创建 `~/.config/spogo/cookies/default.json` 文件：
```json
[
  {
    "name": "sp_dc",
    "value": "USER_SP_DC_VALUE",
    "domain": ".spotify.com",
    "path": "/",
    "expires": "2027-01-01T00:00:00Z",
    "secure": true,
    "http_only": true
  },
  {
    "name": "sp_t",
    "value": "USER_SP_T_VALUE",
    "domain": ".spotify.com",
    "path": "/",
    "expires": "2027-01-01T00:00:00Z",
    "secure": false,
    "http_only": false
  }
]
```

### 4. 验证配置是否正确

```bash
spogo auth status
# → "Cookies: 2 (file)"
```

## 可用的命令

```bash
# Search
spogo search track "query"
spogo search track "query" --json --limit 5

# Play
spogo play spotify:track:ID
spogo play                    # Resume
spogo pause
spogo next / spogo prev

# Devices
spogo device list --json
spogo device set "DEVICE_ID"

# Status
spogo status
spogo status --json
```

## 错误提示：“缺少设备 ID”

- 如果出现“缺少设备 ID”的错误，可能是由于没有活跃的 Spotify 会话导致的。请尝试以下方法：
1. **在浏览器中打开目标歌曲**：
```
browser open https://open.spotify.com/track/TRACK_ID profile=openclaw
```

2. 通过浏览器自动化功能点击“播放”按钮。
3. 将歌曲传输到目标设备上：
```bash
spogo device set "DEVICE_ID"
```

此时，浏览器会保持登录状态（Cookie 会持续有效），并且会话会在播放后数小时内保持活跃。

## 速率限制
- 使用 Connect API 时：没有速率限制（✓）
- 使用 Web API 时（`--engine web`）：存在速率限制（可能会收到 429 错误）
- 如果遇到速率限制，建议使用浏览器自动化功能来访问相关资源。

## 故障排除
- **“缺少设备 ID”**：可能是由于没有活跃的 Spotify 会话。请先通过浏览器启动播放。
- **“401 Unauthorized”**：可能是 Cookie 已过期。请从浏览器中获取新的 Cookie 并更新 `cookies/default.json` 文件。
- **命令可以执行但无法播放声音**：检查 `spogo device list` 命令的输出，确认歌曲是否正在正确的设备上播放。如果需要切换设备，可以使用 `spogo device set "DEVICE_ID"` 命令。

## 注意事项
- **Cookie 的有效期**：大约为 1 年，但如果用户登出或更改密码，Cookie 可能会失效。
- **需要 Premium 账户**：免费账户无法使用 Connect API。
- **地区设置**：请在 `config.toml` 文件中设置 `market` 参数，以选择正确的地区（如 Italy、US 等）。