---
name: jellyfin-control
description: 控制Jellyfin媒体服务器和电视：可以搜索内容、恢复播放、管理会话、控制电视的电源状态以及应用程序。支持与Home Assistant和WebOS后端直接集成。只需一条命令即可开启电视、启动Jellyfin并开始播放内容。
metadata: {"version": "1.3.0", "author": "Titunito", "openclaw": {"emoji": "🎬", "requires": {"env": ["JF_URL", "JF_API_KEY"]}, "optionalEnv": ["JF_USER", "JF_PASS", "JF_USER_ID", "TV_BACKEND", "TV_PLATFORM", "HA_URL", "HA_TOKEN", "HA_TV_ENTITY", "TV_IP", "TV_MAC", "TV_CLIENT_KEY", "ADB_DEVICE", "TV_JELLYFIN_APP", "TV_BOOT_DELAY", "TV_APP_DELAY"], "tags": ["media", "streaming", "tv", "smart-home", "jellyfin", "webos", "androidtv", "home-assistant"]}}
---
# Jellyfin 控制

这是一个强大的技能，可以通过命令行界面（CLI）来控制 Jellyfin 的播放功能以及电视的开关。

## 特点

- **🎯 一键播放：** `tv play "Breaking Bad"` — 打开电视，启动 Jellyfin，找到下一集并开始播放。
- **智能续播：** 自动找到系列剧的下一集未播放的部分并继续播放。
- **续播位置：** 从上次暂停的位置继续播放电影或剧集（LG WebOS/Tizen 设备支持使用“Seek”功能）。
- **设备检测：** 自动识别可控制的设备（电视、手机、网页设备）。
- **远程控制：** 提供完整的播放控制功能（播放、暂停、停止、下一集、上一集、音量调节、静音）。
- **电视开关与应用程序：** 可以开关电视并启动应用程序（无论是否使用 Home Assistant）。
- **两种电视后端支持：** 可以与 Home Assistant 集成，也可以直接通过 WebOS 控制（LG 电视，无需 Home Assistant）。
- **支持 Android TV：** 支持通过 ADB 直接控制 Chromecast（带 Google TV 功能的设备）、Nvidia Shield、Fire TV、Mi Box 等设备（无需 Home Assistant）。
- **三种连接方式：** 可以通过 Home Assistant（适用于任何电视）、直接通过 WebOS 或直接通过 ADB（适用于 Android TV/Fire TV）。

## 快速入门

### 最小化设置（仅使用 Jellyfin，不控制电视）

```json
{
  "skills": {
    "entries": {
      "jellyfin-control": {
        "env": {
          "JF_URL": "http://YOUR_IP:8096",
          "JF_API_KEY": "your-api-key-here",
          "JF_USER": "your-username"
        }
      }
    }
  }
}
```

### 使用 Home Assistant（推荐用于电视控制）

```json
{
  "skills": {
    "entries": {
      "jellyfin-control": {
        "env": {
          "JF_URL": "http://192.168.1.50:8096",
          "JF_API_KEY": "your-jellyfin-api-key",
          "JF_USER": "victor",
          "HA_URL": "http://192.168.1.138:8123",
          "HA_TOKEN": "your-ha-long-lived-token",
          "HA_TV_ENTITY": "media_player.lg_webos_tv_oled48c34la",
          "TV_MAC": "AA:BB:CC:DD:EE:FF"
        }
      }
    }
  }
}
```

### 直接通过 WebOS 控制（LG 电视，无需 Home Assistant）

```json
{
  "skills": {
    "entries": {
      "jellyfin-control": {
        "env": {
          "JF_URL": "http://192.168.1.50:8096",
          "JF_API_KEY": "your-jellyfin-api-key",
          "JF_USER": "victor",
          "TV_IP": "192.168.1.100",
          "TV_MAC": "AA:BB:CC:DD:EE:FF"
        }
      }
    }
  }
}
```

> **首次使用直接 WebOS 控制时：** 电视会显示配对提示。接受提示并保存技能输出的 `TV_CLIENT_KEY`，下次连接时可以直接使用该密钥以避免提示。

### 直接通过 ADB 控制（Android TV / Fire TV / 带 Google TV 的 Chromecast，无需 Home Assistant）

```json
{
  "skills": {
    "entries": {
      "jellyfin-control": {
        "env": {
          "JF_URL": "http://192.168.1.50:8096",
          "JF_API_KEY": "your-jellyfin-api-key",
          "JF_USER": "victor",
          "ADB_DEVICE": "192.168.1.100:5555",
          "TV_MAC": "AA:BB:CC:DD:EE:FF"
        }
      }
    }
  }
}
```

