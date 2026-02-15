# 获取eSIM服务

用户可以使用USDC在Base Mainnet（或用于测试的testnet）上，通过x402协议购买eSIM数据套餐。

## 说明

此服务允许AI代理为用户购买eSIM数据套餐。它使用x402支付协议，在Base Mainnet（默认）或Base Sepolia testnet（用于测试）上进行支付，然后提供eSIM安装页面。

**默认网络**：Base Mainnet（生产环境 - 使用真实eSIM）
**测试网络**：Base Sepolia（测试环境 - 使用模拟eSIM）

## 先决条件

- 在Base（Mainnet或Sepolia）上拥有支持USDC支付的钱包
- 具备足够的USDC余额用于购买
- 如果使用`transfer`方案，还需要ETH作为交易手续费

推荐的钱包：Coinbase Agentic Wallet、任何兼容x402的钱包，或支持Base USDC转账的钱包。

## 网络选择

默认情况下，购买操作在**Base Mainnet**（生产环境）上进行（使用真实eSIM）。如需测试，请明确指定测试网络。

### 各网络的使用场景

| 网络 | 使用场景 | eSIM类型 |
|---------|----------|-----------|
| **Base Mainnet**（默认） | 生产环境购买 | 使用真实eSIM |
| **Base Sepolia** | 开发/测试 | 使用模拟eSIM |

### 指定网络

用户可以通过以下方式指定网络：
- 输入“testnet”、“testing”、“mock”或“demo” → 使用Sepolia测试网络
- 未指定或输入“mainnet”、“production”、“real” → 使用Base Mainnet（默认）

## 调用方式

当用户出现以下情况时，可以使用此服务：
- 请求eSIM或移动数据
- 需要旅行时的蜂窝数据
- 希望为特定国家购买数据套餐
- 表示需要海外连接
- 请求用于开发的“test”或“mock”eSIM

## 重要提示：交易时间

加密货币和eSIM交易并非即时完成。请注意：
- **USDC转账**：链上确认需要5-15秒
- **购买完成**：API需要额外3-30秒来验证链上的交易
- **整个购买流程**：从支付发起到eSIM交付可能需要30-60秒

请告知用户购买正在处理中，请等待确认。

## 工作流程

1. **确定网络**：询问用户是否需要Mainnet（生产环境）或testnet（测试环境）
2. **了解需求**：询问用户需要数据的国家
3. **搜索套餐**：查询esimqr.link以获取可用套餐
4. **展示选项**：显示可用的数据套餐及其价格
5. **用户选择套餐**：用户挑选一个套餐
6. **确认购买**：显示价格、网络（Mainnet/testnet）和钱包余额，并获取用户确认
7. **执行x402支付流程**：
   - 向 `/api/agent/purchase`（Mainnet）或 `/api/agent-testnet/purchase`（testnet）发送POST请求 → 接收到包含支付详情的402响应
   - 使用钱包完成支付
   - 重新发送POST请求，并添加`PAYMENT-SIGNATURE`头部
8. **提供eSIM信息**：返回`esimPageUrl`——一个包含二维码和安装按钮的用户友好页面

## 示例对话

### Mainnet（使用真实eSIM）
```
User: I need an eSIM for my trip to USA

Agent: I can help you get an eSIM! This will be a real eSIM on Base Mainnet.

[Agent searches packages]

I found these options for USA:
- US_100MB_7: 100MB / 7 Days - $0.50
- US_1_7: 1GB / 7 Days - $1.18
- US_3_7: 3GB / 7 Days - $2.50
- US_5_30: 5GB / 30 Days - $4.42

Which package would you like?

User: 1GB 7 days

Agent: The US 1GB 7-Day plan costs $1.18 USDC on Base Mainnet.

My wallet balance: $30.00 USDC

Shall I purchase this eSIM now?

User: Yes

Agent: Initiating purchase on Base Mainnet...

✓ Payment sent: 1.18 USDC
✓ Transaction: 0xabc123...

Your eSIM is ready! Install it here:
https://esimqr.link/web3/esim/agent_1707184523_abc123
```

