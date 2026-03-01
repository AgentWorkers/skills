---
name: xclaw
description: **XClaw 智能技能**：提供实时热门推文、KOL（关键意见领袖）深度分析、实时用户信息抓取、用户资料历史记录以及社交关系追踪功能。
allowed-tools: Bash(node:*) Read Write
metadata:
  {
    "openclaw": { "requires": { "env": ["CRYPTOHUNT_API_KEY"] } },
    "homepage": "https://pro.cryptohunt.ai",
    "codelink": "https://github.com/mookim-eth/xclaw-skill"
  }
---
# 技能：XClaw 智能分析 🚀

XClaw 是专为 OpenClaw 开发者设计的智能分析工具，能够实时获取来自 CryptoHunt 引擎的社交数据及洞察。

## 先决条件
- **需要 API 密钥**：请在您的环境中设置 `CRYPTOHUNT_API_KEY`。
- **获取 API 密钥**：您可以在 [apidashboard.cryptohunt.ai](https://apidashboard.cryptohunt.ai) 购买或注册 API 密钥。
- **官方 API 文档**：详细的端点文档请参阅 [pro.cryptohunt.ai](https://pro.cryptohunt.ai)。

## 核心功能

### 1. 热门趋势分析 (`xclaw_hot`)
- **操作**：获取过去 1 小时、4 小时或 24 小时内表现最佳的推文。
- **多维度过滤**：支持地区（`cn`/`global`）和标签（例如 `AI`、`meme`）的筛选。

### 2. 最新精简推文 (`xclaw_tweets`)
- **操作**：获取最新的 15-20 条推文，并对其进行优化处理（slimTweets），以便更高效地阅读。
- **兼容性**：旧的别名 `xclaw_analyze` 和 `xclaw_crawl` 仍然可用，它们会重定向到此功能。

### 3. 推文删除检测 (`xclaw_ghost`)
- **操作**：检测被特定用户删除的推文。

### 4. 账号信息追踪 (`xclaw_traces`)
- **操作**：检索特定用户的个人资料信息（简介、头像、名称）变更历史，以追踪其身份变化。

### 5. 社交动态 (`xclaw_social`)
- **操作**：跟踪特定用户最近的关注和取消关注操作。

### 6. 账号综合分析 (`xclaw_rank`)
- **操作**：提供全面的账户分析，包括排名、能力模型（六边形图表数据）、灵魂分数（soul score）和兴趣标签。

### 7. 推文详细信息 (`xclaw_detail`)
- **操作**：获取特定推文的所有内容、指标和线程数据。

### 8. 智能内容创意生成 (`xclaw_draft`)
- **操作**：根据地区和标签获取热门话题，生成具有原创链接的高转化率推文草稿。

## 用户命令示例
- `xclaw find hot`：获取过去 4 小时内中国地区的热门加密货币相关推文。
- `xclaw tweets <username>`：获取 @username 的最新精简推文。
- `xclaw analyze <username>` / `xclaw crawl <username>`：这些旧别名与 `xclaw tweets <username>` 的功能相同。
- `xclaw ghost <username>`：查看 @username 尝试删除了哪些推文。
- `xclaw traces <username>`：检查 @username 是否最近更改了个人资料信息。
- `xclaw social <username>`：查看 @username 最近关注或取消关注了哪些人。
- `xclaw rank <username>`：获取 @username 的灵魂分数、排名和能力模型。
- `xclaw detail <URL_or_ID>`：获取特定推文的所有详细信息和统计数据。
- `xclaw draft`：自动获取热门话题，并生成 3 个推文版本的建议。

---
*CryptoHunt 智能分析工具——专为创作者设计的数据服务。*

代码链接：https://github.com/mookim-eth/xclaw-skill