---
name: tech-digest
description: 生成技术新闻摘要，具备统一的来源模型、质量评分功能以及多种输出格式。数据收集途径包括 RSS 源、Twitter/X 的意见领袖（KOLs）以及网络搜索。采用基于管道的脚本架构，支持重试机制和数据去重处理。支持通过 Discord、电子邮件以及 Markdown 模板进行信息发送。
version: "2.0.0"
---

# Tech Digest v2.0

这是一个自动化的技术新闻摘要系统，具备统一的数据源模型、质量评分流程以及基于模板的输出生成功能。

## v2.0 的新特性

- **统一的数据源模型**：使用一个 `sources.json` 文件来管理 RSS、Twitter 和网页来源的数据。
- **增强的主题定义**：提供了更丰富的主题定义，支持搜索查询和过滤功能。
- **流程脚本**：采用了模块化的数据获取 → 合并 → 模板生成的工作流程。
- **质量评分**：支持多源数据的质量评估，包括去重和优先级排序。
- **多种输出格式**：支持 Discord、电子邮件和 Markdown 格式。
- **配置验证**：通过 JSON 模式进行配置验证和一致性检查。
- **用户自定义**：允许用户通过修改 `workspace/config/` 文件来自定义系统设置。

## 快速入门

1. **配置设置**：默认配置文件位于 `config/defaults/` 目录下。您可以将这些配置复制到工作区中进行个性化调整：
   ```bash
   mkdir -p workspace/config
   cp config/defaults/sources.json workspace/config/
   cp config/defaults/topics.json workspace/config/
   ```

2. **环境变量**：
   - `X_BEARER_TOKEN`：Twitter API 的 bearer token（可选）。
   - `BRAVE_API_KEY`：Brave Search API 的 key（可选）。

3. **生成摘要**：
   ```bash
   # Full pipeline
   python3 scripts/fetch-rss.py --config workspace/config
   python3 scripts/fetch-twitter.py --config workspace/config  
   python3 scripts/fetch-web.py --config workspace/config
   python3 scripts/merge-sources.py --rss rss.json --twitter twitter.json --web web.json
   ```

4. **使用模板**：您可以为生成的摘要选择 Discord、电子邮件或 Markdown 格式。

## 配置文件

### `sources.json` - 统一的数据源配置
```json
{
  "sources": [
    {
      "id": "openai-rss",
      "type": "rss",
      "name": "OpenAI Blog",
      "url": "https://openai.com/blog/rss.xml",
      "enabled": true,
      "priority": true,
      "topics": ["llm", "ai-agent"],
      "note": "Official OpenAI updates"
    },
    {
      "id": "sama-twitter",
      "type": "twitter", 
      "name": "Sam Altman",
      "handle": "sama",
      "enabled": true,
      "priority": true,
      "topics": ["llm", "frontier-tech"],
      "note": "OpenAI CEO"
    }
  ]
}
```

### `topics.json` - 增强的主题定义
```json
{
  "topics": [
    {
      "id": "llm",
      "emoji": "🧠",
      "label": "LLM / Large Models",
      "description": "Large Language Models, foundation models, breakthroughs",
      "search": {
        "queries": ["LLM latest news", "large language model breakthroughs"],
        "must_include": ["LLM", "large language model", "foundation model"],
        "exclude": ["tutorial", "beginner guide"]
      },
      "display": {
        "max_items": 8,
        "style": "detailed"
      }
    }
  ]
}
```

## 脚本流程

### 1. `fetch-rss.py` - RSS 源数据获取脚本
```bash
python3 scripts/fetch-rss.py [--config CONFIG_DIR] [--hours 48] [--output FILE] [--verbose]
```
- **特点**：支持并行数据获取、重试机制，以及使用 feedparser 或正则表达式进行数据解析。
- **输出格式**：结构化的 JSON 数据，其中文章按主题分类。
- **超时设置**：每个 RSS 源的请求超时时间为 15 秒，并采用指数级重试策略。

### 2. `fetch-twitter.py` - Twitter/X KOL 监控脚本
```bash
python3 scripts/fetch-twitter.py [--config CONFIG_DIR] [--hours 48] [--output FILE]
```
- **要求**：需要设置 `X_BEARER_TOKEN` 环境变量。
- **特点**：支持速率限制处理、分析用户的互动数据（如回复数等）。
- **API**：使用 Twitter API v2，需要通过应用身份验证。

### 3. `fetch-web.py` - 网页搜索脚本
```bash
python3 scripts/fetch-web.py [--config CONFIG_DIR] [--freshness 48h] [--output FILE]
```
- **使用 Brave API**：可以自动执行搜索任务（需要 `BRAVE_API_KEY`）。
- **不使用 API**：为其他代理程序提供搜索接口。
- **过滤规则**：支持基于内容的筛选机制。

### 4. `merge-sources.py** - 数据合并与质量评分脚本
```bash
python3 scripts/merge-sources.py --rss rss.json --twitter twitter.json --web web.json
```
- **质量评分标准**：来源的可靠性（+3 分）、数据的新鲜度（+2 分）、用户互动度（+1 分）。
- **去重机制**：通过标题相似度检测（85% 的阈值）来去除重复内容。
- **避免重复**：防止最近生成的摘要中包含重复的文章。
- **输出结果**：按主题分类的文章列表，附带质量评分。

