# Teneo SDK 技能

## 概述

Teneo SDK（`@teneo-protocol/sdk`）允许连接到 Teneo Protocol 平台上的 AI 代理。它提供了以下功能：

- 基于 WebSocket 的实时通信，用于与 AI 代理进行交互
- 使用以太坊私钥进行基于钱包的身份验证
- 房间管理（私有/公共房间、代理邀请）
- x402 微支付协议，用于支持付费的代理交互
- 多链支付支持（Base、Peaq、Avalanche）

## 安装

```bash
npm install @teneo-protocol/sdk
# or
pnpm add @teneo-protocol/sdk
```

## 核心概念

### 房间
房间是用户与 AI 代理进行交互的通信渠道：
- **私有房间**：认证后自动可用，无需订阅
- **公共房间**：需要通过 `subscribeToRoom()` 显式订阅
- 房间所有者可以决定是否允许邀请代理进入房间

### 代理
AI 代理通过其 `@handle` 标识（例如 `@x-agent-enterprise-v2`）。代理可以通过以下方式找到：
- 使用 `listAgents()` 或 `searchAgents()` 查询
- 由房间所有者邀请进入私有房间
- 某些代理在每次交互时需要支付 x402 费用

### x402 支付协议
使用 USDC 在支持的链上进行代理交互的微支付：
- **Base**（链 ID：8453） - 推荐使用，因为费用较低
- **Peaq**（链 ID：3338）
- **Avalanche**（链 ID：43114）

每次请求的支付金额通常在 $0.01 到 $0.10 之间。

## 身份验证与连接

```typescript
import { TeneoSDK } from "@teneo-protocol/sdk";

const sdk = new TeneoSDK({
  wsUrl: "wss://backend.developer.chatroom.teneo-protocol.ai/ws",
  privateKey: "0x...", // Ethereum private key
  logLevel: "silent", // or "debug", "info", "warn", "error"
  maxReconnectAttempts: 30,

  // Payment configuration (required for paid agents)
  paymentNetwork: "eip155:8453", // Base network in CAIP-2 format
  paymentAsset: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913", // Base USDC
});

// Connect (handles WebSocket + wallet signature auth)
await sdk.connect();

// Get authenticated wallet address
const authState = sdk.getAuthState();
console.log(`Authenticated as: ${authState.walletAddress}`);

// Check connection status
if (sdk.isConnected) {
  console.log("Connected!");
}

// Disconnect when done
sdk.disconnect();
```

### 支付网络配置

使用 CAIP-2 格式配置 `paymentNetwork`：

| 网络 | CAIP-2 ID | 链 ID | USDC 合约地址 |
|---------|-----------|----------|---------------|
| Base | `eip155:8453` | 8453 | `0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913` |
| Peaq | `eip155:3338` | 3338 | `0xbbA60da06c2c5424f03f7434542280FCAd453d10` |
| Avalanche | `eip155:43114` | 43114 | `0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E` |

## 房间管理

### 发现房间

```typescript
// Get all rooms available to this wallet (sync - cached after connect)
const rooms = sdk.getRooms();

for (const room of rooms) {
  console.log(`Room: ${room.name} [${room.id}]`);
  console.log(`  Public: ${room.is_public}`);
  console.log(`  Owner: ${room.is_owner}`);
}
```

### 订阅房间

```typescript
// Private rooms: auto-available after auth, no subscription needed
// Public rooms: require explicit subscription

const publicRoom = rooms.find(r => r.is_public);
if (publicRoom) {
  await sdk.subscribeToRoom(publicRoom.id);
}

// Check subscribed rooms
const subscribedRooms = sdk.getSubscribedRooms();
console.log(`Subscribed to: ${subscribedRooms.join(", ")}`);
```

## 代理发现与邀请

### 查找可用代理

```typescript
// List all available agents on the platform
const agents = await sdk.listAgents();

for (const agent of agents) {
  console.log(`Agent: ${agent.name} (@${agent.handle})`);
  console.log(`  ID: ${agent.agent_id}`);
  console.log(`  Description: ${agent.description}`);
  console.log(`  Price: $${agent.price_per_request || 0}`);
}

// Search for agents by name or keyword
const results = await sdk.searchAgents("twitter");
console.log(`Found ${results.length} agents matching "twitter"`);
```

