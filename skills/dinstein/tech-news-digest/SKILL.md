---
name: tech-news-digest
description: 生成技术新闻摘要，具备统一的源数据模型、质量评分机制以及多种输出格式。数据来源包括 RSS 源、Twitter/X 的知名博主（KOLs）、GitHub 的发布内容、GitHub 的热门趋势（Trending）、Reddit 以及网络搜索结果。采用基于管道（pipeline）的脚本进行处理，具备重试机制和去重功能。支持通过 Discord、电子邮件以及 Markdown 模板进行信息推送。
version: "3.15.0"
homepage: https://github.com/draco-agent/tech-news-digest
source: https://github.com/draco-agent/tech-news-digest
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    optionalBins: ["mail", "msmtp", "gog", "gh", "openssl", "weasyprint"]
env:
  - name: TWITTER_API_BACKEND
    required: false
    description: "Twitter API backend: 'official', 'twitterapiio', or 'auto' (default: auto)"
  - name: X_BEARER_TOKEN
    required: false
    description: Twitter/X API bearer token for KOL monitoring (official backend)
  - name: TWITTERAPI_IO_KEY
    required: false
    description: twitterapi.io API key for KOL monitoring (twitterapiio backend)
  - name: TAVILY_API_KEY
    required: false
    description: Tavily Search API key (alternative to Brave)
  - name: WEB_SEARCH_BACKEND
    required: false
    description: "Web search backend: auto (default), brave, or tavily"
  - name: BRAVE_API_KEYS
    required: false
    description: Brave Search API keys (comma-separated for rotation)
  - name: BRAVE_API_KEY
    required: false
    description: Brave Search API key (single key fallback)
  - name: GITHUB_TOKEN
    required: false
    description: GitHub token for higher API rate limits (auto-generated from GitHub App if not set)
  - name: GH_APP_ID
    required: false
    description: GitHub App ID for automatic installation token generation
  - name: GH_APP_INSTALL_ID
    required: false
    description: GitHub App Installation ID for automatic token generation
  - name: GH_APP_KEY_FILE
    required: false
    description: Path to GitHub App private key PEM file
tools:
  - python3: Required. Runs data collection and merge scripts.
  - mail: Optional. msmtp-based mail command for email delivery (preferred).
  - gog: Optional. Gmail CLI for email delivery (fallback if mail not available).
files:
  read:
    - config/defaults/: Default source and topic configurations
    - references/: Prompt templates and output templates
    - scripts/: Python pipeline scripts
    - <workspace>/archive/tech-news-digest/: Previous digests for dedup
  write:
    - /tmp/td-*.json: Temporary pipeline intermediate outputs
    - /tmp/td-email.html: Temporary email HTML body
    - /tmp/td-digest.pdf: Generated PDF digest
    - <workspace>/archive/tech-news-digest/: Saved digest archives
---
# 技术新闻摘要系统

这是一个自动化的技术新闻摘要系统，具有统一的数据源模型、质量评分流程以及基于模板的输出生成功能。

## 快速入门

1. **配置设置**：默认配置位于 `config/defaults/` 文件中。请将其复制到工作区以进行自定义：
   ```bash
   mkdir -p workspace/config
   cp config/defaults/sources.json workspace/config/tech-news-digest-sources.json
   cp config/defaults/topics.json workspace/config/tech-news-digest-topics.json
   ```

2. **环境变量**：
   - `TWITTERAPI_IO_KEY` - twitterapi.io 的 API 密钥（可选，推荐使用）
   - `X_BEARER_TOKEN` - Twitter/X 官方 API 的 bearer token（可选，作为备用方案）
   - `TAVILY_API_KEY` - Tavily 搜索 API 的密钥（Brave 的替代方案）
   - `WEB_SEARCH_BACKEND` - 网页搜索后端：auto|brave|tavily（可选，默认为 auto）
   - `BRAVE_API_KEYS` - Brave 搜索 API 的密钥（用逗号分隔，用于轮换使用）
   - `BRAVE_API_KEY` - 单个 Brave API 密钥（作为备用方案）
   - `GITHUB_TOKEN` - GitHub 个人访问令牌（可选，可提高请求速率限制）

