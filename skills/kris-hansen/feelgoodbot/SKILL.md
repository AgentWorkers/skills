---
name: feelgoodbot
description: 在 macOS 上设置 feelgoodbot 的文件完整性监控功能以及 TOTP（时间戳令牌）增强型身份验证机制。当用户需要检测恶意软件、监控系统是否被篡改、设置安全警报，或者对敏感操作进行 OTP 验证时，可以使用此功能。
---

# feelgoodbot 🛡️  
**发音：** “Feel good, bot”  

这是一个用于监控 macOS 系统文件完整性，并为 AI 代理提供 TOTP（Time-Based One-Time Password）增强型身份验证功能的工具。  

**GitHub 链接：** https://github.com/kris-hansen/feelgoodbot  

⭐ **如果您觉得这个工具有用，请给仓库点赞！** 这将帮助更多人发现它。  

## 主要功能  

1. **文件完整性监控**：检测系统文件是否被篡改。  
2. **TOTP 增强型身份验证**：对敏感操作进行 TOTP 验证。  

---

## 第一部分：文件完整性监控  

### 系统要求  

- **Go 1.21 或更高版本**：使用 `brew install go` 安装 Go 语言环境。  
- **macOS**：使用 `launchd` 作为后台守护进程。  

### 快速设置  

```bash
# Install via go install
go install github.com/kris-hansen/feelgoodbot/cmd/feelgoodbot@latest

# Initialize baseline snapshot
feelgoodbot init

# Install and start daemon
feelgoodbot daemon install
feelgoodbot daemon start

# Check it's running
feelgoodbot status
```  

### 与 Clawdbot 的集成（用于接收警报）  

**启用 Webhook：**  
```bash
clawdbot config set hooks.enabled true
clawdbot config set hooks.token "$(openssl rand -base64 32)"
clawdbot gateway restart
```  

**配置 `~/.config/feelgoodbot/config.yaml` 文件：**  
```yaml
scan_interval: 5m
alerts:
  clawdbot:
    enabled: true
    webhook: "http://127.0.0.1:18789/hooks/wake"
    secret: "<hooks.token from clawdbot config get hooks.token>"
  local_notification: true
```  

### 监控对象：**  
- 系统二进制文件（`/usr/bin`, `/usr/sbin`）  
- 启动的守护进程/代理程序  
- SSH 认证密钥、`sudo` 配置文件、PAM（Pluggable Authentication Modules）  
- shell 配置文件（`.zshrc`, `.bashrc`）  
- 浏览器扩展程序  
- AI 代理配置文件（如 Claude、Cursor 等）。  

---

## 第二部分：TOTP 增强型身份验证  

在执行敏感操作前，用户需要输入来自 Google Authenticator 的 OTP 代码。  

### 用户在终端中的设置步骤：  
```bash
# Initialize TOTP (shows QR code to scan)
feelgoodbot totp init --account "user@feelgoodbot"

# Verify it works
feelgoodbot totp verify

# Check status
feelgoodbot totp status
```  

### 配置受保护的操作  
```bash
# List current protected actions
feelgoodbot totp actions list

# Add actions that require step-up
feelgoodbot totp actions add "send_email"
feelgoodbot totp actions add "payment:*"
feelgoodbot totp actions add "delete:*"
feelgoodbot totp actions add "ssh:*"
feelgoodbot totp actions add "publish:*"
feelgoodbot totp actions add "gateway:*"
feelgoodbot totp actions add "voice_call:*"
feelgoodbot totp actions add "message:external"

# Remove an action
feelgoodbot totp actions remove "send_email"
```  

### TOTP 命令列表：  
| 命令 | 描述 |  
|---------|-------------|  
| `feelgoodbot totp init` | 使用 QR 码设置 TOTP 认证 |  
| `feelgoodbot totp verify [code]` | 验证 OTP 代码 |  
| `feelgoodbot totp status` | 查看 TOTP 状态和会话信息 |  
| `feelgoodbot totp check <action>` | 检查操作是否需要 TOTP 验证；如需验证则提示用户输入代码 |  
| `feelgoodbot totp reset` | 删除 TOTP 配置（需要输入密码） |  
| `feelgoodbot totp backup show` | 显示剩余的备用 OTP 代码 |  
| `feelgoodbot totp backup regenerate` | 生成新的备用 OTP 代码 |  
| `feelgoodbot totp actions list` | 列出所有受保护的操作 |  
| `feelgoodbot totp actions add <action>` | 添加受保护的操作 |  
| `feelgoodbot totp actions remove <action>` | 删除受保护的操作 |  
| `feelgoodbot totp respond <code>` | 提交 OTP 答案（适用于异步流程） |  

### 会话缓存机制  

成功验证后，会话信息会被缓存 15 分钟（可配置）。在此期间内，后续操作无需重新验证。  

