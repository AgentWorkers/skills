# ADHD X 书签分析工具

你的书签就像一个“信息坟场”……这个工具能让它们重新“活”过来！

## 该工具的功能

你每天会添加 50 条推特到 X 书签中，但可能只阅读其中 2 条而已。那个关于 20 万美元代理架构的讨论帖？被埋没了吧？那个能帮你节省大量时间的 AI 工具？也被忘掉了吧？

这个工具会将你 X 书签中的杂乱信息转化为可操作的智慧：它会自动抓取你的书签，按主题进行分类，提取关键信息，并将摘要发送到你指定的频道。

**再也不用面对书签的混乱了！** “我保存了关于……的资料”这样的烦恼也不存在了。现在，所有你认为值得保存的信息都变得井井有条、可搜索了。

**专为那些收集了大量信息却无法有效处理它们的 ADHD 用户设计。**

## 主要功能

- ✅ **自动抓取 X 书签**（可定时执行或按需触发）
- ✅ **智能分类**（按主题划分：AI、商业、工具、讨论帖等）
- ✅ **从讨论帖和长篇内容中提取关键信息**
- ✅ **将摘要发送到指定频道**（Discord、Slack、Telegram 或仅以文件形式）
- ✅ **可搜索的存档**：所有你保存的内容都可以轻松查找

## 使用要求

### X 账户认证（必备）

**推荐方案：`bird` CLI**
```bash
# Install bird CLI
npm install -g bird-cli

# Authenticate (opens browser for OAuth)
bird login

# Verify access
bird whoami
bird bookmarks --limit 5
```

认证信息会安全地存储在 `~/.bird/` 文件夹中，该工具不会直接处理原始的访问令牌。

**高级方案：浏览器会话**
如果你更喜欢使用浏览器缓存：
1. 在 Chrome/Safari 中登录 X 账户
2. OpenClaw 的浏览器插件可以访问你的会话信息
**注意：** 这种方式的可靠性较低，会话可能会过期，需要重新登录。

**安全提示：** 切勿将原始的会话 cookie 复制到配置文件中。请使用 `bird` CLI 进行安全的认证。

### 消息发送（可选）

若希望接收摘要信息，请通过 **环境变量** 进行配置（而非使用纯文本文件）：
```bash
# Discord (using OpenClaw's built-in message tool)
# No extra config needed — just specify channel ID in your prompt

# Or use a webhook (store securely):
export BOOKMARK_DISCORD_WEBHOOK="https://discord.com/api/webhooks/..."

# Slack
export BOOKMARK_SLACK_WEBHOOK="https://hooks.slack.com/services/..."
```

该工具会从环境变量中读取这些信息。**切勿将 Webhook 配置保存到文件中**。

## 安装方法

```bash
clawhub install adhd-bookmark-analyzer
```

或者你可以手动将工具复制到你的工作区：
```
~/.openclaw/workspace/skills/adhd-bookmark-analyzer/
├── SKILL.md           # This file (instructions for your agent)
├── bookmark-rules.md  # Categorization logic & settings
```

## 使用方法

### 按需分析

只需向工具发出指令：
```
"Analyze my X bookmarks from this week"
"What did I bookmark about AI agents?"
"Summarize my bookmarks and send to Discord"
```

工具会：
1. 运行 `bird bookmarks` 命令来获取你的书签信息
2. 根据 `bookmark-rules.md` 文件中的规则对书签进行分类和信息提取
3. 将摘要发送到你指定的频道（或直接回复给你）

### 定期每日报告

你可以通过 OpenClaw 的 cron 任务或 HEARTBEAT.md 文件来设置每日报告：
```
# Daily at 9 AM: Analyze yesterday's bookmarks
"Check my X bookmarks from the last 24 hours, categorize them, and post summary to Discord channel 123456789"
```

### 搜索存档

你可以搜索 `bookmark-archive/` 文件夹，找到相关的书签及其上下文信息。

## 示例输出
```
📚 X Bookmark Summary — Feb 15, 2026

You saved 18 bookmarks in the last 24 hours:

🤖 AI & Tech Tools (7)
• New Claude API pricing ($0.25/M output tokens)
• OpenClaw 0.7.0 release notes  
• Thread on RAG vs fine-tuning tradeoffs

💼 Business & Strategy (5)
• How @username built $50K MRR with AI agents
• Pricing psychology thread (15 tactics)
• Case study: AI replacing $200K/year ops role

🔧 Development & Code (4)
• Python async patterns for LLM calls
• GitHub repo: AI code review automation

📖 Threads Worth Reading (2)
• @username's 20-tweet thread on AI safety
• Founder story: 0 to $1M in 8 months
```

## 分类规则

`bookmark-rules.md` 文件中的默认分类规则如下：

| 分类 | 匹配条件 |
|---------|---------|
| AI 与技术工具 | 产品发布、工具评测、API 更新 |
| 商业与策略 | 成长策略、定价信息、案例研究 |
| 开发与代码 | 代码片段、代码仓库、技术讨论帖 |
| 值得阅读的讨论帖 | 长篇内容、故事分享 |
| 资源 | 书籍、课程、指南、列表 |
| 其他 | 无法归入上述分类的内容 |

**你可以自定义分类规则**，只需编辑 `bookmark-rules.md` 文件：
```yaml
categories:
  - name: "Indie Hacking"
    keywords: ["indie hacker", "SaaS", "MRR", "bootstrap"]
  - name: "Crypto Alpha"
    keywords: ["alpha", "degen", "airdrop", "farming"]
```

## 文件结构

运行该工具后，它会在你的工作区生成以下文件结构：
```
~/.openclaw/workspace/skills/adhd-bookmark-analyzer/
├── SKILL.md              # Instructions (this file)
├── bookmark-rules.md     # Categories & settings
└── bookmark-archive/     # Created by agent
    ├── 2026-02-15.json   # Daily snapshots
    └── index.json        # Searchable index
```

## 安全注意事项

1. **认证：** 使用 `bird` CLI 进行 X 账户认证。认证信息存储在 `~/.bird/` 文件夹中。
2. **Webhook：** 将 Discord/Slack 的 webhook 地址保存在环境变量中，而非配置文件中。
3. **数据存储：** 书签存档仅存储在你的本地工作区，不会发送到任何外部服务。
4. **权限：** 该工具仅读取你的书签信息并保存到本地存档，不会发布到 X 账户、修改书签内容或访问私信。

## 常见问题解决方法

**“找不到书签”**
- 确保已正确配置认证信息。
- 检查 `bookmark-rules.md` 文件中的分类关键词是否准确。
- 如果你有特定领域的需求，可以添加相应的分类关键词。

**希望仅以文件形式保存内容（无需通知）**
- 可以不配置 webhook。
- 可以让工具将内容仅保存到存档中。

## 使用建议

1. **大胆地添加书签**——该工具会帮你整理这些信息。
2. **每周查看一次摘要**——快速浏览并筛选出重要的内容。
3. **自定义分类规则**——让分类更符合你的需求。
4. **利用搜索功能**——你的存档会成为你的“第二大脑”。

---

**目标：** 在你需要时，能快速找到有用的信息。不要让书签堆积如山，让重要信息从海量信息中脱颖而出。