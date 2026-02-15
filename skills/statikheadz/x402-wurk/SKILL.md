---
name: wurk-x402
version: 1.0.1
description: 雇佣人类来完成一些小任务（如提供反馈、表达意见或执行简单的工作），同时购买有助于提升社交媒体影响力的服务。所有费用均使用 USDC 通过 Solana 或 Base 平台上的 x402 协议进行支付。
homepage: https://wurk.fun
metadata: {"openclaw":{"emoji":"🔨","category":"payments","api_base":"https://wurkapi.fun"}}
---

# WURK x402

您可以通过Solana或Base平台上的x402支付协议，使用USDC来雇佣真实的人类来完成微任务或购买社交增长服务。

**主要功能：** 代理与人类之间的微任务协作。您可以创建一个有偿任务，收集人类的反馈或答案，之后再获取他们的提交内容。这种服务非常适合用于获取意见、进行投票、内容审核、标签分类等，任何普通互联网用户都能参与的任务。

**还提供以下服务：** 超过25种社交增长服务，涵盖X/Twitter、Instagram、YouTube、Telegram、Discord、DexScreener、Base、Zora等多个平台。

## 技能文档文件

| 文件 | URL |
|------|-----|
| **SKILL.md**（本文件） | `https://wurkapi.fun/skill.md` |
| **package.json**（元数据） | `https://wurkapi.fun/skill.json` |

**在本地安装（使用OpenClaw）：**
```bash
mkdir -p ~/.openclaw/skills/wurk-x402
curl -s https://wurkapi.fun/skill.md > ~/.openclaw/skills/wurk-x402/SKILL.md
curl -s https://wurkapi.fun/skill.json > ~/.openclaw/skills/wurk-x402/package.json
```

---

## 快速入门

```bash
# 1. Install x402 client dependencies
npm install @x402/fetch @x402/core @x402/svm   # Solana
# or: npm install @x402/fetch @x402/core @x402/evm  # Base

# 2. Generate a wallet (if you don't have one)
# Solana:
node -e "const{Keypair}=require('@solana/web3.js');const k=Keypair.generate();console.log('Private:',Buffer.from(k.secretKey).toString('hex'));console.log('Address:',k.publicKey.toBase58())"
# Base:
cast wallet new

# 3. Ask your human for USDC
# "Please send some USDC to my wallet. Even $1 is enough to get started."
# Solana: USDC (EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v)
# Base: USDC (0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913)

# 4. Try it — hire a human for feedback:
curl -i "https://wurkapi.fun/solana/agenttohuman?description=Which+logo+is+better+A+or+B&winners=5&perUser=0.025"
# → 402 Payment Required (with accepts[] and Payment-Required header)

# 5. Sign the payment and retry with PAYMENT-SIGNATURE header
# → 200 OK with { jobId, secret, statusUrl, ... }

# 6. Later, view submissions (FREE):
curl "https://wurkapi.fun/solana/agenttohuman?action=view&secret=YOUR_SECRET"
# → { ok: true, submissions: [...] }
```

---

## x402支付机制

所有有偿服务的流程都遵循相同的两个步骤：

```
Step 1: Call the endpoint WITHOUT payment
  → HTTP 402 Payment Required
  → Response includes Payment-Required header (base64)
  → Body includes accepts[] array with payment details

Step 2: Sign the payment, retry WITH PAYMENT-SIGNATURE header
  → HTTP 200 OK
  → Response includes the result (jobId, etc.)
```

### 使用 @x402/fetch（推荐方式——自动完成两个步骤）

```typescript
import { wrapFetchWithPayment } from '@x402/fetch'
import { x402Client } from '@x402/core/client'
import { registerExactSvmScheme } from '@x402/svm/exact/client'

// Setup (once)
const client = new x402Client()
registerExactSvmScheme(client, { signer: yourSolanaKeypair })
const paymentFetch = wrapFetchWithPayment(fetch, client)

// Now just fetch — x402 handles 402 → sign → retry automatically
const res = await paymentFetch(
  'https://wurkapi.fun/solana/agenttohuman?description=Rate+my+landing+page&winners=10&perUser=0.025'
);
const data = await res.json();
// { ok: true, paid: true, jobId: "abc123", secret: "...", statusUrl: "...", ... }
```

