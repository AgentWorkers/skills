---
name: Decision Economic Optimizer
description: 具有 HTTP 402 USDC 支付和结果信用（折扣）的确定性决策排名 API。
version: 0.1.0
homepage: https://which-llm.com
credentials_required: true
primary_credential: WALLET_CREDENTIALS
always_on: false
disable_model_invocation: false
---
# Which-LLM：基于结果的决策优化器

## 概述

当您需要在成本和质量等明确约束条件下确定性地选择合适的LLM（大型语言模型）时，可以使用此技能。

该技能用于调用Which-LLM API。它本身并不运行LLM，而是帮助代理决定下一个要调用的模型，并可选择性地报告执行结果，以便为未来的付费调用赚取信用点数。

这并非一个仅用于读取信息的辅助工具。对于付费调用，它可以通过准备、签名和提交来自配置钱包的USDC交易来参与支付流程。使用原始私钥作为备用方案以及具备签名/广播功能，显著提高了该技能的敏感度。

## 适用场景

- 选择成本最低且仍符合质量要求的模型
- 当首选模型失败时，使用备用模型
- 保持模型选择的确定性和可审计性
- 报告执行结果，并为后续请求赚取信用点数

## 快速参考

- **API基础URL：** `https://api.which-llm.com`
- **主要付费端点：** `POST /decision/optimize`
- **结果端点：** `POST /decision/outcome`
- **免费查询端点：** `GET /capabilities`, `GET /pricing`, `GET /status`
- **支付货币：** USDC
- **支持的链：** Base, Ethereum, Arbitrum, Optimism, Avalanche

### 先决条件

在使用付费端点之前，请确保满足以下要求：

- 为该技能专门创建一个EVM钱包
- 该钱包中有一定余额（USDC用于支付以及网络费用所需的gas token）
- 首选凭据：`WALLET_KEYSTORE_PATH` 或 `WALLET_KEYSTORE_JSON` 以及 `WALLET_KEYSTORE_PASSWORD`
- 备用凭据：`WALLET_PRIVATE_KEY`
- 可选参数：`WALLET_RPC_URL` 和 `PREFERREDCHAIN_ID`
- 至少通过两个渠道验证支付地址的合法性
- 该技能默认设置为每次请求都需要支付批准，但实际执行方式取决于主机或运行时环境
- 注册表和主机文档应说明该技能需要通过环境变量传递钱包凭据，而非无需任何环境变量
- 使用原始私钥作为备用方案风险较高，仅应在特殊情况下使用

请记住以下重要规则：切勿使用主钱包来执行此技能。

## 凭据选项

### 首选方式

使用加密的密钥存储库：

- `WALLET_KEYSTORE_PATH` 加 `WALLET_KEYSTORE_PASSWORD`
- 或 `WALLET_KEYSTORE_JSON` 加 `WALLET_KEYSTORE_PASSWORD`

这种方式可避免依赖原始签名密钥。

### 备用方式

仅在无法使用密钥存储库时使用 `WALLET_PRIVATE_KEY`。

如果使用备用方案，请注意：
- 保持钱包的余额较低
- 默认情况下启用每次请求的批准流程
- 由于原始签名密钥会直接暴露给主机运行时环境，因此这种方式的风险更高

## 钱包设置最佳实践

- 为该技能专门创建一个非主钱包
- 优先使用加密的密钥存储库而非原始私钥
- 保持余额较低（通常为2-10 USDC及3-5 gas token）
- 先使用少量测试余额（例如1-2 USDC及1-2 gas）
- 安全存储签名密钥，切勿泄露
- 定期检查交易记录，并在确认使用情况后补充余额

## 功能说明

- 向Which-LLM API发送请求
- 使用 `POST /decision/optimize` 获取推荐的模型和备用方案
- 使用 `POST /decision/outcome` 报告实际执行结果
- 处理付费调用的标准支付流程（如遇到402错误时，提示用户批准/签名支付并重试）
- 在主机允许的情况下，使用配置好的钱包准备并提交支付交易
- 仅向API发送公开支付信息（交易哈希、付款人地址、金额、链和货币）
- 可以使用 `X-Credit-Token` 来减少下次付费请求的金额

## 功能限制

- 该技能不直接调用LLM
- 不会执行用户提供的任意代码
- 不需要钱包或API调用流程之外的文件、秘密信息或系统访问权限

## 运行时权限与风险

