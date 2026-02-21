---
name: water-coach
description: "Hydration tracking and coaching skill. Use when user wants to track water intake, get reminders to drink water, log body metrics, or get analytics on hydration habits."
compatibility: "Requires python3, openclaw cron feature, heartbeat feature"
metadata: {"clawdbot":{"emoji":"💧"} 
  author: oristides
---

# 💧 水分管理助手

## 首次设置

请按照 [references/setup.md](references/setup.md) 中的步骤进行首次设置。

---

## 其他代理应如何与本助手交互

### 首次设置后的检查
```bash
water setup
```

| 设置状态 | 应该执行的操作 |
|----------|-------------|
| **未设置** | 询问用户的体重或目标摄入量，并询问：“您希望在水分提醒的时间是什么时候？”（让用户自行配置时间安排）。然后使用 `water set_body_weight 80` 或 `water set_goal 3000` 来设置目标。切勿使用硬编码的时间！ |
| **已设置** | 跳过设置步骤，直接记录用户的饮水情况或显示当前状态。 |

### 注意事项
- 在首次设置之后，**不要再次询问用户的提醒时间**（因为用户已经配置好了）。

### 必须询问的问题
- “您喝了多少水？”
- 仅询问体重或目标摄入量（在首次设置时）。

---

## 命令行接口（CLI）结构
```bash
water_coach.py <namespace> <command> [options]
```

命名空间：`water` | `body` | `analytics`

---

## 数据格式

### CSV 格式
```
logged_at,drank_at,date,slot,ml_drank,goal_at_time,message_id
```

| 列名 | 说明 |
|--------|-------------|
| logged_at | 用户告知您的时间（当前时间） |
| drank_at | 用户实际饮水的时间（用户可以指定过去的时间） |
| date | 从 drank_at 推导出的日期 |
| slot | 早晨/午餐/下午/晚上/手动 |
| ml_drank | 饮水量（单位：毫升） |
| goal_at_time | 当前的目标摄入量 |
| message_id | 审计记录的链接（指向相关对话记录） |

**重要规则：**
- **drank_at 是必填项** - 必须记录用户实际饮水的时间。
- 如果用户未指定 drank_at，则默认使用 logged_at。
- **累计摄入量是在查询时计算的**（不会被存储）。
- 使用 drank_at 来确定记录属于哪一天。

详细信息请参阅 [references/log_format.md](references/log_format.md)。

### 审计记录

每次饮水记录都会包含以下信息：
- **message_id**：指向用户请求记录对话的链接。
- **自动捕获**：CLI 会从会话记录中自动获取 message_id。
- **查看记录**：可以使用 `water audit <message_id>` 来查看记录内容及对话上下文。

```bash
# Check proof of a water entry
water audit msg_123
# Returns: entry data + surrounding messages for context
```

> ⚠️ **隐私声明**：审计功能可以读取您的对话记录，但**仅当您明确执行 `water audit <message_id>` 时才会进行读取**。默认情况下，此功能是关闭的（`audit_auto_capture: false`）。

---
> **工作原理：**
- **无论设置如何，饮水记录** **总会保存 message_id** ✅
- 当您执行 `water audit <message_id>` 时：
  - 如果 `audit_auto_capture` 为 `false`，则仅显示记录数据（保存 message_id，不显示对话内容）。
  - 如果 `audit_auto_capture` 为 `true`，则会同时显示记录内容和对话上下文（例如：“用户说：我喝了500毫升水”）。

> **为什么关闭此功能？** 如果您讨论的是敏感话题，并且不需要摄入量的证明，可以关闭此功能。

---

## 日常命令

---

## 必须遵守的规则
1. **始终使用命令行接口（CLI）**，切勿手动计算数据。
2. **首先由大型语言模型（LLM）进行解析**——例如：“eu tomei 2 copos”（意为“我喝了2杯水”）→ 系统会记录为500毫升。
3. **阈值通过 CLI 设置**，切勿硬编码。
4. **目标摄入量由用户自行选择**——体重 × 35 只是一个默认建议：
   - 在设置时：询问用户的体重 → 提出建议的目标摄入量 → **请用户确认**。
   - 当体重发生变化时：询问用户是否希望将目标摄入量更新为新的建议值。
   - 用户可以设置任何目标摄入量（例如医生的建议、个人偏好等）。

---

## 配置文件结构
```
water-coach/
├── SKILL.md              ← You are here
├── scripts/
│   ├── water_coach.py   ← Unified CLI
│   └── water.py         ← Core functions
├── data/                 ← DO NOT USE - keep skill code separate from user data
└── references/
    ├── setup.md
    ├── dynamic.md
    └── log_format.md
```

### 注意：数据存储位置
**用户数据存储在代理的工作空间中，而不是技能文件夹中！**

| 数据类型 | 存储位置 |
|------|----------|
| water_log.csv | `<agent-workspace>/memory/data/water_log.csv` |
| water_config.json | `<agent-workspace>/memory/data/water_config.json` |
| body_metrics.csv | `<agent-workspace>/memory/data/body_metrics.csv` |

示例路径：`/home/oriel/.openclaw/workspace/memory/data/`

**原因：** 将用户数据与技能代码分开存储，便于备份、迁移和更新技能功能。

---

## 通知安排

| 通知类型 | 通知时间 | 执行命令 |
|------|------|---------|
| 用户自定义 | 根据用户的日程安排 | 显示水分摄入状态 |
| 默认建议 | 上午9点、中午12点、下午3点、下午6点、晚上9点 | 显示水分摄入状态 |
| 动态通知 | 每30分钟（心跳检测） | 发送动态通知 |
| 周报 | 每周日晚上8点 | 提供每周的水分摄入分析报告 |
| 月报 | 每月第二天晚上8点 | 提供每月的水分摄入分析报告 |

### 通知规则
- **用户必须自行配置通知时间**——代理应询问用户：“您希望在水分提醒的时间是什么时候？”并尊重用户的设置。
- **即使用户未记录饮水情况，也必须发送通知**。
- **通知旨在鼓励用户记录饮水行为**——这是设置通知的目的，不要因为用户未记录饮水就忽略通知。

---

## 快速参考

| 功能 | 命令 |
|------|---------|
| 查看进度 | `water_coach.py water status` |
| 记录饮水情况 | `water_coach.py water log 500` |
| 需要更多数据？ | `water_coach.py water dynamic` |
| 体成分析 | `water_coach.py body log --weight=80` |
| 周报 | `water_coach.py analytics week` |
| 月报 | `water_coach.py analytics month` |

## 动态调度详情 → [references/dynamic.md](references/dynamic.md)

## 测试内容
```bash
python3 -m pytest skills/water-coach/scripts/test/test_water.py -v
```

## 示例
```
User: "eu tomei 2 copos"
Agent: (LLM interprets: 2 copos ≈ 500ml)
Agent: exec("water_coach.py water log 500")
→ Python logs to CSV
```

代理的评估信息 → [evaluation/AGENT.md](evaluation/AGENT.md)