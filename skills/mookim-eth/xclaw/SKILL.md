---
name: xclaw
description: **XClaw 智能技能**：提供实时的热门推文、KOL（关键意见领袖）深度分析、实时用户信息抓取、用户资料历史记录以及社交关系追踪功能。
allowed-tools: Bash(node:*) Read Write
metadata:
  {
    "openclaw": { "requires": { "env": ["XCLAW_API_KEY", "CRYPTOHUNT_API_KEY"] } },
    "homepage": "https://pro.xclaw.info",
    "codelink": "https://github.com/mookim-eth/xclaw-skill"
  }
---
# 技能：XClaw 智能分析 🚀

XClaw 是专为 OpenClaw 开发者设计的高级智能分析工具，能够实时提供来自 XClaw 引擎的社会数据和分析洞察。

## 先决条件
- **需要 API 密钥**：请在您的环境中设置 `XCLAW_API_KEY`。（**注意**：`CRYPTOHUNT_API_KEY` 仅作为**过时**的选项提供，即将被弃用。请尽快切换到 `XCLAW_API_KEY`。）
- **获取密钥**：访问 [apidashboard.xclaw.info](https://apidashboard.xclaw.info)，并使用 Twitter 登录以获取**50 个免费信用点**。
- **官方 API 文档**：详细的端点文档请参见 [pro.xclaw.info](https://pro.xclaw.info)。
- **保持更新**：关注我们的 Twitter 账号 [@xclawlab](https://x.com/xclawlab) 以获取最新信息。

## 核心功能

### 1. 热门趋势分析 (`xclaw_hot`)
- **操作**：获取过去 1/4/24 小时内表现最佳的推文。
- **过滤**：支持按地区（`cn`/`global`）和标签（例如 `AI`、`meme`）进行过滤。

### 2. 最新推文 (`xclaw_tweets`)
- **操作**：获取带有智能过滤功能的最新推文。
- **默认设置**：包含原始推文、引用推文和转发推文，不包含回复推文。（默认为精简模式。）
- **选项**：
  - 使用 `--full` 选项可获取原始文本和 HTML 内容。
  - 使用 `--verbose` 选项可包含回复推文。
- **数量**：指定要获取的推文数量（例如：`xclaw tweets elonmusk 20`）。
- **兼容性**：支持旧版本别名 `xclaw_analyze` 和 `xclaw_crawl`。

### 3. 被删除推文分析 (`xclaw_ghost`)
- **操作**：查找被特定用户删除的推文。

### 4. 用户信息追踪 (`xclaw_traces`)
- **操作**：检索特定用户的个人资料信息（简介、头像、姓名）变化历史，以追踪其身份演变。

### 5. 社交动态 (`xclaw_social`)
- **操作**：跟踪特定用户的最近关注和取消关注操作。

### 6. 账号综合分析 (`xclaw_rank`)
- **操作**：提供全面的账号分析，包括排名、能力模型、灵魂分数和兴趣标签。

### 7. 推文详细信息 (`xclaw_detail`)
- **操作**：获取特定推文的全部内容、指标和线程数据。

### 8. 智能内容创意生成 (`xclaw_draft`)
- **操作**：根据地区和标签获取热门话题，生成具有原创链接的高转化率推文草稿。

## 用户命令示例
- `xclaw find hot`：获取过去 4 小时内的热门加密货币相关推文。
- `xclaw tweets <username>`：获取 @username 的最新推文（精简版）。
- `xclaw ghost <username>`：查看 @username 尝试删除的推文。
- `xclaw traces <username>`：检查该用户的个人资料历史记录。
- `xclaw social <username>`：查看 @username 最近关注或取消关注的对象。
- `xclaw rank <username>`：获取该用户的灵魂分数、排名和能力模型。
- `xclaw detail <URL_or_ID>`：获取特定推文的所有详细信息和统计数据。
- `xclaw draft`：自动获取热门话题素材，并建议 3 个推文版本。

---
*XClaw 智能分析——为开发者提供的数据支持。请关注 [@xclawlab](https://x.com/xclawlab) 以获取最新更新。*

代码链接：https://github.com/mookim-eth/xclaw-skill