---
name: claude-oauth-refresher
description: 请确保您的 Claude 访问令牌始终保持有效状态（即随时都是“新鲜的”）。系统会自动在 OAuth 令牌过期前进行刷新，这样您就永远不会遇到认证失败的情况。
---

# Claude-OAuth-Refresher

**为 macOS 上的 Claude Code CLI 自动刷新 OAuth 令牌**

通过自动在 OAuth 令牌过期前进行刷新，确保您的 Claude 账户始终保持登录状态。

---

## ⚠️ 要求

此功能 **仅适用于 macOS**，并需要以下条件：
1. **macOS**（使用 Keychain 来安全存储凭证）
2. **已安装 Claude Code CLI**（可执行 `claude` 命令）
3. **已登录 Claude 账户**（运行 `claude` 后再运行 `login`——令牌将存储在 Keychain 中）
4. **已安装并运行 Clawdbot**

**不确定是否已设置？** 运行验证脚本：
```bash
./verify-setup.sh
```

---

## 功能介绍

- **监控** Claude CLI 令牌的过期时间
- **在令牌过期前自动刷新令牌**（默认延迟 30 分钟）
- **通过三种方式通知您**：
  - 🔄 开始：**“正在刷新 Claude 令牌...”**
  - ✅ 成功：**“Claude 令牌已刷新！”**
  - ❌ 失败：**显示详细错误及故障排除步骤**
- **记录所有刷新尝试以供调试**

---

## 安装

### 快速设置（推荐）

```bash
cd ~/clawd/skills/claude-oauth-refresher
./install.sh
```

**此安装程序只需运行一次**，即可设置每 2 小时自动刷新令牌的机制。

安装程序将：
1. 验证您的系统是否符合要求
2. **交互式配置** 通知偏好设置
3. 自动检测您的通知目标（Telegram、Slack 等）
4. 设置 launchd 以自动执行刷新任务
5. 立即测试刷新功能

**安装完成后：**
- 配置更改会自动生效（刷新脚本每次运行时都会读取配置）
- 编辑 `claude-oauth-refresh-config.json` 以修改设置
- 可请求 Clawdbot 为您修改设置
- **仅在需要重新安装或修复问题时才需要重新运行安装程序**

### 交互式通知设置

在安装过程中，系统会提示您进行相关设置：

```
Configure Notifications:
💡 Recommendation: Keep all enabled for the first run to verify it works.
   You can disable them later by:
   1. Editing ~/clawd/claude-oauth-refresh-config.json
   2. Asking Clawdbot: "disable Claude refresh notifications"

Enable "🔄 Refreshing token..." notification? [Y/n]: 
Enable "✅ Token refreshed!" notification? [Y/n]: 
Enable "❌ Refresh failed" notification? [Y/n]: 
```

**建议：** 先启用所有通知类型以确保一切正常工作，确认无误后再关闭开始/成功通知。

---

## 使用 Clawdbot 管理通知

**您可以请求 Clawdbot 为您更改通知设置！** 无需手动编辑 JSON 文件。

### 示例

**禁用特定通知类型：**
```
"disable Claude refresh start notifications"
"disable Claude refresh success notifications"
"turn off Claude token refresh start messages"
```

**启用通知类型：**
```
"enable Claude refresh start notifications"
"enable all Claude refresh notifications"
"turn on Claude token refresh success messages"
```

**查看当前设置：**
```
"show Claude refresh notification settings"
"what are my Claude token refresh notification settings?"
```

**禁用所有通知：**
```
"disable all Claude refresh notifications"
"turn off all Claude token notifications"
```

**恢复默认设置：**
```
"reset Claude refresh notifications to defaults"
```

### 工作原理

Clawdbot 会：
1. 读取您的 `~/clawd/claude-oauth-refresh-config.json` 文件
2. 更新相应的通知标志
3. 保存文件
4. 确认更改

**更改将在下一次刷新时立即生效**（无需重启任何程序）。

---

## 自动检测（智能默认设置）

**安装脚本会自动检测您的通知设置！**

