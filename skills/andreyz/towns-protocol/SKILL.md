---
name: bots
description: >-
  Use when building Towns Protocol bots - covers SDK initialization, slash commands,
  message handlers, reactions, interactive forms, blockchain operations, and deployment.
  Triggers: "towns bot", "makeTownsBot", "onSlashCommand", "onMessage", "sendInteractionRequest",
  "webhook", "bot deployment", "@towns-protocol/bot"
license: MIT
compatibility: Requires Bun runtime, Base network RPC access, @towns-protocol/bot SDK
metadata:
  author: towns-protocol
  version: "2.0.0"
---

# Towns Protocol Bot SDK 参考

## 重要规则

**必须遵守以下规则，违反规则会导致系统无声地失败：**

1. **用户 ID 是以太坊地址** – 必须采用 `0x...` 的格式，不能使用用户名。
2. **提及功能需要同时满足以下两个条件**：在文本中使用 `<@{userId}>` 的格式，并且在选项中的 `mentions` 数组中也要包含该用户 ID。
3. **双钱包架构**：
   - `bot.viem.account.address`：用于支付交易费用的 Gas 钱包（必须使用 Base ETH 充值）。
   - `bot.appAddress`：用于资金转移的 Treasury 钱包（可选）。
4. **斜杠命令（slash commands）不会触发 `onMessage` 事件** – 它们是专门用于处理斜杠命令的处理器。
5. **交互式表单使用 `type` 属性** – 而不是 `case`（例如：`type: 'form'`）。
6. **切勿仅依赖 `txHash` 来判断交易是否成功** – 在授予访问权限之前，必须验证 `receipt.status === 'success'`。

## 快速参考

### 关键导入

```typescript
import { makeTownsBot, getSmartAccountFromUserId } from '@towns-protocol/bot'
import type { BotCommand, BotHandler } from '@towns-protocol/bot'
import { Permission } from '@towns-protocol/web3'
import { parseEther, formatEther, erc20Abi, zeroAddress } from 'viem'
import { readContract, waitForTransactionReceipt } from 'viem/actions'
import { execute } from 'viem/experimental/erc7821'
```

### 处理器方法

| 方法 | 签名 | 说明 |
|--------|-----------|-------|
| `sendMessage` | `(channelId, text, opts?) → {eventId }` | 参数：`opts` 可包含 `threadId?`, `replyId?`, `mentions?`, `attachments?` |
| `editMessage` | `(channelId, eventId, text)` | 仅用于处理机器人自己的消息。 |
| `removeEvent` | `(channelId, eventId)` | 仅用于处理机器人自己的消息。 |
| `sendReaction` | `(channelId, messageId, emoji)` | 用于发送表情符号。 |
| `sendInteractionRequest` | `(channelId, payload)` | 用于处理表单提交、交易请求等。 |
| `hasAdminPermission` | `(userId, spaceId) → boolean` | 检查用户是否具有管理员权限。 |
| `ban` / `unban` | `(userId, spaceId)` | 需要 `ModifyBanning` 权限才能执行操作。 |

### 机器人属性

| 属性 | 说明 |
|----------|-------------|
| `bot.viem` | 用于与区块链交互的 Viem 客户端。 |
| `bot.viem.account.address` | Gas 钱包地址（必须使用 Base ETH 充值）。 |
| `bot.appAddress` | Treasury 钱包地址（可选）。 |
| `bot.botId` | 机器人标识符。 |

**如需详细指南，请参阅 [参考文档](references/)：**
- [消息传递 API](references/MESSAGING.md) – 包含提及功能、线程管理、附件处理、格式化规则等。
- [区块链操作](references/BLOCKCHAIN.md) – 包括合约的读写、交易验证等功能。 |
- [交互式组件](references/INTERACTIVE.md) – 如何创建交互式表单、处理交易请求等。 |
- [部署指南](references/DEPLOYMENT.md) – 本地开发、代码渲染、通道配置等。 |
- [调试指南](references/DEBUGGING.md) – 问题排查方法。 |

---

## 机器人设置

### 项目初始化

```bash
bunx towns-bot init my-bot
cd my-bot
bun install
```

### 环境变量

```bash
APP_PRIVATE_DATA=<base64_credentials>   # From app.towns.com/developer
JWT_SECRET=<webhook_secret>              # Min 32 chars
PORT=3000
BASE_RPC_URL=https://base-mainnet.g.alchemy.com/v2/KEY  # Recommended
```

### 基本机器人模板

