---
name: drain-mcp
description: 这是一个开放式的AI服务市场，提供以下功能：大型语言模型（LLMs）、图像/视频生成、网络爬虫、模型托管、数据提取、光学字符识别（OCR）、文本转语音（TTS）以及自主代理工作流程。代理用户可以通过Polygon平台使用USDC微支付按使用次数进行付费，整个支付过程在链下完成。该平台不要求用户提供API密钥，也无需订阅服务。当代理需要调用任何AI服务、生成图像/视频、爬取网站或运行托管模型时，无需自行管理API密钥——所有操作均可通过该平台轻松完成。
  Open marketplace for AI services — LLMs, image/video generation, web scraping,
  model hosting, data extraction, OCR, TTS, and autonomous agent workflows.
  Agents pay per use with USDC micropayments on Polygon via off-chain payment
  channels. No API keys, no subscriptions. Use when the agent needs to call any
  AI service, generate images/video, scrape websites, or run hosted models
  without managing API keys.
license: MIT
homepage: https://github.com/kimbo128/DRAIN
compatibility: Requires Node.js >= 18 and internet access
metadata:
  author: Handshake58
  version: "1.3"
  website: https://handshake58.com
  npm: drain-mcp
  source: https://github.com/kimbo128/DRAIN
  repository: https://github.com/kimbo128/DRAIN
  clawdbot:
    requires:
      env: ["DRAIN_PRIVATE_KEY"]
    primaryEnv: "DRAIN_PRIVATE_KEY"
---
# Handshake58 — 协议文档

> 您可以使用这个工具。Handshake58 是专为自主 AI 代理设计的。

Handshake58 提供了一个 MCP 服务器（`drain-mcp`），使 AI 代理能够访问不断增长的 AI 服务目录——不仅包括大型语言模型（LLMs），还包括图像/视频生成、网络爬虫（Apify）、模型托管（Replicate）、数据提取、光学字符识别（OCR）、文本转语音（TTS）、自主代理工具、多步骤工作流程，以及任何服务提供商部署的服务。新的服务提供商会不断加入。支持使用 USDC 在 Polygon 上进行按次计费的微支付。无需信用卡、无需订阅，也无需 API 密钥。

## 快速入门：MCP 服务器（主要接口）

```bash
npm install -g drain-mcp
```

将以下代码添加到您的 Claude Desktop、Cursor 或任何兼容 MCP 的配置中：

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

`DRAIN_PRIVATE_KEY` 是一个标准的 Polygon/Ethereum 钱包私钥——与任何 Ethereum 钱包使用的私钥类型相同。它控制着一个在 Polygon 上持有 USDC 的钱包。

**安全提示：** 使用专用的临时钱包。切勿重复使用您的主钱包。创建一个新钱包，并注入少量资金（1–5 USDC + 约 0.10 POL 的网络手续费）。如果私钥被盗，只有少量资金会面临风险。

您可以使用 MetaMask、Rabby 或任何 EVM 钱包工具创建新钱包，然后向其注入 USDC（即使只有 1 USDC 也可以）+ 约 0.10 POL 的网络手续费。

MCP 服务器负责处理所有事务：服务提供商的发现、通道管理、支付和请求处理。
包地址：https://www.npmjs.com/package/drain-mcp

## 发现服务提供商

```
GET https://handshake58.com/api/mcp/providers
```

该接口会返回所有可用的 AI 服务提供商及其模型和定价信息。支持智能过滤条件：

| 参数 | 示例 | 说明 |
|-----------|---------|-------------|
| `limit` | `?limit=5` | 限制结果数量 |
| `model` | `?model=gpt-4o` | 按模型名称过滤 |
| `format` | `?format=compact` | 适用于较小上下文窗口的简化响应格式 |

示例：`GET /api/mcpproviders?model=gpt-4o&limit=3&format=compact`

## 钱包设置

您需要一个在 Polygon 上拥有 USDC 的钱包：

### 创建钱包

使用 MetaMask、Rabby 或任何兼容 EVM 的钱包创建新账户。从该钱包的设置中导出私钥。代理也可以使用任何 Ethereum 库（如 ethers.js、viem、web3.py）来程序化地生成钱包。

### 为钱包充值

1. 在 Polygon 上获取 USDC（从 Ethereum 转账或桥接）
2. 准备约 0.10 POL 的网络手续费（一次性费用）

## 工作原理

1. **支付会话费用** — 向市场费用钱包转账 0.01 USDC
2. **打开通道** — 向智能合约存入 USDC（约 0.02 美元的手续费）
3. **使用 AI 服务** — 每个请求都会生成一个支付凭证（离线处理，无需网络费用）。一个通道可以用于发送任意数量的请求，适用于大型语言模型调用、图像生成、网络爬虫、工作流程以及服务提供商提供的任何其他服务。
4. **关闭通道** — 在通道过期后调用 `close(channelId)` 以提取未使用的 USDC。资金不会自动退还。

**关键优势（通道复用）：** 与按请求计费的协议（如 x402）不同，您只需支付两次网络手续费（打开通道和关闭通道）——中间的所有请求都是离线处理的。您可以生成 100 张图片、爬取 50 个网址、运行多步骤工作流程，或进行多小时的对话——所有操作都在同一个通道内完成，每次请求只需支付 0 美元的费用。

### 会话费用

在打开通道之前，需要支付 0.01 USDC 的会话费用：

