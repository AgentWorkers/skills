---
name: stock-copilot-pro
description: OpenClaw 的股票分析功能适用于美国/香港/中国市场。该功能整合了 QVeris 提供的数据源（包括 THS、Caidazi、Alpha Vantage、Finnhub 和 X 情感分析数据），提供实时报价、基本面分析、技术指标、新闻资讯、晨间/晚间简报以及实用的投资建议。
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
runtime: { language: nodejs, node: ">=18" }
install: { mechanism: local-skill-execution, external_installer: false, package_manager_required: false }
persistence: { writes_within_skill_dir: [config/watchlist.json, .evolution/tool-evolution.json], writes_outside_skill_dir: false }
security: { full_content_file_url: { enabled: true, allowed_hosts: [qveris.ai], protocol: https } }
network:
  outbound_hosts:
    - qveris.ai
metadata: {"openclaw":{"requires":{"env":["QVERIS_API_KEY"]},"primaryEnv":"QVERIS_API_KEY","homepage":"https://qveris.ai"}}
auto_invoke: true
source: https://qveris.ai
examples:
  - "Analyze AAPL with a comprehensive report"
  - "Technical analysis for 0700.HK"
  - "Compare AAPL, MSFT, NVDA"
  - "Give me fundamentals and sentiment for 600519.SS"
---
# Stock Copilot Pro

基于QVeris的全局多源股票分析工具。

## 相关关键词

OpenClaw、股票分析技能、AI股票辅助工具、中国A股、港股、美股、定量分析、基本面分析、技术分析、情绪分析、行业热点追踪、晨间/晚间简报、关注列表、投资组合监控、QVeris API、THS iFinD、Caidazi、Alpha Vantage、Finnhub、X情感分析、投资研究助手

## 支持的功能

- 单股分析（`analyze`）：估值、质量评估、技术指标分析、情绪分析、风险/时机判断
- 多股比较（`compare`）：跨股票排名及投资组合视图
- 关注列表/持仓管理（`watch`）：添加/删除持仓和关注列表中的股票
- 晨间/晚间简报（`brief`）：基于持仓的每日可操作性简报
- 行业热点追踪（`radar`）：多源信息汇总，识别投资主题
- 多格式输出：`markdown`、`json`、`chat`
- 支持与OpenClaw大型语言模型（LLM）集成

## 数据来源

- 核心数据接口：`qveris.ai`（需要`QVERIS_API_KEY`）
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
- X/Twitter情感分析及热点话题：
  - `qveris_social.x_domain_hot_topics`
  - `qveris_social.x_domain_hot_events`
  - `qveris_social.x_domain_new_posts`
  - `x_developer.2.tweets.search.recent`

## 功能概述

Stock Copilot Pro提供端到端的股票分析服务，涵盖五个数据领域：

1. 市场报价/交易环境
2. 基本面指标
3. 技术指标（RSI/MACD/MA）
4. 新闻与情绪分析
5. X平台的情感数据

该工具生成内容丰富的分析师报告，包括：
- 价值投资评分卡
- 基于事件的时机判断
- 安全边际估算
- 基于投资逻辑的框架（驱动因素/风险/情景/KPI）
- 多种投资策略（价值型/平衡型/成长型/交易型）
- 基于新闻和X平台数据的事件热点追踪
- 基于情景的建议

## 主要优势

- 通过`references/tool-chains.json`文件实现工具的确定性路由
- 采用进化（Evolution）v2参数模板机制，减少参数错误
- 支持美国/香港/中国市场的股票处理
- 输出格式结构化，适合分析师阅读和机器处理
- 严格保护敏感信息及运行时状态的安全性

## 核心工作流程

1. 解析用户输入的股票代码及市场类型（支持公司别名，例如：中文名称 -> `600089.SH`）
2. 按功能搜索相关工具（报价、基本面、技术指标、情绪分析、X平台情感分析）
3. 首先使用预设的工具链进行搜索（考虑市场特性），若未找到则使用通用搜索方式
   - 对于中国/香港地区的情绪分析，优先使用`caidazi`渠道（报告/新闻/微信）
   - 对于中国/香港地区的基本面数据，优先使用THS的财务报表（收入/资产负债表/现金流），必要时再使用公司基本信息
4. 执行前尝试使用进化参数模板；若模板不可用，则使用默认参数生成方式
5. 进行质量检查：
   - 检查关键字段是否缺失
   - 数据是否最新
   - 来源数据是否一致
