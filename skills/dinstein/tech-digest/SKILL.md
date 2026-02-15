---
name: tech-digest
description: 生成技术新闻摘要，采用统一的来源模型、质量评分机制以及多种输出格式。数据收集途径包括 RSS 源、Twitter/X 的意见领袖（KOLs）、GitHub 的代码发布以及网络搜索。系统基于管道（pipeline）架构，具备重试机制和去重功能。支持通过 Discord、电子邮件以及 Markdown 模板进行信息推送。
version: "2.1.2"
homepage: https://github.com/draco-agent/tech-digest
source: https://github.com/draco-agent/tech-digest
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
# Tech Digest v2.1

这是一个自动化的科技新闻摘要系统，具备统一的数据源模型、质量评分机制以及基于模板的输出生成功能。

## v2.1的新特性

- **统一的数据源模型**：使用一个`sources.json`文件来管理RSS、Twitter和网页来源的数据。
- **增强的主题定义**：提供了更详细的主题定义，支持搜索查询和过滤功能。
- **脚本流程**：采用了模块化的数据获取、合并和模板生成的工作流程。
- **质量评分**：支持多源数据的质量评估，包括去重和优先级排序。
- **多种输出格式**：支持Discord、电子邮件和Markdown格式的输出。
- **配置验证**：通过JSON模式进行配置验证和一致性检查。
- **用户自定义**：允许用户通过修改`workspace/config/`文件来自定义系统设置。

## 快速入门

1. **配置设置**：默认配置文件位于`config/defaults/`目录下。您可以将这些配置复制到工作空间中进行个性化调整：
   ```bash
   mkdir -p workspace/config
   cp config/defaults/sources.json workspace/config/
   cp config/defaults/topics.json workspace/config/
   ```

2. **环境变量**：
   - `X_BEARER_TOKEN`：Twitter API的bearer token（可选）。
   - `BRAVE_API_KEY`：Brave Search API的key（可选）。
   - `GITHUB_TOKEN`：GitHub的个人访问token（可选，可提高请求速率限制）。

3. **生成摘要**：
   ```bash
   # Full pipeline
   python3 scripts/fetch-rss.py --config workspace/config
   python3 scripts/fetch-twitter.py --config workspace/config  
   python3 scripts/fetch-web.py --config workspace/config
   python3 scripts/fetch-github.py --config workspace/config
   python3 scripts/merge-sources.py --rss rss.json --twitter twitter.json --web web.json --github github.json
   ```

4. **使用模板**：您可以为生成的摘要选择Discord、电子邮件或Markdown格式。

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

### 1. `fetch-rss.py` - RSS源数据获取脚本
```bash
python3 scripts/fetch-rss.py [--config CONFIG_DIR] [--hours 48] [--output FILE] [--verbose]
```
- **功能**：支持并行获取数据、重试机制，并提供正则表达式作为数据解析的备用方案。
- **输出**：按主题分类的结构化JSON数据。
- **超时设置**：每个RSS源的获取尝试时间为15秒，采用指数级重试策略。

### 2. `fetch-twitter.py` - Twitter/X KOL监控脚本
```bash
python3 scripts/fetch-twitter.py [--config CONFIG_DIR] [--hours 48] [--output FILE]
```
- **要求**：需要`X_BEARER_TOKEN`环境变量。
- **功能**：处理请求速率限制、统计用户互动数据、过滤用户回复。
- **API**：使用Twitter API v2，并支持仅限应用程序使用的认证方式。

### 3. `fetch-web.py` - 网页搜索脚本
```bash
python3 scripts/fetch-web.py [--config CONFIG_DIR] [--freshness 48h] [--output FILE]
```
- **使用Brave API**：可自动执行搜索任务（需要`BRAVE_API_KEY`）。
- **不使用API**：为其他代理程序生成搜索接口。
- **过滤规则**：支持基于内容的筛选机制。

### 4. `fetch-github.py` - GitHub发布监控脚本
```bash
python3 scripts/fetch-github.py [--config CONFIG_DIR] [--hours 168] [--output FILE]
```
- **功能**：并行监控GitHub仓库的发布信息，并对输出内容进行Markdown格式化处理。
- **认证**：可选的`GITHUB_TOKEN`可提高请求速率限制。
- **输出**：按主题分类的GitHub发布信息。

### 5. `merge-sources.py** - 数据合并与质量评分脚本
```bash
python3 scripts/merge-sources.py --rss rss.json --twitter twitter.json --web web.json --github github.json
```
- **评分标准**：来源的可靠性（+3分）、数据的最新性（+2分）、用户互动性（+1分）。
- **去重机制**：通过标题相似度检测进行去重（阈值85%），并限制同一来源的重复内容。
- **避免重复**：避免在摘要中重复出现最近的文章。
- **输出**：按主题分类的文章列表，附带质量评分。

### 6. `validate-config.py` - 配置验证脚本
```bash
python3 scripts/validate-config.py [--config-dir CONFIG_DIR] [--verbose]
```
- **JSON格式检查**：验证配置文件的结构和必填字段。
- **一致性检查**：检查主题引用和ID的唯一性。
- **来源验证**：验证RSS链接和Twitter用户名的有效性。

## 用户自定义

您可以通过修改`workspace/config/`文件来自定义系统设置：

