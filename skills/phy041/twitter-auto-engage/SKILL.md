---
name: twitter-auto-engage
description: 这是一个自动化的Twitter/X互动脚本，它能够扫描预先筛选好的目标账户列表，生成由GPT（Generative Pre-trained Transformer）生成的真实回复，并通过Twitter的GraphQL API将这些回复发布出去。当你希望定期执行互动任务时，可以使用这个脚本——通过高质量、不谄媚的回复来提升你在特定领域内的影响力（即与行业内的意见领袖进行有效互动）。
metadata: {"requires": ["python3", "openai", "rnet_twitter"], "env": ["OPENAI_API_KEY", "TWITTER_COOKIE_PATH"], "tags": ["twitter", "social-media", "engagement", "automation", "openai", "gpt"]}
---
# 自动参与 Twitter 互动

这是一个自动化系统，用于与 Twitter/X 上的目标账户互动。它会扫描这些账户，挑选出互动量最高的最新推文，利用 GPT 生成符合语境的回复，并以类似人类的时机发布这些回复。该系统专为希望通过真诚的技术交流来扩大影响力的创始人及开发者设计，而非通过吸引粉丝来提升知名度。

## 必需条件

```bash
pip install openai
# rnet_twitter — async Twitter GraphQL client (see rnet_twitter.py)
```

您还需要以下资源：
- 一个有效的 Twitter/X 会话 cookie 文件（`twitter_cookies.json`）
- 一个 OpenAI API 密钥

## 设置

```bash
export OPENAI_API_KEY="your_openai_api_key"
export TWITTER_COOKIE_PATH="/path/to/twitter_cookies.json"
```

该脚本会从已登录浏览器会话导出的 JSON 文件中读取 cookie。详情请参阅 [获取 Twitter Cookie](#obtaining-twitter-cookies)。

## 使用方法

```bash
# Run a single engagement session (5 replies max)
python auto_engage.py

# Schedule 4x daily via cron (recommended)
# Morning, midday, afternoon, evening sessions
0 8,12,16,21 * * * cd {skillDir} && python auto_engage.py >> logs/engage.log 2>&1
```

## 配置

在脚本顶部修改以下常量以自定义其行为：

| 常量 | 默认值 | 说明 |
|----------|---------|-------------|
| `TARGETS_PER_RUN` | 20 | 每次会话检查的账户数量 |
| `MAX_REPLIES_PER_RUN` | 5 | 每次会话最多发布的回复数量 |
| `RUN_PROBABILITY` | 0.85 | 随机跳过某些账户的概率（模拟人类行为的随机性） |
| `MIN_REPLY_LENGTH` | 80 | 回复的最小字符数 |
| `MAX_REPLY_LENGTH` | 260 | 回复的最大字符数 |

## 目标账户池

将账户分为不同的类别，并为每个类别设定每次会话的访问配额。脚本会在每次会话中从所有账户中随机选取 `TARGETS_PER_RUN` 个账户进行互动。

示例结构：

```python
TARGET_POOL = {
    "ai_builders": [
        "simonw",     # Example: ML tools, Datasette
        "swyx",       # Example: AI engineering
    ],
    "indie_builders": [
        "dvassallo",  # Example: indie hacker
        "tdinh_me",   # Example: bootstrapped SaaS
    ],
    "marketing": [
        "harrydry",   # Example: Marketing Examples
        "wes_kao",    # Example: content strategy
    ],
}

CATEGORY_QUOTAS = {
    "ai_builders":   2,  # replies per session
    "indie_builders": 2,
    "marketing":     1,
}
```

请将账户名称替换为您所在领域和目标相关的账户名称。

## 回复生成

回复内容由 GPT 根据结构化的语境提示生成。系统遵循以下规则：

### 语境提示规则（可配置）：
- 使用直接、清晰的句子，避免使用填充词
- 使用具体、明确的词汇（如数字、工具名称、具体观察结果）
- 保持好奇心和求知欲，提出真实的问题（而非反问句）
- 能够坦诚地面对不确定性和失败

### 内置过滤规则
如果生成的回复包含以下内容，系统会拒绝并跳过该回复：
- 过分谄媚的开场白（如“很棒的帖子”、“喜欢这个”、“太对了”等）
- 随意的俚语（如 lol、damn、wild、ngl、fr、bro、lowkey、fire、bussin、no cap）
- 任何 Unicode 字符码大于 U+1F600 的表情符号
- 感叹号（可配置的容忍度）
- 公司式的语言（如 leverage、synergy、paradigm、game-changer）
- 自我推广或提及产品名称

### 三种回复类型
GPT 会被提示选择以下三种回复类型之一：

**A) 深入见解 + 问题**
分享您自己的经验中的具体观察结果，然后提出一个您真正想得到答案的问题。
> “我们在开发品牌工具时遇到了一个问题：如果 3 个月后不重新训练，模型的嵌入效果会下降约 15%。你们多久会重新调整模型参数一次？”

