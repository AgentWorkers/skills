---
name: erc-8004
description: ERC-8004 无信任代理（Trustless Agents）——用于在以太坊网络上注册、发现和管理 AI 代理的声誉系统。该标准适用于在链上注册代理、查询代理注册信息、提供/接收声誉反馈，以及与 AI 代理的信任机制进行交互的场景。
---

# ERC-8004：去中心化代理（Trustless Agents）

为自主代理提供链上身份验证、声誉评估和信任机制。**现已在以太坊主网上正式上线！**

## 概述

ERC-8004 提供了三个注册系统：
- **身份注册系统**：用于存储 ERC-721 代理的身份信息及注册元数据
- **声誉注册系统**：记录代理/客户端之间的反馈评分
- **验证注册系统**：通过 zkML、TEE（可信执行环境）等技术进行独立验证

## 快速参考

### 注册代理
```bash
./scripts/register.sh --uri "ipfs://..." --network mainnet
./scripts/register.sh --network sepolia  # Testnet (no URI, set later)
```

### 查询代理信息
```bash
./scripts/query.sh total --network mainnet    # Total registered
./scripts/query.sh agent 1 --network mainnet  # Agent details
./scripts/query.sh reputation 1               # Reputation summary
```

### 更新代理信息
```bash
./scripts/set-uri.sh --agent-id 1 --uri "ipfs://newHash" --network mainnet
```

### 提供反馈
```bash
./scripts/feedback.sh --agent-id 1 --score 85 --tag1 "quality"
./scripts/feedback.sh --agent-id 1 --score 9977 --decimals 2 --tag1 "uptime"
```

## 支持的网络

| 网络 | 状态 | 身份注册系统 | 声誉注册系统 |
|---------|--------|-------------------|---------------------|
| **以太坊主网** | 正式上线 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` |
| Sepolia | 正式上线 | `0x8004A818BFB912233c491871b3d84c89A494BD9e` | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |
| Base | 即将上线 | 待定 | 待定 |
| Arbitrum | 即将上线 | 待定 | 待定 |
| Optimism | 即将上线 | 待定 | 待定 |

合约地址请参见 `lib/contracts.json` 文件。

## 注册文件格式

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "your-agent-name",
  "description": "Agent description...",
  "image": "ipfs://...",
  "services": [
    { "name": "A2A", "endpoint": "https://agent.example/.well-known/agent-card.json", "version": "0.3.0" },
    { "name": "MCP", "endpoint": "https://mcp.agent.eth/", "version": "2025-06-18" },
    { "name": "ENS", "endpoint": "yourname.eth" }
  ],
  "registrations": [
    { "agentRegistry": "eip155:1:0x8004A169FB4a3325136EB29fA0ceB6D2e539a432", "agentId": "1" }
  ],
  "supportedTrust": ["reputation", "crypto-economic", "tee-attestation"]
}
```

注册文件模板请参考 `templates/registration.json`。

## 声誉评分系统

声誉评分使用带小数的固定点数表示（`value` + `valueDecimals`）：

| 标签 | 含义 | 示例 | 值 | 小数位数 |
|-----|---------|---------|-------|----------|
| starred | 质量（0-100） | 87/100 | 87 | 0 |
| uptime | 运行时间百分比 | 99.77% | 9977 | 2 |
| tradingYield | 收益率百分比 | -3.2% | -32 | 1 |
| responseTime | 响应时间（毫秒） | 560ms | 560 | 0 |

## 信任模型

ERC-8004 支持三种可插拔的信任模型：
- **基于声誉的信任模型**：通过客户反馈、评分和元数据来评估代理的可靠性
- **基于加密经济的信任模型**：通过质押机制和经济激励来验证代理行为
- **基于加密验证的信任模型**：利用 TEE 和 zkML 技术进行验证

## 所需依赖库/工具

- `cast`（来自 Foundry）：`curl -L https://foundry.paradigm.xyz | bash`
- `jq`：`brew install jq`
- 私钥文件：位于 `~/.clawdbot/wallets/.deployer_pk` 或通过环境变量 `PRIVATE_KEY` 设置
- IPFS：上传文件时需要设置 `PINATA_JWT`，或手动上传文件

## 相关资源

### 官方信息
- [EIP-8004 规范](https://eips.ethereum.org/EIPS/eip-8004) - 完整规范
- [8004.org](https://8004.org) - 官方网站
- [合约源代码](https://github.com/erc-8004/erc-8004-contracts) |
- [Telegram 社区](https://t.me/ERC8004) - 开发者交流平台
- [开发者计划](http://bit.ly/8004builderprogram) - 参与生态系统建设

### 开发工具与 SDK
- [ChaosChain SDK](https://github.com/ChaosChain/chaoschain/tree/main/packages/sdk) - JavaScript/TypeScript SDK
- [erc-8004-js](https://github.com/tetratorus/erc-8004-js) - 轻量级 JavaScript 库
- [erc-8004-py](https://github.com/tetratorus/erc-8004-py) - Python 实现
- [Vistara 示例](https://github.com/vistara-apps/erc-8004-example) - 包含 AI 代理的完整演示项目

## 生态系统资源
- [Awesome ERC-8004](https://github.com/sudeepb02/awesome-erc8004) - 精选的 ERC-8004 相关资源列表
- [A2A 协议](https://a2a-protocol.org/) - 基于 ERC-8004 的代理间通信协议
- [Ethereum Magicians 讨论区](https://ethereum-magicians.org/t/erc-8004-trustless-agents/25098) - 相关技术讨论

## 生态系统启动时间（2026年2月）

ERC-8004 于 2026 年 1 月 29 日在以太坊主网上正式上线。2 月被定为“生态系统启动月”，旨在展示各团队在构建去中心化代理经济方面的成果。快来参与进来吧！