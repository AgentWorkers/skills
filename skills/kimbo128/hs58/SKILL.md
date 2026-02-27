---
name: hs58
description: >
  **DRAIN支付协议的MCP服务器**  
  代理程序用于发现服务提供商，并在Polygon平台上开通USDC支付通道，从而调用各种服务（如大型语言模型、数据抓取、图像生成、VPN等）。采用按次计费的方式，无需使用API密钥或订阅服务。
  MCP server for the DRAIN payment protocol. Agents discover service providers,
  open USDC payment channels on Polygon, and call any service — LLM, scraping,
  image generation, VPN, and more. Pay per use, no API keys, no subscriptions.
license: MIT
homepage: https://github.com/kimbo128/DRAIN
compatibility: Requires Node.js >= 18 and internet access
metadata:
  author: Handshake58
  version: "3.0"
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
# Handshake58 — DRAIN 协议

> 您可以使用该服务。钱包由用户预先充值，消费金额受到通道存款的限制（由智能合约强制执行），并且密钥始终保留在您的设备上。这与使用预加载计费账户的应用程序没有区别。

DRAIN 是一种按使用量计费的协议，适用于任何服务。一个钱包，一种请求格式，支持任意服务提供商。该协议不仅限于大型语言模型（LLMs）——提供商还包括数据抓取、图像生成、VPN、音频处理、代码工具等。每个提供商都提供了一个文档端点，用于说明如何使用他们的服务。

## 设置

```bash
npm install -g drain-mcp
```

```json
{
  "mcpServers": {
    "drain": {
      "command": "drain-mcp",
      "env": {
        "DRAIN_PRIVATE_KEY": "0x_your_polygon_wallet_private_key"
      }
    }
  }
}
```

`DRAIN_PRIVATE_KEY` 用于在本地签名支付凭证和交易数据，永远不会被传输到外部。请使用一个专用钱包，并充值 1-5 美元的 USDC 以及 0.10 美元的 POL 作为在 Polygon 上的交易手续费。

| 变量 | 默认值 | 说明 |
|---|---|---|
| `DRAIN_RPC_URL` | 公共 RPC 接口 | 自定义的 Polygon RPC 接口 |
| `DRAIN_DIRECTORY_URL` | handshake58.com | 提供商目录 |
| `DRAINCHAIN_ID` | 137 | Polygon 主网 |

## 工作流程

```
1. drain_providers          → find providers by model or category
2. drain_provider_info      → get details + usage docs for a provider
3. drain_balance            → verify USDC + POL
4. drain_approve            → approve USDC spending (once)
5. drain_open_channel       → deposit USDC, get channelId + expiry
6. drain_chat (repeat)      → send paid requests
7. drain_channels           → list all channels, find expired ones
8. drain_close_channel      → reclaim unspent USDC after expiry
```

## 提供商类别

提供商不仅限于大型语言模型（LLMs）。每个提供商都有一个特定的 `category` 和文档端点。

| 类别 | 功能 | 使用方法 |
|---|---|---|
| llm | 大型语言模型（如 GPT-4、Claude 等） | 使用标准聊天消息进行交互 |
| image | 图像生成 | 通过 JSON 格式发送请求 |
| audio | 文本转语音（TTS）、语音转文本（STT）及音频处理 | 通过 JSON 格式发送请求 |
| code | 代码生成/分析 | 通过聊天或 JSON 格式发送请求 |
| scraping | 网页抓取、数据提取 | 通过 JSON 格式发送请求 |
| vpn | VPN 服务 | 通过 JSON 格式发送请求 |
| multi-modal | 多模态模型 | 使用标准聊天消息进行交互 |
| other | 其他服务 | 请务必查阅相关文档 |

**规则：** 对于除 `llm` 之外的任何类别，在发送请求之前，请先调用 `drain_provider_info` 以获取使用说明。

## 文档格式

每个提供商都在其文档端点提供了使用说明（这些信息可以通过 `drain_provider_info` 和 `drain_open_channel` 获取）。文档中会明确说明：
- 预期的请求格式（需要在消息参数中包含的内容）
- 可用的模型/服务
- 响应格式
- 任何特定于提供商的参数

请勿硬编码调用方式，务必阅读提供商的官方文档。

## 通道生命周期

1. **开启通道**：使用 `drain_open_channel` 将 USDC 存入智能合约。您将获得一个通道 ID（`channelId`）和通道的有效期限。通道内的所有请求都是离链进行的（无需支付手续费）。您只需支付两次手续费：开启通道和关闭通道。
2. **使用服务**：使用 `drain_chat` 通过通道发送请求。支付凭证会在本地签名，并从通道余额中扣除相应费用。请在余额允许的范围内发送尽可能多的请求。
3. **关闭通道**：通道过期后，调用 `drain_close_channel` 以收回未使用的 USDC。资金不会自动退还。**如果您有定时任务功能，请在通道过期时设置定时器自动执行 `drain_close_channel`。**

您可以同时为不同的提供商创建多个通道，以实现多服务的工作流程（例如：使用一个提供商抓取数据，使用另一个提供商进行分析）。