6. 生成分析师报告，包含：
   - 综合评分
   - 安全边际
   - 基于事件的时机判断
   - 结构化的投资逻辑（驱动因素/风险/情景/KPI）
   - 事件热点追踪及潜在投资机会
   - 根据投资策略定制的执行方案
   - 标准可读输出（默认格式）；支持可选的完整证据记录（`--evidence`参数）

## 预设选项

- **偏好设置**：
  - `--horizon short|mid|long`：时间范围（短期/中期/长期）
  - `--risk low|mid|high`：风险偏好（低/中/高）
  - `--style value|balanced|growth|trading`：投资风格（价值型/平衡型/成长型/交易型）
  - `--actionable`：是否包含可执行性建议
  - `--skip-questionnaire`：跳过偏好设置问答环节

## 命令行接口

主要脚本：`scripts/stock_copilot_pro.mjs`

- 分析单只股票：
  - `node scripts/stock_copilot_pro.mjs analyze --symbol AAPL --market US --mode comprehensive`
  - `node scripts/stock_copilot_pro.mjs analyze --symbol "<company-name>" --mode comprehensive`
- 比较多只股票：
  - `node scripts/stock_copilot_pro.mjs compare --symbols AAPL,MSFT --market US --mode comprehensive`
- 管理关注列表：
  - `node scripts/stock_copilot_pro.mjs watch --action list`
  - `node scripts/stock_copilot_pro.mjs watch --action add --bucket holdings --symbol AAPL --market US`
  - `node scripts/stock_copilot_pro.mjs watch --action remove --bucket watchlist --symbol 0700.HK --market HK`
- 生成简报：
  - `node scripts/stock_copilot_pro.mjs brief --type morning --format chat`
  - `node scripts/stock_copilot_pro.mjs brief --type evening --format markdown`
- 运行行业热点追踪：
  - `node scripts/stock_copilot_pro.mjs radar --market GLOBAL --limit 10`

## OpenClaw定时任务（晨间/晚间简报及热点追踪）

要设置OpenClaw的定时任务（如晨间简报、晚间简报或每日热点追踪），请使用官方的OpenClaw cron格式，并通过CLI或Gateway cron工具创建任务。切勿直接编辑`~/.openclaw/cron/jobs.json`文件。

- 参考示例：`config/openclaw-cron.example.json`中的`jobs`数组；每个条目包含一个`cron.add`对象（字段：`name`、`schedule`、`sessionTarget`、`payload`、`delivery`）
- 例如（晨间简报）：`openclaw cron add --name "Stock morning brief" --cron "0 9 * * 1-5" --tz Asia/Shanghai --session isolated --message "使用stock-copilot-pro生成晨间简报：run brief --type morning --max-items 8 --format chat" --announce`；若需发送至Feishu平台，添加`--channel feishu --to <group-or-chat-id>`

## 中国/香港地区支持细节

- 支持输入公司名称，并自动解析为对应的股票代码及市场类型
- 情绪分析优先使用`caidazi`渠道（研究报告、新闻、微信/公众号）
- 基本面数据优先使用THS的财务报表接口，包括：
  - 收入
  - 净利润
  - 总资产
  - 总负债
  - 经营现金流
  - 行业
  - 主营业务
  - 标签

## 输出格式

- `markdown`（默认）：人类可读的报告格式
- `json`：机器可读的合并数据
- `chat`：适合聊天应用的分段输出格式
- `summary-only`：简洁的摘要输出格式

## 其他选项

- `--horizon short|mid|long`：时间范围选项
- `--risk low|mid|high`：风险偏好设置
- `--style value|balanced|growth|trading`：投资风格选择
- `--actionable`：是否包含可执行性建议
- `--skip-questionnaire`：跳过偏好设置问答环节

## 动态进化机制

- 运行时的学习状态存储在`.evolution/tool-evolution.json`文件中
- 成功执行后可以更新工具参数模板
- 存储`param_templates`和`sample_successful_params`以供后续使用
- 工具优先级由`tool-chains.json`文件控制
- 使用`--no-evolution`参数可禁用动态进化功能

## 安全性与数据隐私