它将读取 `~/.clawdbot/clawdbot.json` 文件，以获取：
- 您启用的消息通道
- 您的聊天 ID、电话号码或用户 ID
- 并自动将这些信息填充到 `claude-oauth-refresh-config.json` 文件中

**示例：** 如果您启用了 Telegram 并设置了聊天 ID `123456789`，安装程序会生成如下配置：
```json
{
  "notification_channel": "telegram",
  "notification_target": "123456789"
}
```

**如需覆盖设置：** 安装完成后直接编辑 `claude-oauth-refresh-config.json` 文件以使用其他通道或目标。

**如果自动检测失败：** 安装程序会提示您手动配置（详见“查找目标 ID”部分）。

**安装前测试检测功能：**
```bash
./test-detection.sh
# Shows what would be auto-detected without modifying anything
```

---

## 查找目标 ID

要接收通知，您需要在 `claude-oauth-refresh-config.json` 中配置 `notification_target`。以下是针对各平台的配置方法：

### Telegram

**格式：** 数字聊天 ID（例如：`123456789`）

**查找方法：**
```bash
# Option 1: Use Clawdbot CLI
clawdbot message telegram account list

# Option 2: Message @userinfobot on Telegram
# Send any message, it will reply with your ID

# Option 3: Check recent messages
clawdbot message telegram message search --limit 1 --from-me true
```

**示例配置：**
```json
{
  "notification_channel": "telegram",
  "notification_target": "123456789"
}
```

### Slack

**格式：**
- 直接消息：`user:U01234ABCD`
- 频道：`channel:C01234ABCD`

**查找方法：**
```bash
# List channels
clawdbot message slack channel list

# Find user ID
clawdbot message slack user list | grep "your.email@company.com"

# Or click on your profile in Slack → More → Copy member ID
```

**示例配置：**
```json
{
  "notification_channel": "slack",
  "notification_target": "user:U01234ABCD"
}
```

### Discord

**格式：**
- 直接消息：`user:123456789012345678`
- 频道：`channel:123456789012345678`

**查找方法：**
```bash
# Enable Developer Mode in Discord (Settings → Advanced → Developer Mode)
# Then right-click your username → Copy ID

# Or list channels
clawdbot message discord channel list
```

### WhatsApp

**格式：** E.164 电话号码（例如：`+15551234567`）

**查找方法：**
- 使用完整的电话号码（包含国家代码）
- 格式：`+[国家代码][号码]`（无空格、破折号或括号）

**示例：**
- 美国：`+15551234567`
- 英国：`+447911123456`
- 澳大利亚：`+61412345678`

**示例配置：**
```json
{
  "notification_channel": "whatsapp",
  "notification_target": "+15551234567"
}
```

### iMessage

**推荐格式：** `chat_id:123`

**查找方法：**
```bash
# List recent chats to find your chat_id
clawdbot message imessage thread list --limit 10

# Find the chat with yourself or your preferred device
```

**其他格式：**
- 电话：`+15551234567`（E.164 格式）
- 电子邮件：`your.email@icloud.com`

**示例配置：**
```json
{
  "notification_channel": "imessage",
  "notification_target": "chat_id:123"
}
```

### Signal

**格式：** E.164 电话号码（例如：`+15551234567`）

**查找方法：**
- 使用您在 Signal 中注册的电话号码
- 格式：`+[国家代码][号码]`（无空格、破折号或括号）

**示例配置：**
```json
{
  "notification_channel": "signal",
  "notification_target": "+15551234567"
}
```

---

## 配置文件：`claude-oauth-refresh-config.json`

```json
{
  "refresh_buffer_minutes": 30,
  "log_file": "~/clawd/logs/claude-oauth-refresh.log",
  "notifications": {
    "on_start": true,
    "on_success": true,
    "on_failure": true
  },
  "notification_channel": "telegram",
  "notification_target": "YOUR_CHAT_ID"
}
```

### 选项

