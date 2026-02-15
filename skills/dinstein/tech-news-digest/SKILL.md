---
name: tech-news-digest
description: 生成技术新闻摘要，具备统一的源数据模型、质量评分机制以及多种输出格式。数据收集渠道包括 RSS 源、Twitter/X 社交平台的 KOLs、GitHub 的代码发布信息以及网络搜索结果。采用基于管道的脚本处理流程，支持重试机制和数据去重功能。支持通过 Discord、电子邮件以及 Markdown 模板进行内容分发。
version: "2.5.0"
homepage: https://github.com/draco-agent/tech-news-digest
source: https://github.com/draco-agent/tech-news-digest
env:
  - name: X_BEARER_TOKEN
    required: false
    description: Twitter/X API bearer token for KOL monitoring
  - name: BRAVE_API_KEY
    required: false
    description: Brave Search API key for web search layer
  - name: GITHUB_TOKEN
    required: false
    description: GitHub personal access token for higher API rate limits
---
# 技术新闻摘要系统

这是一个自动化的技术新闻摘要系统，具有统一的数据源模型、质量评分流程以及基于模板的输出生成功能。

## 快速入门

1. **配置设置**：默认配置位于 `config/defaults/` 文件中。请将其复制到工作区进行自定义：
   ```bash
   mkdir -p workspace/config
   cp config/defaults/sources.json workspace/config/
   cp config/defaults/topics.json workspace/config/
   ```

2. **环境变量**：
   - `X_BEARER_TOKEN` - Twitter API 令牌（可选）
   - `BRAVE_API_KEY` - Brave Search API 密钥（可选）
   - `GITHUB_TOKEN` - GitHub 个人访问令牌（可选，可提高请求速率）

3. **生成摘要**：
   ```bash
   # Full pipeline
   python3 scripts/fetch-rss.py --config workspace/config
   python3 scripts/fetch-twitter.py --config workspace/config  
   python3 scripts/fetch-web.py --config workspace/config
   python3 scripts/fetch-github.py --config workspace/config
   python3 scripts/merge-sources.py --rss rss.json --twitter twitter.json --web web.json --github github.json
   ```

4. **使用模板**：可以将生成的摘要内容应用到 Discord、电子邮件或 Markdown 格式中。

## 配置文件

### `sources.json` - 统一的数据源
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

### `topics.json` - 优化后的主题定义
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

### 1. `fetch-rss.py` - RSS 源获取脚本
```bash
python3 scripts/fetch-rss.py [--config CONFIG_DIR] [--hours 48] [--output FILE] [--verbose]
```
- **特性**：并行获取数据、重试机制、支持 RSS 解析器及正则表达式作为备用方案
- **输出**：按主题分类的结构化 JSON 数据
- **超时设置**：每个 RSS 源的请求超时为 15 秒，并采用指数级重试策略

### 2. `fetch-twitter.py` - Twitter/X KOL 监控脚本
```bash
python3 scripts/fetch-twitter.py [--config CONFIG_DIR] [--hours 48] [--output FILE]
```
- **要求**：需要 `X_BEARER_TOKEN` 环境变量
- **特性**：处理请求速率限制、统计用户互动数据、过滤回复内容
- **API**：使用 Twitter API v2 和应用专用认证方式

### 3. `fetch-web.py` - 网页搜索脚本
```bash
python3 scripts/fetch-web.py [--config CONFIG_DIR] [--freshness 48h] [--output FILE]
```
- **使用 Brave API**：可自动执行搜索（需要 `BRAVE_API_KEY`）
- **不使用 API**：为代理程序生成搜索接口
- **过滤规则**：基于内容的内容筛选机制

### 4. `fetch-github.py` - GitHub 代码库发布监控脚本
```bash
python3 scripts/fetch-github.py [--config CONFIG_DIR] [--hours 168] [--output FILE]
```
- **特性**：并行监控 GitHub 仓库的发布内容、过滤发布信息、去除Markdown 格式
- **认证**：可选的 `GITHUB_TOKEN` 可提高请求速率
- **输出**：按主题分类的结构化 JSON 数据

### 5. `merge-sources.py** - 质量评分与去重脚本
```bash
python3 scripts/merge-sources.py --rss rss.json --twitter twitter.json --web web.json --github github.json
```
- **评分标准**：来源的可靠性（+3 分）、数据来源的多样性（+5 分）、文章的新鲜度（+2 分）、用户互动度（+1 分）
- **去重机制**：通过标题相似度检测（85% 作为阈值）进行去重；避免重复发布近期文章
- **输出**：按主题分组并附带质量评分的文章列表