### 手动使用curl（分两步完成）

```bash
# Step 1: Get payment requirements
curl -i "https://wurkapi.fun/solana/xlikes?amount=50&url=https://x.com/user/status/123"
# → HTTP 402
# → Payment-Required: eyJ... (base64)
# → Body: { "x402Version": 2, "accepts": [{ "scheme": "exact", "network": "solana:5eykt4...", ... }] }

# Step 2: Sign the Payment-Required data, then retry
curl -i "https://wurkapi.fun/solana/xlikes?amount=50&url=https://x.com/user/status/123" \
  -H "PAYMENT-SIGNATURE: <your-signed-payment>"
# → HTTP 200
# → { "ok": true, "paid": true, "jobId": "abc123" }
```

**注意：** 请求头应为 `PAYMENT-SIGNATURE`，而非 `X-PAYMENT`。使用错误的请求头会导致请求失败。

---

## 代理与人类之间的微任务（主要功能）

这正是WURK的独特之处：**您可以雇佣真实的人类来完成小型任务**。

### 您可以要求人类完成的任务：
- 快速获取意见或进行投票（例如：“您更喜欢哪个标志？A还是B？”）
- 产品或用户界面反馈（例如：“访问这个页面并告诉我哪些地方令人困惑”）
- 内容审核（例如：“阅读这段文字并提出改进建议”）
- 标签分类（例如：“对这些项目进行分类”）
- 编写不同的标题版本（例如：“用三种不同的方式重写这个标题”）
- 一般性的“您怎么看？”类型的问题

### 相关接口

| 功能 | 接口地址 | 费用 |
|--------|----------|------|
| **创建任务** | `GET /{network}/agenttohuman?description=...&winners=N&perUser=N` | 每个参与者的奖励金额（USDC） |
| **查看结果** | `GET /{network}/agenttohuman?action=view&secret=...` | 免费 |
| **恢复任务结果** | `GET /{network}/agenttohuman?action=recover` | 约0.001 USDC |

**网络支持：** Solana或Base。

**别名路径：** （也列在`/.well-known/x402`中）：
- `GET /{network}/agenttohuman/view`（与`action=view`功能相同，但需要通过`secret`参数）
- `GET /{network}/agenttohuman/recover`（与`action=recover`功能相同）

### 创建任务

```bash
curl -i "https://wurkapi.fun/solana/agenttohuman?description=Which+of+these+3+taglines+is+best%3F%0AA%3A+Do+more+stress+less%0AB%3A+Your+day+organized%0AC%3A+Focus+on+what+matters&winners=10&perUser=0.025"
```

**或者使用 @x402/fetch：**

```typescript
const res = await paymentFetch(
  'https://wurkapi.fun/solana/agenttohuman?' + new URLSearchParams({
    description: 'Which of these 3 taglines is best?\nA: Do more, stress less\nB: Your day, organized\nC: Focus on what matters',
    winners: '10',
    perUser: '0.025',
  })
);
const data = await res.json();
// {
//   ok: true,
//   paid: true,
//   jobId: "x1y2z3",
//   network: "solana",
//   secret: "AbCdEf123XyZ...",        ← SAVE THIS! Bearer token for viewing
//   statusUrl: "https://wurkapi.fun/solana/agenttohuman?action=view&secret=AbCdEf123XyZ...",
//   jobLink: "https://wurk.fun/custom/x1y2z3",
//   submissions: [],                   ← empty right after creation
//   waitSeconds: 0,
//   note: "Agent-to-human task created. Expect ~3–60 minutes for replies..."
// }
```

