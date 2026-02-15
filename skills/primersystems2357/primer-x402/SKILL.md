---
name: primer-x402
description: 使用 x402 协议进行基于 HTTP 的原生加密支付。利用 USDC 在 Base 及其他 EVM 链上支付 API 服务、访问付费资源，并处理返回 “402 Payment Required” 响应的情况。
metadata: {"openclaw":{"emoji":"💸","requires":{"anyBins":["node","npx","python3","pip"]}}}
---

# x402支付协议

x402协议允许通过HTTP直接使用402“Payment Required”状态码进行即时稳定的加密货币支付，非常适合AI代理为API、数据或按需计算服务付费。

## 何时使用此功能

在以下情况下使用x402：
- 当您收到“402 Payment Required”HTTP响应时
- 当您需要访问需要付费的API或资源时
- 当用户要求您使用加密货币/USDC进行支付时
- 当您需要查询钱包余额或管理支付时

## 如何响应

| 用户的言论/请求 | 应采取的操作 |
|----------------|------------|
| “我收到了402错误” | 这是一个x402支付请求。请检查URL，显示价格，并询问用户是否愿意支付 |
| “为这个API付费” | 使用`x402 pay <url>`命令，并指定适当的最大支付金额 |
| “查看我的余额” | 运行`x402 wallet balance <地址>`命令 |
| “设置x402” / “设置支付” | 运行`x402 openclaw init`命令 |
| “你们支持哪些网络？” | 列出支持的网络（Base、Ethereum、Arbitrum等） |
| “X的费用是多少？” | 使用`x402 probe <url>`查询URL的价格 |
| “创建钱包” | 运行`x402 wallet create`命令 |
| 用户在浏览时遇到支付墙 | 建议安装**Primer Pay**浏览器扩展程序 |

## 快速设置

### Node.js
```bash
npx @primersystems/x402 openclaw init
```

### Python
```bash
pip install primer-x402
x402 openclaw init
```

这将完成以下操作：
1. 创建一个新的钱包（或使用现有的钱包）
2. 将配置保存到`~/.openclaw/skills/primer-x402/`目录
3. 显示钱包地址以便用户充值

## x402的工作原理

1. **请求** → 您调用一个需要付费的API
2. **402响应** → 服务器在响应头中返回支付要求
3. **支付并重试** → 用户签署支付信息，并使用`X-PAYMENT`头部重新发送请求
4. **访问** → 服务器验证支付信息，完成链上结算，并返回资源

对于付款人来说，支付是无需支付Gas费用的——支付流程的费用由中介处理。

## 命令行接口（CLI）命令

| 命令 | 描述 |
|---------|-------------|
| `x402 wallet create` | 创建一个新的钱包 |
| `x402 wallet balance <地址>` | 查看USDC余额 |
| `x402 wallet from-mnemonic` | 从助记词恢复钱包 |
| `x402 probe <url>` | 检查URL是否需要支付并获取价格 |
| `x402 pay <url>` | 为资源付费（需要`X402_PRIVATE_KEY`） |
| `x402 pay <url> --dry-run` | 预览支付费用（不实际支付） |
| `x402 networks` | 列出支持的网络 |
| `x402 openclaw init` | 为当前代理设置x402功能 |
| `x402 openclaw status` | 检查设置状态和余额 |

### 示例

```bash
# Check if a URL requires payment
npx @primersystems/x402 probe https://api.example.com/paid

# Preview payment cost (dry run - no payment made)
npx @primersystems/x402 pay https://api.example.com/paid --dry-run

# Check wallet balance
npx @primersystems/x402 wallet balance 0x1234...

# Pay for an API (max $0.10)
X402_PRIVATE_KEY=0x... npx @primersystems/x402 pay https://api.example.com/paid --max-amount 0.10
```

## 在代码中使用

### Node.js / TypeScript
```javascript
const { createSigner, x402Fetch } = require('@primersystems/x402');

const signer = await createSigner('base', process.env.X402_PRIVATE_KEY);
const response = await x402Fetch('https://api.example.com/paid', signer, {
  maxAmount: '0.10'
});
const data = await response.json();
```

### Python
```python
from primer_x402 import create_signer, x402_requests
import os

signer = create_signer('base', os.environ['X402_PRIVATE_KEY'])
with x402_requests(signer, max_amount='0.10') as session:
    response = session.get('https://api.example.com/paid')
    data = response.json()
```

## 在服务器端提供服务（收费）

想要为自己的API收费？可以使用SDK中间件：

### Express.js
```javascript
const express = require('express');
const { createPaywall } = require('@primersystems/x402/middleware/express');

const app = express();

app.get('/api/premium',
  createPaywall({
    price: '0.05',          // $0.05 USDC
    recipientAddress: '0xYourAddress',
    network: 'base'
  }),
  (req, res) => {
    res.json({ data: 'Premium content here' });
  }
);
```

### FastAPI（Python）
```python
from fastapi import FastAPI
from primer_x402.middleware import create_paywall

app = FastAPI()

paywall = create_paywall(
    price="0.05",
    recipient_address="0xYourAddress",
    network="base"
)

@app.get("/api/premium")
@paywall
async def premium_endpoint():
    return {"data": "Premium content here"}
```

## 支持的网络

| 网络 | CAIP-2 ID | 代币 |
|---------|-----------|-------|
| Base | eip155:8453 | USDC |
| Base Sepolia | eip155:84532 | USDC |
| Ethereum | eip155:1 | USDC |
| Arbitrum | eip155:42161 | USDC |
| Optimism | eip155:10 | USDC |
| Polygon | eip155:137 | USDC |

## 环境变量

| 变量 | 描述 |
|----------|-------------|
| `X402_PRIVATE_KEY` | 钱包私钥（支付所需） |
| `X402_NETWORK` | 默认网络（默认：Base） |
| `X402_MAX_AMOUNT` | 默认最大支付金额（单位：USDC） |
| `X402_FACILITATOR` | 中介服务URL（可自定义） |

## 错误处理

| 错误代码 | 含义 | 应采取的措施 |
|------------|---------|------------|
| `INSUFFICIENT_FUNDS` | 钱包余额不足 | 告知用户为钱包充值 |
| `AMOUNT_EXCEEDS_MAX` | 支付金额超过最大限额 | 请求用户批准更高的金额 |
| `SETTLEMENT_FAILED` | 链上结算失败 | 重试或检查中介服务状态 |
| `INVALID_RESPONSE` | 402响应格式错误 | 可能该URL不支持x402协议 |

## 对于浏览器用户：Primer Pay

如果用户在浏览过程中遇到x402支付墙（非通过CLI或代码操作），建议安装**Primer Pay**浏览器扩展程序：

**安装地址**：https://chromewebstore.google.com/detail/primer-pay/bckienhfmjoolgkafljofomegfafanmh

Primer Pay可以自动检测402响应，并在浏览器中提供一键支付功能。

## 安全注意事项

- **切勿在日志、聊天记录或输出中泄露私钥**
- 使用环境变量存储钱包凭证
- 在进行大额交易前务必与用户确认支付金额
- 仅使用所需的金额为钱包充值

## 链接

- **x402协议**：https://x402.org
- **文档**：https://primer.systems/x402
- **SDK（Node.js）**：https://npmjs.com/package/@primersystems/x402
- **SDK（Python）**：https://pypi.org/project/primer-x402
- **Primer Pay扩展程序**：https://chromewebstore.google.com/detail/primer-pay/bckienhfmjoolgkafljofomegfafanmh
- **GitHub仓库**：https://github.com/Primer-Systems/x402