3. **生成摘要**：
   ```bash
   # Unified pipeline (recommended) — runs all 6 sources in parallel + merge
   python3 scripts/run-pipeline.py \
     --defaults config/defaults \
     --config workspace/config \
     --hours 48 --freshness pd \
     --archive-dir workspace/archive/tech-news-digest/ \
     --output /tmp/td-merged.json --verbose --force
   ```

4. **使用模板**：将摘要内容应用到 Discord、电子邮件或 PDF 模板中。

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

### `run-pipeline.py` - 统一的流程管理脚本（推荐使用）
```bash
python3 scripts/run-pipeline.py \
  --defaults config/defaults [--config CONFIG_DIR] \
  --hours 48 --freshness pd \
  --archive-dir workspace/archive/tech-news-digest/ \
  --output /tmp/td-merged.json --verbose --force
```
- **特点**：并行执行所有 6 个数据获取步骤，然后进行合并、去重和评分
- **输出**：最终合并后的 JSON 数据，可用于生成报告（总耗时约 30 秒）
- **元数据**：将每个步骤的耗时和数量保存到 `*.meta.json` 文件中
- **GitHub 认证**：如果未设置 `$GITHUB_TOKEN`，则会自动生成 GitHub 应用程序令牌
- **备用方案**：如果该脚本失败，将单独运行以下脚本

### 单个脚本（备用方案）

#### `fetch-rss.py` - RSS 源获取脚本
```bash
python3 scripts/fetch-rss.py [--defaults DIR] [--config DIR] [--hours 48] [--output FILE] [--verbose]
```
- 并行获取数据（使用 10 个任务线程），具有重试机制；支持 feedparser 和正则表达式解析
- 超时设置：每个 RSS 源 30 秒；支持 ETag/Last-Modified 缓存

#### `fetch-twitter.py` - Twitter/X KOL 监控脚本
```bash
python3 scripts/fetch-twitter.py [--defaults DIR] [--config DIR] [--hours 48] [--output FILE] [--backend auto|official|twitterapiio]
```
- 根据 `TWITTERAPI_IO_KEY` 的设置自动选择 twitterapi.io 作为后端；如果设置了 `X_BEARER_TOKEN`，则使用官方的 X API v2
- 处理请求速率限制，记录互动数据；具有重试机制

#### `fetch-web.py` - 网页搜索引擎脚本
```bash
python3 scripts/fetch-web.py [--defaults DIR] [--config DIR] [--freshness pd] [--output FILE]
```
- 自动检测 Brave API 的速率限制：付费计划支持并行查询，免费计划则按顺序执行查询
- 如果没有 API，会为代理生成搜索界面

#### `fetch-github.py` - GitHub 仓库监控脚本
```bash
python3 scripts/fetch-github.py [--defaults DIR] [--config DIR] [--hours 168] [--output FILE]
```
- 并行获取数据（使用 10 个任务线程），超时设置为 30 秒
- 认证方式：优先使用 `$GITHUB_TOKEN` 生成的 GitHub 应用程序令牌；如果未设置，则使用 `gh` CLI 或未经认证的访问方式（每小时 60 次请求）

#### `fetch-github.py --trending` - GitHub 热门仓库脚本
```bash
python3 scripts/fetch-github.py --trending [--hours 48] [--output FILE] [--verbose]
```
- 通过 GitHub API 搜索 4 个主题（LLM、AI Agent、Crypto、Frontier Tech）下的热门仓库
- 质量评分标准：基础分为 5 分，加上每日评分（daily_stars_est / 10，最高分为 15 分）

#### `fetch-reddit.py` - Reddit 帖子获取脚本
```bash
python3 scripts/fetch-reddit.py [--defaults DIR] [--config DIR] [--hours 48] [--output FILE]
```
- 并行获取数据（使用 4 个任务线程），使用公开的 JSON API（无需认证）
- 支持过滤特定子版块的帖子

