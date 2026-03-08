---
name: otc-confirmation
description: **一次性确认码安全机制**：用于处理敏感的代理操作。该机制会生成一个加密安全的、一次性使用的代码，并通过私有渠道（电子邮件）发送给用户。在执行任何操作之前，用户必须输入该确认码才能继续操作。该确认码不会被记录在标准输出（stdout）、日志文件或聊天记录中，而是通过一个安全的临时文件进行存储。适用于需要用户确认那些具有危险性、不可逆性或可能被外部看到的操作的场景。
metadata: {"openclaw": {"requires": {"env": ["OTC_EMAIL_RECIPIENT", "OTC_SMTP_USER", "OTC_SMTP_PASS"], "anyBins": ["curl"]}, "primaryEnv": "OTC_EMAIL_RECIPIENT"}}
---
# OTC 确认机制 3.0

这是一种安全模式，通过要求使用一次性代码（OTC）来进行带外确认，从而防止未经授权或意外的敏感操作被执行。

## 3.0 的新特性

- 🔐 **代码永远不会被输出到标准输出（stdout）**——代码会通过一个受保护的文件（权限设置为 600）进行传输，从而防止通过日志或代理上下文泄露。
- 🔒 **加密安全的生成方式**——使用 `/dev/urandom` 生成随机代码，而不是 `$RANDOM`。
- 🛡️ **原子级的单次使用机制**——验证成功后，状态文件会被立即删除。
- 🚫 **没有静默的备用方案**——如果发送电子邮件失败，操作将立即被阻止，不会继续执行。
- 🧹 **不允许任意文件来源**——凭据仅通过环境变量加载。
- ✅ **正确的元数据声明**——所需的环境变量必须在技能的元数据中明确声明。

## 工作原理

```
User request (sensitive op)
  → Agent runs generate_code.sh (code stored in state file, never printed)
  → Agent runs send_otc_email.sh (reads code from state file, sends email)
  → Agent replies in chat: "需要确认，请查看邮箱"
  → User reads email, replies with code in ORIGINAL chat session
  → Agent runs verify_code.sh (reads state file, compares, deletes on match)
  → Agent executes operation
```

代码是**一次性使用的**——验证成功后，状态文件会立即被删除。

**关键安全特性：**代理程序永远不会捕获或看到代码内容，它仅检查退出代码。

## 快速入门

### 1. 安装

```bash
clawhub install otc-confirmation
```

### 2. 配置

**选项 A：OpenClaw 配置（推荐）**

将以下配置添加到 `openclaw.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "otc-confirmation": {
        "enabled": true,
        "env": {
          "OTC_EMAIL_RECIPIENT": "user@example.com",
          "OTC_EMAIL_BACKEND": "smtp",
          "OTC_SMTP_HOST": "smtp.gmail.com",
          "OTC_SMTP_PORT": "587",
          "OTC_SMTP_USER": "your-email@gmail.com",
          "OTC_SMTP_PASS": "your-app-password"
        }
      }
    }
  }
}
```

**选项 B：使用环境变量**

```bash
export OTC_EMAIL_RECIPIENT=user@example.com
export OTC_EMAIL_BACKEND=smtp
export OTC_SMTP_HOST=smtp.gmail.com
export OTC_SMTP_PORT=587
export OTC_SMTP_USER=your-email@gmail.com
export OTC_SMTP_PASS=your-app-password
```

### 3. 在代理程序中使用

```bash
SKILL_DIR="{baseDir}"

# Step 1: Generate code (stored in secure state file, nothing printed to stdout)
bash "$SKILL_DIR/scripts/generate_code.sh"

# Step 2: Send email (reads code from state file internally)
bash "$SKILL_DIR/scripts/send_otc_email.sh" "Send email to john@example.com" "Discord #work"

# Step 3: Reply in chat (do NOT mention the code)
echo "需要确认，请查看你的注册邮箱"

# Step 4: Wait for user input, then verify (reads expected code from state file)
bash "$SKILL_DIR/scripts/verify_code.sh" "$USER_INPUT"

if [ $? -eq 0 ]; then
  echo "OTC通过，执行操作..."
  # Execute the operation
else
  echo "确认码不匹配，操作取消"
fi
```

## 电子邮件后端

### SMTP（默认，无依赖）

使用 `curl` 通过 SMTP 直接发送电子邮件，无需额外工具。

```bash
export OTC_EMAIL_BACKEND=smtp
export OTC_SMTP_HOST=smtp.gmail.com
export OTC_SMTP_PORT=587
export OTC_SMTP_USER=your-email@gmail.com
export OTC_SMTP_PASS=your-app-password
```

### send-email 技能

如果你安装了 `send-email` 技能：