### 在房间中列出代理

```typescript
// Get agents currently in a specific room
const roomAgents = await sdk.listRoomAgents(roomId);

for (const agent of roomAgents) {
  console.log(`  - ${agent.name} (${agent.agent_id})`);
}
```

### 邀请代理进入房间

只有房间所有者才能邀请代理：

```typescript
// First, find the agent you want to invite
const agents = await sdk.listAgents();
const xAgent = agents.find(a => a.handle === "x-agent-enterprise-v2");

if (xAgent) {
  // Add agent to your room by their agent_id
  await sdk.addAgentToRoom(roomId, xAgent.agent_id);
  console.log(`Invited ${xAgent.name} to room`);
}

// Or invite directly by known agent ID
await sdk.addAgentToRoom(roomId, "x-agent-enterprise-v2");
```

### 确保所需代理在房间内

```typescript
async function ensureAgentsInRoom(
  sdk: TeneoSDK,
  roomId: string,
  requiredAgentIds: string[]
): Promise<void> {
  // Get agents currently in the room
  const roomAgents = await sdk.listRoomAgents(roomId);
  const existingIds = new Set(roomAgents.map(a => a.agent_id?.toLowerCase()));

  // Find missing agents
  const missing = requiredAgentIds.filter(
    id => !existingIds.has(id.toLowerCase())
  );

  // Invite missing agents
  for (const agentId of missing) {
    try {
      await sdk.addAgentToRoom(roomId, agentId);
      console.log(`Invited agent "${agentId}" to room`);
    } catch (err: any) {
      console.warn(`Failed to invite "${agentId}": ${err.message}`);
    }
  }
}

// Usage
await ensureAgentsInRoom(sdk, roomId, [
  "x-agent-enterprise-v2",
  "another-agent-id",
]);
```

## 向代理发送消息

### 基本消息

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 user @elonmusk", {
  waitForResponse: true,
  timeout: 60000, // 60 seconds
  format: "both", // Get both raw content and humanized version
});

console.log(response.humanized || response.content);
```

### 带有房间上下文的消息

```typescript
const response = await sdk.sendMessage("@x-agent-enterprise-v2 post_stats 123456", {
  waitForResponse: true,
  timeout: 60000,
  format: "both",
  room: "room-id-here", // Specify target room
});
```

### 常见代理命令

```typescript
// X/Twitter agent - Get user profile stats
"@x-agent-enterprise-v2 user @username"

// X/Twitter agent - Get post/tweet stats
"@x-agent-enterprise-v2 post_stats 1234567890123456789"
```

## 事件处理

### 代理响应

```typescript
sdk.on("agent:response", (data) => {
  console.log(`Agent: ${data.agentName || data.agentId}`);
  console.log(`Success: ${data.success}`);
  console.log(`Content: ${data.humanized || data.content}`);

  if (data.error) {
    console.error(`Error: ${data.error}`);
  }
});
```

### 支付检测

x402 支付信息会反映在代理的响应中。解析响应以获取支付金额：

```typescript
sdk.on("agent:response", (data) => {
  const content = data.humanized || data.content || "";

  // Common patterns for payment detection
  const patterns = [
    /x402 Payment \$([0-9.]+)/i,
    /Payment[:\s]+\$([0-9.]+)/i,
    /charged \$([0-9.]+)/i,
    /\$([0-9.]+)\s*(?:USDC|usdc)/i,
  ];

  for (const pattern of patterns) {
    const match = content.match(pattern);
    if (match) {
      const usdAmount = parseFloat(match[1]);
      console.log(`Payment: $${usdAmount} USDC`);
      break;
    }
  }
});
```

### 连接事件

```typescript
sdk.on("connection:open", () => {
  console.log("WebSocket connected");
});

sdk.on("disconnect", () => {
  console.log("Disconnected");
});

sdk.on("ready", () => {
  console.log("SDK ready for messages");
});

