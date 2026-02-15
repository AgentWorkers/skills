---
name: linkedin-inbox
description: **LinkedIn收件箱管理工具：支持定时扫描、根据用户沟通风格自动生成回复模板以及审批工作流程**  
该工具适用于监控LinkedIn消息、起草回复、在非工作时间管理收件箱，或设置每日早晨的LinkedIn活动汇总通知。  

**主要功能：**  
1. **定时扫描**：定期自动检查LinkedIn收件箱，确保您不会错过任何重要信息。  
2. **自动回复模板**：根据用户的沟通习惯和偏好，自动生成标准化的回复模板，提高回复效率。  
3. **审批流程**：支持多级审批机制，确保回复内容经过审核后再发送给对方。  
4. **离线管理**：支持离线操作，让您在无需联网的情况下管理收件箱。  
5. **每日汇总**：每天早上自动发送LinkedIn活动摘要，帮助您快速了解当天的重要动态。  

**适用场景：**  
- 监控工作邮件和商业联系  
- 自动处理日常沟通  
- 在非工作时间管理邮件  
- 提高工作效率和响应速度  

**使用建议：**  
- 根据个人沟通风格定制回复模板  
- 设置合适的审批流程以确保回复质量  
- 利用离线功能在移动设备上管理邮件  
- 定期查看每日活动汇总以把握工作进展
---

# LinkedIn收件箱管理器

该工具可自动监控LinkedIn收件箱，并在需要时由人工审核并回复邮件。它使用Peekaboo进行用户界面自动化操作（无需遵守API使用频率限制，适用于任何LinkedIn账户）。

## 系统要求

- 安装了Peekaboo CLI的macOS系统（使用`brew install steipete/tap/peekaboo`命令安装）
- 已启用屏幕录制功能及相应的访问权限
- 通过浏览器登录LinkedIn（推荐使用Chrome浏览器）
- 确保已安装具备浏览器功能的Clawdbot

## 快速入门

### 1. 一次性设置
```bash
# Grant Peekaboo permissions
peekaboo permissions

# Verify LinkedIn is accessible
peekaboo app launch "Google Chrome"
peekaboo see --app "Google Chrome" --annotate --path /tmp/linkedin-check.png
```

### 2. 配置用户风格
在工作区创建`linkedin-inbox-config.json`文件：
```json
{
  "scan": {
    "intervalMinutes": 60,
    "activeHours": { "start": 9, "end": 18, "timezone": "America/Los_Angeles" },
    "skipWeekends": true
  },
  "drafting": {
    "styleProfile": "USER.md",
    "templates": {
      "decline": "Thanks for reaching out. Not a fit for us right now, but best of luck.",
      "interested": "This looks interesting. Happy to chat more. What's your availability?",
      "referral": "I might know someone. Let me check and get back to you."
    }
  },
  "notifications": {
    "channel": "discord",
    "target": "#linkedin"
  }
}
```

### 3. 启动监控
向代理发送命令“Start LinkedIn inbox monitoring”，或将其添加到`HEARTBEAT.md`文件中：
```markdown
- Check LinkedIn inbox if last scan >1 hour ago
```

## 核心工作流程

### 扫描收件箱
```bash
# Navigate to LinkedIn messaging
peekaboo app launch "Google Chrome"
peekaboo menu click --app "Google Chrome" --item "New Tab"
peekaboo type "https://www.linkedin.com/messaging/" --return
sleep 3

# Capture inbox state
peekaboo see --app "Google Chrome" --window-title "Messaging" --annotate --path /tmp/linkedin-inbox.png
```

代理会读取带有注释的截图，以识别以下内容：
- 未读邮件（名称以粗体显示，旁边有蓝色圆点）
- 邮件预览
- 发件人名称和邮件标题

### 起草回复
对于每封未读邮件：
1. 代理会阅读邮件内容
2. 分类邮件类型（如推销信息、社交请求、工作咨询或垃圾邮件）
3. 根据用户的沟通风格起草回复
4. 将草稿发送到通知通道等待用户审核

