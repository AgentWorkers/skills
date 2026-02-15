# 频道提醒

这是一个用于通过 cron 作业创建提醒并在 Telegram 中发送通知的技能。

---

## ⚠️ 使用前请务必检查以下要求

### 1. 必须启用 Heartbeat 功能

在 `~/.openclaw/openclaw.json` 文件中，请检查以下内容：

```json
{
  "agents": {
    "defaults": {
      "heartbeat": {
        "every": "5m",      // ← НЕ должен быть "0m" или отсутствовать
        "target": "last"    // ← Куда отправлять ответы
      }
    }
  }
}
```

如果 `heartbeat.every` 的值为 "0m" 或该字段不存在，那么提醒功能将无法正常工作！

### 2. HEARTBEAT.md 文件中必须包含相关指令

在 `HEARTBEAT.md` 文件中，**必须** 添加用于处理提醒的指令：

```markdown
### Напоминания (systemEvent)

Когда получаешь systemEvent с напоминанием (обычно содержит ⏰, 📅, 💰, 📞, ✅, 🔔, 💊, 🏃 и т.д.) — передай его пользователю в Telegram.

**Пример:**
- Получено: `⏰ НАПОМИНАНИЕ: оплатить интернет`
- Ответ в Telegram: `💰 Напоминаю: пора оплатить интернет!`

Просто доставь напоминание без лишних комментариев.
```

### 3. cron 作业中的 `wakeMode` 设置为 "now"

请始终将 `wakeMode` 设置为 "now"，以确保 heartbeat 能够立即执行：

```json
{
  "sessionTarget": "main",
  "wakeMode": "now",    // ← ОБЯЗАТЕЛЬНО для немедленного срабатывания
  "payload": { ... }
}
```

否则，提醒将会等待下一次 heartbeat（最长等待时间为 5 分钟）。

---

## 安装完成后：进行测试

安装该技能后，请务必与用户一起测试所有功能：

### 第一步：测试简单的提醒功能（主代理）

```
Поставь тестовое напоминание через 1 минуту
```

### 第二步：通过 message 工具进行测试（如果有多个机器人）

```
Отправь тестовое сообщение через message tool
```

### 第三步：确定最佳方案

测试完成后，请记录下哪种方式最有效：

**示例：在 `MEMORY.md` 或 `memory/YYYY-MM-DD.md` 文件中记录结果：**
```markdown
## Напоминания

**Рабочий подход:** sessionTarget: "main" + systemEvent + wakeMode: "now"
**Проверено:** 2026-02-14
**Chat ID пользователя:** 7977422300
```

### 如果测试失败，请检查以下内容：
1. ✅ Heartbeat 功能已启用（`heartbeat.every` 的值不等于 "0m"）
2. ✅ HEARTBEAT.md 文件中包含提醒处理指令
3. ✅ cron 作业中的 `wakeMode` 设置为 "now"
4. ✅ Telegram 频道已配置并正常运行

---

## 快速启动指南

### 对于主代理（MAIN Agent）

```json
{
  "name": "Напоминание",
  "schedule": { "kind": "at", "at": "2026-02-14T15:00:00+03:00" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "⏰ НАПОМИНАНИЕ: текст напоминания"
  }
}
```

主代理会接收到 systemEvent，然后触发 heartbeat 功能，随后代理会在聊天中回复用户。

---

### 对于非主代理（Semen、Andrey、Hristofor、Discussions）

**请使用以下方案：** 主代理 + message 工具

```json
{
  "agentId": "main",
  "name": "Напоминание от Semen",
  "schedule": { "kind": "at", "at": "2026-02-14T15:00:00+03:00" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "📤 ОТПРАВИТЬ НАПОМИНАНИЕ:\naccountId: semen\ntarget: 7977422300\nmessage: 🤗 текст напоминания"
  }
}
```

**工作原理如下：**
1. cron 作业触发 → 主代理的 session 收到 systemEvent
2. 主代理在 `HEARTBEAT.md` 文件中看到 “发送提醒” 的指令
3. 主代理解析 `accountId`、`target` 和 `message` 参数
4. 主代理使用 `message` 工具向指定的 `accountId` 发送提醒信息
5. 用户会收到来自非主代理机器人的通知

---

## 所需数据

### 用户的 Telegram 聊天 ID

**获取方式：**
```bash
curl "https://api.telegram.org/bot<BOT_TOKEN>/getUpdates" | jq '.result[].message.chat.id'
```

**或者从消息元数据中获取**：在 Telegram 消息的标题中可以看到 `id:XXXXXXXX`。

### 每个代理的 AccountId

| 代理 | AccountId |
|-------|-----------|
| John Zoydberg (main) | main |
| Semen | semen |
| Andrey | andrey |
| Hristofor | hristofor |
| Discussions | discussions |

---

## 日程类型

### 一次性提醒（at）

```json
{ "kind": "at", "at": "2026-02-14T15:00:00+03:00" }
```

⚠️ **请务必指定时区！** 如果未指定时区，系统将使用 UTC 时区。

### 定期提醒（cron）

