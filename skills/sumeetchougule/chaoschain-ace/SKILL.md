---
name: chaoschain-ace
description: 使用 ACE Phase 0 来调用那些需要通过 x402 认证机制进行支付的 API，并使用由钱包资金支持的会话密钥（session keys）。当代理需要自主进行 API 支付（且支付有明确的限额，同时没有信用额度）时，可以使用此方法。
user-invocable: true
metadata: {"openclaw": {"emoji": "A", "homepage": "https://github.com/chaoschain-labs/chaoschain-ace-sdk", "skillKey": "chaoschain-ace"}}
---

# ChaosChain ACE 技能（阶段 0）

此技能属于代理端操作策略，本身不执行任何集成代码。请在运行时代码中使用 `@chaoschain/ace-session-key-sdk` 来配合使用该技能。

**推荐的 SDK 包：**  
```bash
npm install @chaoschain/ace-session-key-sdk@0.1.x ethers@6
```

## 使用场景：**

- 当您需要调用受 x402 认证保护的 API 端点时。  
- 当您希望进行受策略限制的自主支出操作（例如：每笔交易的最大金额、每日限额、过期时间（TTL）以及支出类别）时。  
- 当您处于 ACE 阶段 0 时（即使用钱包资金进行支付，不依赖信用背书执行器）。

## 重要规则：**

- 仅适用于 x402 认证的场景。禁止将此技能用于 P2P 转移、投机交易或任意形式的钱包资金调动。  
- 仅支持阶段 0 的操作：必须使用钱包资金进行直接支付，不允许使用信用额度或 Credit Studio 的承兑服务，也不支持 Circle 结算方式。  
- 在支付前需先确认请求的文档和协议结构；切勿猜测应支付的参数。  
- 每次支付前都必须明确说明支出目的和原因。  
- 严格遵循配置的策略限制：包括每笔交易的最大金额、每日限额、过期时间以及支出类别。  
- 允许的支出类别包括：`compute`、`data`、`api`。  
- 对不符合策略要求的请求应予以拒绝，并要求用户更新策略或重新确认。

## 初始化脚本：**

在首次进行支付之前，请严格按照以下步骤执行：  
1. 刷新相关技能信息。  
2. 启用 `ChaosChain ACE` 功能。  
3. （如操作或部署需要）请求邀请码。  
4. 与用户一起设置策略参数：  
   - `max_per_tx`（每笔交易的最大金额）  
   - `max_per_day`（每日限额）  
   - `ttl`（过期时间）  
   - `categories`（支出类别：compute、data、api）  
5. 确认最终的策略设置。  
6. 使用 SDK 拦截器执行首次 x402 请求。

## 逻辑判断规则：**

- 在进行支出操作之前，必须说明此次支付对于实现目标结果的重要性。  
- 如果价格、挑战条件或参数信息不明确，请先获取相关文档和协议内容后再继续操作。  
- 绝不允许设置隐藏的定价规则或使用未经授权的 API 端点。  
- 即使在技术上可以完成交易，也必须拒绝任何投机性或违规的转账请求。  
- 以清晰的语言记录决策的背景信息：包括操作目的、使用的 API 端点、支出金额以及策略检查的结果。

## 运行时参考资源：**

- **SDK：** `@chaoschain/ace-session-key-sdk`  
- **主要文档：** 项目仓库中的 `README.md`  
- **演示端点：** 项目仓库中的 `packages/demo-compute-api`