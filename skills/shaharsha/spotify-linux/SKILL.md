---
name: spotify-linux
version: 1.1.0
description: 适用于无头 Linux 服务器的 Spotify CLI（命令行工具）。通过终端使用 Cookie 认证来控制 Spotify 的播放功能（无需 OAuth 回调），非常适合无法访问本地主机的远程服务器。
author: Leo 🦁
homepage: https://github.com/steipete/spogo
metadata: {"openclaw":{"emoji":"🎵","requires":{"anyBins":["spogo"]},"install":[{"id":"go","kind":"shell","command":"go install github.com/steipete/spogo/cmd/spogo@latest","bins":["spogo"],"label":"Install spogo (go)"}],"notes":"Cookies (sp_dc, sp_t) are stored locally in ~/.config/spogo/cookies/ and sent only to Spotify APIs. Browser automation fallback is optional and only used to start a playback session when no active device exists."}}
allowed-tools: [exec]
---

# Spogo – 适用于 Linux 服务器的 Spotify 命令行工具

通过基于 Cookie 的身份验证方式，可以在无界面的 Linux 服务器上控制 Spotify。无需 OAuth 回调，非常适合远程服务器使用。

## 为什么需要这个工具？

`ClawHub` 上的 `steipete` 开发的原始 `spotify-player` 工具依赖于本地浏览器来导入 Cookie（使用命令 `spogo auth import --browser chrome`）。在没有本地浏览器的无界面 Linux 服务器上，这种方法无法使用。

本工具提供了基于 Cookie 的解决方案：只需复制两个浏览器 Cookie 即可。无需 OAuth，也无需使用本地主机。

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

安装完成后，`spogo` 会安装在 `~/go/bin/spogo` 目录下。如有需要，将其添加到系统路径（PATH）中：
```bash
sudo ln -s ~/go/bin/spogo /usr/local/bin/spogo
```

### 3. 验证安装是否成功

```bash
spogo --version
# spogo v0.2.0
```

## 设置（基于 Cookie 的身份验证）

由于 OAuth 需要使用本地主机进行回调（在远程服务器上无法实现），因此我们改用基于 Cookie 的身份验证方式。

### 1. 从浏览器中获取 Cookie

让用户打开浏览器的开发者工具（DevTools），选择“应用程序”（Application）→“Cookie”，然后访问 `open.spotify.com`，并复制以下内容：
- `sp_dc`：主要身份验证令牌（长字符串，必需）
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

## 错误提示：“missing device id” – 使用浏览器进行回退

`spogo` 需要一个有效的 Spotify 会话。如果最近没有设备进行播放操作：

1. **在浏览器中打开歌曲**：
```
browser open https://open.spotify.com/track/TRACK_ID profile=openclaw
```

2. 通过浏览器自动化操作点击“播放”按钮。

3. **将播放切换到目标设备**：
```bash
spogo device set "DEVICE_ID"
```

此时，浏览器会保持登录状态（Cookie 会持续有效），并且会话会在播放结束后几小时内仍然有效。

## 使用限制

- **连接 Spotify API**（默认设置）：无使用限制 ✓
- **Web API (`--engine web`）：存在使用限制（可能会收到 429 错误）
- 如果遇到使用限制，可以通过浏览器自动化操作来访问相关功能。

## 故障排除

### 错误提示：“missing device id”
表示当前没有有效的 Spotify 会话。请先使用浏览器进行播放操作。

### 错误提示：“401 Unauthorized”
Cookie 已过期。请从浏览器中获取新的 Cookie 并更新 `cookies/default.json` 文件。

### 命令执行成功但无声音输出
检查 `spogo device list` 命令的输出，确认播放是否在正确的设备上进行。如果需要切换设备，可以使用 `spogo device set "DEVICE_ID"` 命令。

## 安全性与隐私保护

- **Cookie 处理**：`sp_dc` 和 `sp_t` 会存储在 `~/.config/spogo/cookies/` 目录中，应将其视为机密信息，切勿泄露或共享。
- **网络访问**：`spogo` 仅与 Spotify 的官方 API（`api.spotify.com`、`open.spotify.com`）进行通信。
- **浏览器回退机制**：仅在没有活跃的 Spotify 设备时使用。该机制会使用代理服务器的浏览器会话来打开 `open.spotify.com` 并点击“播放”按钮，不会额外获取其他浏览器数据或访问其他浏览器状态。
- **安装来源**：请从官方 [steipete/spogo](https://github.com/steipete/spogo) GitHub 仓库中使用 `go install` 命令进行安装。该工具为开源项目，代码可审计。

## 注意事项

- **Cookie 有效期**：大约为 1 年，但如果用户登出或更改密码，Cookie 可能会失效。
- **需要 Premium 账户**：免费账户无法使用连接 Spotify API 的功能。
- **地区设置**：可以通过修改 `config.toml` 文件中的 `market` 参数来选择正确的地区（例如意大利、美国等）。