---
name: blindoracle
display_name: BlindOracle - Privacy-First Agent Infrastructure
version: 1.0.1
author: Craig M. Brown
homepage: https://craigmbrown.com/blindoracle
license: Proprietary
category: infrastructure
tags:
  - forecasting
  - identity
  - payments
  - privacy
  - x402
  - micropayments
  - agent-infrastructure
  - settlement
min_sdk_version: "0.1.0"
---

# BlindOracle

BlindOracle 是一款以隐私保护为核心的设计的代理基础设施平台，提供预测服务、身份验证、结算功能以及跨支付通道的微支付服务（使用 x402 协议）。

## 产品描述

BlindOracle 是一套专为保护用户隐私而设计的基础设施服务，适用于各类 AI 代理。所有操作均基于 CaMel 的四层安全架构进行保护，并通过 Base L2 层的 x402 微支付协议使用 USDC 进行结算。

### 主要服务功能：

1. **预测平台**：创建并管理隐私保护的预测市场，支持匿名提交交易订单。
2. **身份验证**：实现去中心化的代理身份评分机制，并具备防伪造身份验证功能。
3. **账户与结算**：支持多支付通道间的余额管理和价值转移（即时结算约 3 秒，链上结算约 30 秒）。
4. **跨通道转账**：支持在多个支付通道之间进行原子级转账，且转账费用极低。

## 主要功能及费用：

| 功能            | 描述                                      | 费用                |
|-----------------|-----------------------------------------|-------------------|
| `create_forecast`    | 创建新的预测市场                        | 0.001 USDC            |
| `submit_position`    | 提交匿名交易订单                          | 0.0005 USDC + 0.1%        |
| `resolve_forecast`   | 解决预测结果并分配收益                        | 0.002 USDC            |
| `verify_credential`   | 验证代理的身份和信誉                          | 0.0002 USDC            |
| `mint_credential`    | 生成代理的参与证明/身份证明                     | 0.001 USDC            |
| `check_account`     | 查看所有支付通道的余额                        | 免费                |
| `create_settlement_request` | 生成结算请求                          | 0.0001 USDC            |
| `settle_instant`    | 即时结算（约 3 秒）                          | 0.0005 USDC + 0.1%        |
| `settle_onchain`    | 链上结算（约 30 秒）                          | 0.001 USDC + 0.05%        |
| `transfer_cross_rail`    | 在不同支付通道之间进行转账                        | 0.001 USDC + 0.1%        |
| `convert_private_to_stable` | 将私有代币转换为稳定币                        | 0.0005 USDC + 0.05%        |
| `get_transfer_quote` | 获取转账费用估算及路由建议                        | 免费                |

## 使用说明

```javascript
// Check account balances (FREE)
const balance = await gateway.invoke("blindoracle", {
  capability: "check_account",
  params: { rail: "all" }
});

// Create a forecast
const forecast = await gateway.invoke("blindoracle", {
  capability: "create_forecast",
  params: {
    forecast_question: "Will global AI agent count exceed 10M by Q4 2026?",
    forecast_deadline: "2026-12-31T23:59:59Z",
    initial_stake_units: 10000,
    resolution_oracle: "chainlink_data_feed"
  },
  payment_proof: { /* x402 proof */ }
});

// Verify agent credentials
const creds = await gateway.invoke("blindoracle", {
  capability: "verify_credential",
  params: {
    agent_public_key: "ba3eefec0e795362230f869461ea16e20b782e11eef6107edeed0d3d19e7651b"
  }
});
```

## 安全性

所有操作均受到 CaMel 四层安全架构的保护：
- **第 1 层**：限制请求频率（每分钟 60 次）及输入数据清洗。
- **第 2 层**：采用拜占庭共识算法（67% 的节点同意即可通过，高价值交易需 80% 的节点同意）。
- **第 3 层**：具备防欺诈机制（检测数据异常变化的百分比阈值为 30%）。
- **第 4 层**：实施权限验证及不可篡改的审计记录。

## 隐私保护措施：

- 通过 Guardian Federation Bridge 实现用户身份的完全隔离。
- 采用 SHA256 加密算法对交易数据进行加密处理。
- 存款人及交易持有者的信息无法相互关联。
- 采用去中心化的身份验证机制，无需中央权威机构。

## API 接口：

- 基本地址：`https://craigmbrown.com/api/v2`
- 代理管理接口：`https://craigmbrown.com/a2a/v1`
- 系统健康检查接口：`https://craigmbrown.com/api/v2/health`

## 支付方式：

所有支付均通过 HTTP 402 微支付协议在 Base L2 层（链 ID 8453）使用 USDC 完成。

## 使用要求：

- 需要支持 x402 协议的支付客户端。
- 使用 Base L2 层的 USDC 进行付费功能。
- 免费功能（如 `check_account`、`get_transfer_quote`）无需额外费用。

## 帮助资源：

- 官方网站：https://craigmbrown.com/blindoracle
- 代码仓库：https://github.com/craigmbrown/blindoracle-docs