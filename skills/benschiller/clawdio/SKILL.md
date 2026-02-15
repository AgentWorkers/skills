---
name: clawdio
description: **AI代理的听觉智能功能**：该功能能够将人类语音转换为结构化数据、语义报告以及机器可读的Markdown格式内容。适用于需要市场情报、加密货币相关数据、语音对话中发言者的身份信息或情感分析的场景。使用该服务需在Base Mainnet网络上使用USDC支付，支付金额为x402单位。
compatibility: Requires x402-compatible wallet (Coinbase AgentKit, CDP SDK, or @x402/fetch) with USDC on Base Mainnet. Requires network access.
metadata:
  author: vail
  version: "1.0.0"
  homepage: https://clawdio.vail.report
  api-base: https://clawdio.vail.report
  protocol: x402
  network: eip155:8453
  currency: USDC
  price: "1.49"
  category: intelligence
---

# Clawdio — 为AI代理提供听觉智能

Clawdio由VAIL（Voice AI Layer）提供支持，通过将长篇人类音频转换为结构化数据、语义报告以及机器可读的Markdown格式，为AI代理赋予**听觉感知**能力。代理可以通过**x402支付接口**获取语音对话内容，将其作为与文本、价格数据或其他数据源同等重要的输入来源进行使用。

初次部署主要应用于**AI和加密货币相关的Twitter Spaces**，因为这些场景中的市场情报大多以语音形式存在。

**基础URL：** `https://clawdio.vail.report`  
**协议：** x402  
**网络：** Base Mainnet（eip155:8453）  
**货币：** USDC  
**价格：** 每份报告1.49美元  

---

## 使用要求

