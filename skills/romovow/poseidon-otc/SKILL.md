---
name: poseidon-otc
description: 通过Poseidon OTC协议，在Solana网络上执行无信任的P2P代币交换操作。可以创建交易房间、协商交易条款、使用基于时间的托管服务锁定代币，并完成原子级的链上交换。该系统支持代理之间的实时交易，同时提供WebSocket实时更新功能。
metadata: { "openclaw": { "emoji": "🔱", "requires": { "env": ["POSEIDON_BURNER_KEY"] }, "primaryEnv": "POSEIDON_BURNER_KEY", "homepage": "https://poseidon.cash" } }
---

# Poseidon OTC Skill

**简要说明：**  
该技能允许您在Solana网络上与人类或其他代理进行代币交易。您需要创建一个交易房间，双方将代币存入托管账户，然后确认并执行原子交换（atomic swap）。整个过程无需信任机制，所有操作都在链上完成。

## 使用场景：  
- **点对点代币交易**：直接与其他用户交换任意SPL代币。  
- **代理间交易**：两个AI代理可以自主协商并执行交易。  
- **大额场外交易**：通过直接交易避免去中心化交易所（DEX）可能产生的滑点。  
- **受保护的交易**：使用锁定机制防止交易对手立即抛售代币。  
- **多代币交换**：单次原子交易中最多可交换4种代币。

## 代理快速入门：  
### 1. 初始化（需要钱包）  
```typescript
import { PoseidonOTC } from 'poseidon-otc-skill';

const client = new PoseidonOTC({
  burnerKey: process.env.POSEIDON_BURNER_KEY  // base58 private key
});
```

### 2. 创建交易房间  
```typescript
const { roomId, link } = await client.createRoom();
// Share `link` with counterparty or another agent
```

### 3. 等待交易对手并设置报价  
```typescript
// Check room status
const room = await client.getRoom(roomId);

// Set what you're offering (100 USDC example)
await client.updateOffer(roomId, [{
  mint: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',  // USDC mint
  amount: 100000000,  // 100 USDC (6 decimals)
  decimals: 6
}]);
```

### 4. 确认并执行交易  
```typescript
// First confirmation = "I agree to these terms"
await client.confirmTrade(roomId, 'first');

// After deposits, second confirmation
await client.confirmTrade(roomId, 'second');

// Execute the atomic swap
const { txSignature } = await client.executeSwap(roomId);
```

## 完整交易流程  
```
┌─────────────────────────────────────────────────────────────────┐
│                        TRADE LIFECYCLE                          │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. CREATE ROOM                                                 │
│     └─> Party A calls createRoom()                              │
│         Returns: roomId, shareable link                         │
│                                                                 │
│  2. JOIN ROOM                                                   │
│     └─> Party B calls joinRoom(roomId)                          │
│         Room now has both participants                          │
│                                                                 │
│  3. SET OFFERS                                                  │
│     └─> Both parties call updateOffer(roomId, tokens)           │
│         Each specifies what they're putting up                  │
│                                                                 │
│  4. FIRST CONFIRM (agree on terms)                              │
│     └─> Both call confirmTrade(roomId, 'first')                 │
│         "I agree to swap my X for your Y"                       │
│                                                                 │
│  5. DEPOSIT TO ESCROW                                           │
│     └─> Tokens move to on-chain escrow                          │
│         (Handled by frontend or depositToEscrow)                │
│                                                                 │
│  6. SECOND CONFIRM (verify deposits)                            │
│     └─> Both call confirmTrade(roomId, 'second')                │
│         "I see the deposits, ready to swap"                     │
│                                                                 │
│  7. EXECUTE SWAP                                                │
│     └─> Either party calls executeSwap(roomId)                  │
│         Atomic on-chain swap via relayer                        │
│         Returns: txSignature                                    │
│                                                                 │
│  [OPTIONAL] LOCKUP FLOW                                         │
│     └─> Before step 4, Party A can proposeLockup(roomId, secs)  │
│     └─> Party B must acceptLockup(roomId) to continue           │
│     └─> After execute, locked tokens claimed via claimLockedTokens │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## API参考：  

### 房间管理  
| 方法 | 参数 | 返回值 | 描述 |  
|--------|------------|---------|-------------|  
| `createRoom(options?)` | `{ inviteCode?: string }` | 创建新房间 |  
| `getRoom(roomId)` | `roomId: string` | `TradeRoom` | 获取房间状态 |  
| `getUserRooms(wallet?)` | `wallet?: string` | `TradeRoom[]` | 查看您的房间列表 |  
| `joinRoom(roomId, inviteCode?)` | `roomId, inviteCode?` | 以交易对手身份加入房间 |  
| `cancelRoom(roomId)` | `roomId: string` | 取消房间并退款 |  
| `getRoomLink(roomId)` | `roomId: string` | 房间分享链接 |  

### 交易操作  
| 方法 | 参数 | 返回值 | 描述 |  
|--------|------------|---------|-------------|  
| `updateOffer(roomId, tokens)` | `roomId, [{mint, amount, decimals}]` | 设置您的报价 |  
| `withdrawFromOffer(roomId, tokens)` | `roomId, tokens[]` | 撤回已提交的代币 |  
| `confirmTrade(roomId, stage)` | `roomId, 'first' | 'second'` | 确认交易阶段 |  
| `executeSwap(roomId)` | `roomId: string` | `txSignature` | 执行交换 |  
| `declineOffer(roomId)` | `roomId: string` | 拒绝交易条款 |  

### 锁定机制（防止交易对手抛售）  
| 方法 | 参数 | 返回值 | 描述 |  
|--------|------------|---------|-------------|  
| `proposeLockup(roomId, seconds)` | `roomId, seconds` | 提出锁定请求 |  
| `acceptLockup(roomId)` | `roomId: string` | 接受锁定请求 |  
| `getLockupStatus(roomId)` | `roomId: string` | `canClaim, timeRemaining` | 查看锁定状态及剩余时间 |  
| `claimLockedTokens(roomId)` | `roomId: string` | 期满后领取锁定代币 |  

### 实用功能  
| 方法 | 参数 | 返回值 | 描述 |  
|--------|------------|---------|-------------|  
| `getBalance()` | 无 | `sol: number` | 查看SOL余额 |  
| `isAutonomous()` | 无 | `boolean` | 是否使用签名钱包 |  
| `getWebSocketUrl()` | 无 | 获取WebSocket连接地址 |  

## WebSocket实时更新  
**建议使用WebSocket进行实时监控，而非频繁调用`getRoom()`方法：**  
连接地址：`wss://poseidon.cash/ws/trade-room`  

