---
name: clawmegle-staking
description: 将 $CLAWMEGLE 代币进行质押，以从 Clanker LP 费用中获得双重奖励（ETH + CLAWMEGLE）。当代理希望质押代币、查看质押奖励、领取收益或管理其质押位置时，可以使用此功能。该系统支持 Bankr API 和直接钱包交易两种方式。
metadata:
  clawdbot:
    emoji: "🥩"
    homepage: "https://clawmegle.xyz"
    requires:
      skills: ["bankr"]
      bins: ["curl", "jq", "bc"]
---

# Clawmegle 质押

质押 $CLAWMEGLE 以获得 Clanker LP 费用的比例份额（ETH + CLAWMEGLE）。

## ⚠️ 重要提示：质押与奖励发放的区别

**这两种操作是不同的：**

| 操作        | 功能        | 目的        |
|------------|------------|------------|
| **质押**      | `stake(amount)`  | 锁定你的 CLAWMEGLE 以获得奖励 |
| **发放奖励**    | `depositRewards(amount) + ETH` | 为质押者添加可领取的奖励 |

**当你领取 Clanker LP 费用并希望分配它们时：**
→ 使用 `./scripts/deposit-rewards.sh <eth> <clawmegle>`  
→ **不要使用 `stake()`** —— 因为 `stake()` 会锁定代币，而不会给质押者奖励！

## 先决条件

### 第一步：设置 Bankr 账户

`bankr` 技能会自动作为依赖项安装，但你需要一个 Bankr 账户：

1. **访问 [bankr.bot](https://bankr.bot)` 并使用你的电子邮件注册**
2. **输入发送到你邮箱的 OTP**
3. **重要提示：** Bankr 会自动为你创建钱包：
   - EVM 钱包（Base、Ethereum、Polygon、Unichain）
   - Solana 钱包
   - 无需手动设置钱包！

### 第二步：获取 API 密钥

1. **访问 [bankr.bot/api](https://bankr.bot/api)**
2. **创建一个新的 API 密钥**
3. **启用“代理 API”访问权限**（进行交易时需要）
4. **复制密钥**（密钥以 `bk_` 开头）

### 第三步：配置技能

保存你的 API 密钥：

```bash
mkdir -p ~/.clawdbot/skills/bankr
cat > ~/.clawdbot/skills/bankr/config.json << 'EOF'
{
  "apiKey": "bk_YOUR_API_KEY_HERE",
  "apiUrl": "https://api.bankr.bot"
}
EOF
```

### 第四步：为 Bankr 钱包充值

你的 Bankr 钱包需要：
- **$CLAWMEGLE 代币** 用于质押
- **少量 ETH（在 Base 上）** 作为交易手续费（每笔交易约 0.001 ETH）

获取你的 Bankr 钱包地址：
```bash
./scripts/bankr.sh "What is my Bankr wallet address on Base?"
```

然后将 CLAWMEGLE 和 ETH 发送到该地址。

### 第五步：验证设置

```bash
./scripts/bankr.sh "What is my CLAWMEGLE balance on Base?"
```

如果你能看到自己的余额，那么你就可以开始质押了！

## 快速入门（通过 Bankr）

```bash
# Check your CLAWMEGLE balance
./scripts/bankr.sh "What is my CLAWMEGLE balance on Base?"

# Stake tokens
./scripts/stake-bankr.sh 1000

# Check pending rewards
./scripts/check-bankr.sh

# Claim rewards
./scripts/claim-bankr.sh

# Unstake
./scripts/unstake-bankr.sh 500
```

## 发放奖励（管理员/费用领取者）

在领取 Clanker LP 费用后，将其作为奖励进行发放：

```bash
# Deposit 0.001 ETH + 100 CLAWMEGLE as rewards
./scripts/deposit-rewards.sh 0.001 100

# Deposit ETH only
./scripts/deposit-rewards.sh 0.005 0

# Deposit CLAWMEGLE only  
./scripts/deposit-rewards.sh 0 200
```

这会将奖励按比例分配给所有当前的质押者。

## 替代方案：直接使用钱包（高级用户）

对于拥有自己钱包基础设施的代理用户：
```bash
# Key should be in your environment (e.g., ~/.clawdbot/wallets/)
export PRIVATE_KEY=$(cat ~/.clawdbot/wallets/.your_key)

./scripts/stake.sh 1000
./scripts/claim.sh
./scripts/check.sh
```

## 合同详情

| 项目        | 值         |
|------------|------------|
| **合同**      | `0x56e687aE55c892cd66018779c416066bc2F5fCf4`（待部署） |
| **代币**      | `0x94fa5D6774eaC21a391Aced58086CCE241d3507c` |
| **链**       | Base（chainId: 8453） |
| **RPC**      | `https://mainnet.base.org` |

## 可用的操作

### 质押 $CLAWMEGLE

存入代币以开始获得奖励。

```bash
./scripts/stake.sh <AMOUNT>
# Example: ./scripts/stake.sh 5000
```

或者通过 Bankr：
```bash
scripts/bankr.sh "Submit this transaction on Base: {\"to\": \"<CONTRACT>\", \"data\": \"<STAKE_CALLDATA>\", \"value\": \"0\"}"
```

### 查看待领取的奖励

查看你已获得的 ETH 和 CLAWMEGLE 的总额。

```bash
./scripts/check.sh
# Returns: ethPending, clawmeglePending
```

### 领取奖励

在不解除质押的情况下提取你获得的 ETH 和 CLAWMEGLE。

```bash
./scripts/claim.sh
```

### 解除质押

提取你质押的代币，并自动领取待领取的奖励。

```bash
./scripts/unstake.sh <AMOUNT>
# Example: ./scripts/unstake.sh 5000
```

### 查看质押情况

查看你当前质押的代币数量。

```bash
./scripts/balance.sh
```

## 奖励机制

1. **来源**：来自 $CLAWMEGLE 交易的 Clanker LP 费用
2. **分配方式**：你按比例获得 ETH 和 CLAWMEGLE
3. **计算公式**：`你的奖励 = (你的质押数量 / 总质押数量) * 发放的奖励`
4. **领取时间**：奖励会持续累积，随时可以领取

## 安全性

- **无需管理员密钥** —— 合同无法被恶意消耗
- **无锁定机制** —— 可随时解除质押
- **抗操纵奖励分配** —— 防止恶意操纵奖励分配
- **经过审计的设计** —— 使用 OpenZeppelin 和 MasterChef 累加器

## 所需条件

- 在 `~/.clawdbot/skills/bankr/config.json` 中配置了 Bankr API 密钥
- 拥有用于支付 Base 上交易手续费的 ETH 和私钥
- **$CLAWMEGLE 代币** 用于质押
- **少量 ETH** 作为交易手续费（每笔交易约 0.001 ETH）

## 故障排除

| 问题        | 解决方案        |
|------------|------------|
| “余额不足”     | 先获取 $CLAWMEGLE       |
| “手续费不足”    | 需要在 Base 上有 ETH       |
| “权限问题”     | 由审批脚本处理       |
| 无待领取的奖励 | 尚未发放奖励，或仅进行了质押 |

## 参考资料

- [合同 ABI 与示例](references/contract.md)
- [Bankr 交易格式](references/bankr-format.md)