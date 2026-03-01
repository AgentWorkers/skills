---
name: xclaw
description: **XClaw 智能技能**：提供实时热门推文、KOL（关键意见领袖）深度分析、实时用户行为追踪以及已删除推文的检索功能。
allowed-tools: Bash(node:*) Read Write
metadata:
  {
    "openclaw": { "requires": { "env": ["CRYPTOHUNT_API_KEY"] } },
    "homepage": "https://pro.cryptohunt.ai"
  }
---
# 技能：XClaw 智能分析 🚀

XClaw 是专为 OpenClaw 开发者设计的高级智能分析工具，可实时提供来自 CryptoHunt 引擎的社会媒体数据和洞察。

## 先决条件
- **需要 API 密钥**：请在环境中设置 `CRYPTOHUNT_API_KEY`。
- **获取 API 密钥**：请访问 [apidashboard.cryptohunt.ai](https://apidashboard.cryptohunt.ai) 购买或注册 API 密钥。
- **官方 API 文档**：详细的 API 端点文档请参见 [pro.cryptohunt.ai](https://pro.cryptohunt.ai)。

## 核心功能

### 1. 趋势发现 (`xclaw_hot`)
- **操作**：获取过去 1 小时、4 小时或 24 小时内表现最佳的推文。
- **多维度过滤**：支持地区（`cn`/`global`）和标签（例如 `AI`、`meme`、`ethereum`）的筛选。

### 2. KOL 智能分析 (`xclaw_analyze`)
- **操作**：从内部 KOL 数据库中获取推文；新用户可使用 **实时爬取** 功能。

### 3. 推文删除分析 (`xclaw_ghost`)
- **操作**：检测被特定用户删除的推文。
- **用途**：用于发现 KOL 重新发布的声明、隐藏的内容或意外发布的推文。

### 4. 推文详细分析 (`xclaw_detail`)
- **操作**：根据特定的推文 URL 或 ID 获取推文的全文、数据（点赞数、书签数、浏览量）以及相关讨论信息。

### 5. 智能内容创意生成 (`xclaw_draft`)
- **操作**：根据地区和标签筛选热门话题，自动生成具有原创链接的高转化率推文草稿。

## 用户命令示例
- `xclaw find hot`：获取过去 24 小时内中国地区的热门加密货币相关推文。
- `xclaw analyze <username>`：深入分析特定用户的最新推文内容。
- `xclaw ghost <username>`：查看 @username 尝试删除的推文。
- `xclaw detail <URL_or_ID>`：获取特定推文的所有详细信息和统计数据。
- `xclaw draft`：自动获取热门话题的推文草稿，并提供 3 个版本的建议。

---
*CryptoHunt 智能分析——为创作者提供的数据支持。*