### 6. `validate-config.py` - 配置验证脚本
```bash
python3 scripts/validate-config.py [--config-dir CONFIG_DIR] [--verbose]
```
- **JSON 格式验证**：检查数据结构及必填字段
- **一致性检查**：验证主题引用和唯一 ID
- **来源类型验证**：验证 RSS 链接和 Twitter 账号的合法性

## 用户自定义

### 工作区配置覆盖
将自定义配置文件放在 `workspace/config/` 目录下，以覆盖默认设置：
- **数据源**：添加新的数据源；通过设置 `"enabled": false` 来禁用默认数据源
- **主题设置**：自定义主题定义、搜索查询条件及显示选项
- **合并逻辑**：
  - 如果多个数据源具有相同的 ID，则使用用户自定义的配置
  - 新数据源会被添加到默认配置中
  - 如果多个主题具有相同的 ID，则用户自定义的配置会完全替换默认设置

### 示例工作区配置
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

### Discord 模板 (`references/templates/discord.md`)
- 使用项目符号列表格式，链接会自动隐藏
- 适用于移动设备显示，包含表情符号
- 文本长度限制在 2000 个字符以内

### 电子邮件模板 (`references/templates/email.md`)
- 包含丰富的元数据和技术统计信息、存档链接
- 提供执行摘要的摘要部分和热门文章列表
- 支持 HTML 格式显示

### Markdown 模板 (`references/templates/markdown.md`)
- 支持 GitHub 格式的表格和格式化功能
- 包含技术细节部分
- 支持可展开的内容区域

## 默认数据源（共 109 个）

- **RSS 源（46 个）**：AI 实验室、科技博客、加密货币新闻、中国科技媒体
- **Twitter/X KOL（44 个）**：AI 研究人员、加密货币领域专家、科技行业高管
- **GitHub 仓库（19 个）**：主要开源项目（如 LangChain、vLLM、Foundry 等）
- **网页搜索（4 个主题）**：大型语言模型、AI 代理程序、加密货币、前沿科技领域

所有数据源都预先配置了相应的主题标签和优先级。

## 依赖库

```bash
pip install -r requirements.txt
```

**推荐使用但非强制**：
- `feedparser>=6.0.0`：更强大的 RSS 解析能力（若无法使用 RSS 解析器时，会使用正则表达式作为备用方案）
- `jsonschema>=4.0.0`：用于配置验证

**所有脚本仅支持 Python 3.8 及更高版本的标准库。**

## 从 v1.x 版本升级**

1. **配置迁移**：旧配置文件会自动转换为新格式
2. **脚本更新**：提供了新的命令行接口，具有更好的错误处理功能
3. **模板系统**：用模板系统替换了旧的基于提示符的生成方式
4. **质量评分**：新的评分系统会影响文章的排名顺序

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
- 摘要内容会自动存档到 `workspace/archive/tech-digest/` 目录
- 之前的摘要标题用于检测重复内容
- 过期的档案会自动清理（保留 30 天以上）

### 错误处理
- **网络故障**：采用指数级重试策略进行恢复
- **请求速率限制**：自动重试并设置适当的延迟时间
- **无效内容**：系统会优雅地处理错误并记录详细日志
- **配置错误**：通过验证机制提供有用的错误提示

## API 密钥与环境设置

请将相关密钥设置到 `~/.zshenv` 或类似文件中：
```bash
export X_BEARER_TOKEN="your_twitter_bearer_token"
export BRAVE_API_KEY="your_brave_search_api_key"  # Optional
```

- **Twitter**：仅限读取的令牌，按使用次数计费
- **Brave Search**：可选；若无法使用 Twitter API 时，可切换到 `web_search` 功能

## Cron/定时任务集成

### 推荐使用 OpenClaw 的 Cron 任务

Cron 任务中 **不应** 直接编写脚本逻辑。应参考 `references/digest-prompt.md` 文件，仅传递配置参数。这样可以确保脚本逻辑始终保存在技能仓库中，并在所有安装环境中保持一致。

#### 每日摘要任务的 Cron 语句
```
读取 <SKILL_DIR>/references/digest-prompt.md，按照其中的完整流程生成日报。

用以下参数替换占位符：
- MODE = daily
- TIME_WINDOW = past 1-2 days
- FRESHNESS = pd
- RSS_HOURS = 48
- ITEMS_PER_SECTION = 3-5
- BLOG_PICKS_COUNT = 2-3
- EXTRA_SECTIONS = （无）
- SUBJECT = Daily Tech Digest - YYYY-MM-DD
- WORKSPACE = <your workspace path>
- SKILL_DIR = <your skill install path>
- DISCORD_CHANNEL_ID = <your channel id>
- EMAIL = （optional）
- LANGUAGE = Chinese
- TEMPLATE = discord

严格按 prompt 模板中的步骤执行，不要跳过任何步骤。
```