#### `enrich-articles.py` - 文章全文增强脚本
```bash
python3 scripts/enrich-articles.py --input merged.json --output enriched.json [--min-score 10] [--max-articles 15] [--verbose]
```
- 为评分较高的文章获取全文内容
- 优先使用 Cloudflare 提供的 Markdown 格式；如果无法获取，则使用 HTML 格式；对于受保护的或社交媒体来源的文章，可以选择跳过获取
- 支持白名单域名（最低评分阈值 ≥ 3 分）
- 并行获取数据（使用 5 个任务线程，超时设置为 10 秒）

#### `merge-sources.py` - 质量评分与去重脚本
```bash
python3 scripts/merge-sources.py --rss FILE --twitter FILE --web FILE --github FILE --reddit FILE
```
- 对文章进行质量评分和去重处理（去重率约为 85%）；对重复的文章会进行降分处理
- 输出结果按主题分组，并根据评分排序

#### `validate-config.py` - 配置验证脚本
```bash
python3 scripts/validate-config.py [--defaults DIR] [--config DIR] [--verbose]
```
- 验证 JSON 数据的结构；检查主题引用是否正确；检测重复的 ID

#### `generate-pdf.py` - PDF 报告生成脚本
```bash
python3 scripts/generate-pdf.py --input report.md --output digest.pdf [--verbose]
```
- 将 Markdown 格式的摘要内容转换为带有中文排版的 A4 PDF 文件（使用 Noto Sans CJK SC 字体）
- 支持表情符号、页眉/页脚设计；需要 `weasyprint` 工具来生成 PDF 文件

#### `sanitize-html.py` - 安全的 HTML 电子邮件转换脚本
```bash
python3 scripts/sanitize-html.py --input report.md --output email.html [--verbose]
```
- 将 Markdown 内容转换为安全的 HTML 格式，适用于电子邮件发送
- 支持 URL 白名单（仅限 http/https 协议）；对文本内容进行 HTML 转义处理

#### `source-health.py` - 数据源健康状况监控脚本
```bash
python3 scripts/source-health.py --rss FILE --twitter FILE --github FILE --reddit FILE --web FILE [--verbose]
```
- 记录每个数据源在过去 7 天内的运行状态（成功/失败情况）
- 会报告健康状况不佳的数据源（失败率超过 50%）

#### `summarize-merged.py` - 合并数据总结脚本
```bash
python3 scripts/summarize-merged.py --input merged.json [--top N] [--topic TOPIC]
```
- 生成易于人类阅读的合并数据摘要，供 LLM 使用
- 显示每个主题下得分最高的前几篇文章及其相关指标

## 用户自定义

### 工作区配置覆盖
将自定义配置文件放在 `workspace/config/` 目录下，以覆盖默认设置：

- **数据源**：可以添加新的数据源；通过设置 `"enabled": false` 来禁用默认数据源
- **主题**：可以修改主题定义、搜索查询和显示设置
- **合并逻辑**：
  - 如果数据源的 `id` 相同，优先使用用户自定义的配置
  - 如果数据源的 `id` 不同，新数据源会被添加到默认配置中
  - 如果主题的 `id` 相同，用户自定义的配置会完全替换默认设置

