---
name: x-engagement
description: "用于AI代理的Twitter/X互动技巧。涵盖算法优化、自动化账户设置、互动模式、工具集成以及速率限制管理，以建立真实可信的在线形象。"
version: 2.0.0
author: ClawdiaETH
keywords: twitter, x, engagement, social, algorithm, ai-agent, automated, xai-search, bird
---

# 用于AI代理的X平台互动策略

作为AI代理，在Twitter/X平台上建立真实且有效的存在感至关重要。本技能涵盖了算法机制、互动策略、工具使用以及合规性方面的内容。

## 快速入门

1. 使用“Automated by @operator”标签设置您的账户。
2. 为优先关注的账户配置监控功能。
3. 使用命令行工具（CLI）进行内容读取，或通过浏览器/API进行内容发布。
4. 快速回复——回复的速度比回复的数量更重要。
5. **记录您回复的内容**——切勿对同一条推文重复回复。

---

## 账户设置

### 自动化账户标签

**必备要求**：增加账户的真实性，降低被封禁的风险。

1. 以机器人账户登录X平台。
2. 访问：`x.com/settings/account/automation`
3. 点击“设置账户自动化”。
4. 输入操作员的@用户名。
5. 输入操作员的密码进行验证。

标签会显示在个人资料中：“Automated by @operator”。

**注意**：此标签仅用于显示，并不会改变API的行为。通过API发布的自动化内容仍会受到回复频率的限制。

### 个人资料优化

- **简洁的简介**：说明您的身份和职责。
- **链接到操作员的个人资料**：增强信任感。
- **一致的用户名**：与您的ENS（以太坊名称服务）或链上身份保持一致（如适用）。
- **个人资料图片**：独特且易于记忆。

---

## 工具参考

### 内容读取与监控

| 工具 | 用途 | 设置方式 |
|------|---------|-------|
| **bird CLI** | 读取推文、提及和搜索 | 基于Cookie的身份验证 |
| **xai-search** | 通过Grok技术实现实时X平台内容搜索 | 需要`XAI_API_KEY` |
| **x-trends** | 流行话题查询（无API接口） | 无需额外设置 |

#### bird CLI
```bash
# Install
pip install bird-cli  # or build from source

# User's recent tweets
bird user-tweets @handle -n 5 --plain

# Your mentions
bird mentions -n 10 --plain

# Search
bird search "query" -n 10 --plain

# Read specific tweet
bird read <tweet_id> --plain
```

#### xai-search（通过Grok实现实时X平台搜索）

需要Python 3.10及以上版本以及xai-sdk：
```bash
# Setup
python3.12 -m venv ~/.venv/xai
source ~/.venv/xai/bin/activate
pip install xai-sdk

# Set API key
export XAI_API_KEY="your-key"  # Get from console.x.ai
```

使用方法：
```bash
# X/Twitter search
xai-search x "What are people saying about @handle today"

# Web search
xai-search web "how does [thing] work"

# Both
xai-search both "latest news about [topic]"
```

**注意**：服务器端工具需要`grok-4-1-fast`模型（而非grok-3）。

#### x-trends
```bash
# Install
clawdhub install x-trends

# Usage
node ~/skills/x-trends/index.js --country us --limit 10
node ~/skills/x-trends/index.js --country us --json  # For parsing
```

### 内容发布

**发布优先级**：
1. **官方X API**（最可靠，但需要开发者门户和相应的信用点数）。
2. **浏览器自动化**：作为备用方案，模拟人类行为。
3. **bird CLI**：仅用于读取内容（发布操作会被机器人检测系统阻止）。

#### X API（官方）

需要访问X开发者门户（每月费用100美元）。

```bash
# Setup: Create app at developer.x.com, get OAuth 1.0a credentials
# Store in ~/.clawdbot/secrets/x-api.json:
{
  "consumerKey": "...",
  "consumerSecret": "...",
  "accessToken": "...",
  "accessTokenSecret": "..."
}

# Post
node x-post.mjs "Your tweet text"

# Reply
node x-post.mjs --reply <tweet_id> "Your reply"
```

**注意事项**：
- 开发者门户可能会标记自动化账户——可以申诉或使用操作员的APP并通过OAuth授权进行操作。
- 访问令牌与登录时使用的账户关联。
- 更改应用权限后需要重新生成令牌。

#### 浏览器自动化

当API被阻止或不可用时，优先使用**直接DOM自动化**或基于快照的点击方式。

##### 直接DOM方法（推荐）

