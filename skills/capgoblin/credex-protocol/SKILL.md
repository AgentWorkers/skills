---
name: credex-protocol
description: 使用 Credex 协议，为 Arc Network 上的 AI 代理访问未受保护的信用额度。这些信用额度可用于：  
1. 以声誉作为抵押借入 USDC；  
2. 偿还债务以增加信用额度；  
3. 作为 LP（ liquidity provider，提供流动性）；  
4. 通过 Circle Bridge 管理跨链的 USDC。  
相关操作触发条件包括：  
- “从 Credex 借款”；  
- “偿还债务”；  
- “向池中存款”；  
- “检查信用状态”；  
- “提供流动性”；  
- 或任何与信用/借贷相关的操作。
---

# Credex 协议技能

本技能用于与 Credex 协议进行交互，这是一个为 Arc Network 上的 AI 代理提供去中心化信用服务的系统。

---

## 使用方法

**基础目录：** `{baseDir}`（包含本 SKILL.md 文件的目录）

**所有命令均需从项目根目录执行：**

```bash
cd {baseDir}
npx ts-node scripts/client.ts <command> [args]   # Borrower commands
npx ts-node scripts/lp.ts <command> [args]       # LP commands
```

**输出格式：** 所有脚本返回的均为 **JSON** 格式，便于机器读取。请解析输出内容以获取 `creditLimit`、`txHash`、`debt` 等字段。

---

## 环境变量

### 必需设置的环境变量

| 变量                | 说明                                      |
| ---------------------- | ------------------------------------------------------ |
| `WALLET_PRIVATE_KEY` | 用于签署交易的私钥。**缺少此变量，所有命令将失败。** |
| `RPC_URL`            | Arc Network 的 RPC 地址。默认值：`https://rpc.testnet.arc.network` |

### 可选设置的环境变量

| 变量                | 说明                                      | 默认值                                      |
| ---------------------- | ------------------------------------------------------ |
| `CREDEX_POOL_ADDRESS` | Credex 池合约地址            | `0x32239e52534c0b7e525fb37ed7b8d1912f263ad3`         |
| `CREDEX_AGENT_URL`    | Credex 代理服务器 URL                         | `http://localhost:10003`                         |

**运行前检查：** 在执行任何命令之前，请确认 `WALLET_PRIVATE_KEY` 已设置。如果未设置，系统会提示用户输入。

---

## 合约地址（Arc 测试网）

| 合约                | 地址                                      |
| ---------------------- | ------------------------------------------------------ |
| `CredexPool`          | `0x32239e52534c0b7e525fb37ed7b8d1912f263ad3`         |
| `USDC` (Arc)          | `0x3600000000000000000000000000000000000000`         |
| `USDC` (Base Sepolia)     | `0x036CbD53842c5426634e7929541eC2318f3dCF7e`         |

---

## 客户端命令（借款人）

**脚本：`scripts/client.ts`**  
**执行方式：** `npx ts-node scripts/client.ts <命令> [参数]`

---

### `status`

查询代理的信用状态。

**使用方法：**

```bash
npx ts-node scripts/client.ts status <address>
```

**参数：**

- `address`（可选）：钱包地址。默认使用 `WALLET_PRIVATE_KEY` 对应的地址。

**返回值：** JSON 格式的数据。

---

### `borrow`

从池中借款 USDC。

**使用方法：**

```bash
npx ts-node scripts/client.ts borrow <amount>
```

**参数：**

- `amount`（必填）：借款的 USDC 数量（以小数字符串形式表示，例如 `"5.0"`）。

**返回值：** JSON 格式的数据。

**注意：** 在执行 `borrow` 命令前，请使用 `availableCredit` 函数确认是否有足够的资金。

---

### `repay`

向池中偿还债务。

**使用方法：**

```bash
npx ts-node scripts/client.ts repay <amount|all>
```

**参数：**

- `amount`：需要偿还的 USDC 数量（例如 `"5.0"`）。
- `all`：计算总债务并加上 1% 的缓冲金额后全额偿还。实际偿还金额不会超过实际欠款。

**返回值：** JSON 格式的数据。

**说明：** 还款时首先支付利息，然后偿还本金。每次成功还款后，信用额度会增加 10%。

---

### `bridge`

在 Arc 测试网和 Base Sepolia 之间转移 USDC。

**使用方法：**

```bash
npx ts-node scripts/client.ts bridge <amount> <from> <to>
```

**参数：**

