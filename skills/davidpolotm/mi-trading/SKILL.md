---
name: clawdex
description: 使用 ClawDex CLI 在 Solana 上进行代币交易。适用于用户需要交换代币、查看余额、获取报价或管理 Solana 交易钱包的场景。
tools: Bash, Read
metadata:
  tags: solana, trading, defi, jupiter, swap, crypto
---

# ClawDex — Solana DEX交易技能

通过Jupiter聚合器进行Solana代币的交易，支持模拟交易、安全防护机制，并提供完整的JSON输出结果。

## 先决条件

在使用此技能之前，请确保已安装并配置了ClawDex：

```bash
which clawdex || npm install -g clawdex@latest
```

如果尚未配置，请运行初始化脚本：
```bash
clawdex status --json
```
如果初始化失败，请按照以下步骤进行配置：
```bash
clawdex onboarding \
  --jupiter-api-key "$JUPITER_API_KEY" \
  --rpc "${SOLANA_RPC_URL:-https://api.mainnet-beta.solana.com}" \
  --wallet ~/.config/solana/id.json \
  --json
```

## 命令

### 查看钱包余额

```bash
clawdex balances --json
```

返回一个包含`{ token, symbol, mint, balance, decimals }`对象的数组。零余额的账户也会被包含在JSON输出中。

### 获取报价（不执行交易）

```bash
clawdex quote --in SOL --out USDC --amount 0.01 --json
```

仅用于查看价格信息，无需模拟交易或使用钱包。

### 模拟交易（预测试）

```bash
clawdex swap --in SOL --out USDC --amount 0.01 --simulate-only --json
```

在链上执行完整的模拟交易，但不会广播交易信息。执行此命令时无需使用`--yes`参数。可用于预览交易金额和交易路径。

### 执行交易

```bash
clawdex swap --in SOL --out USDC --amount 0.01 --yes --json
```

**执行非交互式交易时必须使用`--yes`参数**。如果不使用此参数，ClawDex将以代码1退出。

### 健康检查

```bash
clawdex status --json
```

验证RPC连接是否正常、钱包是否有效以及配置是否正确。

## 交易流程

请始终按照以下顺序操作：

1. **健康检查**：`clawdex status --json` — 如果`rpc.healthy`的值为false，则中止操作。
2. **查看余额**：`clawdex balances --json` — 确认有足够的资金。
3. **模拟交易**：`clawdex swap --simulate-only --json` — 预览交易结果。
4. **执行交易**：`clawdex swap --yes --json` — 仅在模拟结果正常的情况下执行交易。
5. **验证交易结果**：`clawdex balances --json` — 确认余额是否更新（在公共RPC请求中可能需要等待几秒钟）。

## 代币规范

代币可以通过符号或发行地址来指定：
- **按符号指定**：`SOL`、`USDC`、`USDT`
- **按发行地址指定**：`EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v`

## 退出代码

| 代码 | 含义 | 代理操作 |
|------|---------|-------------|
| 0 | 成功 | 继续执行 |
| 1 | 一般错误 | 查看错误信息 |
| 2 | 配置错误 | 运行初始化脚本 |
| 3 | 违反安全规则 | 减少交易金额或调整交易限额 |
| 4 | 模拟失败 | 尝试其他代币对或交易金额 |
| 5 | 交易发送失败 | 重试交易 |

## 安全措施

设置安全防护机制以防止交易失控：
```bash
clawdex safety set max_slippage_bps=300 max_trade_sol=1 max_price_impact_bps=100
```

当安全防护机制被触发时，JSON响应中会包含一个`violations`数组，说明具体违反了哪些规则。

## 重要提示

- **始终使用`--json`参数**以获得机器可解析的输出结果。
- **执行真实交易时必须使用`--yes`参数**（模拟交易时无需此参数）。
- **除非有正当理由，否则切勿跳过模拟步骤**——请先使用`--simulate-only`进行预览。
- **将`balance`字段解析为字符串**，而不是数字，以保留小数点的精度。
- **务必检查退出代码**——非零的退出代码表示交易未成功。
- **在验证交易结果前请稍作等待**——在完成交易后，RPC请求返回的余额数据可能需要几秒钟才能更新。