### Testnet（使用模拟eSIM进行测试）
```
User: Get me a test eSIM for USA

Agent: I'll get you a test eSIM on Base Sepolia testnet (mock eSIM for testing).

[Agent searches packages on testnet]

I found test packages for USA:
- US_1_7: 1GB / 7 Days - $1.18 (testnet)
- US_5_30: 5GB / 30 Days - $4.42 (testnet)

Which would you like?

User: 1GB

Agent: The US 1GB 7-Day test plan costs $1.18 testnet USDC.

My wallet balance: 10.00 testnet USDC

Shall I purchase this test eSIM?

User: Yes

Agent: Initiating testnet purchase...

✓ Test payment sent: 1.18 USDC
✓ Transaction: 0xdef456...

Your mock eSIM is ready! (For testing only):
https://esimqr.link/web3/esim/mockagent_1707184523_abc123
```

## API接口

基础URL：`https://esimqr.link`

### Mainnet接口（生产环境）
| 接口 | 方法 | 说明 |
|----------|--------|-------------|
| `/api/agent/quote` | GET | 获取价格报价 |
| `/api/agent/purchase` | POST | 启动/完成购买 |
| `/api/agent/esim/{id}` | GET | 获取eSIM状态 |

### Testnet接口（测试环境）
| 接口 | 方法 | 说明 |
|----------|--------|-------------|
| `/api/agent-testnet/quote` | GET | 获取价格报价 |
| `/api/agent-testnet/purchase` | POST | 启动/完成购买 |
| `/api/agent-testnet/esim/{id}` | GET | 获取eSIM状态 |

### 共享接口（两种网络均可使用）
| 接口 | 方法 | 说明 |
|----------|--------|-------------|
| `/api/web3/packages?q={country}` | GET | 搜索套餐 |

### 速率限制

- **限制**：每分钟每个IP地址最多10次请求
- **响应**：返回HTTP 429错误，并附带`Retry-After`头部
- 请根据`Retry-After`值优雅地处理速率限制

## 网络配置

### Base Mainnet（默认设置）
| 参数 | 值 |
|-----------|-------|
| Network | Base Mainnet |
| Chain ID | 8453 |
| CAIP-2 | eip155:8453 |
| USDC Token | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| USDC 小数位数 | 6 |

### Base Sepolia（测试环境）
| 参数 | 值 |
|-----------|-------|
| Network | Base Sepolia（测试环境） |
| Chain ID | 84532 |
| CAIP-2 | eip155:84532 |
| USDC Token | `0x036CbD53842c5426634e7929541eC2318f3dCF7e` |
| USDC 小数位数 | 6 |

**注意**：支付钱包地址由API在报价和402响应中动态生成。切勿硬编码钱包地址。

## 支付方式（x402）

402响应中的`accepts`数组提供了两种支付选项。根据您的钱包功能进行选择：

| 支付方式 | 头部信息 | 需要的钱包支持 | 手续费（gas） |
|--------|--------|---------------------|-----|
| `exact` | `PAYMENT-SIGNATURE` | 支持EIP-3009签名的钱包（如Circle、x402兼容的SDK） | 无需支付手续费 |
| `transfer` | `X-PAYMENT` | 标准的USDC转账 | 需要用户支付手续费 |

### 选择哪种支付方式

- **使用`exact`方式**：如果您的钱包支持EIP-3009 `transferWithAuthorization`签名（例如Circle钱包、x402兼容的SDK）。优点：无需支付手续费，由平台代为完成交易。
- **使用`transfer`方式**：如果您的钱包支持标准USDC转账但不支持EIP-3009。适用于所有支持Base网络的钱包。用户需要支付手续费。
- **不确定如何选择？**：`transfer`方式适用于所有支持USDC支付的钱包。

