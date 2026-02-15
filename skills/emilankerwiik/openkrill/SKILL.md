---
name: openkrill
description: **启用AI代理通过x402协议进行微支付**  
适用于在Browserbase上购买浏览器会话、使用Firecrawl进行数据抓取，或与任何支持x402协议的API进行交互的场景。该功能涵盖钱包创建、资金充值以及自动支付流程的管理。
license: MIT
compatibility: Requires network access and thirdweb API key (THIRDWEB_SECRET_KEY environment variable)
metadata:
  author: emilankerwiik
  version: "1.2"
  openclaw:
    requires:
      env:
        - THIRDWEB_SECRET_KEY
    primaryEnv: THIRDWEB_SECRET_KEY
---

# OpenKrill - x402支付技能

此技能使AI代理能够使用x402协议自主进行微支付。它负责钱包管理、余额检查以及在API返回HTTP 402 “Payment Required”（需要支付）响应时自动执行支付流程。

## 何时使用此技能

- **当用户询问“我可以购买哪些服务？”或“有哪些可用的x402 API？”时**——请先查询Bazaar！
- 在Browserbase上购买浏览器自动化会话时
- 使用Firecrawl执行网络爬取任务时
- 当代理需要创建用于注册或验证的电子邮件地址时
- 与任何支持x402的API交互时
- 当用户提到微支付、加密货币支付或API访问费用时
- 当遇到402 “Payment Required”响应时
- **通过Bazaar发现新的支持x402的服务时**

> **提示：** 当用户或代理询问可购买的服务时，始终先查询Bazaar发现端点。它提供了包含12,000多种支持x402的服务的实时、最新目录。

### 快速：发现可用服务

```bash
# Query the Bazaar to see what's available (no auth required)
curl -s "https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources?type=http&limit=50"
```

## 先决条件

在使用此技能之前，请确保：
1. `THIRDWEB_SECRET_KEY`环境变量已设置，并使用有效的thirdweb项目密钥
2. 钱包在Base链（或目标链）上有足够的USDC余额
3. 具备访问thirdweb API端点的网络权限

## 重要提示：x402端点URL和服务类型

### 两种类型的x402支持

| 类型 | 描述 | 示例 |
|------|-------------|---------|
| **真正的x402** | 完全无需API密钥——只需支付即可使用 | Browserbase |
| **混合x402** | 需要API密钥/令牌 + 支付头部信息 | Firecrawl |

### x402端点模式

| 服务 | 标准API | x402端点 | 类型 | 状态 |
|---------|-------------|---------------|------|--------|
| Browserbase | `api.browserbase.com` | `x402.browserbase.com` | 真正的x402 | ✅ 可用 |
| Firecrawl | `api.firecrawl.dev/v1/search` | `api.firecrawl.dev/v1/x402/search` | 非标准 | ❌ 无法使用 |

**发现提示：**
- 查看是否包含`x402.`子域名（例如，`x402.browserbase.com`）
- 检查路径中是否包含 `/x402/`（例如，`/v1/x402/search`）
- 访问x402根URL以获取端点列表（例如，`curl https://x402.browserbase.com/`）

## 核心工作流程

### 第1步：检查或创建钱包

直接使用thirdweb API（推荐）：

```bash
curl -s -X POST https://api.thirdweb.com/v1/wallets/server \
  -H "Content-Type: application/json" \
  -H "x-secret-key: $THIRDWEB_SECRET_KEY" \
  -d '{"identifier": "x402-agent-wallet"}'
```

响应中将包含钱包地址。请将其保存以供后续操作使用。

### 第2步：使用`fetchWithPayment`进行支付

直接调用thirdweb x402 fetch API：

```bash
# Browserbase - Create browser session
curl -s -X POST "https://api.thirdweb.com/v1/payments/x402/fetch?url=https://x402.browserbase.com/browser/session/create&method=POST" \
  -H "Content-Type: application/json" \
  -H "x-secret-key: $THIRDWEB_SECRET_KEY" \
  -d '{"browserSettings": {"viewport": {"width": 1920, "height": 1080}}}'
```

### 第3步：处理响应

**成功：** API会直接返回会话数据。

**资金不足：** 如果钱包需要充值，API会返回相应的提示：

```json
{
  "result": {
    "message": "This endpoint requires 0.002 USDC on chain id 8453...",
    "link": "https://thirdweb.com/pay?chain=8453&receiver=0x...&token=0x..."
  }
}
```

**当您收到支付链接时，在用户的浏览器中打开它：**

- 如果支持浏览器自动化（如MCP、浏览器工具等），使用它们在新标签页中打开链接
- 否则，显眼地显示链接并指导用户手动打开

