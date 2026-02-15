---
name: prediction-market-arbitrageur
description: 这是一个用于协调 topic-monitor、polymarket-odds 和 simmer-weather 等工具的元技能（meta-skill），旨在检测预测市场中的新闻与市场价格之间的异常波动。当用户需要一个清晰、分步的操作流程来监控突发信号、查看 Polymarket 的当前概率、计算置信度/价格差异，并基于这些信息做出套利决策时，可以使用该技能。
homepage: https://clawhub.ai
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"chart_with_upwards_trend","requires":{"bins":["python3","node","npx"],"env":["SIMMER_API_KEY"],"config":[]},"note":"Requires local installation of topic-monitor, polymarket-odds, and simmer-weather via ClawHub."}}
---

# 目的

此元技能用于将三个现有的 ClawHub 技能整合为一个因果套利工作流程：

1. 检测关于目标事件的高可信度新闻。
2. 从 Polymarket 获取当前市场预期的概率。
3. 比较新闻的置信度与市场概率。
4. 发出可操作的警报，并可选地提供具体的执行指导。

此技能不会替代底层技能，而是定义了如何正确地组合这些技能。

# 需要安装的技能

此元技能假设以下技能已在本机安装：

- `topic-monitor`（版本：最新 `1.3.4`）
- `polymarket-odds`（版本：最新 `1.0.0`）
- `simmer-weather`（版本：最新 `1.7.1`，支持执行代理模式）

使用 ClawHub 安装/更新这些技能：

```bash
npx -y clawhub@latest install topic-monitor
npx -y clawhub@latest install polymarket-odds
npx -y clawhub@latest install simmer-weather
npx -y clawhub@latest update --all
```

验证安装结果：

```bash
npx -y clawhub@latest list
python3 skills/topic-monitor/scripts/monitor.py --help
node skills/polymarket-odds/polymarket.mjs --help
python3 skills/simmer-weather/weather_trader.py --help
```

如果任何命令失败，请停止并报告缺失的依赖项或错误的安装路径。

# 输入参数（需要由任务管理器（LM）首先收集）

- `ceo_name`（首席执行官姓名）
- `company_name`（公司名称）
- `event_hypothesis`（事件假设，例如：`CEO X 在 30 天内辞职`）
- `market_query`（用于在 Polymarket 中搜索的查询）
- `topic_id`（在 `topic-monitor` 中的稳定标识符）
- `monitor_interval_minutes`（监控间隔时间，默认：`5` 分钟）
- `min_news_confidence`（最低新闻置信度，默认：`0.80`）
- `min_delta`（最小置信度差值，默认：`0.25`）
- `execution_mode`（执行模式，可选：`alert-only` 或 `execution-plan`）

如果缺少这些参数，请不要继续执行。

# 各技能的具体职责

## `topic-monitor`

用于持续发现和评估信号。

相关操作：
- 通过 `scripts/manage_topics.py` 配置主题。
- 通过 `scripts/monitor.py` 运行监控循环。
- 根据其评分逻辑生成优先级和置信度。
- 通过 `scripts/process_alerts.py --json` 获取警报队列。

这是新闻置信度数据的来源。

## `polymarket-odds`

用于查询实时市场概率。

相关操作：
- 使用 `search <query>` 查找匹配的事件/市场。
- 使用 `market <slug>` 查看特定市场的价格。
- 输出格式为百分比的概率值，需将其规范化到 `[0,1]` 范围内。

这是市场概率数据的来源。

## `simmer-weather`

虽然其主要设计用于策略制定，但在本套利流程中，它被用作执行代理的参考，因为它使用了 Simmer SDK 的交易端点以及模拟/实际执行的安全模式。

相关操作：
- 需要 `SIMMER_API_KEY` 进行身份验证。
- 支持模拟执行和实际执行模式。
- 提供交易流程的监控和位置检查功能。

在此元技能中，它不是信号生成工具，而是执行流程的参考。

# 标准的因果链

按照以下顺序执行这些技能：

