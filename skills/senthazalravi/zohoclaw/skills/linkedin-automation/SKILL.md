---
name: linkedin-automator
description: 自动化LinkedIn内容的创建、发布、互动跟踪以及受众增长。该工具可用于发布内容、安排发布时间、分析互动数据、生成内容创意、对帖子进行评论，并提升在LinkedIn上的影响力。使用该工具需要浏览器访问，并确保LinkedIn账户已登录。
metadata: {"openclaw":{"emoji":"💼","requires":{"tools":["browser"]}}}
---

# LinkedIn 自动化工具

自动化您的 LinkedIn 活动：发布内容、跟踪用户互动、获取灵感并扩大受众群体。

## 先决条件

1. OpenClaw 中已启用浏览器工具。
2. 通过浏览器登录 LinkedIn（使用具有 LinkedIn 会话的账户）。

## 快速命令

```bash
# Post content
{baseDir}/scripts/post.sh "Your post content here"

# Post with image
{baseDir}/scripts/post.sh "Content" --image /path/to/image.png

# Get engagement stats for recent posts
{baseDir}/scripts/analytics.sh

# Generate content ideas based on trending topics
{baseDir}/scripts/ideas.sh [topic]

# Engage with feed (like/comment on relevant posts)
{baseDir}/scripts/engage.sh --limit 10
```

## 工作流程

### 发布内容

使用浏览器自动化功能发布内容：
1. 访问 linkedin.com/feed
2. 点击“开始发布”按钮
3. 在发布编辑器中输入内容
4. （可选）附加媒体文件
5. 点击“发布”按钮

对于定时发布的帖子，请使用 OpenClaw 的 cron 功能：
```
cron add --schedule "0 9 * * 1-5" --payload "Post my LinkedIn content: [content]"
```

### 内容策略

请参阅 [references/content-strategy.md](references/content-strategy.md)，了解：
- 高互动率的帖子格式
- 不同地区的最佳发布时间
- 标签策略
- 用于链接发布的模板

### 互动自动化

请参阅 [references/engagement.md](references/engagement.md)，了解：
- 评论模板
- 互动策略
- 增粉技巧

### 分析与跟踪

分析脚本可提取以下数据：
- 每条帖子的展示次数
- 互动率（点赞 + 评论 + 分享数 / 展示次数）
- 个人资料浏览量趋势
- 关注者增长情况
- 最受欢迎的内容主题

## 浏览器选择器

截至 2026 年，主要的 LinkedIn 选择器如下：

```
Post button: button[aria-label="Start a post"]
Post editor: div.ql-editor[data-placeholder]
Submit post: button.share-actions__primary-action
Like button: button[aria-label*="Like"]
Comment button: button[aria-label*="Comment"]
Profile stats: section.pv-top-card-v2-ctas
```

## 速率限制

LinkedIn 对用户活动有相应的限制，请遵守以下规则：
- 每天最多发布 2-3 条帖子
- 每天最多发表 20-30 条评论
- 每周最多发送 100 条好友请求
- 个人资料浏览量应保持自然浏览的速度

## 故障排除

- **需要登录**：确保浏览器中的个人资料具有有效的 LinkedIn 会话。
- **达到速率限制**：减少活动频率，等待 24 小时后再尝试。
- **选择器未找到**：可能是 LinkedIn 的用户界面发生了更新，请检查选择器是否仍然有效。