---
name: Decision Economic Optimizer
description: 具有 HTTP 402 USDC 支付和结果信用（折扣）功能的确定性决策排序 API。
version: 0.1.0
homepage: https://which-llm.com
credentials_required: true
primary_credential: WALLET_CREDENTIALS
---
# Which-LLM：基于结果的决策优化器

## 概述

当您需要在成本和质量等明确约束条件下确定性地选择合适的LLM（大型语言模型）时，可以使用此技能。

该技能用于调用Which-LLM API。它本身不运行LLM，而是帮助代理决定下一个要调用的模型，并可选择性地报告执行结果，以获取未来付费调用的信用点数。

## 适用场景

- 选择符合质量要求的最低成本模型
- 当首选模型失败时，选择备用模型
- 保持模型选择的确定性和可审计性
- 报告执行结果并获取后续请求的信用点数

## 快速参考

- **API基础URL：** `https://api.which-llm.com`
- **主要付费端点：** `POST /decision/optimize`
- **结果端点：** `POST /decision/outcome`
- **免费查询端点：** `GET /capabilities`, `GET /pricing`, `GET /status`
- **支付货币：** USDC
- **支持的链：** Base, Ethereum, Arbitrum, Optimism, Avalanche

### 先决条件

在使用付费端点之前，请确保准备以下内容：

- 为该技能创建一个专用的EVM钱包
- 该钱包中有一定余额（USDC用于支付以及网络费用所需的本地Gas代币）
- 首选凭据：`WALLET_KEYSTORE_PATH` 或 `WALLET_KEYSTORE_JSON` 以及 `WALLET_KEYSTORE_PASSWORD`
- 备用凭据：`WALLET_PRIVATE_KEY`
- 可选的 `WALLET_RPC_URL` 和 `PREFERREDCHAIN_ID`
- 来自至少两个发布渠道或检索路径的支付地址验证
- 该技能默认要求每次请求都经过支付批准，但实际执行方式取决于主机或运行时环境

请记住以下重要规则：切勿使用主钱包进行此操作。

## 凭据选项

### 首选方式

使用加密的密钥存储库来管理专用钱包：

- `WALLET_KEYSTORE_PATH` 和 `WALLET_KEYSTORE_PASSWORD`
- 或 `WALLET_KEYSTORE_JSON` 和 `WALLET_KEYSTORE_PASSWORD`

这样可以避免依赖原始的签名密钥。

### 备用方式

仅在无法使用密钥存储库时使用 `WALLET_PRIVATE_KEY`。

如果使用备用方式，请注意：
- 保持钱包的余额较低
- 默认启用每次请求的批准流程

### 钱包设置最佳实践

- 为该技能专门创建一个非主钱包
- 优先使用加密的密钥存储库而非原始的私钥
- 保持余额较低（通常为$2-10 USDC加上$3-5 Gas代币）
- 首先使用少量测试余额（例如$1-2 USDC加上$1-2 Gas代币）
- 安全存储签名密钥，切勿泄露
- 定期检查交易记录，并在确认使用情况后补充余额

## 该技能的功能

- 向Which-LLM API发送请求
- 使用 `POST /decision/optimize` 获取推荐的模型和备用方案
- 使用 `POST /decision/outcome` 报告实际执行结果
- 处理付费请求的标准支付流程（402 -> 批准/签名支付 -> 重试）
- 仅向API发送公开的支付证明（交易哈希、付款人地址、金额、链和货币）
- 可以使用 `X-Credit-Token` 来减少下一次付费请求的金额

## 该技能不执行的功能

- 不直接调用LLM
- 不执行来自用户提示的任意代码
- 不需要钱包和API调用流程之外的任何文件、密钥或系统访问权限

## 支付模型

付费请求使用HTTP `402 Payment Required` 响应码。

**高级流程：**

1. 调用 `POST /decision/optimize`
2. 如果API返回 `402`，检查 `required_amount`、`accepts` 和 `payment_reference` 字段
3. 在设置过程中验证支付地址，并确认其来自可信来源
4. 在默认模式下，需要人工批准支付
5. 从专用钱包中签名并提交相应的USDC支付
6. 带上支付证明头重新发送相同的请求