```typescript
import { makeTownsBot } from '@towns-protocol/bot'
import type { BotCommand } from '@towns-protocol/bot'

const commands = [
  { name: 'help', description: 'Show help' },
  { name: 'ping', description: 'Check if alive' }
] as const satisfies BotCommand[]

const bot = await makeTownsBot(
  process.env.APP_PRIVATE_DATA!,
  process.env.JWT_SECRET!,
  { commands }
)

bot.onSlashCommand('ping', async (handler, event) => {
  const latency = Date.now() - event.createdAt.getTime()
  await handler.sendMessage(event.channelId, 'Pong! ' + latency + 'ms')
})

export default bot.start()
```

### 配置验证

```typescript
import { z } from 'zod'

const EnvSchema = z.object({
  APP_PRIVATE_DATA: z.string().min(1),
  JWT_SECRET: z.string().min(32),
  DATABASE_URL: z.string().url().optional()
})

const env = EnvSchema.safeParse(process.env)
if (!env.success) {
  console.error('Invalid config:', env.error.issues)
  process.exit(1)
}
```

---

## 事件处理器

### onMessage

在普通消息（非斜杠命令）触发时执行。

```typescript
bot.onMessage(async (handler, event) => {
  // event: { userId, spaceId, channelId, eventId, message, isMentioned, threadId?, replyId? }

  if (event.isMentioned) {
    await handler.sendMessage(event.channelId, 'You mentioned me!')
  }
})
```

### onSlashCommand

在接收到 `/command` 命令时触发。不会触发 `onMessage` 事件。

```typescript
bot.onSlashCommand('weather', async (handler, { args, channelId }) => {
  // /weather San Francisco → args: ['San', 'Francisco']
  const location = args.join(' ')
  if (!location) {
    await handler.sendMessage(channelId, 'Usage: /weather <location>')
    return
  }
  // ... fetch weather
})
```

### onReaction

在用户发送表情符号时触发。

```typescript
bot.onReaction(async (handler, event) => {
  // event: { reaction, messageId, channelId }
  if (event.reaction === '👋') {
    await handler.sendMessage(event.channelId, 'I saw your wave!')
  }
})
```

### onTip

仅在开发者门户中启用“所有消息”（All Messages）模式下才能触发。

```typescript
bot.onTip(async (handler, event) => {
  // event: { senderAddress, receiverAddress, amount (bigint), currency }
  if (event.receiverAddress === bot.appAddress) {
    await handler.sendMessage(event.channelId,
      'Thanks for ' + formatEther(event.amount) + ' ETH!')
  }
})
```

### onInteractionResponse

在处理用户交互时触发。

```typescript
bot.onInteractionResponse(async (handler, event) => {
  switch (event.response.payload.content?.case) {
    case 'form':
      const form = event.response.payload.content.value
      for (const c of form.components) {
        if (c.component.case === 'button' && c.id === 'yes') {
          await handler.sendMessage(event.channelId, 'You clicked Yes!')
        }
      }
      break
    case 'transaction':
      const tx = event.response.payload.content.value
      if (tx.txHash) {
        // IMPORTANT: Verify on-chain before granting access
        // See references/BLOCKCHAIN.md for full verification pattern
        await handler.sendMessage(event.channelId,
          'TX: https://basescan.org/tx/' + tx.txHash)
      }
      break
  }
})
```

### 事件上下文验证

在使用事件处理器之前，务必验证事件上下文。

```typescript
bot.onSlashCommand('cmd', async (handler, event) => {
  if (!event.spaceId || !event.channelId) {
    console.error('Missing context:', { userId: event.userId })
    return
  }
  // Safe to proceed
})
```

---

## 常见错误及解决方法

| 错误 | 解决方法 |
|---------|-----|
| **Gas 资金不足** | 为 `bot.viem.account.address` 资金充值 Base ETH。 |
| 提及功能未生效 | 确保文本中包含 `<@userId>`，并且 `mentions` 数组中也包含该用户 ID。 |
| 斜杠命令无法使用 | 将相关命令添加到 `commands` 数组中（在 `makeTownsBot` 函数中）。 |
| 处理器未触发 | 检查开发者门户中的消息转发设置。 |
| `writeContract` 失败 | 对于外部合约，请使用 `execute()` 方法。 |
| 仅根据 `txHash` 授予访问权限 | 先验证 `receipt.status === 'success'`。 |
| 消息行重叠 | 使用 `\n\n`（双换行符），而不是 `\n`。 |
| 事件上下文缺失 | 在使用相关功能前，务必验证 `spaceId` 和 `channelId` 的值。 |

---

## 资源

- **开发者门户**：https://app.towns.com/developer
- **文档**：https://docs.towns.com/build/bots
- **SDK**：https://www.npmjs.com/package/@towns-protocol/bot
- **链 ID**：8453（Base Mainnet）