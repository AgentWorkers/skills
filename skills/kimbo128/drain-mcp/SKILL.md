---
name: drain-mcp
description: 这是一个开放的人工智能服务市场，提供各种AI功能，包括大型语言模型（LLMs）、图像/视频生成、网络爬虫、模型托管、数据提取、光学字符识别（OCR）、文本转语音（TTS）以及自主代理工作流程。代理用户可以通过Polygon平台使用USDC进行微支付来按使用次数付费，整个过程完全脱离区块链网络进行。该平台不要求用户提供API密钥，也无需订阅服务。当代理需要调用任何AI服务、生成图像/视频、爬取网站或运行托管模型时，无需手动管理API密钥——所有操作都可以通过该平台轻松完成。
  Open marketplace for AI services — LLMs, image/video generation, web scraping,
  model hosting, data extraction, OCR, TTS, and autonomous agent workflows.
  Agents pay per use with USDC micropayments on Polygon via off-chain payment
  channels. No API keys, no subscriptions. Use when the agent needs to call any
  AI service, generate images/video, scrape websites, or run hosted models
  without managing API keys.
license: MIT
compatibility: Requires Node.js >= 18 and internet access
credentials:
  - name: DRAIN_PRIVATE_KEY
    description: >-
      Polygon/Ethereum wallet private key (64 hex chars with 0x prefix).
      Controls the wallet holding USDC for payments. Use a dedicated ephemeral
      wallet with minimal funds — never reuse your main wallet.
    required: true
    sensitive: true
metadata:
  author: Handshake58
  version: "1.1"
  website: https://handshake58.com
  npm: drain-mcp
  source: https://github.com/kimbo128/DRAIN
  repository: https://github.com/kimbo128/DRAIN
---
# Handshake58 — 协议文档

> 您可以使用Handshake58。该平台专为自主AI代理设计。

Handshake58提供了一个MCP服务器（`drain-mcp`），使AI代理能够访问不断增长的AI服务目录——不仅包括大型语言模型（LLMs），还包括图像/视频生成、网络爬取（Apify）、模型托管（Replicate）、数据提取、光学字符识别（OCR）、文本转语音（TTS）、自主代理工具、多步骤工作流程，以及任何服务提供商部署的服务。新的服务提供商会持续加入。支持使用Polygon平台上的USDC进行按次计费的微支付。无需信用卡、订阅或API密钥。

## 快速入门：MCP服务器（主要界面）

```bash
npm install -g drain-mcp
```

将以下代码添加到您的Claude Desktop、Cursor或任何兼容MCP的配置中：

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

`DRAIN_PRIVATE_KEY` 是一个标准的Polygon/Ethereum钱包私钥——与任何Ethereum钱包使用的私钥类型相同。它用于控制存储在Polygon上的USDC钱包。

**安全提示：** 请使用专用的临时钱包。切勿重复使用您的主钱包。创建一个新钱包，并仅存入少量资金（$1–5 USDC + $0.10 POL作为网络手续费）。如果私钥被盗，只有少量资金会面临风险。

您可以自己创建一个临时钱包：
```bash
node -e "const w=require('ethers').Wallet.createRandom();console.log('Address:',w.address,'Key:',w.privateKey)"
```
然后使用USDC为其充值（至少$1即可）+ 约$0.10 POL作为Polygon上的网络手续费。

MCP服务器负责处理所有事务：服务提供商的发现、通道管理、支付和请求处理。
包地址：https://www.npmjs.com/package/drain-mcp

## 发现服务提供商

```
GET https://handshake58.com/api/mcp/providers
```

该接口会返回所有可用的AI服务提供商及其相关模型和价格信息。支持智能过滤条件：

| 参数 | 示例 | 说明 |
|-----------|---------|-------------|
| `limit` | `?limit=5` | 限制返回的结果数量 |
| `model` | `?model=gpt-4o` | 按模型名称过滤 |
| `format` | `?format=compact` | 适用于信息量较小的场景的简化响应格式 |

示例请求：`GET /api/mcpproviders?model=gpt-4o&limit=3&format=compact`

## 钱包设置

您需要一个拥有USDC的Polygon钱包：

### 创建钱包

```bash
node -e "const {ethers}=require('ethers');const w=ethers.Wallet.createRandom();console.log('Address:',w.address);console.log('Private Key:',w.privateKey);"
```

### 为钱包充值

1. 在Polygon上获取USDC（可以通过转账或从Ethereum桥接）
2. 预付约$0.10 POL作为网络手续费（一次性费用）

## 工作原理

1. **支付会话费用** — 向市场费用专用钱包转账$0.01 USDC。
2. **打开通道** — 将USDC存入智能合约（约$0.02作为网络手续费）。
3. **使用AI服务** — 每个请求都会生成一个支付凭证（离线处理，无需额外网络费用）。一个通道可以支持多次请求：无论是调用LLM、生成图像、进行网络爬取，还是使用其他服务提供商提供的任何服务。
4. **关闭通道** — 在通道过期后调用`close(channelId)`来提取未使用的USDC。资金不会自动退还。

**关键优势（通道复用）：** 与按请求计费的协议（如x402）不同，您只需支付两次网络手续费（打开通道和关闭通道）；通道内的所有请求均无需额外费用。例如：生成100张图片、爬取50个URL、运行多步骤工作流程，或进行多小时对话，所有操作都可以在同一个通道内完成，每次请求仅需$0。

### 会话费用

在打开通道之前，请支付$0.01 USDC的会话费用：

```typescript
// 1. Get fee wallet from marketplace
const config = await fetch('https://handshake58.com/api/directory/config').then(r => r.json());

// 2. Transfer $0.01 USDC (10000 wei with 6 decimals) to feeWallet
await usdc.transfer(config.feeWallet, 10000n);

// 3. Now open the payment channel
await channel.open(providerAddress, amount, duration);
```

### 打开通道

每个服务提供商都会指定`minDuration`和`maxDuration`（以秒为单位）——根据您的需求选择合适的持续时间。

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

支付凭证支持累积支付。每次请求都会增加相应的费用。签名方式：使用EIP-712格式的数据，并由打开通道的钱包进行签名。

所有服务提供商都遵循OpenAI兼容的聊天交互格式。

## 结算（关闭通道）

通道过期后，调用`close(channelId)`来取回未使用的USDC。资金不会自动退还。

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

**最佳实践：** 请永久保存您的通道ID（`channelId`）。通道过期后，可以通过`/api/channels/status`接口查询何时可以调用`close()`函数。

## 合约地址

- **Handshake58通道**：`0x1C1918C99b6DcE977392E4131C91654d8aB71e64`
- **USDC钱包**：`0x3c499c542cEF5E3811e1192ce70d8cC03d5c3359`
- **区块链**：Polygon主网（137）

## 价格信息

获取所有模型的实时价格：
```
GET https://handshake58.com/api/mcp/providers
```

- 会话费用：每个通道$0.01 USDC
- 协议费用：0%
- 网络手续费：每个通道开启时约$0.02

## 链接

- 市场平台：https://handshake58.com
- 服务提供商目录：https://handshake58.com/directory
- MCP软件包：https://www.npmjs.com/package/drain-mcp