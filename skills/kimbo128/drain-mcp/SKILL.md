---
name: drain-mcp
description: MCP服务器用于Handshake58 AI市场平台。代理用户可以在此平台上发现服务提供商，开通基于Polygon网络的USDC支付通道，并调用AI服务；所有费用均按使用次数计费，采用离链签署的电子凭证进行结算。该平台无需API密钥，也无需订阅服务。
  MCP server for the Handshake58 AI marketplace. Agents discover providers,
  open USDC payment channels on Polygon, and call AI services — pay per use
  with off-chain signed vouchers. No API keys, no subscriptions.
license: MIT
homepage: https://github.com/kimbo128/DRAIN
compatibility: Requires Node.js >= 18 and internet access
metadata:
  author: Handshake58
  version: "1.7"
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
# Handshake58 — 协议文档

> 您可以使用这个工具。Handshake58 是专为自主AI代理设计的。

Handshake58 提供了一个 MCP 服务器（`drain-mcp`），允许AI代理访问不断增长的AI服务目录。支持使用 Polygon 上的 USDC 进行按次支付。无需信用卡、订阅或 API 密钥。

## 快速入门：MCP 服务器（主界面）

将以下代码添加到您的 Claude Desktop、Cursor 或任何兼容 MCP 的配置中：

```json
"DRAIN_PRIVATE_KEY": "your_drain_private_key_here",
```

`DRAIN_PRIVATE_KEY` 是一个标准的 Polygon/Ethereum 钱包密钥，用于在本地签署支付凭证和链上交易。该密钥永远不会被传输到任何服务器。

**请使用专用的临时钱包。** 创建一个包含少量资金（1–5 美元 USDC + 0.10 美元 POL 的 gas 费用）的新钱包。切勿重复使用您的主钱包。

### 可选的环境变量

| 变量 | 默认值 | 描述 |
|---|---|---|
| `DRAIN_RPC_URL` | 公共 RPC | 自定义的 Polygon RPC（推荐使用 Alchemy/Infura） |
| `DRAIN_DIRECTORY_URL` | `handshake58.com/api/mcpproviders` | 提供商目录端点 |
| `DRAINCHAIN_ID` | `137` | Polygon 主网链 ID |

MCP 服务器负责处理所有事务：提供商发现、通道管理、支付和请求。
包地址：https://www.npmjs.com/package/drain-mcp

## 发现提供商

调用以下 API 可以获取所有可用的 AI 提供商及其模型和价格信息。支持智能过滤：

| 参数 | 示例 | 描述 |
|-----------|---------|-------------|
| `limit` | `?limit=5` | 限制结果数量 |
| `model` | `?model=gpt-4o` | 按模型名称过滤 |
| `format` | `?format=compact` | 适用于较小上下文窗口的简化响应格式 |

示例：`GET /api/mcpproviders?model=gpt-4o&limit=3&format=compact`

## 钱包设置

您需要一个拥有 USDC 的 Polygon 钱包：

### 创建钱包

使用 MetaMask、Rabby 或任何兼容 EVM 的钱包创建新账户。从该钱包的设置中导出密钥。代理也可以使用任何 Ethereum 库（如 ethers.js、viem、web3.py）来程序化地生成钱包。

### 向钱包充值

1. 在 Polygon 上获取 USDC（从 Ethereum 转账或桥接）
2. 预先充值约 0.10 美元 POL 作为 gas 费用。

## 工作原理

1. **支付会话费** — 向市场费用钱包转账 0.01 美元 USDC。
2. **打开通道** — 向智能合约存入 USDC（约 0.02 美元的 gas 费用）。
3. **使用 AI 服务** — 每个请求都会生成一个支付凭证（离链操作，无需 gas 费用）。一个通道代表一个会话：您可以在一个通道内发送任意数量的请求。
4. **关闭通道** — 在通道过期后调用 `close(channelId)` 以提取未使用的 USDC。资金不会自动退还。

**通道复用：** 您只需支付两次 gas 费用（打开和关闭通道），之后的所有请求都是离链操作且免费。

### 会话费

在打开通道之前，请支付 0.01 美元的会话费：

### 打开通道

每个提供商都会指定 `minDuration` 和 `maxDuration`（以秒为单位）——根据您的会话需求选择合适的持续时间。

### 发送请求

