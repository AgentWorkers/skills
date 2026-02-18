---
name: stock-copilot-pro
description: OpenClaw 提供针对美国/香港/中国市场的股票分析功能。该工具整合了 QVeris 的多个数据源（THS、Caidazi、Alpha Vantage、Finnhub、X 情感分析），提供实时报价、基本面数据、技术分析指标、新闻资讯、每日晨报/晚报，以及实用的投资建议。
env:
  - QVERIS_API_KEY
requirements:
  env_vars:
    - QVERIS_API_KEY
credentials:
  required:
    - QVERIS_API_KEY
  primary: QVERIS_API_KEY
  scope: read-only
  endpoint: https://qveris.ai/api/v1
network:
  outbound_hosts:
    - qveris.ai
auto_invoke: true
source: https://qveris.ai
examples:
  - "Analyze AAPL with a comprehensive report"
  - "Technical analysis for 0700.HK"
  - "Compare AAPL, MSFT, NVDA"
  - "Give me fundamentals and sentiment for 600519.SS"
---
# Stock Copilot Pro

利用 QVeris 进行全球多源股票分析。

## 相关关键词

OpenClaw、股票分析工具、AI 股票辅助系统、中国 A 股、香港股票、美国股票、定量分析、基本面分析、技术分析、情绪分析、行业热点追踪、晨间/晚间简报、关注列表、投资组合监控、QVeris API、THS iFinD、Caidazi、Alpha Vantage、Finnhub、X 情绪分析、投资研究助手

## 支持的功能

- 单股分析（`analyze`）：估值、质量评估、技术分析、情绪分析、风险/时机判断
- 多股比较（`compare`）：跨股票排名及投资组合视图
- 关注列表/持仓管理（`watch`）：添加/删除持仓和关注列表中的股票
- 晨间/晚间简报（`brief`）：基于持仓的每日可操作性简报
- 行业热点追踪（`radar`）：多源信息聚合，识别投资主题
- 多格式输出：`markdown`、`json`、`chat`
- 支持与 OpenClaw LLM 的集成：结构化数据与 `SKILL.md` 格式的叙述性输出

## 数据来源

- 核心数据接口：`qveris.ai`（需要 `QVERIS_API_KEY`）
- 中国/香港股票报价及基本面数据：
  - `ths_ifind.real_time_quotation`
  - `ths_ifind.financial_statements`
  - `ths_ifind.company_basics`
  - `ths_ifind.history_quotation`
- 中国/香港新闻及研究资料：
  - `caidazi.news.query`
  - `caidazi.report.query`
  - `caidazi.search.hybrid.list`
  - `caidazi.search.hybrid_v2.query`
- 全球新闻情绪数据：
  - `alpha_news_sentiment`
  - `finnhub.news`
- X/Twitter 情绪及热点话题：
  - `qveris_social.x_domain_hot_topics`
  - `qveris_social.x_domain_hot_events`
  - `qveris_social.x_domain_new_posts`
  - `x_developer.2.tweets.search.recent`

## 功能概述

Stock Copilot Pro 提供端到端的股票分析服务，涵盖五个数据领域：

1. 市场报价/交易信息
2. 基本面指标
3. 技术分析指标（RSI/MACD/MA）
4. 新闻与情绪数据
5. X 情绪分析

该工具生成内容丰富的分析师报告，包括：
- 价值投资评分卡
- 基于事件的时机判断
- 安全边际估算
- 基于投资逻辑的投资框架（驱动因素/风险/情景/关键绩效指标）
- 多种投资策略（价值型/平衡型/成长型/交易型）
- 基于新闻和 X 情绪的热点主题推荐
- 根据情景的建议

## 主要优势

- 通过 `references/tool-chains.json` 文件实现工具的确定性路由
- 采用进化版本 2 的参数模板机制，减少参数错误
- 支持美国/香港/中国市场的股票处理
- 输出格式结构化，适合分析师阅读和机器处理
- 严格管理敏感信息和运行时状态

## 核心工作流程

1. 解析用户输入的股票代码及市场类型（支持公司别名，例如：中文名称 -> `600089.SH`）
2. 按功能搜索相应工具（报价、基本面、技术指标、情绪分析、X 情绪分析）
3. 首先使用预定义的工具链进行搜索（考虑市场特性），若未找到则使用通用搜索方式：
   - 对于中国/香港地区的情绪数据，优先使用 `caidazi` 的新闻/报告/微信渠道
   - 对于中国/香港地区的基本面数据，优先使用 THS 的财务报表（收入/资产负债表/现金流），必要时使用公司基本信息