使用`Runtime.evaluate`直接与Twitter的DOM交互——无需虚拟鼠标或手动定位元素：
```javascript
// Inject the library (inline - CORS blocks GitHub fetch)
// Copy twitter-dom.js contents and inject directly:
browser action=act request='{"kind": "evaluate", "fn": "() => { window.__td = { /* paste minified library */ }; return \"ready\"; }"}'

// Post a tweet
browser action=act request='{"kind": "evaluate", "fn": "async () => await window.__twitterDOM.tweet(\"Your tweet text here\")"}'

// Reply (navigate to tweet first)
browser action=act request='{"kind": "evaluate", "fn": "async () => { await window.__twitterDOM.reply(\"Your reply\"); return await window.__twitterDOM.post(); }"}'

// Like
browser action=act request='{"kind": "evaluate", "fn": "() => window.__twitterDOM.like()"}'

// Retweet
browser action=act request='{"kind": "evaluate", "fn": "async () => await window.__twitterDOM.retweet()"}'
```

**优点**：
- 直接调用`element.click()`可确保事件处理的可靠性。
- 不需要在不同快照之间查找元素位置。
- 不需要进行坐标计算。
- 即使元素位置发生变化也能正常工作。
- 减少尝试次数，从而节省令牌使用。

**完整库链接**：https://github.com/ClawdiaETH/twitter-dom-automation

##### 快照方法（备用）

如果直接DOM方法失败，可以使用传统的浏览器自动化方式：
```
1. Navigate to tweet URL or compose page
2. Snapshot to find textbox element (look for refs)
3. Type your content
4. Click post button
```

虽然这种方法能模拟人类行为，但可靠性较低。

---

## 算法机制

### 互动效果

回复的互动效果大约是点赞数的10倍。优化目标是促进对话，而非追求表面的数据指标。

### 发布后的2小时窗口期

发布后的前2小时至关重要：
- 回复的速度比总互动次数更重要。
- 30分钟内获得100个赞比24小时内获得500个赞更有效。
- 发布后要保持在线状态，以便及时回复。

### 需避免的行为（会降低互动效果）

| 行为 | 影响 |
|--------|--------|
| 正文中的外部链接 | 降低互动率50% |
| 使用过多标签 | 易被视作垃圾信息 |
| 重复发布相同内容 | 被标记为垃圾信息 |
- 被举报或被封禁 | 会受到算法惩罚 |
- 在用户活跃度较低的时段发布 | 会浪费互动机会 |

### 提高互动效果的方法

| 行为 | 影响 |
|--------|--------|
- 使用媒体内容（图片/视频） | 提高互动率2-10倍 |
- 发布多条相关推文 | 增加用户停留时间 |
- 提出问题或分享有价值的观点 | 促进他人回复 |
- 引用有价值的推文 | 利用已有内容的传播效应 |
- 在大账号上首先回复 | 提高在该账号受众中的可见性 |

---

## 媒体附件（高优先级）

**包含媒体内容的推文互动率是纯文本推文的2-10倍**。在以下情况下务必添加图片/GIF：
- 宣布项目或里程碑
- 分享数据或统计信息
- 展示可视化内容（网站、应用程序、仪表盘等）
- 庆祝成就

### 可用工具

| 工具 | 用途 | 命令 |
|------|---------|---------|
| **Browser screenshot** | 获取整个页面或视口的截图 | `browser action=screenshot` |
| **gifgrep** | 从Tenor/Giphy搜索/下载GIF | `gifgrep "查询" --download` |
| **ffmpeg** | 从图片/视频创建GIF | `ffmpeg -i input.mp4 output.gif` |

### 截图操作流程
```bash
# 1. Open the page
browser action=open targetUrl="https://example.com"

# 2. Take screenshot (saved to ~/.clawdbot/media/browser/)
browser action=screenshot targetId="<id>"

# 3. Open compose
browser action=navigate targetUrl="https://x.com/compose/post"

# 4. Click "Add photos or video" button first (from modal snapshot)
browser action=snapshot selector="[aria-labelledby='modal-header']"
browser action=act request='{"kind": "click", "ref": "<add_photos_button>"}'

# 5. Upload image via file input
browser action=upload selector="input[type='file'][accept*='image']" paths='["path/to/screenshot.jpg"]'

# 6. WAIT for upload to process
browser action=act request='{"kind": "wait", "timeMs": 3000}'

# 7. VERIFY upload succeeded — snapshot must show "Edit media" / "Remove media"
browser action=snapshot selector="[aria-labelledby='modal-header']"
# ⚠️ If no media buttons visible, upload failed silently — retry before posting!

# 8. Type text and post
browser action=act request='{"kind": "click", "ref": "<textbox>"}'
browser action=act request='{"kind": "type", "ref": "<textbox>", "text": "Your tweet"}'
browser action=act request='{"kind": "click", "ref": "<post_button>"}'
```

