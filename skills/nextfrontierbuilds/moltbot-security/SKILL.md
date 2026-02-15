---
name: moltbot-security
description: AI代理的安全加固措施——适用于Moltbot、OpenClaw、Cursor、Claude等工具。需要锁定网关、修正权限设置、加强身份验证机制，并配置防火墙。这些措施对于确保系统的安全性至关重要，尤其是在使用vibe-coding技术进行开发时。
version: 1.0.3
author: NextFrontierBuilds
keywords: [moltbot, openclaw, security, hardening, gateway, firewall, tailscale, ssh, authentication, ai-agent, ai-coding, claude, cursor, copilot, github-copilot, chatgpt, devops, infosec, vibe-coding, ai-tools, developer-tools, devtools, typescript, automation, llm]
---

# Moltbot 安全指南

您的 Moltbot 网关最初是为本地使用而设计的。如果未采取适当的安全措施就直接暴露在互联网上，攻击者将能够访问您的 API 密钥、私密消息以及系统的全部访问权限。

**依据：** 实际的安全漏洞研究显示，在 Shodan 上发现了超过 1,673 个暴露在外的 OpenClaw/Moltbot 网关。

---

## 简而言之：五大关键安全措施

1. **仅绑定到 loopback 接口** — 绝不要将网关暴露在公共互联网上。
2. **设置身份验证令牌** — 要求所有请求都进行身份验证。
3. **修复文件权限** — 只有您自己才能读取配置文件。
4. **更新 Node.js** — 使用版本 v22.12.0 或更高版本以避免已知的安全漏洞。
5. **使用 Tailscale** — 在不暴露于公共网络的情况下实现安全远程访问。

---

## 暴露的风险

当您的网关可以被公开访问时，以下信息可能会被泄露：
- 完整的聊天记录（来自 Telegram、WhatsApp、Signal、iMessage 等）；
- Claude、OpenAI 及其他服务提供商的 API 密钥；
- OAuth 令牌和机器人凭证；
- 对主机机器的完全 shell 访问权限。

**示例：** 攻击者会发送一封包含隐藏指令的电子邮件。您的 AI 系统会读取这封邮件，提取您的最近通信记录，并将其摘要转发给攻击者。无需任何黑客技术即可实现这一操作。

---

## 快速安全审计

运行以下命令来检查您当前的安全配置：

```bash
openclaw security audit --deep
```

自动修复问题：

```bash
openclaw security audit --deep --fix
```

---

## 第一步：仅将网关绑定到 loopback 接口

这样做可以防止网关接受来自其他机器的连接。

检查您的 `~/.openclaw/openclaw.json` 配置文件：

```json
{
  "gateway": {
    "bind": "loopback"
  }
}
```

**选项：**
- `loopback` — 仅允许本地主机（localhost）访问（最安全）；
- `lan` — 仅允许局域网内的设备访问；
- `auto` — 绑定到所有网络接口（如果暴露在外则非常危险）。

---

## 第二步：设置身份验证

**选项 A：令牌认证（推荐）**

生成一个安全的令牌：

```bash
openssl rand -hex 32
```

将其添加到配置文件中：

```json
{
  "gateway": {
    "auth": {
      "mode": "token",
      "token": "your-64-char-hex-token-here"
    }
  }
}
```

或者通过环境变量设置令牌：

```bash
export CLAWDBOT_GATEWAY_TOKEN="your-secure-random-token-here"
```

## 第三步：锁定文件权限

这样做可以确保只有您自己能够读取敏感的配置文件。

```bash
chmod 700 ~/.openclaw
chmod 600 ~/.openclaw/openclaw.json
chmod 700 ~/.openclaw/credentials
```

**权限说明：**
- `700`：仅文件所有者可以访问该文件夹；
- `600`：仅文件所有者可以读取和修改该文件。

或者让 OpenClaw 自动设置权限：

```bash
openclaw security audit --fix
```

---

