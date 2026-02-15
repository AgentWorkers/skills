---
name: morpho-earn
description: 通过在 Morpho（Base）平台的 Moonwell Flagship USDC 金库中提供 USDC 来获得收益。该功能适用于存入 USDC、从金库中提取资金、查看持仓/年化收益率（APY），或为去中心化金融（DeFi）收益服务设置钱包凭证时使用。
version: 1.2.0
metadata: {"clawdbot":{"emoji":"🌜🌛","category":"defi","requires":{"bins":["node"]}}}
---

# Morpho Earn — 通过 Moonwell Flagship USDC 仓库安全地获取收益

您可以通过 Base（Morpho 协议）上的 Moonwell Flagship USDC 仓库来获取 USDC 的收益。

**仓库地址：** `0xc1256Ae5FF1cf2719D4937adb3bbCCab2E00A2Ca`  
**链：** Base（8453）  
**资产：** USDC（`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`）

## 为什么选择这个仓库？

Moonwell Flagship USDC 仓库是 **在 Base 上获取收益的最安全方式之一**：

- **为 Coinbase 提供支持** — 为 Coinbase 的 BTC/ETH 借款产品提供超过 2000 万美元的流动性  
- **仅使用优质抵押品** — 借款由 ETH、cbETH、wstETH、cbBTC 支持  
- **保守的杠杆比率** — 严格的抵押品要求  
- **隔离的风险管理** — 风险被有效隔离  
- **禁止再抵押** — 您的 USDC 不会被再次借出  
- **经过严格测试** — Morpho 的代码库仅有不到 650 行，且不可更改，经过全面审计  
- **多层治理结构** — Moonwell DAO + Block Analitica/Protocol 策展者 + 安全委员会共同管理

### 当前年化收益率（约 4.5-5%）

| 组成部分 | 年化收益率 | 来源 |
|-----------|-----|--------|
| Base 收益 | 约 4% | 借款人的利息 |
| 奖励 | 约 0.5-1% | WELL + 通过 Merkl 的 MORPHO 奖励 |
| **总计** | 约 4.5-5% | 来自真实借款需求 |

收益率来源于真实的借款需求，而非不可持续的发行。您可以使用 `npx tsx status.ts` 查看当前年化收益率。

## 快速入门

```bash
cd ~/clawd/skills/morpho-yield/scripts
npm install
npx tsx setup.ts
```

设置向导将：
1. 配置您的钱包（私钥文件、环境变量或 1Password）  
2. 设置通知偏好（每日/每周报告）  
3. 设置复利阈值和自动复利选项  
4. 自动将相关信息添加到 HEARTBEAT.md 文件中

## 命令

### 交互式设置

```bash
npx tsx setup.ts
```

指导您完成钱包配置和偏好设置。

### 查看持仓和年化收益率

```bash
npx tsx status.ts
```

返回：当前存款金额、仓库份额、年化收益率以及钱包余额。

### 生成报告

```bash
# Telegram/Discord format (default)
npx tsx report.ts

# JSON format (for automation)
npx tsx report.ts --json

# Plain text
npx tsx report.ts --plain
```

生成格式精美的报告，显示您的持仓、奖励和预估收益。

### 存入 USDC

```bash
npx tsx deposit.ts <amount>
# Example: deposit 100 USDC
npx tsx deposit.ts 100
```

将 USDC 存入 Moonwell 仓库。需要足够的 USDC 余额和 Base 上的 ETH（作为交易手续费）。

### 提取

```bash
# Withdraw specific amount of USDC
npx tsx withdraw.ts <amount>

# Withdraw all (redeem all shares)
npx tsx withdraw.ts all
```

### 查看奖励

```bash
npx tsx rewards.ts
```

返回：可领取的 MORPHO、WELL 以及其他通过 Merkl 发放的奖励代币。

### 领取奖励

```bash
npx tsx rewards.ts claim
```

从 Merkl 分发器将所有待领取的奖励领取到您的钱包。

### 自动复利

```bash
npx tsx compound.ts
```

一站式命令：
1. 从 Merkl 领取所有待领取的奖励  
2. 通过 Odos 中继器将奖励代币（MORPHO、WELL）兑换成 USDC  
3. 将 USDC 存回仓库

## Heartbeat 集成

设置完成后，系统会根据您的存款金额定期检查您的持仓情况：

| 存款金额 | 复利检查频率 | 原因 |
|--------------|----------------|-----------|
| $10,000+ | 每日 | 大额持仓能快速累积可观收益 |
| $1,000-$10,000 | 每 3 天 | 在交易手续费和收益积累之间取得平衡 |
| $100-$1,000 | 每周 | 小额持仓需要更多时间才能覆盖交易手续费 |
| <$100 | 每两周 | 极小额持仓，仅在收益超过手续费时才进行复利 |

系统将：
- 按设定频率检查奖励余额  
- 当奖励超过阈值（默认为 $0.50）时进行复利计算  
- 根据您的偏好发送持仓报告（每日/每周）  
- 在交易手续费不足时提醒您

## 配置

配置文件位置：`~/.config/morpho-yield/config.json`  
偏好设置文件位置：`~/.config/morpho-yieldpreferences.json`

## 安全性

⚠️ **本功能涉及实际资金，请谨慎操作：**  
- 私钥在运行时从您指定的来源加载  
- 脚本从不记录或保存私钥到磁盘  
- 所有交易在执行前都会进行模拟  
- 每次运行时都会验证合约地址  
- 脚本在发送交易前会显示交易预览

### 推荐设置：

1. **专用钱包** — 为该功能创建一个专用热钱包  
2. **限制存款金额** — 仅存入您愿意放在热钱包中的资金  
3. **安全存储私钥** — 使用加密文件或 1Password 进行存储  
4. **定期监控交易** — 定期检查钱包交易记录  
5. **确保有足够的 ETH** — 在 Base 上保持少量 ETH 以支付交易手续费

## 奖励

该仓库通过 [Merkl](https://merkl.xyz) 为您赚取额外收益：
- **WELL** — Moonwell 的治理代币奖励  
- **MORPHO** — Morpho 协议的奖励  

奖励大约每 8 小时更新一次。`compound.ts` 脚本负责：
1. 从 Merkl 分发器领取奖励  
2. 通过 [Odos](https://odos.xyz) 中继器将奖励代币兑换成 USDC  
3. 将 USDC 存回仓库

## 错误处理

| 错误类型 | 原因 | 解决方法 |
|-------|-------|-----|
| USDC 不足 | 钱包中 USDC 不够 | 从 Base 向钱包中转移更多 USDC |
| 交易手续费不足 | Base 上的 ETH 不够 | 向钱包中添加 ETH |
| 配置未完成 | 配置文件缺失 | 运行 `npx tsx setup.ts`  
| RPC 错误 | 网络问题 | 检查 RPC 地址或重试 |
| 交易失败 | 交易手续费估算错误 | 脚本会自动添加 50% 的缓冲金 |

## 依赖项

这些脚本需要 Node.js 18.0 及更高版本。首次运行前请安装以下依赖项：

```bash
cd scripts && npm install
```

使用的包：
- `viem` — 用于与 Ethereum 交互  
- `tsx` — 用于 TypeScript 的执行环境