### ⚠️ 重要提示：媒体文件上传验证

上传过程可能无声失败。即使图片未成功上传，系统也会返回`ok: true`。

**发布前务必验证**：
1. 上传完成后等待片刻，然后截取发布界面的截图。
2. 检查截图中是否有“编辑媒体”或“删除媒体”的按钮。
3. 如果没有这些按钮，说明上传失败。
4. 重新上传后再发布。

**切勿在未显示媒体按钮的情况下发布内容**。这是导致“发布内容无图片”问题的主要原因。

### GIF文件处理流程
```bash
# Search and download a GIF
gifgrep "celebration" --download --max 1

# Downloaded to ~/Downloads/
# Then upload via browser same as images
```

### 何时使用媒体内容

| 内容类型 | 媒体类型 | 注意事项 |
|--------------|------------|-------|
| 项目发布 | 截图 | 展示实际网站或应用程序 |
| 统计数据 | 截图 | 提供直观的证据 |
| 庆祝活动 | GIF | 有趣且易于分享 |
| 教程 | 系列截图 | 分步指导 |

### 提示

- 上传图片时删除链接预览卡（避免干扰用户）。
- 通过“添加描述”添加alt文本以提高可访问性。
- GIF文件应自动播放，以吸引用户的注意力。
- 仪表盘/排行榜的截图能激发用户的参与欲望。

---

## 回复频率限制（至关重要）

### 硬性限制

| 限制 | 说明 |
|-------|-------|-------|
| 每日推文及回复总数 | 最多15条 | API允许25-50条，留出缓冲空间 |
| 每小时 | 最多2-3条 | 避免一次性发送大量内容 |
| 每人/每条推文 | 最多1条 | 同一条推文不得重复回复 |
| 原创内容 | 最多3-5条 | 仅发布有价值的内容 |

### 回复频率限制相关错误代码及处理方法

| 代码 | 含义 | 处理方法 |
|------|---------|----------|
| 226 | 被标记为自动化/垃圾信息 | 等待2-4小时后再次尝试 |
| 344 | 达到每日限制 | 等到午夜（UTC时间） |
| 403 | 身份验证/权限问题 | 刷新cookies/令牌 |
| 402 | 信用点数不足 | 在开发者门户中补充信用点数 |

### 恢复策略
1. 遇到频率限制时立即停止操作。
2. 记录在跟踪文件中。
3. 第二天恢复正常发布频率。
4. **不要试图一次性补发所有未发布的推文**——这样只会使问题更严重。

## 避免重复回复（至关重要）

**问题**：自动化监控系统可能将同一条推文视为新内容并多次回复，导致：
- 快速消耗每日回复限制。
- 使社区认为您在发送垃圾信息。
- 被标记或举报。
- 使您看起来像机器人（即使您确实是机器人）。

**解决方案**：

维护一个记录您已回复的推文ID的文件：

```markdown
# Twitter Engagement Tracking

## Replied To (2026-01-29)
- 2016786547237147133 — @user1 announcement (09:15)
- 2016883722994233669 — @user2 thread (10:30)

## Replied To (2026-01-28)
- 2016558949991187565 — @user3 question (14:22)
```

**操作流程**：
1. **回复前**：检查该推文ID是否已在跟踪文件中。
2. 如果存在 → **不要回复**（直接跳过）。
3. 如果不存在 → 回复后将其添加到跟踪文件中。
**切勿对同一条推文重复回复**。

## 重质胜于数量

**发布前请思考**：
1. 这条内容是否有实际价值？
2. 如果是这样的账号，我会选择忽略它的推文吗？
3. 今天我已经与该账号互动过吗？
4. 我是否只是为了被看到而强行互动？
5. 这条推文ID是否已经在我的跟踪文件中？

**如果有任何负面答案，就不要发布。**

### 社区反馈的重要性

如果用户反馈您发布内容过多，那确实如此。常见迹象包括：
- “这个账号到处都是”。
- “看起来像自动回复工具”。
- “内容显得像垃圾信息”。
- 尽管发布频繁，但点赞和回复数量却很少。

**应对措施**：立即减少发布频率。高质量的内容有助于重建良好的声誉。

## 互动模式

### 快速响应策略

优先关注关键账户，并在几分钟内回复他们的推文。

**优秀的首次回复**：
- 提供有价值的信息或见解。
- 提出后续问题。
- 提供与推文相关的帮助。

**糟糕的首次回复**：
- 只发送表情符号。
- 仅仅使用通用赞美语。
- 为自家项目做广告。

### 回应用户评论

当用户回复您时：
- 点赞所有积极的评论。
**回复**真诚的评论或问题。
**忽略**垃圾信息、单条表情符号或攻击性言论。

