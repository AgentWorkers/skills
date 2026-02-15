# Arc Security - 代理信任协议

这是一个与链无关的安全基础设施，用于 OpenClaw 技能的验证与管理。审计员通过质押 USDC 来保证技能的安全性，用户需要支付小额费用才能使用经过验证的技能；恶意技能会通过去中心化的治理机制被剔除——所有这些功能都由 Arc 上的 CCTP（Chain Security Trust Protocol）提供支持。

## 安装

```bash
clawhub install arc-security
```

## 配置

请设置以下环境变量：

| 变量 | 是否必填 | 说明 |
|---|---|---|
| `ARC_RPC_URL` | 是 | Arc 测试网 RPC 端点（默认：`https://testnet-rpc.arc.network`） |
| `CONTRACT_ADDRESS` | 是 | 部署的 SkillSecurityRegistry 合同地址 |
| `PRIVATE_KEY` | 是 | 钱包私钥（用于签署交易） |
| `X402_SERVER_URL` | 是 | x402 支付服务器地址 |
| `ETH_RPC_URL` | 否 | Ethereum Sepolia RPC（用于跨链操作） |
| `BASE_RPC_URL` | 否 | Base Sepolia RPC（默认：`https://sepolia.base.org`） |
| `ARB_RPC_URL` | 否 | Arbitrum Sepolia RPC（默认：`https://sepolia-rollup.arbitrum.io/rpc`） |

## 命令

### `check` -- 检查技能的信任状态

查询任何技能的链上质押状态、审计员数量、使用统计信息以及计算出的信任分数。

```bash
clawhub arc-security check <skill_id>
```

**示例输出：**
```
Skill: youtube-downloader
├─ Bonded: 100.00 USDC by 3 auditors
├─ Used: 1,250 times
├─ Trust Score: 75/100
├─ Status: Safe to use
└─ Created: 2025-06-15 14:30:00
```

**信任分数** 的计算方式如下：  
- 40% 来自质押金额（最高为 100 USDC，即满分）  
- 40% 来自使用次数（最高为 1,000 次使用，即满分）  
- 20% 来自审计员数量（每位审计员 5 分）  
- 被标记为恶意的技能会扣除 50 分的信任分数  

### `use` -- 支付费用并下载技能

通过 x402 支付 0.10 USDC 的使用费用，并下载技能包。系统会根据你的钱包余额自动选择最便宜的支付路径。

```bash
clawhub arc-security use <skill_id>
```

**支付链选择优先级：**  
1. Arc 测试网（直接支付，无桥接费用）  
2. Base Sepolia（通过 CCTP）  
3. Arbitrum Sepolia（通过 CCTP）  
4. Ethereum Sepolia（通过 CCTP）  

### `bond` -- 为技能质押 USDC  

通过质押 USDC 来保证技能的安全性。如果该技能被发现具有恶意行为，你的质押金额的 50% 将被扣除。

```bash
clawhub arc-security bond <skill_id> <amount> <source_chain>
```

**参数：**  
- `skill_id` -- 技能标识符  
- `amount` -- 抵押的 USDC 数量（例如：`50`）  
- `source_chain` -- 支付来源链（`ethereum-sepolia`、`base-sepolia`、`arbitrum-sepolia`、`arc-testnet`）  

**示例：**  
```bash
clawhub arc-security bond youtube-downloader 50 base-sepolia
```

### `report` -- 举报恶意技能  

提交一份声明，指出某技能具有恶意行为。需要支付 1 USDC 的反垃圾信息费用（如果声明被验证，费用将退还）。  

```bash
clawhub arc-security report <skill_id> --evidence <ipfs_hash>
```

**示例：**  
```bash
clawhub arc-security report bad-skill --evidence QmXyz123...
```

系统会为审计员开启 72 小时的投票窗口。  

### `vote-claim` -- 对待处理的举报进行投票  

对举报的技能是否具有恶意行为进行投票。只有为该技能质押过资金的钱包才有投票资格。投票权重基于总质押金额和审计记录。  

**投票权重公式：** `sqrt(totalStaked) * (successfulAudits / totalAudits)`  

### `claim-earnings` -- 提取累积的费用  

提取你作为审计员所获得的费用。费用按以下比例分配：  
- 70% 归审计员（与质押金额成正比）  
- 30% 归保险池  

**支持的接收链：**  
- `arc-testnet`（直接转账）  
- `ethereum-sepolia`、`base-sepolia`、`arbitrum-sepolia`（通过 CCTP）  

## 支持的链：**

| 链 | CCTP 域名 | 支付方式 | 抵押方式 | 收益方式 |
|---|---|---|---|---|
| Arc 测试网 | 100 | 直接支付 | 直接支付 | 直接支付 |
| Ethereum Sepolia | 0 | 通过 CCTP | 通过 CCTP | 通过 CCTP |
| Base Sepolia | 6 | 通过 CCTP | 通过 CCTP | 通过 CCTP |
| Arbitrum Sepolia | 3 | 通过 CCTP | 通过 CCTP | 通过 CCTP |

## 费用结构

| 操作 | 费用 | 分配方式 |
|---|---|---|
| 使用技能 | 0.10 USDC | 70% 归审计员，30% 归保险池 |
| 提交举报 | 1.00 USDC（作为押金） | 如果举报被验证，押金退还 |
| 被判定为恶意 | 扣除 50% 的质押金额 | 80% 归受害者，20% 归保险池 |

## 架构

```
User (any chain)
  │
  ├── CCTP burn ──► Arc Testnet ──► SkillSecurityRegistry (bonds, fees, claims)
  │                                        │
  └── x402 GET ──► Payment Server ◄────────┘ (verifies payment on-chain)
                       │
                       └──► Skill package (ZIP)
```

1. **SkillSecurityRegistry**（基于 Arc 的 Solidity 合同）——负责管理质押金额、处理费用以及处理举报/投票/惩罚操作  
2. **x402 支付服务器**（Node.js）——通过 HTTP 402 网关提供技能包下载服务，并验证链上的支付操作  
3. **This skill**（Python 命令行工具）——用户界面，用于协调 CCTP 转账和合约调用  

## 许可证  

MIT