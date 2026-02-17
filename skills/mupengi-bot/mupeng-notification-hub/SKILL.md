---
name: notification-hub
description: 统一通知中心：收集所有技能相关的警报信息，并根据优先级进行推送。
author: 무펭이 🐧
---
# notification-hub

**通知集成** — 集中收集所有技能相关的通知，并根据优先级进行分发，以减少用户收到的通知疲劳。

## 🎯 目的

集中管理来自各种技能的通知，并根据其重要性，在适当的时间和渠道进行推送。

## 📥 通知来源

从 `events/` 目录中收集所有事件文件：

```
events/
  ├── health-2026-02-14.json         (health-monitor)
  ├── scrape-result-2026-02-14.json  (data-scraper)
  ├── dm-check-2026-02-14.json       (insta-post)
  ├── competitor-2026-02-14.json     (competitor-watch)
  └── workflow-2026-02-14.json       (skill-composer)
```

## 🚦 优先级过滤

### 1. `紧急` — 立即通过 Discord 私信发送

**条件：**
- 安全问题（异常登录、可疑访问）
- 系统错误（OpenClaw 停止运行、浏览器断开连接）
- 费用超出限制（API 使用量超过 90%）
- 关键性提及

**发送方式：**
- 通过 Discord 私信（`TOOLS.md` 中配置的频道 ID）
- 立即发送（1 分钟内）

**示例：**
```
🚨 Urgent: Browser disconnected
Port 18800 not responding. Auto-recovery attempted but failed.
Manual check needed: openclaw browser start
```

### 2. `重要` — 包含在下次心跳更新中

**条件：**
- 新的 Instagram 私信（未读）
- 检测到热门关键词的突然增加
- 竞争对手发布了新服务
- 需要推送 Git 提交（有 10 条或更多未提交的更改）

**发送方式：**
- 包含在下次心跳更新中（约 30 分钟间隔）
- 将多个通知合并成一条消息发送

**示例：**
```
📢 3 Updates

📩 2 Instagram DMs (iam.dawn.kim, partner_xyz)
📈 Trend: "AI agent" surging (+150%)
🔄 Git: 12 commits waiting for push
```

### 3. `信息` — 仅包含在每日报告中

**条件：**
- 定期统计更新
- 每日令牌使用情况
- 完成的工作流程
- 一般系统日志

**发送方式：**
- 在每日报告技能执行时包含这些通知
- 每日发送一次汇总

**示例：**
```
📊 Daily Report (2026-02-14)

✅ 3 workflows completed
📊 Tokens: 45,230 / 100,000 (45%)
📝 Memory: 3.2 GB
🔧 Health check: OK
```

## 🔕 避免重复发送

同一事件不会被重复发送多次。

### 重复检测

```json
{
  "event_id": "health-check-2026-02-14-07:00",
  "fingerprint": "sha256(source + type + key_data)",
  "notified_at": "2026-02-14T07:05:00+09:00"
}
```

### 历史记录存储

**文件结构：`sent-YYYY-MM-DD.json`**

**发送方式：**
```json
{
  "date": "2026-02-14",
  "notifications": [
    {
      "id": "health-check-2026-02-14-07:00",
      "priority": "info",
      "sent_at": "2026-02-14T07:05:00+09:00",
      "channel": "discord_dm",
      "source": "health-monitor"
    }
  ]
}
```

## 📢 发送渠道

### Discord 私信
- **频道 ID**：在 `TOOLS.md` 中配置
- **用途**：发送紧急和重要的通知
- **格式**：Markdown 格式（包含表情符号、标题和内容）

### 心跳更新
- **用途**：汇总重要通知
- **格式**：简洁的列表形式

### 每日报告
- **用途**：汇总信息通知
- **格式**：结构化的内容组织

## 🎤 触发方式

使用以下关键词激活相关技能：
- "notification settings"
- "notification"
- "check notifications"
- "anything new"

## 🚀 使用示例

### 检查通知
```
"Anything new?"
→ Immediately summarize important+ notifications
```

### 通知设置
```
"Set Instagram DMs to immediate notification"
→ Promote dm-check events to urgent
```

### 通知历史记录
```
"Show today's notification history"
→ Read memory/notifications/sent-2026-02-14.json
```

## ⚙️ 实施指南

### 1. 收集事件
```javascript
// Scan events/ directory
const events = fs.readdirSync('events/')
  .filter(f => f.endsWith('.json'))
  .map(f => JSON.parse(fs.readFileSync(`events/${f}`)));
```

### 2. 按优先级分类
```javascript
const urgent = events.filter(e => e.priority === 'urgent');
const important = events.filter(e => e.priority === 'important');
const info = events.filter(e => e.priority === 'info');
```

### 3. 检查重复通知
```javascript
const sent = loadSentHistory(today);
const newEvents = events.filter(e => 
  !sent.notifications.some(n => n.id === e.id)
);
```

### 4. 发送通知
```javascript
// urgent → Immediate Discord DM
if (urgent.length > 0) {
  await sendDiscordDM(urgent);
}

// important → Add to heartbeat queue
if (important.length > 0) {
  await addToHeartbeatQueue(important);
}

// info → Add to daily-report queue
if (info.length > 0) {
  await addToDailyReportQueue(info);
}
```

### 5. 保存历史记录
```javascript
saveSentHistory(today, newlySentNotifications);
```

## 📊 事件优先级指南

指导每个技能在创建事件时添加 `priority` 字段：

```json
{
  "timestamp": "2026-02-14T07:58:00+09:00",
  "skill": "health-monitor",
  "priority": "urgent",  // urgent | important | info
  "message": "Browser disconnected",
  "data": { ... }
}
```

---

> 🐧 由 **무펭이** 开发 — [Mupengism](https://github.com/mupeng) 生态系统技能