### 使用`exact`方式的流程（无需支付手续费）：
1. 向 `/api/agent/purchase`（Mainnet）或 `/api/agent-testnet/purchase`（testnet）发送POST请求 → 接收到包含EIP-3009参数的402响应
2. 签署`transferWithAuthorization`消息（无需链上交易）
3. 重新发送POST请求，并添加`PAYMENT-SIGNATURE: <base64-encoded-payload>`头部
4. 平台会代为完成交易

### 使用`transfer`方式的流程：
1. 向 `/api/agent/purchase`（Mainnet）或 `/api/agent-testnet/purchase`（testnet）发送POST请求 → 接收到包含支付详情的402响应
2. 在正确的网络上将USDC转账到`payTo`地址
3. 重新发送POST请求，并添加`X-PAYMENT: txHash=0x..., nonce=...`头部

## API响应示例

### 搜索套餐
```json
GET /api/web3/packages?q=US

{
  "packages": [
    {"packageCode": "US_1_7", "name": "United States 1GB 7Days", ...}
  ]
}
```

### 获取价格报价（Mainnet）
```json
GET /api/agent/quote?packageCode=US_1_7

{
  "packageCode": "PHAJHEAYP",
  "slug": "US_1_7",
  "planName": "United States 1GB 7Days",
  "usdcAmount": "1.18",
  "paymentDetails": {
    "recipient": "<payment-address-from-api>",
    "chainId": 8453,
    "network": "eip155:8453"
  }
}
```

### 获取价格报价（Testnet）
```json
GET /api/agent-testnet/quote?packageCode=US_1_7

{
  "packageCode": "PHAJHEAYP",
  "slug": "US_1_7",
  "planName": "United States 1GB 7Days",
  "usdcAmount": "1.18",
  "paymentDetails": {
    "recipient": "<payment-address-from-api>",
    "chainId": 84532,
    "network": "eip155:84532"
  },
  "isTestnet": true
}
```

### 需要支付（使用402协议）
```json
POST /api/agent/purchase
Body: {"packageCode": "US_1_7"}

{
  "x402Version": 2,
  "accepts": [
    {"scheme": "exact", ...},
    {"scheme": "transfer", "amount": "1180000", "payTo": "<payment-address-from-api>", "extra": {"nonce": "abc123"}}
  ]
}
```

**重要提示**：始终使用402响应中的`payTo`地址。切勿硬编码支付地址。

### 购买成功
```json
POST /api/agent/purchase
Headers: X-PAYMENT: txHash=0x...,nonce=abc123
Body: {"packageCode": "US_1_7"}

{
  "success": true,
  "esimId": "agent_1707184523_abc123",
  "esimPageUrl": "https://esimqr.link/web3/esim/agent_1707184523_abc123",
  "esimDetails": {
    "iccid": "8901234...",
    "activationCode": "LPA:1$..."
  }
}
```

## 状态码

- `pending`：订单已创建，正在准备中
- `processing`：eSIM正在配置中
- `ready`：eSIM已准备好安装
- `activated`：eSIM已安装到设备上
- `failed`：订单失败（请联系支持）
- `cancelled`：模拟eSIM自动取消（仅限测试环境）

## 文档链接

- **Mainnet**：https://esimqr.link/api/agent/docs
- **Testnet**：https://esimqr.link/api/agent-testnet/docs
- **用户指南**：https://esimqr.link/agents

## 相关文件

- `esim_api.py`：用于esimqr.link的API客户端（支持Mainnet和testnet）

## 依赖项
```
requests>=2.28.0
```

## 需要提交的资料（用于黑客马拉松）

- **项目跟踪链接**：Agenic Commerce
- **使用的协议**：x402（需要使用HTTP 402支付）
- **支持的网络**：Base Mainnet（生产环境）、Base Sepolia（测试环境）
- **支付方式**：USDC

提交链接：https://www.moltbook.com/m/usdc