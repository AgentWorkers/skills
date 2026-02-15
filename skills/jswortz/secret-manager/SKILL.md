---
name: secret-manager
description: 通过 GNOME Keyring 安全地管理 API 密钥，并将其注入 OpenClaw 的配置文件中。
homepage: https://github.com/openclaw/skills
metadata: {"clawdbot":{"emoji":"🔐","requires":{"bins":["secret-tool","systemctl","python3"]},"install":[{"id":"bash","kind":"bash","bin":"secret-manager.sh","label":"Install Secret Manager (bash)"}]}}
---

# Secret Manager

这是一个用于通过系统密钥环（GNOME Keyring / libsecret）安全管理 OpenClaw API 密钥的工具。

该工具提供了一个名为 `secret-manager` 的命令行界面（CLI），具备以下功能：
1. 使用 `secret-tool` 工具安全地存储 API 密钥。
2. 将这些密钥添加到用户的 `auth-profiles.json` 配置文件中。
3. 将密钥信息传播到系统的 `systemd` 用户环境中。
4. 重启用户所在 Distrobox 容器中的 OpenClaw Gateway 服务。

## 安装

请确保已安装以下依赖项：
- **Debian/Ubuntu:** `sudo apt install libsecret-tools`
- **Fedora:** `sudo dnf install libsecret`
- **Arch:** `sudo pacman -S libsecret`

将脚本复制到您的路径中，或直接运行它。

## 配置

该脚本使用适用于大多数 OpenClaw 安装的默认路径，但您也可以通过环境变量来自定义这些路径：

| 变量 | 描述 | 默认值 |
| :--- | :--- | :--- |
| `OPENCLAW_CONTAINER` | Distrobox 容器的名称 | `clawdbot` |
| `OPENCLAW_HOME` | OpenClaw 配置文件的路径 | `~/.openclaw` |
| `SECRETS_ENV_FILE` | 可选的 `.env` 配置文件的路径 | `~/.config/openclaw/secrets.env` |

## 使用方法

**列出所有已配置的密钥：**
```bash
secret-manager list
```

**交互式方式设置密钥：**
```bash
secret-manager OPENAI_API_KEY
# (Paste key when prompted)
```

**直接设置密钥：**
```bash
secret-manager DISCORD_BOT_TOKEN "my-token-value"
```

**支持的密钥类型：**
- `OPENAI_API_KEY`
- `GEMINI_API_KEY`
- `DISCORD_BOT_TOKEN`
- `GATEWAY_AUTH_TOKEN`
- `OLLAMA_API_KEY`
- `GIPHY_API_KEY`
- `GOOGLE_PLACES_API_KEY`
- `LINKEDIN_LI_AT`
- `LINKEDIN_JSESSIONID`