4. 执行前尝试使用进化版本参数模板；若模板不可用，则使用默认参数生成器
5. 进行质量检查：
   - 检查关键字段是否缺失
   - 确保数据时效性
   - 检查数据来源是否一致
6. 生成分析师报告，包含：
   - 综合评分
   - 安全边际
   - 基于事件的时机判断
   - 结构化的投资逻辑（驱动因素/风险/情景/关键绩效指标）
   - 热点主题推荐
   - 根据投资策略制定的执行方案
   - 可选的输出格式（默认为 `markdown`，支持 `--evidence` 选项以显示完整数据来源）

## 预设偏好设置

- 如果未设置偏好选项，脚本会首先显示问卷
- 可通过 `--skip-questionnaire` 参数跳过问卷环节

## 命令行接口

主要脚本：`scripts/stock_copilot_pro.mjs`

- 分析单只股票：
  `node scripts/stock_copilot_pro.mjs analyze --symbol AAPL --market US --mode comprehensive`
  `node scripts/stock_copilot_pro.mjs analyze --symbol "<company-name>" --mode comprehensive`
- 比较多只股票：
  `node scripts/stock_copilot_pro.mjs compare --symbols AAPL,MSFT --market US --mode comprehensive`
- 管理关注列表：
  `node scripts/stock_copilot_pro.mjs watch --action list`
  `node scripts/stock_copilot_pro.mjs watch --action add --bucket holdings --symbol AAPL --market US`
  `node scripts/stock_copilot_pro.mjs watch --action remove --bucket watchlist --symbol 0700.HK --market HK`
- 生成简报：
  `node scripts/stock_copilot_pro.mjs brief --type morning --format chat`
  `node scripts/stock_copilot_pro.mjs brief --type evening --format markdown`
- 运行行业热点追踪：
  `node scripts/stock_copilot_pro.mjs radar --market GLOBAL --limit 10`

## OpenClaw 定时任务（晨间/晚间简报和热点追踪）

要设置 OpenClaw 的定时任务（如晨间简报、晚间简报或每日热点追踪），请使用官方的 OpenClaw 定时格式，并通过 CLI 或 Gateway 定时工具创建任务。切勿直接编辑 `~/.openclaw/cron/jobs.json` 文件。

- 参考示例：`config/openclaw-cron.example.json` 中的 `jobs` 数组，每个条目包含一个 `cron.add` 对象（字段：`name`、`schedule`、`sessionTarget`、`payload`、`delivery`）
- 示例（晨间简报）：`openclaw cron add --name "Stock morning brief" --cron "0 9 * * 1-5" --tz Asia/Shanghai --session isolated --message "Use stock-copilot-pro to generate morning brief: run brief --type morning --max-items 8 --format chat" --announce`；若需发送到 Feishu，添加 `--channel feishu --to <group-or-chat-id>`
- 注意：使用旧格式（如将 `schedule` 作为字符串、`command` 或 `delivery_channels` 作为数组）或直接将示例代码粘贴到 `jobs.json` 中可能导致解析失败或系统崩溃

## 中国/香港地区支持细节

- 支持输入公司名称，并自动解析为对应的股票代码和市场类型
- 情绪数据优先使用 `caidazi` 的新闻/报告/微信渠道
- 基本面数据优先使用 THS 的财务报表接口，包括以下字段：
  - 收入
  - 净利润
  - 总资产
  - 总负债
  - 经营现金流
  - 行业
  - 主要业务
  - 标签

## 输出格式

- `markdown`（默认）：适合人类阅读的格式
- `json`：适合机器处理的合并数据格式
- `chat`：适合聊天应用的分段输出格式
- `summary-only`：简洁的摘要输出格式

## 预设参数与事件选项

- 预设偏好选项：
  - `--horizon short|mid|long`：时间范围（短期/中期/长期）
  - `--risk low|mid|high`：风险偏好（低/中/高）
  - `--style value|balanced|growth|trading`：投资风格（价值型/平衡型/成长型/交易型）
  - `--actionable`：是否包含可执行的操作建议
  - `--skip-questionnaire`：跳过问卷环节