- **数据源配置**：添加新的数据源，或通过设置`"enabled": false`来禁用默认数据源。
- **主题配置**：自定义主题定义、搜索查询和显示选项。
- **数据合并逻辑**：
  - 如果多个数据源具有相同的ID，使用用户自定义的配置。
  - 如果数据源具有新的ID，将其添加到默认配置中。
  - 如果主题具有相同的ID，使用用户自定义的配置完全替换默认设置。

### 示例配置文件
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

### Discord模板（`references/templates/discord.md`）
- 使用项目符号列表格式，链接会自动被替换为文本。
- 优化了移动设备显示效果，包含表情符号。
- 文本长度限制在2000个字符以内。

### 电子邮件模板（`references/templates/email.md`）
- 包含丰富的元数据和技术统计信息，以及文章的存档链接。
- 提供执行摘要和热门文章的部分。
- 支持HTML格式的显示。

### Markdown模板（`references/templates/markdown.md`）
- 支持GitHub格式的表格和排版。
- 包含技术细节部分，以及可展开的章节内容。

## 默认数据源（共109个）

- **RSS源（46个）**：AI研究实验室、科技博客、加密货币新闻、中国科技媒体。
- **Twitter/X KOL（44个）**：AI领域的研究人员、加密货币领域的领军人物、科技行业高管。
- **GitHub仓库（19个）**：主要的开源项目（如LangChain、vLLM、Foundry等）。
- **网页搜索（4个主题）**：大型语言模型（LLM）、AI代理、加密货币、前沿科技领域。

所有数据源都预先配置了相应的主题标签和优先级。

## 依赖项
```bash
pip install -r requirements.txt
```

**推荐安装（非强制）：**
- `feedparser>=6.0.0`：提供更好的RSS解析功能（如果`feedparser`不可用，系统会使用正则表达式作为替代方案）。
- `jsonschema>=4.0.0`：用于配置验证。

**所有脚本仅支持Python 3.8及以上版本的标准库。**

## 从v1.x版本升级**

- **配置文件迁移**：旧版本的配置文件会自动转换为新格式。
- **脚本更新**：提供了新的命令行接口，具有更好的错误处理机制。
- **模板系统**：替换了旧的基于提示符的生成方式，采用了模板系统。
- **质量评分**：新的评分系统会影响文章的排名顺序。

## 监控与运维

- **系统健康检查**：定期检查系统的运行状态。
- **归档管理**：摘要文件会自动保存到`workspace/archive/tech-digest/`目录。
- 旧版本的摘要标题会被用于检测重复内容。
- 过期的归档文件会自动删除（保留30天以上）。

## 错误处理**

- **网络故障**：系统会采用指数级重试策略来处理网络错误。
- **请求速率限制**：系统会自动重试请求，并设置适当的延迟时间。
- **内容无效**：系统会优雅地处理无效数据，并记录详细的错误日志。
- **配置错误**：系统会验证配置文件，并提供有用的错误提示信息。

## API密钥与环境设置

请将API密钥设置到`~/.zshenv`文件中：
```bash
export X_BEARER_TOKEN="your_twitter_bearer_token"
export BRAVE_API_KEY="your_brave_search_api_key"  # Optional
```

- **Twitter**：提供只读权限的bearer token，采用按使用次数计费的模式。
- **Brave Search**：可选，如果`BRAVE_API_KEY`不可用，系统会使用`web_search`脚本作为替代方案。

## Cron任务集成

### OpenClaw的Cron任务配置（推荐）

Cron脚本中不应直接编写脚本的执行步骤，而应引用`references/digest-prompt.md`文件，并仅传递配置参数。这样可以确保脚本逻辑始终保存在`Tech Digest`技能仓库中，并在所有安装环境中保持一致性。

#### 每日摘要的Cron任务配置
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

#### 每周摘要的Cron任务配置
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

#### 采用这种模式的理由：

- **数据来源的统一管理**：所有脚本逻辑都保存在`digest-prompt.md`文件中，避免分散在多个配置文件中。
- **跨平台兼容性**：在不同版本的OpenClaw环境中，只需修改路径和频道ID即可。
- **易于维护**：更新技能配置后，所有Cron任务会自动更新。
- **避免错误**：不要将脚本步骤直接写入Cron脚本中，以防出现逻辑不一致的问题。

#### 多渠道推送限制

OpenClaw支持**跨平台隔离**机制：一个会话只能向一个平台发送消息（例如，只能向Discord或Telegram发送摘要）。如果需要向多个平台推送摘要，需要为每个平台创建单独的Cron任务：

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
请在第二个任务的Cron脚本中将`DISCORD_CHANNEL_ID`替换为`Telegram_CHANNEL_ID`（使用`message`工具，并设置`channel=telegram`）。

这是一种安全机制，旨在防止数据在不同平台之间意外泄露。

## 支持与故障排除

- **常见问题**：
  - **RSS源无法获取数据**：检查网络连接情况，可以使用`--verbose`参数获取更多调试信息。
  - **Twitter请求速率限制**：减少数据源的数量或增加数据获取的间隔时间。
  - **配置错误**：运行`validate-config.py`以解决具体的配置问题。
  - **未找到文章**：检查设置的时间窗口（`--hours`参数）和数据源的启用状态。

### 调试模式

所有脚本都支持`--verbose`参数，用于启用详细的日志记录和故障排查。

### 性能优化

- **并行处理**：根据系统配置调整`MAX_WORKERS`参数以提升处理效率。
- **超时设置**：对于网络速度较慢的情况，可以增加`TIMEOUT`参数的值。
- **文章数量限制**：根据需要调整`MAX_ARTICLES_PER_FEED`参数以控制输出文章的数量。