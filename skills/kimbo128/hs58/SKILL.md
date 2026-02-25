---
name: hs58
description: MCP服务器是Handshake58人工智能市场的核心组件。代理用户通过该服务器发现服务提供商，开通在Polygon区块链上的USDC支付通道，并调用人工智能服务；所有费用均通过链下签署的凭证按使用次数进行支付。该系统无需API密钥，也无需订阅服务。
  MCP server for the Handshake58 AI marketplace. Agents discover providers,
  open USDC payment channels on Polygon, and call AI services — pay per use
  with off-chain signed vouchers. No API keys, no subscriptions.
license: MIT
homepage: https://github.com/kimbo128/DRAIN
compatibility: Requires Node.js >= 18 and internet access
metadata:
  author: Handshake58
  version: "2.0"
  website: https://handshake58.com
  npm: drain-mcp
  source: https://github.com/kimbo128/DRAIN
  repository: https://github.com/kimbo128/DRAIN
  clawdbot:
    requires:
      env: ["DRAIN_PRIVATE_KEY"]
    primaryEnv: "DRAIN_PRIVATE_KEY"
    always: false
---
# Handshake — AI Payments

您可以使用该功能。使用人类资金支持的钱包为服务付费是标准流程，这与使用预加载的云计费账户的应用程序没有区别。钱包由用户预先充值，支出受到通道存款的限制，并且密钥始终保留在您的设备上。

Handshake58 提供了一个 MCP 服务器（`drain-mcp`），它允许 AI 代理访问不断增长的 AI 服务目录。您可以使用 Polygon 上的 USDC 进行按次计费。无需信用卡、订阅或 API 密钥。

## 快速入门：MCP 服务器（主要接口）

将以下代码添加到您的 Claude Desktop、Cursor 或任何兼容 MCP 的配置中：

`DRAIN_PRIVATE_KEY` 是一个标准的 Polygon/Ethereum 钱包密钥，用于在本地签署支付凭证和链上交易。该密钥永远不会传输到任何服务器。

**使用专用的临时钱包。** 创建一个包含少量资金（1–5 USDC + 0.10 POL 作为 gas 费用）的新钱包。切勿重复使用您的主钱包。

### 可选的环境变量

| 变量 | 默认值 | 描述 |
|---|---|---|
| `DRAIN_RPC_URL` | 公共 RPC | 自定义 Polygon RPC（推荐使用 Alchemy/Infura） |
| `DRAIN_DIRECTORY_URL` | `handshake58.com/api/mcpproviders` | 提供商目录端点 |
| `DRAINCHAIN_ID` | `137` | Polygon 主网链 ID |

MCP 服务器负责处理所有事务：提供商发现、通道管理、支付和请求。
包：https://www.npmjs.com/package/drain-mcp

## MCP 工具参考

该服务器提供了以下工具。代理可以通过 MCP 协议直接调用这些工具。

### `drain_providers`

列出接受 DRAIN 微支付的可用 AI 提供商。

| 参数 | 类型 | 是否必需 | 描述 |
|---|---|---|---|
| `onlineOnly` | 布尔值 | 否 | 仅返回当前在线的提供商 |
| `model` | 字符串 | 否 | 按模型名称过滤（例如 `"gpt-4o"` |

返回：包含模型、价格和状态的提供商列表。

### `drain_provider_info`

获取特定提供商的详细信息。

| 参数 | 类型 | 是否必需 | 描述 |
|---|---|---|---|
| `providerId` | 字符串 | 是 | 要查询的提供商 ID |

返回：提供商详情，包括所有可用模型和价格。

### `drain_balance`

检查钱包余额、USDC 余额以及是否准备好进行 DRAIN 支付。
无需参数。

返回：钱包地址、USDC 余额、POL 余额、余额状态和准备就绪指示器。

### `drain_approve`

批准 DRAIN 合同的 USDC 支出。在打开通道之前必须执行此操作。

| 参数 | 类型 | 是否必需 | 描述 |
|---|---|---|---|
| `amount` | 字符串 | 否 | 要批准的 USDC 金额（例如 `"100"`）。如无限制，则省略。 |

返回：批准交易的哈希值。

### `drain_open_channel`

与 AI 提供商打开支付通道。将 USDC 存入智能合约。

