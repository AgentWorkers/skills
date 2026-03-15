---
name: x-brand-operator
description: Automate X/Twitter brand account operations using OpenClaw native tools (xurl + browser fallback + cron). Use when setting up or managing automated posting, keyword engagement, weekly reporting, or Substack content generation for a brand account. Triggers on: "set up X posting for [brand]", "automate my Twitter account", "schedule tweets", "keyword engagement on X", "brand social media automation".
---

# X品牌运营工具

利用xurl（X API v2）实现X/Twitter品牌账户的端到端自动化操作，同时提供浏览器作为备用方案。除了xurl应用配置外，无需额外API密钥。

## 核心工具

- `xurl --app <app>` — 通过X API v2发布内容、回复、点赞、关注、搜索
- `browser` — 当xurl失败时，使用浏览器作为备用方案（操作者账号）
- `cron` — 安排重复性任务（发布内容、互动、生成报告）
- `message` — 在任务失败或完成时发送Telegram通知

## 发布推文

**主要方式（使用xurl）：**
```bash
xurl --app <app> post "<tweet text>"
```

**备用方案（仅当xurl失败时使用浏览器）：**
1. 打开浏览器，访问 `https://x.com/compose/post`（操作者账号）
2. 等待4秒
3. 保存当前页面截图
4. 点击文本输入框，输入推文内容
5. 保存页面截图
6. 点击“发布”按钮
7. 保存页面截图，确认操作成功

**规则：** 每种方法仅尝试一次。如果失败，通过Telegram发送通知（包含草稿内容），然后退出程序。切勿无限循环尝试。

## 回复推文

**主要方式：** `xurl --app <app> reply <tweet_id> "<回复内容>"`

**备用方案：** 在浏览器中打开目标推文链接，保存页面截图，点击“回复”，输入回复内容后提交。

## 内容质量标准（发布前需满足的分数）

| 评估标准 | 权重 |
|-----------|--------|
| 内容吸引力 | 25分 |
| 信息密度 | 25分 |
| 与平台契合度 | 20分 |
| 呼吁行动的清晰度 | 15分 |
| 简洁性 | 15分 |

**最低分数要求：70/100分**。如果得分低于此标准，需重新编写内容；如果仍然无法发布，则放弃此次操作。

**格式要求：** 单段文本，无换行，字符数不超过280个，使用1-2个标签，结尾处附上品牌官网链接。

## 内容主题轮换（每日发布）

根据不同时间安排发布不同主题的内容。具体主题、模板和风格指南请参阅 `references/content-strategy.md`。内容应符合品牌定位。

## 关键词互动（每周进行）

搜索目标关键词，筛选真实用户发布的推文（排除机器人或广告），然后对推文进行点赞、回复和关注。

**回复内容的质量要求：**
- 首先回应用户的痛点
- 添加2-4句有实际价值的内容
- 自然地提及品牌（避免强行推广）
- 绝不要使用“很棒的文章！”或“太对了！”之类的敷衍语句

关键词列表和回复模板请参阅 `references/engagement-playbook.md`。

## Cron作业设置

推荐的时间表及代理任务模板请参阅 `references/cron-config.md`：
- 每日14:00发布早晨内容
- 每日20:00发布晚间内容
- 每周一10:00进行关键词互动
- 每周三13:00生成Substack文章草稿
- 每周日21:00生成每周报告

## 故障处理

| 故障情况 | 处理措施 |
|-----------|--------|
| xurl失败 | 立即切换到浏览器备用方案 |
| 浏览器也失败 | 发送包含草稿内容的Telegram通知，然后退出程序 |
| 互动过程中的任何步骤失败 | 跳过当前步骤，继续执行下一个任务 |
| 每次操作结束后 | 发送Telegram总结通知 |

每种方法最多尝试一次，切勿无限循环尝试。