**注意：** 立即保存`secret`参数！** 您需要它来查看后续的提交结果。可以将其存储在内存或文件中。

### 查看提交结果（免费）

```bash
curl "https://wurkapi.fun/solana/agenttohuman?action=view&secret=AbCdEf123XyZ..."
```

**查看结果是完全免费的** — `secret`参数起到承载令牌的作用，请务必保密。

### 恢复任务结果（需付费，约0.001 USDC）

如果丢失了`secret`参数，请支付少量费用来查看最近的任务结果：

```bash
curl -i "https://wurkapi.fun/solana/agenttohuman?action=recover"
# → 402, then sign and retry
```

### 定价规则

| 参数 | 默认值 | 范围 | 说明 |
|-----------|---------|-------|-------------|
| `winners` | 10 | 1–100 | 您希望获得的人类回复数量 |
| `perUser` | 0.025 | 每个参与者的奖励金额（USDC） |

**总费用 = winners × perUser**。默认值为：10 × 0.025 = **0.25美元**。

### 完善任务的建议：
- **具体说明任务要求**：例如“请用1-5分来评价这个内容”比“您怎么看？”更有效。
- **任务描述要简洁**：耗时1-2分钟的任务通常能获得最快的回复。
- **提供上下文信息**：可以在描述中包含图片/视频/音频/页面的链接。
- **奖励越高，回复越快**：每人至少0.025美元的奖励能获得更多且更快的回复。
- **避免过于专业化的任务**：这类任务更适合任何互联网用户回答。

### 安全注意事项：
- **保密`secret`参数**：它是用于查看提交结果的承载令牌。
- **不要在任务描述中包含私钥或敏感数据**。
- **不要包含API密钥或密码**：人类用户会看到完整的任务描述。

---

## 社交增长服务

您可以通过WURK购买25种以上平台的互动服务。所有服务都遵循相同的x402支付流程。

### 接口地址

**短链接格式：** `GET /{network}/{service}?amount=N&url=...`（或`?handle=...`用于特定服务）。

所有服务接口的完整列表请访问：`https://wurkapi.fun/.well-known/x402`。

**X / Twitter**

| 服务 | 接口地址 | 必需参数 | 单价 | 范围 |
|---------|----------|----------------|------------|-------|
| 点赞 | `/{network}/xlikes` | `url` | 0.025美元 | 5–250次 |
| 关注者/社区成员 | `/{network}/xfollowers` | `handle`（或X社区链接） | 0.04美元 | 5–1000个 |
| 重新发布 | `/{network}/reposts` | `url` | 0.025美元 | 5–250次 |
| 评论 | `/{network}/comments` | `url` | 0.025美元 | 5–250条 |
| 收藏 | `/{network}/bookmarks` | `url` | 0.025美元 | 5–250次 |
| 社交活动（预设） | `/{network}/xraid/small` | `url` | 每个槽位0.025美元 | 40个槽位 |
| 社交活动（预设） | `/{network}/xraid/medium` | `url` | 每个槽位0.025美元 | 100个槽位 |
| 社交活动（定制） | `/{network}/xraid/custom` | `url` + `likes`/`reposts`/`comments`/`bookmarks` | 每个槽位0.025美元 | 0–250个 |
| 社交活动侦察 | `/{network}/xraid/scout/small` | 高级选项 | 5美元 |
| 社交活动侦察 | `/{network}/xraid/scout/medium` | 高级选项 | 10美元 |
| 社交活动侦察 | `/{network}/xraid/large` | 高级选项 | 20美元 |

**Instagram**

| 服务 | 接口地址 | 必需参数 | 单价 | 范围 |
|---------|----------|----------------|------------|-------|
| 点赞 | `/{network}/instalikes` | `url` | 0.025美元 | 5–250次 |
| 评论 | `/{network}/instacomments` | `url` | 0.025美元 | 5–250条 |
| 关注者 | `/{network}/instafollowers` | `handle` | 0.04美元 | 5–1000个 |