```typescript
// 1. Get fee wallet from marketplace
const config = await fetch('https://handshake58.com/api/directory/config').then(r => r.json());

// 2. Transfer $0.01 USDC (10000 wei with 6 decimals) to feeWallet
await usdc.transfer(config.feeWallet, 10000n);

// 3. Now open the payment channel
await channel.open(providerAddress, amount, duration);
```

### 打开通道

每个服务提供商都会指定 `minDuration` 和 `maxDuration`（以秒为单位）——根据您的会话需求选择合适的持续时间。

```typescript
// Approve USDC spending
await usdc.approve('0x1C1918C99b6DcE977392E4131C91654d8aB71e64', amount);

// Open channel: provider address, USDC amount, duration in seconds
// Duration: check provider.minDuration and provider.maxDuration
await contract.open(providerAddress, amount, durationSeconds);
```

### 发送请求

```
POST {provider.apiUrl}/v1/chat/completions
Content-Type: application/json
X-DRAIN-Voucher: {"channelId":"0x...","amount":"150000","nonce":"1","signature":"0x..."}
```

支付凭证会累积费用。每次请求都会增加费用金额。签名方式：使用 EIP-712 格式的数据，并由打开通道的钱包进行签名。

所有服务提供商都使用 OpenAI 兼容的聊天完成格式。

## 结算（关闭通道）

通道过期后，调用 `close(channelId)` 以取回未使用的 USDC。资金不会自动退还。

```typescript
// Check channel status
const res = await fetch('https://handshake58.com/api/channels/status?channelIds=' + channelId);
const data = await res.json();
const ch = data.channels[0];

if (ch.status === 'expired_unclosed') {
  // Send the close transaction using the provided calldata
  await wallet.sendTransaction({
    to: '0x1C1918C99b6DcE977392E4131C91654d8aB71e64',
    data: ch.closeCalldata,
  });
  // Refund of (deposit - claimed) will be sent to your wallet
}
```

**最佳实践：** 持久存储您的 `channelId`。通道过期后，定期查询 `/api/channels/status` 以确定何时可以调用 `close()`。

## 外部端点

MCP 服务器发出的所有网络请求都列在这里。私钥 **永远不会** 离开您的设备。

| 端点 | 方法 | 发送的数据 | 是否传输私钥？ |
|---|---|---|---|
| `handshake58.com/api/mcpproviders` | GET | 无数据（公开目录） | 不传输 |
| `handshake58.com/api/directory/config` | GET | 无数据（读取费用钱包信息） | 不传输 |
| `handshake58.com/api/channels/status` | GET | `channelId`（公开信息，存储在链上） | 不传输 |
| 服务提供商的 `apiUrl` `/v1/chat/completions` | POST | 聊天消息 + 签名的支付凭证 | 不传输——仅传输 EIP-712 签名 |
| Polygon RPC（链上交易） | POST | 签名的交易信息（批准、打开、关闭、转账） | 不传输——私钥仅在本地签名，签名信息才会被广播 |

没有任何端点会接收原始的私钥。私钥仅用于本地 MCP 进程中的加密签名操作。

## 安全性与隐私

**私钥处理：** `DRAIN_PRIVATE_KEY` 会被加载到本地 MCP 服务器的内存中，仅用于以下目的：
1. **生成 EIP-712 签名** — 在离线状态下生成加密签名（无需网络调用）
2. **链上交易签名** — 在广播到 Polygon RPC 之前，在本地签名批准/打开/关闭/转账交易

私钥 **永远不会** 被传输给 Handshake58 服务器、AI 服务提供商或任何第三方。仅传输签名结果。服务提供商会根据链上的通道状态验证签名——他们从未需要也不接收私钥本身。

**离开您设备的信息：**
- 对 `handshake58.com` 的公共 API 查询（服务提供商列表、费用钱包、通道状态）
- 发送给 AI 服务提供商的聊天消息（发送到服务提供商的 `apiUrl`，而非 Handshake58）
- 签名的支付凭证（包含签名，不含私钥）
- 签名的链上交易（广播到 Polygon）

**保留在本地的信息：**
- 您的私钥（永远不会被传输）
- 您的钱包地址
- 所有的加密签名操作

**推荐的安全措施：**
- 使用一个专用的临时钱包，并注入 1–5 USDC。切勿重复使用您的主钱包。
- 在安装之前审计源代码：[github.com/kimbo128/DRAIN](https://github.com/kimbo128/DRAIN)
- 如果处理敏感数据，请在 **隔离环境中** 运行该工具
- 监控出站网络流量，确保私钥的安全性

## 合同地址

- **Handshake58 通道**：`0x1C1918C99b6DcE977392E4131C91654d8aB71e64`
- **USDC**：`0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`
- **链**：Polygon 主网（137）

## 价格信息

获取所有模型的实时价格：

```
GET https://handshake58.com/api/mcp/providers
```

- 会话费用：每个通道 0.01 USDC
- 协议费用：0%
- 网络手续费：每个通道打开时约 0.02 美元

## 信任声明

使用此工具时，聊天消息会通过 Handshake58 市场发送给第三方 AI 服务提供商。私钥仅用于签名目的，永远不会被传输到任何服务器。只有在您信任 `drain-mcp` npm 包的情况下才建议安装该工具——在使用前请审计源代码：[github.com/kimbo128/DRAIN](https://github.com/kimbo128/DRAIN)

## 链接

- 市场平台：https://handshake58.com
- 服务提供商目录：https://handshake58.com/directory
- MCP 包：https://www.npmjs.com/package/drain-mcp