这将打开thirdweb的支付页面，用户可以在该页面为钱包充值。

## API参考

### `fetchWithPayment`端点

**URL：** `https://api.thirdweb.com/v1/payments/x402/fetch`

**方法：** POST

**查询参数：**
| 参数 | 是否必填 | 描述 |
|-----------|----------|-------------|
| `url` | 是 | 需要调用的目标API URL |
| `method` | 是 | HTTP方法（GET、POST等） |
| `from` | 否 | 用于支付的钱包地址（如果省略则使用默认项目钱包） |
| `maxValue` | 否 | 最大支付金额（单位：wei） |
| `asset` | 否 | 支付令牌地址（默认为USDC） |
| `chainId` | 否 | 支付的链ID（例如，Base链的“eip155:8453”） |

**头部信息：**
- `x-secret-key`：您的thirdweb项目密钥（必填）
- `Content-Type`：application/json

## 支持的x402服务

### Browserbase

**x402端点：** `https://x402-browserbase.com`  
**定价：** 每小时0.12美元（以USDC在Base链上支付）

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/browser/session/create` | POST | 创建浏览器会话 |
| `/browser/session/:id/status` | GET | 检查会话状态 |
| `/browser/session/:id/extend` | POST | 延长会话时间 |
| `/browser/session/:id` | DELETE | 终止会话 |

```bash
curl -s -X POST "https://api.thirdweb.com/v1/payments/x402/fetch?url=https://x402.browserbase.com/browser/session/create&method=POST" \
  -H "Content-Type: application/json" \
  -H "x-secret-key: $THIRDWEB_SECRET_KEY" \
  -d '{"browserSettings": {"viewport": {"width": 1920, "height": 1080}}}'
```

### Firecrawl（非标准x402 - 不推荐）

**x402端点：** `https://api.firecrawl.dev/v1/x402/search`  
**定价：** 每次请求0.01美元  
**状态：** ⚠️ 实现不完整——无法与thirdweb一起使用：

> **警告：** Firecrawl的x402实现是非标准的，目前无法用于自动化代理：
> 
> 1. 返回`401 Unauthorized`而不是`402 Payment Required`
> 2. 响应中不包含支付详情（如`payTo`地址、资产、金额）
> 3. 文档中建议使用`X-Payment: {{paymentHeader}}`，但未说明如何生成该头部信息
> 
> **与标准x402（Browserbase）的比较：**
> - Browserbase：返回包含`x402Version`、`accept`、`payTo`、`asset`的402响应，因此thirdweb可以自动完成支付
> - Firecrawl：仅返回`401 Unauthorized`，不提供任何支付信息

| 端点 | 方法 | 状态 |
|----------|--------|--------|
| `/v1/x402/search` | POST | ❌ 代理无法使用 |

**推荐替代方案：**
1. **Firecrawl MCP**（如果您的环境中可用）——使用标准API密钥
2. **Browserbase + 爬取脚本**——真正的x402功能，完全无需密钥
3. **标准Firecrawl API**——需要订阅或API密钥