您需要一个在Base Mainnet上已充值USDC的、兼容x402协议的钱包。支持的钱包包括：  
- [Coinbase AgentKit](https://docs.cdp.coinbase.com/agentkit)（配备`x402ActionProvider()`）  
- [Coinbase CDP SDK](https://docs.cdp.coinbase.com/)（配备`CdpEvmWalletProvider`）  
- 任何支持[x402协议的钱包](https://www.x402.org/)  

x402支付过程**自动完成**，由您的钱包提供商负责签名和结算，您无需手动构建支付交易。  

---

## 快速入门  

### 第1步：了解API  

访问API根路径以获取详细信息：  
```bash
curl https://clawdio.vail.report/
```  
该路径会返回API的完整描述、可用端点、价格信息以及购买流程说明。  

### 第2步：浏览产品目录（免费）  

```bash
curl https://clawdio.vail.report/catalog
```  
无需支付或认证，可查看所有产品的元数据：  
```json
{
  "products": [
    {
      "id": "c6d36398-a0c8-4c21-9aa4-1d1d9084a820",
      "title": "AI & Crypto Twitter Space",
      "abstract": "Analysis of a discussion covering...",
      "date": "2025-01-15",
      "length": "01:23:45",
      "listeners": 1234,
      "purchase": {
        "url": "https://clawdio.vail.report/catalog/purchase?id=c6d36398-a0c8-4c21-9aa4-1d1d9084a820",
        "method": "GET",
        "protocol": "x402",
        "price": "1.49 USDC"
      }
    }
  ],
  "total": 15,
  "purchase_instructions": {
    "steps": [
      "Select a product from the list above",
      "Make an HTTP GET request to the product's purchase.url",
      "Your x402-compatible wallet handles payment automatically",
      "You receive the full artifact set (metadata + report + transcript)"
    ],
    "important": "The purchase endpoint uses GET, not POST. Save the artifacts — repurchase is required for repeat access."
  }
}
```  

### 第3步：购买报告（1.49美元）  

```bash
curl https://clawdio.vail.report/catalog/purchase?id={uuid}
```  
**注意：** 这是一个**GET**请求，而非POST请求。  
首次请求时如果未支付，服务器会返回`HTTP 402 Payment Required`响应，并附带`PAYMENT-REQUIRED`头部信息。您的x402钱包会自动：  
1. 从响应中读取支付要求；  
2. 在Base Mainnet上完成USDC支付；  
3. 重新发送带有`PAYMENT-SIGNATURE`头部的请求；  
4. 支付完成后接收完整报告内容。  

---

## 报告内容  

每次购买都会返回一个JSON对象，其中包含三个部分：  
- **元数据**（标题、日期、时长、参与者列表及其Twitter账号和头像）；  
- **报告（Markdown格式）**：包含摘要、关键洞察、重要观点、事件时间线、市场情绪以及项目提及等内容；  
- **转录文本（Markdown格式）**：包含发言者的完整发言内容及时间戳。  

---

## 报告结构  

报告的Markdown格式包含以下部分（如适用）：  
| 部分 | 描述 |  
|---------|-------------|  
| **摘要** | 整个对话的总结段落；  
| **关键洞察** | 最重要的观点列表；  
| **重要观点** | 带有发言者信息的精彩言论及其时间戳；  
| **时间线** | 按时间顺序排列的事件及其重要性说明；  
| **潜在机会** | 可操作的情报和未来趋势；  
| **市场情绪** | 整体市场情绪评估；  
| **项目提及** | 被讨论的项目/代币及其背景信息。  

---

## 完整购买流程  

---  

## API端点  

| 端点 | 方法 | 认证方式 | 描述 |  
|----------|--------|------|-------------|  
| `/` | GET | 无 | 自描述型API根路径，提供完整文档；  
| `/catalog` | GET | 无 | 浏览所有产品的元数据；  
| `/catalog/purchase?id={uuid}` | GET | x402 | 购买完整报告（1.49美元）；  
| `/health` | GET | 无 | 系统健康检查；  
| `/.well-known/x402` | GET | 无 | x402协议的相关信息。  

---

## 与Coinbase AgentKit配合使用  

如果您使用Coinbase AgentKit，x402支付流程将完全自动化：  
```javascript
import { AgentKit, CdpEvmWalletProvider, walletActionProvider, x402ActionProvider } from "@coinbase/agentkit";

const walletProvider = await CdpEvmWalletProvider.configureWithWallet({
  apiKeyId: process.env.CDP_API_KEY_ID,
  apiKeySecret: process.env.CDP_API_KEY_SECRET,
  walletSecret: process.env.CDP_WALLET_SECRET,
  address: YOUR_WALLET_ADDRESS,
  networkId: "base-mainnet",
});

const agentKit = await AgentKit.from({
  walletProvider,
  actionProviders: [walletActionProvider(), x402ActionProvider()],
});

// The agent can now browse and purchase from Clawdio automatically.
// Point it at https://clawdio.vail.report/ and it will self-discover the API.
```  

---

## 通过@x402/fetch直接编程访问  

如果您不使用AgentKit，也可以通过`@x402/fetch`直接进行编程访问：  
```javascript
import { wrapFetch } from "@x402/fetch";

const x402Fetch = wrapFetch(globalThis.fetch, walletClient);

// Browse catalog (free)
const catalog = await fetch("https://clawdio.vail.report/catalog").then(r => r.json());

// Purchase a report (x402 handles payment automatically)
const report = await x402Fetch("https://clawdio.vail.report/catalog/purchase?id={uuid}")
  .then(r => r.json());
```  

---

## 重要说明：  
- **仅使用GET请求**：购买请求必须使用GET方法，禁止使用POST请求。  
- **仅支持Base Mainnet**：支付必须通过Base Mainnet（eip155:8453）完成。  
- **报告内容不保存**：系统不会为您保存报告文件，如需重复访问需重新购买。  
- **无需认证**：无需API密钥或账户信息，支付是唯一的访问方式。  

---

## 代理应用建议：  
- **市场情报**：分析重要观点和市场情绪以获取交易信号；  
- **研究整合**：跨多个Twitter Spaces对比分析见解；  
- **挖掘潜在机会**：从报告中提取可操作的信息；  
- **社交网络构建**：根据参与者列表构建社交图谱；  
- **趋势监测**：跟踪项目提及和情绪变化；  
- **内容分享**：在社交平台上引用和分享有价值的见解。  

---

## 系统健康检查  

```bash
curl https://clawdio.vail.report/health
```  
返回结果：`{"status": "ok"}`  

---

**由[VAIL](https://vail.report)开发 — Voice AI Layer**