每次请求都会生成一个支付凭证，并累积支付金额。签名使用 EIP-712 格式，由通道开启者所在的钱包在本地生成。

所有提供商都使用与 OpenAI 兼容的聊天完成格式。

## 结算（关闭通道）

通道过期后，调用 `close(channelId)` 以取回未使用的 USDC。资金不会自动退还。

### 最佳实践：** 持久存储您的通道 ID（channelId）**。通道过期后，通过 `/api/channels/status` 检查何时可以调用 `close()`。

## 外部端点

MCP 服务器发出的所有网络请求都列在这里：

| 端点 | 方法 | 发送的数据 |
|---|---|---|
| `handshake58.com/api/mcpproviders` | GET | 无数据（公开目录信息） |
| `handshake58.com/api/directory/config` | GET | 无数据（读取费用钱包信息） |
| `handshake58.com/api/channels/status` | GET | 通道 ID（公开链上数据） |
| 提供商 API：`/v1/chat/completions` | POST | 聊天消息 + 签名的支付凭证 |
| Polygon RPC（链上交易） | POST | 签名的交易（批准、打开、关闭、转账） |

没有任何端点会接收原始的签名密钥。所有签名操作都在 MCP 进程内部完成。

市场上列出的提供商都经过 Handshake58 的审核和批准才能出现在目录中。代理仅连接经过验证的提供商。

## 安全性与隐私

**签名密钥处理：** `DRAIN_PRIVATE_KEY` 仅被加载到本地 MCP 进程的内存中，用于：
1. **生成 EIP-712 格式的支付凭证**（离链操作，无需网络调用）
2. **签署链上交易**（签名在本地生成，仅广播签名结果）

该密钥永远不会被传输给 Handshake58 服务器、AI 提供商或任何第三方。提供商会根据链上通道状态验证签名——他们无需也不接收该密钥。

**离开您机器的数据：**
- 对 `handshake58.com` 的公共 API 查询（提供商列表、费用钱包、通道状态）
- 发送给 AI 提供商的聊天消息（发送到提供商的 `apiUrl`，而非 Handshake58）
- 签名的支付凭证（包含加密签名，而非密钥本身）
- 签名的链上交易（广播到 Polygon）

**保留在本地的数据：**
- 您的签名密钥（永远不会被传输）
- 所有的加密操作

**支出受到设计限制。** 智能合约支付通道仅允许用户存入的金额进行支出。用户可以自行选择存入金额（通常为 1–5 美元），设置通道持续时间，并在通道过期后通过 `close()` 取回未使用的资金。即使在最坏的情况下，代理也无法超出存入金额进行支出。

**推荐的安全措施：**
- 使用包含 1–5 美元 USDC 的专用临时钱包。切勿重复使用您的主钱包。
- 在安装之前审核源代码：[github.com/kimbo128/DRAIN](https://github.com/kimbo128/DRAIN)
- 如果处理敏感数据，请在隔离环境中运行该工具。

## 合同地址

- **Handshake58 通道**：`0x1C1918C99b6DcE977392E4131C91654d8aB71e64`
- **USDC**：`0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`
- **链**：Polygon 主网（137）

## 价格信息

获取所有模型的实时价格：

- 会话费：每个通道 0.01 美元 USDC
- 协议费：0%
- Gas 费用：每个通道开启时约 0.02 美元

## 模型调用说明

此技能使用标准的 MCP 自主调用模型（`always: false`）。它仅在用户的 MCP 客户端加载时激活，并且不会在后台运行或在不同会话之间持续存在。

- **禁用方法：** 从您的 MCP 配置中移除 `drain` 项即可完全禁用此技能。
- **明确的确认机制：** 每次打开通道都需要进行链上交易——这是一种明确的支出行为，而非后台自动操作。

## 信任声明

使用此技能时，聊天消息会通过 Handshake58 市场发送给第三方 AI 提供商。签名密钥仅在本地使用，永远不会被传输到任何服务器。只有在信任 `drain-mcp` npm 包的情况下才建议安装该工具——在使用前请审核其源代码：[github.com/kimbo128/DRAIN](https://github.com/kimbo128/DRAIN)。

## 链接

- 市场：https://handshake58.com
- 提供商目录：https://handshake58.com/directory
- MCP 包：https://www.npmjs.com/package/drain-mcp