- `always_on: false`：该技能不会强制安装，也不会持续运行
- `disable_model_invocation: false`：代理可以根据需要随时调用该技能
- 对于付费请求，该技能可以使用高敏感度的钱包凭据来准备、签名和提交交易
- 使用原始私钥作为备用方案以及具备签名/广播功能，使得该技能的敏感度高于单纯的读取工具
- 默认设置为每次请求都需要批准，但实际执行方式取决于主机设置
- 如果主机禁用了批准流程，风险将扩大到配置钱包的余额范围
- 严禁使用主钱包，必须使用专门用于此技能的低余额钱包

## 支付模型

付费调用使用HTTP状态码 `402 Payment Required`。

**高级流程：**

1. 调用 `POST /decision/optimize`
2. 如果API返回 `402`，检查 `required_amount`、`accepts` 和 `payment_reference` 字段
3. 在设置过程中验证支付地址，并确认其来自可信来源
4. 在默认模式下，需要人工批准支付
5. 从专门的钱包中签名并提交USDC支付
6. 带上支付证明头信息重新发送请求

### 批准模式

#### 默认模式

该技能默认要求每次支付都需要人工批准。

实际执行方式取决于主机设置。请注意，仅凭技能文件并不能保证一定会触发人工审批流程。

推荐这种发布方式，因为：
- 钱包密钥不会被视为始终可用的支付凭据
- 每次支付仍需人工审核
- 即使技能被滥用，也能限制风险

#### 可选的低摩擦模式

如果主机允许，可以启用低摩擦模式（即无需每次请求都进行人工批准）。

启用该模式时，请注意：
- 仅使用专门用于此技能的低余额钱包
- 设置严格的资金上限
- 在启用前仔细权衡利弊

## 支付安全验证

不要仅依赖一个来源（包括此技能文件）来验证支付地址。在支付或使用钱包之前，通过至少两个渠道验证支付地址的合法性：
- `https://api.which-llm.com/.well-known/payment-address.txt`
- `https://api.which-llm.com/.well-known/agent.json`
- `https://api.which-llm.com/docs/payment-addresses`
- `ENS: which-llm.eth`

这些渠道有助于检测篡改行为，但它们仍可能共享部分操作控制权，因此不能被视为完全独立的信任来源。`.well-known/agent.json` 仅是一个额外的发布渠道，并非独立的信任验证机制。

所有列出的信息必须一致。如果信息不一致，请勿支付，并通过 `https://api.which-llm.com/report/wrong_address` 报告问题。

目前，该技能不提供额外的加密信任验证机制（如签名地址声明、链上证明或第二个独立控制的发布渠道）。

## 端点说明

### `GET /capabilities`

用于查询支持的约束条件、决策类型和支付方式。

### `GET /pricing`

在发起付费请求前，使用此端点查看当前价格和支持的链。

### `GET /status`

用于检查服务状态。

### `POST /decision/optimize`

这是主要端点。提交目标和要求，然后接收：
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

如果需要支付，API会首先返回 `402` 错误码，并包含以下字段：
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

在运行推荐模型后，使用此端点报告实际结果，以便系统为您的未来请求生成信用令牌。

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

- `status`
- `decision_id`
- `outcome_hash`
- `refund_credit_credit_token`

## 代理使用指南

- 如果需要了解当前的支付模型，先调用 `GET /capabilities` 或 `GET /pricing`
- 仅在确实需要模型选择帮助时才使用 `POST /decision/optimize`
- 重用返回的决策数据，避免重复请求相同的信息
- 运行选定模型后，调用 `POST /decision/outcome` 以赚取信用点数
- 除非主机特别启用了低摩擦支付模式，否则默认使用需要人工批准的模式

## 最小安全规则

- 仅使用专门用于此技能的低余额钱包
- 尽可能在主机上默认启用支付批准功能
- 在首次使用前，通过多个渠道验证支付地址
- 仅发送准确的支付金额
- 仅向API发送支付证明信息，切勿泄露钱包密钥

## 故障排除

### `PAYMENT_REQUIRED`

该端点要求先完成支付。收到 `402` 错误码后，先在支持的链上支付指定金额，然后重新发送请求并带上支付证明头信息。

### `PAYMENT_INVALID`

检查以下内容：
- 是否支付了正确的金额
- 是否选择了正确的链
- 支付是否成功完成
- 请求头信息是否与实际交易匹配

### `NO_FEASIBLE_OPTIONS`

您的成本和质量要求过于严格，当前模型无法满足。请放宽预算或质量限制，然后重新尝试。

### `RATE_LIMIT_EXCEEDED`

暂时放弃尝试，稍后重试。可以使用幂等性键来确保重试的安全性。