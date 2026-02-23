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
| **未设置** | 询问用户的体重或目标摄入量，并询问：“您希望在水分摄入提醒的时间是什么时候？”（允许用户配置提醒时间）。然后使用 `water set_body_weight 80` 或 `water set_goal 3000` 来设置目标。不要使用固定的时间！ |
| **已设置** | 跳过设置步骤，直接记录水分摄入量或显示当前状态。 |

### 注意事项：**首次设置后不要询问**  
- 用户已经配置了提醒时间。

### 必须询问的问题  
- “您喝了多少水？”  
- 仅在用户首次设置时询问体重或目标摄入量。

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
| logged_at | 用户通知您的时间（当前时间） |
| drank_at | 用户实际喝水的时间（用户可以指定过去的时间） |
| date | 从 drank_at 推导出的日期 |
| slot | 早晨/午餐/下午/晚上/手动 |
| ml_drank | 喝入的水量（单位：毫升） |
| goal_at_time | 当前的目标摄入量 |
| message_id | 审计追踪记录——指向对应的对话记录 |

**重要规则：**  
- `drank_at` 是必填项。  
- 如果用户未指定 `drank_at`，则默认为 `logged_at`。  
- 累计摄入量是在查询时计算的（不存储在数据库中）。  
- 使用 `drank_at` 来确定记录属于哪一天。  
详细信息请参阅 [references/log_format.md](references/log_format.md)。

### 审计追踪记录

每条水分摄入记录包含以下信息：  
- **message_id**：指向用户请求记录对话的链接。  
- **自动获取**：CLI 会从会话记录中自动获取 `message_id`。  
- **查看记录**：使用 `water audit <message_id>` 可以查看记录内容及对话背景。  

```bash
# Check proof of a water entry
water audit msg_123
# Returns: entry data + surrounding messages for context
```

> ⚠️ **隐私声明**：审计功能会读取您的对话记录，但 **仅当您明确运行 `water audit <message_id>` 时才会发生**。默认情况下该功能是关闭的（`audit_auto_capture: false`）。  

> ```bash
> # Edit water_config.json and set:
> "audit_auto_capture": true
> ```  
>
> **工作原理：**  
> - 无论设置如何，水分摄入记录 **始终** 会保存 `message_id` ✅  
> - 当您运行 `water audit <message_id>` 时：  
   - 如果 `audit_auto_capture` 为 `false`，则仅显示记录数据（包含 `message_id`，不显示对话内容）；  
   - 如果 `audit_auto_capture` 为 `true`，则会显示对话内容（例如：“用户说：我喝了500毫升水”）。  

> **为什么关闭此功能？**  
> 如果您讨论敏感话题且不需要摄入量证明，可以关闭此功能。

---

## 日常命令

---

## 必须遵守的规则  
1. **始终使用 CLI** —— 不要手动计算摄入量。  
2. **先由 LLM 解释用户指令** —— 例如：“eu tomei 2 copos”（意为“我喝了2杯水”），系统会记录为500毫升。  
3. **阈值通过 CLI 设置** —— 使用 `water threshold` 命令来设置阈值，不要硬编码。  
4. **目标摄入量由用户决定** —— 体重乘以35只是默认建议值：  
   - 设置时：询问用户体重 → 提供建议目标 → **确认用户是否同意**；  
   - 体重更新时：询问用户是否要更新目标摄入量。  
   - 用户可以设置任何目标摄入量（如医生建议的摄入量、个人偏好等）。

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
**用户数据存储在代理的工作空间中，而非技能文件夹内！**  
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
| 用户自定义 | 根据用户设置的提醒时间 | `water status` |
| 默认建议时间 | 上午9点、中午12点、下午3点、下午6点、晚上9点 | `water status` |
| 动态通知 | 每30分钟 | `water dynamic` |
| 周报 | 每周日晚上8点 | `analytics week` |
| 月报 | 每月第二个晚上8点 | `analytics month` |

### 通知规则  
- **用户必须自行配置提醒时间** —— 代理应询问用户：“您希望在水分摄入提醒的时间是什么时候？”并尊重用户的设置。  
- **不要因为用户未记录摄入量就跳过通知** —— 按时发送通知。  
- **通知旨在鼓励用户记录摄入量** —— 这正是通知的目的！不要假设用户会主动记录自己的摄入情况。

---

## 快速参考

| 功能 | 命令 |
|------|---------|
| 检查进度 | `water_coach.py water status` |
| 记录摄入量 | `water_coach.py water log 500` |
| 需要更多数据？ | `water_coach.py water dynamic` |
| 身体指标 | `water_coach.py body log --weight=80` |
| 周报 | `water_coach.py analytics week` |
| 月报 | `water_coach.py analytics month` |

## 动态调度详情  
→ [references/dynamic.md](references/dynamic.md)

### ⚠️ 错误修复（2026年2月）  
- `water dynamic` 命令存在一个问题：每小时的通知计数器在时间变更时不会重置。现已修复：  
  - 脚本会检查当前时间是否与上次记录的时间不同，并相应地重置计数器。  
  - 这确保了在时间边界（例如下午4点）后通知仍能正确发送。  

### ⚠️ 错误修复（2026年2月）—— 分析功能  
- `analyticsPM → 5 week` 和 `analytics month` 命令存在问题：  
  - 之前尝试从 CSV 文件中读取不存在的 `cumulative_ml` 列；  
  - 现在改为计算每天的总摄入量（`ml_drank`）。  

### ✅ 如何生成准确的周报/月报  
**使用以下脚本：**  
- **周报**：`water_coach.py analytics week`  
- **月报**：`water_coach.py analytics month`  
这些脚本会调用 `water.py` 中的 `get_week_stats()` 和 `get_month_stats()` 函数。  

**更新分析功能时，请遵循以下规则：**  
1. **包括所有天数，即使某天的摄入量为0毫升**。  
```python
# In get_week_stats() / get_month_stats()
# Include every day in the range, not just days with data
for i in range(days):
    d = (date.today() - timedelta(days=i)).strftime("%Y-%m-%d")
    ml = by_date.get(d, {}).get("ml", 0)  # Default to 0, not skip
```  
2. **计算实际的平均摄入量**。  
```python
# Average = total_ml / ALL days (including zeros), not just tracked days
avg_ml = total_ml / days  # e.g., 15440ml / 7 days = 2205ml/day
```  
3. **以表格格式显示所有数据**。  
```python
| Dia | ML | % | Status |
| Sab 22 | 2250ml | 67.7% | ⚠️ |
| Seg 17 | 0ml | 0.0% | ❌ |
```  
这样用户可以更准确地了解自己的饮水习惯。

---

## 测试信息  
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

代理评估信息 → [evaluation/AGENT.md](evaluation/AGENT.md)