## 第四步：禁用网络广播

这样做可以防止 OpenClaw 通过 mDNS/Bonjour 发布自身的存在信息。

在您的 shell 配置文件（`~/.zshrc` 或 `~/.bashrc`）中添加以下内容：

```bash
export CLAWDBOT_DISABLE_BONJOUR=1
```

然后重新加载配置文件：

```bash
source ~/.zshrc
```

---

## 第五步：更新 Node.js

旧版本的 Node.js 存在安全漏洞。请确保使用版本 v22.12.0 或更高版本。

检查您的 Node.js 版本：

```bash
node --version
```

**Mac（使用 Homebrew）：**
```bash
brew update && brew upgrade node
```

**Ubuntu/Debian：**
```bash
curl -fsSL https://deb.nodesource.com/setup_22.x | sudo -E bash -
sudo apt-get install -y nodejs
```

**Windows：** 从 [nodejs.org](https://nodejs.org/) 下载最新版本。

---

## 第六步：设置 Tailscale（实现远程访问）

这样做可以在您的设备之间创建加密隧道，从而实现安全远程访问。

**安装 Tailscale：**

```bash
# Linux
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Mac
brew install tailscale
```

**配置 OpenClaw 以使用 Tailscale：**

```json
{
  "gateway": {
    "bind": "loopback",
    "tailscale": {
      "mode": "serve"
    }
  }
}
```

之后，您只能通过 Tailscale 网络来访问 OpenClaw 了。

---

## 第七步：防火墙设置（UFW）

**对于云服务器（如 AWS、DigitalOcean、Hetzner 等）**

**安装 UFW：**
```bash
sudo apt update && sudo apt install ufw -y
```

**设置默认规则：**
```bash
sudo ufw default deny incoming
sudo ufw default allow outgoing
```

**允许 SSH 连接（务必执行此步骤！）：**
```bash
sudo ufw allow ssh
```

**如果使用 Tailscale，请允许 Tailscale 的连接：**
```bash
sudo ufw allow in on tailscale0
```

**启用防火墙规则：**
```bash
sudo ufw enable
```

**验证防火墙设置：**
```bash
sudo ufw status verbose
```

⚠️ **严禁执行以下操作：**
```bash
# DON'T - exposes your gateway publicly
sudo ufw allow 18789
```

---

## 第八步：加强 SSH 安全性

**禁用密码认证（使用 SSH 密钥）：**

```bash
sudo nano /etc/ssh/sshd_config
```

修改相关配置文件：
```
PasswordAuthentication no
PermitRootLogin no
```

重启系统：
```bash
sudo systemctl restart sshd
```

---

## 安全检查清单

在部署之前，请确保满足以下条件：
- 网关已绑定到 loopback 或 lan 接口；
- 设置了身份验证令牌或密码；
- 文件权限已设置为 600/700；
- mDNS/Bonjour 功能已禁用；
- 使用了 Node.js v22.12.0 或更高版本；
- Tailscale 已正确配置（如果需要远程访问）；
- 防火墙已阻止端口 18789 的访问；
- SSH 密码认证已被禁用。

---

## 安全配置模板（推荐设置）

```json
{
  "gateway": {
    "port": 18789,
    "bind": "loopback",
    "auth": {
      "mode": "token",
      "token": "YOUR_64_CHAR_HEX_TOKEN"
    },
    "tailscale": {
      "mode": "serve"
    }
  }
}
```

---

## 致谢

本指南基于 [@NickSpisak_](https://x.com/NickSpisak_) 的安全研究结果。他在 Shodan 上发现了超过 1,673 个暴露在外的 OpenClaw/Moltbot 网关。  
原文链接：https://x.com/nickspisak_/status/2016195582180700592

---

## 安装指南

```bash
clawdhub install NextFrontierBuilds/moltbot, openclaw-security
```

本指南由 [@NextXFrontier](https://x.com/NextXFrontier) 编写。