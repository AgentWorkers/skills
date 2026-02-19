---
name: monolith
description: 专为AI代理设计的加密钱包：采用硬件隔离的密钥存储技术（Apple Secure Enclave），支持ERC-4337标准智能合约，具备链上消费限额功能，并内置默认的拒绝访问策略引擎（default-deny policy engine）。
homepage: https://github.com/slaviquee/monolith
source: https://github.com/slaviquee/monolith/tree/main/skill
metadata: {"openclaw":{"displayName":"Monolith","source":"https://github.com/slaviquee/monolith/tree/main/skill","homepage":"https://github.com/slaviquee/monolith","requires":{"bins":["MonolithDaemon"]},"install":[{"id":"daemon-pkg","kind":"download","label":"Install Monolith Daemon (macOS pkg)","url":"https://github.com/slaviquee/monolith/releases/download/v0.1.2/MonolithDaemon-v0.1.2.pkg","os":"darwin"},{"id":"companion-zip","kind":"download","label":"Download Monolith Companion (macOS app zip)","url":"https://github.com/slaviquee/monolith/releases/download/v0.1.2/MonolithCompanion.app.zip","os":"darwin"}]},"clawdbot":{"displayName":"Monolith","source":"https://github.com/slaviquee/monolith/tree/main/skill","homepage":"https://github.com/slaviquee/monolith","requires":{"bins":["MonolithDaemon"]},"install":[{"id":"daemon-pkg","kind":"download","label":"Install Monolith Daemon (macOS pkg)","url":"https://github.com/slaviquee/monolith/releases/download/v0.1.2/MonolithDaemon-v0.1.2.pkg","os":"darwin"},{"id":"companion-zip","kind":"download","label":"Download Monolith Companion (macOS app zip)","url":"https://github.com/slaviquee/monolith/releases/download/v0.1.2/MonolithCompanion.app.zip","os":"darwin"}]}}
---
# Monolith — 加密钱包技能

这是一个专为 OpenClaw 代理设计的安全加密钱包。Monolith 结合了硬件隔离的密钥（Apple Secure Enclave）、链上交易控制以及基于策略的审批机制，确保代理可以在不暴露私钥的情况下安全地进行交易。

## 命令

| 命令 | 功能 | 是否需要守护进程？ |
|---------|-------------|------------------|
| `send <接收地址> <金额> [代币] [链ID]` | 向指定地址发送 ETH 或 USDC | 是 |
| `swap <ETH 金额> [输出代币] [链ID]` | 通过 Uniswap 将 ETH 交换为其他代币 | 是 |
| `balance <地址> [链ID]` | 查看 ETH 和稳定币的余额 | 否（仅读） |
| `capabilities` | 显示当前的限额、预算和 gas 状态 | 是 |
| `decode <目标> <输入数据> <值>` | 将交易意图解码为人类可读的摘要 | 是 |
| `panic` | 紧急冻结——立即生效，无需 Touch ID | 是 |
| `status` | 检查守护进程的健康状况和钱包信息 | 是 |
| `identity [查询\|注册]` | 执行 ERC-8004 身份相关操作 | 部分支持 |
| `setup` | 运行设置向导，显示钱包状态和配置 | 是 |
| `policy` | 查看当前的支出策略 | 是 |
| `policy update '<json>'` | 更新支出策略（需要 Touch ID） | 是 |
| `allowlist <添加\|删除> <地址> [标签>` | 将地址添加或从允许列表中删除（需要 Touch ID） | 是 |
| `audit-log` | 查看守护进程的审计日志 | 是 |

## 安全模型

- 该技能本身是不可信的（即它不会自行修改任何交易参数）。它仅负责构建交易意图（包括目标地址、输入数据和交易金额）。
- 该技能绝不会设置交易中的随机数（nonce）、gas 费用、链ID、交易费用或签名信息。
- 所有交易操作都由本地的 macOS 进程（即签名守护进程）根据预设的策略来执行。
- 在策略允许的范围内，交易会自动执行。
- 超出限制或使用未知输入数据的交易需要用户通过 8 位验证码进行手动批准。
- 任何代币相关的操作（如 `approve`、`permit` 等）都必须获得明确的批准。

## 需要批准的情况：

- 超过单次交易或每日交易额度的转账
- 向未列入允许列表的地址转账
- 任何代币相关的操作（如 `approve`、`permit` 等）
- 使用未知的输入数据（默认为拒绝策略）
- 超过滑点限制的交换操作

## 自动执行的功能：

- 在允许列表内的地址之间进行 ETH 和 USDC 的转账（在限额范围内）
- 在允许列表内的去中心化交易所（如 Uniswap）中进行交易（在滑点限制范围内）
- 在允许列表内的去中心化金融（DeFi）平台上进行存款/取款操作
- 查看余额、查询状态以及解码交易数据

## 设置步骤：

1. 从 ClawHub 安装 Monolith（macOS 安装包中包含守护进程及相关辅助工具）。
2. 运行 `monolith setup` 命令以验证钱包状态；如果守护进程或辅助工具未运行，系统会提示手动启动命令。
3. 如果设置过程中提示缺少组件，请从发布资源中安装 `MonolithDaemon.pkg` 和 `MonolithCompanion.app`。
4. 用 ETH 向钱包地址充值。
5. 开始进行交易。

## 错误处理：

- 如果守护进程未运行，所有签名相关命令都会失败，并显示明确的错误信息。
- 如果 gas 费用不足，守护进程会拒绝交易——请为钱包补充 ETH。
- 如果钱包被冻结，在解冻之前无法进行任何出站交易（需要使用 Touch ID 并等待 10 分钟）。
- 如果受到 Pimlico 的速率限制，守护进程会自动采用指数退避策略（即逐渐增加请求频率）。

## 审批流程：

当交易超出策略限制或使用未知的输入数据时，守护进程会返回 HTTP 202 状态码，并附带原因、交易摘要和失效时间。代理应：

1. 向用户展示审批原因和摘要。
2. 请求用户输入 8 位验证码（该验证码会通过守护进程的 macOS 对话框显示）。
3. 使用相同的交易意图以及 `approvalCode` 参数重新调用 `/sign` 命令以完成交易。

**注意：** 不需要单独的审批脚本——只需在调用 `send` 或 `swap` 命令时传递审批代码即可。

## 支持的链：

- Ethereum 主网（链ID 1）
- Base（链ID 8453）