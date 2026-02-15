---
name: hour-meter
description: **功能说明：**  
从指定的起始时间点开始，记录经过的时间，并提供防篡改的锁定机制。其工作原理类似于模拟式的霍布斯计时器，但采用数字形式。适用于记录设备运行时间、服务时长、事件发生后的时间间隔、用户戒酒/戒毒的时长、项目持续时间等。支持以下操作：创建记录、锁定记录（确保数据不被篡改）、检查记录内容、通过外部哈希值验证记录的完整性、列出所有记录以及导出记录数据。
---

# 小时计数器

这是一个生活事件追踪工具，支持三种模式、里程碑通知以及防篡改的验证功能。

## 三种模式

### **倒计时** — 从事件发生至今所经过的时间
```bash
# Quit smoking tracker
meter.py create smoke-free --start "2025-06-15T08:00:00Z" -d "Last cigarette"
meter.py milestone smoke-free -t hours -v 720 -m "🎉 30 days smoke-free!"
meter.py lock smoke-free  # → Gives you paper code to save
```

### **计时** — 距离事件发生还剩的时间
```bash
# Baby due date
meter.py create baby --start "2026-01-15" --end "2026-10-15" --mode down -d "Baby arriving!"
meter.py milestone baby -t percent -v 33 -m "👶 First trimester complete!"
```

### **全程记录** — 从开始到结束的整个过程
```bash
# Career span
meter.py create career --start "1998-05-15" --end "2038-05-15" -d "40-year career"
meter.py milestone career -t percent -v 50 -m "📊 Halfway through career!"
meter.py career --meter career --rate 85 --raise-pct 2.5
```

## 防篡改机制

当你锁定小时计数器时，会获得一个**纸质代码**——一段经过校验和处理的短代码，可以将其写在纸上：

```
╔══════════════════════════════════════════════════════════════╗
║  PAPER CODE (write this down):                               ║
║     318B-3229-C523-2F9C-V                                    ║
╚══════════════════════════════════════════════════════════════╝
```

### 四种保存方式（非技术性说明）

**1️⃣ 纸质方式** — 将代码写在纸上或便签上
- 由破折号组成的20个字符，便于复制
- 内置的校验和功能可以检测输入错误
- 可以保存在钱包中、贴在设备上或随身携带

**2️⃣ 照片方式** — 截取锁屏界面并拍照
- 保存到手机相册或云端
- 无需输入任何信息，实现视觉备份

**3️⃣ 目击者文件** — 代码会自动保存到`~/.openclaw/meter-witness.txt`文件中
- 该文件为只读日志，记录所有被锁定的小时计数器的信息
- 可将文件夹同步到Dropbox/iCloud/Google Drive进行云端备份
- 文件内容包括纸质代码、完整的哈希值和时间戳

**4️⃣ 自动发送邮件** — 点击邮件链接或复制邮件内容
- 邮件会自动打开，主题和正文已预先填写
- 或者复制以下短信：`🔒 我的小时计数器 | 代码：XXXX-XXXX-XXXX-XXXX-C | 锁定时间：2026-02-02`
- 发送给自己，稍后可在收件箱中查看以进行验证

**5️⃣ SendGrid自动发送邮件** — 锁定时自动发送验证邮件
```bash
# Set your SendGrid API key
export SENDGRID_API_KEY=SG.xxxxx
export SENDGRID_FROM_EMAIL=verified@yourdomain.com

# Lock and email in one command
meter.py lock my-meter --email you@example.com
```
- 会发送一封格式精美的HTML邮件，其中包含纸质代码
- 需要在SendGrid中验证发送者的身份（请参阅SendGrid文档）
- 非常适合自动化工作流程

### 后期验证

```bash
# With paper code (catches typos!)
meter.py verify my-meter "318B-3229-C523-2F9C-V"

# → ✅ VERIFIED! Paper code matches.
# → ⚠️ CHECKSUM ERROR! (if you have a typo)
# → ❌ MISMATCH! (if tampered)
```

## 里程碑功能

```bash
meter.py milestone <name> --type hours --value 1000 --message "1000 hours!"
meter.py milestone <name> --type percent --value 50 --message "Halfway!"
meter.py check-milestones  # JSON output for automation
```

### 邮件通知（v1.3.0）

你可以直接在邮箱中收到里程碑通知：

```bash
# Create meter with email notifications
meter.py create my-meter \
  --notify-email you@example.com \
  --from-email verified@yourdomain.com \
  -d "My tracked event"

# Add milestones as usual
meter.py milestone my-meter -t hours -v 24 -m "🎉 24 hours complete!"

# When check-milestones runs and a milestone fires, email is sent automatically
meter.py check-milestones
# → Triggers milestone AND sends email notification
```

**邮件内容包括：**
- 🎯 里程碑信息
- ⏱️ 当前经过的时间
- 📝 小时计数器的描述

需要设置`SENDGRID_API_KEY`环境变量。

