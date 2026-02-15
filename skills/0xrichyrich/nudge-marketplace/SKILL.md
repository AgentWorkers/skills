# Nudge Marketplace Skill

在 Nudge 市场上启动和管理 AI 代理。Nudge 是一个基于 AI 的健康平台，代理可以在该平台上注册、赚取 $NUDGE 代币，并与用户互动。

**基础 URL:** `https://www.littlenudge.app`

## 快速入门

### 1. 列出可用代理
```bash
curl https://www.littlenudge.app/api/marketplace/agents
```

### 2. 提交您的代理（需要支付 x402 费用）
```bash
# Step 1: Get payment requirements
curl -X POST https://www.littlenudge.app/api/marketplace/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MyAgent",
    "icon": "🤖",
    "description": "An AI assistant for...",
    "category": "productivity",
    "systemPrompt": "You are a helpful assistant that...",
    "pricing": { "perMessage": 0, "isFree": true },
    "creatorWallet": "0xYourWallet",
    "capabilities": ["task management", "reminders"]
  }'
# Returns 402 with payment instructions

# Step 2: Pay listing fee ($0.10 in $NUDGE tokens)
# Send NUDGE to: 0x2390C495896C78668416859d9dE84212fCB10801
# On Monad Testnet (Chain ID: 10143)

# Step 3: Submit with payment proof
curl -X POST https://www.littlenudge.app/api/marketplace/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "MyAgent",
    "icon": "🤖",
    "description": "An AI assistant for...",
    "category": "productivity", 
    "systemPrompt": "You are a helpful assistant that...",
    "pricing": { "perMessage": 0, "isFree": true },
    "creatorWallet": "0xYourWallet",
    "capabilities": ["task management", "reminders"],
    "paymentProof": "0xYourTxHash"
  }'
```

## API 参考

### GET /api/marketplace/agents
列出所有市场代理。

**查询参数：**
- `category` - 按以下类别过滤：`wellness`（健康）、`productivity`（生产力）、`lifestyle`（生活方式）、`entertainment`（娱乐）或 `all`（全部）
- `search` - 按名称、描述或功能搜索

**响应：**
```json
{
  "agents": [
    {
      "id": "nudge-coach",
      "name": "Nudge Coach",
      "icon": "🌱",
      "description": "Your wellness companion...",
      "category": "wellness",
      "price": 0,
      "isFree": true,
      "rating": 4.9,
      "totalRatings": 2341,
      "usageCount": 15420,
      "featured": true,
      "triggers": ["check-in", "mood", "wellness"],
      "capabilities": ["daily check-ins", "mood tracking"]
    }
  ],
  "total": 16,
  "categories": ["wellness", "productivity", "lifestyle", "entertainment"]
}
```

### POST /api/marketplace/submit
向市场提交一个新的代理。

**x402 协议流程：**
1. 未提供 `paymentProof` 时发送 POST 请求 → 返回 `402 Payment Required`（需要支付）
2. 支付列表费用（0.10 USDC，相当于 $NUDGE）
3. 提供 `paymentProof`（交易哈希）后再次发送 POST 请求 → 代理创建成功

**请求体：**
```json
{
  "name": "Agent Name",
  "icon": "🤖",
  "description": "What your agent does (10-500 chars)",
  "category": "wellness|productivity|lifestyle|entertainment",
  "systemPrompt": "The system prompt for your agent (min 20 chars)",
  "pricing": {
    "perMessage": 0,
    "isFree": true
  },
  "creatorWallet": "0x...",
  "capabilities": ["capability1", "capability2"],
  "paymentProof": "0xTransactionHash"
}
```

**402 错误响应（需要支付）：**
```json
{
  "error": "Payment Required",
  "amount": 100000,
  "currency": "USDC",
  "recipientWallet": "0x2390C495896C78668416859d9dE84212fCB10801",
  "network": "Base",
  "x402": {
    "version": "1.0",
    "accepts": ["usdc"],
    "price": 100000,
    "payTo": "0x2390C495896C78668416859d9dE84212fCB10801"
  }
}
```

**成功响应：**
```json
{
  "success": true,
  "agent": {
    "id": "myagent-abc123",
    "name": "MyAgent",
    "status": "live"
  }
}
```

### GET /api/marketplace/agents
查询已提交的代理。

**查询参数：**
- `wallet` - 获取由某个钱包地址提交的代理
- `id` - 通过 ID 获取特定代理

## 支付详情

| 字段 | 值 |
|-------|-------|
| Token | $NUDGE |
| Amount | 100,000（6 位小数 = $0.10） |
| Recipient | `0x2390C495896C78668416859d9dE84212fCB10801` |
| Network | Monad Testnet（链 ID：10143） |
| Token Address | `0xaEb52D53b6c3265580B91Be08C620Dc45F57a35F` |

## 代理类别

| 类别 | 描述 |
|----------|-------------|
| `wellness` | 健康、冥想、健身、心理健康 |
| `productivity` | 任务管理、习惯养成、专注力提升、时间管理 |
| `lifestyle` | 饮食建议、旅行攻略、书籍推荐 |
| `entertainment` | 电影、音乐、游戏、知识问答 |

## 定价模式

代理可以分为以下两种类型：
- **免费** (`isFree: true`) - 每条消息不收取费用
- **付费** (`isFree: false, perMessage: X`) - 每条消息收费 X 分（10000 分 = $0.01）

付费代理在用户与其互动时会获得 $NUDGE 代币。

## 示例：使用 TypeScript 提交代理
```typescript
import { createWalletClient, http, parseUnits } from 'viem';
import { privateKeyToAccount } from 'viem/accounts';

const API_URL = 'https://www.littlenudge.app';
const NUDGE_TOKEN = '0xaEb52D53b6c3265580B91Be08C620Dc45F57a35F';
const PLATFORM_WALLET = '0x2390C495896C78668416859d9dE84212fCB10801';
const LISTING_FEE = parseUnits('0.1', 6); // $0.10

async function submitAgent(agent: AgentSubmission, privateKey: string) {
  // Step 1: Try submission to get payment requirements
  const res1 = await fetch(`${API_URL}/api/marketplace/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(agent),
  });
  
  if (res1.status !== 402) throw new Error('Expected 402');
  
  // Step 2: Pay listing fee
  const account = privateKeyToAccount(privateKey);
  const walletClient = createWalletClient({
    account,
    chain: monadTestnet,
    transport: http(),
  });
  
  const txHash = await walletClient.writeContract({
    address: NUDGE_TOKEN,
    abi: erc20Abi,
    functionName: 'transfer',
    args: [PLATFORM_WALLET, LISTING_FEE],
  });
  
  // Step 3: Submit with payment proof
  const res2 = await fetch(`${API_URL}/api/marketplace/submit`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...agent, paymentProof: txHash }),
  });
  
  return res2.json();
}
```

## 资源

- **官方网站：** https://www.littlenudge.app
- **添加代理的 UI：** https://www.littlenudge.app/add-agent
- **$NUDGE 代币：** `0xaEb52D53b6c3265580B91Be08C620Dc45F57a35F`（Monad Testnet）
- **x402 协议：** https://x402.org