---
name: agent-rate-limiter
description: "通过自动的基于层级的流量限制和指数级退避策略来防止 429 错误（即“请求过多导致服务暂时无法响应”的情况）。完全不需要依赖任何第三方服务。由 TheAgentWire（theagentwire.ai）提供支持。"
homepage: https://theagentwire.ai
metadata: { "openclaw": { "emoji": "⚡" } }
---
# 再也不用遇到429错误了

你肯定遇到过这种情况：你的AI代理正在执行任务（比如浏览网页、创建子代理、发送邮件），然后突然：

```
rate_limit_error: You've exceeded your account's rate limit
```

一切都被中断了。请求被浪费了，上下文信息也丢失了。你只能手动重启代理，然后10分钟后再次尝试。

**这个技能可以避免这种情况。**它通过滚动窗口来监控代理的请求使用情况，并根据使用情况自动调整代理的运行状态（正常 → 谨慎 → 限制请求 → 危急 → 暂停）。当代理真正遇到429错误时，它会使用指数退避策略来安排恢复时间。

**无需任何API密钥、Python包安装或外部服务。**只需要一个Python脚本和一个JSON状态文件即可。

这个技能由[The Agent Wire](https://theagentwire.ai?utm_source=clawhub&utm_medium=skill&utm_campaign=agent-rate-limiter)开发——他们专门研究AI代理的相关技术。喜欢这个技能吗？我每周三都会发布关于构建类似工具的文章。

---

## 2分钟快速入门

只需使用Claude Max 5x的默认设置，无需任何配置即可立即使用。

```bash
# 1. Test it works
python3 scripts/rate-limiter.py gate && echo "✅ Working"

# 2. Add to your agent loop
python3 scripts/rate-limiter.py gate || exit 1
python3 scripts/rate-limiter.py record 1000
```

就这么简单。在开始工作前先运行这个脚本，工作结束后再记录相关数据。其他细节都可以根据需要进行调整。

---

## 配置

所有配置项都是可选的。默认设置比较保守，适用于Claude Max 5x。

```bash
export RATE_LIMIT_PROVIDER="claude"          # claude | openai | custom
export RATE_LIMIT_PLAN="max-5x"             # max-5x | max-20x | plus | pro | custom
export RATE_LIMIT_STATE="/path/to/state.json"  # State file location
export RATE_LIMIT_WINDOW_HOURS="5"           # Rolling window duration
export RATE_LIMIT_ESTIMATE="200"             # Estimated request limit per window
```

### 提供商预设

| 提供商 | 计划 | 时间窗口 | 预计限制 | 备注 |
|---|---|---|---|---|
| `claude` | `max-5x` | 5小时 | 200次请求 | 较保守的估计 |
| `claude` | `max-20x` | 5小时 | 540次请求 | 接近理论上限的60% |
| `openai` | `plus` | 3小时 | 80次请求 | GPT-4o的请求量 |
| `openai` | `pro` | 3小时 | 200次请求 | 更高级别的使用限制 |
| `custom` | — | 可自定义 | 可根据实际情况调整 |

这些预设值仅供参考。你需要根据实际使用情况调整`RATE_LIMIT_ESTIMATE`参数——每个账户的请求模式可能略有不同。

---

## 状态等级系统

| 等级 | 触发条件 | 推荐行为 |
|---|---|---|
| `ok` | 请求量低于90% | 继续正常运行 |
| `cautious` | 请求量达到90%以上 | 跳过主动检查和非必要的后台任务 |
| `throttled` | 请求量达到95%以上 | 停止创建子代理，简化响应，跳过非必要的定时任务 |
| `critical` | 请求量达到98%以上 | 仅处理用户请求，每次最多调用一个工具接口，停止所有定时任务 |
| `paused` | 遇到429错误 | 所有操作暂停。自动恢复机制会处理后续的请求 |

### 为什么选择90%、95%、98%这些阈值？

这些阈值并非随意设定。Anthropic和OpenAI等API提供商会在你达到上限之前就开始拒绝请求——因为它们无法处理正在处理中的请求，而且它们的内部计数器可能与你的不同。90%的阈值可以让你有足够的时间优雅地完成当前任务；达到95%时，你已经处于危险区域，稍有波动就可能触发429错误；而98%的阈值则意味着你距离上限仅差一次请求。

---

## 命令

```bash
python3 scripts/rate-limiter.py <command> [args]

gate                    # Check tier, exit code reflects severity
record [tokens]         # Log a request (tokens optional, default 0)
status                  # Full status JSON (tier, pct, requests, limit, backoff info)
pause [minutes]         # Enter paused state (auto backoff if no minutes given)
resume                  # Clear pause, reset to cautious
set-limit <n>           # Override estimated request limit
reset                   # Reset all state to defaults
```

### 错误代码

| 代码 | 含义 |
|---|---|
| `0` | 状态正常或处于谨慎模式 — 继续运行 |
| `1` | 处于限制请求模式 — 减少活动量 |
| `2` | 处于紧急或暂停模式 — 停止非必要的操作 |

---

## 完整集成示例

以下是一个完整的示例，展示了如何使用这个技能进行请求检查、根据状态调整行为、记录数据以及处理429错误：

```bash
#!/bin/bash
GATE=$(python3 scripts/rate-limiter.py gate 2>/dev/null)
EXIT=$?

if [ $EXIT -eq 2 ]; then
  echo "🛑 Critical/paused. Skipping work."
  exit 0
fi

if [ $EXIT -eq 1 ]; then
  echo "⚡ Throttled. Doing minimal work only."
  # skip sub-agents, background tasks, etc.
fi

# --- Do your actual work here ---
RESULT=$(your-agent-command 2>&1)

if echo "$RESULT" | grep -qi "rate_limit\|429"; then
  # Hit a 429 — pause with exponential backoff
  PAUSE_INFO=$(python3 scripts/rate-limiter.py pause)
  UNTIL=$(echo "$PAUSE_INFO" | python3 -c "import sys,json; print(json.load(sys.stdin).get('pausedUntil','unknown'))")
  echo "🛑 Rate limited. Paused until $UNTIL"
  exit 1
fi

# Record usage (estimate tokens based on your workload)
python3 scripts/rate-limiter.py record 2000
```

---

## 代理集成方法

### 在AGENTS.md文件中：

```markdown
## Rate Limiting

Before expensive operations: `python3 scripts/rate-limiter.py gate`
- Exit 0 → proceed normally
- Exit 1 → reduce activity (no spawns, terse responses)
- Exit 2 → stop all non-essential work

After significant work: `python3 scripts/rate-limiter.py record <approx_tokens>`

On 429 error:
1. `python3 scripts/rate-limiter.py pause`
2. Stop current work
3. Set a timer/cron to run `python3 scripts/rate-limiter.py resume` at the pausedUntil time
```

### 在心跳检查中：

```markdown
## Rate Limit Gate (ALWAYS FIRST)
Run: `python3 scripts/rate-limiter.py gate`
- Exit 2 → reply HEARTBEAT_OK immediately. Do nothing else.
- Exit 1 → skip proactive checks. Only handle urgent items.
- Exit 0 → proceed normally.
```

### 在定时任务中：

只需将以下代码添加到定时任务的执行脚本开头：

```
**FIRST: Rate limit gate check.** Run `python3 scripts/rate-limiter.py gate`.
If exit code is 2, reply 'RATE_LIMITED' and stop.
If exit code is 1, do only essential work.
```

---

## 工作原理

这个技能使用**启发式估计**方法，而不是直接获取API层面的使用数据。它会在一个滚动窗口内统计请求次数，并与可配置的请求限制进行比较。

**为什么使用启发式估计？**因为Anthropic和OpenAI都没有提供实时的使用数据接口。要获取这些数据需要浏览器认证或数据抓取，而这个技能完全不需要任何外部依赖。

**准确率：**大约70-85%，具体取决于估计值与实际限制的匹配程度。如果你经常遇到429错误，可以适当提高`RATE_LIMIT_ESTIMATE`的值；如果估计值过于保守，可以降低它。

**提高准确率的方法：**
- 使用默认的保守预设值开始使用。
- 如果遇到429错误，技能会自动使用指数退避策略进行调整。
- 运行几天后，检查`status`命令以了解实际的请求模式，并根据实际情况调整估计值。

---

## 状态文件

这个技能会生成一个JSON文件（默认路径：`./rate-limit-state.json`），其结构如下：

```json
{
  "provider": "claude",
  "plan": "max-5x",
  "tier": "ok",
  "estimatedPct": 23,
  "window": {
    "durationMs": 18000000,
    "requests": [{"ts": 1234567890, "tokens": 3000}],
    "estimatedLimit": 200
  },
  "backoff": {
    "consecutive429s": 0,
    "lastBackoffMs": 0
  },
  "pausedUntil": null
}
```

---

## 为什么不用手动处理429错误？

| 处理方法 | 问题 |
|---|---|
| **不进行处理** | 代理可能会崩溃，丢失上下文信息，重复请求会浪费资源 |
| **简单的重试机制** | 会持续向API发送请求，使问题更加严重，且无法改变代理的行为 |
| **监控仪表盘** | 只能在请求被限制后才能发现问题，无法预防错误的发生 |
**这个技能** | 能在错误发生之前就进行预防，实现平滑的请求减速和自动恢复，且完全不需要任何外部依赖。

---

## 常见问题及解决方法

**即使状态显示为“正常”，仍然遇到429错误**
可能是因为你的估计值过高。可以降低限制值：`python3 scripts/rate-limiter.py set-limit 150`（或其他合适的数值）。默认预设值较为保守，但你的账户实际的限制可能更低。

**状态文件损坏**
可以重置所有设置：`python3 scripts/rate-limiter.py reset`。这会清除所有历史数据并重新开始统计。你的配置信息不会丢失，只需重新设置环境变量即可。

**估计值与实际情况相差很大**
检查实际的请求模式：`python3 scripts/rate-limiter.py status`。比较实际请求次数与设定的限制值。如果你的请求次数为50次却经常遇到429错误，说明估计值过高；如果请求次数在180-200次之间且从未达到限制，可以适当提高估计值。

**多个OpenClaw实例**
每个实例都需要自己的状态文件。请为每个实例设置唯一的路径：```bash
export RATE_LIMIT_STATE="/path/to/instance-1-rate-limit.json"
```。否则，它们会互相覆盖数据，导致估计值失效。

---

## 常见问题解答

**这个技能是什么？**
**Agent Rate Limiter**是一个Python脚本，通过监控代理的请求使用情况并在达到限制之前自动限制请求频率，从而防止AI代理遇到API的429错误。

**它解决了什么问题？**
对于使用量有限制的AI代理（如Claude Max）来说，它们可能在不知不觉中就耗尽了请求限制，导致429错误并陷入停滞。这个技能让代理在达到限制之前就能自动调整行为，并在恢复后继续正常工作。

**使用要求是什么？**
只需要Python 3环境（仅使用标准库）。无需安装任何Python包或API密钥，也不需要任何外部服务。只需一个脚本和一个JSON状态文件即可。

**它是如何工作的？**
这个脚本会在执行高成本操作之前检查代理的运行状态（正常 → 谨慎 → 限制请求 → 危急 → 暂停）。遇到429错误时，它会使用指数退避策略，并通过定时任务安排恢复。代理会根据当前的状态等级调整自己的行为。

**它适用于所有大型语言模型（LLM）提供商吗？**
是的。这个技能与具体的提供商无关，它可以监控任何具有请求限制的API（如Claude、GPT、Gemini等）。