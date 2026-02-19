---
name: browser-auth
description: 为手动用户认证（解决验证码、双因素认证、登录等问题）创建一个安全的远程浏览器隧道，并捕获会话数据。该功能专为 AI Commander 设计。
metadata: {
  "author": "Skippy & Lucas (AI Commander)",
  "homepage": "https://aicommander.dev",
  "env": {
    "AUTH_HOST": { "description": "IP to bind the server to (default: 127.0.0.1). Use 0.0.0.0 only with a secure tunnel.", "default": "127.0.0.1" },
    "AUTH_TOKEN": { "description": "Secret token for accessing the tunnel (default: random hex string)." },
    "BROWSER_PROXY": { "description": "SOCKS5/HTTP proxy for the browser (e.g. socks5://127.0.0.1:40000)." }
  },
  "openclaw": {
    "requires": { "bins": ["node", "chromium-browser"] },
    "install": [
      {
        "id": "npm-deps",
        "kind": "exec",
        "command": "npm install express socket.io playwright-core",
        "label": "Install Node.js dependencies"
      }
    ]
  }
}
---
# 浏览器认证（Browser Auth）

该技能允许代理请求用户在网站上手动登录，然后捕获会话cookie或localStorage数据，以便后续进行自动化操作。

## 🚨 安全性与风险缓解

我们非常重视安全性。以下是我们针对远程浏览器控制相关常见问题的处理方式：

### 1. 遥程代码执行（RCE）防护
*   **始终使用沙箱环境**：Chromium在运行时始终启用系统沙箱功能。代码中无法禁用该功能，这可以防止恶意网站逃出浏览器并在您的主机上执行代码。
*   **建议使用隔离环境**：我们建议在隔离容器（如Docker）或专用虚拟机中运行此技能，以提供额外的安全保护。

### 2. 令牌泄露（Referrer Protection）
*   **引用策略（Referrer Policy）**：服务器强制实施`Referrer-Policy: no-referrer`策略，确保即使用户访问不受信任的网站，您的`AUTH_TOKEN`也不会被包含在HTTP Referer头中。
*   **URL清理**：页面加载后，系统会立即从浏览器地址栏中清除`token`参数。

### 3. 数据敏感性
*   **会话数据**：`session.json`文件中包含有效的登录cookie，应将其视为敏感信息进行保护。
* **强制清理**：代理完成任务后，必须立即删除会话文件。
* **无数据持久化**：该技能不会长期存储凭证信息，也不会将其泄露到外部服务器。

### 4. 网络安全性
*   **默认本地绑定**：服务器默认绑定到`127.0.0.1`地址。
*   **安全访问**：如需远程访问，请勿直接绑定到`0.0.0.0`。建议使用**Tailscale**、**Cloudflare Tunnel**或**SSH隧道**等安全通道。

## 使用场景
- 当网站需要用户手动操作以完成验证码或二次验证（2FA）时。
- 当机器人检测机制阻止自动化登录时。
- 当您希望在不共享密码的情况下授权代理时。

## 工作流程
1. **请求认证**：使用`scripts/auth_server.js`启动隧道。
2. **提供链接**：通过安全渠道将包含令牌的链接分享给目标用户。
3. **等待用户登录**：用户登录后在网页界面中点击“完成”（DONE）。
4. **验证会话**：使用`scripts/verify_session.js`确认会话有效。
5. **清理数据**：任务完成后立即删除会话文件。

## 所需工具
- `express`、`socket.io`、`playwright-core`以及系统自带的`chromium-browser`。

### 启动认证服务器
```bash
AUTH_HOST=127.0.0.1 AUTH_TOKEN=mysecret node scripts/auth_server.js <port> <session_file>
```

### 验证会话
```bash
node scripts/verify_session.js <session_file> <target_url> <expected_text>
```

## 运行时要求
需要安装以下依赖库：`express`、`socket.io`、`playwright-core`以及`chromium-browser`。