---
name: agent-rate-limiter
description: "通过自动的基于层级的限流机制和指数级退避策略来防止 429 错误（即请求超时错误）。完全不需要依赖任何外部服务。由 The Agent Wire（theagentwire.ai）提供支持。"
homepage: https://theagentwire.ai
metadata: { "openclaw": { "emoji": "⚡" } }
---
# 再也不要遇到429错误了

你肯定经历过这种情况：你的AI代理正在执行任务（比如浏览网页、创建子代理、发送邮件），然后突然：

```
rate_limit_error: You've exceeded your account's rate limit
```

一切都被中断了。请求次数被浪费了，上下文信息也丢失了。你只能手动重启代理，然后10分钟后再次尝试。

**这个工具可以避免这种情况**。它通过滚动窗口来监控代理的请求频率，并根据请求频率为代理分配不同的等级（正常 → 谨慎 → 限制请求 → 危急 → 暂停）。当代理的请求频率达到限制时，它会自动降低请求频率。如果真的遇到了429错误，它会根据指数衰减算法来安排恢复时间。

**无需任何API密钥、pip安装或外部服务**，只需要一个Python脚本和一个JSON状态文件即可。

该工具由[The Agent Wire](https://theagentwire.ai)开发——这是一个专注于AI代理的团队。

---

## 2分钟快速入门

只需使用Claude Max的默认设置即可，无需任何配置。

```bash
# 1. Test it works
python3 scripts/rate-limiter.py gate && echo "✅ Working"

# 2. Add to your agent loop
python3 scripts/rate-limiter.py gate || exit 1
python3 scripts/rate-limiter.py record 1000
```

就这样简单。在开始工作前先运行这个脚本，工作结束后再运行一次记录脚本。其余的配置都可以根据需要进行调整。

---

## 配置

所有配置项都是可选的。默认值采用Claude Max的保守设置。

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
| `claude` | `max-5x` | 5小时 | 200次请求 | 保守的估计值 |
| `claude` | `max-20x` | 5小时 | 540次请求 | 约为理论最大值的60% |
| `openai` | `plus` | 3小时 | 80次请求 | GPT-4o的请求量 |
| `openai` | `pro` | 3小时 | 200次请求 | 更高级别的使用计划 |
| `custom` | — | 可自定义 | 可根据实际情况调整 | 自定义限制值 |

这些预设值仅供参考。你可以根据实际使用情况调整`RATE_LIMIT_ESTIMATE`参数——每个账户的请求频率可能会有所不同。

---

## 等级系统

| 等级 | 触发条件 | 推荐行为 |
|---|---|---|
| `ok` | 请求频率<90% | 继续正常运行 |
| `cautious` | 请求频率≥90% | 跳过主动检查和非必要的后台任务 |
| `throttled` | 请求频率≥95% | 不创建子代理，回复简洁，跳过非必要的定时任务 |
| `critical` | 请求频率≥98% | 仅处理用户请求，每次最多调用一个工具接口，所有定时任务暂停 |
| `paused` | 遇到429错误 | 所有操作停止，自动恢复 |

### 为什么选择90%、95%和98%作为阈值？

这些阈值并非随意设定。Anthropic和OpenAI等API提供商会在你达到请求限制之前就开始拒绝请求——因为它们无法处理正在处理中的请求，而且它们的内部计数可能与你的不同。90%的阈值可以让你有时间优雅地完成当前的任务。当请求频率达到95%时，你就进入了危险区域，任何突然的请求都可能导致429错误。而98%的阈值则意味着你距离请求限制只有一步之遥。这样的分级设置可以实现平滑的减速过程，而不会导致系统突然崩溃。

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
| `0` | 状态正常或处于谨慎等级 — 继续运行 |
| `1` | 处于限制请求等级 — 减少请求频率 |
| `2` | 处于紧急或暂停等级 — 停止非必要的操作 |

---

## 完整集成示例

以下是一个完整的示例，展示了如何使用该工具进行请求频率检查、根据等级调整行为、记录请求情况以及处理429错误：

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

## 代理集成

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

将以下代码添加到定时任务的开始部分：

```
**FIRST: Rate limit gate check.** Run `python3 scripts/rate-limiter.py gate`.
If exit code is 2, reply 'RATE_LIMITED' and stop.
If exit code is 1, do only essential work.
```

---

## 工作原理

该工具使用**启发式估计**方法，而不是直接获取API层面的使用数据。它会在一个滚动窗口内统计请求次数，并与可配置的请求限制进行比较。

**为什么使用启发式估计？**因为Anthropic和OpenAI都没有提供实时的使用数据API。要获取这些数据需要浏览器认证或爬取操作，而这个工具完全不需要任何外部依赖。

**准确性：**根据实际情况，准确率约为70-85%。如果你经常遇到429错误，可以降低`RATE_LIMIT_ESTIMATE`的值；如果你的系统过于保守，可以适当提高这个值。

**提高准确性的方法：**
- 使用默认的保守预设值。
- 如果遇到429错误，工具会自动通过指数衰减算法进行调整。
- 运行几天后，检查`status`命令以了解实际的请求模式，并根据实际情况调整`RATE_LIMIT_ESTIMATE`。

---

## 状态文件

该工具会生成一个JSON文件（默认路径：`./rate-limit-state.json`）。文件结构如下：

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

| 处理方式 | 问题 |
|---|---|
| **不进行处理** | 代理可能会崩溃，丢失上下文信息，重复请求会浪费资源 |
| **简单的重试循环** | 会持续向API发送请求，导致更严重的限制问题，且无法改变代理的行为 |
| **监控仪表盘** | 只能在请求被限制后才能发现问题，无法预防错误的发生 |
| **这个工具** | 可以在错误发生之前就进行预防，实现平滑的请求减速，并自动恢复 |

**关键区别：**这个工具是预防性的，而不是在错误发生后才采取行动。它会在请求频率达到限制之前就自动降低代理的请求频率，从而保护代理的正常运行并避免资源浪费。

---

## 故障排除

**即使显示“ok”状态仍然遇到429错误**
可能是因为你的请求频率估计过高。可以通过`python3 scripts/rate-limiter.py set-limit 150`（或其他合适的值）来降低限制。默认的预设值比较保守，但你的账户实际的限制可能更低。

**状态文件损坏**
可以使用`python3 scripts/rate-limiter.py reset`来重置所有设置。这会清除所有历史数据并重新开始统计。你的配置信息不会丢失，只需重新导出环境变量即可。

**估计值与实际情况相差较大**
可以使用`python3 scripts/rate-limiter.py status`来检查实际的请求模式。比较实际请求次数与设定的限制值：如果你只有50次请求就遇到了429错误，说明估计值过高；如果你有180到200次请求却从未达到限制，可以适当提高估计值。

**多个OpenClaw实例**
每个实例都需要有自己的状态文件。需要为每个实例设置唯一的路径来存储状态文件（例如：`python3 scripts/rate-limiter.py set-rate-limit-state /path/to/instance`）。否则，它们会覆盖彼此的统计数据，导致估计值失效。

---

## 常见问题解答

**这个工具是什么？**
`Agent Rate Limiter`是一个Python脚本，通过监控代理的请求频率并在达到限制之前自动降低请求频率，从而防止AI代理遇到API的429错误。

**它能解决什么问题？**
在使用有请求限制的服务（如Claude Max）时，AI代理可能会在不知情的情况下耗尽所有请求次数，导致429错误并停止运行。这个工具可以让代理在达到限制之前自动降低请求频率，并在恢复后自动恢复正常。

**需要什么环境？**
只需Python 3环境（仅使用标准库）。无需安装额外的库或API密钥，也不需要任何外部服务。

**它是如何工作的？**
该工具会在执行高成本操作之前检查代理的当前等级（正常 → 谨慎 → 限制请求 → 危急 → 暂停）。遇到429错误时，它会根据指数衰减算法安排恢复时间，并通过定时任务来执行恢复操作。代理会根据当前等级自动调整自己的行为。

**它适用于所有大型语言模型（LLM）提供商吗？**
是的。该工具与提供商无关，它可以监控任何有请求限制的API（如Claude、GPT、Gemini等）。