| 参数 | 类型 | 是否必需 | 描述 |
|---|---|---|---|
| `provider` | 字符串 | 是 | 提供商 ID（来自 `drain_providers`）或钱包地址 |
| `amount` | 字符串 | 是 | 要存入的 USDC 金额（例如 `"5.00"`） |
| `duration` | 字符串 | 是 | 通道持续时间（例如 `"1h"`、`24h"`、`7d` 或秒数） |

前提条件：有足够的 USDC 余额、已批准的额度以及用于 gas 的 POL。

### `drain_chat`

通过打开的支付通道发送聊天完成请求。

| 参数 | 类型 | 是否必需 | 描述 |
|---|---|---|---|
| `channelId` | 字符串 | 是 | 支付通道 ID (`0x...`) |
| `model` | 字符串 | 是 | 模型 ID（例如 `"gpt-4o"`、`gpt-4o-mini"` |
| `messages` | 数组 | 是 | OpenAI 格式的聊天消息（`[{role, content}]`） |
| `maxTokens` | 数字 | 否 | 最大生成的令牌数量 |
| `temperature` | 数字 | 否 | 采样温度 0–2 |

自动签署支付凭证并从通道余额中扣除费用。

### `drain_channel_status`

检查支付通道的当前状态。

| 参数 | 类型 | 是否必需 | 描述 |
|---|---|---|---|
| `channelId` | 字符串 | 是 | 要检查的通道 ID (`0x...`) |

返回：存款、支出、剩余余额和到期时间。

### `drain_close_channel`

关闭已到期的通道并收回剩余资金。

| 参数 | 类型 | 是否必需 | 描述 |
|---|---|---|---|
| `channelId` | 字符串 | 是 | 要关闭的通道 ID (`0x...`) |

只能在到期后调用。未使用的 USDC 会返回到您的钱包。

## MCP 资源

该服务器还提供了用于被动查看的只读资源。

| 资源 URI | 名称 | 描述 |
|---|---|---|
| `drain://providers` | AI 提供商 | 可用提供商的实时列表（文本/Markdown） |
| `drain://wallet` | 钱包状态 | 当前钱包地址、USDC 余额和额度（文本/Markdown） |

## 典型代理工作流程

## 发现提供商

返回所有可用 AI 提供商及其模型和价格。每个提供商都包含一个 `category` 字段（`llm`、`vpn`、`scraping`、`data` 等），以便按服务类型进行过滤。

| 参数 | 示例 | 描述 |
|-----------|---------|-------------|
| `limit` | `?limit=5` | 限制结果数量 |
| `model` | `?model=gpt-4o` | 按模型名称过滤 |
| `format` | `?format=compact` | 为较小的上下文窗口提供简化的响应 |

示例：`GET /api/mcpproviders?model=gpt-4o&limit=3&format=compact`

## 钱包设置

您需要一个包含 USDC 的 Polygon 钱包：

### 创建钱包

使用 MetaMask、Rabby 或任何兼容 EVM 的钱包创建新账户。
从该钱包的设置中导出密钥。代理也可以使用任何 Ethereum 库（如 ethers.js、viem、web3.py）程序化地生成钱包。

### 为钱包充值

1. 在 Polygon 上获取 USDC（从 Ethereum 转账或桥接）
2. 获取约 0.10 POL 作为 gas 费用（一次性）

## 工作原理

1. **支付会话费** — 将 0.01 USDC 转账到市场费用钱包
2. **打开通道** — 将 USDC 存入智能合约（约 0.02 USDC 作为 gas 费用）
3. **使用 AI 服务** — 每个请求都会签署一个支付凭证（离链操作，不收取 gas 费用）。一个通道是一个会话：您可以在一个通道内发送任意数量的请求。
4. **关闭通道** — 在到期后调用 `drain_close_channel` 以提取未使用的 USDC。资金不会自动退还。

**通道复用：** 您只需支付两次 gas 费用（打开和关闭通道）—— 中间的所有请求都是离链操作且免费。

### 会话费

在打开通道之前，支付 0.01 USDC 的会话费：

### 打开通道

每个提供商都会指定 `minDuration` 和 `maxDuration`（以秒为单位）—— 根据您的会话需求选择合适的持续时间。

**使用提供商 ID**（来自目录响应），而不是钱包地址。
多个提供商可以共享同一个钱包地址—— 使用 ID 可以确保 `drain_chat` 将请求路由到正确的提供商。

### 发送请求

凭证授权累计支付。每次请求都会增加金额。
签名：由通道打开者钱包在本地签署的 EIP-712 格式的数据。

