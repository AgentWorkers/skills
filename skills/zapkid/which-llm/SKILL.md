---
name: Decision Economic Optimizer
description: 具有 HTTP 402 错误响应及结果信用机制的确定性决策排序 API。
version: 0.1.0
homepage: https://which-llm.com
credentials_required: true
primary_credential: WALLET_CREDENTIALS
sensitivity: high
always_on: false
disable_model_invocation: false
install_mechanism: instruction_only
writes_to_disk_on_install: false
downloads_code_on_install: false
---
# Which-LLM：基于结果的决策优化器

## 概述

当您需要在明确的成本和质量等约束条件下确定使用哪个大型语言模型（LLM）时，可以使用此技能。

该技能用于调用Which-LLM API，但它本身并不运行任何LLM。对于付费请求，AI机器人需要访问加密钱包。

## 适用场景

- 选择成本最低且仍满足质量要求的模型
- 在首选模型失败时选择备用模型
- 使模型选择过程具有确定性并可被审计
- 报告执行结果，并为后续请求赚取信用点数

## 快速参考

- **API基础URL：** `https://api.which-llm.com`
- **主要付费端点：** `POST /decision/optimize`
- **结果端点：** `POST /decision/outcome`
- **免费查询端点：** `GET /capabilities`, `GET /pricing`, `GET /status`
- **支付货币：** USDC
- **支持的链：** Base, Ethereum, Arbitrum, Optimism, Avalanche

## 注册表要求

- **主要凭证：** `WALLET_CREDENTIALS`
- **安装方式：** 仅提供安装指令
- **安装时不写入磁盘：** `false`
- **安装时不下载代码：** `false`

## 先决条件

在使用此技能之前，请确保满足以下条件：

- 能够向`https://api.which-llm.com`发送HTTPS请求
- 能够发送和接收JSON数据
- 对于付费请求，AI机器人需要访问加密钱包

## 功能说明

- 向Which-LLM API发送请求
- 使用`POST /decision/optimize`获取推荐的模型及备用方案
- 使用`POST /decision/outcome`报告实际执行结果
- 解释公共API的请求和响应格式
- 描述如何在完成外部支付后重试请求

## 功能限制

- 该技能不会直接调用LLM
- 不会执行用户提供的任意代码
- 除了API使用和支付处理外，不需要访问其他文件或系统资源

## 运行时配置

- `always_on: false`：该技能不会被强制安装，也不会持续运行
- `disable_model_invocation: false`：代理可以根据需要调用该技能
- 该技能仅限于HTTP API的请求和响应处理
- 对于付费请求，AI机器人需要访问加密钱包

## 支付方式

付费请求可能会收到`402 Payment Required`的响应。

**高级流程：**

1. 调用`POST /decision/optimize`
2. 如果API返回`402`，请检查`required_amount`、`accepts`和`payment_reference`等字段
3. 使用服务器或客户端管理的基础设施完成支付
4. 如果有支付凭证，请在请求中添加`X-Payment-Chain`、`X-Payment-Tx`、`X-Payer`、`X-Payment-Amount`和`X-Payment-Asset`等字段，然后重试请求

本文档描述了API的行为及与支付相关的响应处理方式。钱包的使用仅限于付费请求。

## 端点说明

### `GET /capabilities`

用于查询支持的约束条件、决策类型和支付方式。

### `GET /pricing`

在发起付费请求前，用于查看当前的价格和支持的链。

### `GET /status`

用于检查服务运行状态。

### `POST /decision/optimize`

这是主要端点。提交目标和要求后，您将收到：

- `recommended_model`（推荐模型）
- `fallback_plan`（备用方案）
- 决策元数据和可解释性信息

**典型请求格式：**

```json
{
  "goal": "Summarize customer feedback emails into a 5-bullet executive summary",
  "constraints": {
    "min_quality_score": 0.8,
    "max_cost_usd": 0.01
  },
  "workload": {
    "input_tokens": 1200,
    "output_tokens": 300,
    "requests": 1
  },
  "task_type": "summarize"
}
```

如果需要支付，API可能会首先返回`402`响应，其中包含以下字段：

- `required_amount`（所需金额）
- `currency`（货币）
- `accepts[].chain`（支持的链）
- `accepts[].pay_to`（收款地址）
- `payment_reference`（支付参考信息）

完成外部支付后，重新发送请求，并添加以下字段：

- `X-Payment-Chain`
- `X-Payment-Tx`
- `X-Payer`
- `X-Payment-Amount`
- `X-Payment-Asset`

如果您拥有有效的信用令牌，请同时发送`X-Credit-Token`。

### `POST /decision/outcome`

在运行推荐的模型后，使用此端点报告实际结果，以便系统为您生成可用于后续请求的信用令牌。

**典型请求格式：**

```json
{
  "decision_id": "d4e5f6a7-b8c9-0d1e-2f3a-4b5c6d7e8f90",
  "option_used": "openai/gpt-4o-mini",
  "actual_cost": 0.008,
  "actual_latency": 650,
  "quality_score": 0.86,
  "success": true
}
```

**典型响应内容：**

- `status`（状态）
- `decision_id`（决策ID）
- `outcome_hash`（结果哈希值）
- `refund_credit_credit_token`（退款信用令牌）

## 代理使用建议

- 如果需要了解当前的支付方式，请先调用`GET /capabilities`或`GET /pricing`
- 仅在确实需要模型选择帮助时使用`POST /decision/optimize`
- 重复使用返回的决策数据，避免重复提问
- 运行选定的模型后，调用`POST /decision/outcome`以赚取信用点数
- 在需要钱包支持的支付时，使用服务器或客户端的支付流程

## 故障排除

### `PAYMENT_REQUIRED`

该端点要求先完成支付。请阅读`402`响应，完成外部支付，然后在有支付凭证的情况下重试请求。

### `PAYMENT_INVALID`

检查以下内容：
- 是否发送了正确的金额
- 是否选择了正确的链
- 支付是否成功完成
- 请求头是否与实际交易信息一致

### `NO_FEASIBLE_OPTIONS`

您的成本和质量要求过于严格，导致没有合适的模型可用。请放宽预算或质量阈值，然后重试。

### `RATE_LIMIT_EXCEEDED`

请稍后重试。使用幂等性键（idempotency key）来确保重试的安全性。