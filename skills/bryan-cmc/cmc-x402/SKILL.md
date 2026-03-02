---
name: cmc-x402
description: >
  通过 x402 每次请求付费协议访问 CoinMarketCap（CMC）的数据，并使用 USDC 进行支付。  
  适用于以下场景：  
  - 用户提到 x402 协议时；  
  - 用户希望获取 CMC 数据但无需 API 密钥；  
  - 用户询问关于按请求付费的 API 的信息；  
  - 用户需要将 CMC 与链上支付系统集成。  
  相关关键词：  
  x402、按请求付费、无需 API 密钥、USDC 支付、无需订阅即可获取 CMC 数据、/cmc-x402
homepage: https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap
source: https://github.com/coinmarketcap/skills-for-ai-agents-by-CoinMarketCap
user-invocable: true
---
# CoinMarketCap x402

这是一个基于x402协议的按请求计费的加密货币市场数据服务。您可以通过链上的USDC支付立即访问CoinMarketCap的API端点，无需API密钥或订阅。

## 什么是x402？

x402是由Coinbase开发的一种开放支付协议，它支持通过HTTP自动进行稳定币支付。您无需管理API密钥，只需在Base平台上为每个请求支付0.01美元的USDC费用。x402客户端库会自动处理支付签名流程。

了解更多信息：https://docs.x402.org

## 前提条件

在使用x402 API端点之前，请确保您满足以下条件：
1. 安装了Node.js 18及以上版本及npm。
2. 拥有一个您可以控制的Base网络钱包及其私钥。
3. 在Base平台上拥有足够的USDC用于支付请求费用（每个请求0.01美元）。
4. 拥有少量的ETH以支付网络交易手续费。

## 使用场景

- **获取特定加密货币的当前价格**：使用`/x402/v3/cryptocurrency/quotes/latest`接口，并提供货币符号或ID作为参数。例如：获取投资组合追踪器中BTC和ETH的价格。
- **列出排名前后的加密货币**：使用`/x402/v3/cryptocurrency/listing/latest`接口，并设置`limit`参数。例如：显示按市值排名前100的加密货币。
- **搜索DEX代币**：使用`/x402/v1/dex/search`接口，并提供关键词作为参数。例如：在不知道合约地址的情况下，通过名称查找某个memecoin。
- **获取DEX交易对的数据**：使用`/x402/v4/dex/pairs/quotes/latest`接口，并提供交易对地址。例如：监控某个Uniswap交易对的流动性和交易量。
- **访问AI代理的数据**：使用`https://mcp.coinmarketcap.com/x402/mcp`上的MCP接口。例如：让Claude或其他大型语言模型（LLM）自动获取实时加密货币数据。

## 快速入门

- 安装x402的TypeScript SDK：[安装指南](```bash
npm install @x402/axios @x402/evm viem
```)
- 使用自动支付功能获取数据：[使用示例](```typescript
import { createX402AxiosClient } from "@x402/axios";
import { ExactEvmScheme, toClientEvmSigner } from "@x402/evm";
import { privateKeyToAccount } from "viem/accounts";
import { createPublicClient, http } from "viem";
import { base } from "viem/chains";

// SECURITY: Never hardcode private keys in source code.
// Use environment variables: process.env.PRIVATE_KEY
// For production, use a dedicated hot wallet with limited funds.
const account = privateKeyToAccount(process.env.PRIVATE_KEY as `0x${string}`);
const publicClient = createPublicClient({ chain: base, transport: http() });
const signer = toClientEvmSigner(account, publicClient);

const client = createX402AxiosClient({
  schemes: [new ExactEvmScheme(signer)],
});

const response = await client.get(
  "https://pro.coinmarketcap.com/x402/v3/cryptocurrency/quotes/latest",
  { params: { symbol: "BTC,ETH" } }
);

console.log(response.data);
```)

## API端点

Base URL：`https://pro.coinmarketcap.com`

| API端点 | 路径 | 用途 |
|----------|------|---------|
| Quotes | `/x402/v3/cryptocurrency/quotes/latest` | 获取特定加密货币的当前价格 |
| Listings | `/x402/v3/cryptocurrency/listing/latest` | 获取按市值排名的加密货币列表 |
| DEX Search | `/x402/v1/dex/search` | 通过关键词搜索DEX代币 |
| DEX Pairs | `/x402/v4/dex/pairs/quotes/latest` | 获取DEX交易对的交易数据 |

所有标准CMC Pro API的参数都适用于x402 API端点。请参阅[endpoints.md](references/endpoints.md)以获取完整的参数参考信息。

## 用于AI代理的MCP接口

x402的MCP接口允许AI代理通过自动支付方式访问CoinMarketCap的数据。

- **连接URL**：[连接地址](```
https://mcp.coinmarketcap.com/x402/mcp
```)
- **传输方式**：支持Streamable HTTP（POST请求）

您可以使用任何支持x402协议的HTTP传输工具来连接该接口。服务器提供的工具与REST API端点相同，并支持自动发现相应的接口。

## 费用

在Base平台上，每个请求的费用为0.01美元（链ID：8453）。只有在数据成功传输后才会扣费；如果请求失败，则不会产生任何费用。

## 参考资料

- [endpoints.md](references/endpoints.md)：所有API端点的完整参数参考
- [payment-details.md](references/payment-details.md)：x402的响应格式、合约地址及手动集成指南

## 相关资源

- x402协议：https://x402.org
- x402官方文档：https://docs.x402.org
- x402 GitHub仓库：https://github.com/coinbase/x402
- CoinMarketCap API文档：https://coinmarketcap.com/api/documentation