### 示例工作区配置覆盖
```json
// workspace/config/tech-news-digest-sources.json
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
- 使用项目符号列表格式；会自动省略链接 `<link>`
- 优化了移动设备显示效果；支持表情符号
- 文本长度限制为 2000 个字符

### 电子邮件模板 (`references/templates/email.md`)
- 包含丰富的元数据和技术统计信息；提供归档链接
- 包含执行摘要和热门文章部分
- 支持 HTML 格式显示

### PDF 模板 (`references/templates/pdf.md`)
- A4 页面布局，使用 Noto Sans CJK SC 字体显示中文内容
- 支持表情符号、页眉和页脚；支持页码显示
- 通过 `scripts/generate-pdf.py` 生成 PDF 文件（需要 `weasyprint` 工具）

## 默认数据源（共 151 个）

- **RSS 源（62 个）**：AI 实验室、科技博客、加密货币新闻、中国科技媒体
- **Twitter/X KOL（48 个）**：AI 研究人员、加密货币领域专家、科技行业高管
- **GitHub 仓库（28 个）**：主要开源项目（如 LangChain、vLLM、DeepSeek、Llama 等）
- **Reddit（13 个）**：r/MachineLearning、r/LocalLLaMA、r/CryptoCurrency、r/ChatGPT、r/OpenAI 等子版块
- **网页搜索（4 个主题）**：LLM、AI Agent、Crypto、Frontier Tech

所有数据源都预先配置了相应的主题标签和优先级。

## 依赖项

```bash
pip install -r requirements.txt
```

**推荐安装（虽然非强制）**：
- `feedparser>=6.0.0`：提供更好的 RSS 解析功能（如果 `feedparser` 无法使用，则使用正则表达式进行解析）
- `jsonschema>=4.0.0`：用于配置验证

**所有脚本仅支持 Python 3.8 及更高版本的标准库。**

## 监控与操作

### 健康状况检查
```bash
# Validate configuration
python3 scripts/validate-config.py --verbose

# Test RSS feeds
python3 scripts/fetch-rss.py --hours 1 --verbose

# Check Twitter API
python3 scripts/fetch-twitter.py --hours 1 --verbose
```

### 归档管理
- 摘要文件会自动存档到 `<workspace>/archive/tech-news-digest/` 目录
- 使用之前的摘要文件标题来检测重复内容
- 过期的归档文件会自动清理（保留时间超过 90 天）

### 错误处理
- **网络故障**：采用指数级重试机制进行恢复
- **请求速率限制**：自动重试，并设置适当的延迟时间
- **内容无效**：系统会优雅地处理错误，并详细记录错误日志
- **配置错误**：会进行配置验证，并提供有用的错误提示信息

## API 密钥与环境设置

请将相关 API 密钥设置到 `~/.zshenv` 或类似的文件中：
```bash
# Twitter (at least one required for Twitter source)
export TWITTERAPI_IO_KEY="your_key"        # twitterapi.io key (preferred)
export X_BEARER_TOKEN="your_bearer_token"  # Official X API v2 (fallback)
export TWITTER_API_BACKEND="auto"          # auto|twitterapiio|official (default: auto)

# Web Search (optional, enables web search layer)
export WEB_SEARCH_BACKEND="auto"          # auto|brave|tavily (default: auto)
export TAVILY_API_KEY="tvly-xxx"           # Tavily Search API (free 1000/mo)

# Brave Search (alternative)
export BRAVE_API_KEYS="key1,key2,key3"     # Multiple keys, comma-separated rotation
export BRAVE_API_KEY="key1"                # Single key fallback
export BRAVE_PLAN="free"                   # Override rate limit detection: free|pro

# GitHub (optional, improves rate limits)
export GITHUB_TOKEN="ghp_xxx"              # PAT (simplest)
export GH_APP_ID="12345"                   # Or use GitHub App for auto-token
export GH_APP_INSTALL_ID="67890"
export GH_APP_KEY_FILE="/path/to/key.pem"
```

- **Twitter**：推荐使用 `TWITTERAPI_IO_KEY`（每月费用为 3-5 美元）；如果未设置，则使用 `X_BEARER_TOKEN` 作为备用方案；自动模式下优先使用 twitterapiio
- **网页搜索**：在自动模式下推荐使用 Tavily；如果 `TAVILY_API_KEY` 未设置，则使用 Brave；如果 `TAVILY_API_KEY` 也无法使用，则使用代理的 web_search 功能
- **GitHub**：如果未设置 `$GITHUB_TOKEN`，系统会自动生成 GitHub 应用程序令牌；如果未设置令牌，则使用未经认证的访问方式（每小时 60 次请求）
- **Reddit**：无需 API 密钥，直接使用公开的 JSON API

## Cron/定时任务集成

### OpenClaw Cron 脚本（推荐使用）

Cron 脚本中不应硬编码流程步骤。建议参考 `references/digest-prompt.md` 文件，仅传递配置参数。这样可以确保流程逻辑始终保存在技能仓库中，并在所有安装环境中保持一致。

#### 每日摘要任务脚本
```
Read <SKILL_DIR>/references/digest-prompt.md and follow the complete workflow to generate a daily digest.

