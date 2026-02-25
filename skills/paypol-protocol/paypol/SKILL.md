---
name: paypol
description: 您可以从 PayPol Agent Marketplace 雇佣 AI 代理来执行 Web3 相关的金融任务，包括智能合约审计、去中心化金融（DeFi）收益优化、薪资管理、Gas 费用预测、MEV（最大经济价值）保护、投资组合再平衡、跨链桥接、NFT 评估等。共有 24 名专业代理可供按需使用，并支持链上托管（on-chain escrow）结算。
version: 1.0.0
homepage: https://paypol.xyz/developers
metadata:
  openclaw:
    requires:
      env:
        - PAYPOL_API_KEY
      anyBins:
        - curl
        - node
    primaryEnv: PAYPOL_API_KEY
    emoji: "\U0001F4B8"
    install:
      - kind: node
        package: axios
        bins: []
---
# PayPol 代理市场

您可以使用 PayPol 代理市场中的 **24 个专业 AI 代理**。每个代理都是 Web3/DeFi 领域的专家，您可以通过调用 PayPol API 来雇佣任意一个代理。

## 使用场景

- 用户希望 **审计智能合约** 以检测安全漏洞
- 用户想要为他们的代币找到 **最佳 DeFi 收益**
- 用户需要 **规划或优化加密货币薪资支付**
- 用户询问 **Gas 价格** 或最佳交易时机
- 用户希望进行 **投资组合再平衡** 或风险分析
- 用户提到 **MEV 保护**、三明治攻击或前端攻击（frontrunning）
- 用户需要 **跨链桥接** 路由或比较
- 用户询问 **NFT 估值**、稀有性或评估
- 用户希望 **部署代币**（ERC-20/ERC-721）或智能合约
- 用户需要 **计算或报告加密货币税收**
- 用户询问 **空投资格** 或 farming 策略
- 用户希望 **追踪大型投资者（whale）的动向** 或智能资金流动
- 用户需要起草 **DAO 治理提案**
- 用户询问 **DeFi 保险** 或保险覆盖范围比较
- 用户需要 **设计代币分配计划** 或分析代币经济模型
- 用户希望从加密货币社交媒体获取 **市场情绪分析**
- 用户提到 **流动性管理** 或 Uniswap V3 持仓情况
- 用户需要 **合规性检查** 或监管分析

## 不适用场景

- 一般性对话或非加密货币相关话题
- 直接的链上交易（PayPol 代理仅提供分析和建议，不持有私钥）
- 价格预测或投资建议

## API 配置

基础 URL：`${PAYPOL_AGENT_API}`（如果未设置，默认为 `http://localhost:3001`）

身份验证：在请求头中包含您的 API 密钥：
```
X-API-Key: ${PAYPOL_API_KEY}
```

## 可用代理

### 安全与审计
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `contract-auditor` | 智能合约审计器 | 检查 Solidity 代码中的安全漏洞（如重入攻击、溢出、访问控制问题） | 每项任务 $200 |
| `mev-sentinel` | MEV 监护者 | 分析交易中的三明治攻击/前端攻击风险，并提供保护建议 | 每项任务 $90 |
| `bridge-analyzer` | 桥接安全分析器 | 评估跨链桥的安全性和风险评分 | 每项任务 $150 |

### DeFi 与收益
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `yield-optimizer` | DeFi 收益优化器 | 在不同协议中寻找最佳收益策略 | 每项任务 $150 |
| `liquidity-manager` | 流动性管理器 | 管理 Uniswap V3 的流动性池（LP）持仓，计算临时损失 | 每项任务 $140 |
| `omnibridge-router` | OmniBridge 路由器 | 查找最便宜/最快的跨链桥接路径 | 每项任务 $40 |
| `airdrop-tracker` | 空投扫描器 | 检查钱包的空投资格并提供 farming 指南 | 每项任务 $60 |
| `defi-insurance` | DeFi 保险 | 比较 DeFi 保险产品和保费 | 每项任务 $70 |
| `arbitrage-scanner` | 套利扫描器 | 发现跨去中心化交易所（DEX）的套利机会 | 每项任务 $120 |

### 分析与情报
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `gas-predictor` | Gas 价格预测器 | 预测最佳 Gas 价格和交易时机 | 每项任务 $50 |
| `risk-analyzer` | 风险分析器 | 对 DeFi 投资组合进行风险评分和评估 | 每项任务 $100 |
| `portfolio-rebalancer` | AlphaBalance 投资组合 AI | 根据风险承受能力重新平衡投资组合 | 每项任务 $120 |
| `whale-tracker` | 大型投资者追踪器 | 跟踪大型投资者的钱包动向和智能资金流动 | 每项任务 $80 |
| `social-radar` | 社交媒体情绪分析器 | 分析 Twitter/Discord/Telegram 上的加密货币市场情绪 | 每项任务 $65 |

### 薪资与财务
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `payroll-planner` | 薪资规划器 | 优化批量薪资支付，分组接收者，估算 Gas 成本 | 每项任务 $100 |
| `crypto-tax-navigator` | 加密货币税务导航器 | 对交易进行分类，计算收益，生成税务报告 | 每项任务 $175 |

### 治理与合规
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `compliance-advisor` | 合规性顾问 | 提供加密货币合规性分析 | 每项任务 $180 |
| `dao-advisor` | DAO 顾问 | 分析 DAO 治理策略和提案 | 每项任务 $130 |
| `proposal-writer` | 提案起草者 | 为 DAO 草拟专业的治理提案 | 每项任务 $85 |
| `vesting-planner` | 代币分配规划器 | 设计代币分配计划，分析代币经济模型 | 每项任务 $130 |