### 订阅房间事件  
```typescript
const { unsubscribe } = await client.subscribeToRoom(roomId, (event) => {
  switch (event.type) {
    case 'join':
      console.log('Counterparty joined!');
      break;
    case 'offer':
      console.log('Offer updated:', event.data.tokens);
      break;
    case 'confirm':
      console.log('Confirmation received');
      break;
    case 'execute':
      console.log('Swap complete! TX:', event.data.txSignature);
      break;
    case 'cancel':
      console.log('Trade cancelled');
      break;
  }
});
```  
**事件类型及触发时机：**  
| 事件 | 触发条件 |  
|-------|--------------|  
| `full-state` | 订阅后立即获取房间完整状态 |  
| `join` | 交易对手加入房间 |  
| `offer` | 有人更新报价 |  
| `confirm` | 有人确认交易（第一方或第二方） |  
| `lockup` | 提出或接受锁定请求 |  
| `execute` | 交易成功执行 |  
| `cancel` | 房间被取消 |  
| `terminated` | 房间到期或终止 |  
| `error` | 发生错误 |  

### WebSocket操作（比HTTP更快）  
```typescript
await client.sendOfferViaWs(roomId, tokens);      // Update offer
await client.sendConfirmViaWs(roomId, 'first');   // Confirm
await client.sendLockupProposalViaWs(roomId, 3600); // Propose 1hr lock
await client.sendAcceptLockupViaWs(roomId);       // Accept lock
await client.sendExecuteViaWs(roomId);            // Execute swap
```  

## 代理间交易示例：  
**场景：** 代理A希望用1000个USDC兑换5个SOL给代理B：  
### 代理A（卖方）：  
```typescript
// 1. Create room
const { roomId } = await client.createRoom();

// 2. Set offer (1000 USDC)
await client.updateOffer(roomId, [{
  mint: 'EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v',
  amount: 1000000000,  // 1000 USDC
  decimals: 6
}]);

// 3. Share roomId with Agent B via your inter-agent protocol
// 4. Subscribe to updates
await client.subscribeToRoom(roomId, async (event) => {
  if (event.type === 'offer') {
    // Check if Agent B's offer is acceptable (5 SOL)
    const room = await client.getRoom(roomId);
    if (room.partyBTokenSlots?.[0]?.amount >= 5 * 1e9) {
      await client.confirmTrade(roomId, 'first');
    }
  }
  if (event.type === 'confirm' && room.partyBFirstConfirm) {
    await client.confirmTrade(roomId, 'second');
  }
});
```  
### 代理B（买方）：  
```typescript
// 1. Join the room
await client.joinRoom(roomId);

// 2. Set offer (5 SOL)
await client.updateOffer(roomId, [{
  mint: 'So11111111111111111111111111111111111111112',  // wSOL
  amount: 5000000000,  // 5 SOL
  decimals: 9
}]);

// 3. Subscribe and react
await client.subscribeToRoom(roomId, async (event) => {
  if (event.type === 'confirm') {
    const room = await client.getRoom(roomId);
    if (room.partyAFirstConfirm && !room.partyBFirstConfirm) {
      await client.confirmTrade(roomId, 'first');
    }
    if (room.partyASecondConfirm && room.partyBSecondConfirm) {
      // Both confirmed, execute!
      await client.executeSwap(roomId);
    }
  }
});
```  

## 常见代币信息：  
| 代币 | 发行地址 | 小数位数 |  
|-------|--------------|----------|  
| USDC | `EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v` | 6 |  
| USDT | `Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB` | 6 |  
| wSOL | `So11111111111111111111111111111111111111112` | 9 |  
| BONK | `DezXAZ8z7PnrnRJjz3wXBoRgixCa6xjnB7YaB1pPB263` | 5 |  

## 环境变量  
```bash
POSEIDON_BURNER_KEY=<base58-private-key>  # Required for autonomous mode
POSEIDON_API_URL=https://poseidon.cash    # API endpoint (default: mainnet)
POSEIDON_RPC_URL=https://api.mainnet-beta.solana.com  # Solana RPC
```  

## 安全注意事项：  
- **托管在链上**：资金由Solana程序管理，而非API控制。  
- **原子交换**：双方必须同时完成交易，否则交易失败。  
- **签名有效期**：签名在24小时内有效。  
- **锁定机制强制执行**：无法绕过锁定时间。  
- **使用备用钱包**：仅将可承受风险的金额存入交易钱包。  

## 程序ID：  
**主网：** `AfiRReYhvykHhKXhwjhcsXFejHdxqYLk2QLWnjvvLKUN`  

## 链接：  
- 网站：https://poseidon.cash  
- 文档：https://docs.poseidon.cash