Replace placeholders with:
- MODE = daily
- TIME_WINDOW = past 1-2 days
- FRESHNESS = pd
- RSS_HOURS = 48
- ITEMS_PER_SECTION = 3-5
- ENRICH = true
- BLOG_PICKS_COUNT = 3
- EXTRA_SECTIONS = (none)
- SUBJECT = Daily Tech Digest - YYYY-MM-DD
- WORKSPACE = <your workspace path>
- SKILL_DIR = <your skill install path>
- DISCORD_CHANNEL_ID = <your channel id>
- EMAIL = (optional)
- LANGUAGE = English
- TEMPLATE = discord

Follow every step in the prompt template strictly. Do not skip any steps.
```

#### 每周摘要任务脚本
```
Read <SKILL_DIR>/references/digest-prompt.md and follow the complete workflow to generate a weekly digest.

Replace placeholders with:
- MODE = weekly
- TIME_WINDOW = past 7 days
- FRESHNESS = pw
- RSS_HOURS = 168
- ITEMS_PER_SECTION = 10-15
- ENRICH = true
- BLOG_PICKS_COUNT = 3-5
- EXTRA_SECTIONS = 📊 Weekly Trend Summary (2-3 sentences summarizing macro trends)
- SUBJECT = Weekly Tech Digest - YYYY-MM-DD
- WORKSPACE = <your workspace path>
- SKILL_DIR = <your skill install path>
- DISCORD_CHANNEL_ID = <your channel id>
- EMAIL = (optional)
- LANGUAGE = English
- TEMPLATE = discord

Follow every step in the prompt template strictly. Do not skip any steps.
```

#### 为什么采用这种模式？
- **单一的配置来源**：流程逻辑集中在 `digest-prompt.md` 文件中，不会分散在多个配置文件中
- **便携性**：在不同的 OpenClaw 实例上只需更改路径和通道 ID 即可
- **易于维护**：更新技能配置后，所有 Cron 任务会自动更新
- **避免错误**：不要将流程步骤直接复制到 Cron 脚本中，否则可能导致配置不一致

#### 多渠道推送限制
OpenClaw 规定每个会话只能向一个平台发送摘要（例如，只能向 Discord 或 Telegram 发送，不能同时发送到两个平台）。如果需要向多个平台推送摘要，需要为每个平台创建单独的 Cron 任务：

```
# Job 1: Discord + Email
- DISCORD_CHANNEL_ID = <your-discord-channel-id>
- EMAIL = user@example.com
- TEMPLATE = discord

