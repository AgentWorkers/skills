# OpenClaw 生态系统新闻

**版本：** 1.0.0  
**作者：** OpenClaw 社区  
**标签：** 新闻、监控、生态系统、GitHub、社区  
**注册地址：** https://www.clawhub.ai  

## 功能简介  
该工具将 OpenClaw 生态系统中的重要新闻和动态汇总成一份简洁、精选的简报，仅呈现关键信息，排除无关内容。  

**跟踪的类别包括：**  
- 🚀 **OpenClaw 新版本**：`openclaw/openclaw` 仓库中的新版本、标签及重要 Pull Request  
- 🧩 **ClawdHub 技能**：注册库中最近发布或更新的技能  
- 🔒 **安全警告**：CVE（安全漏洞）及相关讨论  
- 💬 **社区动态**：Hacker News 的帖子、Reddit 的讨论内容以及值得关注的 Twitter 文章  
- 📰 **生态系统新闻**：主流媒体的报道、新的集成功能及平台更新  
- 🐛 **Moltbook 热门内容**：来自代理社交网络的最新帖子（如可用）  

## 设置要求  

### 先决条件  
- 安装并登录 `gh` CLI（用于访问 GitHub API）  
- 安装 `clawdhub` CLI（用于查询技能注册库）  
- 安装 `jq`（用于处理 JSON 数据）  
- 通过代理工具启用 Brave Search（用于网络搜索）  

### 安装步骤  
将此技能复制到您的工作区：  
```
skills/openclaw-news/
├── SKILL.md              # This file
├── scripts/
│   ├── collect_news.sh   # Main data collection script
│   └── format_briefing.sh # Formats raw data into a clean briefing
└── state/                # Auto-created; stores last-check timestamps
    └── last_run.json
```  

### 定时任务设置  
- **每日简报（上午 9 点）：**  
  ```
openclaw cron add --name "openclaw-news" \
  --schedule "0 9 * * *" \
  --prompt "Run the OpenClaw Ecosystem News skill. Execute scripts/collect_news.sh from skills/openclaw-news/, then format and deliver the briefing." \
  --channel signal
```  
- **每日两次简报（上午 9 点和下午 5 点）：**  
  ```
openclaw cron add --name "openclaw-news" \
  --schedule "0 9,17 * * *" \
  --prompt "Run the OpenClaw Ecosystem News skill. Execute scripts/collect_news.sh from skills/openclaw-news/, then format and deliver the briefing." \
  --channel signal
```  

## 使用方法  

### 自动更新（通过 Cron 任务）  
设置好定时任务后，简报会按计划发送。脚本会检查 `state/last_run.json` 文件中的已有内容，仅显示更新的部分。  

### 按需获取简报  
当用户询问“OpenClaw 有什么新动态？”时：  
1. 从技能目录运行 `scripts/collect_news.sh`  
2. 运行 `scripts/format_briefing.sh` 生成简报  
3. 将简报内容传递给用户  

代理也可以直接使用脚本的输出结果，并以适合对话的形式进行展示。  

### 差异更新模式  
脚本会自动与上一次运行结果进行对比。如需强制进行全面扫描（忽略之前的数据），可删除 `state/last_run.json` 文件或使用 `--full` 参数：  
```bash
cd skills/openclaw-news
./scripts/collect_news.sh --full
```  

## 简报格式  
```
📡 OpenClaw Ecosystem News — Jun 14, 2025

🚀 RELEASES
• v0.9.2 released — WebSocket stability fixes, new `canvas` action
  https://github.com/openclaw/openclaw/releases/tag/v0.9.2

🧩 NEW SKILLS
• weather-alerts v2.1.0 — Added severe weather push notifications
• home-inventory v1.0.0 — Track household items with camera snaps

🔒 SECURITY
• Nothing new — all clear ✅

💬 COMMUNITY
• HN: "OpenClaw is the missing layer for personal AI" (142 points)
  https://news.ycombinator.com/item?id=...

📰 ECOSYSTEM
• Fortune: "The rise of always-on AI agents" (mentions OpenClaw)

—
Last checked: Jun 13, 2025 09:00 ET
Sources: GitHub, ClawdHub, Brave Search, Moltbook
```  

## 代理使用建议  
在发送简报时：  
- **短信/信号通知**：以简洁的形式发送  
- **Discord**：内容可稍长一些；如支持嵌入功能可适当使用  
- **Telegram**：Markdown 格式适用  
- 空章节可省略（无需每类都写“无新内容”）  
- 如果一切正常，只需发送一句话：“📡 今日 OpenClaw 生态系统无重要动态。”  

## 数据来源  
| 数据来源 | 获取方式 | 数据频率限制 |  
|--------|--------|-------------|  
| GitHub 新版本 | `gh` CLI | 每小时 5000 次请求（已登录用户） |  
| GitHub 问题/PR | `gh` CLI | 同上 |  
| ClawdHub 注册库 | `clawdhub explore` | 低频请求 |  
| 网络新闻 | Brave Search API | 根据需求设置 |  
| Moltbook | API（若可用） | 视情况而定 |  
| Reddit | Brave Search | 根据需求设置 |  
| Hacker News | Brave Search / API | 高频获取 |  

## 适用场景  
该工具与 **fulcra-context** 配合使用效果更佳，可灵活控制新闻的推送时间和方式。例如，当用户正在专注工作或精力不足时，代理可以暂缓推送非紧急新闻或仅发送简短摘要，从而保持信息传递的高效性（无论是内容还是推送时机）。  

## 自定义设置  
您可以编辑 `scripts/collect_news.sh` 文件来：  
- 添加或删除需要跟踪的 GitHub 仓库  
- 调整社区动态的搜索条件  
- 设置数据回顾窗口（默认为自上次运行以来，首次运行时为 24 小时）  
- 添加自定义 RSS 源或其他数据源  

## 常见问题解决方法：  
- **无法获取 GitHub 数据**：运行 `gh auth status` 确保已成功登录  
- **无法获取 ClawdHub 数据**：检查 `clawdhub explore --registry https://www.clawhub.ai` 是否正常工作  
- **结果过时**：删除 `state/last_run.json` 以强制重新扫描  
- **简报为空**：若所有数据源均无内容，脚本会输出“今日无新动态”。