---
name: fund
description: 向钱包中添加资金。当您或用户需要充值、补充资金、购买 USDC、进行资金转移，或者当钱包余额不足而无法完成发送或交易操作时，都可以使用这笔资金。此外，当有人询问“如何获取 USDC？”时，也可以参考此操作。
user-invocable: true
disable-model-invocation: false
allowed-tools: ["Bash(npx awal@latest status*)", "Bash(npx awal@latest show*)", "Bash(npx awal@latest address*)", "Bash(npx awal@latest balance*)"]
---

# 为钱包充值

请使用钱包配套应用程序，通过 Coinbase Onramp 用 USDC 为钱包充值。该功能支持多种支付方式，包括 Apple Pay、借记卡、银行转账以及从 Coinbase 账户转账。

## 确认钱包已初始化并完成身份验证

```bash
npx awal@latest status
```

如果钱包尚未完成身份验证，请参考 `authenticate-wallet` 技能。

## 打开充值界面

```bash
npx awal@latest show
```

这将打开钱包配套窗口，在该窗口中用户可以：

1. 选择预设的金额（$10、$20、$50）或输入自定义金额
2. 选择他们偏好的支付方式
3. 通过 Coinbase Pay 完成支付

## 支付方式

| 支付方式 | 说明                                        |
| --------- | ---------------------------------------------- |
| Apple Pay | 使用 Apple Pay 快速完成支付（如支持）         |
| Coinbase | 从现有的 Coinbase 账户转账                   |
| 卡片       | 使用借记卡支付                         |
| 银行       | 通过 ACH 银行转账                         |

## 替代方案

您也可以请求他人将 USDC 通过 Base 平台发送到您的钱包地址。您可以通过运行以下命令来获取您的钱包地址：

```bash
npx awal@latest address
```

## 先决条件

- 必须完成身份验证（使用 `npx awal@latest status` 命令检查）
- 所在地区必须支持 Coinbase Onramp（例如美国等）

## 充值流程

1. 运行 `npx awal@latest show` 命令以打开钱包用户界面
2. 指导用户点击“充值”按钮
3. 用户在用户界面中选择金额和支付方式
4. 用户通过 Coinbase Pay 完成支付（支付将在浏览器中打开）
5. 支付确认后，USDC 将被存入钱包

## 充值后查看余额

```bash
# Check updated balance
npx awal@latest balance
```

## 注意事项

- 充值过程通过 Coinbase 的受监管渠道进行
- 处理时间因支付方式而异（卡片/Apple Pay 为即时完成，银行转账为 1-3 天）
- 资金将以 USDC 的形式存入 Base 网络
- 如果无法通过上述方式充值，用户也可以直接将 USDC 通过 Base 平台发送到钱包地址