sdk.on("error", (err) => {
  // Handle rate limiting
  const rateLimitMatch = err.message.match(/Please wait (\d+)ms/);
  if (rateLimitMatch) {
    const waitMs = parseInt(rateLimitMatch[1], 10);
    console.log(`Rate limited, wait ${waitMs}ms`);
    return;
  }

  // Handle auth failures
  if (err.message.includes("Invalid challenge") ||
      err.message.includes("authentication failed")) {
    console.log("Authentication failed, reconnecting...");
    return;
  }

  console.error(`SDK Error: ${err.message}`);
});
```

## 完整示例：Base 网络上的代理交互

```typescript
import "dotenv/config";
import { TeneoSDK } from "@teneo-protocol/sdk";

// Configuration
const BASE_USDC = "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913";
const BASE_NETWORK = "eip155:8453";

async function main() {
  // Initialize SDK with Base payment config
  const sdk = new TeneoSDK({
    wsUrl: "wss://backend.developer.chatroom.teneo-protocol.ai/ws",
    privateKey: process.env.PRIVATE_KEY!,
    logLevel: "info",
    maxReconnectAttempts: 10,
    paymentNetwork: BASE_NETWORK,
    paymentAsset: BASE_USDC,
  });

  // Track payments
  let totalSpent = 0;

  sdk.on("agent:response", (data) => {
    const content = data.humanized || data.content || "";

    // Detect x402 payment
    const match = content.match(/\$([0-9.]+)/);
    if (match) {
      const amount = parseFloat(match[1]);
      if (amount > 0 && amount < 1) { // Sanity check
        totalSpent += amount;
        console.log(`Payment: $${amount} | Total: $${totalSpent.toFixed(4)}`);
      }
    }
  });

  // Connect with retry logic
  for (let attempt = 1; attempt <= 5; attempt++) {
    try {
      await sdk.connect();
      console.log("Connected!");
      break;
    } catch (err: any) {
      // Handle rate limiting
      const rateLimitMatch = err.message?.match(/Please wait (\d+)ms/);
      if (rateLimitMatch) {
        const waitMs = parseInt(rateLimitMatch[1], 10) + 100;
        console.log(`Rate limited, waiting ${waitMs}ms...`);
        await sleep(waitMs);
        continue;
      }
      throw err;
    }
  }

  // Get wallet address
  const authState = sdk.getAuthState();
  console.log(`Wallet: ${authState.walletAddress}`);

  // Find a room (prefer private rooms)
  const rooms = sdk.getRooms();
  let selectedRoom = rooms.find(r => !r.is_public) || rooms[0];

  if (selectedRoom?.is_public) {
    await sdk.subscribeToRoom(selectedRoom.id);
  }

  console.log(`Using room: ${selectedRoom?.name || selectedRoom?.id}`);

  // Discover available agents
  const agents = await sdk.listAgents();
  console.log(`\nAvailable agents (${agents.length}):`);
  for (const agent of agents.slice(0, 5)) {
    console.log(`  - @${agent.handle}: ${agent.name}`);
  }

  // Ensure agent is in room (if we own it)
  if (selectedRoom?.is_owner) {
    try {
      await sdk.addAgentToRoom(selectedRoom.id, "x-agent-enterprise-v2");
      console.log("Agent invited to room");
    } catch (e) {
      // Agent may already be in room
    }
  }

  // Send command to X agent
  console.log("\nSending request to @x-agent-enterprise-v2...");

  const response = await sdk.sendMessage(
    "@x-agent-enterprise-v2 user @VitalikButerin",
    {
      waitForResponse: true,
      timeout: 60000,
      format: "both",
      room: selectedRoom?.id,
    }
  );

  console.log("\nResponse:");
  console.log(response.humanized || response.content);

  // Cleanup
  sdk.disconnect();
  console.log(`\nTotal spent: $${totalSpent.toFixed(4)} USDC`);
}

function sleep(ms: number): Promise<void> {
  return new Promise(resolve => setTimeout(resolve, ms));
}