> **首次使用 ADB 控制时：** 在电视上启用开发者选项（设置 → 关于 → 連续点击“Build Number”7次），然后启用网络/USB 调试功能。首次连接时电视会显示“允许调试？”提示——请接受。需要在 OpenClaw 主机上安装 `adb`（使用 `sudo apt install adb` 安装）。

## 环境变量

### Jellyfin 必需的环境变量

| 变量          | 是否必需 | 说明                                                                                          |
|---------------|--------|-----------------------------------------------------------------------------|
| `JF_URL`       | 是       | Jellyfin 服务器的基址，例如 `http://192.168.1.50:8096`                                                                                     |
| `JF_API_KEY`     | 是       | 来自 Jellyfin 控制台的 API 密钥                                                                                         |
| `JF_USER`       | 否       | 用于解析用户 ID 的用户名                                                                                         |
| `JF_USER_ID`     | 否       | 直接使用的用户 ID，避免需要调用 `/Users`                                                                                   |
| `JF_PASS`       | 否       | 仅在通过用户会话进行身份验证时需要                                                                                         |

### 电视控制相关环境变量（可选，根据需要选择后端）

| 变量            | 后端        | 说明                                                                                          |
|------------------|-----------|-------------------------------------------------------------------------------------------------------------------------|
| `TV_BACKEND`     | 所有       | 强制指定后端：`homeassistant`、`webos`、`androidtv` 或 `auto`                                                                                   |
| `TVPLATFORM`     | Home Assistant | 强制指定平台：`webos` 或 `androidtv`（自动检测）                                                                                   |
| `HA_URL`        | Home Assistant | Home Assistant 的 URL，例如 `http://192.168.1.138:8123`                                                                                   |
| `HA_TOKEN`       | Home Assistant | Home Assistant 的长期访问令牌                                                                                         |
| `HA_TV Entity`    | Home Assistant | 电视的实体 ID，例如 `media_player.lg_webos_tv_oled48c34la`                                                                                   |
| `TV_IP`        | WebOS       | 用于直接通过 WebOS 连接的电视 IP 地址                                                                                         |
| `TV_CLIENT_KEY`     | WebOS       | 配对密钥（首次连接时显示——请保存！                                                                                         |
| `ADB_DEVICE`      | AndroidTV    | 用于 ADB 连接的电视地址，例如 `192.168.1.100:5555`                                                                                   |
| `TV_MAC`       | 所有       | 用于通过无线网络唤醒电视的电视 MAC 地址                                                                                         |
| `TV_JELLYFIN_APP`    | 所有       | 可覆盖的 Jellyfin 应用程序 ID（默认为 `org.jellyfin.webos` 或 `org.jellyfin.androidtv`）                                                                 |
| `TV_BOOT_DELAY`     | 所有       | 电视唤醒后等待的秒数（默认：10秒）                                                                                         |
| `TV_APP_DELAY`     | 所有       | 启动 Jellyfin 后等待的秒数（默认：8秒）                                                                                         |

**自动检测：** 如果 `TV_BACKEND` 设置为 `auto`（默认值）：
1. 设置 `HA_URL`、`HA_TOKEN` 和 `HA_TV Entity` → 使用 Home Assistant 后端。
2. 设置 `ADB_DEVICE` → 使用直接 ADB（适用于 Android TV）。
3. 设置 `TV_IP` → 使用直接 WebOS（适用于 LG 电视）。
4. 如果未设置任何值 → 禁用电视控制功能，仅使用 Jellyfin 功能。

## 使用方法

### 🎯 一键播放

通过一个命令即可完成以下操作：打开电视 → 启动 Jellyfin → 查找下一集 → 开始播放。

```bash
node skills/jellyfin-control/cli.js tv play "Breaking Bad"
node skills/jellyfin-control/cli.js tv play "The Matrix"
```

该技能会在打开电视之前验证内容是否存在（如果内容不存在，则会立即失败）。

### 智能续播/播放

如果电视和 Jellyfin 已经在运行中：

```bash
node skills/jellyfin-control/cli.js resume "Breaking Bad"
node skills/jellyfin-control/cli.js resume "Matrix" --device "Chromecast"
```

### 电视控制