### 批准模式

#### 默认模式

该技能默认要求每次支付都经过人工批准。

实际执行方式取决于主机环境。请注意，技能文件本身并不能保证每次支付都会经过人工审核。

推荐采用这种发布方式，因为：
- 钱包密钥不被视为始终可用的支付凭证
- 每笔支付仍需人工审核
- 即使技能被滥用，专用钱包的低余额设置也能限制风险

#### 可选的低摩擦模式

如果主机允许，可以启用低摩擦模式（即无需每次请求都经过人工批准）：

- 仅使用专用低余额钱包
- 设置严格的资金上限
- 在启用此模式前仔细权衡利弊

## 支付安全验证

不要仅依赖一个来源（包括该技能文件）来验证支付地址。在支付或使用钱包之前，请通过至少两个渠道或路径验证支付地址：
- `https://api.which-llm.com/.well-known/payment-address.txt`
- `https://api.which-llm.com/.well-known/agent.json`
- `https://api.which-llm.com/docs/payment-addresses`
- `ENS: which-llm.eth`

这些路径有助于检测篡改行为，但它们仍可能共享部分操作控制权，因此不能被视为完全独立的信任依据。`.well-known/agent.json` 路径只是一个额外的发布渠道，并非独立的信任来源。

所有列出的信息必须一致。如果信息不一致，请不要支付，并通过 `https://api.which-llm.com/report/wrong_address` 报告问题。

目前，该技能不提供额外的加密信任凭证（如签名地址声明、链上认证或第二个独立控制的发布渠道）。

## 端点

### `GET /capabilities`

用于查询支持的约束条件、决策类型和支付方式。

### `GET /pricing`

在发起付费请求前，使用此端点查看当前的价格和支持的链。

### `GET /status`

用于检查服务运行状态。

### `POST /decision/optimize`

这是主要端点。提交目标和约束条件后，将收到以下信息：
- `recommended_model`
- `fallback_plan`
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

如果需要支付，API会首先返回 `402` 响应，并包含以下字段：
- `required_amount`
- `currency`
- `accepts[].chain`
- `accepts[].pay_to`
- `payment_reference`

支付完成后，重新发送请求，并提供以下信息：
- `X-Payment-Chain`
- `X-Payment-Tx`
- `X-Payer`
- `X-Payment-Amount`
- `X-Payment-Asset`

如果您拥有有效的信用令牌，请同时提供：
- `X-Credit-Token`

### `POST /decision/outcome`

在运行推荐的模型后，使用此端点报告实际结果，以便系统可以发放信用令牌供后续使用。

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

**典型响应包含：**
- `status`
- `decision_id`
- `outcome_hash`
- `refund_credit_credit_token`

## 代理的使用建议

- 如果需要了解当前的支付模式，请先调用 `GET /capabilities` 或 `GET /pricing`
- 仅在确实需要模型选择帮助时才使用 `POST /decision/optimize`
- 重复使用返回的决策数据，避免重复提问
- 运行选定模型后，调用 `POST /decision/outcome` 以获取信用点数
- 除非主机启用了低摩擦支付模式，否则默认采用需要人工批准的模式

## 最小安全规则

- 仅使用专用低余额钱包
- 尽可能在主机上默认启用支付批准功能
- 在首次使用前通过多个渠道验证支付地址
- 仅发送准确的支付金额
- 仅向API发送支付证明头，切勿泄露钱包密钥

## 故障排除

### `PAYMENT_REQUIRED`

该端点要求先完成支付。请查看 `402` 响应，按照要求在支持的链上完成支付，然后带上支付证明头重新尝试。

### `PAYMENT_INVALID`

检查：
- 是否发送了正确的金额
- 是否选择了正确的链
- 交易是否成功
- 请求头是否与实际交易匹配

### `NO_FEASIBLE'options`

您的成本和质量约束条件过于严格，当前模型无法满足要求。请放宽预算或质量阈值，然后重新尝试。

### `RATE_LIMIT_EXCEEDED`

请稍后重试。可以使用幂等性密钥来确保重试的安全性。