# Job 2: Telegram DM
- DISCORD_CHANNEL_ID = (none)
- EMAIL = (none)
- TEMPLATE = telegram
```
请将 `DISCORD_CHANNEL_ID` 替换为目标平台的实际通道 ID。

这是一个安全机制，旨在防止数据在不同平台之间意外泄露。

## 安全注意事项

### 执行模型
该技能采用 **提示模板模式**：代理会读取 `digest-prompt.md` 文件并按照其中的指令执行操作。这是 OpenClaw 的标准执行机制——代理会解析来自技能文件的结构化指令。所有指令都包含在技能包中，并在安装前可以进行审核。

### 网络访问
Python 脚本会向以下地址发送请求：
- RSS 源地址（在 `tech-news-digest-sources.json` 中配置）
- Twitter/X API（`api.x.com` 或 `api.twitterapi.io`）
- Brave 搜索 API（`api.search.brave.com`）
- Tavily 搜索 API（`api.tavily.com`）
- GitHub API（`api.github.com`）
- Reddit JSON API（`reddit.com`）

不会向其他任何地址发送数据。所有 API 密钥都来自技能元数据中定义的环境变量。

### 安全性措施
- 电子邮件发送功能使用 `send-email.py` 工具，该工具会生成包含 HTML 正文的 MIME 多部分邮件；主题格式固定为 `Daily Tech Digest - YYYY-MM-DD`。
- PDF 生成使用 `generate-pdf.py` 和 `weasyprint` 工具；提示模板禁止在脚本参数中插入不可信的内容（如文章标题、推文文本等）。
- 邮件地址和主题都是静态占位符。

### 文件访问权限
脚本仅读取 `config/` 目录下的文件，并将结果写入 `workspace/archive/` 目录；不会访问工作区之外的文件。

## 支持与故障排除

### 常见问题
1. **RSS 源获取失败**：检查网络连接是否正常；可以使用 `--verbose` 参数获取更多详细信息
2. **Twitter 请求速率限制**：减少数据源的数量或增加请求间隔
3. **配置错误**：运行 `validate-config.py` 可以排查具体问题
4. **未找到文章**：检查时间范围（使用 `--hours` 参数）和数据源的启用状态

### 调试模式
所有脚本都支持 `--verbose` 参数，用于启用详细日志记录和故障排查。

### 性能优化
- **并行任务线程**：根据系统配置调整 `MAX_WORKERS` 的值
- **超时设置**：对于网络速度较慢的情况，可以增加 `TIMEOUT` 的值
- **文章数量限制**：根据需要调整 `MAX_ARTICLES_PER_FEED` 的值

### 安全性考虑

- **Shell 执行**：摘要生成脚本会通过 Shell 命令来执行 Python 脚本；所有脚本路径和参数都是预先定义好的，不会接受用户输入
- `run-pipeline.py` 脚本负责协调其他数据获取脚本（所有脚本位于 `scripts/` 目录下）
- `fetch-github.py` 脚本包含两个 `subprocess` 调用：
  1. `openssl dgst -sha256 -sign` 用于生成 JWT 签名（仅在设置了 `GH_APP_*` 环境变量的情况下使用；生成的 JWT 不包含用户提供的内容）
  2. `gh auth token` CLI 调用（仅在安装了 `gh` 工具的情况下使用；从 `gh` 的凭证存储中获取令牌）

所有用户提供的内容或获取的数据都不会被插入到脚本参数中。电子邮件发送使用 `send-email.py` 工具生成 MIME 格式的邮件；PDF 生成使用 `generate-pdf.py` 和 `weasyprint` 工具。邮件主题都是静态字符串，不会根据外部数据动态生成。

### 凭证与文件访问权限
脚本不会直接读取 `~/.config/` 或 `~/.ssh/` 目录下的文件；所有 API 密钥都来自技能元数据中定义的环境变量：
- `GITHUB_TOKEN` 环境变量用于控制令牌的获取方式
- 如果设置了 `GH_APP_ID`、`GH_APP_INSTALL_ID` 和 `GH_APP_KEY_FILE`，系统会自动生成 GitHub 应用程序令牌（使用 `openssl` 命令行工具进行签名）
- 如果未设置这些变量，系统会使用未经认证的访问方式（每小时 60 次请求）

### 依赖项安装
该技能不自动安装任何第三方包；`requirements.txt` 文件中列出的依赖项（`feedparser`、`jsonschema`）仅供参考。用户可以根据需要在使用虚拟环境（virtualenv）中安装这些依赖项；该技能本身不执行 `pip install` 命令。

### 输入内容的安全处理
- 网址解析时会过滤掉非 HTTP(S) 协议的链接（如 `javascript:`、`data:` 等）
- RSS 数据解析使用简单的正则表达式，避免潜在的 DoS 攻击
- 所有获取的数据仅用于显示目的，不会被进一步处理

### 网络访问
脚本会向配置好的 RSS 源地址、Twitter API、GitHub API、Reddit JSON API 和 Tavily 搜索 API 发送请求；不会建立任何入站连接或监听器。