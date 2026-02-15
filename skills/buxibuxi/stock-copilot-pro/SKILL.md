---
name: stock-copilot-pro
description: 由 QVeris 提供支持的高性能全球股票分析辅助工具。该工具整合了报价数据、基本面分析、技术分析、新闻情绪以及社交媒体的情绪数据，并通过自适应工具学习机制，提升分析的准确性和信号的质量。
env:
  - QVERIS_API_KEY
credentials:
  required:
    - QVERIS_API_KEY
  primary_env: QVERIS_API_KEY
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

使用 QVeris 进行全球多源股票分析。

## 该功能的用途

Stock Copilot Pro 可以通过五个数据领域进行端到端的股票分析：
1. 市场报价/交易信息
2. 基本面指标
3. 技术指标（RSI/MACD/MA）
4. 新闻和情绪分析
5. X 情绪分析

然后，它会生成一份内容丰富的分析师报告，其中包含：
- 价值投资评分卡
- 事件时机判断与避免追涨的策略
- 安全边际估算
- 基于不同市场情景的建议
- 标准可读的输出格式（默认）+ 可选的全证据追踪（`--evidence` 参数）

## 主要优势

- 通过 `references/tool-chains.json` 文件实现工具的确定性路由
- 采用 Evolution v2 参数模板机制，减少参数错误的发生
- 具备强大的跨提供商和市场的数据处理能力
- 支持美国/香港/中国市场的股票分析
- 输出格式既适合分析师阅读，也适合机器处理
- 对敏感信息和运行时状态采取严格的安全管理措施

## 核心工作流程

1. 将用户输入解析为股票代码和市场代码（支持公司名称别名，例如 `特变电工` -> `600089.SH`）
2. 根据功能搜索相应的分析工具（报价、基本面数据、技术指标、情绪分析、X 情绪分析）
3. 首先尝试使用预定义的工具链进行搜索（考虑市场特性），如果找不到合适的工具，则切换到通用搜索方式：
   - 对于中国/香港地区的情绪分析，优先使用 `caidazi` 渠道（研究报告、新闻、微信）
   - 对于中国/香港地区的基本面数据，优先使用 THS 的财务报表（收入/资产负债表/现金流），如果这些数据不可用，则使用公司基本信息
4. 在执行分析之前，尝试使用参数模板；如果模板不可用，则使用默认的参数生成机制
5. 进行质量检查：
   - 确保关键字段齐全
   - 数据的时效性
   - 来源数据的一致性
6. 生成分析师报告，内容包括：
   - 综合评分
   - 安全边际
   - 基于事件的时机判断与风险规避策略
   - 市场情景建议
   - 当启用 `--evidence` 参数时，还包括解析后的原始数据或证据

## 命令行接口

主要脚本：`scripts/stock_copilot_pro.mjs`

- 分析单个股票：
  `node scripts/stock_copilot_pro.mjs analyze --symbol AAPL --market US --mode comprehensive`
  `node scripts/stock_copilot_pro.mjs analyze --symbol "特变电工" --mode comprehensive`
- 比较多个股票：
  `node scripts/stock_copilot_pro.mjs compare --symbols AAPL,MSFT --market US --mode comprehensive`

## 中国/香港地区的支持细节

- 支持输入公司名称，并自动将其解析为对应的市场代码和股票代码
- 情绪分析优先使用 `caidazi` 渠道（研究报告、新闻、微信/公众号）
- 基本面数据分析优先使用 THS 的财务报表接口，同时会补充公司基本信息：
  - 收入
  - 净利润
  - 总资产
  - 总负债
  - 经营现金流
  - 行业
  - 主营业务
  - 标签

## 输出格式

- `markdown`（默认）：适合人类阅读的报告格式
- `json`：适合机器处理的合并数据格式

## 动态进化机制

- 运行时的学习状态存储在 `.evolution/tool-evolution.json` 文件中
- 每次成功执行后，系统会更新工具参数模板
- 存储的参数模板和成功执行的参数可供后续使用
- 工具的优先级由 `tool-chains.json` 文件控制
- 可以使用 `--no-evolution` 参数禁用运行时的学习功能

## 安全性与数据披露

- 仅使用 `QVERIS_API_KEY` 进行 API 调用
- 所有 API 请求均通过 HTTPS 协议传输
- 不会将 API 密钥存储在日志、报告或运行时状态文件中
- 运行时数据的持久化仅限于 `.evolution/tool-evolution.json` 文件（仅包含元数据和参数模板）
- 该脚本不执行任何软件包的安装或任意命令执行操作
- 仅提供研究用途的数据，不提供投资建议