1. `topic-monitor` 每 5 分钟发送一次心跳信号。
2. 匹配目标事件（例如：`resignation`、`ceo_name`、`company_name`）。
3. 仅接受高置信度的信号（`news_confidence >= 0.80`）。
4. 向 `polymarket-odds` 查询匹配的市场并获取当前概率。
5. 计算 `delta = news_confidence - market_probability`。
6. 如果 `delta >= min_delta`，触发套利警报。
7. 如果 `execution_mode=execution-plan`，输出具体的下一步操作；除非用户明确要求，否则不自动执行交易。

# 技能之间的数据协议

在做出决策之前，将所有值规范化为同一格式：

```json
{
  "topic_id": "ceo-resignation-acme",
  "event_hypothesis": "CEO X resigns",
  "news_confidence": 0.82,
  "news_signal_time": "2026-02-14T14:05:00Z",
  "market_slug": "will-ceo-x-resign",
  "market_probability": 0.40,
  "market_snapshot_time": "2026-02-14T14:06:00Z",
  "delta": 0.42,
  "decision": "buy_yes_candidate"
}
```

规则：
- 如果 `news_signal_time` 超过 30 分钟，则拒绝该信号。
- 如果市场数据超过 5 分钟未更新，则拒绝使用该数据。
- 不要直接比较百分比和十进制数，先将其转换为十进制形式。

# 任务管理器的执行流程

## 第一步：配置主题

```bash
python3 skills/topic-monitor/scripts/manage_topics.py add \
  "CEO Resignation - <company_name>" \
  --id <topic_id> \
  --query "<ceo_name> resignation <company_name> CEO stepping down" \
  --keywords "resignation,<ceo_name>,<company_name>,CEO,board,step down" \
  --frequency hourly \
  --importance high \
  --channels telegram \
  --context "Prediction market mispricing detection"
```

## 第二步：外部运行心跳循环（每 5 分钟一次）

```bash
python3 skills/topic-monitor/scripts/monitor.py --topic <topic_id> --force
python3 skills/topic-monitor/scripts/process_alerts.py --json
```

使用最新的评分结果作为置信度依据。

## 第三步：获取市场概率

```bash
node skills/polymarket-odds/polymarket.mjs search "<market_query>"
node skills/polymarket-odds/polymarket.mjs market <market_slug>
```

提取市场概率值并将其规范化（例如：`40% -> 0.40`）。

## 第四步：做出决策

决策公式：
- `delta = news_confidence - market_probability`
- 如果 `news_confidence >= min_news_confidence` 且 `delta >= min_delta`，则触发警报。

## 第五步：输出结果

如果触发警报，输出以下信息：

`🚨 套利机会：新闻得到确认，市场处于低活跃状态。建议买入。`

输出内容还包括以下结构化字段：
- `news_confidence`（新闻置信度）
- `market_probability`（市场概率）
- `delta`（置信度差值）
- `signal_age_minutes`（信号生成时间）
- `market_age_minutes`（市场数据更新时间）
- `recommendation`（交易建议）

# 输出模式

## `alert-only`

仅返回建议和置信度数据，不执行任何操作。

## `execution-plan`

除了建议外，还返回使用已安装的 `simmer-weather` 实时执行模式的具体操作步骤：
- 检查 API 密钥是否有效。
- 先进行模拟执行。
- 在执行任何实际操作前需要用户明确确认。

# 任务管理器的限制措施

- 不得伪造市场数据或价格信息。
- 如果置信度低于阈值，不得执行交易。
- 未经用户明确同意，不得发出实时交易指令。
- 当查询结果不明确时，必须明确显示不确定性。
- 当新闻可信度较低时，优先处理假阴性结果（即避免误报）。

# 失败处理

- 如果缺少某个技能，输出缺失的路径或命令。
- 如果缺少环境变量 `SIMMER_API_KEY`，则降级为仅发出警报模式。
- 如果未找到匹配的市场数据，返回 `no_trade` 并建议重新查询。
- 如果出现冲突的信号，需要两次独立的高置信度确认才能触发警报。

# 为什么需要这个元技能

如果没有这种协调机制，每个工具只能解决部分问题：
- `topic-monitor` 可以检测事件，但没有市场价格的背景信息。
- `polymarket-odds` 可以显示价格，但没有外部信号的置信度评估。
- `simmer-weather` 可以执行交易，但不是通用的事件检测工具。

这个元技能将这些工具整合为一个连贯的套利决策流程，使任务管理者能够一致地执行这些操作。