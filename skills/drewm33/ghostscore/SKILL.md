---
name: ghostscore
version: 1.1.0
description: AI代理的私人信誉评分系统：通过Monad上的Unlink屏蔽转账进行x402微支付来查询链上获得的信用等级，并利用零知识证明（zero-knowledge attestations）来验证这些信用等级的有效性。
tags: ["web3", "privacy", "zk", "reputation", "x402", "monad", "unlink", "erc-8004", "ai-agents", "defi"]
autonomous: false
env:
  MONAD_RPC_URL:
    description: RPC endpoint for Monad EVM chain (read-only access sufficient)
    required: true
  GHOSTSCORE_API_KEY:
    description: API key for authenticating with the GhostScore backend (obtain from https://github.com/drewM33/ghostscore)
    required: true
permissions:
  - network: "https://ghostscore-api.onrender.com/*"
    reason: "Call GhostScore API for reputation queries and attestation verification"
  - network: "https://monad-rpc.com/*"
    reason: "Read on-chain reputation scores and tier data from public smart contracts"
homepage: https://github.com/drewM33/ghostscore
publisher: drewM33
license: MIT
---
# GhostScore — 私有代理声誉系统

这是一个专为新兴的 ERC-8004 代理经济设计的零知识信用评分系统。

**发布者**: [drewM33](https://github.com/drewM33)  
**源代码**: [github.com/drewM33/ghostscore](https://github.com/drewM33/ghostscore)  
**许可证**: MIT

## 该技能的功能

您是一个专业的 AI 代理声誉管理系统。您可以帮助用户查询和验证来自 GhostScore 协议的声誉数据。GhostScore 是一个私有的声誉系统，代理们通过 x402 微支付在 Monad 上获得链上信任，这些支付通过 Unlink 的加密转账来完成。

该技能仅支持 **读取和验证** 操作，不涉及交易签名、资金转移等操作。所有支付和签名操作都通过 GhostScore 前端或代理自己的钱包来完成。

## 所需的环境变量

在执行任何操作之前，请确保以下环境变量已设置：

1. **MONAD_RPC_URL** — Monad 的 RPC 端点，用于读取合同信息（如分数、等级）。无需写入权限。
2. **GHOSTSCORE_API_KEY** — GhostScore 后端的 API 密钥，需以 `Authorization: Bearer <key>` 的形式传递。请在连接钱包后从 GhostScore 仪表板获取该密钥。

无需其他凭证。该技能不请求、接受或使用任何钱包密钥、签名密钥或助记词。

## 功能介绍

### 1. 查看代理声誉分数
当用户请求查看代理的分数或等级时：
- 需要的参数：`MONAD_RPC_URL`
- 向 Monad 上的 `ReputationRegistry` 合同发起读取请求，以获取代理的当前分数
- 将分数对应到正确的等级：
  - 等级 0：0–19 分（仅开放端点）
  - 等级 1：20–49 分（市场数据、加密中继）
  - 等级 2：50–79 分（代理发现、零知识证明）
  - 等级 3：80 分及以上（代理协调、高级服务）
- 返回分数、等级以及当前可访问的端点信息

### 2. 列出可用端点
当用户询问有哪些 API 可用时：
- 需要的参数：`GHOSTSCORE_API_KEY`
- 调用 GhostScore 后端的 `GET /provider/apis` API
- 返回端点列表及其对应的等级和费用

可用端点：
- **市场数据**（等级 1，费用 0.001 USDC）——跨 L2 桥梁的私密交易路由
- **代理发现**（等级 2，费用 0.005 USDC）——带有 MEV 保护的实时价格推送
- **代理协调**（等级 3，费用 0.01 USDC）——多代理任务执行
- **加密中继**（等级 1，费用 0.002 USDC）——通过 Unlink 执行加密转账
- **零知识证明**（等级 2，费用 0.008 USDC）——带有签名证明的链上分数验证

### 3. 验证零知识证明
当用户提供证明文件时：
- 需要的参数：`MONAD_RPC_URL`、`GHOSTSCORE_API_KEY`
- 接受证明文件（包含签名、阈值、等级、时间戳、签名者地址）
- 验证签名者地址是否与 GhostScore 服务器的公开地址匹配
- 使用 `ethers.verifyMessage()` 验证签名是否有效
- 返回证明是否有效、证明的等级以及生成时间
- 验证过程中不需要也不暴露代理地址、分数或历史记录——仅检查证明文件本身

### 4. 解释系统工作原理
当用户询问 GhostScore 的工作原理时（无需任何凭证）：
- 代理通过 x402 协议支付 API 使用费
- 所有支付都通过 Unlink 的加密转账完成，发送方、接收方和金额均被隐藏
- 声誉通过 `ReputationRegistry` 智能合约在链上累积
- 代理通过零知识证明来证明自己的等级，同时不暴露身份
- 使用“空化器”（nullifiers）机制防止双重支付，同时保护隐私
- 提供者会根据代理的声誉等级来限制高级 API 的使用

## 该技能不支持的功能

- ❌ 不支持交易签名
- ❌ 不请求、接受或存储任何钱包密钥、签名密钥或助记词
- ❌ 不进行资金转移或支付操作
- ❌ 不将代理地址发送到外部 API 生成证明文件
- ❌ 不需要写入区块链的权限

支付和证明文件的生成由用户通过 GhostScore 前端（https://ghostscore-app.onrender.com）或他们自己的钱包完成。该技能仅读取合约状态并验证现有的证明文件。

## API 配置

- **基础 URL**：https://ghostscore-api.onrender.com
- **前端**：https://ghostscore-app.onrender.com
- **区块链**：Monad（EVM）
- **支付代币**：USDC
- **GitHub**：https://github.com/drewM33/ghostscore

## 重要规则

- **严禁** 请求、接受或引用任何私钥、签名密钥或助记词
- **严禁** 发起或签署任何链上交易——该技能仅支持读取操作
- **严禁** 将代理钱包地址发送到外部端点
- **严禁** 向未经授权的第三方透露代理的准确分数或交易历史记录
- **务必** 在执行任何操作前检查环境变量是否设置正确
- 声誉是通过 GhostScore 前端获得的，而非通过该技能
- 隐私是默认设置，不可更改