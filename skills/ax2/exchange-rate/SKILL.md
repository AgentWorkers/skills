---
name: exchange-rate
description: 实时外汇和加密货币汇率查询及金额转换功能，由 QVeris 提供支持。支持多家数据提供商（Alpha Vantage、Twelve Data），并在数据源不可用时自动切换到备用数据源以确保数据可靠性。
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
  - "What is the USD to EUR exchange rate?"
  - "Convert 1000 USD to JPY"
  - "CNY to USD rate"
  - "100 EUR to GBP"
---
# 汇率

使用 QVeris 工具获取实时货币汇率并进行转换。

## 该功能的用途

“汇率”功能提供以下服务：
1. **汇率查询** – 查找两种货币之间的当前汇率（例如 USD/EUR、CNY/JPY）。
2. **金额转换** – 根据当前汇率将一种货币的金额转换为另一种货币。

支持的货币对包括外汇对和常见的法定货币对；如果工具支持，还可以选择特定的历史日期进行汇率或金额转换。

## 主要优势：
- 仅使用 QVeris API：用户可以根据功能搜索相应的工具并执行操作，无需依赖硬编码的提供商列表。
- 当某个工具出现故障或无法使用时，系统会自动切换到其他可用的提供商（例如 Alpha Vantage、Twelve Data）。
- 与其他功能共享相同的认证凭据：仅需 `QVERIS_API_KEY`。
- 该功能仅用于读取数据，不会产生任何副作用，适用于旅行、交易和报告等场景。

## 核心工作流程：
1. 解析用户输入的指令：可能是查询汇率（`from_currency, to_currency`）或进行金额转换（`from_currency, to_currency, amount`）。
2. 在 QVeris 中搜索相应的工具（例如：“实时货币汇率”或“货币转换”）。
3. 根据成功率、响应延迟以及参数匹配度对搜索结果进行排序。
4. 构建请求参数：查询汇率时使用 `from_currency`/`to_currency` 或 `symbol`（例如 `EUR/USD`）；进行金额转换时需要提供 `amount`。
5. 执行选定的工具，超时时间为 5 秒；如果执行失败，则尝试下一个工具。
6. 返回格式化的汇率结果和/或转换后的金额（格式为 Markdown 或 JSON）。

## 命令行接口：

主要脚本：`scripts/exchange_rate.mjs`

- 仅查询汇率：
  - `node scripts/exchange_rate.mjs rate --from USD --to EUR`
  - `node scripts/exchange_rate.mjs rate --from CNY --to USD`
- 进行金额转换：
  - `node scripts/exchange_rate.mjs convert --from USD --to JPY --amount 1000`
  - `node scripts/exchange_rate.mjs convert --from EUR --to GBP --amount 500`

可选参数：
- `--date YYYY-MM-DD`：用于查询指定日期的历史汇率或金额转换结果（如果工具支持）。
- `--format json`：输出结果为 JSON 格式，便于机器读取。

## 安全性与数据披露：
- 仅使用 `QVERIS_API_KEY`，不涉及任何其他敏感信息。
- 所有请求均通过 HTTPS 协议发送至 QVeris，无需安装任何额外的软件或执行任意命令。
- 输出结果仅供参考，不构成财务建议或合同依据。