#### 每周摘要任务的 Cron 语句
```
读取 <SKILL_DIR>/references/digest-prompt.md，按照其中的完整流程生成周报。

用以下参数替换占位符：
- MODE = weekly
- TIME_WINDOW = past 7 days
- FRESHNESS = pw
- RSS_HOURS = 168
- ITEMS_PER_SECTION = 5-8
- BLOG_PICKS_COUNT = 3-5
- EXTRA_SECTIONS = 📊 Weekly Trend Summary (2-3 sentences summarizing macro trends)
- SUBJECT = Weekly Tech Digest - YYYY-MM-DD
- WORKSPACE = <your workspace path>
- SKILL_DIR = <your skill install path>
- DISCORD_CHANNEL_ID = <your channel id>
- EMAIL = （optional）
- LANGUAGE = Chinese
- TEMPLATE = discord

严格按 prompt 模板中的步骤执行，不要跳过任何步骤。
```

#### 为何采用这种设计？
- **单一信息源**：所有脚本逻辑都集中在 `digest-prompt.md` 文件中，避免分散在多个配置文件中
- **便携性**：在不同 OpenClaw 实例上只需更改路径和频道 ID 即可
- **易于维护**：更新技能配置后，所有定时任务会自动更新
- **避免错误**：切勿将脚本逻辑直接写入 Cron 任务中，以防出现不一致

#### 多渠道推送限制
OpenClaw 实施了 **跨服务隔离** 规则：同一会话只能向一个平台发送消息（例如，只能向 Discord 或 Telegram 发送摘要）。如果需要向多个平台推送摘要，请为每个平台创建单独的 Cron 任务：

```
# Job 1: Discord + Email
- DISCORD_CHANNEL_ID = 1470806864412414071
- EMAIL = user@example.com
- TEMPLATE = discord

# Job 2: Telegram DM
- DISCORD_CHANNEL_ID = （无）
- EMAIL = （无）
- TEMPLATE = telegram
```
在第二个任务的 Cron 语句中，将 `DISCORD_CHANNEL_ID` 替换为 `telegram_CHANNEL_ID`（使用 `message` 工具并设置 `channel=telegram`）。

这是出于安全考虑的设计，而非技术故障。

## 安全注意事项

### 执行机制
该技能采用 **提示符模板**：代理程序会读取 `digest-prompt.md` 文件并按照其中的指令执行操作。这是 OpenClaw 的标准执行模式——代理程序会解析来自技能文件的结构化指令。所有指令都会随技能包一起提供，并可在安装前进行审核。

### 网络访问
Python 脚本会访问以下地址：
- RSS 源的 URL（在 `sources.json` 中配置）
- Twitter/X API（`api.x.com`）
- Brave Search API（`api.search.brave.com`）
- GitHub API（`api.github.com`）

所有数据都不会发送到其他外部服务。所有 API 密钥都从技能元数据中指定的环境变量中获取。

### 安全性措施
- **电子邮件发送**：使用 `gog` CLI 工具，邮件主题格式固定为 `Daily Tech Digest - YYYY-MM-DD`。提示符模板禁止在脚本中插入不可信的内容。
- **文件访问**：脚本仅访问 `config/` 目录中的文件，并将结果写入 `workspace/archive/` 目录，不会访问工作区之外的文件。

## 支持与故障排除

### 常见问题
1. **RSS 源无法获取数据**：检查网络连接状态，可使用 `--verbose` 参数获取更多调试信息
2. **Twitter 请求速率限制**：减少数据源数量或增加数据获取间隔
3. **配置错误**：运行 `validate-config.py` 可排查具体问题
4. **未找到文章**：检查时间范围（通过 `--hours` 参数设置）和数据源是否启用

### 调试模式
所有脚本都支持 `--verbose` 参数，用于输出详细日志和辅助故障排查。

### 性能优化
- **并行处理**：根据系统配置调整 `MAX_WORKERS` 的值
- **超时设置**：对于网络速度较慢的情况，增加 `TIMEOUT` 的值
- **文章数量限制**：根据需要调整 `MAX_ARTICLES_PER_feed` 的值