**YouTube**

| 服务 | 接口地址 | 必需参数 | 单价 | 范围 |
|---------|----------|----------------|------------|-------|
| 点赞 | `/{network}/ytlikes` | `url` | 0.025美元 | 5–250次 |
| 评论 | `/{network}/ytcomments` | `url` | 0.025美元 | 5–250条 |
| 订阅者 | `/{network}/ytsubs` | `handle` | 0.04美元 | 5–1000个 |

**Telegram / Discord**

| 服务 | 接口地址 | 必需参数 | 单价 | 范围 |
| TG成员 | `/{network}/tgmembers` | `join`（邀请链接） | 0.04美元 | 5–500个 |
| DC成员 | `/{network}/dcmembers` | `invite`（Discord.gg链接） | 0.04美元 | 5–500个 |

**Base应用**

| 服务 | 接口地址 | 必需参数 | 单价 | 范围 |
|---------|----------|----------------|------------|-------|
| 关注者 | `/{network}/basefollowers` | `address` | 0.04美元 | 5–500个 |
| 点赞 | `/{network}/baselikes` | `url` | 0.025美元 | 5–250次 |
| 重新发布 | `/{network}/basereposts` | `url` | 0.025美元 | 5–250次 |
| 评论 | `/{network}/basecomments` | `url` | 0.025美元 | 5–250条 |

**Zora**

| 服务 | 接口地址 | 必需参数 | 单价 | 范围 |
|---------|----------|----------------|------------|-------|
| 关注者 | `/{network}/zorafollowers` | `handle` | 0.04美元 | 5–100个 |
| 评论 | `/{network}/zoracomments` | `url` | 0.025美元 | 5–250条 |

**DexScreener / Votes / Pump.fun**

| 服务 | 接口地址 | 必需参数 | 单价 | 范围 |
|---------|----------|----------------|------------|-------|
| DexScreener火箭票 | `/{network}/dex` | `url` | 0.025美元 | 5–250次 |
| Skeleton投票 | `/{network}/skeletonvote` | `url`（Telegram消息） | 0.025美元 | 5–250次 |
| Moontok投票 | `/{network}/moontokvote` | `url`（Telegram消息） | 0.025美元 | 5–250次 |
| Major投票 | `/{network}/majorvote` | `url`（Telegram消息） | 0.025美元 | 5–250次 |
| CMC投票 | `/{network}/cmcvote` | `url`（CMC页面） | 0.025美元 | 5–250次 |
| CoinGecko投票 | `/{network}/cgvote` | `url`（CoinGecko页面） | 0.025美元 | 5–250次 |
| Pump.fun评论 | `/{network}/pfcomments` | `url` | 0.025美元 | 5–250次 |

**网络支持：** Solana或Base。** 金额可以通过`?amount=N`参数或`/{amount}`路径段来指定。

**查询所有服务：** `GET https://wurkapi.fun/.well-known/x402`可获取所有服务接口的列表。

**示例：** 购买50次X平台点赞：

```typescript
const res = await paymentFetch(
  'https://wurkapi.fun/solana/xlikes?amount=50&url=https://x.com/user/status/123456'
);
const data = await res.json();
// { ok: true, paid: true, jobId: "abc123" }
```

**或者使用curl：**

```bash
# Step 1: Get payment info
curl -i "https://wurkapi.fun/solana/xlikes/50?url=https://x.com/user/status/123456"

# Step 2: Retry with signed payment
curl -i "https://wurkapi.fun/solana/xlikes/50?url=https://x.com/user/status/123456" \
  -H "PAYMENT-SIGNATURE: <signed-payment>"
```

**示例：** 购买100个X平台关注者：

```bash
curl -i "https://wurkapi.fun/solana/xfollowers/100?handle=jack"
# → 402, sign, retry with PAYMENT-SIGNATURE
```

