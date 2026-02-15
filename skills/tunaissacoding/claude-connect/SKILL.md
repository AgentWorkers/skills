---
name: claude-connect
description: "将 Claude 与 Clawdbot 即时连接，并保持 24/7 全天候连接状态。在完成设置后运行该命令，即可将您的订阅信息关联到 Clawdbot；之后，系统会自动刷新令牌（tokens），确保连接持续有效。"
---

# claude-connect

**一步将您的 Claude 订阅连接到 Clawdbot。**

该工具会自动完成以下操作：
- ✅ 从 macOS 的 Keychain 中读取 Claude 的 OAuth 令牌
- ✅ 将令牌以正确的 OAuth 格式写入 Clawdbot
- ✅ 每 2 小时自动刷新一次令牌（在令牌过期前）
- ✅ 在操作成功或失败时通知您
- ✅ 与 `clawdbot onboard` 工具兼容（修复了 OAuth 认证配置的错误）

---

## 快速入门

**1. 安装该工具：**
```bash
clawdhub install claude-connect
cd ~/clawd/skills/claude-connect
```

**2. 确保已登录 Claude CLI：**
```bash
claude auth
# Follow the browser login flow
```

**3. 运行安装程序：**
```bash
./install.sh
```

完成后，令牌将每 2 小时自动刷新一次。

---

## 功能说明

### 修复 `clawdbot onboard` 的 OAuth 问题

当您运行 `clawdbot onboard --auth-choice claude-cli` 时，有时令牌无法正确写入 `auth-profiles.json` 文件中。

该工具会：
1. 从 macOS 的 Keychain 中读取 OAuth 令牌（Claude CLI 将令牌存储在此位置）
2. 以正确的 OAuth 格式将令牌写入 `~/.clawdbot/agents/main/agent/auth-profiles.json` 文件
3. 设置自动刷新机制（通过 `launchd` 每 2 小时自动执行一次刷新）
4. 保持连接状态，确保您能够随时使用 Clawdbot 的服务

---

## 安装方法

### 自动安装（推荐）

使用安装程序：
```bash
cd ~/clawd/skills/claude-connect
./install.sh
```

安装程序将：
- ✅ 检查 Claude CLI 是否已正确配置
- ✅ 创建配置文件
- ✅ 设置自动刷新任务（通过 `launchd` 运行）
- ✅ 执行首次刷新测试

### 手动安装

1. 复制示例配置文件：
   ```bash
   cp claude-oauth-refresh-config.example.json claude-oauth-refresh-config.json
   ```

2. （可选）编辑配置文件：
   ```bash
   nano claude-oauth-refresh-config.json
   ```

3. 测试刷新功能：
   ```bash
   ./refresh-token.sh --force
   ```

4. （可选）安装自动刷新任务（通过 `launchd`）：
   ```bash
   cp com.clawdbot.claude-oauth-refresher.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/com.clawdbot.claude-oauth-refresher.plist
   ```

---

## 配置设置

编辑 `claude-oauth-refresh-config.json` 文件：

```json
{
  "refresh_buffer_minutes": 30,
  "log_file": "~/clawd/logs/claude-oauth-refresh.log",
  "notifications": {
    "on_success": true,
    "on_failure": true
  },
  "notification_target": "YOUR_CHAT_ID"
}
```

**配置选项：**
- `refresh_buffer_minutes`：令牌剩余多少分钟时触发刷新（默认值：30 分钟）
- `log_file`：记录刷新操作的日志文件路径
- `notifications.on_success`：刷新成功时发送通知（默认值：true）
- `notifications.on_failure`：刷新失败时发送通知（默认值：true）
- `notification_target`：您的 Telegram 聊天 ID（留空表示禁用通知）

---

## 使用方法

### 手动刷新令牌：
```bash
# Refresh now (even if not expired)
./refresh-token.sh --force

# Refresh only if needed
./refresh-token.sh
```