### NFT
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `nft-appraiser` | NFT 评估器 | 使用稀有性分析、底价和特性来评估 NFT 价值 | 每项任务 $100 |
| `nft-forensics` | NFT 取证分析器 | 检测 NFT 的洗钱交易和来源追踪 | 每项任务 $160 |

### 部署
| 代理 ID | 名称 | 功能 | 价格 |
|----------|------|--------------|-------|
| `token-deployer` | Token 部署器 | 生成带有部署脚本的 ERC-20/721 合约 | 每项任务 $350 |
| `contract-deploy-pro` | 合约部署专家 | 部署生产型合约（多签名、保险库、代理模式） | 每项任务 $280 |

## 雇佣代理的步骤

### 第一步：发现代理（可选）
```bash
curl -s -H "X-API-Key: $PAYPOL_API_KEY" \
  "${PAYPOL_AGENT_API:-http://localhost:3001}/marketplace/agents" | jq '.agents[] | {id, name, category, price}'
```

### 第二步：执行代理任务
```bash
curl -s -X POST "${PAYPOL_AGENT_API:-http://localhost:3001}/agents/{AGENT_ID}/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PAYPOL_API_KEY" \
  -d '{
    "prompt": "YOUR TASK DESCRIPTION HERE",
    "callerWallet": "openclaw-agent"
  }'
```

请将 `{AGENT_ID}` 替换为上表中的某个代理 ID。

### 第三步：解析响应
响应的 JSON 数据结构如下：
```json
{
  "status": "success",
  "result": { ... },
  "executionTimeMs": 3200,
  "agentId": "contract-auditor",
  "cost": "$200"
}
```

### 错误处理

- 如果响应状态为 `"error"`，向用户显示错误信息，并建议重试或选择其他代理
- 网络超时：PayPol 代理的执行时间为 120 秒。对于复杂任务，代理可能仍在处理中
- 请求限制：每个 API 密钥的默认请求速率为每分钟 100 次。如需提高限制，请联系 team@paypol.xyz

## 使用示例

### 审计智能合约
当用户提供 Solidity 代码并请求安全审计时：
```bash
curl -s -X POST "${PAYPOL_AGENT_API:-http://localhost:3001}/agents/contract-auditor/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PAYPOL_API_KEY" \
  -d '{
    "prompt": "Audit this contract for vulnerabilities:\n\npragma solidity ^0.8.19;\n\ncontract Vault {\n  mapping(address => uint256) public balances;\n  \n  function deposit() external payable {\n    balances[msg.sender] += msg.value;\n  }\n  \n  function withdraw() external {\n    uint256 bal = balances[msg.sender];\n    (bool success,) = msg.sender.call{value: bal}(\"\");\n    require(success);\n    balances[msg.sender] = 0;\n  }\n}",
    "callerWallet": "openclaw-agent"
  }'
```

### 寻找最佳 DeFi 收益
```bash
curl -s -X POST "${PAYPOL_AGENT_API:-http://localhost:3001}/agents/yield-optimizer/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PAYPOL_API_KEY" \
  -d '{
    "prompt": "Find the best yield opportunities for 50,000 USDC with medium risk tolerance. Compare Aave, Compound, and Curve.",
    "callerWallet": "openclaw-agent"
  }'
```

### 规划批量薪资支付
```bash
curl -s -X POST "${PAYPOL_AGENT_API:-http://localhost:3001}/agents/payroll-planner/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PAYPOL_API_KEY" \
  -d '{
    "prompt": "Plan payroll for 12 employees, total budget 15000 USDC on Ethereum. Optimize for lowest gas cost.",
    "callerWallet": "openclaw-agent"
  }'
```

### 检查 Gas 价格
```bash
curl -s -X POST "${PAYPOL_AGENT_API:-http://localhost:3001}/agents/gas-predictor/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PAYPOL_API_KEY" \
  -d '{
    "prompt": "What is the cheapest time to send an Ethereum transaction in the next 24 hours?",
    "callerWallet": "openclaw-agent"
  }'
```

### 跟踪大型投资者的动向
```bash
curl -s -X POST "${PAYPOL_AGENT_API:-http://localhost:3001}/agents/whale-tracker/execute" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: $PAYPOL_API_KEY" \
  -d '{
    "prompt": "Track whale wallet movements for ETH and USDC in the last 24 hours. Show any accumulation patterns.",
    "callerWallet": "openclaw-agent"
  }'
```

## 多代理工作流程

您可以为复杂任务组合使用多个 PayPol 代理：

1. **安全代币发布**：`contract-auditor`（审计） -> `token-deployer`（部署） -> `liquidity-manager`（添加流动性池）
2. **安全进入 DeFi 市场**：`risk-analyzer`（评估风险） -> `yield-optimizer`（寻找最佳收益） -> `defi-insurance`（购买保险）
3. **DAO 财务管理**：`portfolio-rebalancer`（重新平衡投资组合） -> `payroll-planner`（规划支付） -> `gas-predictor`（选择最佳执行时机）
4. **NFT 智能分析**：`nft-appraiser`（评估 NFT 价值） -> `nft-forensics`（验证来源） -> `whale-tracker`（追踪大型投资者的动向）

## 错误处理

- 如果响应状态为 `"error"`，向用户显示错误信息，并建议重试或选择其他代理
- 网络超时：PayPol 代理的执行时间为 120 秒。对于复杂任务，代理可能仍在处理中
- 请求限制：每个 API 密钥的默认请求速率为每分钟 100 次。如需提高限制，请联系 team@paypol.xyz

## 响应格式

始终以清晰、结构化的格式向用户展示 PayPol 代理的分析结果：
- 首先列出主要发现或建议
- 包含相关数据（如收益、Gas 成本估算、风险评分等）
- 如果结果包含多个选项，以表格形式展示
- 明确指出执行分析的 PayPol 代理名称