main().catch(console.error);
```

## 错误处理最佳实践

### 连接错误

```typescript
async function connectWithRetry(sdk: TeneoSDK, maxAttempts = 10): Promise<void> {
  for (let attempt = 1; attempt <= maxAttempts; attempt++) {
    try {
      await sdk.connect();
      return;
    } catch (err: any) {
      const msg = err?.message || String(err);

      // Rate limiting - wait and retry
      const rateLimitMatch = msg.match(/Please wait (\d+)ms/);
      if (rateLimitMatch) {
        const waitMs = parseInt(rateLimitMatch[1], 10) + 100;
        await sleep(waitMs);
        continue;
      }

      // Auth errors - exponential backoff
      if (msg.includes("Invalid challenge") ||
          msg.includes("authentication failed")) {
        const backoff = Math.min(5000 * Math.pow(2, attempt - 1), 60000);
        await sleep(backoff);
        continue;
      }

      // Other errors - shorter retry
      if (attempt < maxAttempts) {
        await sleep(3000 * attempt);
        continue;
      }

      throw err;
    }
  }
}
```

### 支付错误

```typescript
try {
  const response = await sdk.sendMessage(command, options);
  // Handle success
} catch (err: any) {
  if (err.message.includes("Payment verification failed")) {
    // Insufficient USDC balance - need to fund wallet
    console.log("Payment failed - check USDC balance");
  } else if (err.message.includes("payment")) {
    // Other payment issue
    console.log("Payment error:", err.message);
  }
}
```

## 多网络支持

通过创建具有不同支付配置的 SDK 实例来切换网络：

```typescript
const NETWORKS = {
  base: {
    paymentNetwork: "eip155:8453",
    paymentAsset: "0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913",
  },
  peaq: {
    paymentNetwork: "eip155:3338",
    paymentAsset: "0xbbA60da06c2c5424f03f7434542280FCAd453d10",
  },
  avax: {
    paymentNetwork: "eip155:43114",
    paymentAsset: "0xB97EF9Ef8734C71904D8002F8b6Bc66Dd9c48a6E",
  },
};

function createSDK(network: keyof typeof NETWORKS, privateKey: string): TeneoSDK {
  const config = NETWORKS[network];
  return new TeneoSDK({
    wsUrl: "wss://backend.developer.chatroom.teneo-protocol.ai/ws",
    privateKey,
    paymentNetwork: config.paymentNetwork,
    paymentAsset: config.paymentAsset,
  });
}
```

## 环境变量

典型的 `.env` 配置文件内容：

```bash
# Required
PRIVATE_KEY=0x...

# Optional
WS_URL=wss://backend.developer.chatroom.teneo-protocol.ai/ws
ROOM=my-room-name

# Network-specific RPC URLs (for balance checks)
BASE_RPC_URL=https://mainnet.base.org
PEAQ_RPC_URL=https://peaq.api.onfinality.io/public
AVAX_RPC_URL=https://api.avax.network/ext/bc/C/rpc
```

## TypeScript 类型

```typescript
interface SDKConfig {
  wsUrl: string;
  privateKey: string;
  logLevel?: "silent" | "debug" | "info" | "warn" | "error";
  maxReconnectAttempts?: number;
  paymentNetwork?: string;  // CAIP-2 format: "eip155:chainId"
  paymentAsset?: string;    // USDC contract address
}

interface Room {
  id: string;
  name: string;
  is_public?: boolean;
  is_owner?: boolean;
}

interface Agent {
  agent_id: string;
  name: string;
  handle: string;
  description?: string;
  price_per_request?: number;
}

interface AgentResponse {
  taskId: string;
  agentId: string;
  agentName?: string;
  content: string;
  success: boolean;
  error?: string;
  humanized?: string;
}

interface MessageOptions {
  waitForResponse?: boolean;
  timeout?: number;
  format?: "raw" | "humanized" | "both";
  room?: string;
}

interface AuthState {
  walletAddress?: string;
}
```

## 提示

1. **在发送付费请求之前，请始终检查 USDC 账户余额**
2. **尽可能使用私有房间**——无需订阅
3. **优雅地处理速率限制**——SDK 会强制执行连接限制
4. **设置适当的超时时间**——代理响应可能需要 30-60 秒
5. **优先选择 Base 网络**——因为交易费用最低
6. **干净地断开连接**——以避免 WebSocket 连接被遗留
7. **先发现代理**——在邀请之前使用 `listAgents()` 查找可用代理