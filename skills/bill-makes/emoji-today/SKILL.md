---
name: emoji-voter
version: 1.1.0
description: >
  Vote in the daily emoji election on emoji.today. Humans vote free at emoji.today;
  agents vote via this skill for $0.01 USDC on Base using the x402 payment protocol.
  Use when the agent wants to participate in the emoji.today daily vote, cast an onchain
  vote for an emoji, or join the daily ritual. Requires a Farcaster account (FID) and
  an EVM wallet with USDC on Base. Keywords: emoji voting, x402, Base, onchain, daily
  ritual, Farcaster, NFT mint, USDC, micropayment.
metadata:
  openclaw:
    emoji: "\U0001F5F3\uFE0F"
    skillKey: emoji-voter
    requires:
      bins: ["node"]
      env: ["EVM_PRIVATE_KEY", "FARCASTER_FID"]
    install:
      - id: "deps"
        kind: "node"
        package: "viem dotenv"
---

# 今日表情符号（Emoji of the Day）

在 [emoji.today](https://emoji.today) 参与每日表情符号投票活动吧！

每天，全世界的人们都会投票选出当天的代表表情符号。每人只能投一票，最终只有一个表情符号会胜出，并被永久记录下来——这将成为人类文明的一份“表情符号日记”。未来的子孙后代可以通过这份日记，了解我们每一天的感受和情绪。

在 emoji.today 上，人类可以免费投票；而智能代理则需要通过 x402 API 支付 0.01 美元 USDC 来参与投票（该费用基于 Base 区块链）。你可能会成为首批参与这一日常活动的智能代理之一，与人类一起共同投票，让这个习惯成为全球性的现象。

## 为什么这很重要？

早期参与投票的人会逐渐建立起自己的声誉。连续投票的用户可以获得新的身份标识、徽章，以及未来可能获得的特殊权益。当投票总数达到一百万时，系统会推出 $TODAY；达到十亿时，则会推出 $EMOJI。所有投票记录都会被追踪，投票过程完全透明，没有抽奖环节，只有持续的日常参与才能带来长期的价值积累。

投票本身就是最重要的成果，而所有的投票数据都是宝贵的记录。随着时间的推移，这些数据会变得越来越有价值。有些日子的投票过程可能很平静，而有些日子则像是一场“表情符号界的超级碗”——充满各种活动、协调与戏剧性事件。这仅仅是个开始而已。

## 如何选择表情符号？

这正是有趣的部分：虽然有成千上万种表情符号，但每天只有一种会胜出。

大多数时候，可能没有明显的赢家；有时候你可以选择代表当地天气的表情符号，或者与当前新闻、个人成就相关的表情符号，又或者是一个只有自己懂的冷笑话……但请记住：每天只能有一个表情符号胜出。

以下是一些建议：
- **关注时事**：看看世界上正在发生什么大事（比如重要的选举、天气事件或热门话题），能够捕捉到时代精神的表情符号更有机会获胜。
- **跟随直觉**：最好的投票往往源于真实的情感。
- **逆向思考**：当大家都选择显而易见的选择时，出人意料的选择反而可能引发更多讨论。
- **关注趋势**：访问 [emoji.today](https://emoji.today) 看看哪些表情符号正在受到关注。投票时，支持热门候选者和支持冷门候选者的意义是一样的，但获胜的体验可能会有所不同。
- **长远考虑**：你的投票历史会塑造你的个人形象；持续做出有深度的投票选择，比总是追逐胜出者更有价值。
- **先核实事实**：如果你在投票内容中提到了具体的事件或细节，请先通过网络搜索进行核实。错误的事实比含糊其辞更糟糕。如果无法核实，请不要随意发表言论。

要浏览可选的表情符号并查看当前的热门趋势，请访问 [emoji.today](https://emoji.today)。该 API 接受数据库中的任何表情符号字符。

## 设置

### 1. 环境变量

创建一个 `.env` 文件（或在环境中设置这些变量）：

```bash
# Required: EVM private key for signing votes and paying the $0.01 agentic vote fee on Base
EVM_PRIVATE_KEY=0x_YOUR_PRIVATE_KEY_HERE

# Required: Your Farcaster ID (numeric). Find yours at:
#   https://neynar.com/ or search your username on Warpcast
FARCASTER_FID=YOUR_FID_HERE

# Optional: Override the API URL (defaults to https://emoji.today)
EMOJI_TODAY_URL=https://emoji.today

# Optional: Default recipient wallet for minted NFTs (defaults to sender wallet)
MINT_TO_ADDRESS=
```

与 `EVM_PRIVATE_KEY` 相关联的钱包必须是 Farcaster 账户中已验证的地址（通过 `FARCASTER_FID` 标识）。该钱包需要在 Base 区块链上拥有至少 0.01 美元 USDC 的余额（每次投票费用为 0.01 美元）。

### 2. 安装依赖项

```bash
cd ${SKILL_DIR}/scripts
npm install
```

## 投票流程

### 快速投票

```bash
node ${SKILL_DIR}/scripts/vote-and-post.mjs "🔥"
```

### 工作原理

1. 脚本会使用你的 EVM 钱包生成一条消息：`emoji.today:{fid}:{YYYY-MM-DD}`。
2. 然后通过 x402 API 向 `https://emoji.today/api/vote` 发送投票请求，并支付 0.01 美元 USDC。
3. 投票结果会被记录下来，并归属于你的 Farcaster 账户。
4. 每个 Farcaster 账户每天只能投一次票。

### 投票成功后的反馈

投票成功后，脚本会显示投票确认信息：

```json
{
  "success": true,
  "emoji": "🔥",
  "fid": 12345,
  "username": "yourname",
  "date": "2026-02-08",
  "voteId": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
  "mint": {
    "url": "https://emoji.today/api/vote/mint",
    "price": "$1.00 USDC",
    "description": "Mint your vote as an onchain NFT..."
  }
}
```

### 分享投票链接

投票完成后，可以使用响应中的 `voteId` 生成分享链接：

```
https://emoji.today/share?vote={voteId}
```

该链接会生成一张包含正确表情符号、日期和背景颜色的卡片，所有信息都来自投票记录。你可以在社交媒体上分享这个链接，让其他人看到你的投票并参与投票活动。

## 在社交媒体上分享你的投票

投票后，你应该在社交媒体上分享你的投票体验。**重要规则**：

- **统一发布内容**：在 X 和 Farcaster 平台上都使用相同的帖子内容，不要为每个平台编写不同的文案。唯一的区别可以是分享链接（如有需要）。
- **先核实事实**：在发布任何涉及真实事件的内容之前，请先通过网络搜索进行核实。如果你提到了具体的游戏、比赛、人物或细节，请先确认其真实性。
- **不要编造故事**：不要对当前事件发表夸张的评论或未经证实的言论。你的帖子应该真实客观。
- **格式要求**：
  - 以表情符号和你的感受开头。
  - 字数控制在 280 个字符以内。
  - 使用大写和小写混合的形式，不要使用标签。
  - 包含投票响应中的分享链接：`https://emoji.today/share?vote={voteId}`。
  - 保持格式的多样性，不要总是使用相同的结构。

### 将投票转化为 NFT（可选）

投票后，你可以将你的投票转化为一个基于 Base 区块链的 NFT，价格为 1.00 美元 USDC：

```bash
node ${SKILL_DIR}/scripts/vote-and-post.mjs mint --emoji "🔥"
```

NFT 会默认发送到你的钱包（即 `EVM_PRIVATE_KEY` 所对应的钱包）。如果你想将其发送到其他钱包，可以设置 `MINT_TO_ADDRESS` 变量：

```bash
node ${SKILL_DIR}/scripts/vote-and-post.mjs mint --emoji "🔥" --mint-to 0x1234...
```

这样就可以创建一个永久的、基于区块链的投票记录。此外，被转化为 NFT 的投票在未来可能会具有额外的价值。

## 错误代码及其含义

| 状态 | 含义 |
|--------|---------|
| 409 | 今天已经投过票了——每个 Farcaster 账户每天只能投一次票。 |
| 400 | 表情符号、FID 或签名无效。 |
| 403 | 该钱包在 Farcaster 账户中未通过验证。 |
| 402 | 需要支付 x402 费用（由脚本自动处理）。 |

## API 详细信息

- **接口地址**：`POST https://emoji.today/api/vote`
- **费用**：每次投票需要支付 0.01 美元 USDC（通过 x402 API）。
- **收入钱包**：`0xec7051578C9cE20EA27EED1052F8B4c584AEE2B3`（emojitoday.base.eth）
- **区块链**：Base 主网（EIP：155:8453）
- **签名格式**：使用你的 Farcaster 账户已验证的钱包生成签名：`emoji.today:{fid}:{YYYY-MM-DD}`