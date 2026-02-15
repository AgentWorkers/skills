---
name: clawdbot-security
description: Clawdbot/Moltbot 的安全审计与加固措施：检测暴露的网关、修复权限问题、启用身份验证功能，并指导用户配置防火墙及 Tailscale 系统。
version: 1.0.0
author: lxgicstudios
keywords: clawdbot, moltbot, security, audit, hardening, firewall, tailscale, permissions
---

# Clawdbot 安全审计

针对 Clawdbot/Moltbot 安装的全面安全扫描工具及加固指南。

**为何这很重要**：在 Shodan 上发现了 1,673 多个暴露的 Clawdbot 网关。如果您在服务器或虚拟专用服务器（VPS）上安装了 Clawdbot，您也可能在其中之一。

---

## 快速入门

```bash
# Scan for issues
npx clawdbot-security-audit

# Scan and auto-fix
npx clawdbot-security-audit --fix

# Deep scan (includes network check)
npx clawdbot-security-audit --deep --fix
```

---

## 检查内容

### 1. 网关绑定
- **安全**：`bind: "loopback"`（127.0.0.1）
- **危险**：`bind: "lan"` 或 `bind: "0.0.0.0"`

### 2. 文件权限
- 配置目录：700（仅所有者可访问）
- 配置文件：600（所有者可读写）
- 凭据：700（仅所有者可访问）

### 3. 认证
- 应启用令牌认证或密码认证
- 未经认证的情况下，任何找到您的网关的人都可以获得完全访问权限

### 4. Node.js 版本
- 最低要求：20.x
- 推荐版本：22.12.0 及以上
- 旧版本存在已知的安全漏洞

### 5. mDNS 广播
- Clawdbot 使用 Bonjour 进行本地发现
- 在服务器上，应禁用此功能

### 6. 外部可访问性（--deep）
- 检查您的网关端口是否可以从互联网访问
- 使用您的公共 IP 进行测试

---

## 手动加固步骤

### 第一步：仅绑定到本地主机

```json
// ~/.clawdbot/clawdbot.json
{
  "gateway": {
    "bind": "loopback",
    "port": 18789
  }
}
```

### 第二步：锁定文件权限

```bash
chmod 700 ~/.clawdbot
chmod 600 ~/.clawdbot/clawdbot.json
chmod 700 ~/.clawdbot/credentials
```

### 第三步：启用认证

```json
{
  "gateway": {
    "auth": {
      "mode": "token"
    }
  }
}
```

然后设置令牌：
```bash
export CLAWDBOT_GATEWAY_TOKEN=$(openssl rand -hex 32)
```

### 第四步：禁用 mDNS

```bash
export CLAWDBOT_DISABLE_BONJOUR=1
```

### 第五步：配置防火墙（UFW）

```bash
# Default deny incoming
sudo ufw default deny incoming
sudo ufw default allow outgoing

# Allow SSH (don't lock yourself out!)
sudo ufw allow ssh

# Allow Tailscale if using
sudo ufw allow in on tailscale0

# Enable firewall
sudo ufw enable

# DO NOT allow port 18789 publicly!
```

### 第六步：配置 Tailscale（推荐）

```bash
# Install
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up

# Configure Clawdbot
# Add to clawdbot.json:
{
  "gateway": {
    "bind": "loopback",
    "tailscale": {
      "mode": "serve"
    }
  }
}
```

---

**当存在漏洞时，哪些信息会被暴露？**

当 Clawdbot 网关被暴露时，以下信息可能会被泄露：
- ❌ 完整的聊天记录（Telegram、WhatsApp、Signal、iMessage）
- ❌ API 密钥（Claude、OpenAI 等）
- ❌ OAuth 令牌和机器人凭证
- ❌ 对主机机器的完全 shell 访问权限
- ❌ 工作区中的所有文件

**提示注入攻击** 可以通过一封电子邮件或消息提取这些数据。

---

## 清单

- [ ] 网关仅绑定到本地主机
- [ ] 文件权限已锁定（700/600）
- [ ] 已启用认证（令牌或密码）
- [ ] 使用 Node.js 22.12.0 及以上版本
- [ ] 服务器上的 mDNS 功能已禁用
- [ ] 防火墙已配置（UFW）
- [ ] 使用 Tailscale 进行远程访问（不进行端口转发）
- [ ] 仅使用 SSH 密钥进行认证（无密码）

---

## 安装

```bash
# npm
npm install -g clawdbot-security-audit

# ClawdHub
clawdhub install lxgicstudios/clawdbot-security
```

---

由 **LXGIC Studios** 开发 - [@lxgicstudios](https://x.com/lxgicstudios)