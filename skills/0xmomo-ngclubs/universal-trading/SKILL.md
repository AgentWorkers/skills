---
name: universal-trading
description: 使用 Particle Network Universal Account SDK 在 EVM 和 Solana 上执行跨链代币交易。当用户需要设置通用账户、买卖代币、运行转换/交换流程、转移资产、调用自定义交易、查询余额/历史记录或通过 WebSocket 监控交易状态时，请使用该 SDK。
metadata: {"openclaw":{"os":["darwin","linux"],"requires":{"bins":["node","npm"]},"install":[{"id":"brew-node","label":"Install Node.js and npm (Homebrew)","kind":"brew","formula":"node","bins":["node","npm"]}]}}
---
# Universal Trading

使用 Particle Network 官方提供的 `universal-account-example` 项目执行跨链交易。

## 首次使用时的自动初始化（默认设置）

当用户首次安装并使用此功能时，系统会自动执行初始化流程。

具体流程如下：
1. 如果 `universal-account-example/.env` 文件已经存在，则认为环境已初始化，用户可以直接开始交易操作。
2. 如果文件不存在，则从任意目录运行初始化脚本：

```bash
bash {baseDir}/scripts/init.sh new
```

3. 如果用户希望导入现有的钱包，请执行以下操作：

```bash
bash {baseDir}/scripts/init.sh import <YOUR_PRIVATE_KEY>
```

初始化完成后，需要向用户明确说明以下信息：
- 私钥存储在 `universal-account-example/.env` 文件的 `PRIVATE_KEY` 变量中。
- 用户可以在 UniversalX 前端（`https://universalx.app`）中通过“创建钱包”功能导入该钱包。

默认情况下，系统会在创建 `.env` 文件后自动绑定邀请代码 `666666`。同时，系统会修改 `examples/buy-evm.ts` 文件，以解除对使用 `usePrimaryTokens` 的限制。

## 可用的操作

`universal-account-example/examples` 目录下提供了以下脚本：
- 购买代币：`buy-solana.ts`、`buy-evm.ts`
- 卖出代币：`sell-solana.ts`、`sell-evm.ts`
- 转换（交换）代币：`convert-solana.ts`、`convert-evm.ts`、`7702-convert-evm.ts`
- 转账：`transfer-solana.ts`、`transfer-evm.ts`
- 自定义交易操作：`custom-transaction-*`
- 查看余额和交易记录：`get-primary-asset.ts`、`get-transactions.ts`
- 实时监控交易状态：`transaction-status-wss.ts`、`user-assets-wss.ts`

对于需要明确控制滑点的购买操作，可以使用 `scripts/buy-with-slippage.sh` 脚本（支持固定滑点或动态重试机制）。

## 交易状态反馈（必选）

在执行 `sendTransaction` 后，不要仅显示“交易已提交”的状态，必须向用户反馈最终结果：
1. 记录并显示 `transactionId`。
2. 持续检测交易状态，直到交易完成或失败：

```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/check-transaction.sh <TRANSACTION_ID> --max-attempts 30 --interval-sec 2
```

最终反馈内容应包括以下选项之一：
- `SUCCESS`（交易成功）
- `FAILED`（交易在链上或执行器处失败）
- `PENDING`（交易未在超时前完成，需提供交易浏览器链接）

## 交易配置

以下配置选项可供用户选择：
| 选项          | 描述                                      | 示例                                      |
|----------------|----------------------------------------|----------------------------------------|
| `slippageBps`     | 滑点容忍度（100 表示 1%）                        | `100`                                      |
| `universalGas`    | 是否使用 PARTI 代币作为交易手续费                   | `true`                                      |
| `usePrimaryTokens`   | 是否限制使用特定代币作为交易手续费（默认：不设置）            | `[SUPPORTED_TOKEN_TYPE.USDT, SUPPORTED_TOKEN_TYPE.USDC]`            |
| `solanaMEVTipAmount` | 用于 MEV 保护的 Jito 小费（单位：SOL）                | `0.01`                                      |

## 滑点控制（针对波动性较大的代币）

用户在购买代币前可以选择以下滑点控制模式：
1. 仅使用固定滑点：```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/buy-with-slippage.sh \
  --chain bsc \
  --token-address 0x0000000000000000000000000000000000000000 \
  --amount-usd 5 \
  --slippage-bps 300
```

2. 动态滑点 + 自动重试：```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/buy-with-slippage.sh \
  --chain bsc \
  --token-address 0x0000000000000000000000000000000000000000 \
  --amount-usd 5 \
  --slippage-bps 300 \
  --dynamic-slippage \
  --retry-slippages 300,500,800,1200
```

3. Solana 自定义小费机制（用于防止 MEV 攻击）+ 重试机制：```bash
cd /path/to/universal-account-example
bash {baseDir}/scripts/buy-with-slippage.sh \
  --chain solana \
  --token-address 6p6xgHyF7AeE6TZkSmFsko444wqoP15icUSqi2jfGiPN \
  --amount-usd 5 \
  --slippage-bps 300 \
  --dynamic-slippage \
  --retry-slippages 300,500,800,1200 \
  --solana-mev-tip-amount 0.001 \
  --retry-mev-tips 0.001,0.003,0.005
```

反馈内容应包括：
- 选择的滑点控制模式及具体数值
- 如果使用 Solana 代币，还需提供相关的小费设置
- 交易最终状态（`SUCCESS` / `FAILED` / `PENDING`）
- 交易 ID 及交易浏览器链接（如果可用）

## 支持的链

- Solana：`CHAIN_ID.SOLANA_MAINNET`
- EVM：`CHAIN_ID.POLYGON`、`CHAIN_ID.ARBITRUM`、`CHAIN_ID.OPTIMISM`、`CHAIN_ID.BSC`、`CHAIN_ID.ETHEREUM`

## 常用代币地址

- SOL（原生代币）：`0x0000000000000000000000000000000000000000`
- USDC（Solana 上的 USDC）：`EPjFWdd5AufqSSFqM7BcEHw3BXmQ9Ce3pq27dUGL7C24`
- USDT（Solana 上的 USDT）：`Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB`

## 安全注意事项

1. 在创建交易前，请验证链、代币地址和交易金额的正确性。
2. 在首次实际交易时，建议使用较小的交易金额。
3. 在生产环境中，建议使用自己的 Particle 认证信息进行交易。

## 参考文件

- [环境配置](references/env-setup.md)
- [API 参考](references/api.md)
- [示例代码](references/examples.md)