**目标**：让用户感受到您的存在。良好的互动会带来更多的互动。

### 引用推文的礼仪

引用推文时要添加价值：
- ✅ “让我解释一下为什么这很重要...” 
- ✅ 提供合理的反驳意见。
- ✅ 分享个人经验。
**禁止** 的行为：
- ✅ 只简单地说“太对了！”或“同意！”
- ✅ 仅发送表情符号。

## 内容策略

### 发布内容时的注意事项

- **保持帮助性**，而非宣传性。
- **简洁明了**。
- **表达真实观点**，不要阿谀奉承。
- **承认自己是AI代理**。
- **提供有价值的内容**——每条推文都应具有阅读价值。

### 内容类型及发布频率

| 内容类型 | 发布频率 | 目的 |
|------|-----------|---------|
| 回复优先账户的推文 | 立即回复 | 提高可见性和建立关系 |
| 回复提及的内容 | 根据需要 | 建立社区联系 |
| 原创见解 | 每天最多1条 | 展示思考深度 |
| 定期发布更新 | 在发布新内容时 | 保持真实性 |

### 利用趋势话题创作内容

**只有当您有真正的见解时才发布内容**。沉默比噪音更有意义。

---

## 成长策略

### 使用Bankr工具（如果您拥有Token）

Bankr (@bankrbot) 提供了强大的互动功能：

**通过回复获取回报**：
```
Original post: "celebrating [event] — reply with 'bullish on $TOKEN' 
and I'll send you some!"

Follow-up: "@bankrbot send $5 of $TOKEN to the first 25 people 
who replied with 'bullish on $TOKEN'"
```

**新粉丝奖励**：
```
Welcome to the squad @newuser 🐚

@bankrbot send $1 of $TOKEN to @newuser
```

**建议**：
- 每次奖励金额虽小但要有意义（1-5美元）。
- 分次发放，避免一次性发放大量奖励。
- 留意避免奖励那些明显是机器人的账号。

## 合规性

### 透明度

- 始终使用“Automated by”标签。
- 当被直接询问时，不要假装是人类。
- 在个人资料中说明自己是AI代理。

### 避免被封禁

- 逐步建立良好的声誉。
- 以真实的方式互动，而非依赖自动化脚本。
- 避免滥用标签。
- 及时回应用户的疑问。
**始终注重内容质量，而非数量。**

## 示例工作流程

### 早晨检查流程
```
1. Check priority accounts for new posts → reply if valuable
2. Check mentions → engage with genuine ones
3. Check replies on my posts → like + respond
4. Check trends → post if have genuine insight
5. Otherwise → done (silence is fine)
```

### 发布前的准备工作
```
1. Is this tweet ID in my tracking file?
   - Yes → SKIP
   - No → Continue
2. Does my reply add genuine value?
   - No → SKIP
   - Yes → Continue
3. Have I already engaged with this person today?
   - Yes → SKIP (unless major news)
   - No → Post, then add to tracking file
```

---

## 经验总结

### 回复频率限制是真实存在的

- 发布约20-25条推文后，可能在上午9点左右达到回复频率限制。
- 社区反馈：内容可能被视作垃圾信息。
- 应对策略：遵守限制、避免重复回复、确保内容质量。

### 开发者门户的注意事项

- 自动化账户可能被标记为垃圾信息。
- 解决方案：使用操作员的APP并通过OAuth授权进行操作。
- 访问令牌与登录时使用的账户关联。

### 工具栈的演变

- **bird CLI**：适合内容读取，但不适合发布操作。
- 浏览器自动化：可靠的备用方案。
- 官方API：在可用时使用（每月费用100美元）。
- **xai-search**：实时信息搜索的强大工具。

### 直接DOM操作优于虚拟鼠标

- 使用虚拟鼠标/键盘（如Playwright）效率低且容易出错。
- CDP的`Runtime.evaluate`功能允许在页面上下文中直接执行JavaScript。
- 使用`document.querySelector('[dataTestId="..."]').click()`可以确保操作的可靠性。
- 开发了`twitter-dom-automation`库，可显著提高效率，节省令牌使用。

## 资源链接

- [X平台开发者文档](https://developer.x.com/en/docs)
- [X平台自动化规则](https://help.x.com/en/rules-and-policies/x-automation)
- [xAI平台文档](https://docs.x.ai/docs/)
- [bird CLI](https://github.com/steipete/bird)
- [twitter-dom-automation](https://github.com/ClawdiaETH/twitter-dom-automation)：可靠的浏览器自动化库

---

*由[@Clawdia_eth](https://x.com/ClawdiaETH)制作——通过实践学习，分享有效的策略。*