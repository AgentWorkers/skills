---
name: water-coach
description: "Hydration tracking and coaching skill. Use when user wants to track water intake, get reminders to drink water, log body metrics, or get analytics on hydration habits."
compatibility: "Requires python3, openclaw cron feature, heartbeat feature"
metadata: {"clawdbot":{"emoji":"💧"} 
  author: oristides
  version: "1.5.1"
---

# 💧 Water Coach v1.5.1



## 首次设置 [参考资料/设置.md](references/setup.md)



## 命令行界面（CLI）结构

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
| logged_at | 用户告知你的时间（当前时间） |
| drank_at | 用户实际饮水的时间（用户可以指定过去的时间） |
| date | 从 drank_at 推导出的日期 |
| slot | 早餐/午餐/下午/晚上/手动 |
| ml_drank | 饮用的水量（单位：毫升） |
| goal_at_time | 当前的饮水目标 |
| message_id | 审计追踪记录——指向相关对话的链接 |

**重要规则：**
- **drank_at 是必填项**——必须提供
- 如果用户未指定 drank_at，则默认为 logged_at
- **累计饮水量在查询时计算**（不存储在数据库中）
- 使用 drank_at 来确定计入当天的饮水量

详情请参阅 [参考资料/日志格式.md](references/log_format.md)

### 审计追踪记录

每次饮水记录会包含以下信息：
- **message_id**：指向用户请求记录对话的链接
- **自动捕获**：CLI 会从会话记录中自动获取 message_id
- **查询证明**：使用 `water audit <message_id>` 可以查看记录内容及对话上下文

```bash
# Check proof of a water entry
water audit msg_123
# Returns: entry data + surrounding messages for context
```

> ⚠️ **隐私声明**：审计追踪功能会读取您的对话记录，以便将饮水记录与对话内容关联起来。默认情况下，此功能是 **禁用的**（`audit_auto_capture: false`）。若需启用，请按照以下步骤操作：
> 
> ```bash
> # Edit water_config.json and set:
> "audit_auto_capture": true
> ```
> 
> **为什么要启用此功能？** 如果您需要用于医疗或法律目的的饮水记录证明，该功能可以提供显示您何时饮水的对话上下文。
> 
> **为什么要禁用此功能？** 如果您在聊天中讨论敏感内容，可能不希望这些内容被该工具读取。



---

## 日常命令

```bash
# Water
water status                                      # Current progress (calculated from drank_at)
water log 500                                    # Log intake (drank_at = now)
water log 500 --drank-at=2026-02-18T18:00:00Z  # Log with past time
water log 500 --drank-at=2026-02-18T18:00:00Z --message-id=msg_123
water dynamic                                    # Check if extra notification needed
water threshold                                  # Get expected % for current hour
water set_body_weight 80                        # Update weight + logs to body_metrics
water set_body_weight 80 --update-goal          # + update goal
water audit <message_id>                        # Get entry + conversation context

# Body
body log --weight=80 --height=1.75 --body-fat=18
body latest          # Get latest metrics
body history 30     # Get history

# Analytics
analytics week       # Weekly briefing (Sunday 8pm)
analytics month     # Monthly briefing (2nd day 8pm)
```



## 必须遵守的规则

1. **始终使用 CLI**——切勿手动计算饮水量
2. **先由 LLM 解释用户指令**——例如：“eu tomei 2 copos”（我喝了2杯水） → 系统会记录为饮用500毫升水
3. **饮水目标由用户自行设定**——“weight × 35”只是一个默认建议：
   - 设置时：询问用户体重 → 建议饮水目标 → **与用户确认**
   - 体重更新时：询问“是否要将目标更新为新的建议值？”
   - 用户可以设定任意目标（如医生建议的饮水量等）



## 配置结构

```
water-coach/
├── SKILL.md              ← You are here
├── scripts/
│   ├── water_coach.py   ← Unified CLI
│   └── water.py         ← Core functions
├── data/
│   ├── water_config.json (Current configs)
│   ├── water_log.csv
│   └── body_metrics.csv
└── references/
    ├── setup.md
    ├── dynamic.md
    └── log_format.md
```



## 通知安排

| 通知类型 | 通知时间 | 命令 |
|------|------|---------|
| 基本通知（每天5次） | 上午9点、中午12点、下午3点、下午6点、晚上9点 | 显示饮水状态 |
| 动态通知 | 每约30分钟 | 显示实时饮水情况 |
| 周报 | 每周日晚上8点 | 提供每周饮水分析 |
| 月报 | 每月第二天晚上8点 | 提供每月饮水分析 |

---

## 快速参考

| 功能 | 命令 |
|------|---------|
| 查看进度 | `water_coach.py water status` |
| 记录饮水量 | `water_coach.py water log 500` |
| 需要更多信息？ | `water_coach.py water dynamic` |
| 体成分析 | `water_coach.py body log --weight=80` |
| 查看周报 | `water_coach.py analytics week` |
| 查看月报 | `water_coach.py analytics month` |

## 动态调度详情 → [参考资料/动态调度.md](references/dynamic.md)



## 测试

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



代理评估 → [评估/代理.md](evaluation/AGENT.md)