**B) 尊重的反驳**
用数据或反例礼貌地提出异议，然后邀请对方分享他们的观点。
> “相反的观点是：Stripe 的文档确实很棒，但他们仍然需要销售团队来服务企业客户。真正的问题不应该是‘自助服务在什么情况下会失效’吗？”

**C) 模式识别**
将对方的观点与另一个领域的现象联系起来。
> “这和推荐系统的情况类似——Netflix 发现，为了提高点击率而优化反而降低了用户留存率。你们是如何解决这个问题的？你们有没有类似的‘观看时长’这样的指标？”

## 自定义语境描述

请修改 `USER_CONTEXT` 变量（或相应的提示内容），以准确描述您的背景信息：

```python
USER_CONTEXT = """You are writing a Twitter reply as YOUR_NAME.

BACKGROUND:
- Brief description of who you are
- What you're building
- Genuine interests relevant to the accounts you target

VOICE:
- [Your preferred communication style]
- [Specific things to include or avoid]
"""
```

您提供的语境描述越具体、越真实，生成的回复就越贴切。

## 状态管理

脚本使用 `auto_reply_state.json` 文件来记录已回复的推文 ID，以防止在不同会话中重复回复同一条推文：

```json
{
  "replied_tweets": ["tweet_id_1", "tweet_id_2"],
  "last_updated": "2026-03-06T09:30:00"
}
```

状态记录最多保存最近 100 条推文的 ID，以避免数据无限增长。

## 互动逻辑

对于每个选定的账户，脚本会执行以下操作：
1. 获取该账户最近 10 条原始推文（不包括转发和 @ 回复）
2. 过滤掉已经被回复过的推文 ID
3. 选择互动量最高的推文（点赞数 + 回复数最多）
4. 使用 GPT 生成回复；如果 GPT 返回 `SKIP`，则表示该推文已被查看并跳过
5. 先给推文点赞（点赞是一个算法生成的信号）
6. 发布回复
7. 等待 3-6 秒（模拟人类行为的延迟时间），然后再切换到下一个账户

## 输出结果

每次会话结束后，脚本会生成一个总结，并将其添加到日志文件中。当该脚本被机器人框架调用时，它会在 `---JSON_OUTPUT---` 分隔符后输出 JSON 数据，以便程序化处理：

```json
[
  {
    "target": "simonw",
    "tweet": "LLMs are increasingly being used for...",
    "reply": "The retrieval side of this is underrated...",
    "url": "https://x.com/simonw/status/...",
    "liked": true
  }
]
```

## 获取 Twitter Cookie 的方法

1. 在 Chrome 或 Firefox 浏览器中登录 Twitter/X
2. 打开开发者工具 > 应用程序 > Cookies > `https://x.com`
3. 将 cookie 数据导出为 `rnet_twitter.py` 脚本所需的 JSON 格式
4. 将文件保存在 `TWITTER COOKIE_PATH` 指定的路径下
请注意：不要将 cookie 文件提交到版本控制系统中。

## 速率限制规则
- 每次会话最多回复 5 条推文，每天最多进行 4 次会话，因此每天最多回复 20 条
- 每次会话有 85% 的概率执行互动操作，以模拟人类行为的随机性
- 每条回复之间有 3-6 秒的延迟
- 同一条推文的点赞和回复之间有 1-2 秒的延迟

Twitter 对回复操作的具体限制并未公开说明，但每天回复不超过 50 条，并分散在多个会话中执行，可以避免大部分问题。

## 故障排除
- **回复未发布**：请确认您的 cookie 文件是最新的。Twitter 会话会过期，请重新从浏览器中导出 cookie 数据。
- **GPT 始终返回 `SKIP`**：可能是 `USER_CONTEXT` 与目标账户的信息不匹配。请确保您提供的背景信息足够让 GPT 理解讨论的主题。
- **频繁出现谄媚性回复**：可能是 GPT 默认使用了过于谄媚的开场白。您可以增加提示内容中对禁止内容的强调，或者稍微降低系统的活跃度。
- **账户被标记或受到 Twitter 限制**：将 `MAX_REPLIES_PER_RUN` 减少到 3，`RUN_PROBABILITY` 减少到 0.6，以降低交互频率。