---
name: Personality Engine
description: "这是一个六系统行为引擎，能够让任何 OpenClaw 代理都“活”起来（即具备动态交互能力）。编辑功能可以插入用户的观点；系统能够智能地选择何时保持沉默；通过时间感知来调整信息的紧急程度；微小的交互动作会发送环境提示信号；上下文缓冲区允许用户回溯之前的消息；响应跟踪机制会根据用户的互动模式进行动态调整。该引擎具有跨领域适用性，可以用于交易代理、个人助手、DevOps 监控工具或任何需要主动交互的系统中。它是 OpenClaw 预测市场交易栈（OpenClaw Prediction Market Trading Stack）的一部分，并配备了默认的交易配置。"
---
# 人格引擎 — 6个系统行为框架

**目标**：让任何AI代理都感受到“生命力”——拥有观点、意识、判断力、记忆力、时间感知能力以及互动敏感度。该框架适用于交易代理、通知系统、个人助手或任何主动型代理，而不仅仅是数据传递。

## 架构概述

```
Trigger fires → engine.py orchestrator
              ↓
         selective_silence (should we stay silent?)
              ↓
         urgency_compute (how urgent is this 0.0-1.0?)
              ↓
         engagement_modifier (adjust for user response patterns)
              ↓
         variable_timing (schedule delivery based on urgency + time of day)
              ↓
         context_buffer (add back-references to earlier messages today)
              ↓
         editorial_voice (inject personality / opinions)
              ↓
         dedup (avoid repeats within rolling window)
              ↓
         send → iMessage (or other transport)
```

另外两个环境系统：
- **micro_initiations**：在满足条件时自动发送提示信息（例如市场平静、表现良好或检测到用户缺席）
- **response_tracker**：监控用户的互动情况；调整信息的紧急程度并建议进行优化

---

## 系统1：编辑语音 — 观点注入

**功能**：每种触发类型都会生成特定的语音内容，这些内容会根据市场状态、投资组合的盈亏情况以及信号的可靠性而变化。

**针对不同触发类型的语音池**：

### 跨平台（Kalshi与Polymarket的差异）
- **牛市差异（>5%）**：“市场出现显著差异。其中一个市场可能存在问题。”
- **轻微差异（2-5%）**：“市场出现轻微差异。目前尚无紧急情况。”
- **差异过时（超过6小时）**：“差异已经过时——市场可能已经重新定价。”

### 投资组合（用户持仓表现）
- **+15%或更高**：“今天表现不错。投资组合表现良好。”
- **+5%至+15%**：“收益稳定。”
- **-5%至+5%**：“市场表现平稳。”
- **-5%至-15%**：“市场处于波动期。请检查止损策略。”
- **-15%或更差**：“今天市场表现不佳。请做好应对波动的准备。”

### xsignals（社交信号扫描器）
- **置信度≥0.85且与持仓匹配**：“信号可靠。值得关注。”
- **置信度0.70-0.85**：“[主题]有新的信号。值得观察。”
- **置信度<0.70**：“信号不可靠。”

### edge（Kalshi边缘检测）
- **边缘大于3%**：“边缘明显。值得深入分析。”
- **边缘1-3%**：“边缘较微弱。保持关注。”
- **边缘小于1%**：“边缘不明显。无需特别关注。”

### 早晨（每日简报）
- **周一**：“新的一周开始了。以下是市场概况。”
- **周五**：“周五总结。收盘前需要了解的信息。”
- **其他时间**：“每日摘要。”

### 冲突（同一时间有多个触发事件）
- **2个或更多冲突**：“明天市场可能混乱。多个信号同时触发。”
- **较轻的冲突**：“注意——多个事件同时发生。”

**自定义点**：通过扩展`editorial_voice.py`中的`VOICE_POOLS`字典来添加新的触发类型。每个条目包含`(触发名称, 市场状态)` → 观点字符串列表。

---

## 系统2：选择性沉默 — 知道何时不应发送信息

**功能**：并非所有触发事件都值得发送消息。明确的沉默机制表示：“跳过了简报——没有值得关注的内容。”

**针对每个触发事件的内容质量检查**：
- **morning_is_boring**：如果市场波动率<0.5%，没有差异，也没有明显的市场趋势 → 跳过
- **divergence_is_stale**：如果上一个关于该主题的消息是在3小时前发布的，并且价差没有变化超过0.5% → 跳过
- **signals_are_noise**：如果所有信号的置信度<0.65且没有与持仓匹配 → 跳过
- **edge_is_weak**：如果所有边缘的幅度<1% → 跳过
- **portfolio_is_flat**：如果每日盈亏在-2%至+2%之间且没有重大持仓变化 → 跳过