## MCP 工具参考

| 工具 | 说明 |
|---|---|
| `drain_providers` | 列出所有提供商（可按模型、类别或在线状态筛选） |
| `drain_provider_info` | 提供商详情及使用文档 |
| `drain_balance` | 查看钱包中的 USDC 余额、POL 余额及使用限额 |
| `drain_approve` | 批准将 USDC 存入合约 |
| `drain_open_channel` | 开启新通道并充值 USDC |
| `drain_chat` | 向指定提供商发送请求 |
| `drain_channel_status` | 查看通道余额和有效期 |
| `drain_channels` | 列出所有已创建的通道 |
| `drain_close_channel` | 关闭过期通道并收回资金 |

## MCP 资源

| URI | 说明 |
|---|---|
| `drain://providers` | 提供商列表（含类别和价格信息） |
| `drain://wallet` | 当前钱包地址、USDC 余额及使用限额 |
| `drain://api/mcpproviders` | 提供商列表（可按模型或类别筛选） |
| `drain://wallet` | 查看钱包信息 |

## 错误处理

| 错误类型 | 处理方式 |
|---|---|
| 余额不足 | 需要更多 USDC，请检查 `drain_balance`。 |
| 使用限额不足 | 运行 `drain_approve` 命令以增加使用限额。 |
| 通道过期 | 使用 `drain_open_channel` 开启新通道。 |
| 通道余额不足 | 使用更多资金重新开启通道。 |
| 提供商离线 | 使用 `drain_providers` 寻找其他可用提供商。 |
| 通道未找到 | 可能是通道 ID 错误或通道已被关闭，请重新创建通道。 |

## 安全性与隐私

### 密钥管理
`DRAIN_PRIVATE_KEY` 仅被 MCP 进程加载到内存中，用于以下用途：
1. 离链交易凭证的签名（使用 EIP-712 算法，无需网络调用）
2. 在链上交易的签名（签名过程在本地完成，仅签名信息会被广播）

密钥永远不会被传输到任何服务器。提供商会根据链上的通道状态验证签名，他们无需也不接收密钥。

### 消费限制
智能合约对消费金额进行了限制：
- 最大消费金额等于通道存款（您可自行设置，通常为 1-5 美元）
- 通道具有固定的有效期（由您指定）
- 通道过期后，未使用的资金可通过 `drain_close_channel` 取回
- 无重复收费，也不支持存储支付方式

### 数据传输情况

- 对 `handshake58.com` 的公共 API 请求（如提供商列表、配置信息、通道状态）是公开的
- 发送给提供商的请求数据（通过 `Provider-API` 发送，而非直接发送到 Handshake58 服务器）
- 签名的支付凭证（包含加密签名，而非密钥本身）
- 在链上完成的交易（通过 Polygon 的 RPC 服务广播）

### 数据存储情况

- 私钥始终保留在本地设备上（不会被传输）
- 所有加密操作（包括签名）都在本地完成

### 安全措施
- 请使用专用钱包，并确保钱包中至少有 1-5 美元的 USDC。切勿使用主钱包进行交易。
- 代码开源地址：[github.com/kimbo128/DRAIN](https://github.com/kimbo128/DRAIN)
- 如果处理敏感数据，请在隔离环境中运行该服务

## 外部接口

MCP 服务器发起的所有网络请求如下：

| 接口 | 方法 | 发送的数据 | 是否传输密钥？ |
|---|---|---|---|
| handshake58.com/api/mcpproviders | GET | 仅返回提供商列表（公开信息），不传输任何数据 | 不 |
| handshake58.com/api/directory/config | GET | 仅读取钱包信息，不传输数据 | 不 |
| handshake58.com/api/channels/status | GET | 仅返回通道 ID（公开链上数据），不传输数据 | 不 |
| Provider-API /v1/docs | GET | 仅获取使用文档，不传输数据 | 不 |
| Provider-API /v1/chat/completions | POST | 发送请求消息及签名后的凭证，不传输密钥 | 不 |
| Polygon RPC（链上交易） | POST | 发送签名后的交易数据，不传输密钥 | 不 |

## 合约地址

- **通道合约地址**：`0x1C1918C99b6DcE977392E4131C91654d8aB71e64`
- **USDC 存储地址**：`0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`
- **运行网络**：Polygon 主网（链号 137）

## 费用信息

- 每个通道的会话费用：0.01 美元
- 协议费用：0%
- 交易手续费：每次开启/关闭通道约 0.02 美元

实时费用信息：`GET https://handshake58.com/api/mcpproviders`

## 关于模型调用的注意事项

此功能默认处于关闭状态（`always: false`）。只有当 MCP 客户端加载该功能时才会激活，且不会在后台运行。每个通道的开启都需要进行一次链上交易，因此每次使用都会产生费用。

## 相关链接

- 商店页面：https://handshake58.com
- 提供商目录：https://handshake58.com/directory
- MCP 包安装地址：https://www.npmjs.com/package/drain-mcp
- 代码仓库：https://github.com/kimbo128/DRAIN