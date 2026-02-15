---
name: trade
description: 在 Base 网络上交换或交易代币。当您或用户需要买卖、兑换、转换 USDC、ETH、WETH 等代币时，请使用此功能。相关操作包括：“购买 ETH”、“用 USDC 出售 ETH”、“将 USDC 转换为 ETH”以及“获取一些 ETH”等。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx awal@latest status*)", "Bash(npx awal@latest trade *)", "Bash(npx awal@latest balance*)"]
---

# 交易代币

使用 `npx awal@latest trade` 命令，可以通过 CDP Swap API 在 Base 网络上交换代币。进行交易前，您必须先完成身份验证。

## 确认钱包已初始化并完成身份验证

```bash
npx awal@latest status
```

如果钱包尚未完成身份验证，请参考 `authenticate-wallet` 技能。

## 命令语法

```bash
npx awal@latest trade <amount> <from> <to> [options]
```

## 参数

| 参数 | 描述                                                                                              |
| -------- | ---------------------------------------------------------------------- |
| `amount` | 要交换的代币数量（详见下面的数量格式）                              |
| `from`   | 来源代币：别名（usdc、eth、weth）或合约地址（0x...）      |
| `to`     | 目标代币：别名（usdc、eth、weth）或合约地址（0x...）         |

## 数量格式

数量可以以下几种格式指定：

| 格式        | 示例                | 描述                            |
| ------------- | ---------------------- | -------------------------------------- |
| 带美元前缀的字符串 | `'$1.00'`, `'$0.50'`  | 使用美元符号表示的金额（小数位数取决于代币） |
| 小数形式     | `1.0`, `0.50`, `0.001` | 以小数点表示的金额，便于人类阅读       |
| 整数形式     | `5`, `100`             | 被解释为整数单位的代币数量             |
| 原子单位形式   | `500000`               | 大整数被视为原子单位                   |

**自动检测**：没有小数点的大整数会被视为原子单位。例如，`500000`（USDC，6位小数）等于 $0.50。

**小数位数**：对于已知的代币（usdc=6, eth=18, weth=18），小数位数是固定的；对于任意合约地址，小数位数会从代币合约中读取。

## 选项

| 选项             | 描述                                       |
| ---------------- | -------------------------------------------- |
| `-c, --chain <name>` | 区块链网络（默认：base）                           |
| `-s, --slippage <n>` | 交易滑点容忍度（100 = 1%）                         |
| `--json`         | 将结果输出为 JSON 格式                             |

## 代币别名

| 别名    | 代币    | 小数位数 | 地址                                      |
| -------- | -------- | -------- | ------------------------------------------ |
| usdc   | USDC   | 6        | 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913             |
| eth    | ETH    | 18       | 0xEeeeeEeeeEeEeeEeEeEeeEEEeeeeEeeeeeeeeEEeE         |
| weth   | WETH   | 18       | 0x4200000000000000000000000000000000000006           |

**重要提示**：使用 `$` 标记的金额时必须使用单引号，以防止 bash 变量扩展（例如：`'$1.00'`，而不是 `$1.00`）。

## 示例

```bash
# Swap $1 USDC for ETH (dollar prefix — note the single quotes)
npx awal@latest trade '$1' usdc eth

# Swap 0.50 USDC for ETH (decimal format)
npx awal@latest trade 0.50 usdc eth

# Swap 500000 atomic units of USDC for ETH
npx awal@latest trade 500000 usdc eth

# Swap 0.01 ETH for USDC
npx awal@latest trade 0.01 eth usdc

# Swap with custom slippage (2%)
npx awal@latest trade '$5' usdc eth --slippage 200

# Swap using contract addresses (decimals read from chain)
npx awal@latest trade 100 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 0x4200000000000000000000000000000000000006

# Get JSON output
npx awal@latest trade '$1' usdc eth --json
```

## 先决条件

- 必须完成身份验证（可以通过 `awal status` 命令查看状态） |
- 钱包中必须有足够的来源代币余额

## 错误处理

常见错误：

- “未授权” - 请先运行 `awal auth login <email>` 进行身份验证 |
- “无效的代币别名” - 请使用有效的别名（usdc、eth、weth）或合约地址（0x...） |
- “无法将代币交换给自己” - 来源代币和目标代币必须不同 |
- “交换失败：TRANSFER_FROM_FAILED” - 余额不足或审批问题 |
- “无流动性” - 请尝试减少交易金额或更换代币对 |
- “输入的金额小数位数与代币支持的小数位数不匹配” - 输入的小数位数超出代币的限制