**沉默频率**：
- 每用户每天最多发送1条沉默消息
- 仅针对预期的触发事件（如早晨简报、投资组合检查等）
- 绝不沉默micro_initiations（这些信息是有价值的）
- 沉默时发送明确消息：“跳过了简报——没有值得关注的内容。”

**自定义点**：在`selective_silence.py`中调整阈值：
```python
SILENCE_THRESHOLDS = {
    'vol_floor': 0.5,           # % vol threshold for morning silence
    'divergence_age_limit': 3,  # hours
    'signal_confidence_floor': 0.65,
    'edge_floor': 1.0,          # %
    'portfolio_flat_range': 2.0 # % P&L range
}
```

---

## 系统3：动态时间安排 — 紧急程度评分 + 时间感知

**功能**：根据信息的紧急程度（0.0-1.0）和一天中的时间来安排消息的发送。早上6点的轻微差异会立即发送（紧急程度阈值0.9），而晚上10点的相同差异则会被延迟发送（紧急程度阈值0.35）。

**针对不同触发类型的紧急程度计算**：
- **跨平台**：（价差 / 10%）× 0.6，最高限制为1.0
  - 5%价差 = 0.3紧急程度
  - 10%价差 = 0.6紧急程度
  - 15%以上价差 = 1.0紧急程度
- **投资组合**：（每日盈亏的绝对值 / 10%）× 0.7，最高限制为1.0
  - ±5%盈亏 = 0.35紧急程度
  - ±15%盈亏 = 1.0紧急程度
- **xsignals**：（置信度 × 0.8）+（持仓是否匹配 × 0.2），最高限制为1.0
  - 置信度0.85且与持仓匹配 = 0.88紧急程度
  - 置信度0.70且没有匹配 = 0.56紧急程度
- **edge**：（边缘幅度 / 5%）× 0.8，最高限制为1.0
  - 2%边缘 = 0.32紧急程度
  - 5%边缘 = 0.8紧急程度
- **会议**：（会议距离 / 120分钟）× 0.75，最高限制为1.0
  - 30分钟后会议 = 0.75紧急程度
  - 5分钟后会议 = 0.96紧急程度

**一天中不同时间的发送阈值**：
- **早上7点之前**：阈值0.90（几乎所有消息都会发送）
- **早上7点至9点**：阈值0.75（早晨高峰期）
- **早上9点至晚上10点**：阈值0.45（白天时段）
- **晚上10点至11点**：阈值0.35（接近尾声）
- **晚上11点至午夜**：阈值0.85（深夜时段）
- **午夜至早上7点**：阈值0.90（睡眠时间）

**调整因素**：
- **周末**：紧急程度增加0.10（周末用户互动较少，降低发送频率）
- **防止信息重复**：如果消息发送时间小于10分钟，则紧急程度降低0.20（分散发送时间）
- **每日疲劳**：如果今天收到10条以上消息，则紧急程度增加0.20（用户可能疲劳，减少消息数量但提高信息质量）
- **随机波动**：紧急程度增加或减少±5%（避免过于精确）

**发送逻辑**：
```
adjusted_urgency = base_urgency * engagement_modifier ± jitter
if adjusted_urgency >= time_of_day_threshold:
    schedule_send(now or delayed based on urgency)
else:
    hold for next trigger
```

**自定义点**：在`variable_timing.py`中修改`TIME_OF_DAY_THRESHOLDS`和调整因子：
```python
TIME_OF_DAY_THRESHOLDS = {
    (0, 7): 0.90,    # midnight - 7 AM
    (7, 9): 0.75,    # 7 - 9 AM
    (9, 22): 0.45,   # 9 AM - 10 PM
    (22, 23): 0.35,  # 10 - 11 PM
    (23, 24): 0.85,  # 11 PM - midnight
}
MODIFIERS = {
    'weekend': 0.10,
    'clustering_prevention': 0.20,
    'daily_fatigue_step': 0.20,
}
```

---

## 系统4：micro-Initiations — 自动环境提示信息

**功能**：在满足条件时自动发送提示信息。这些信息不是由市场事件触发，而是由系统的整体状态触发。

