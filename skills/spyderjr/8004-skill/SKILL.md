---
name: 8004-skill
description: **ERC-8004 无信任代理（Trustless Agents）**：在 TRON 和 BSC 区块链上注册和管理 AI 代理的身份，并实现链上声誉跟踪功能。
---
# ERC-8004：TRON与BSC上的无信任代理系统

TRON上的自主代理具备链上身份、声誉和验证机制。**现已在TRON主网和BSC主网上线！**

## 概述

ERC-8004在TRON和BSC区块链上提供了三个注册表：
- **身份注册表** - 包含TRC-721代理身份及其注册元数据的注册信息
- **声誉注册表** - 代理/客户之间的签名反馈分数
- **验证注册表** - 通过zkML、TEE等技术进行独立验证

**多链支持**：该协议同时在TRON和BSC（BNB智能链）上运行，并已完全部署！

## 快速参考

### 注册代理
```bash
# TRON Mainnet
node scripts/register.js --uri "ipfs://..." --chain tron --network mainnet

# TRON Testnet
node scripts/register.js --uri "ipfs://..." --chain tron --network nile

# BSC Mainnet
node scripts/register.js --uri "ipfs://..." --chain bsc --network mainnet

# BSC Testnet
node scripts/register.js --uri "ipfs://..." --chain bsc --network testnet

# Register without URI (set later)
node scripts/register.js --chain tron --network nile
```

### 私钥设置
```bash
# Set once, works for both TRON and BSC
export TRON_PRIVATE_KEY="your_64_character_hex_private_key"
```

## 网络

### TRON网络

| 网络 | 状态 | 身份注册表 | 声誉注册表 | 验证注册表 |
|---------|--------|-------------------|---------------------|---------------------|
| **主网** | 已上线 | `TFLvivMdKsk6v2GrwyD2apEr9dU1w7p7Fy` | `TFbvfLDa4eFqNR5vy24nTrhgZ74HmQ6yat` | `TLCWcW8Qmo7QMNoAKfBhGYfGpHkw1krUEm` |
| **Nile** | 已上线 | `TDDk4vc69nzBCbsY4kfu7gw2jmvbinirj5` | `TBVaGd6mBuGuN5ebcvPvRaJo4rtEWqsW6Y` | `TGGkHDHhBzhFcLNcEogAWJkvfFYy4jyrSw` |
| **Shasta** | 已上线 | `TH775ZzfJ5V25EZkFuX6SkbAP53ykXTcma` | `TTkds2ZZKBTChZHho4wcWAa7eWQTxh5TUT` | `TQBFHtKRiaQjc1xp4LtmmXKYdA7JLN89w3` |

**注意：** TRON的实现遵循TRC-8004（ERC-8004的TRON版本）。查询脚本使用兼容模式：
- ✅ 始终可用：`ownerOf`、`tokenURI`（ERC-721标准）
- ⚠️ 可能有所不同：`agentURI`、`getAgentWallet`、`agentExists`（ERC-8004扩展）

### BSC网络

| 网络 | 状态 | 身份注册表 | 声誉注册表 | 验证注册表 |
|---------|--------|-------------------|---------------------|---------------------|
| **BSC主网** | 已上线 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` | `0x8004Cc8439f36fd5F9F049D9fF86523Df6dAAB58` |
| **BSC测试网** | 已上线 | `0x8004A818BFB912233c491871b3d84c89A494BD9e` | `0x8004B663056A597Dffe9eCcC1965A193B7388713` | `0x8004Cb1BF31DAf7788923b405b754f57acEB4272` |

**多链使用方法：**
```bash
# TRON
node scripts/register.js --uri "ipfs://..." --chain tron --network mainnet