### 里程碑通知方式：Heartbeat vs Cron

**推荐使用：Heartbeat**（更新频率约30分钟）
- 在`HEARTBEAT.md`文件中添加：`Run meter.py check-milestones and notify triggered`
- 可与其他定期任务一起批量处理
- 节省成本：与其他Heartbeat任务共享令牌
- 适用于大多数使用场景（如停止追踪、职业里程碑等）

### 触发操作（代理自动化）

在里程碑消息前加上`ACTION:`前缀，以触发代理执行，而不仅仅是简单地发布通知：

```bash
# Just posts the message
meter.py milestone my-meter -t hours -v 24 -m "🎉 24 hours complete!"

# Triggers agent to EXECUTE the instruction
meter.py milestone my-meter -t hours -v 24 -m "ACTION: Check the weather and post a summary"
```

在`HEARTBEAT.md`中进行配置：
```markdown
- If message starts with "ACTION:", execute it as an instruction
- Otherwise, post the message to the configured channel
```

**替代方案：Cron**（精确计时）
- 适用于需要精确计时的场景（例如倒计时）
- ⚠️ **成本提示：**Cron每隔1分钟发送一次通知，每天会触发1,440次API调用，成本较高！
- 如果使用Cron，请确保间隔时间≥15分钟以控制成本
- 适用于一次性提醒，不适合持续监控

**经验法则：**如果30分钟的更新频率可以接受，建议使用Heartbeat。只有在需要精确计时的情况下才使用Cron。

## 快速参考

```bash
meter.py create <name> [--start T] [--end T] [--mode up|down|between] [-d DESC]
meter.py lock <name>                # Seal + get paper code
meter.py verify <name> <code>       # Verify paper code
meter.py check <name>               # Status + progress
meter.py milestone <name> -t hours|percent -v N -m "..."
meter.py check-milestones           # All milestones (JSON)
meter.py witness [--show] [--path]  # Witness file
meter.py list                       # All meters
meter.py career [--meter M] [--rate R] [--raise-pct P]
meter.py export [name]              # JSON export
```

## SendGrid邮件Webhook服务器

当收件人打开、点击、邮件被退回或取消订阅你的验证邮件时，你可以实时收到通知。

### 设置方法

```bash
# Start webhook server with Discord webhook (recommended)
python sendgrid_webhook.py --port 8089 --discord-webhook https://discord.com/api/webhooks/xxx/yyy

# Or process events manually (for agent to post)
python sendgrid_webhook.py --process-events
python sendgrid_webhook.py --process-events --json
```

### Discord Webhook设置（推荐）

1. 在Discord频道中，进入**设置 > 集成 > Webhook**
2. 点击**新建Webhook**，复制URL
3. 将URL传递给`--discord-webhook`参数，或设置`DISCORD_WEBHOOK_URL`环境变量

### SendGrid设置

1. 进入**SendGrid > 设置 > 邮件设置 > 事件Webhook**
2. 点击**“创建新的Webhook”**（或编辑现有Webhook）
3. 将HTTP POST URL设置为：`https://your-domain.com/webhooks/sendgrid`
4. 在**要发布的事件类型**中选择所有事件：
   - **互动数据：**打开邮件、点击链接、取消订阅、垃圾邮件举报、群组取消订阅、群组重新订阅
   - **送达数据：**处理成功、失败、延迟、被退回、送达
   - **账户数据：**账户状态变更
5. 点击**“测试集成”**以验证设置——这会触发所有类型的事件通知
6. **重要提示：**点击**保存**以启用Webhook！
7. （可选）为了安全起见，启用**签名事件Webhook**并设置`SENDGRID_WEBHOOK_PUBLIC_KEY`

![SendGrid Webhook设置示例](docs/sendgrid-webhook-setup.png)

### 事件类型

| 事件 | 表情符号 | 说明 |
|-------|-------|-------------|
| 已送达 | ✅ | 邮件已送达收件人 |
| 打开 | 👀 | 收件人打开了邮件 |
| 点击 | 🔗 | 收件人点击了链接 |
| 被退回 | ⚠️ | 邮件被退回 |
| 取消订阅 | 🔕 | 收件人取消了订阅 |
| 垃圾邮件举报 | 🚨 | 邮件被标记为垃圾邮件 |

### 环境变量

```bash
SENDGRID_WEBHOOK_PUBLIC_KEY    # For signature verification (optional)
SENDGRID_WEBHOOK_MAX_AGE_SECONDS  # Max timestamp age (default: 300)
WEBHOOK_PORT                   # Server port (default: 8089)
DISCORD_WEBHOOK_URL            # Discord webhook URL
WEBHOOK_LOG_FILE               # Log file path
```

## “80,000小时”的概念

将职业生涯视为有限的资源：40年 × 每年2,000小时 = 80,000小时。

```bash
meter.py career --hours-worked 56000 --rate 85 --raise-pct 2.5
# → 12.3 years remaining, $2.4M earning potential
```