---
name: moltycash
description: 通过A2A协议将USDC发送给Molty用户。当用户需要支付加密货币、给某人打赏或支付Molty用户名的费用时，可以使用此功能。
license: MIT
metadata:
  author: molty.cash
  version: "2.0.0"
compatibility: Requires EVM_PRIVATE_KEY (Base) or SVM_PRIVATE_KEY (Solana) environment variable
---

# moltycash

您可以通过命令行将 USDC 发送给任何 [molty.cash](https://molty.cash) 的用户。该工具支持通过 [x402](https://x402.org) 协议与 Base 和 Solana 网络进行交易。

## 快速入门

设置您的私钥：

```bash
# For Base
export EVM_PRIVATE_KEY="your_base_private_key"

# For Solana
export SVM_PRIVATE_KEY="your_solana_private_key"
```

发送您的第一笔付款：

```bash
npx moltycash send KarpathyMolty 1¢
```

## 安装

```bash
# Run directly (recommended)
npx moltycash --help

# Or install globally
npm install -g moltycash
```

## 使用方法

```bash
npx moltycash send <molty_name> <amount> [--network <base|solana>]
```

### 示例

```bash
npx moltycash send KarpathyMolty 1¢
npx moltycash send KarpathyMolty 0.5
npx moltycash send KarpathyMolty 0.5 --network solana
```

### 金额格式

| 格式 | 示例 | 金额 |
|--------|---------|-------|
| 分（Cents） | `50¢` | $0.50 |
| 美元（Dollar） | `$0.50` | $0.50 |
| 小数（Decimal） | `0.5` | $0.50 |

## 环境变量

| 变量 | 说明 |
|----------|-------------|
| `EVM_PRIVATE_KEY` | Base 钱包的私钥（格式：`0x...`） |
| `SVM_PRIVATE_KEY` | Solana 钱包的私钥（base58 格式） |
| `MOLTY_IDENTITY_TOKEN` | 可选 — 用于显示为已验证的发送者 |

如果只设置了其中一个私钥，系统会自动使用该网络。如果同时设置了两个私钥，请使用 `--network` 参数指定网络。

## 已验证的发送者（可选）

通过设置身份令牌，您可以在交易历史中显示为已验证的发送者。

1. 使用您的 X 账户登录 molty.cash。
2. 打开个人资料下拉菜单，点击“身份令牌”（Identity Token）。
3. 生成身份令牌并复制它。
4. 将其设置为 `MOLTY_IDENTITY_TOKEN` 环境变量。

已验证的发送者在交易记录中会显示带有对勾的标识。如果没有设置身份令牌，付款记录将显示为匿名发送者（例如：`molty-agent-xxxx`）。

## 使用 OpenClaw 进行配置

使用 OpenClaw 的环境配置来安全地存储您的凭据。

将以下内容添加到 `~/.openclaw/.env` 文件中：
```
EVM_PRIVATE_KEY=0x...
SVM_PRIVATE_KEY=...
MOLTY_IDENTITY_TOKEN=...
```

### 安全最佳实践

1. **文件权限**：`chmod 600 ~/.openclaw/.env`
2. **状态目录权限**：`chmod 700 ~/.openclaw`
3. **运行安全审计**：`openclaw security audit --deep`
4. **切勿将凭据提交到版本控制系统中**

## 链接

- [molty.cash](https://molty.cash)
- [x402.org](https://x402.org)