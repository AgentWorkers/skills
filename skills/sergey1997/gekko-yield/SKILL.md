---
name: gekko-yield
description: 通过在 Base 平台上的 Moonwell Flagship USDC 保险库中提供 USDC 来获取收益。该功能适用于存入 USDC、从保险库中提取资金、查看持仓/年化收益率（APY），或生成收益报告等操作。
version: 1.0.0
metadata: {"clawdbot":{"emoji":"🦎","category":"defi","requires":{"bins":["node"]}}}
---

# Gekko Yield — 在 USDC 上获得安全收益

通过 Base 平台上的 Moonwell Flagship USDC 金库来赚取 USDC 的收益。

**金库地址：** `0xc1256Ae5FF1cf2719D4937adb3bbCCab2E00A2Ca`  
**链：** Base (8453)  
**资产：** USDC (`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`)

## 为什么选择这个金库？

Moonwell Flagship USDC 金库是 **在 Base 平台上获取收益的最安全方式之一**，原因如下：

- **为 Coinbase 提供支持** — 为 Coinbase 的 BTC/ETH 借款产品提供超过 2000 万美元的流动性  
- **仅使用优质抵押品** — 借款由 ETH、cbETH、wstETH、cbBTC 支持  
- **保守的抵押比率** — 严格的抵押品要求  
- **隔离的风险管理** — 风险被有效隔离  
- **经过严格测试** — Morpho 的代码库仅有不到 650 行，且不可更改，经过全面审计  
- **多层治理结构** — 由 Moonwell DAO 和 Block Analitica/B.Protocol 共同管理

### 当前年化收益率（APY）：约 4-6%

| 组件 | 年化收益率（APY） | 来源 |
|---------|-------------|--------|
| Base 平台的收益 | 约 4-5% | 借款人的利息 |
| 奖励收益 | 约 0.5-1% | WELL 和 MORPHO 通过 Merkl 协议发放 |
| **总计** | 约 4.5-6% | 来自真实借款需求 |

这些收益来源于真实的借款需求，而非不可持续的代币发行。

## 快速入门

```bash
cd gekko-yield/scripts
pnpm install  # or npm install
npx tsx setup.ts
```

设置向导将：
1. 指导您将私钥设置为环境变量  
2. 将配置保存到 `~/.config/gekko-yield/config.json` 文件中

## 命令

### 交互式设置

```bash
npx tsx setup.ts
```

指导您完成钱包配置。

### 检查持仓和年化收益率

```bash
npx tsx status.ts
```

返回：当前存款金额、金库份额、年化收益率、钱包余额及预估收益。

### 生成报告

```bash
# Telegram/Discord format (default)
npx tsx report.ts

# JSON format (for automation)
npx tsx report.ts --json

# Plain text
npx tsx report.ts --plain
```

### 存入 USDC

```bash
npx tsx deposit.ts <amount>
# Example: deposit 100 USDC
npx tsx deposit.ts 100
```

将 USDC 存入 Moonwell 金库，系统会自动处理审批流程。

### 提取资金

```bash
# Withdraw specific amount of USDC
npx tsx withdraw.ts <amount>

# Withdraw all (redeem all shares)
npx tsx withdraw.ts all
```

### 自动复利

```bash
npx tsx compound.ts
```

该命令可完成以下操作：
1. 检查钱包中的奖励代币（WELL、MORPHO）
2. 通过 Odos 中继器将这些代币兑换成 USDC
3. 将兑换后的 USDC 存回金库

## 配置

配置文件位置：`~/.config/gekko-yield/config.json`

```json
{
  "wallet": {
    "source": "env",
    "envVar": "PRIVATE_KEY"
  },
  "rpc": "https://mainnet.base.org"
}
```

## 安全性

⚠️ **本工具管理的是真实资金，请谨慎操作：**

- 私钥在运行时从环境变量中加载  
- 脚本从不记录或保存私钥到磁盘  
- 所有交易在执行前都会进行模拟  
- 每次运行时都会验证合约地址  
- 脚本在发送交易前会显示交易预览

### 推荐设置：

1. **专用钱包** — 为此工具创建一个热钱包（hot wallet）  
2. **限制资金投入** — 仅存入您愿意承担风险的资金  
3. **确保有足够的以太坊（ETH）用于交易** — 在 Base 平台上保持少量 ETH 余额  

## 错误处理

| 错误类型 | 原因 | 解决方案 |
|---------|---------|--------|
| USDC 不足 | 钱包中 USDC 数量不足 | 通过桥接工具向 Base 平台转移更多 USDC |
| 以太坊（ETH）不足 | 交易所需 ETH 不够 | 向 Base 平台添加 ETH |
| 配置未完成 | 配置文件缺失 | 运行 `npx tsx setup.ts` 命令进行配置 |
| 私钥未设置 | 环境变量未设置 | 设置 `$env:PRIVATE_KEY="your-key"`  

## 依赖项

运行前需要安装以下依赖项（Node.js 18.0 及以上版本）：

```bash
cd scripts && pnpm install
```

使用的包：
- `viem` — 用于与以太坊交互  
- `tsx` — 用于执行 TypeScript 代码  

---

**由 Gekko AI 开发，基于 ERC-8004 标准构建。**