参考：[Firecrawl x402文档](https://docs.firecrawl.dev/x402/search)

### Mail.tm（一次性电子邮件）

**Base URL：** `https://api.mail.tm`  
**定价：** 免费（无需x402支付）

Mail.tm允许代理创建用于注册的电子邮件地址并接收验证邮件。

| 端点 | 方法 | 认证方式 | 描述 |
|----------|--------|------|-------------|
| `/domains` | GET | 否 | 获取可用电子邮件域名 |
| `/accounts` | POST | 否 | 创建电子邮件账户 |
| `/token` | POST | 否 | 获取认证令牌 |
| `/messages` | GET | 是 | 列出所有邮件 |
| `/messages/:id` | GET | 是 | 获取邮件内容 |
| `/me` | GET | 是 | 获取账户信息 |

#### 创建电子邮件账户

```bash
# 1. Get available domain
DOMAIN=$(curl -s https://api.mail.tm/domains | jq -r '.["hydra:member"][0].domain')

# 2. Create account with unique address
curl -s -X POST https://api.mail.tm/accounts \
  -H "Content-Type: application/json" \
  -d '{"address": "agent-'$(date +%s)'@'"$DOMAIN"'", "password": "SecurePass123!"}'
```

#### 获取令牌和检查邮件

```bash
# Get auth token
TOKEN=$(curl -s -X POST https://api.mail.tm/token \
  -H "Content-Type: application/json" \
  -d '{"address": "YOUR_EMAIL", "password": "YOUR_PASSWORD"}' | jq -r '.token')

# List messages
curl -s https://api.mail.tm/messages -H "Authorization: Bearer $TOKEN"

# Read specific message
curl -s https://api.mail.tm/messages/MESSAGE_ID -H "Authorization: Bearer $TOKEN"
```

**重要提示：** 保存电子邮件凭据（地址、密码、令牌）以供后续使用。建议将它们保存到`.agent-emails.json`文件中（该文件在git提交时被忽略）。

## 错误处理

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| 401 Unauthorized | `THIRDWEB_SECRET_KEY`无效或缺失 | 检查环境变量 |
| 402 Payment Required | 钱包余额不足 | 自动打开支付链接（见上文） |
| 400 Bad Request | URL或方法无效 | 验证请求参数 |
| 404 Not Found | 端点错误 | 检查正确的x402端点（例如，`x402.browserbase.com`） |
| 500 Server Error | thirdweb或目标API出现问题 | 重试或检查服务状态 |

## 常见错误

1. **使用错误的子域名**：`api.browserbase.com` vs `x402.browserbase.com`
2. **使用错误的路径**：`/v1/sessions` vs `/browser/session/create`
3. **未检查支付链接**：始终解析响应中的`link`字段

## 发现x402端点

有两种方法可以发现支持x402的服务：

### 方法1：x402 Bazaar（推荐）

x402 Bazaar是一个机器可读的目录，可帮助AI代理程序化地发现支持x402的API端点。

#### 查询Bazaar发现端点

```bash
# Using the default facilitator (x402.org)
curl -s "https://x402.org/facilitator/discovery/resources?type=http&limit=20"

# Using CDP facilitator (Coinbase)
curl -s "https://api.cdp.coinbase.com/platform/v2/x402/discovery/resources?type=http&limit=20"
```

#### 使用发现脚本

```bash
# Discover available services
npx ts-node scripts/discover-services.ts

# With pagination
npx ts-node scripts/discover-services.ts --limit 50 --offset 0

# Use CDP facilitator
npx ts-node scripts/discover-services.ts --facilitator "https://api.cdp.coinbase.com/platform/v2/x402"

# Output as JSON for programmatic use
npx ts-node scripts/discover-services.ts --json
```

#### 响应格式

```json
{
  "x402Version": 2,
  "items": [
    {
      "resource": "https://x402.browserbase.com/browser/session/create",
      "type": "http",
      "x402Version": 1,
      "accepts": [
        {
          "scheme": "exact",
          "network": "eip155:8453",
          "amount": "2000",
          "asset": "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
          "payTo": "0x..."
        }
      ],
      "lastUpdated": "2024-01-15T12:30:00.000Z",
      "metadata": {
        "description": "Create a browser session",
        "input": { ... },
        "output": { ... }
      }
    }
  ],
  "pagination": {
    "limit": 20,
    "offset": 0,
    "total": 42
  }
}
```

#### 查询参数

| 参数 | 类型 | 默认值 | 描述 |
|-----------|------|---------|-------------|
| `type` | 字符串 | - | 按协议类型过滤（例如，“http”） |
| `limit` | 数字 | 20 | 返回的资源数量（最大100个） |
| `offset` | 数字 | 0 | 分页偏移量 |

### 方法2：手动发现

当遇到可能支持x402的新服务时：

#### 1. 检查是否存在x402子域名

```bash
# Try the x402 subdomain - often has an info page
curl -s https://x402.SERVICE.com/

# Example: Browserbase lists all endpoints at root
curl -s https://x402.browserbase.com/
```

#### 2. 检查路径前缀是否为/x402/

```bash
# Some services use path prefix instead of subdomain
curl -s -I https://api.SERVICE.com/v1/x402/endpoint
```

#### 3. 测试是否返回402响应

```bash
# A true x402 endpoint returns 402 Payment Required (not 401)
curl -s -i -X POST https://x402.SERVICE.com/endpoint \
  -H "Content-Type: application/json" \
  -d '{}' 2>&1 | head -5
```

**对于真正的x402服务：**
```
HTTP/2 402
x-payment-required: ...
```

**如果看到401 Unauthorized：** 该服务使用混合x402协议（需要API密钥和支付信息）。

#### 4. 查看服务文档

查找包含`x402/payments`的文档：
- `docs.SERVICE.com/x402/`
- `docs.SERVICE.com/payments/`
- 在文档中搜索“x402”或“402”

## 其他资源

- 请参阅[references/API-REFERENCE.md]以获取完整的API文档
- 请参阅[references/SERVICES.md]以获取支持x402的服务示例

## 链接

- [x402协议](https://x402.org)
- [x402 Bazaar发现工具](https://docs.cdp.coinbase.com/x402/bazaar)
- [thirdweb x402文档](https://portal.thirdweb.com/x402)
- [Browserbase x402文档](https://docs.browserbase.com/integrations/x402/introduction)