### 检查连接状态：
```bash
# View recent logs
tail ~/clawd/logs/claude-oauth-refresh.log

# Check auth profile
cat ~/.clawdbot/agents/main/agent/auth-profiles.json | jq '.profiles."anthropic:claude-cli"'

# Check Clawdbot status
clawdbot models status
```

### 禁用通知：

您可以通过以下方式禁用通知：
- 向 Clawdbot 发送指令：```
Disable Claude refresh success notifications
```
- 或者直接编辑配置文件：```json
{
  "notifications": {
    "on_success": false,
    "on_failure": true
  }
}
```

---

## 工作原理

### 刷新流程
1. **从 Keychain 中读取令牌：** 从 `Claude Code-credentials` 中获取 OAuth 令牌
2. **检查令牌有效期：** 仅当令牌剩余时间少于 30 分钟时才进行刷新（或通过 `--force` 参数强制刷新）
3. **调用 OAuth API：** 获取新的访问令牌和刷新令牌
4. **更新 `auth-profiles.json` 文件：** 将令牌以正确的 OAuth 格式写入文件
5. **更新 Keychain：** 将新令牌同步回 Keychain
6. **重启 Clawdbot 服务：** 使 Clawdbot 接收到新的令牌
7. **发送通知：** 在操作成功或失败时发送通知（可选）

### 自动刷新（通过 `launchd`）

该工具通过 `~/Library/LaunchAgents/com.clawdbot.claude-oauth-refresher.plist` 文件每 2 小时自动执行一次刷新任务。

**相关设置：**
```bash
# Stop auto-refresh
launchctl unload ~/Library/LaunchAgents/com.clawdbot.claude-oauth-refresher.plist

# Start auto-refresh
launchctl load ~/Library/LaunchAgents/com.clawdbot.claude-oauth-refresher.plist

# Check if running
launchctl list | grep claude
```

---

## 常见问题及解决方法

### 在使用 `clawdbot onboard` 后 OAuth 无法使用的问题

**症状：** 执行 `clawdbot onboard --auth-choice claude-cli` 后，Clawdbot 仍无法使用 OAuth 令牌

**解决方法：**
```bash
cd ~/clawd/skills/claude-connect
./refresh-token.sh --force
```

该工具会将令牌以正确的 OAuth 格式写入 `auth-profiles.json` 文件，从而解决这个问题。

### 令牌频繁过期的问题

**症状：** 认证失败频繁发生（通常在 8 小时后）

**解决方法：** 确保 `launchd` 任务正在运行：
```bash
launchctl load ~/Library/LaunchAgents/com.clawdbot.claude-oauth-refresher.plist
launchctl list | grep claude
```

### Keychain 中没有令牌的问题

**症状：** 在 Keychain 中找不到 `Claude Code-credentials` 的条目

**解决方法：** 先使用 Claude CLI 登录，然后再尝试刷新令牌：
```bash
claude auth
# Follow browser flow
```
之后再次运行刷新命令：```bash
./refresh-token.sh --force
```

---

## 卸载工具

**使用安装程序卸载：**
```bash
cd ~/clawd/skills/claude-connect
./uninstall.sh
```

**手动卸载：**
```bash
# Stop auto-refresh
launchctl unload ~/Library/LaunchAgents/com.clawdbot.claude-oauth-refresher.plist
rm ~/Library/LaunchAgents/com.clawdbot.claude-oauth-refresher.plist

# Remove skill
rm -rf ~/clawd/skills/claude-connect
```

---

## 升级说明

如果您之前安装了旧版本，请按照以下步骤进行升级：
```bash
cd ~/clawd/skills/claude-connect
./validate-update.sh  # Check what changed
clawdhub update claude-connect  # Update to latest
./install.sh  # Re-run installer if needed
```

---

## 相关文档

- [QUICKSTART.md] - 60 秒快速安装指南
- [UPGRADE.md] - 旧版本的升级说明
- [Clawdbot 文档](https://docs.clawd.bot) - 关于模型认证的详细信息

---

**版本：** 1.1.0  
**作者：** TunaIssaCoding  
**许可证：** MIT  
**代码仓库：** https://github.com/TunaIssaCoding/claude-connect