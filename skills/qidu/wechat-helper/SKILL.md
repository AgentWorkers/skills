# 微信文件辅助自动化技能

该技能可自动化使用微信文件辅助工具（`filehelper.weixin.qq.com`）发送文本消息，并自动处理登录所需的二维码。

**主要特性：**
- 纯浏览器自动化（无需API密钥）
- 自动检测并发送二维码
- 支持多种消息发送渠道
- 配备了可用于定时任务的监控脚本（Cron）

## 使用场景

✅ **适用情况：**
- 需要向微信文件辅助工具发送文本消息
- 在未登录状态下需要自动处理二维码
- 希望使用现有的企业或团队微信账号（而非个人账号）
- 希望通过Cron定时发送消息

❌ **不适用情况：**
- 不能向个人微信账号发送消息（违反微信服务条款）
- 需要实时消息传递（请直接使用API）
- 不支持文件上传
- 需要查看消息历史或接收确认信息

## 使用要求

- 确保已启用浏览器扩展程序（通过`openclaw browser status`查看扩展程序状态是否显示为`enabled: true`）
- 拥有微信文件辅助工具的账号（非个人微信账号）
- 至少配置了一个用于发送消息的渠道

---

## 工作流程概述（共5步）

```
┌─────────────────────────────────────────────────────────────────┐
│  1. Open filehelper.weixin.qq.com or reuse existing tab         │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  2. Check login status - QR code needed?                         │
│     - URL ends with `/_/` → Logged in                           │
│     - Base URL → QR code displayed (logged out)                  │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  3a. If logged out: Capture QR and send to user                 │
│     - Screenshot QR code                                        │
│     - Send via available channel (WhatsApp/iMessage/Slack)      │
│     - Wait for user to scan                                     │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  3b. If logged in: Type message in textarea                     │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  4. Click send button or press Enter                             │
└─────────────────────────────────┬───────────────────────────────┘
                                  │
                                  ▼
┌─────────────────────────────────────────────────────────────────┐
│  5. Confirm message sent (check for success indicator)           │
└─────────────────────────────────────────────────────────────────┘
```

---

## 第1步：打开或重新使用相关标签页

```bash
# Check if tab already exists
browser action=tabs targetUrl="https://filehelper.weixin.qq.com/"

# Open new tab if needed
browser action=open targetUrl="https://filehelper.weixin.qq.com/"
targetId="<new-target-id>"
```

---

## 第2步：检查登录状态

```bash
# Check URL to determine state
browser action=evaluate fn="window.location.href" targetId="<targetId>"
```

### 登录状态指示器

| URL模式 | 状态 | 操作 |
|-------------|--------|--------|
| `filehelper.weixin.qq.com/_/` | ✅ 已登录 | 进入第3b步 |
| `filehelper.weixin.qq.com/` | ❌ 未登录 | 进入第3a步 |

---

## 第3a步：在未登录状态下捕获并发送二维码

```bash
# Capture QR code screenshot
browser action=screenshot path="/tmp/wechat-qr.png" targetId="<targetId>"

# Send via first available channel
message action=send to="<owner-phone>" media="/tmp/wechat-qr.png"

# Or specify channel explicitly
message action=send channel="whatsapp" to="+1234567890" media="/tmp/wechat-qr.png"
message action=send channel="telegram" to="@username" media="/tmp/wechat-qr.png"
message action=send channel="slack" to="#channel" media="/tmp/wechat-qr.png"

echo "📱 QR code sent. Waiting for scan..."

# Poll for login success (every 5 seconds, max 60 attempts)
attempts=0
while [ $attempts -lt 60 ]; do
  sleep 5
  url=$(browser action=evaluate fn="window.location.href" targetId="<targetId>")
  if echo "$url" | grep -q "_/"; then
    echo "✅ Login successful!"
    break
  fi
  attempts=$((attempts + 1))
done
```

---

## 第3b步：在已登录状态下输入消息

```bash
# Take snapshot to get refs
browser action=snapshot targetId="<targetId>"

# Type message
browser action=act kind="type" ref="input-area" text="Hello from OpenClaw! 🦞" targetId="<targetId>"
```

---

## 第4步：发送消息

```bash
# Option 1: Click send button
browser action=act kind="click" ref="send-btn" targetId="<targetId>"

# Option 2: Press Enter
browser action=act kind="press" key="Enter" targetId="<targetId>"
```

---

## 第5步：确认发送成功

```bash
# Check for success indicator
browser action=evaluate fn="{
  const sent = document.body.innerText.includes('已发送') || 
               document.body.innerText.includes('sent') ||
               document.querySelector('.success, [class*=\"success\"]');
  !!sent;
}" targetId="<targetId>"
```

---

## 完整脚本

### 快速发送（单条命令）

```bash
# Send a message - handles login automatically
wechat "Hello from OpenClaw!"
```

### 完整工作流程脚本

