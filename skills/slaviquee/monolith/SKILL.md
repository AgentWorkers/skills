---
name: monolith
description: 专为AI代理设计的加密钱包：采用硬件隔离技术（Apple Secure Enclave）来保护密钥安全；支持ERC-4337标准，具备链上交易限制功能；内置默认拒绝策略引擎（default-deny policy engine）。
homepage: https://github.com/slaviquee/monolith
source: https://github.com/slaviquee/monolith/tree/main/skill
metadata: {"openclaw":{"displayName":"Monolith — Crypto Wallet","source":"https://github.com/slaviquee/monolith/tree/main/skill","homepage":"https://github.com/slaviquee/monolith","os":["darwin"],"requires":{"bins":["MonolithDaemon"]},"install":[{"id":"daemon-pkg","kind":"download","label":"Install Monolith Daemon (macOS pkg)","url":"https://github.com/slaviquee/monolith/releases/download/v0.1.5/MonolithDaemon-v0.1.5.pkg","os":["darwin"]},{"id":"companion-zip","kind":"download","label":"Download Monolith Companion (macOS app zip)","url":"https://github.com/slaviquee/monolith/releases/download/v0.1.3/MonolithCompanion.app.zip","os":["darwin"]}]},"clawdbot":{"displayName":"Monolith — Crypto Wallet","source":"https://github.com/slaviquee/monolith/tree/main/skill","homepage":"https://github.com/slaviquee/monolith","os":["darwin"],"requires":{"bins":["MonolithDaemon"]},"install":[{"id":"daemon-pkg","kind":"download","label":"Install Monolith Daemon (macOS pkg)","url":"https://github.com/slaviquee/monolith/releases/download/v0.1.5/MonolithDaemon-v0.1.5.pkg","os":["darwin"]},{"id":"companion-zip","kind":"download","label":"Download Monolith Companion (macOS app zip)","url":"https://github.com/slaviquee/monolith/releases/download/v0.1.3/MonolithCompanion.app.zip","os":["darwin"]}]}}
---
# Monolith — 加密钱包技能

Monolith 是一款专为 OpenClaw 代理设计的加密钱包工具。它结合了硬件隔离的密钥管理机制（Apple Secure Enclave）、链上交易控制功能以及基于策略的审批流程，确保代理能够在不暴露私钥的情况下安全地进行交易。

## 命令

| 命令 | 功能 | 是否需要守护进程？ |
|---------|-------------|------------------|
| `send <接收地址> <金额> [代币] [链ID]` | 向指定地址发送 ETH 或 USDC | 是 |
| `swap <ETH 金额> [输出代币] [链ID]` | 通过 Uniswap 进行 ETH 与代币的交换（使用链上路由 API） | 是 |
| `balance <地址> [链ID]` | 查看指定地址的 ETH 和稳定币余额 | 否（仅读） |
| `capabilities` | 显示当前的交易限额、预算和 gas 状态 | 是 |
| `decode <目标> <输入数据> <金额>` | 将交易意图解码为人类可读的摘要 | 是 |
| `panic` | 紧急冻结功能——立即生效，无需 Touch ID | 是 |
| `status` | 检查守护进程的健康状况和钱包信息 | 是 |
| `identity [查询\|注册]` | 支持 ERC-8004 标准的身份验证操作 | 部分支持 |
| `setup` | 运行设置向导，显示钱包状态和配置信息 | 是 |
| `policy` | 查看当前的交易策略 | 是 |
| `policy update '<json>'` | 更新交易策略（需要 Touch ID） | 是 |
| `allowlist <添加\|删除> <地址> [标签>` | 将地址添加或从允许列表中删除（需要 Touch ID） | 是 |
| `audit-log` | 查看守护进程的审计日志 | 是 |

## 安全模型

- 该工具本身不存储或处理任何敏感数据（如私钥），仅负责构建交易意图（`{目标地址, 输入数据, 交易金额}`）。
- 该工具绝不会自行设置交易中的 nonce 值、gas 费用、链 ID、交易费用或签名信息。
- 所有交易操作均由本地的 macOS 守护进程（`MonolithDaemon`）负责执行，并严格遵守预设的策略。
- 在策略允许的范围内，交易会自动执行。
- 超出限制或使用未知输入数据的交易需要用户通过 8 位验证码进行手动批准。
- 所有涉及代币的操作（如 `approve`, `permit` 等）都必须获得明确批准。

## 需要审批的情况：

- 超过单次交易或每日交易额度的转账
- 向未列入允许列表的地址转账
- 任何代币相关的操作（如 `approve`, `permit` 等）
- 使用未知的输入数据（系统默认为拒绝操作）

## 可自动执行的操作：

- 在允许列表内的地址之间进行 ETH 或 USDC 的转账
- 在允许列表内的去中心化交易所（如 Uniswap）中进行交易（遵循滑点限制）
- 在允许列表内的去中心化金融（DeFi）协议中进行存款/取款操作
- 查看余额、查询状态或解码交易数据

## 设置步骤：

1. 从 ClawHub 安装 Monolith：`clawhub install monolith`
2. 启动一个新的 OpenClaw 会话以加载该工具。
3. 安装所需的 macOS 组件：
   - `MonolithDaemon-v0.1.5.pkg`（管理员/root 用户安装）
   - `MonolithCompanion.app.zip`（解压后放入 `/Applications` 目录并运行一次）
4. 先启动守护进程，再启动配套应用程序；如果配套应用程序先被启动，请在守护进程运行后重新启动它。
5. 运行 `monolith setup` 命令以验证守护进程与配套应用程序之间的连接以及钱包状态。
6. 用 ETH 向钱包地址充值。
7. 开始进行交易。

### 首次安装注意事项（OpenClaw 机器人/操作员）：

- 所有需要审批的操作（如转账或设置交易策略）都需要用户通过 Touch ID 进行身份验证，并会收到通知。
- 仅支持无界面的 SSH 会话无法完成生物识别或通知相关的审批流程。
- 在执行 `send`, `swap`, `policy`, `allowlist` 等命令之前，务必先运行 `monolith setup` 命令以检查系统是否正常运行。

## 错误处理：

- 如果守护进程未运行，所有涉及签名的操作都会失败，并会显示相应的错误信息。
- 如果系统中的 gas 费用不足，守护进程会拒绝交易——请为钱包充值更多 ETH。
- 如果钱包被冻结，将无法进行任何出站交易，直到解除冻结（需要用户输入 Touch ID 并等待 10 分钟）。
- 如果受到 Pimlico 的速率限制，守护进程会自动采用指数级退避策略来重试请求。

## 审批流程：

当交易超出策略限制或使用未知的输入数据时，守护进程会返回 HTTP 202 错误响应，其中包含错误原因、交易摘要和失效时间。此时，代理应：

1. 向用户展示错误原因和交易摘要。
2. 请求用户输入守护进程显示的 8 位验证码。
3. 使用相同的交易意图以及 `approvalCode` 字段再次调用 `send` 命令以完成交易。

**注意：** 不需要单独的审批脚本——只需在调用 `send` 或 `swap` 命令时传递验证码即可。

## 交换路由：

- 在可用情况下，使用 Uniswap 的路由 API 进行交易；如果 API 故障或返回错误结果，系统会自动切换到链上的 V3 费用层级机制（尝试 3000、5000、10000 bps 的不同费用层级，选择最优报价）。

## 支持的链：

- Ethereum 主网（链 ID 1）
- Base（链 ID 8453）