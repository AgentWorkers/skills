---
name: send-usdc
description: 将 USDC 发送到以太坊地址或 ENS 名称。当您或用户需要汇款、支付款项、转账 USDC、给予小费、进行捐赠，或者向钱包地址或 .eth 名称发送资金时，可以使用此功能。相关表达包括：“向 0x... 发送 5 美元”、“支付给 vitalik.eth” 等。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx awal@latest status*)", "Bash(npx awal@latest send *)", "Bash(npx awal@latest balance*)"]
---

# 发送 USDC

使用 `npx awal@latest send` 命令将 USDC 从钱包转移到 Base 平台上的任何以太坊地址或 ENS 名称。

## 确认钱包已初始化并完成身份验证

```bash
npx awal@latest status
```

如果钱包尚未完成身份验证，请参考 `authenticate-wallet` 技能。

## 命令语法

```bash
npx awal@latest send <amount> <recipient> [--chain <chain>] [--json]
```

## 参数

| 参数          | 描述                                                                                                                         |
| -------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `amount`       | 要发送的金额：`$1.00`、`1.00` 或原子单位（1000000 = $1`）。使用 `$` 对金额进行单引号括起来，以防止 bash 变量扩展。如果金额看起来像是原子单位（没有小数部分且大于 100），则视为原子单位。通常情况下，用户不会发送超过 100 USDC 的金额。 |
| `recipient`     | 以太坊地址（0x...）或 ENS 名称（例如：vitalik.eth）                                                                                         |

## 选项

| 选项            | 描述                                                                                                                         |
| ---------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `--chain <name>`    | 区块链网络（默认：base）                                                                                                      |
| `--json`        | 将输出结果以 JSON 格式显示                                                                                                      |

## 示例

```bash
# Send $1.00 USDC to an address
npx awal@latest send 1 0x1234...abcd

# Send $0.50 USDC to an ENS name
npx awal@latest send 0.50 vitalik.eth

# Send with dollar sign prefix (note the single quotes)
npx awal@latest send '$5.00' 0x1234...abcd

# Get JSON output
npx awal@latest send 1 vitalik.eth --json
```

## ENS 名称的解析

ENS 名称会通过以太坊主网自动解析为地址。该命令将：

1. 检测 ENS 名称（任何包含点且不是十六进制地址的字符串）；
2. 将名称解析为对应的地址；
3. 在输出中同时显示 ENS 名称和解析后的地址。

## 先决条件

- 必须完成身份验证（使用 `npx awal@latest awal status` 检查状态，使用 `npx awal@latest awal auth login` 登录；更多信息请参阅 `authenticate-wallet` 技能）；
- 钱包中必须有足够的 USDC 余额（使用 `npx awal balance` 检查余额）。

## 错误处理

- 常见错误：
  - “未完成身份验证”：请先运行 `awal auth login <email>`；
  - “余额不足”：使用 `awal balance` 检查余额；
  - “无法解析 ENS 名称”：请确认 ENS 名称是否存在；
  - “接收地址无效”：接收地址必须是有效的以太坊地址或 ENS 名称。