| 选项 | 类型 | 默认值 | 说明 |
|--------|------|---------|-------------|
| `refresh_buffer_minutes` | 数字 | `30` | 令牌在过期前多久进行刷新 |
| `log_file` | 字符串 | `~/clawd/logs/claude-oauth-refresh.log` | 日志保存路径 |
| `notifications.on_start` | 布尔值 | `true` | 发送 “🔄 正在刷新令牌...” 通知 |
| `notifications.on_success` | 布尔值 | `true` | 发送 “✅ 令牌已刷新！” 通知 |
| `notifications.on_failure` | 布尔值 | `true` | 发送 “❌ 刷新失败” 通知及详细错误信息 |
| `notification_channel` | 字符串 | `telegram` | 使用的通道（参见上述选项） |
| `notification_target` | 字符串 | `YOUR_CHAT_ID` | 目标 ID（参见“查找目标 ID”部分） |

### 通知类型说明

**🔄 开始（`on_start`）**
- 在刷新过程开始时发送
- 有助于调试或了解刷新时间
**建议：** 确认设置无误后关闭此选项（可能会产生较多通知）

**✅ 成功（`on_success`）
- 令牌成功刷新时发送
- 包含令牌的有效期限（例如：“有效期 24 小时”）
**建议：** 确信设置无误后关闭此选项（可能会产生较多通知）

**❌ 失败（`on_failure`）
- 令牌刷新失败时发送详细错误信息
- 包含基于错误类型的故障排除步骤
**建议：** 保持此选项开启！您需要了解失败情况**

### 示例配置

**最小化配置（仅显示失败通知）：**
```json
{
  "notifications": {
    "on_start": false,
    "on_success": false,
    "on_failure": true
  }
}
```

**详细配置（显示所有通知）：**
```json
{
  "notifications": {
    "on_start": true,
    "on_success": true,
    "on_failure": true
  }
}
```

**静音配置（不显示任何通知）：**
```json
{
  "notifications": {
    "on_start": false,
    "on_success": false,
    "on_failure": false
  }
}
```

---

## 详细失败信息

当刷新失败时，您会收到包含以下内容的详细通知：
1. **错误信息**：出错的原因
2. **详细信息**：额外的上下文（如 HTTP 状态码、错误响应等）
3. **故障排除**：根据错误类型提供的具体步骤
4. **帮助**：日志存放位置及获取支持的途径

### 失败通知示例**

```
❌ Claude token refresh failed

Error: Network timeout connecting to auth.anthropic.com
Details: Connection timed out after 30s

Troubleshooting:
- Check your internet connection
- Verify you can reach auth.anthropic.com
- Try running manually: ~/clawd/skills/claude-oauth-refresher/refresh-token.sh

Need help? Message Clawdbot or check logs:
~/clawd/logs/claude-oauth-refresh.log
```

### 常见错误及解决方法

**网络/超时错误**
```
Troubleshooting:
- Check your internet connection
- Verify you can reach auth.anthropic.com
- Try running manually: ./refresh-token.sh
```

**无效的刷新令牌**
```
Troubleshooting:
- Your refresh token may have expired
- Re-authenticate: claude auth logout && claude auth
- Verify Keychain access: security find-generic-password -s 'claude-cli-auth' -a 'default'
```

**Keychain 访问被拒绝**
```
Troubleshooting:
- Check Keychain permissions
- Re-run authentication: claude auth
- Verify setup: ./verify-setup.sh
```

**缺少认证配置文件**
```
Troubleshooting:
- Run: claude auth
- Verify file exists: ~/.config/claude/auth-profiles.json
- Check file permissions: chmod 600 ~/.config/claude/auth-profiles.json
```

---

## 使用方法

### 检查状态**

```bash
# View recent logs
tail -f ~/clawd/logs/claude-oauth-refresh.log

# Check launchd status
launchctl list | grep claude-oauth-refresher

# Manual refresh (for testing)
cd ~/clawd/skills/claude-oauth-refresher
./refresh-token.sh
```

### 修改设置

**方法 1：请求 Clawdbot 帮助（最简单）**
```
"disable Claude refresh start notifications"
"show Claude refresh notification settings"
```

**方法 2：手动编辑配置文件**
```bash
nano ~/clawd/skills/claude-oauth-refresher/claude-oauth-refresh-config.json
```

更改会在下一次刷新时自动生效（每 2 小时一次，或手动触发时生效）。