```json
{ "kind": "cron", "expr": "0 9 * * *", "tz": "Europe/Moscow" }
```

| 表达式 | 含义 |
|-----------|----------|
| `0 9 * * *` | 每天 9:00 |
| `0 9 * * 1-5` | 工作日 9:00 |
| `0 18 * * 5` | 每周五 18:00 |
| `0 */2 * * *` | 每隔 2 小时 |

### 间隔时间（every）

```json
{ "kind": "every", "everyMs": 3600000 }
```

| 间隔时间（毫秒） | 对应的 cron 表达式 |
|----------|--------------|
| 5 分钟 | `0 9 * * *` |
| 1 小时 | `0 18 * * *` |
| 24 小时 | `0 */2 * * *` |

---

## 示例

### 主代理：10 分钟后发送提醒

```json
{
  "name": "Напоминание через 10 мин",
  "schedule": { "kind": "at", "at": "<текущее время + 10 мин>" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "⏰ НАПОМИНАНИЕ: проверить почту"
  }
}
```

### Semen：每日提醒

```json
{
  "agentId": "main",
  "name": "Утреннее напоминание от Semen",
  "schedule": { "kind": "cron", "expr": "0 9 * * *", "tz": "Europe/Moscow" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "📤 ОТПРАВИТЬ НАПОМИНАНИЕ:\naccountId: semen\ntarget: 7977422300\nmessage: 🤗 Доброе утро! Проверь задачи на сегодня."
  }
}
```

### Hristofor：支付提醒

```json
{
  "agentId": "main",
  "name": "Оплата интернета",
  "schedule": { "kind": "at", "at": "2026-02-25T10:00:00+03:00" },
  "sessionTarget": "main",
  "wakeMode": "now",
  "payload": {
    "kind": "systemEvent",
    "text": "📤 ОТПРАВИТЬ НАПОМИНАНИЕ:\naccountId: hristofor\ntarget: 7977422300\nmessage: 💰 Напоминание: оплатить интернет до 28 февраля"
  }
}
```

---

## 提醒管理

### 查看所有提醒

```
cron list
```

### 删除提醒

```
cron remove jobId: "uuid"
```

### 关闭/启用提醒功能

```
cron update jobId: "uuid" patch: { enabled: false }
cron update jobId: "uuid" patch: { enabled: true }
```

---

## 非主代理的 systemEvent 格式

```
📤 ОТПРАВИТЬ НАПОМИНАНИЕ:
accountId: <accountId бота>
target: <Chat ID пользователя>
message: <текст напоминания с эмодзи>
```

**不同代理使用的表情符号：**
| 表情符号 | 代理类型 |
|--------|-------|
| 🤗 | Semen |
| 🧑💻 | Andrey |
| 💰 | Hristofor |
| 💬 | Discussions |

---

## 主代理的 HEARTBEAT.md 配置

### 检查

在使用该技能之前，请确保主代理的 `HEARTBEAT.md` 文件中包含 “发送提醒” 的指令。

**检查文件路径：** `~/.openclaw/workspace-main/HEARTBEAT.md`

**查找相关内容：**
```markdown
### Напоминания от других агентов (📤 ОТПРАВИТЬ НАПОМИНАНИЕ)
```

### 如果缺少该内容，请添加：

```markdown
### Напоминания от других агентов (📤 ОТПРАВИТЬ НАПОМИНАНИЕ)

Когда получаешь systemEvent с `📤 ОТПРАВИТЬ НАПОМИНАНИЕ:` — это запрос от НЕ-main агента отправить сообщение через их бота.

**Формат:**
\`\`\`
📤 ОТПРАВИТЬ НАПОМИНАНИЕ:
accountId: semen
target: 7977422300
message: 🤗 текст напоминания
\`\`\`

**Действие:** Используй `message` tool:
\`\`\`json
{
  "action": "send",
  "channel": "telegram",
  "accountId": "<accountId из systemEvent>",
  "target": "<target из systemEvent>",
  "message": "<message из systemEvent>"
}
\`\`\`

Ничего больше не отвечай после отправки (NO_REPLY).
```

**工作原理：**
当主代理收到 systemEvent 时，它会：
1. 从文本中解析 `accountId`、`target` 和 `message` 参数
2. 使用 `message` 工具发送相应的提醒信息
3. 通知会从指定的 `accountId` 发送，不会重复发送到主代理的聊天中

---

## 该方案为何有效：
1. **主代理具有稳定的 heartbeat 功能**，确保所有 systemEvent 都能被处理
2. **message 工具已验证可用**（通过 CLI 和工具调用测试）
3. `accountId` 被正确路由，确保信息来自正确的机器人
4. `target` 参数指定了接收提醒的用户（即用户的 Telegram 聊天 ID）

---

## 替代方案：直接使用 message 工具发送通知

如果代理需要立即发送通知（而非按照预定时间），可以采取以下方法：

```json
{
  "action": "send",
  "channel": "telegram",
  "accountId": "semen",
  "target": "7977422300",
  "message": "🤗 Текст сообщения"
}
```

该方法适用于所有能够使用 `message` 工具的代理。