### 5. `validate-config.py** - 配置验证脚本
```bash
python3 scripts/validate-config.py [--config-dir CONFIG_DIR] [--verbose]
```
- **验证内容**：检查配置文件的结构和必填字段。
- **一致性检查**：确保主题引用和 ID 的唯一性。
- **来源验证**：验证 RSS 链接和 Twitter 账号的合法性。

## 用户自定义

您可以通过修改 `workspace/config/` 文件来自定义系统设置：

- **添加新数据源**：通过设置 `"enabled": true` 来启用新的数据源。
- **修改主题定义**：自定义主题的搜索查询和显示方式。
- **合并规则**：
  - 如果多个数据源具有相同的 ID，使用用户自定义的配置。
  - 如果数据源具有新的 ID，将其添加到默认配置中。
  - 如果主题具有相同的 ID，使用用户自定义的配置完全替换默认设置。

### 示例配置文件（`workspace/config/`）
```json
// workspace/config/sources.json
{
  "sources": [
    {
      "id": "simonwillison-rss",
      "enabled": false,
      "note": "Disabled: too noisy for my use case"
    },
    {
      "id": "my-custom-blog", 
      "type": "rss",
      "name": "My Custom Tech Blog",
      "url": "https://myblog.com/rss",
      "enabled": true,
      "priority": true,
      "topics": ["frontier-tech"]
    }
  ]
}
```

## 模板与输出格式

### Discord 模板（`references/templates/discord.md`）
- 采用列表格式展示内容，链接会自动被省略。
- 优化了移动设备显示效果，支持表情符号。
- 文本长度限制为 2000 个字符。

### 电子邮件模板（`references/templates/email.md`）
- 包含丰富的元数据和技术统计信息。
- 提供文章的摘要和精选文章列表。
- 支持 HTML 格式显示。

### Markdown 模板（`references/templates/markdown.md`）
- 采用 GitHub 标准的表格格式。
- 包含详细的技术说明。
- 支持可展开的章节结构。

## 默认数据源（共 65 个）

- **RSS 源（32 个）**：涵盖 AI 实验室、科技博客、加密货币新闻和中文科技媒体。
- **Twitter/X KOL（29 个）**：包括 AI 研究人员、加密货币领域专家和技术高管。
- **网页搜索（4 个主题）**：涉及大型语言模型（LLM）、AI 代理、加密货币和前沿科技领域。

所有数据源都预先配置了相应的主题标签和优先级。

## 依赖库

```bash
pip install -r requirements.txt
```

**推荐安装（非强制）：**
- `feedparser>=6.0.0`：提供更好的 RSS 解析功能（如果 `feedparser` 未安装，系统会使用正则表达式作为备用方案）。
- `jsonschema>=4.0.0`：用于配置文件的验证。

**所有脚本仅支持 Python 3.8 及更高版本的标准库。**

## 从 v1.x 迁移

- **配置文件迁移**：旧配置文件会自动转换为新的格式。
- **脚本更新**：提供了新的命令行接口和更完善的错误处理机制。
- **模板系统**：替换了旧的基于提示符的生成方式，采用了模板系统。
- **质量评分**：新的评分系统会影响文章的排名顺序。

## 监控与运维

### 系统健康检查
```bash
# Validate configuration
python3 scripts/validate-config.py --verbose

# Test RSS feeds
python3 scripts/fetch-rss.py --hours 1 --verbose

# Check Twitter API
python3 scripts/fetch-twitter.py --hours 1 --verbose
```

### 档案管理
- 摘要文件会自动保存到 `workspace/archive/tech-digest/` 目录。
- 旧版本的摘要标题会被用于检测重复内容。
- 过期的档案会自动清理（超过 30 天）。

### 错误处理
- **网络故障**：采用指数级重试策略来处理网络问题。
- **速率限制**：遇到速率限制时系统会自动重试。
- **内容无效**：系统会优雅地处理无效数据，并记录详细的错误信息。
- **配置错误**：提供有用的错误提示和相应的解决方案。

## API 密钥与环境设置

请将 API 密钥配置在 `~/.zshenv` 或类似的文件中：
```bash
export X_BEARER_TOKEN="your_twitter_bearer_token"
export BRAVE_API_KEY="your_brave_search_api_key"  # Optional
```

- **Twitter**：提供只读权限的 bearer token，按使用次数计费。
- **Brave Search**：可选，如果 `BRAVE_API_KEY` 无法使用，则使用 `web_search` 功能作为备用方案。

## 定时任务集成

- **每日摘要生成**：可以设置每日自动执行摘要生成的任务。
- **每周摘要生成**：也可以设置每周生成一次摘要的任务。

## 支持与故障排除

### 常见问题与解决方法
- **RSS 源数据获取失败**：检查网络连接情况，可以使用 `--verbose` 参数获取更多详细信息。
- **Twitter 的速率限制**：可以减少数据源的数量或增加数据获取的间隔时间。
- **配置错误**：运行 `validate-config.py` 可以诊断具体的配置问题。
- **未找到文章**：检查指定的时间范围（使用 `--hours` 参数）和数据源的启用状态。

### 调试模式
所有脚本都支持 `--verbose` 参数，用于输出详细的日志信息，便于故障排查。

### 性能优化
- **并行处理**：根据系统配置调整 `MAX_WORKERS` 的值以提升处理效率。
- **超时设置**：对于网络速度较慢的情况，可以增加 `TIMEOUT` 的值。
- **文章数量限制**：根据实际需求调整 `MAX_ARTICLES_PER_FEED` 的值。