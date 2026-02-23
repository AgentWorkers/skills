---
name: boltzpay
description: 自动支付 API 数据费用——支持多种协议（x402 + L402）及多链网络
metadata: {"openclaw": {"emoji": "\u26a1", "requires": {"bins": ["npx"]}, "install": [{"id": "boltzpay-cli", "kind": "node", "label": "BoltzPay CLI"}]}}
---
# BoltzPay — 为AI代理提供付费API访问服务

BoltzPay允许AI代理自动支付API数据的使用费用。它支持多种支付协议（x402和L402）以及多种区块链（Base和Solana），支持使用USDC或Bitcoin Lightning进行支付。代理可以在一个工作流程中发现、评估并购买API数据。

## 快速入门

从付费API端点获取数据：

```
npx @boltzpay/cli fetch https://invy.bot/api
```

## 命令

| 命令 | 描述 | 所需凭据 |
|---------|-------------|--------------------|
| `npx @boltzpay/cli fetch <url>` | 获取API数据并支付费用 | 需要凭据 |
| `npx @boltzpay/cli check <url>` | 检查URL是否需要支付 | 不需要凭据 |
| `npx @boltzpay/cli quote <url>` | 获取价格报价 | 不需要凭据 |
| `npx @boltzpay/cli discover` | 浏览兼容的API | 不需要凭据 |
| `npx @boltzpay/cli budget` | 检查支出预算 | 不需要凭据 |
| `npx @boltzpay/cli history` | 查看支付历史 | 不需要凭据 |
| `npx @boltzpay/cli wallet` | 查看钱包地址和余额 | 不需要凭据 |
| `npx @boltzpay/cli demo` | 交互式演示 | 不需要凭据 |

## 设置

为了使用付费API功能，请设置以下环境变量：

- `COINBASE_API_KEY_ID` — 您的Coinbase CDP API密钥ID |
- `COINBASE_API_KEY_SECRET` — 您的Coinbase CDP API密钥密钥 |
- `COINBASE_WALLET_SECRET` — 您的Coinbase CDP钱包密钥 |
- `BOLTZPAY_DAILY_BUDGET` — 每日支出限额（以USD为单位，可选，默认：无限制）

您可以在[portal.cdp.coinbase.com](https://portal.cdp.coinbase.com)获取您的Coinbase CDP密钥。

## 示例

### 1. 发现可用的API

```
npx @boltzpay/cli discover
```

浏览与BoltzPay兼容的付费API目录。无需任何凭据。

### 2. 支付前查看价格

```
npx @boltzpay/cli check https://invy.bot/api
```

在不支付任何费用的情况下查看支付协议、金额和区块链选项。

### 3. 获取付费数据

```
npx @boltzpay/cli fetch https://invy.bot/api
```

自动检测支付协议，使用USDC支付，并返回API响应。

## 不需要凭据？

八个命令中有七个可以在不提供Coinbase凭据的情况下使用：

- `check` — 检查URL是否需要支付 |
- `quote` — 获取详细价格信息 |
- `discover` — 浏览API目录 |
- `budget` — 检查支出限额 |
- `history` — 查看过去的交易记录 |
- `wallet` — 查看钱包地址和余额 |
- `demo` — 交互式演示 |

只有`fetch`命令需要凭据（因为它会实际执行支付操作）。

## 链接

- [GitHub](https://github.com/leventilo/boltzpay) |
- [npm](https://www.npmjs.com/package/@boltzpay/sdk) |
- [文档](https://boltzpay.ai)