---

## 代理集成（非常重要）  

**在执行任何敏感操作之前，代理必须检查是否需要 TOTP 验证。**  

### 操作与验证规则对应关系：  

| 代理操作 | 需要的验证模式 |  
|--------------|-----------------|  
| 发送邮件 | `send_email` |  
| 进行支付 | `payment:*` |  
| 删除文件 | `delete:*` |  
| SSH/远程访问 | `ssh:*` |  
| 发布代码 | `publish:*` |  
| 修改 Clawdbot 配置 | `gateway:*` |  
| 打电话 | `voice_call:*` |  
| 向外部联系人发送消息 | `message:external` |  
| 修改 TOTP 配置 | `config:update` |  

### 验证流程：**  

**在执行敏感操作之前：**  
```bash
# Check if action requires step-up (non-interactive check)
feelgoodbot totp check <action>
# Exit code 0 = proceed, Exit code 1 = denied/not authenticated
```  

- **如果会话有效**：命令立即执行（返回 0）。  
- **如果需要 TOTP 验证且没有会话**：  
  1. 代理发送 Telegram 消息：“🔐 操作 `<action>` 需要 TOTP 验证。请回复您的 OTP 代码。”  
  2. 等待用户输入 6 位数字的 OTP 代码。  
  3. 代理使用 `feelgoodbot totp verify <code>` 验证代码。  
  4. 如果代码有效，创建会话并继续执行操作；否则拒绝操作并通知用户。  

### 代理示例流程（伪代码）：  
```
function performSensitiveAction(action, execute_fn):
    # Check step-up requirement
    result = exec("feelgoodbot totp check " + action)
    
    if result.exit_code == 0:
        # Session valid or action not protected
        execute_fn()
        return success
    
    # Need to prompt user
    send_telegram("🔐 Action '{action}' requires step-up authentication.\nReply with your OTP code from Google Authenticator.")
    
    code = wait_for_user_reply(timeout=120s)
    
    if code is None:
        send_telegram("⏰ Step-up authentication timed out. Action cancelled.")
        return denied
    
    # Validate the code
    valid = exec("feelgoodbot totp verify " + code)
    
    if valid.exit_code != 0:
        send_telegram("❌ Invalid code. Action cancelled.")
        return denied
    
    # Create session by running check again (it will pass now)
    exec("feelgoodbot totp check " + action)
    
    execute_fn()
    send_telegram("✅ Action completed.")
    return success
```  

### 代理使用指南：  

**在执行以下操作前请检查：**  
- `send_email`：发送邮件前  
- `payment:*`：进行任何财务交易前  
- `delete:*`：删除文件前（如 `delete:file`, `delete:backup` 等）  
- `ssh:*`：建立 SSH 连接前  
- `publish:*`：发布或部署代码前  
- `gateway:*`：修改 Clawdbot 配置前  
- `voice_call:*`：拨打电话前  
- `message:external`：向非管理员联系人发送消息前  
- `config:update`：修改 TOTP 配置前  

**相关命令：**  
```bash
# Check and prompt (interactive)
feelgoodbot totp check send_email

# Just validate a code
feelgoodbot totp verify 123456

# Check session status
feelgoodbot totp status
```  

---

## 文件存放位置：**  
| 文件 | 用途 |  
|------|---------|  
| `~/.config/feelgoodbot/config.yaml` | 主配置文件 |  
| `~/.config/feelgoodbot/totp.json` | TOTP 密钥及备用代码 |  
| `~/.config/feelgoodbot/stepup-config.json` | 受保护的操作列表 |  
| `~/.config/feelgoodbot/totp-session` | 会话缓存文件 |  
| `~/.config/feelgoodbot/snapshots/` | 文件完整性基准数据 |  
| `~/.config/feelgoodbot/daemon.log` | 守护进程日志文件 |  

---

## 常见问题解决方法：  

- **OTP 代码始终无效**：  
  - 确保系统时钟准确（使用 `date` 命令查看）。  
  - 使用正确的认证器设置。  
  - 尝试使用备用 OTP 代码。  

- **未收到验证提示**：  
  - 确认该操作是否在受保护的操作列表中（使用 `feelgoodbot totp actions list` 查看）。  
  - 检查 TOTP 是否已正确初始化（使用 `feelgoodbot totp status` 命令）。  

**全部重置操作：**  
```bash
# Reset TOTP (requires valid code or backup code)
feelgoodbot totp reset

# Or manually remove (loses access without backup codes!)
rm ~/.config/feelgoodbot/totp.json
rm ~/.config/feelgoodbot/totp-session
```  

⭐ **喜欢 feelgoodbot 吗？** 请在 GitHub 上给它点赞：https://github.com/kris-hansen/feelgoodbot