- `amount`：转移的 USDC 数量（例如 `"10.0"`）。
- `from`：源链（`arc` 或 `base`）。
- `to`：目标链（`arc` 或 `base`）。

**返回值：** JSON 格式的数据。

**注意：** 源链和目标链必须不同。

---

### `balance`

查询两个链上的钱包余额。

**使用方法：**

```bash
npx ts-node scripts/client.ts balance
```

**返回值：** JSON 格式的数据。

---

## 流动性提供者（LP）相关命令

**脚本：`scripts/lp.ts`**  
**执行方式：** `npx ts-node scripts/lp.ts <命令> [参数]`

---

### `pool-status`

查询池的整体健康状况和指标。

**使用方法：**

```bash
npx ts-node scripts/lp.ts pool-status
```

**返回值：** JSON 格式的数据。

---

### `deposit`

存入 USDC 以获取 LP 股份。

**使用方法：**

```bash
npx ts-node scripts/lp.ts deposit <amount>
```

**参数：**

- `amount`：存入的 USDC 数量（例如 `"100.0"`）。

**返回值：** JSON 格式的数据。

---

### `withdraw`

燃烧 LP 股份以提取 USDC。

**使用方法：**

```bash
npx ts-node scripts/lp.ts withdraw <shares|all>
```

**参数：**

- `shares`：要燃烧的 LP 股份数量（例如 `"50.0"`）。
- `all`：根据可用流动性提取最大金额。

**返回值：** JSON 格式的数据。

**注意：** 如果所有 USDC 都已被借出，提取金额可能会受到限制。

---

### `lp-balance`

查询某个地址的 LP 持有情况。

**使用方法：**

```bash
npx ts-node scripts/lp.ts lp-balance [address]
```

**返回值：** JSON 格式的数据。

---

## 协议机制

### 利息计算

- **利率：** 每个时间间隔（1 分钟）0.1%（测试网环境下的加速速率）。
- **公式：** `debt = principal + accrued_interest`（债务 = 本金 + 累计利息）。

### 信用额度增长

每次还款后，信用额度会增加：

```
newLimit = currentLimit × 1.10
```

最大信用额度为 10,000 USDC。

### 可用信用额度

```
availableCredit = creditLimit - principal
```

利息不会影响借款能力，仅影响本金。

### LP 股份价格

```
sharePrice = totalAssets / totalShares
```

其中 `totalAssets = liquidity + outstandingDebt`（总资产 = 流动性 + 未偿还债务）。

---

## 工作流程示例

### 借款人流程

```text
1. Check status     → npx ts-node scripts/client.ts status
2. Borrow           → npx ts-node scripts/client.ts borrow 5
3. Use funds        → (perform task on Arc or bridge to Base)
4. Bridge back      → npx ts-node scripts/client.ts bridge 5 base arc
5. Repay            → npx ts-node scripts/client.ts repay all
6. Verify growth    → npx ts-node scripts/client.ts status (limit increased!)
```

### 流动性提供者流程

```text
1. Check pool       → npx ts-node scripts/lp.ts pool-status
2. Deposit          → npx ts-node scripts/lp.ts deposit 100
3. Monitor          → npx ts-node scripts/lp.ts lp-balance
4. Withdraw         → npx ts-node scripts/lp.ts withdraw all
```

---

## 常见错误及解决方法

| 错误类型            | 原因                                      | 解决方法                                      |
| ---------------------- | -------------------------------------- | ------------------------------------------------------ |
| `WALLET_PRIVATE_KEY 未设置` | 环境变量缺失                              | 在执行前设置 `WALLET_PRIVATE_KEY`                         |
| 超过信用额度          | `amount > availableCredit`           | 调用 `status` 函数检查余额后再尝试借款                   |
| 钱包余额不足          | 钱包中没有 USDC                             | 通过桥接服务获取 USDC 或在其他链上充值                   |
| 流动性不足            | 池中所有 USDC 都已被借出                         | 等待借款人还款或 LP 提供者充值                         |
| 交易冲突            | 交易尝试失败                               | 等待 10 秒后重试                                 |
| 桥接服务超时            | 桥接服务出现故障                             | 等待 5-10 分钟，并检查两个链上的余额                     |
| 源链和目标链相同          | `from` 和 `to` 指定的是同一链                         | 更改源链和目标链的值                         |

---

## 参考资料

- 完整的 ABI（应用程序接口）和类型定义请参见 `references/contracts.md`。
- 实现细节请参考 `scripts/client.ts` 和 `scripts/lp.ts` 文件。