**无需重启任何程序！** 刷新脚本每次运行时都会读取配置文件。

---

## 故障排除

### 问题：`verify-setup.sh` 报告未找到 Claude CLI**

**解决方法：**
```bash
# Install Claude CLI
brew install claude

# Or download from https://github.com/anthropics/claude-cli
```

### 问题：`verify-setup.sh` 报告未找到刷新令牌**

**解决方法：**
```bash
# Authenticate with Claude
claude auth

# Follow the prompts to log in
```

### 问题：通知未送达**

**解决方法：**
1. 确认您的 `notification_target` 格式是否符合上述示例
2. 手动测试：`./refresh-token.sh`
3. 检查 Clawdbot 是否正在运行：`clawdbot gateway status`
4. 验证通知设置：`./claude-oauth-refresh-config.json`

### 问题：刷新失败并显示 “invalid_grant”

**解决方法：**
```bash
# Re-authenticate from scratch
claude auth logout
claude auth

# Test refresh again
cd ~/clawd/skills/claude-oauth-refresher
./refresh-token.sh
```

### 问题：升级后找不到配置文件**

**解决方法：**
配置文件已从 `config.json` 更名为 `claude-oauth-refresh-config.json`。

```bash
# If you have an old config.json, run the installer to migrate:
cd ~/clawd/skills/claude-oauth-refresher
./install.sh
# Choose to keep existing config when prompted
```

### 需要重新安装或修复问题**

**解决方法：**
**安装程序会：**
- 检测现有配置并询问是否保留
- 更新 launchd 任务
- 测试刷新功能

---

## 卸载

```bash
cd ~/clawd/skills/claude-oauth-refresher
./uninstall.sh
```

卸载程序将：
- 停止并卸载 launchd 服务
- 删除 plist 文件
- 可选：删除日志和配置文件

---

## 工作流程

1. **安装程序（`install.sh`）**：仅运行一次，用于设置：
   - 自动检测通知目标
   - 交互式配置通知类型
   - 创建 launchd 任务
   - 立即测试刷新功能

2. **launchd**：每 2 小时自动运行 `refresh-token.sh`

3. **刷新脚本（`refresh-token.sh`）**：每次运行时：
   - 读取配置文件（配置更改会自动生效！）
   - 从 `~/.config/claude/auth-profiles.json` 检查令牌过期时间
   - 如果令牌在指定时间窗口（默认 30 分钟）内过期：
     - 发送开始通知（如果启用）
     - 从 Keychain 中获取新令牌
     - 调用 OAuth 端点获取新令牌
     - 更新认证配置和 Keychain
     - 发送成功通知（如果启用）
   - 如果刷新失败：
     - 发送详细失败通知及故障排除信息
   - 所有操作都会记录在 `~/clawd/logs/claude-oauth-refresh.log` 中

4. **配置更改**：可随时编辑 `claude-oauth-refresh-config.json` 文件
   - 可请求 Clawdbot 为您修改配置
   - 更改将在下一次刷新时生效
   **无需重启！**

---

## 安全性

- **令牌永远不会被写入日志或配置文件**
- 刷新令牌安全存储在 macOS Keychain 中
- 令牌缓存于 `~/.config/claude/auth-profiles.json` 文件中（权限设置为 600）
- 所有 HTTP 请求均使用 Claude 的官方 OAuth 端点
- 配置文件为公开可读格式（不包含任何敏感信息）

## 支持方式

**日志：** `~/clawd/logs/claude-oauth-refresh.log`

**遇到问题时：**
1. 运行 `./verify-setup.sh` 进行诊断
2. 查看日志中的详细错误信息
3. 手动测试刷新功能：`./refresh-token.sh`
4. 检查通知设置：`cat claude-oauth-refresh-config.json | jq .notifications`

**需要帮助？** 请提供以下信息：
- `./verify-setup.sh` 的执行结果
- 日志的最后 20 行：`tail -20 ~/clawd/logs/claude-oauth-refresh.log`
- macOS 版本：`sw_vers`
- 配置文件内容（已屏蔽敏感信息）：`cat claude-oauth-refresh-config.json | jq 'del(.notification_target)'`