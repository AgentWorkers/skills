---
name: linkedin-automation
description: LinkedIn自动化工具：支持发布内容（包含图片上传）、发表评论（可@提及他人）、编辑/删除评论、重新发布内容、查看动态流、分析用户互动数据、监控点赞情况、跟踪用户参与度，以及管理内容发布的审批流程。该工具基于Playwright框架开发，能够持久化保存浏览器会话状态。适用于各种LinkedIn相关任务，包括内容策略制定、定时发布内容、分析用户互动情况以及提升受众规模。
---

# LinkedIn自动化

> **作者：**社区贡献者

>
> ⚠️ **免责声明 — 仅限个人使用**
> 本技能仅用于**个人、非商业用途**。它可自动化您的LinkedIn账户，提升个人的生产力和互动效率。请勿将此技能用于发送垃圾信息、大规模联系用户、抓取其他用户的数据或任何商业自动化服务。请负责任地使用，并遵守[LinkedIn的用户协议](https://www.linkedin.com/legal/user-agreement)。作者对滥用或账户被封禁的情况不承担任何责任。

通过无头Playwright浏览器和持久会话来自动化LinkedIn上的互动。

## 先决条件

- 安装了Python 3.10及Playwright（`pip install playwright && playwright install chromium`）
- 已登录的LinkedIn浏览器会话（持久的Chromium配置文件）
- 根据您的设置调整`scripts/lib/browser.py`中的路径

## 命令

```bash
CLI={baseDir}/scripts/linkedin.py

# Check if session is valid
python3 $CLI check-session

# Read feed
python3 $CLI feed --count 5

# Create a post (text only)
python3 $CLI post --text "Hello world"

# Create a post with image (handles LinkedIn's image editor modal automatically)
python3 $CLI post --text "Hello world" --image /path/to/image.png

# Comment on a post (supports @Mentions — see below)
python3 $CLI comment --url "https://linkedin.com/feed/update/..." --text "Great insight @Betina Weiler!"

# Edit a comment (match by text fragment)
python3 $CLI edit-comment --url "https://..." --match "old text" --text "new text"

# Delete a comment
python3 $CLI delete-comment --url "https://..." --match "text to identify"

# Repost with thoughts
python3 $CLI repost --url "https://..." --thoughts "My take..."

# Engagement analytics for recent posts
python3 $CLI analytics --count 10

# Profile-level stats (followers, views)
python3 $CLI profile-stats

# Monitor your likes for new ones (for comment suggestions)
python3 $CLI scan-likes --count 15

# Scrape someone's activity
python3 $CLI activity --profile-url "https://linkedin.com/in/someone/" --count 5
```

所有命令的输出均为JSON格式。启用调试日志记录：`LINKEDIN_DEBUG=1`。

## @提及

评论支持`@FirstName LastName`的语法。该技能：
1. 输入`@FirstName`后，会等待自动完成输入的姓氏选项；
2. 如需要，会逐个输入姓氏的字母；
3. 仅当名字和姓氏都匹配时才会点击对应的链接；
4. 如果找不到匹配的人，会返回`mention_failed`的警告。

请在JSON结果中查看`mentions`字段，以确认提及操作是否成功。

## 点赞监控

`scan-likes`命令会检查您最近的点赞/互动记录，并返回**自上次检查以来的新点赞**。为了避免重复提醒，系统会保留这些信息。非常适合与cron/心跳任务集成：

```
# In HEARTBEAT.md or cron job:
python3 $CLI scan-likes → if new likes found → suggest comment for each
```

## ⚠️ 重要规则

**未经用户明确同意，切勿发布、评论、转发、编辑或删除任何内容。**

在执行任何操作前，务必向用户明确展示将要显示的内容，并获得用户的明确许可。只读操作（如查看动态、分析数据、检查会话状态、扫描点赞记录）可以自由执行。

## 内容日历（定时发布）

基于用户批准的完整发布流程，支持自动发布。详情请参阅**[references/content-calendar.md]**。

- **Webhook**（`scripts/cc-webhook.py`）：从前端UI接收批准/编辑/跳过的指令；
- **自动应用**：简单的编辑（如“旧文本 → 新文本”）会通过Webhook立即生效；
- **代理处理**：复杂的编辑内容会由AI进行文本重写；
- **自动发布**：已批准但未在预定时间发布的帖子会通过cron任务自动发布；
- **图片策略**：使用真实照片和AI生成的故事叠加层（而非库存图片）。

```bash
# Start the webhook (or install as systemd service)
python3 scripts/cc-webhook.py

# Env vars for config:
# CC_DATA_FILE=/path/to/cc-data.json
# CC_ACTIONS_FILE=/path/to/actions.json
# CC_WEBHOOK_PORT=8401
```

## 内容策略与互动

- **[references/content-strategy.md]** — 发布策略、帖子结构、发布时间、标签策略、4-1-1规则
- **[references/engagement.md]** — 算法提示、评论质量标准、频率限制、每周例行任务
- **[references/dom-patterns.md]** — LinkedIn的DOM模式解析，用于故障排除
- **[references/content-calendar.md]** — 内容日历设置、数据格式、Webhook API

## 频率限制

| 操作 | 每日最大次数 | 每周最大次数 |
|--------|----------|-----------|
| 发布帖子 | 2–3次 | 10–15次 |
| 评论 | 20–30次 | — |
| 点赞 | 100次 | — |
| 添加好友请求 | 30次 | 100次 |

## 设置步骤

1. 安装依赖项：`pip install playwright && playwright install chromium`
2. 在`scripts/lib/browser.py`中配置浏览器配置文件路径（或设置`LINKEDIN_BROWSER_PROFILE`环境变量）
3. 手动登录LinkedIn一次（会话会持续保存）
4. 运行`python3 scripts/linkedin.py check-session`进行验证
5. **学习您的发言风格**：运行`python3 scripts/linkedin.py learn-profile`——该脚本会扫描您最近的帖子和评论，以学习您的发言风格、主题、语言和表达方式。代理在生成评论或帖子时将使用此配置文件，确保内容听起来像您本人，而非机器人。

## 语音与风格

在首次设置时，`learn-profile`会分析您的内容并生成一个风格配置文件（`~/.linkedin-style.json`），其中包含：
- **语言**（德语/英语/混合）
- **语气**（随意/正式/友好）
- **表情符号的使用频率**（高/中等/低）
- **您常用的标签**
- **用于参考的样例帖子和评论**

代理在生成任何评论或帖子建议前，必须始终读取此配置文件（`get-style`）。切勿强行使用与用户风格不符的语气。

## 帖子发布时间警告

**重要提示：**在建议对任何帖子发表评论之前，请检查帖子的发布时间：
- **< 2周**：可以安全地发表评论；
- **> 2周**：请明确告知用户（“⚠️ 这篇帖子已发布X周了——在旧帖子上评论可能会被误认为是机器人行为。您仍要评论吗？”）；
- **> 1个月**：除非有特殊原因，否则强烈建议不要评论。

在旧帖子上评论可能会让人觉得您像是在用机器人刷数据。务必标记帖子的发布时间。

## 故障排除

- **会话过期**：通过浏览器配置文件重新登录；
- **选择器失效**：LinkedIn的UI经常更新——请查看`references/dom-patterns.md`并更新`scripts/lib/selectors.py`；
- **调试截图**：失败时截图会保存在`/tmp/linkedin_debug_*.png`文件夹中。