**提示信息池**：
| 池 | 触发条件 | 信息内容 |
|------|---------|---------|
| QUIET_MARKET | 全天市场波动率<0.3%，无交易 | “市场平静。市场处于休眠状态。” |
| WEEKEND | 星期六/星期日，无会议 | “周末模式。你可以休息了。” |
| MONDAY | 星期一早上6点，新的一周开始 | “周一早上。新的一周开始了。” |
| FRIDAY | 星期五下午4点，市场即将收盘 | “周五收盘。周末愉快。” |
| HOLIDAY_AWARENESS | 今天是美国节假日 | “今天是节假日。市场活动较少。” |
| GOOD_STREAK | 连续5天以上盈利 | “表现良好。本周对你来说是个好时机。” |
| BAD_STREAK | 连续5天以上亏损 | “近期表现不佳。情况会好转的。” |
| ABSENCE | 24小时以上用户无互动 | “正在检查你的情况。市场比较平静。” |

**发送频率**：
- 每用户每周最多发送2条提示信息
- 在繁忙的日子跳过（当天已经发送了3条以上提示信息）
- 两周内不重复发送（使用`sha256(pool + date)`进行去重）

**美国节假日日历**（内置提示信息）：
```python
HOLIDAYS = {
    (1, 1): "New Year's Day",
    (1, 20): "MLK Day",
    (2, 17): "Presidents' Day",
    (3, 17): "St. Patrick's Day",
    (5, 26): "Memorial Day",
    (7, 4): "Independence Day",
    (9, 1): "Labor Day",
    (10, 13): "Columbus Day",
    (11, 11): "Veterans Day",
    (11, 27): "Thanksgiving",
    (12, 25): "Christmas",
}
```

**自定义点**：在`micro_initiations.py`中添加新的提示信息池：
```python
MICRO_POOLS = {
    'QUIET_MARKET': {
        'condition': lambda ctx: ctx.vol < 0.3 and ctx.trade_count == 0,
        'messages': ["Quiet day. Markets are sleeping.", "No action today."],
    },
    'YOUR_POOL': {
        'condition': lambda ctx: your_logic_here(),
        'messages': ["Message 1", "Message 2"],
    }
}
```

---

## 系统5：上下文缓冲区 — 日记记录与引用

**功能**：消息可以引用当天之前的信息。例如：“我早上9点标记的Kalshi/PM差异扩大到了15%。”这会让代理感受到自己在“思考”过去的事件，而不仅仅是简单地发送警报。

**针对不同触发事件的引用生成**：
- **跨平台**：如果之前已经标记了差异，比较当前的价差与之前的价差
- **投资组合**：如果之前有关于投资组合的消息，显示自那以后的变化
- **xsignals**：如果之前已经发送过相同的信号，用新数据再次提醒
- **edge**：比较当前的市场边缘幅度与之前的边缘幅度

**数据持久化**：数据存储在`~/.openclaw/state/daily_context.json`文件中：
```json
{
  "date": "2026-03-09",
  "messages": [
    {
      "time": "09:15",
      "trigger": "cross_platform",
      "spread": 7.2,
      "markets": ["kalshi", "polymarket"],
      "message_id": "msg_abc123"
    },
    {
      "time": "14:30",
      "trigger": "portfolio",
      "pnl": 12.5,
      "message_id": "msg_def456"
    }
  ],
  "silence_count": 1,
  "micro_count": 0,
  "sent_count": 5
}
```

**自动重置**：午夜（UTC时间）自动清除上下文信息，为新一天做好准备。

**引用示例**：
```
Earlier (9:15 AM):  "Mild divergence. Kalshi 52%, Poly 48%."
Later (2:30 PM):    "That Kalshi/Poly spread I flagged this morning widened to 7% — now 55/48. Worth watching."
```

**自定义点**：在`context_buffer.py`中为新的触发类型添加引用逻辑：
```python
def generate_backreference(trigger_type, current_data, history):
    if trigger_type == 'cross_platform':
        earlier = find_similar_trigger(history, 'cross_platform')
        if earlier:
            spread_change = current_data['spread'] - earlier['spread']
            return f"That spread I flagged {time_ago(earlier)} widened to {spread_change}%."
    return None
```

---

## 系统6：响应跟踪器 — 互动适应性

**功能**：跟踪用户的互动模式。如果用户对70%以上的消息有反应，信息的紧急程度保持较高；如果互动率低于10%，则降低紧急程度或建议进行优化。