### 示例通知内容：
```
💼 LinkedIn: New message from **Alex M.** (Founder @ SomeCompany)

Preview: "Hi, I noticed you're growing and wondered if..."

**My read:** Services pitch. Doesn't fit current needs.

**Draft reply:**
> Thanks for reaching out. We're set on that side for now, but I'll keep you in mind if that changes.

React ✅ to send, ❌ to skip, or reply with edits.
```

### 发送审核通过的邮件
收到用户审核通过后，系统会发送邮件：
```bash
# Click into conversation
peekaboo click --on [message-element-id] --app "Google Chrome"
sleep 1

# Type response
peekaboo type "Your approved message here" --app "Google Chrome"

# Send (Enter or click Send button)
peekaboo press return --app "Google Chrome"
```

## 沟通风格匹配
该工具会读取`USER.md`文件（或用户配置的样式文件），以匹配用户的沟通风格：

**需要提取的沟通风格信息包括：**
- 文化正式程度（非正式或正式）
- 常用的问候语
- 结尾语模式
- 句子长度偏好
- 禁用的词汇/短语
- 回复内容的长度规范

**应用到草稿中时：**
- 保持与用户风格一致
- 使用用户常用的词汇
- 保持与用户相同的直接表达方式
- 遵循用户的沟通准则（避免使用过于夸张或激动的表达）

详细指导请参阅`references/style-extraction.md`文件。

## 早晨提醒功能
该工具可将LinkedIn的收件箱摘要信息整合到用户的早晨提醒中：
```markdown
📣 The Morning Ping — Monday, Jan 27

**LinkedIn:**
• 💚 Sarah Chen replied — "That sounds great, let's do Thursday" → Draft ready
• 💚 Mike R. replied — "Not interested right now" → No action needed
• 📩 3 new connection requests (2 sales pitches, 1 relevant)
• 📩 1 unread message from Alex (job inquiry) → Draft ready

Reply "send sarah" to approve, "skip mike" to archive.
```

## 审核命令
用户可以通过以下命令进行操作：
- `send [name]`：发送已起草的回复
- `send all`：发送所有待审核的草稿
- `skip [name]`：将邮件归档但不回复
- `edit [name]: [new message]`：替换草稿内容后重新发送
- `show [name]`：显示完整的邮件对话记录

## 定时扫描
### 推荐使用Cron任务进行定时扫描
```json
{
  "schedule": "0 */2 9-18 * * 1-5",
  "text": "Scan LinkedIn inbox and post any new messages to #linkedin with draft replies"
}
```

### 通过Heartbeat服务进行定时扫描
在`HEARTBEAT.md`文件中进行相关配置：
```markdown
- If 9am-6pm PT and last LinkedIn scan >60min: scan inbox, draft replies, post to #linkedin
```

## 安全规则

1. **未经明确许可，切勿发送任何邮件**——始终等待用户确认
2. **遵守使用频率限制**——每小时最多执行20次LinkedIn相关操作
3. **尊重用户的休息时间**——避免在非指定时间扫描收件箱
4. **记录所有操作**——将所有操作记录在每日日志文件中
5. **保留原始邮件**——仅将邮件归档，不删除

## 常见问题解决方法

### “找不到邮件界面”
- 确保Chrome浏览器已打开且已登录LinkedIn
- 检查窗口标题是否正确（可能因语言不同而有所差异）
- 可使用`peekaboo list windows --app "Google Chrome" --json`命令进行调试

### “会话过期”
- LinkedIn会话会定期过期，请在浏览器中重新登录
- 该工具会检测到登录页面并通知用户

### “Peekaboo权限被拒绝”
```bash
peekaboo permissions  # Check status
# Grant via System Preferences > Privacy & Security > Screen Recording + Accessibility
```

## 相关文件
- `scripts/scan_inbox.sh`：用于捕获收件箱内容的Peekaboo脚本
- `scripts/send_message.sh`：用于发送邮件的Peekaboo脚本
- `references/style-extraction.md`：关于沟通风格匹配的参考指南