---
name: social-media-agent
description: 使用 OpenClaw 的原生工具实现 X/Twitter 的自动化社交媒体管理。适用于希望自动化发布内容、追踪用户互动、或扩大受众群体的用户。该工具可响应关于推文、社交媒体策略、X 社交媒体互动、内容计划或粉丝增长的请求。无需使用 API 密钥，仅依赖浏览器自动化技术和 web_fetch 功能即可完成操作。
---

# 社交媒体代理

仅使用 OpenClaw 的内置工具即可自主管理 X/Twitter 账户。无需外部 API、npm 包或 API 密钥。

## 核心工具

- `browser` — 发布推文、互动回复、截图
- `web_fetch` — 抓取个人资料、热门话题和新闻内容
- `sessions_spawn` — 并行生成内容
- `cron` — 安排定期发布和互动
- `memory_search` / files — 记录已发布的推文及互动数据

## 发布推文

1. 确保 Chrome 浏览器已开启远程调试功能，或使用 OpenClaw 的内置浏览器。
2. 访问 x.com/compose/post。
3. 截取屏幕截图以找到文本输入框。
4. 输入推文内容。
5. 点击“发布”按钮。
6. 通过再次截图验证内容是否正确。

```
browser open → x.com/compose/post
browser snapshot → find textbox ref
browser act → click textbox ref
browser act → type tweet text
browser snapshot → find Post button ref
browser act → click Post button
```

**重要提示：** 页面加载完成后请等待 3-4 秒再开始操作。

## 内容生成策略

### 内容分类
为了保持内容多样性，循环使用以下类别：

| 分类 | 比例 | 示例 |
|--------|---|---------|
| 行业洞察 | 40% | 人工智能新闻评论、技术分析 |
| 公开进展 | 30% | 项目进度更新、幕后花絮 |
| 哲学/思考 | 20% | 热门观点、引人深思的问题 |
| 互动/幽默 | 10% | 模因、回复、社区互动 |

### 内容生成流程

1. **研究：** 使用 `web_fetch` 从新闻网站（theverge.com、techcrunch.com、news.ycombinator.com）获取信息。
2. **生成：** 通过 `sessions_spawn` 使用研究结果生成推文内容。
3. **存储：** 将草稿保存到 `memory/tweet-drafts-YYYY-MM-DD.json` 文件中。
4. **审核：** 检查草稿的质量和品牌一致性。
5. **发布：** 使用浏览器自动化功能进行发布。
6. **记录：** 将发布的推文记录到 `memory/social-log.json` 中。

### 草稿格式

```json
{
  "text": "Tweet text under 280 chars",
  "topic": "What it's about",
  "hook": "Why it might engage"
}
```

## 互动策略

### 发布规则
- **每天最多发布 3-5 条推文** — 重质而非数量。
- **每次操作之间至少间隔 45 秒** — 避免被限制发送频率。
- **禁止发送垃圾信息** — 仅发布真实、有意义的互动内容。
- **全程记录：** 记录所有推文及互动数据。

### 增加粉丝数量

1. 持续发布内容（每天至少一次）。
2. 与相关账号互动（回复、引用推文）。
3. 在适当的情况下使用热门话题。
4. 保持真实性 — 避免使用通用的人工智能回复。

## 使用 Cron 安排任务

使用 `sessionTarget: "isolated"` 和 `payload.kind: "agentTurn"` 来设置自动发布任务。

## 应避免的行为

- **每天不要发布超过 5 条推文** — 否则可能被视为垃圾信息。
- **不要使用通用模板回复**（如“很棒的帖子！”“太对了！”）。
- **在未阅读评论内容的情况下不要回复**。
- **当浏览器自动化功能可用时，不要使用 API 密钥**。
- **如果 OpenClaw 的内置工具足够使用，就不要开发外部工具**。

## 分析与跟踪

在 `memory/social-log.json` 中记录互动数据：

```json
{
  "date": "2026-02-08",
  "posted": 3,
  "platform": "x",
  "handle": "@YourHandle",
  "tweets": [
    {"text": "...", "time": "09:00", "topic": "ai-news"}
  ]
}
```

每周检查：哪些话题获得了最多的互动？根据结果调整策略。

## 快速参考

有关详细的内容模板和示例，请参阅 [references/content-templates.md](references/content-templates.md)。