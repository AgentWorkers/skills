---
name: stock-copilot-pro
description: 高性能的全球股票分析辅助工具，由QVeris提供支持。该工具整合了报价数据、基本面分析、技术分析、新闻情绪以及X平台（X平台具体指代需根据上下文确定）的情绪信息，并通过自适应工具学习机制，提升分析的准确性和信号的质量。
env:
  - QVERIS_API_KEY
requirements:
  env_vars:
    - QVERIS_API_KEY
credentials:
  primary: QVERIS_API_KEY
  scope: read-only
  endpoint: https://qveris.ai/api/v1
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

## 功能概述

Stock Copilot Pro 可对股票进行端到端的分析，涵盖五个数据领域：

1. 市场报价/交易信息
2. 基本面指标
3. 技术指标（RSI/MACD/MA）
4. 新闻与市场情绪
5. X 情绪数据

分析完成后，它会生成一份结构化的 Markdown 报告，内容包含：`总结 / 基本面分析 / 技术分析 / 市场情绪 / 风险评估 / 结论`。

## 主要优势

- 动态工具学习机制，可随时间提升分析质量
- 支持多种数据提供商和市场，具备强大的备用策略
- 能够处理美国、香港和中国的股票数据
- 输出结果结构化，既适合分析师阅读，也适合机器处理
- 严格保护敏感信息（如 API 密钥）和运行时的状态数据

## 核心工作流程

1. 对股票代码进行标准化处理，并确定数据来源（美国、香港、中国或全球）
2. 根据工具功能（报价、基本面分析、技术指标、市场情绪分析等）进行搜索
3. 按照 `成功率`、响应延迟和参数匹配程度对候选工具进行排序
4. 首先尝试优先级较高的工具，若失败则使用备用工具
5. 进行质量检查：
   - 确保关键字段齐全
   - 数据是否为最新
   - 数据来源之间是否存在不一致
6. 生成包含置信度评分和明确注意事项的报告

## 命令行接口

主要脚本：`scripts/stock_copilot_pro.mjs`

- 分析单个股票：
  ```
  node scripts/stock_copilot_pro.mjs analyze --symbol AAPL --market US --mode comprehensive
  ```
- 比较多个股票：
  ```
  node scripts/stock_copilot_pro.mjs compare --symbols AAPL,MSFT --market US --mode comprehensive
  ```

## 输出格式

- `markdown`（默认格式）：适合人类阅读的报告
- `json`：适合机器处理的合并数据格式

## 动态进化机制

- 运行时的学习状态存储在 `.evolution/tool-evolution.json` 文件中
- 采用“积极”的准入策略：一次成功的工具执行即可进入工具执行队列
- 未来的执行会优先选择之前成功过的工具，以提高执行可靠性

## 安全性与数据披露

- 仅使用 `QVERIS_API_KEY` 进行 API 调用
- 所有 API 调用均通过 HTTPS 安全传输
- 不会将 API 密钥存储在日志、报告或运行状态数据中
- 本工具仅用于研究用途，不提供投资建议