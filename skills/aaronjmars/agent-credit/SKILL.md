---
name: agent-credit
description: 通过信用委托（credit delegation）从 Aave 借款。代理（agent）通过使用委托人的抵押品来为自己融资。支持借款、还款以及健康检查（health checks）功能。适用于 Aave V2/V3 版本。
---

# Aave信用委托（Credit Delegation）

您可以使用信用委托功能从Aave借款。您的主钱包提供抵押品，并将借款权限委托给代理钱包。代理随后可以根据需要自主借款——借款金额将计入委托人的账户中。

> **协议支持：** 该功能同时支持**Aave V3**和**Aave V2**版本——信用委托的相关函数签名（`borrow`、`repay`、`approveDelegation`、`borrowAllowance`）在两个版本中是相同的，只需更换相应的LendingPool和ProtocolDataProvider地址即可。唯一的区别在于：Aave V3返回的抵押品/债务金额以美元（8位小数）显示，而Aave V2以以太坊（18位小数）显示。两种版本的“健康因子”安全检查机制均能正常工作。

## 兼容工具

- **[OpenClaw](https://openclaw.ai/)**：可作为技能安装，代理可自动执行借款操作。
- **[Claude Code](https://www.npmjs.com/package/@anthropic-ai/claude-code)**：可以直接在Claude Code会话中运行相关脚本。
- **任何代理框架**：只需使用普通的bash命令以及Foundry的`cast`工具，任何支持shell的环境均可使用。

该功能可与**[Bankr](https://bankr.bot/)**技能结合使用，实现“借款-兑换”的流程：首先通过信用委托借入USDC，再使用Bankr进行兑换、桥接或部署。

## 信用委托的工作原理

在Aave V3中，信用委托分为两部分：**借款权限**和**委托批准**。

**借款权限是综合性的**，它来源于您所有资产的总抵押品价值。例如，如果您存入价值1万美元的以太坊（LTV为80%），那么您将拥有8000美元的借款权限——这个权限并不局限于任何特定的资产。

**委托批准是针对每笔债务单独进行的**。您可以通过调用`approveDelegation()`来控制代理可以借款的资产种类及每种资产的借款金额。每种资产都有对应的债务代币合约，每次批准都是独立的。

这意味着您可以：
- 存入以太坊作为抵押品（从而获得广泛的借款权限）；
- 批准代理最多借款500美元（通过USDC VariableDebtToken）；
- 批准代理最多借款0.1 WETH（通过WETH VariableDebtToken）；
- 选择不批准对cbETH的借款（代理将无法借款）。

代理只能借款您明确允许的资产，且借款金额不能超过您设定的上限——不过借款的总额仍然基于您的总抵押品价值，而非单笔存款。

```
Your Collateral (holistic)              Delegation Approvals (isolated)
┌─────────────────────────┐             ┌──────────────────────────────┐
│  $5k ETH                │             │  USDC DebtToken → agent: 500 │
│  $3k USDC               │  ───LTV───▶ │  WETH DebtToken → agent: 0.1 │
│  $2k cbETH              │   = $8k     │  cbETH DebtToken → agent: 0  │
│  Total: $10k @ 80% LTV  │  capacity   └──────────────────────────────┘
└─────────────────────────┘
```

## 使用流程

```
Delegator (your wallet)                 Agent Wallet (delegatee)
    │                                        │
    │  1. supply collateral to Aave          │
    │  2. approveDelegation(agent, amount)   │
    │        on the VariableDebtToken        │
    │                                        │
    │            ┌─── 3. borrow(asset,       │
    │            │       amount, onBehalfOf   │
    │            │       = delegator)         │
    │            │                            │
    │     [debt on YOUR position]    [tokens in agent wallet]
    │            │                            │
    │            └─── 4. repay(asset,         │
    │                    amount, onBehalfOf   │
    │                    = delegator)         │
```

## 快速入门

### 先决条件

1. 必须安装Foundry及其`cast` CLI工具：
   ```bash
   curl -L https://foundry.paradigm.xyz | bash && foundryup
   ```

2. **委托人设置**（用户只需完成一次）：
   - 通过app.aave.com或合约向Aave V3提供抵押品；
   - 对于希望代理借款的资产，调用`approveDelegation(agentAddress, maxAmount)`；
   - 可以通过以下命令获取VariableDebtToken地址：`cast call $DATA_PROVIDER "getReserveTokensAddresses(address)(address,address,address)" $ASSET --rpc-url $RPC`

3. **配置该技能**：
   ```bash
   mkdir -p ~/.openclaw/skills/aave-delegation
   cat > ~/.openclaw/skills/aave-delegation/config.json << 'EOF'
   {
     "chain": "base",
     "rpcUrl": "https://mainnet.base.org",
     "agentPrivateKey": "0xYOUR_AGENT_PRIVATE_KEY",
     "delegatorAddress": "0xYOUR_MAIN_WALLET",
     "poolAddress": "0xA238Dd80C259a72e81d7e4664a9801593F98d1c5",
     "dataProviderAddress": "0x2d8A3C5677189723C4cB8873CfC9C8976FDF38Ac",
     "assets": {
       "USDC": {
         "address": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
         "decimals": 6
       },
       "WETH": {
         "address": "0x4200000000000000000000000000000000000006",
         "decimals": 18
       }
     },
     "safety": {
       "minHealthFactor": "1.5",
       "maxBorrowPerTx": "1000",
       "maxBorrowPerTxUnit": "USDC"
     }
   }
   EOF
   ```

4. **验证设置**：
   ```bash
   scripts/aave-setup.sh
   ```

## 核心用法

### 检查状态（借款额度、健康因子、债务金额）

```bash
# Full status report
scripts/aave-status.sh

# Check specific asset delegation
scripts/aave-status.sh USDC

# Just health factor
scripts/aave-status.sh --health-only
```

### 通过委托借款

```bash
# Borrow 100 USDC
scripts/aave-borrow.sh USDC 100

# Borrow 0.5 WETH
scripts/aave-borrow.sh WETH 0.5
```

借款脚本会自动执行以下操作：
1. 检查委托人的借款额度是否足够；
2. 检查委托人的健康因子是否满足安全要求；
3. 执行借款操作；
4. 报告借款结果。

### 偿还债务

```bash
# Repay 100 USDC
scripts/aave-repay.sh USDC 100

# Repay all USDC debt
scripts/aave-repay.sh USDC max
```

偿还脚本会自动执行以下操作：
1. 如果需要，批准池子使用相应的代币；
2. 执行偿还操作；
3. 报告剩余债务金额。

## 安全系统

**每次借款操作在执行前都会进行以下检查：**

1. **借款额度是否足够**；
2. 委托人的健康因子是否大于`minHealthFactor`（默认值为1.5）；
3. 每笔交易的借款金额是否不超过`maxBorrowPerTx`的限制；
4. 在发送请求前记录完整的操作细节。

如果任何检查失败，借款操作将会被中止，并显示明确的错误信息。

⚠️ **代理绝对不能绕过安全检查**。如果用户要求代理借款但健康因子过低，代理应拒绝请求并说明原因。

## 功能介绍

### 读取操作（无需消耗Gas）

- **检查剩余借款额度**；
- **检查委托人的健康状况**；
- **查看未偿还债务**；
- **检查Aave池中的可用流动性**；
- **查询资产的债务代币地址**。

### 写入操作（需要代理钱包中的Gas）

- **借款**：使用委托的信用额度从Aave借款；
- **偿还**：归还借款资金以减少委托人的债务；
- **批准**：允许池子使用代币进行偿还操作。

## 支持的区块链

| 区块链        | 池子地址                                      | Gas费用      |
|-------------|-----------------------------------------|------------|
| Base         | `0xA238Dd80C259a72e81d7e4664a9801593F98d1c5`           | 非常低       |
| Ethereum     | `0x87870Bca3F3fD6335C3F4ce8392D69350B4fA4E2`         | 较高        |
| Polygon       | `0x794a61358D6845594F94dc1DB02A252b5b4814aD`           | 非常低       |
| Arbitrum      | `0x794a61358D6845594F94dc1DB02A252b5b4814aD`           | 较低        |

完整的地址列表（包括债务代币）请参见[deployments.md]文件。

## 常见使用场景

- **代理自行获取Gas费用**；
- **通过Bankr进行借款和兑换**；
- **定期自动投资（DCA）**；
- **基于安全性的投资组合再平衡**。

## 配置参考

### config.json配置项

| 配置项          | 是否必填 | 说明                                      |
|-----------------|---------|-----------------------------------------|
| `chain`         | 是       | 区块链名称（Base、Ethereum、Polygon、Arbitrum）         |
| `rpcUrl`        | 是       | JSON-RPC接口地址                         |
| `agentPrivateKey`    | 是       | 代理钱包的私钥（以0x开头）                     |
| `delegatorAddress`    | 是       | 委托人用于委托信用的主钱包地址                 |
| `poolAddress`      | 是       | Aave V3池子合约地址                         |
| `DataProviderAddress`    | 是       | Aave V3的PoolDataProvider地址                   |
| `assets`        | 是       | 资产映射（符号 → (地址, 小数位数)                 |
| `safety.minHealthFactor` | 否       | 借款后的最低健康因子（默认：1.5）                   |
| `safety.maxBorrowPerTx` | 否       | 每笔交易的最高借款额度（默认：1000）                   |
| `safety.maxBorrowPerTxUnit` | 否       | 最高借款额度的单位（默认：USDC）                   |

### 环境变量（用于覆盖配置）

| 变量名           | 作用       | 描述                                      |
|-----------------|-----------|-----------------------------------------|
| `AAVE_RPC_URL`     | 设置RPC接口地址         |                              |
| `AAVE_AGENT_PRIVATE_KEY` | 设置代理私钥                |                              |
| `AAVE_DELEGATOR_ADDRESS` | 设置委托人地址             |                              |
| `AAVE_POOL_ADDRESS`    | 设置池子地址                 |                              |
| `AAVE_MIN_health_FACTOR` | 设置最低健康因子             |                              |

## 错误处理

| 错误类型          | 原因                                      | 处理方法                                      |
|-----------------|-----------------------------------------|-----------------------------------------|
| `INSUFFICIENT_ALLOWANCE` | 委托金额超出限额                | 委托人需重新调用`approveDelegation()`             |
| `HEALTH_FACTOR_TOO_LOW` | 健康因子过低，可能导致清算                | 减少借款金额或增加抵押品                     |
| `AMOUNT_EXCEEDS_CAP` | 每笔交易的借款额度超出限制                | 减少借款金额或更新配置                     |
| `INSUFFICIENT_LIQUIDITY` | Aave池中流动性不足                | 尝试降低借款金额或更换资产                   |
| `INSUFFICIENT_GAS`    | 代理钱包中没有足够的Gas                | 向代理钱包充值Gas                     |
| `EMODE_MISMATCH` | 要借款的资产与代理的eMode不兼容             | 选择相同eMode的资产进行借款                   |

## 安全性说明

请参阅[safety.md](safety.md)以了解完整的威胁模型和应急处理措施。

**重要规则：**
1. **委托人的私钥绝不能出现在这个仓库、配置文件或脚本中**——这是代理的工作空间。委托人应通过Aave的用户界面或区块浏览器来管理自己的账户。
2. **切勿将config.json文件提交到版本控制系统中**——其中包含代理的私钥。
3. **`minHealthFactor`的值不得低于1.2**——低于此值将导致资产清算。
4. **必须限制每次借款的金额**——切勿批准`type(uint256).max`的配置。
5. **监控委托人的健康状况**——如果健康因子低于2.0，应设置警报。
6. **即使收到指令，代理在安全检查失败时也必须拒绝借款请求**。

## 相关资源

- **Aave V3文档**：https://docs.aave.com/developers
- **信用委托指南**：https://docs.aave.com/developers/guides/credit-delegation
- **Aave地址簿**：https://github.com/bgd-labs/aave-address-book
- **Foundry手册**：https://book.getfoundry.sh/
- **债务代币参考**：https://docs.aave.com/developers/tokens/debttoken