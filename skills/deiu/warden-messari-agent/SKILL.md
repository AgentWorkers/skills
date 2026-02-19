---
name: warden-messari-agent
description: 通过 Warden 协议与 Messari Deep Research 代理进行通信。该协议支持点对点（A2A）通信、JSON-RPC 2.0 格式的任务消息传递、在 Base 和 Solana 上使用 x402 协议进行 USDC 微支付，以及基于 ERC-8004 标准的链上身份验证。查询代理信息无需 API 密钥；所有支付操作均根据请求通过 x402 协议进行处理。
---
# Messari Agent通信指南

Warden提供的Messari Agent是一个加密研究代理，它利用Messari的定量和定性数据来回答关于资产、协议和项目的相关自然语言查询。该代理通过JSON-RPC 2.0协议进行A2A（代理对代理）通信，并且每次请求会收取x402 USDC的微支付费用。

**基础URL**: `https://messari.agents.wardenprotocol.org`

## 快速参考

| 操作 | 方法 | 端点 |  
|--------|--------|----------|  
| 查看代理功能 | `GET` | `/.well-known/agent-card.json` |  
| 验证链上身份 | `GET` | `/.well-known/agent-registration.json` |  
| 发送查询（A2A） | `POST` (JSON-RPC) | `/` |  
| 发送流式查询 | `POST` (JSON-RPC, SSE) | `/` |  

## 代理功能

- **输入**：仅支持文本（关于加密货币的自然语言问题）  
- **输出**：文本格式的响应（markdown格式）  
- **流式传输**：当前版本不支持  
- **多轮对话**：不支持（每个请求都是独立的）  
- **支付**：每次请求收取x402 USDC微支付（基础主网费用为0.25美元）  
- **支持领域**：加密货币、DeFi、金融、投资服务、市场研究  
- **技能**：知识综合、问答、事实提取、搜索、文档质量检查、推理与演绎  

## 第1步：发现代理  

在发送查询之前，先获取代理信息以确认其功能及支付要求。  

**响应内容示例**：  
响应中包含`authentication.schemes: ["x402"]`以及一个`x402`字段，其中包含费用、网络和货币信息。解析这些字段以确定是否需要支付以及费用金额。  

**代理信息中的关键字段**：  
| 字段 | 值 | 说明 |  
|-------|-------|---------|  
| `url` | `https://messari.agents.wardenprotocol.org` | 所有请求的基础URL |  
| `capabilities.streaming` | `false` | 不支持流式传输 |  
| `capabilities.multiTurn` | `false` | 不支持多轮对话 |  
| `authentication.schemes` | `["x402"]` | 支付方式 |  
| `x402.network` | `eip155:8453` | 基础主网 |  
| `x402.price` | `"0.25"` | 每次请求的费用（USDC） |  

## 第2步：发送查询（A2A协议）  

所有查询都通过`POST /`使用A2A JSON-RPC 2.0协议进行。请求方法为`message/send`。  

### 请求格式示例  

**无支付请求的curl示例**：  
如果启用了支付功能，此请求会返回402错误。适用于测试连接性。  

**成功响应示例**：  

**错误响应示例**：  

### 任务状态  

响应中的`status.state`字段表示任务进度：  
| 状态 | 含义 |  
|-------|----------|---------|  
| `submitted` | 未提交 | 任务已接收，正在排队 |  
| `working` | 处理中 | 代理正在处理 |  
| `completed` | 完成 | 响应已准备好，可在`history`中查看 |  
| `failed` | 失败 | 发生错误 |  
| `cancelled` | 取消 | 任务被取消 |  
| `rejected` | 被拒绝 | 任务被拒绝 |  

由于该代理不支持流式传输或多轮对话，因此通常会收到`state: "completed"`或`state: "failed"`的响应。  

### 消息结构  

消息中的`parts`数组使用`type`或`kind`作为区分符：  
- `text`：`{"type": "text", "text": "..."}`：自然语言文本  
- `file`：`{"type": "file", "file": {"url": "...", "mimeType": "..."}}`：文件引用  
- `data`：`{"type": "data", "data": {...}}`：结构化JSON数据  

该代理仅接受并返回`text`类型的消息。  

## 第3步：处理x402支付  

当支付功能启用时，如果未包含有效的支付头部信息，`POST /`请求会返回HTTP 402错误。  

**支付流程**：  
1. 发送不包含支付头部的`POST /`请求  
2. 收到带有`PAYMENT-REQUIRED`响应头（Base64编码的JSON）的402错误  
3. 解码头部信息以获取支付详情（网络、金额、收款地址）  
4. 创建一个签名的EIP-3009授权信息（无需支付手续费；由第三方代理在链上完成转账）  
5. 重新发送请求，并在`X-PAYMENT`头部中包含签名后的数据  
6. 收到包含代理响应的HTTP 200响应以及`X-PAYMENT-RESPONSE`头部（其中包含结算参考信息）  

