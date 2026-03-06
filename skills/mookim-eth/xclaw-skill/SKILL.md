---
name: xclaw
description: **XClaw 智能技能**：提供实时热门推文、KOL（关键意见领袖）深度分析、实时用户行为追踪、用户资料历史记录以及社交关系监测功能。
allowed-tools: Bash(node:*) Read Write
metadata:
  {
    "openclaw": { "requires": { "env": ["CRYPTOHUNT_API_KEY"] } },
    "homepage": "https://pro.cryptohunt.ai",
    "codelink": "https://github.com/mookim-eth/xclaw-skill"
  }
---
# 技能：XClaw 智能分析 🚀

XClaw 是专为 OpenClaw 开发者设计的智能分析工具，能够实时提供来自 CryptoHunt 引擎的社会数据与洞察。

## 先决条件
- **需要 API 密钥**：请在您的环境中设置 `CRYPTOHUNT_API_KEY`。
- **获取 API 密钥**：您可以在 [apidashboard.cryptohunt.ai](https://apidashboard.cryptohunt.ai) 购买或注册 API 密钥。
- **官方 API 文档**：详细的端点文档请参阅 [pro.cryptohunt.ai](https://pro.cryptohunt.ai)。

## 核心功能

### 1. 热门趋势分析 (`xclaw_hot`)
- **操作**：获取过去 1/4/24 小时内表现最佳的推文。
- **多维度过滤**：支持地区（`cn`/`global`）和标签（例如 `AI`、`meme`）的筛选。

### 2. 最新推文 (`xclaw_tweets`)
- **操作**：通过智能过滤机制获取最新推文。
- **默认设置**：包含原始推文、引用推文和转发推文，不包含回复推文（默认为精简模式）。
- **选项**：
  - 使用 `--full` 可获取原始文本和 HTML 内容。
  - 使用 `--verbose` 可包含回复推文。
  - `Count`：指定要获取的推文数量（例如：`xclaw tweets elonmusk 20`）。
- **兼容性**：支持旧版别名 `xclaw_analyze` / `xclaw_crawl`。

### 3. 被删除的推文分析 (`xclaw_ghost`)
- **操作**：检测被特定用户删除的推文。

### 4. 账号信息追踪 (`xclaw_traces`)
- **操作**：检索特定用户的个人资料信息（简介、头像、名称）变化历史，以追踪其身份演变。

### 5. 社交动态 (`xclaw_social`)
- **操作**：跟踪特定用户的最近关注和取消关注操作。

### 6. 账号综合分析 (`xclaw_rank`)
- **操作**：提供全面的账号分析，包括排名、能力模型（六边形图表数据）、灵魂分数和兴趣标签。

### 7. 推文详细信息 (`xclaw_detail`)
- **操作**：获取特定推文的全部内容、指标和线程数据。

### 8. 智能内容生成 (`xclaw_draft`)
- **操作**：根据地区和标签筛选热门话题，生成具有原创链接的高转化率推文草稿。

## 用户命令示例
- `xclaw find hot`：获取过去 4 小时内中国的热门加密货币相关推文。
- `xclaw tweets <username>`：获取 @username 的最新推文（精简模式）。
- `xclaw analyze <username>` / `xclaw crawl <username>`：使用旧版别名，功能与 `xclaw tweets <username>` 相同。
- `xclaw ghost <username>`：查看 @username 尝试删除的推文。
- `xclaw traces <username>`：检查 @username 是否最近更改了个人资料或名称。
- `xclaw social <username>`：查看 @username 最近关注或取消关注了哪些用户。
- `xclaw rank <username>`：获取 @username 的灵魂分数、排名和能力模型。
- `xclaw detail <URL_or_ID>`：获取特定推文的全部详细信息和统计数据。
- `xclaw draft`：自动获取热门话题内容，并生成 3 个推文版本。

---
*CryptoHunt 智能分析工具——专为开发者设计的数据服务。*

代码链接：https://github.com/mookim-eth/xclaw-skill