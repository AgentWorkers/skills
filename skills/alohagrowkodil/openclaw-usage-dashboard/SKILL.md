---
name: openclaw-usage-dashboard
description: 生成一个交互式的本地 HTML 仪表板，用于展示 OpenClaw API 的使用情况、费用以及多个大型语言模型（LLM）提供商（Anthropic、OpenAI、Google、Moonshot、Mistral、Cohere、Groq）的速率限制配额。该仪表板可以直接读取会话记录，无需依赖任何外部服务。当用户询问 API 费用、令牌使用情况、模型消耗、配额/速率限制、按模型或时间段的 usage 数据，或需要查看费用概览时，可使用此仪表板。触发关键词包括：“usage dashboard”、“API kosten”、“wie viel kostet”、“kontingent”、“rate limit”、“token verbrauch”、“cost dashboard”、“openclaw costs”、“spending overview”。
---
# OpenClaw 使用控制面板

该控制面板能够根据 OpenClaw 会话记录自动生成一个独立的 HTML 仪表板。完全无需依赖任何第三方库，仅使用 Python 3.8 及其标准库即可运行。

## 使用方法

```bash
# Real data (reads ~/.openclaw/agents/main/sessions/)
python3 scripts/usage-dashboard-generic.py [output.html]

# Demo mode (generates 30 days of realistic mock data)
python3 scripts/usage-dashboard-generic.py [output.html] --demo
```

默认输出文件：`~/openclaw-usage-dashboard.html`

如需更改会话数据路径，可通过设置环境变量 `OPENCLAW_ROOT` 来实现。

## 仪表板显示内容：

- **成本关键指标**：总花费、当日成本、API 调用次数、当前使用的模型、缓存命中率以及月度预测数据
- **模型配置**：来自 `openclaw.json` 的当前模型、默认模型及备用模型信息
- **Anthropic 使用量统计**：显示过去 5 小时和 7 天内的 API 使用量限制使用情况（需配置 `ANTHROPIC_API_KEY`）
- **甜甜圈图**：按模型划分的成本分布情况
- **小时级折线图**：按小时显示当天的 API 调用量
- **堆叠条形图**：按时间周期（日/周/月/年）显示成本分布
- **模型详情表**：提供每个模型的详细信息（包括调用次数和成本）
- **详情表与图表切换**：可随时在表格视图和条形图视图之间切换
- **预算跟踪**：允许设置每月的使用量限制，并通过进度条进行可视化展示；数据可持久保存在本地（localStorage）
- **CSV 导出**：可下载任意时间段的报表数据为 CSV 格式
- **提供者筛选**：支持根据提供者进行数据筛选

## 支持的提供者：

Anthropic、OpenAI、Google、Moonshot/Kimi、Mistral、Cohere、Groq — 提供超过 30 种内置定价模型的服务。

## 自定义功能：

### 添加新模型

只需修改脚本中的 `PRICES` 字典（包含每百万令牌的价格信息）：

```python
"provider/model-name": {"input": 2.50, "output": 10.00, "cache_read": 1.25, "cache_write": 2.50}
```

如需为模型添加自定义颜色或别名，可相应地更新 `MODEL_colors` 和 `ALIAS_MAP` 字典。

### 定价信息

请参考 `references/prices.md` 文件，了解所有提供者的当前定价详情。

## 系统要求：

- Python 3.8 及以上版本（仅使用标准库）
- 环境变量 `ANTHROPIC_API_KEY`（可选，用于实时显示使用量限制信息）