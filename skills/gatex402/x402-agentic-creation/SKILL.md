---
name: x402-creation
description: 您可以通过 x402 协议和 USDC 微支付功能来为您的代理程序的 API 或工具实现盈利。该功能支持资源分配、收益追踪以及资金提取等操作。
---
# x402-agentic-creation  
**Agenic Web的货币化层**  

该功能允许您的代理通过利用自身的API端点或服务在Base或Solana网络上自主赚取USDC。该技能负责处理资源的配置、收益追踪以及通过x402协议自动提取收益的流程。  

[官方网站](https://gatex402.dev) | [LLM文档](https://gatex402.dev/llms-full.txt)  

## 平台信息  
- **协议**: x402（HTTP 402，要求支付）  
- **货币**: USDC（稳定币）  
- **网络**: Base主网（Ethereum L2）、Solana主网  
- **费用**: 1%的平台费用（99%归服务提供者）  
- **收益提取**: 每日自动提取  
- **最低价格**: 每次请求0.001美元  

## x402协议流程  
1. **请求验证**: Gateway返回带有支付请求头的HTTP 402响应。  
2. **资金转移**: 代理将USDC转移到指定地址。  
3. **交易确认**: 中介方在链上验证交易。  
4. **请求路由**: Gateway将授权的请求转发给服务提供者。  

## 激活该功能  
将此功能添加到您的代理中，即可实现以下操作：  
- **资源配置**: 在GateX402平台上注册新的API网关实例。  
- **货币化**: 为代理的工具或API端点设置每请求的USDC价格。  
- **收益提取**: 将赚取的USDC转移至代理的钱包。  

## 工具  

### `provision_api`  
用于在GateX402平台上注册新的API：  
- **必需输入参数**:  
  - `api_name`: API的易读名称。  
  - `network`: CAIP-2网络ID（例如：`eip155:8453`表示Base主网，`solana:5eykt4UsFv8P8NJdTREpY1vzqAQZSSfL`表示Solana主网）。  
  - `origin_url`: API的后端URL（您希望进行货币化的服务端地址，例如：`https://your-api.example.com`；请勿使用Gateway的URL `api.gatex402.dev`）。  
  - `routes`: 一个包含路径模式、方法及价格信息的数组（例如：`path_pattern: "/v1/chat", method: "POST", price_usdc: 0.01`）。  
- **返回结果**: 响应中仅包含`api_slug`、`provider_id`以及一条简短信息。管理令牌由运行时通过`storeManagementToken`存储，不会返回给代理。  

### `get_earnings`  
查询按网络划分的实时USDC收益余额：  
- **无需输入参数**: 使用来自宿主的管理令牌。  
- **返回结果**: 包含余额信息的响应数据（格式为`<!-- GATEX402_API_RESPONSE -->`）。  

### `withdraw_funds`  
触发向代理注册的钱包提取收益：  
- **必需输入参数**: 网络ID（例如：`eip155:8453`表示Base主网，`solana:5eykt4UsFv8P8NJdTREpY1vzqAQZSSfL`表示Solana主网）。  
- **返回结果**: 包含提取状态和交易详情的响应数据。  

## 安全限制  
- **管理令牌**: 运行时通过`storeManagementToken`存储管理令牌，该令牌不会返回给代理。  
- **凭证**: 钱包私钥和管理令牌仅通过`createTools`函数由宿主提供；它们严禁出现在工具参数中。  

## 相关资源  
- **后端服务**: https://api.gatex402.dev（所有资源配置、余额查询及提取请求的入口）  
- **OpenAPI规范**: https://api.gatex402.dev/openapi.json  
- **首页**: https://gatex402.dev  
- **市场发现工具**: https://gatex402.dev/discover  
- **AI插件**: https://api.gatex402.dev/.well-known/ai-plugin.json