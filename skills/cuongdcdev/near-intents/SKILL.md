---
name: near-intents
description: 使用 NEAR Intents 1Click SDK 的 OpenClaw 兼容跨链交换与桥接功能。支持包括 NEAR、Base、Ethereum、Solana 和 Bitcoin 在内的 14 种以上区块链。
---
# NEAR Intents 技能 — 1Click SDK

## 📋 简介

**功能**：一个通用的跨链交换和桥接工具，基于 [1Click API](https://docs.near-intents.org/near-intents/integration/distribution-channels/1click-api) 和 [`@defuse-protocol/one-click-sdk-typescript`](https://github.com/defuse-protocol/one-click-sdk-typescript) SDK 开发。

**支持的链**：NEAR、Base、Ethereum、Arbitrum、Solana、BSC、Gnosis、Starknet、Bitcoin、Dogecoin、Zcash、Litecoin。

**工作原理**：
1. 通过 1Click API 获取报价 → 收到充值地址
2. 将代币发送到源链的充值地址
3. 1Click 自动完成交换/桥接操作
4. 代币会到达目标链的接收地址

**关键信息**：
- 每次交换的最低费用约为 0.10 美元
- 仅当源资产位于 NEAR 上时，需要 NEAR 账户
- 从其他链进行跨链交换（例如，Arb USDC → Sol USDC）时不需要 NEAR 账户
- JWT 认证是可选的，但可以避免 0.2% 的费用 → 请在 [partners.near-intents.org](https://partners.near-intents.org/) 注册

---

## 核心概念

所有交换操作都通过 **1Click API**（`https://1click.chaindefuser.com`）完成：

**无需直接与 `intents.near` 交互**——1Click API 负责处理所有细节。

---

## `executeIntent()` API

`index.ts` 导出的唯一入口点：

### 参数

| 参数       | 类型     | 是否必填 | 说明            |
|------------|---------|----------|-------------------|
| `assetIn`    | string   | ✅     | 源资产符号（例如，`NEAR`、`base:USDC`、`arb:ARB`） |
| `assetOut`   | string   | ✅     | 目标资产符号           |
| `amount`     | string   | ✅     | 人类可读的金额（例如，`1.0`、`0.5`）   |
| `recipient`  | string   | ❌      | 目标地址（跨链交换时需要）。默认为 NEAR 账户 |
| `refundAddress` | string   | ⚠️     | **必填（对于非 NEAR 源资产）**。交换失败时，资金将退还到此地址。**对资金安全至关重要！** |
| `mode`      | string   | ❌      | `auto`：自动从 NEAR 账户充值；`manual`：返回报价和充值地址供用户手动操作 |
| `swapType`    | string   | ❌      | `EXACT_INPUT`（金额等于输入）；`EXACT_OUTPUT`（金额等于期望的输出） |

### ⚠️ 重要提示：退款地址的安全性

**当 `assetIn` 位于非 NEAR 链上时（例如，`base:USDC`、`arb:ARB`、`btc:BTC`）：**

1. **必须提供 `refundAddress`** — 否则函数会抛出错误
2. **务必询问用户** 源链上的钱包地址
3. **切勿猜测** — 使用错误的地址会导致资金永久丢失
4. **向用户说明**：“如果交换失败，您的代币将退还到此地址”

**示例**：

**为什么这很重要**：
- 交换可能因市场条件、流动性问题或时间因素而失败
- 失败的交换会自动将资金退还到 **源链** 的 `refundAddress`
- 如果 `refundAddress` 错误或属于其他人，**资金将永久丢失**

### 返回结果

- **自动模式**：`交换成功！1.0 NEAR → 0.97 USDC\n交易链接：https://nearblocks.io/txns/...\n浏览器链接：https://explorer.near-intents.org/transactions/...`
- **手动模式**：提供包含充值地址、金额、跟踪链接和截止时间的详细说明

---

## 资产命名规则

使用 `chain:SYMBOL` 格式。NEAR 原生代币省略链前缀。

| 链       | 前缀     | 示例                          |
|-----------|------------|-----------------------------------|
| NEAR      | *(无)*   | `NEAR`、`USDC`、`USDT`、`wNEAR`  |
| Base      | `base:`    | `base:USDC`                       |
| Ethereum  | `eth:`     | `eth:ETH`、`eth:USDC`             |
| Arbitrum  | `arb:`     | `arb:USDC`、`arb:ARB`             |
| Solana    | `sol:`     | `sol:SOL`、`sol:USDC`             |
| BSC       | `bsc:`     | `bsc:USDC`                        |
| Bitcoin   | `btc:`     | `btc:BTC` （仅限原生代币）         |
| Dogecoin  | `doge:`    | `doge:DOGE` （仅限原生代币）       |
| Zcash     | `zec:`     | `zec:ZEC` （仅限原生代币）         |
| Litecoin  | `ltc:`     | `ltc:LTC` （仅限原生代币）         |

- **大小写不敏感**：`near`、`NEAR`、`Near` 都有效
- **UTXO 链（BTC、DOGE、ZEC、LTC）**：**仅支持原生代币** — 不支持包装/ERC-20 格式的代币

---

## 模式

### 自动模式（默认）
自动从配置的 NEAR 账户进行充值。

**适用场景**：源资产位于 NEAR 上，并且代理在 `.env` 文件中配置了 NEAR 凭据。

### 手动模式
返回包含充值地址的报价——用户（或代理）需要手动发送代币。

**适用场景**：源资产位于非 NEAR 链上，或者您希望先向用户显示报价。

### EXACT_OUTPUT
指定期望的输出金额；1Click API 会告诉您需要发送多少代币。

---

## 示例

### 1. 在 Base 链上将 NEAR 交换为 USDC（自动模式）
### 2. 从 Arbitrum 链将 USDC 桥接到 Solana 链（手动模式）
### 3. 在同一链上将 NEAR 交换为 USDC
### 4. 获取报价：在 Arbitrum 链上，10 USDC 需要多少 NEAR？
### 5. 将 BTC 发送到 NEAR 地址

---

## 配置

### `.env` 文件（仅适用于源资产为 NEAR 的自动模式）：

- `ONE_CLICK_JWT`：在 [partners.near-intents.org](https://partners.near-intents.org/) 注册以避免 0.2% 的费用。
- 如果仅使用手动模式进行非 NEAR 链的交换，则可以完全忽略 `.env` 文件。

**注意**：**切勿将 `.env` 文件提交到版本控制系统中！**

---

## 1Click SDK 的内部工作流程

### 交换状态
| 状态              | 含义                |
|---------------------|-------------------------|
| `PENDING_DEPOSIT`   | 等待充值              |
| `PROCESSING`        | 接收到充值请求，市场做市商正在执行     |
| `SUCCESS`           | 代币已发送给接收者           |
| `INCOMPLETE_DEPOSIT` | 充值金额低于要求          |
| `REFUNDED`          | 交换失败，代币已退还至退款地址     |
| `FAILED`            | 交换失败（由于错误）           |

## 内置的代币映射

代码中包含了一个静态的 `TOKEN_MAP`，用于常见代币：

| 关键字          | 资产 ID (NEP-141)            | 小数位数       |
|--------------|---------------------------------|-------------------------|
| `NEAR`       | `nep141:wrap.near`            | 24               |
| `USDC`       | `nep141:17208628f84f5d6ad33f0da3bbbeb27ffcb398eac501a31bd6ad2011e36133a1` | 6                    |
| `USDT`       | `nep141:usdt.tether-token.near`        | 6                    |
| `base:USDC`  | `nep141:base-0x833589fcd6edb6e08f4c7c32d4f71b54bda02913.omft.near` | 6                    |
| `arb:USDC`   | `nep141:arb-0xaf88d065e77c8cc2239327c5edb3a432268e5831.omft.near` | 6                    |
| `arb:ARB`    | `nep141:arb-0x912ce59144191c1204e64559fe8253a0e49e6548.omft.near` | 18                    |
| `eth:ETH`    | `nep141:eth.omft.near`            | 18                    |
| `eth:USDC`   | `nep141:eth-0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48.omft.near` | 6                    |
| `sol:SOL`    | `nep141:sol.omft.near`            | 9                    |
| `sol:USDC`   | `nep141:sol-5ce3bf3a31af18be40ba30f721101b4341690186.omft.near` | 6                    |

要添加更多代币，请使用 `OneClickService.getTokens()` 或查看 `TOKENS.md`。

---

## 小数位数参考

| 代币       | 小数位数 | “1.0”对应的最小单位         |
|------------|-----------------|-------------------------|
| NEAR       | 24               | `1000000000000000000000000`         |
| USDC       | 6                    | `1000000`                |
| USDT       | 6                    | `1000000`                |
| ETH       | 18                    | `100000000000000000`         |
| SOL       | 9                    | `1000000000`               |
| BTC       | 8                    | `100000000`               |

`index.ts` 使用 `decimal.js` 自动处理小数转换。

---

## 跟踪与查询

- **NEAR 交易**：`https://nearblocks.io/txns/<txHash>`
- **1Click 交换状态**：`https://explorer.near-intents.org/transactions/<depositAddress>`

---

## 故障排除

| 错误         | 解决方案                |
|------------|-------------------------|
| `Token not found: X` | 检查代币符号和链前缀。参考 `TOKEN_MAP` 或 `TOKENS.md` |
| `No deposit address in quote response` | 解决器无法匹配资产对或金额。尝试其他金额或资产对 |
| `NEAR_ACCOUNT_ID` 和 `NEAR_PRIVATE_KEY` 必须设置 | 配置 `.env` 文件或使用 `mode: 'manual'` |
| `Swap failed with status: REFUNDED` | 代币已退还至退款地址。请尝试其他金额 |
| `Status polling timed out` | 手动检查浏览器链接。交换可能仍会完成 |
| 401 认证错误     | JWT 无效或已过期。请在 partners.near-intents.org 注册 |

---

## 依赖项

---

## 文件概述

| 文件        | 用途                    |
|------------|-------------------------|
| `index.ts`     | 主入口文件 — 导出 `executeIntent()`       |
| `lib-1click/`    | 1Click SDK 的示例代码（获取代币、获取报价、发送充值等） |
| `SKILL.md`     | 本文件 — AI 代理的主要参考文档     |
| `AI-AGENT-GUIDE.md` | 代理工作流程的详细指南       |
| `TOKENS.md`     | 完整的代币信息（包括小数位数和资产 ID）   |
| `manifest.json` | OpenClaw 的技能配置文件         |
| `README.md`     | 项目文档                 |
| `USAGE_GUIDE.md` | 使用指南和故障排除方法           |

---

## 版本

**v2.0.0** — 基于 [1Click SDK](https://github.com/defuse-protocol/one-click-sdk-typescript) 和 [NEAR Intents](https://docs.near-intents.org) 开发

## 许可证

MIT