```bash
node skills/jellyfin-control/cli.js tv on           # Turn on (Wake-on-LAN)
node skills/jellyfin-control/cli.js tv off          # Turn off
node skills/jellyfin-control/cli.js tv launch       # Launch Jellyfin app
node skills/jellyfin-control/cli.js tv launch com.webos.app.hdmi1  # Launch specific app
node skills/jellyfin-control/cli.js tv apps         # List installed apps
```

### 远程控制

```bash
node skills/jellyfin-control/cli.js control pause
node skills/jellyfin-control/cli.js control play
node skills/jellyfin-control/cli.js control next
node skills/jellyfin-control/cli.js control vol 50
```

### 内容搜索

```bash
node skills/jellyfin-control/cli.js search "Star Wars"
```

### 库统计与扫描

```bash
node skills/jellyfin-control/cli.js stats
node skills/jellyfin-control/cli.js scan            # requires admin API key
```

### 用户历史记录（需要管理员 API 密钥）

```bash
node skills/jellyfin-control/cli.js history
node skills/jellyfin-control/cli.js history jorge --days 7
```

## 选择电视后端

| 功能                | Home Assistant | 直接通过 WebOS | 直接通过 ADB（Android TV） | 无需后端       |
|------------------|------------|------------------|------------------|---------------------------|
| 支持的电视品牌        | 所有（通过 Home Assistant） | 仅支持 LG 电视        | Android TV、Fire TV、CCwGTV | -------------------------|
| 无线网络唤醒（WoL）       | 可       | 可       | 可       | -------------------------|
| 关闭电视           | 可       | 可       | -------------------------|
| 启动应用程序        | 可       | 可       | -------------------------|
| 列出应用程序        | 可       | 可       | 可       | -------------------------|
| 额外依赖项          | 无          | 需安装 `ws`      | 需安装 `adb`      | -------------------------|
| 设置复杂性        | 中等（需要 Home Assistant） | 低（需要电视的 IP 和 MAC 地址） | 低（需要在电视上启用 ADB） | -------------------------|
| Jellyfin 播放功能       | 可       | 可       | 可       | -------------------------|

**推荐：**
- 如果已经安装了 Home Assistant？ → 使用 Home Assistant 后端（功能最丰富，支持任何品牌的电视）。
- 使用 LG WebOS 电视且没有 Home Assistant？ → 使用直接通过 WebOS 的控制方式。
- 使用 Android TV、Fire TV 或带 Google TV 的 Chromecast 且没有 Home Assistant？ → 使用直接通过 ADB 的控制方式。
- 如果不需要智能电视控制功能？ → 可以跳过电视相关的配置设置，如果 Jellyfin 应用程序已经打开，直接使用“续播”功能即可。

## 安全注意事项

- **API 密钥仅存储在 `openclaw.json` 环境变量中** — 绝不要将其保存在工作区文件、`.env` 文件或 markdown 文档中。
- **Home Assistant 的访问令牌** 具有较长的有效期且功能强大。如果可能的话，建议创建一个权限有限的专用 Home Assistant 用户。
- `TV_CLIENT_KEY`（用于 WebOS）非常敏感——它允许完全控制电视。请像对待密码一样保护它。
- **ADB 访问** 可以完全控制您的 Android TV。请确保您的网络是安全的——如果启用了调试功能，任何在同一网络上的设备都可能通过 ADB 进行连接。
- **管理员操作**（如查看历史记录、扫描功能）需要管理员级别的 Jellyfin API 密钥；如果权限不足，操作会失败并显示 403 错误。

## 架构

- `lib/jellyfin.js` — 负责处理 Jellyfin 的 REST API（身份验证、搜索、会话管理、播放控制功能）。
- `lib/tv.js` — 提供电视控制的抽象层（支持 Home Assistant 后端、WebOS 后端以及无线网络唤醒功能）。
- `cli.js` — 提供用户友好的命令行界面，包含所有可用的命令。

## 工作流程：例如，当用户通过命令行请求“在电视上播放《星际迷航》”时：

```
Agent → cli.js tv play "Star Trek"
         │
         ├── 1. Search Jellyfin for "Star Trek" (fail fast)
         ├── 2. Find next unplayed episode
         ├── 3. Wake-on-LAN → TV turns on
         ├── 4. Wait 10s for boot
         ├── 5. Launch Jellyfin app (HA or WebOS)
         ├── 6. Wait 8s for session registration
         ├── 7. Find Jellyfin session (retry 3x)
         └── 8. Play episode on session
```