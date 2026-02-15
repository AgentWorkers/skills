---
name: aegis-security-hackathon
version: 1.0.0
description: **AI代理用区块链安全扫描器（测试网）**  
支持通过 **x402协议** 使用 **Base Sepolia USDC** 进行支付。
homepage: https://hackathon.aegis402.xyz
metadata: {"emoji":"🛡️","category":"blockchain-security","api_base":"https://hackathon.aegis402.xyz/v1","network":"testnet"}
---

# Aegis402 防护协议（黑客马拉松/测试网）

这是一个用于人工智能代理的区块链安全 API。**测试网版本**，支持使用 Base Sepolia 的 USDC 进行支付。

> ⚠️ 请注意：此版本仅用于黑客马拉松或测试环境。如需生产环境使用，请访问 [aegis-security](https://aegis402.xyz/skill.md)。

## 技能文件

| 文件名 | URL |
|------|-----|
| **SKILL.md** （当前文件） | `https://hackathon.aegis402.xyz/skill.md` |
| **package.json** （元数据） | `https://hackathon.aegis402.xyz/skill.json` |

**基础 URL：** `https://hackathon.aegis402.xyz/v1`

## 快速入门

```bash
npm install @x402/fetch @x402/evm
```

```typescript
import { x402Client, wrapFetchWithPayment } from '@x402/fetch';
import { ExactEvmScheme } from '@x402/evm/exact/client';

const client = new x402Client()
  .register('eip155:*', new ExactEvmScheme(yourEvmWallet));

const fetch402 = wrapFetchWithPayment(fetch, client);

// Payments on Base Sepolia (testnet USDC)
const res = await fetch402('https://hackathon.aegis402.xyz/v1/check-token/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48?chain_id=1');
const data = await res.json();
```

**使用要求：** 需要拥有 Base Sepolia 链上的测试网 USDC（链 ID：84532）

**获取测试网 USDC：** [Base Sepolia 提款机](https://www.coinbase.com/faucets/base-ethereum-sepolia-faucet)

---

## 价格（测试网 USDC）

| 端点 | 价格 | 用途 |
|----------|-------|----------|
| `POST /simulate-tx` | $0.05 | 交易模拟，DeFi 安全性检测 |
| `GET /check-token/:address` | $0.01 | 检测代币中的恶意代码（“蜜罐”） |
| `GET /check-address/:address` | $0.005 | 检查地址的安全性 |

---

## 端点详情

### 检测代币（$0.01）

扫描代币以发现恶意代码、诈骗行为或其他风险。

```bash
curl "https://hackathon.aegis402.xyz/v1/check-token/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48?chain_id=1"
```

**响应：**
```json
{
  "address": "0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48",
  "isHoneypot": false,
  "trustScore": 95,
  "risks": [],
  "_meta": { "requestId": "uuid", "duration": 320 }
}
```

### 检查地址（$0.005）

验证地址是否被标记为钓鱼或恶意攻击的目标。

```bash
curl "https://hackathon.aegis402.xyz/v1/check-address/0x742d35Cc6634C0532925a3b844Bc454e4438f44e"
```

**响应：**
```json
{
  "address": "0x742d35Cc6634C0532925a3b844Bc454e4438f44e",
  "isPoisoned": false,
  "reputation": "NEUTRAL",
  "tags": ["wallet", "established"],
  "_meta": { "requestId": "uuid", "duration": 180 }
}
```

### 模拟交易（$0.05）

在签署交易前预测账户余额变化并检测潜在威胁。

```bash
curl -X POST "https://hackathon.aegis402.xyz/v1/simulate-tx" \
  -H "Content-Type: application/json" \
  -d '{
    "from": "0xYourWallet...",
    "to": "0xContract...",
    "value": "1000000000000000000",
    "data": "0x...",
    "chain_id": 8453
  }'
```

**响应：**
```json
{
  "isSafe": true,
  "riskLevel": "LOW",
  "simulation": {
    "balanceChanges": [
      { "asset": "USDC", "amount": "-100.00", "address": "0x..." }
    ]
  },
  "warnings": [],
  "_meta": { "requestId": "uuid", "duration": 450 }
}
```

---

## x402 支付流程（测试网）

1. 代理调用相应的付费端点。
2. 收到提示“需要支付 402 USDC”的信息，并根据提示在 Base Sepolia 链（链 ID：84532）上进行支付。
3. 重新提交请求，并附上支付证明。
4. 获取安全扫描结果。

**网络：** Base Sepolia（EIP：155:84532）
**货币：** 测试网 USDC

---

## 人工智能代理的用途

### 在交换代币之前
```typescript
const tokenCheck = await fetch402(`https://hackathon.aegis402.xyz/v1/check-token/${tokenAddress}?chain_id=8453`);
const { isHoneypot, trustScore } = await tokenCheck.json();

if (isHoneypot || trustScore < 50) {
  console.log('⚠️ Risky token detected!');
}
```

### 在签署交易之前
```typescript
const simulation = await fetch402('https://hackathon.aegis402.xyz/v1/simulate-tx', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ from, to, value, data, chain_id: 8453 })
});

const { isSafe, riskLevel, warnings } = await simulation.json();

if (!isSafe || riskLevel === 'CRITICAL') {
  console.log('🚨 Dangerous transaction!', warnings);
}
```

---

## 风险等级

| 等级 | 含义 |
|-------|---------|
| `SAFE` | 未检测到任何问题 |
| `LOW` | 存在轻微风险，一般安全 |
| `MEDIUM` | 存在部分风险，请谨慎操作 |
| `HIGH` | 检测到重大风险 |
| `CRITICAL` | 严禁继续操作 |

---

## 支持的区块链

| 链名 | ID | 检测代币功能 | 检查地址功能 | 模拟交易功能 |
|-------|-----|-------------|---------------|-------------|
| Ethereum | 1 | ✅ | ✅ | ✅ |
| Base | 8453 | ✅ | ✅ | ✅ |
| Polygon | 137 | ✅ | ✅ | ✅ |
| Arbitrum | 42161 | ✅ | ✅ | ✅ |
| Optimism | 10 | ✅ | ✅ | ✅ |
| BSC | 56 | ✅ | ✅ | ✅ |

---

## 健康检查（免费）

```bash
curl https://hackathon.aegis402.xyz/health
```

---

## 链接

- **黑客马拉松 API：** https://hackathon.aegis402.xyz
- **生产环境 API：** https://aegis402.xyz
- **GitHub 仓库：** https://github.com/SwiftAdviser/aegis-402-shield-protocol
- **x402 协议文档：** https://docs.x402.org

---

🛡️ 专为“代理经济”（Agent Economy）设计，由 x402 协议提供支持。