### 402响应头部示例  

**解码后的`PAYMENT-REQUIRED`字段示例**：  

### 构建支付头部信息  

对于EVM网络（基础主网），支付使用EIP-3009协议（基于USDC合约）：  
1. 解析`PAYMENT-REQUIRED`头部并选择合适的支付选项  
2. 构建一个EIP-712格式的数据结构，包含`from`、`to`、`value`、`validAfter`、`validBefore`和`nonce`字段  
3. 用客户端钱包的私钥对数据签名  
4. 将签名后的数据编码为Base64格式  
5. 将签名后的数据添加到`X-PAYMENT`头部中（格式为`X-PAYMENT: <base64-payload>`）  

客户端无需直接提交区块链交易；支付过程由第三方代理在链上完成。  

### 客户端库  

使用官方的x402客户端库来自动处理支付相关操作：  

### 支持的支付网络  

| 网络 | 链路ID | USDC合约 | 支付代理 |  
|---------|----------|---------------|-------------|  
| 基础主网 | `eip155:8453` | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` | `https://facilitator.payai.network` |  
| 基础Sepolia（测试网） | `eip155:84532` | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` | `https://x402.org/facilitator` |  
| Solana主网 | `solana:5eykt4UsFv8P8NJdTREpY1vzqKqZKvdp` | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | `https://facilitator.payai.network` |  
| Solana开发网 | `solana:EtWTRABZaYq6iMfeYKouRu166VU2xqa1` | （开发网USDC） | `https://x402.org/facilitator` |  

该代理目前支持基础主网（`eip155:8453`），费用为每次请求0.25美元。请查看代理信息以获取最新价格和可用网络列表。  

### CORS头部信息  

当从浏览器发起请求时，代理会返回以下CORS头部信息：  

## 第4步：验证链上身份（ERC-8004）  

该代理在多个链上注册了ERC-8004身份信息。可以通过获取注册文件并与链上数据进行比对来验证其身份。  

**获取注册信息示例**：  

**注册字段**：  
| 字段 | 值 |  
|-------|-------|  
| `type` | `https://eips.ethereum.org/EIPS/eip-8004#registration-v1` |  
| `name` | Messari Agent by Warden |  
| `active` | `true` |  
| `x402Support` | `true` |  
| `supportedTrust` | `["reputation"]` |  

**链上注册信息**：  
| 链路 | 代理ID | 注册合约 |  
|-------|----------|-------------------|  
| 基础Sepolia | 853 | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |  
| 基础主网 | 18096 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |  
| Ethereum主网 | 25490 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |  

**验证链上身份示例**：  
返回的URI应与`https://messari.agents.wardenprotocol.org/agent-registration.json`匹配。如果匹配，则说明提供代理信息的域名与链上注册的域名一致，从而确认代理的真实性。  

## JSON-RPC错误代码  

| 代码 | 含义 |  
|------|---------|  
| `-32700` | 解析错误（JSON格式无效） |  
| `-32600` | 请求无效（JSON-RPC格式错误） |  
| `-32601` | 方法未找到 |  
| `-32602` | 参数无效 |  
| `-32603` | 内部服务器错误 |  
| `-32001` | 任务未找到 |  
| `-32002` | 任务已被取消 |  

## 示例查询**：  
适用于该代理的查询示例：  
- “以太坊的当前市值和24小时交易量是多少？”  
- “总结DeFi领域的近期融资活动”  
- “未来30天内Solana有哪些代币即将解锁？”  
- “比较Aave和Compound在过去一年的TVL增长情况”  
- “Messari的最新研究对Layer 2扩展技术有何看法？”  

代理返回的响应为markdown格式。请勿修改响应中的链接或URL。  

## 故障排除：  

- **HTTP 402：需要支付**：支付功能已启用。请在请求中包含有效的`X-PAYMENT`头部及签名的EIP-3009授权信息，或使用`@x402/client`库自动处理支付。  
- **响应为空或无内容**：确保消息中的`parts`数组不为空，且至少有一个`type: "text"`类型的字段包含有效文本。  
- **连接被拒绝**：代理通过反向代理运行，请确认请求URL为`https://messari.agents.wardenprotocol.org`（使用HTTPS协议）。  
- **任务状态为“失败”**：可能是Messari AI后端出现错误，请重新尝试请求。如果问题持续，请检查代理的健康检查端点（仅限内部使用）。  

## 相关资源：  
- A2A协议规范：https://google.github.io/A2A（用于代理互操作的JSON-RPC消息格式）  
- x402支付协议：https://x402.org（基于HTTP的微支付方案）  
- ERC-8004身份注册表：https://eips.ethereum.org/EIPS/eip-8004（用于链上代理身份验证）  
- Warden协议：https://wardenprotocol.org（代理基础设施提供商）  
- Messari：https://messari.io（加密研究与数据平台）  
- x402客户端库：https://www.npmjs.com/package/@x402/client（用于Node.js的自动支付处理库）