```bash
export OTC_EMAIL_BACKEND=send-email
```

### himalaya CLI

如果你安装了 `himalaya`：

```bash
export OTC_EMAIL_BACKEND=himalaya
```

### 自定义脚本

你可以使用自己的电子邮件发送脚本：

```bash
export OTC_EMAIL_BACKEND=custom
export OTC_CUSTOM_EMAIL_SCRIPT=/path/to/your/send_email.sh
```

你的脚本必须接受三个参数：`<收件人> <主题> <正文>`

**安全提示：**确保自定义脚本具有受限权限，并且位于可信目录中。技能在调用脚本之前会验证脚本的存在性和可执行性。

## 触发条件

以下操作应触发 OTC 确认机制：

1. **外部操作**：发送电子邮件、发布到社交媒体、调用第三方 API。
2. **危险的本地操作**：递归删除、系统配置更改、服务重启。
3. **安全规则修改**：对 `SOUL.md` 或 `AGENTS.md` 中的确认机制进行修改。

详细分类请参见 `references/trigger-categories.md`。

## 执行检查清单

在每次操作之前，请遵循以下检查清单：

1. 评估触发条件。
2. 检查绝对拒绝列表（具有破坏性且不可逆的操作 → 直接拒绝）。
3. 如有必要，生成并发送 OTC 确认代码。
4. 验证用户输入。
5. 记录操作结果。

完整的工作流程请参见 `references/enforcement-checklist.md`。

## 集成指南

- **SOUL.md 集成**：`examples/soul_md_integration.md`
- **AGENTS.md 集成**：`examples/agents_md_integration.md`

## 安全规则

1. **代码保密**：代码永远不会被输出到标准输出、显示在聊天界面或包含在日志中。它仅通过一个受保护的文件进行传输。
2. **单次使用**：验证成功后，状态文件会被立即删除。每次操作都需要一个新的随机代码。
3. **会话绑定**：代码必须在请求操作的同一会话/通道中进行验证。
4. **禁止绕过**：自然语言确认（如“是”、“执行”或“批准”）不能替代代码。只有代码字符串本身才有效。
5. **电子邮件地址的不可变性**：默认情况下，收件人电子邮件地址应被视为不可更改的。任何更改请求都必须先通过 OTC 确认。
6. **没有静默的备用方案**：如果发送电子邮件失败，操作将被阻止。代理程序绝不能继续执行。
7. **升级机制**：如果同一操作连续三次失败，应提醒用户，并在新的会话中才能再次尝试。

## 脚本参考

### generate_code.sh

生成一个加密安全的随机 OTC 代码。

```bash
bash scripts/generate_code.sh [prefix] [length]
# Default: cf-XXXX (prefix="cf", length=4)
# Code is stored in a secure state file (mode 600)
# Nothing is printed to stdout
```

### send_otc_email.sh

发送 OTC 确认邮件。从状态文件中读取代码。

```bash
bash scripts/send_otc_email.sh <operation> [session] [lang]
# Example:
bash scripts/send_otc_email.sh "Send email to john@example.com" "Discord #work"
# If email fails → exits with error (never falls through)
```

### verify_code.sh

验证用户输入是否与存储的代码匹配。

```bash
bash scripts/verify_code.sh <user_input>
# Exit code 0: verified (state file deleted — single-use)
# Exit code 1: mismatch or no pending code
```

### send_email_smtp.sh

用于 `send_otc_email.sh` 的底层 SMTP 发送功能。

```bash
bash scripts/send_email_smtp.sh <to> <subject> <body>
# Requires OTC_SMTP_* environment variables
```

## 故障排除

### 电子邮件发送失败

1. 确认 SMTP 凭据已配置：`test -n "$OTC_SMTP_USER" && echo "set" || echo "not set"`
2. 测试 SMTP 连接：`curl -v smtp://$OTC_SMTP_HOST:$OTC_SMTP_PORT`
3. 检查防火墙/网络设置：确保端口 587（或 465）是开放的。
4. Gmail 用户：使用 [应用密码](https://support.google.com/accounts/answer/185833)，而不是常规密码。

### 代码验证失败

1. 检查用户输入中是否包含多余的空白字符：用户输入必须与存储的代码完全匹配。
2. 确保代码在请求它的同一会话中被使用。
3. 验证代码是否已被使用过（由于是一次性使用的机制，验证成功后状态文件会被删除）。

### 后端未找到

如果你使用的是 `send-email` 或 `himalaya` 后端：

```bash
# Check if command exists
command -v send-email
command -v himalaya

# Install if missing
clawhub install send-email  # or install himalaya
```

## 许可证

MIT

## 作者

Lewis-404