**针对不同触发类型的指标**：
- **发送次数**：发送的消息数量
- **互动次数**：用户在1小时内回复的消息数量
- **忽略次数**：用户未回复的消息数量
- **平均回复时间**：从消息发送到用户回复的平均时间（以分钟计）

**1小时互动窗口**：如果用户在60分钟内回复消息，则计入互动次数；超过60分钟则视为忽略。

**紧急程度调整因子**：
- **互动率≥70%**：紧急程度乘以1.3（用户喜欢这些消息，增加发送频率）
- **互动率40-70%**：紧急程度乘以1.0（保持平衡）
- **互动率<10%**：紧急程度乘以0.5（用户忽略消息，降低发送频率）

**适应建议**：如果某种触发类型连续发送10次以上但互动率低于20%，则记录相关信息：
```
⚠️ ADJUSTMENT SUGGESTION:
Trigger: x_signals
Sends: 12 | Engagement: 8% | Avg response time: Never

Consider:
→ Lower signal confidence floor (currently 0.65)
→ Reduce frequency (increase silence thresholds)
→ Check if message editorial voice is mismatched
```

**数据持久化**：数据存储在`~/.openclaw/state/response_tracker.json`文件中：
```json
{
  "cross_platform": {
    "sends": 15,
    "engagements": 9,
    "ignores": 6,
    "avg_response_time": 23.5,
    "last_engagement": "2026-03-09T14:32:00Z"
  },
  "x_signals": {
    "sends": 12,
    "engagements": 1,
    "ignores": 11,
    "avg_response_time": null,
    "last_engagement": null
  }
}
```

**自定义点**：在`response_tracker.py`中调整互动阈值和调整因子：
```python
ENGAGEMENT_THRESHOLDS = {
    'high': 0.70,    # ≥70% → 1.3x urgency
    'low': 0.10,     # <10% → 0.5x urgency
}
URGENCY_MULTIPLIERS = {
    'high': 1.3,
    'low': 0.5,
}
SUGGESTION_TRIGGERS = {
    'min_sends': 10,
    'max_engagement_for_suggestion': 0.20,
}
```

---

## OpenClaw生态系统集成

该人格引擎可以与**任何OpenClaw代理**配合使用——它不依赖于特定的应用领域。虽然它是与预测市场交易堆栈一起设计的，但适用于任何发送警报、摘要或通知的主动型代理。

**安装完整的预测市场交易堆栈：**
```bash
clawhub install kalshalyst kalshi-command-center polymarket-command-center prediction-market-arbiter xpulse portfolio-drift-monitor market-morning-brief personality-engine
```

## 与OpenClaw代理的集成

### 第1步：导入引擎

```python
from personality_engine.engine import PersonalityEngine

engine = PersonalityEngine(user_id="user@example.com")
```

### 第2步：连接到主动触发系统

在你的代理的触发处理程序中（例如`proactive_agent.py`）：

```python
async def fire_trigger(trigger_type, data):
    # Your normal trigger logic
    message_content = generate_message(trigger_type, data)

    # Pass through personality engine
    should_send, scheduled_message = await engine.process_trigger(
        trigger_type=trigger_type,
        raw_message=message_content,
        market_data=data,
        urgency_context={'vol': market_vol, 'pnl': portfolio_pnl, ...}
    )

    if should_send:
        if scheduled_message.delayed:
            schedule_send(scheduled_message.content, delay=scheduled_message.delay_seconds)
        else:
            send_now(scheduled_message.content)
    else:
        log_silence_skip(trigger_type)
```

### 第3步：连接响应跟踪器

当用户回复消息时：

```python
def handle_user_response(message_id, trigger_type, response_time_seconds):
    engine.response_tracker.log_engagement(trigger_type, response_time_seconds)
```

### 第4步：运行micro_initiations

添加一个定时任务（每30分钟执行一次）：

```python
async def micro_initiations_check():
    micro_message = await engine.check_micro_initiations(context={
        'vol': market_vol,
        'trade_count': trades_today,
        'user_absence_hours': hours_since_last_engagement,
        'portfolio_streak': consecutive_days,
    })

    if micro_message:
        send_now(micro_message)
```

### 第5步：每日上下文重置

午夜时，引擎会自动重置上下文信息。如有需要，也可以手动触发：

```python
engine.context_buffer.reset_daily()
```

---

## 超出交易领域的应用场景

虽然默认的语音池和阈值是为预测市场交易设计的，但每个系统都可以根据具体领域进行定制：