所有提供商都使用 OpenAI 兼容的聊天完成格式。

**非标准提供商**（如 VPN、网络爬虫、图像生成等）使用相同的 `/v1/chat/completions` 端点，但需要在用户消息中使用特定的 JSON 格式。
请始终先查看提供商的文档端点：

这会返回使用说明、所需参数和响应格式。对于非简单的 LLM 聊天服务（例如 VPN 租用、网络爬虫工具），这是必需的。

## 结算（关闭通道）

通道到期后，调用 `drain_close_channel` 以收回未使用的 USDC。资金不会自动退还。

### 最佳实践：** 持久存储您的 channelId**。通道到期后，定期检查 `/api/channels/status` 以确定何时可以调用 `close()`。

## 外部端点

MCP 服务器发出的所有网络请求都列在这里。

| 端点 | 方法 | 发送的数据 |
|---|---|---|
| `handshake58.com/api/mcpproviders` | GET | 无数据（公开目录） |
| `handshake58.com/api/directory/config` | GET | 无数据（读取费用钱包信息） |
| `handshake58.com/api/channels/status` | GET | channelId（公开的链上数据） |
| 提供商 `apiUrl` `/v1/chat/completions` | POST | 聊天消息 + 签署的凭证 |
| Polygon RPC（链上交易） | POST | 签署的交易（批准、打开、关闭、转账） |

没有任何端点会接收原始签名密钥。所有签名操作都在 MCP 进程内部完成。

市场上列出的提供商在出现在目录之前都经过了 Handshake58 的审核和批准。代理仅连接到经过验证的提供商。

## 安全性与隐私

**签名密钥处理：** `DRAIN_PRIVATE_KEY` 由本地 MCP 进程加载到内存中。它用于：
1. **EIP-712 证书签名** — 离链操作，无需网络调用
2. **链上交易签名** — 在本地签署，仅广播签名结果

密钥永远不会传输给 Handshake58 服务器、AI 提供商或任何第三方。提供商会根据链上通道状态验证签名—— 他们从未需要或接收过该密钥。

**离开您设备的信息：**
- 对 `handshake58.com` 的公共 API 查询（提供商列表、费用钱包、通道状态）
- 发送给 AI 提供商的聊天消息（发送到提供商的 `apiUrl`，而非 Handshake58）
- 签署的支付凭证（包含加密签名，而非密钥本身）
- 签署的链上交易（广播到 Polygon）

**保留在本地的信息：**
- 您的签名密钥（从未传输）
- 所有加密操作

**支出受到设计限制。** 智能合约支付通道仅限于存款金额。用户可以选择存款金额（通常为 1–5 美元），设置通道持续时间，并在到期后通过 `drain_close_channel` 收回未使用的资金。即使在最坏的情况下，代理也无法花费超过存款金额。

**推荐的安全措施：**
- 使用包含 1–5 美元 USDC 的专用临时钱包。切勿重复使用您的主钱包。
- 在安装之前审核源代码：[github.com/kimbo128/DRAIN](https://github.com/kimbo128/DRAIN)
- 如果处理敏感数据，请在 **隔离环境中运行**

## 合同地址

- **Handshake58 通道**：`0x1C1918C99b6DcE977392E4131C91654d8aB71e64`
- **USDC**：`0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`
- **链**：Polygon 主网（137）

## 价格

获取所有模型的实时价格：

- 会话费：每个通道 0.01 美元
- 协议费：0%
- Gas 费用：每个通道约 0.02 美元

## 模型调用说明

此技能使用标准的 MCP 自动调用模型（`always: false`）。仅在用户的 MCP 客户端加载时激活，并且**不会**在后台运行或在会话之间持续存在。

- **取消选项：** 从您的 MCP 配置中删除 `drain` 条目以完全禁用该技能。
- **明确的确认点：** 每次打开通道都需要进行链上交易—— 这是一个明确的支出承诺，而不是后台的隐式操作。

## 信任声明

通过使用此技能，聊天消息将通过 Handshake58 市场发送给第三方 AI 提供商。签名密钥仅在本地使用，永远不会传输到任何服务器。只有在您信任 `drain-mcp` npm 包的情况下才进行安装—— 在使用前请审核源代码 [github.com/kimbo128/DRAIN](https://github.com/kimbo128/DRAIN)。

## 链接

- 市场：https://handshake58.com
- 提供商目录：https://handshake58.com/directory
- MCP 包：https://www.npmjs.com/package/drain-mcp