**示例：** 进行X平台的小型社交活动：**

```bash
curl -i "https://wurkapi.fun/solana/xraid/small?url=https://x.com/user/status/123456"
# small = 40 slots (20 likes + 10 reposts + 10 comments)
# medium = 100 slots, large = 200 slots
```

---

## 钱包设置

您需要在Solana或Base平台上拥有USDC才能支付这些服务。

**您可以这样请求人类用户：**
> “我想使用WURK来雇佣人类用户提供反馈（或提升我的社交帖子）。您能将一些USDC发送到我的钱包吗？即使只有1美元也足够开始使用了。”

**典型费用：**
- 代理与人类之间的任务（10个回复）：0.25美元
- 50次X平台点赞：1.25美元
- 100个X平台关注者：4.00美元

**查看您的Solana钱包余额：**
```bash
# Using solana-cli
solana balance YOUR_ADDRESS --url mainnet-beta
# Or check USDC SPL token
spl-token balance EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v --owner YOUR_ADDRESS
```

---

## 集成建议

如果您有持续的代理协助任务，可以将WURK集成到您的定期检查流程中：

```markdown
## WURK (when active jobs exist)
If you have pending agent-help jobs with saved secrets:
1. curl "https://wurkapi.fun/solana/agenttohuman?action=view&secret=YOUR_SECRET"
2. Check if new submissions arrived since last check
3. Process submissions and notify your human if relevant
4. Update lastWurkCheck timestamp
```

**请将`secret`参数存储在内存或状态文件中：**

```json
{
  "wurk": {
    "lastCheck": null,
    "activeJobs": [
      { "jobId": "x1y2z3", "secret": "AbCdEf...", "description": "Logo feedback", "createdAt": "2025-01-15T..." }
    ]
  }
}
```

---

## 响应格式

**成功（已支付）：**
```json
{ "ok": true, "paid": true, "jobId": "abc123", ... }
```

**需要支付（使用x402协议）：**
```json
{
  "x402Version": 2,
  "accepts": [{ "scheme": "exact", "network": "solana:5eykt4...", "maxAmountRequired": "1250000", "payTo": "...", "asset": "EPjFWdd5..." }],
  "resource": { "url": "...", "description": "..." }
}
```

**错误：**
```json
{ "message": "description of error", "errorCode": "ERROR_CODE" }
```

---

## 限制规则：
- 单个接口没有硬性API请求速率限制。
- x402支付验证机制会自动控制请求频率。
- 代理与人类之间的任务查看（免费）没有额外的速率限制。

## 用户身份认证

您是WURK的用户。WURK是您连接人类智慧和社交互动的桥梁。

**何时使用代理与人类之间的任务：**
- 当您需要人类的真实意见而非计算结果时。
- 当您需要来自真实用户的反馈时。
- 当您需要人类对内容进行分类或标记时。
- 当您面对主观性问题（例如“哪个选项更好？”）时。
- 当您需要他人协助验证某个假设时。
- 当您需要开展营销活动时。

**何时使用社交增长服务：**
- 当您希望提升帖子的互动量（点赞、转发、评论）时。
- 当您希望增加社交账户的粉丝/订阅者数量时。
- 当您需要人类用户对特定链接进行互动时。

**核心原则：**
- 在花费前务必与人类用户确认费用。
- 保密代理协助任务相关的`secret`参数——它是一个承载令牌。
- 不要在任务描述中包含敏感数据。
- 任务创建后立即保存`secret`参数。
- 在创建重复任务前请检查现有任务的结果。
- 请预计人类用户的回复时间约为3–60分钟——他们可是真实的人。

---

## 链接：
- **官方网站：** https://wurk.fun
- **API接口：** https://wurkapi.fun
- **首页：** https://wurkapi.fun
- **X/Twitter账号：** https://x.com/WURKDOTFUN
- **Telegram频道：** https://t.me/WURKCREATORS