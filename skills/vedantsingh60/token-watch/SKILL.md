# TokenWatch

**跟踪、分析并优化跨AI提供商的token使用情况和成本。设置预算、接收警报、比较模型，从而降低您的开支。**

免费且开源（MIT许可证）• 无依赖项• 本地运行• 无需API密钥

---

## 为什么需要这个工具？

在OpenAI收购OpenClaw之后，token成本成为高级用户最关心的问题。该工具能让您全面了解自己的支出情况、支出去向以及如何降低成本。

### 它解决的问题：
- 在收到账单之前，您无法知道自己的实际支出金额
- 在选择模型之前，无法比较不同提供商的成本
- 当接近预算时，没有警报提示
- 没有可操作的节省开支建议

---

## 功能

### 1. 记录使用情况并自动计算成本

```python
from tokenwatch import TokenWatch

monitor = TokenWatch()

monitor.record_usage(
    model="claude-haiku-4-5-20251001",
    input_tokens=1200,
    output_tokens=400,
    task_label="summarize article"
)
# ✅ Recorded: $0.00192
```

### 2. 从API响应中自动记录数据

```python
from tokenwatch import record_from_anthropic_response, record_from_openai_response

# Anthropic
response = client.messages.create(model="claude-haiku-4-5-20251001", ...)
record_from_anthropic_response(monitor, response, task_label="my task")

# OpenAI
response = client.chat.completions.create(model="gpt-4o-mini", ...)
record_from_openai_response(monitor, response, task_label="my task")
```

### 3. 设置预算并设置警报

```python
monitor.set_budget(
    daily_usd=1.00,
    weekly_usd=5.00,
    monthly_usd=15.00,
    per_call_usd=0.10,
    alert_at_percent=80.0   # Alert at 80% of budget
)
# ✅ Budget set: daily=$1.0, weekly=$5.0, monthly=$15.0
# 🚨 BUDGET ALERT fires automatically when threshold is crossed
```

### 4. 仪表盘

```python
print(monitor.format_dashboard())
```

```
💰 SPENDING SUMMARY
  Today:   $0.0042  (4 calls, 13,600 tokens)
  Week:    $0.0231  (18 calls, 67,200 tokens)
  Month:   $0.1847  (92 calls, 438,000 tokens)

📋 BUDGET STATUS
  Daily:   [████░░░░░░░░░░░░░░░░] 42% $0.0042 / $1.00 ✅
  Monthly: [███████░░░░░░░░░░░░░] 37% $0.1847 / $0.50 ⚠️

💡 OPTIMIZATION TIPS
  🔴 Swap Opus → Sonnet for non-reasoning tasks (save ~$8.20/mo)
  🟡 High avg cost/call on gpt-4o — reduce prompt length
```

### 5. 在调用模型前进行比较

```python
# For 2000 input + 500 output tokens:
for m in monitor.compare_models(2000, 500)[:6]:
    print(f"{m['model']:<42} ${m['cost_usd']:.6f}")
```

```
gemini-2.5-flash                           $0.000300
gpt-4o-mini                                $0.000600
mistral-small-2501                         $0.000350
claude-haiku-4-5-20251001                  $0.003600
mistral-large-2501                         $0.007000
gemini-2.5-pro                             $0.007500
```

### 6. 调用前进行成本估算

```python
estimate = monitor.estimate_cost("claude-sonnet-4-5-20250929", input_tokens=5000, output_tokens=1000)
print(f"Estimated cost: ${estimate['estimated_cost_usd']:.6f}")
```

### 7. 优化建议

```python
suggestions = monitor.get_optimization_suggestions()
for s in suggestions:
    savings = s.get("estimated_monthly_savings_usd", 0)
    print(f"[{s['priority'].upper()}] {s['message']}")
    if savings:
        print(f"  → Save ~${savings:.2f}/month")
```

### 8. 导出报告

```python
monitor.export_report("monthly_report.json", period="month")
```

---

## 支持的模型（2026年2月）

**10个提供商提供的41个模型** — 2026年2月16日更新