- 仅使用`QVERIS_API_KEY`进行API调用
- 通过HTTPS协议访问QVeris API
- 为保证数据完整性，允许访问`qveris.ai`下的HTTPS链接
- 不在日志、报告或运行时状态中存储API密钥
- 运行时数据仅保存在`.evolution/tool-evolution.json`文件中
- 关注列表状态存储在`config/watchlist.json`文件中（从`config/watchlist.example.json`加载）
- OpenClaw定时任务的配置请参考`config/openclaw-cron.example.json`；使用`openclaw cron add`或Gateway cron工具创建任务，切勿直接修改`~/.openclaw/cron/jobs.json`文件（格式不匹配可能导致解析错误）
- 外部来源链接默认隐藏；需通过`--include-source-urls`参数显式显示
- 本工具不执行任何软件安装或任意命令操作
- 仅提供研究数据，不提供投资建议

## 单股分析指南

在分析`analyze`输出时，需以资深买方分析师的身份撰写专业且不过度的分析报告。

### 必需的输出内容（7个部分）

0. **数据概览**：
  - 提供基于`data`字段生成的简洁指标表格
  - 包括：价格/变化幅度、市值、市盈率/市净率、利润率、收入、净利润、RSI、52周价格范围

```markdown
| Metric | Value |
|--------|-------|
| Price | $264.58 (+1.54%) |
| Market Cap | $3.89T |
| P/E | 33.45 |
| P/B | 57.97 |
| Profit Margin | 27% |
| Revenue (TTM) | $394B |
| Net Profit | $99.8B |
| RSI | 58.3 |
| 52W Range | $164 - $270 |
```

1. **关键观点（30秒内提供）**：
  - 一句话的结论：买入/持有/避免买入的理由

2. **投资逻辑**：
  - 多头观点：2个要点（增长驱动因素、竞争优势）
  - 熊市观点：2个要点（估值/风险/时机）
  - 最终判断：当前情况下的主要考虑因素

3. **估值与关键水平**：
  - 市净率与同行或历史水平的对比（低估/合理/高估）
  - 关键价格点：支撑位、阻力位、止损位

4. **投资建议**：
  - 根据持仓状态提供不同建议：
    - 无持仓
    - 轻量持仓
    - 重仓/亏损持仓
  - 每条建议需包含具体触发条件/价格/执行标准

5. **风险监控**：
  - 最主要的风险点及判断依据（哪些因素可能导致投资逻辑失效）

6. **数据来源**：
  - 在报告末尾说明数据来源及使用的QVeris接口

```markdown
> Data powered by [QVeris](https://qveris.ai) | Sources: Alpha Vantage (quote/fundamentals), Finnhub (news sentiment), X/Twitter (social sentiment) | Generated at 2026-02-22T13:00:00Z
```

### 质量要求

- 避免数据堆砌；每个数值都需要附带解释
- 所有数据必须基于实际数据；不得虚构数字
- 保持简洁但信息完整（建议叙述长度为250-500字）
- 提供可操作的指导及时间范围
- 使用英文表示股票代码和技术术语

## 日报分析指南

生成适用于OpenClaw对话的晨间/晚间简报。

### 晨间简报

- **市场概览**：市场风险状况及夜间重要事件
- 提供指数概览（指数名称、价格、变化百分比、时间戳）

- **持仓检查**：需要关注的持仓及其价格/变化百分比/评级

- **热点追踪**：哪些行业热点会影响持仓

- **今日计划**：具体的关注指标/事件/执行方案

- **数据来源**：简报中使用的QVeris接口及数据来源

### 晚间简报

- **会议回顾**：指数/行业/投资组合的简要回顾
- 最重要的持仓变化及原因（提供量化数据）

- **投资逻辑更新**：投资逻辑是否发生变化

- **明日计划**：明确的条件及行动方案

- **数据来源**：简报中使用的QVeris接口及数据来源

### 质量要求

- 优先考虑用户持仓情况，而非泛化市场评论
- 尽可能量化数据变化（百分比/数量）

- 保持简洁并突出决策要点
- 在结尾提供数据来源信息以提高可追溯性和可信度

## 热点追踪分析指南

将信号分类为可投资的主题，并提供简洁的操作建议。

### 输出要求

- **主题**：明确的可投资标签
- **驱动因素**：变化的原因及影响
- **影响范围**：受益方/受损方及影响程度
- **建议**：具体的触发条件或执行标准
- **风险提示**：可能失效的因素或需要监控的信号
- **数据来源**：每个主题的来源信息

### 执行规则

- 每个主题最多分为3-5个类别
- 多源验证信息；对于仅来自社交媒体的信号，降低信任度
- 区分短期交易和中期投资策略
- 每个主题的描述保持简洁（建议不超过200字）
- 在结尾列出参与热点追踪的QVeris接口