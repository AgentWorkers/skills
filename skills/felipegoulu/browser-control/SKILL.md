---
name: browser-control
description: 支持通过远程浏览器进行登录、两步验证（2FA）、验证码验证以及手动操作。该功能由 Google OAuth 保护，只有已配置的电子邮件地址才能访问。适用于需要用户登录网站、完成两步验证/多因素认证（2FA/MFA）、输入验证码或执行任何手动浏览器操作的场景。
---
# 浏览器控制

提供远程浏览器访问功能，支持登录、双因素认证（2FA）、验证码验证以及手动操作。

该功能由 Google OAuth 保护，用户必须使用自己的 Google 账户进行登录。

## 安装（仅首次使用）

在使用此功能之前，请运行安装程序以配置 ngrok 和 Google OAuth：

```bash
bash ~/.openclaw/skills/browser-control/install.sh
```

安装程序将：
1. 安装所需依赖项（VNC、noVNC、ngrok）
2. 请求您的 **ngrok 自动令牌**（从 https://dashboard.ngrok.com/get-started/your-authtoken 获取）
3. 验证您的 **Google 账户**（只有该账户才能访问浏览器）

每台机器只需执行此操作一次。

## 适用场景

当您需要用户执行以下操作时，可以使用此功能：
- 登录网站
- 完成双因素认证（2FA）/ 多因素认证（MFA）
- 解决验证码问题
- 执行任何手动浏览器操作

## 检查是否正在运行

```bash
~/.openclaw/skills/browser-control/status.sh
```

该命令会返回关于 VNC、noVNC 和 ngrok 隧道的运行状态（以 JSON 格式）。

## 启动服务（如未运行）

```bash
~/.openclaw/skills/browser-control/start-tunnel.sh
```

使用 Google OAuth 启动 VNC、noVNC 和 ngrok 隧道。启动过程大约需要 30 秒。

## 获取隧道地址

**⚠️ 在将隧道地址发送给用户之前，请务必重新读取此文件的内容。切勿使用缓存的数据。**

```bash
cat ~/.openclaw/skills/browser-control/config.json
```

该命令会返回隧道的实际地址。

**注意：** 隧道地址会在每次重新启动后发生变化。请务必每次都重新读取文件内容，切勿依赖内存中的数据。

## 工作流程

1. 使用 `status.sh` 命令检查服务状态。
2. 如果服务未运行，使用 `start-tunnel.sh` 命令启动服务。
3. **立即** 从 `config.json` 文件中获取隧道地址（切勿依赖内存中的数据！）
4. 将隧道地址发送给用户。
5. 用户使用自己的 Google 账户登录。
6. 用户完成所需的操作（如登录、输入验证码等）。
7. 等待用户确认操作完成。
8. 用户可以通过 CDP（localhost:9222）继续使用浏览器。

**重要提示：** 隧道地址会频繁变化。在发送地址之前，请务必再次从 `config.json` 文件中获取最新地址。

## 给用户的提示信息示例

```
🔐 I need you to log in.

Open: https://xxx.ngrok.app/vnc.html?password=xxx&autoconnect=true

You'll need to sign in with your Google account.
Let me know when you're done!
```

**注意：** 请勿在提示信息中提及密码。链接支持自动登录功能。用户只需：
1. 点击链接
2. 使用 Google 账户登录
3. 完成操作
4. 告诉您操作已完成。

## 安全性

- 该功能由 Google OAuth 保护，确保只有安装时配置的账户才能访问。
- 无需泄露密码，认证过程完全通过 Google 完成。
- 隧道地址会在重启后发生变化，从而增加安全性。

## 停止服务（可选）

```bash
~/.openclaw/skills/browser-control/stop-tunnel.sh
```

**操作完成后，隧道不会自动重新启动。** 需要手动运行 `start-tunnel.sh` 命令来重新启动服务。

在确认隧道已启动之前，请务必先检查 `status.sh` 的状态。

## 相关文件

```
~/.openclaw/skills/browser-control/
├── SKILL.md           # This file
├── start-tunnel.sh    # Start everything
├── stop-tunnel.sh     # Stop everything
├── status.sh          # Check status
├── config.json        # Current URL (read this before sending to user!)
├── ngrok-config.json  # Configured email
├── vnc-password       # VNC password (auto-included in URL)
└── ngrok.log          # ngrok logs
```