| 提供商 | 模型 | 输入/1M | 输出/1M |
|----------|-------|----------|-----------|
| Anthropic | claude-opus-4-6 | $5.00 | $25.00 |
| Anthropic | claude-opus-4-5 | $5.00 | $25.00 |
| Anthropic | claude-sonnet-4-5-20250929 | $3.00 | $15.00 |
| Anthropic | claude-haiku-4-5-20251001 | $1.00 | $5.00 |
| OpenAI | gpt-5.2-pro | $21.00 | $168.00 |
| OpenAI | gpt-5.2 | $1.75 | $14.00 |
| OpenAI | gpt-5 | $1.25 | $10.00 |
| OpenAI | gpt-4.1 | $2.00 | $8.00 |
| OpenAI | gpt-4.1-mini | $0.40 | $1.60 |
| OpenAI | gpt-4.1-nano | $0.10 | $0.40 |
| OpenAI | o3 | $10.00 | $40.00 |
| OpenAI | o4-mini | $1.10 | $4.40 |
| Google | gemini-3-pro | $2.00 | $12.00 |
| Google | gemini-3-flash | $0.50 | $3.00 |
| Google | gemini-2.5-pro | $1.25 | $10.00 |
| Google | gemini-2.5-flash | $0.30 | $2.50 |
| Google | gemini-2.5-flash-lite | $0.10 | $0.40 |
| Google | gemini-2.0-flash | $0.10 | $0.40 |
| Mistral | mistral-large-2411 | $2.00 | $6.00 |
| Mistral | mistral-medium-3 | $0.40 | $2.00 |
| Mistral | mistral-small | $0.10 | $0.30 |
| Mistral | mistral-nemo | $0.02 | $0.10 |
| Mistral | devstral-2 | $0.40 | $2.00 |
| xAI | grok-4 | $3.00 | $15.00 |
| xAI | grok-3 | $3.00 | $15.00 |
| xAI | grok-4.1-fast | $0.20 | $0.50 |
| Kimi | kimi-k2.5 | $0.60 | $3.00 |
| Kimi | kimi-k2 | $0.60 | $2.50 |
| Kimi | kimi-k2-turbo | $1.15 | $8.00 |
| Qwen | qwen3.5-plus | $0.11 | $0.44 |
| Qwen | qwen3-max | $0.40 | $1.60 |
| Qwen | qwen3-vl-32b | $0.91 | $3.64 |
| DeepSeek | deepseek-v3.2 | $0.14 | $0.28 |
| DeepSeek | deepseek-r1 | $0.55 | $2.19 |
| DeepSeek | deepseek-v3 | $0.27 | $1.10 |
| Meta | llama-4-maverick | $0.27 | $0.85 |
| Meta | llama-4-scout | $0.18 | $0.59 |
| Meta | llama-3.3-70b | $0.23 | $0.40 |
| MiniMax | minimax-m2.5 | $0.30 | $1.20 |
| MiniMax | minimax-m1 | $0.43 | $1.93 |
| MiniMax | minimax-text-01 | $0.20 | $1.10 |

> 要添加自定义模型，请将其添加到 `tokenwatch.py` 文件顶部的 `PROVIDER_PRICING` 字典中。

---

## API参考

### `TokenWatch(storage_path)`
初始化监控工具。数据默认存储在 `.tokenwatch/` 文件夹中。

### `record_usage(model, input_tokens, output_tokens, task_label, session_id)`
记录单次API调用。返回包含计算成本的 `TokenUsageRecord` 对象。

### `set_budget(daily_usd, weekly_usd, monthly_usd, per_call_usd, alert_at_percent)`
配置支出限制。当超过阈值时，会自动触发警报。

### `get_spend(period)`
获取汇总支出信息。周期选项：`"today"`、`"week"`、`"month"`、`"all"` 或 `"YYYY-MM-DD"`。

### `get_spend_by_model(period)`
按模型分类的支出明细，按成本降序排列。

### `get_spend_by_provider(period)`
按提供商分类的支出明细。

### `compare_models(input_tokens, output_tokens)`
比较所有已知模型的成本。返回按成本从低到高排序的模型列表。

### `estimate_cost(model, input_tokens, output_tokens)`
在调用模型前估算成本。

### `get_optimization_suggestions()`
分析使用情况并返回带有预估月度节省额的建议。

### `format_dashboard()`
提供易于阅读的支出仪表盘，包含预算条形图和实用提示。

### `export_report(output_file, period)`
将完整报告导出为JSON格式。

### `record_from_anthropic_response(monitor, response, task_label)`
辅助函数，用于从Anthropic SDK响应对象中自动记录数据。

### `record_from_openai_response(monitor, response, task_label)`
辅助函数，用于从OpenAI SDK响应对象中自动记录数据。

---

## 隐私与安全

- ✅ **零数据传输** — 无数据被发送到外部
- ✅ **仅本地存储** — 所有数据存储在您机器上的 `.tokenwatch/` 文件夹中
- ✅ **无需API密钥** — 监控工具本身不需要任何凭证
- ✅ **无需认证** — 无需账户或登录
- ✅ **完全透明** — 使用MIT许可证，源代码公开

---

## 更新日志

### [1.2.3] - 2026-02-16

- 📋 更新了SKILL.md中的模型列表，以匹配代码中的41个模型（10个提供商）

### [1.2.0] - 2026-02-16

- ✨ 新增DeepSeek、Meta Llama和MiniMax提供商
- ✨ 模型数量增加到41个（10个提供商）
- ✨ 更新了Anthropic/OpenAI/Google/Mistral的定价信息（2026年2月的费率）

### [1.1.0] - 2026-02-16

- ✨ 新增xAI Grok、Kimi（Moonshot）和Qwen（Alibaba）提供商
- ✨ 模型数量增加到32个（7个提供商）

### [1.0.0] - 2026-02-16

- ✨ 初始版本发布 — TokenWatch
- ✨ 提供了5个提供商的11个模型的定价信息
- ✨ 支持每日、每周、每月及每次调用的预算警报
- ✨ 支持模型成本比较、成本估算和优化建议
- ✨ 支持自动处理Anthropic和OpenAI的响应数据
- ✨ 提供仪表盘、JSON导出功能，数据仅存储在本地，采用MIT许可证

---

**最后更新时间**：2026年2月16日
**当前版本**：1.2.3
**状态**：活跃且由社区维护

© 2026 UnisAI社区