- 事件追踪选项：
  - `--event-window-days 7|14|30`：事件窗口天数（7/14/30 天）
  - `--event-universe global|same_market`：事件范围（全球/同一市场）
  - `--event-view timeline|theme`：事件展示方式（时间线/主题）

## 动态进化机制

- 运行时的学习状态保存在 `.evolution/tool-evolution.json` 文件中
- 成功执行一次后，系统会更新参数模板
- 存储 `param_templates` 和 `sample_successful_params` 以供后续使用
- 工具优先级由 `tool-chains.json` 文件控制
- 可使用 `--no-evolution` 参数禁用运行时学习功能

## 安全性与数据保护

- 仅使用 `QVERIS_API_KEY`
- 通过 HTTPS 调用 QVeris 的 API
- 保留 `full_content_file_url` 的获取功能以确保数据完整性，但仅允许使用 `qveris.ai` 下的 HTTPS URL
- 不在日志、报告或运行时状态中存储 API 密钥
- 运行时数据仅保存在 `.evolution/tool-evolution.json` 文件中
- 关注列表状态保存在 `config/watchlist.json` 文件中（从 `config/watchlist.example.json` 自动加载）
- OpenClaw 定时任务的配置请参考 `config/openclaw-cron.example.json`，使用官方格式（`schedule.kind`、`payload.kind`、`sessionTarget` 等）通过 `openclaw cron add` 或 Gateway 定时工具创建任务；切勿直接修改 `~/.openclaw/cron/jobs.json` 文件（格式不匹配可能导致解析失败）
- 外部来源 URL 默认隐藏；需通过 `--include-source-urls` 显式启用显示
- 该工具不执行任何软件安装或任意命令操作
- 仅提供研究数据，不提供投资建议

## 单股分析指南

在分析结果时，应像资深买方分析师一样提供专业且客观的报告：

### 必需的输出内容（5 个部分）

1. **关键结论（30 秒内）**
   - 买入/持有/避免的建议及理由

2. **投资逻辑**
   - 多头观点：2 个要点（增长驱动因素/有利条件）
   - 熊市观点：2 个要点（估值/风险/时机）
   - 综合判断：当前最关键的因素

3. **估值与关键水平**
   - 相对市盈率/市净率与历史百分位比较（低估/合理/高估）
   - 关键价格水平：当前价格、支撑位、阻力位、止损位

4. **投资建议（必选）**
   - 根据持仓情况提供不同建议：
     - 无持仓
     - 轻量持仓
     - 重仓/亏损持仓
   - 每条建议需包含具体触发条件/价格/执行标准

5. **风险监控**
   - 最主要的 2-3 个风险点及判断依据（可能导致投资逻辑错误的因素）

### 质量要求

- 避免简单的数据堆砌；每个关键数据点都需附带解释
- 语言简洁明了（建议字数在 250-500 字之间）
- 提供可操作的指导建议及时间窗口
- 使用英文表示股票代码和技术术语

## 日报分析指南

生成适用于 OpenClaw 对话的晨间/晚间简报：

### 晨间简报

1. **市场概况**：市场风险状况及夜间重要事件
2. **持仓检查**：需要立即处理的持仓
3. **热点主题影响**：哪些热点主题与持仓相关
4. **今日计划**：具体的关注点/执行方案

### 晚间简报

1. **会议回顾**：指数/行业/投资组合的简要总结
2. **持仓变动**：表现最佳的/最差的持仓及其原因
3. **投资逻辑更新**：投资逻辑是否发生变化
4. **明日计划**：明确的操作建议和条件

### 质量要求

- 重点关注用户持仓情况，而非泛化市场评论
- 尽可能量化变化（百分比/具体数值）
- 语言简洁，注重决策导向

## 热点主题分析指南

将分析结果归纳为可投资的主题，并提供简洁的操作建议：

### 必需的输出内容（每个主题）

- **主题**：明确的、可投资的标签
- **驱动因素**：变化的原因及影响
- **影响范围**：受益方/受损方及影响程度
- **建议**：具体的操作建议或价格阈值
- **风险提示**：可能导致投资逻辑失效的关键因素

### 执行规则

- 最多归纳 3-5 个主题
- 多源验证信息；对于仅来自社交媒体的数据，降低信任度
- 区分短期交易和中期投资策略
- 每个主题的描述尽量简洁（建议不超过 200 字）