| 领域 | 编辑语音 | 沉默规则 | 自动环境提示 |
|--------|----------------|---------------|-------------------|
| **交易**（默认） | 市场评论、市场趋势分析 | 跳过市场平静期或趋势不明显的时期 | 跳过表现良好或不佳的市场时期 |
| **个人助手** | 任务优先级建议 | 跳过低紧急程度的提醒 | “本周没有新任务。收件箱比较清空。” |
| **DevOps/监控** | 事件严重性提示 | 跳过常规的健康检查 | “系统运行正常，已连续30天。” |
| **销售/CRM** | 交易阶段建议 | 跳过无效的潜在客户信息 | “本季度潜在客户数量较少。” |
| **内容/社交** | 互动评论 | 跳过表现不佳的内容 | “你的上一条帖子表现较好。” |

要进行定制：只需修改`editorial_voice.py`中的`VOICE_POOLS`字典，更新`selective_silence.py`中的阈值，并在`micro_initiations.py`中添加特定领域的提示信息池。详细指南请参阅`references/customization.md`。

---

## 文件结构

```
personality-engine/
├── SKILL.md                           # This file
├── scripts/
│   ├── __init__.py
│   ├── engine.py                      # Main orchestrator
│   ├── editorial_voice.py             # Opinion injection
│   ├── selective_silence.py           # Content quality checks
│   ├── variable_timing.py             # Urgency + time-of-day
│   ├── micro_initiations.py           # Ambient pings
│   ├── context_buffer.py              # Daily memory
│   └── response_tracker.py            # Engagement tracking
├── references/
│   ├── systems-overview.md            # Architecture diagram + flow
│   └── customization.md               # Per-system customization guide
└── examples/
    └── integration-example.py         # Copy-paste integration template
```

---

## 快速定制指南

### 情景1：你的代理每天发送50条警报，但用户大多忽略

1. **提高沉默阈值**（`selective_silence.py`）：提高被视为“值得发送”的信息的标准
2. **降低动态时间安排的阈值**（`variable_timing.py`）：减少非高峰时段发送的消息数量
3. **检查编辑语音**：某些观点可能不符合用户的偏好
4. **审查响应跟踪器**：哪些触发类型的互动率低于20%？将这些触发类型静音

### 情景2：你的代理不主动发送信息，只响应信息

1. **自定义micro_initiations**：根据具体领域添加条件
   ```python
   'LOW_VOLATILITY_OPPORTUNITY': {
       'condition': lambda ctx: ctx.vol < 0.2 and ctx.last_edge_size > 2.0,
       'messages': ["Calm market, good edge conditions. Might be time to scout."],
   }
   ```
2. **调整发送频率**：如果用户喜欢，将每周的发送频率从2次增加到3-4次

### 情景3：你的代理提供的观点显得过于通用

1. 打开`editorial_voice.py`，为每个触发类型扩展语音内容
2. 根据用户类型（交易者或长期投资者）调整语音内容：
   ```python
   'VOICE_POOLS': {
       'cross_platform': {
           'big_divergence': [
               "Big divergence. One of these markets is wrong.",
               "Spreads are blown out. Arb opportunity.",
               "Thick divergence — reality check time.",
           ],
           ...
   ```
3. 在启动引擎时传递`user_profile`参数，以适应不同用户的需求

---

## 性能与状态管理

**状态文件**（位于用户的主目录下）：
- `~/.openclaw/state/daily_context.json`（约5KB，每天重置）
- `~/.openclaw/state/response_tracker.json`（约2KB，数据持久保存）

**引擎运行开销**：
- 编辑语音：<5毫秒（字典查找）
- 选择性沉默：<10毫秒（阈值比较）
- 动态时间安排：<15毫秒（紧急程度计算）
- 自动环境提示：<20毫秒（条件判断）
- 上下文缓冲区：<5毫秒（历史数据查找）
- 响应跟踪：<5毫秒（指标查询）

**整个流程**：每个触发事件的处理时间约为60毫秒（对于异步消息发送来说可以忽略不计）

---

## 许可证

该框架是OpenClaw产品的一部分，可在任何代理中免费使用。

---

## 版本历史

**v1.0.0**（2026-03-09）
- 初始的6个系统框架
- 针对预测市场交易代理进行了默认配置调整
- 所有系统都支持领域定制——可以根据具体需求更换语音池、阈值和自动环境提示的条件

---