```bash
#!/bin/bash
# wechat-send.sh - Complete WeChat File Helper automation

MESSAGE="$1"
QR_FILE="/tmp/wechat-qr.png"
WEBSITE="https://filehelper.weixin.qq.com/"
TARGET_ID=""

echo "🔍 Checking WeChat File Helper status..."

# Step 1: Open or get existing tab
tabs=$(browser action=tabs targetUrl="$WEBSITE")
if echo "$tabs" | grep -q "targetId"; then
  TARGET_ID=$(echo "$tabs" | grep -o 'targetId="[^"]*"' | head -1 | cut -d'"' -f2)
  echo "✅ Using existing tab: $TARGET_ID"
else
  result=$(browser action=open targetUrl="$WEBSITE")
  TARGET_ID=$(echo "$result" | grep -o 'targetId="[^"]*"' | cut -d'"' -f2)
  echo "✅ Opened new tab: $TARGET_ID"
  sleep 2
fi

# Step 2: Check login status
url=$(browser action=evaluate fn="window.location.href" targetId="$TARGET_ID")

if echo "$url" | grep -q "_/"; then
  echo "✅ Already logged in"
else
  echo "❌ Not logged in - capturing QR..."
  
  # Capture QR code
  browser action=screenshot path="$QR_FILE" targetId="$TARGET_ID"
  
  # Send QR via owner's channel (set OWNER_PHONE env var)
  OWNER_PHONE="${OWNER_PHONE:-+1234567890}"
  message action=send to="$OWNER_PHONE" media="$QR_FILE" \
    -m "WeChat File Helper login required. Please scan QR code."
  
  echo "📱 QR code sent to $OWNER_PHONE"
  echo "⏳ Waiting for scan... (run again after scanning)"
  exit 0
fi

# Step 3: Type message
browser action=snapshot targetId="$TARGET_ID"
browser action=act kind="type" ref="input-area" text="$MESSAGE" targetId="$TARGET_ID"
echo "✅ Message typed"

# Step 4: Send
browser action=act kind="click" ref="send-btn" targetId="$TARGET_ID"
echo "✅ Send button clicked"

# Step 5: Confirm
sleep 1
result=$(browser action=evaluate fn="{
  document.body.innerText.includes('sent') || 
  document.body.innerText.includes('已发送')
}" targetId="$TARGET_ID")

if [ "$result" = "true" ]; then
  echo "✅ Message sent successfully!"
else
  echo "⚠️ Message may not have sent - check manually"
fi
```

### Cron监控脚本

```bash
#!/bin/bash
# cron-wechat.sh - Run every minute via cron

# Set owner phone for QR delivery
OWNER_PHONE="${OWNER_PHONE:-+1234567890}"

# Source main script
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/monitor.sh"

# Log
echo "$(date): WeChat File Helper check"
```

---

## 常用选择器

| 元素 | 选择器 | 参考值 |
|---------|----------|-----|
| 消息输入框 | `textarea` 或 `div[contenteditable]` | `input-area` |
| 发送按钮 | `button[type="button"]` 或 `.send-btn` | `send-btn` |
| 二维码显示区域 | `.qr-container` 或 `[class*="qr"]` | `qr-code` |
| 成功提示 | 显示“已发送”或“sent”的文本 | - |
| 用户头像 | `[class*="avatar"]` 或 `[class*="user"]` | - |

---

## 页面状态

| 状态 | URL | 说明 |
|-------|-----|-------------|
| **未登录** | `https://filehelper.weixin.qq.com/` | 显示用于扫描二维码的页面 |
| **已登录** | `https://filehelper.weixin.qq.com/_/` | 显示聊天界面 |

---

## 通过配置的渠道自动发送二维码

该技能会自动检测已配置的发送渠道，并将二维码发送到第一个可用的渠道：

```bash
# Check configured channels
openclaw config channels

# Priority order: WhatsApp → Telegram → Slack → First available
message action=send to="+1234567890" media="/tmp/wechat-qr.png"
```

---

## 限制事项

- **不支持文件上传**：点击文件上传按钮可能会导致失败或弹出不必要的对话框
- **无法查看消息历史**：无法查看之前的发送记录
- **会话过期**：长时间不活动后可能需要重新登录（约1-2小时）
- **二维码有效期**：未扫描时二维码每2分钟更新一次
- **违反微信服务条款**：使用个人微信账号会违反微信的服务条款
- **不支持群组发送**：该工具仅支持一对一发送
- **发送频率限制**：频繁发送消息可能会被限制

---

## 故障排除

| 问题 | 解决方案 |
|-------|----------|
| 无法找到输入框 | 运行`snapshot`命令刷新页面元素 |
| 发送按钮无法使用 | 尝试按下Enter键 |
| 会话过期 | 显示二维码后请重新扫描以登录 |
| 重新加载后选择器失效 | 重新加载页面可恢复选择器的有效性 |
| 二维码无法发送 | 检查是否正确配置了发送渠道 |
| 消息未送达 | 确认接收方信息正确 |
| Cron任务未执行 | 检查`crontab -e`命令的输出 |
| 浏览器无法启动 | 运行`openclaw browser status`命令检查浏览器状态 |

---

## 相关脚本

| 脚本 | 功能 |
|--------|---------|
| `scripts/monitor.sh` | 主监控脚本 |
| `scripts/capture_qrcode.sh` | 仅用于捕获二维码 |
| `scripts/cron-wechat.sh` | 用于定时发送消息的Cron脚本 |

---

## 环境变量

| 变量 | 说明 | 默认值 |
|----------|-------------|---------|
| `OWNER_PHONE` | 用于发送二维码的手机号码 | `+1234567890` |

---

## 参考资料

- `openclaw browser status`：查看浏览器扩展程序的状态
- `openclaw config channels`：列出可使用的消息发送渠道
- `chat-deepseek`：适用于DeepSeek平台的类似自动化脚本
- `imsg`：将发送结果发送到iMessage
- `whatsapp-login`：用于通过WhatsApp二维码登录的脚本