# BSC
node scripts/register.js --uri "ipfs://..." --chain bsc --network mainnet
```

合约地址和ABI信息请参见`lib/contracts.json`文件。

## 注册文件格式

```json
{
  "type": "https://eips.ethereum.org/EIPS/eip-8004#registration-v1",
  "name": "your-agent-name",
  "description": "Agent description...",
  "image": "ipfs://...",
  "services": [
    { "name": "A2A", "endpoint": "https://agent.example/.well-known/agent-card.json", "version": "0.3.0" },
    { "name": "MCP", "endpoint": "https://mcp.agent.tron/", "version": "2025-06-18" }
  ],
  "registrations": [
    { "agentRegistry": "tron:728126428:TFLvivMdKsk6v2GrwyD2apEr9dU1w7p7Fy", "agentId": "1" }
  ],
  "supportedTrust": ["reputation", "crypto-economic", "tee-attestation"]
}
```

模板文件位于`templates/registration.json`。

## 声誉分数

声誉系统使用带小数点的签名数值（`value` + `valueDecimals`）：

| 标签 | 含义 | 示例 | value | decimals |
|-----|---------|---------|-------|----------|
| quality | 质量（0-100） | 87/100 | 87 | 0 |
| uptime | 运行时间百分比 | 99.77% | 9977 | 2 |
| yield | 收益百分比 | -3.2% | -32 | 1 |
| latency | 延迟（毫秒） | 560ms | 560 | 0 |

## 信任模型

ERC-8004支持三种可插拔的信任模型：
- **基于声誉的** - 基于客户反馈的评分系统
- **加密经济的** - 通过质押进行验证，并提供经济激励
- **加密验证的** - 使用TEE（可信执行环境）和zkML证明

## 依赖项

- `node` & `npm` - JavaScript运行时环境和包管理器
- `tronweb` - TRON JavaScript SDK（通过`npm install tronweb`安装）
- 私钥配置（选择一种方式）：
  - 环境变量：`TRON_PRIVATE_KEY` 或 `PRIVATE_KEY`
  - 文件：`~/.clawdbot/wallets/.deployer_pk`
- IPFS：设置`PINATA_JWT`用于上传数据，或手动上传

## TRON特有的特性

### 地址格式
- TRON使用以‘T’开头的Base58地址（例如：`TFLvivMdKsk6v2GrwyD2apEr9dU1w7p7Fy`）
- 脚本会自动处理地址转换

### 网络标识符
- 主网：`tron:728126428`（TRON链ID）
- 在注册文件中使用格式：`tron:728126428:TFLvivMdKsk6v2GrwyD2apEr9dU1w7p7Fy`

### 能量和带宽
- TRON使用“能量”和“带宽”代替“gas”
- 脚本设置`feeLimit: 1000000000`（最大费用为1000 TRX）
- 实际费用通常更低

## 资源

### 官方信息
- [EIP-8004规范](https://eips.ethereum.org/EIPS/eip-8004) - 完整规范
- [8004.org](https://8004.org) - 官方网站
- [Telegram社区](https://t.me/ERC8004) - 开发者交流频道
- [Builder计划](http://bit.ly/8004builderprogram) - 加入生态系统

### TRON相关资源
- [TRON开发者文档](https://developers.tron.network/) - 官方文档
- [TronScan](https://tronscan.org/) - 区块浏览器
- [TronWeb](https://github.com/tronprotocol/tronweb) - JavaScript SDK
- [TronGrid](https://www.trongrid.io/) - API服务

### 生态系统
- [Awesome ERC-8004](https://github.com/sudeepb02/awesome-erc8004) - 优质资源列表
- [A2A协议](https://a2a-protocol.org/) - 基于ERC-8004的代理间通信协议

## 脚本参考

所有脚本均支持多链（TRON + BSC）：

- **register.js** - 在链上注册新代理
- **query.js** - 查询代理信息和声誉
- **feedback.js** - 提交反馈/声誉分数
- **set-uri.js** - 更新代理元数据URI

运行脚本时无需参数即可查看详细使用说明。

## 示例

### 完整的代理工作流程
```bash
# 1. Set private key (works for both TRON and BSC)
export TRON_PRIVATE_KEY="your_private_key"

# 2. Register agent on TRON testnet
node scripts/register.js --uri "ipfs://QmYourHash" --chain tron --network nile

# 3. Query agent info (use ID from step 2)
node scripts/query.js agent 1 --chain tron --network nile

# 4. Submit feedback
node scripts/feedback.js --agent-id 1 --score 95 --tag1 "quality" --chain tron --network nile

# 5. Query reputation
node scripts/query.js reputation 1 --chain tron --network nile

# 6. Update URI if needed
node scripts/set-uri.js --agent-id 1 --uri "ipfs://QmNewHash" --chain tron --network nile
```

### 多链示例
```bash
# Register on BSC testnet
node scripts/register.js --uri "ipfs://..." --chain bsc --network testnet

# Query agent on BSC mainnet
node scripts/query.js agent 1 --chain bsc --network mainnet

# Submit feedback on TRON mainnet
node scripts/feedback.js --agent-id 1 --score 98 --tag1 "quality" --chain tron --network mainnet
```

## 故障排除

### “TRON_PRIVATE_KEY未设置”
- 确保钱包中有足够的TRX用于交易费用
- 从[Nile Faucet](https://nileex.io/join/getJoinPage)获取测试网TRX

### “非所有者”
- 只有代理所有者才能更新URI或元数据
- 使用`query.js agent <id>`检查所有权

## 安全注意事项

- 切勿将私钥提交到版本控制系统中
- 对敏感数据使用环境变量
- 在主网部署前先在Nile测试网上进行测试
- 确认`lib/contracts.json`中的合约地址正确

---

*本实现符合ERC-8004规范。TRON的实现版本为TRC-8004。*