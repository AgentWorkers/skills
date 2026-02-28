---
name: tech-news-digest
description: 生成技术新闻摘要，采用统一的源模型、质量评分机制以及多种输出格式。数据来源包括 RSS 源、Twitter/X 社交媒体上的意见领袖（KOLs）、GitHub 的代码发布信息、Reddit 网站以及网络搜索结果。整个系统基于管道式脚本设计，具备重试机制和去重功能。支持通过 Discord、电子邮件以及 Markdown 模板进行信息推送。
version: "3.11.0"
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

1. **配置设置**：默认配置位于 `config/defaults/` 文件中。请将其复制到工作区进行自定义：
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
   - `BRAVE_API_KEYS` - Brave 搜索 API 的密钥（用逗号分隔，用于轮询）
   - `BRAVE_API_KEY` - 单个 Brave API 密钥（作为备用方案）
   - `GITHUB_TOKEN` - GitHub 个人访问令牌（可选，可提高请求速率）

3. **生成摘要**：
   ```bash
   # Unified pipeline (recommended) — runs all 5 sources in parallel + merge
   python3 scripts/run-pipeline.py \
     --defaults config/defaults \
     --config workspace/config \
     --hours 48 --freshness pd \
     --archive-dir workspace/archive/tech-news-digest/ \
     --output /tmp/td-merged.json --verbose --force
   ```

4. **使用模板**：将摘要内容应用到 Discord、电子邮件或 PDF 模板中。

## 配置文件

### `sources.json` - 统一数据源
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

### `topics.json` - 强化后的主题定义
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

### `run-pipeline.py` - 统一处理流程（推荐使用）
```bash
python3 scripts/run-pipeline.py \
  --defaults config/defaults [--config CONFIG_DIR] \
  --hours 48 --freshness pd \
  --archive-dir workspace/archive/tech-news-digest/ \
  --output /tmp/td-merged.json --verbose --force
```
- **特性**：并行执行所有 5 个数据获取步骤，然后合并、去重并评分
- **输出**：最终合并后的 JSON 数据，可用于生成报告（总耗时约 30 秒）
- **元数据**：将每一步的耗时和计数保存到 `*.meta.json` 文件中
- **GitHub 认证**：如果未设置 `$GITHUB_TOKEN`，则会自动生成 GitHub 应用程序令牌
- **备用方案**：如果此步骤失败，将单独运行以下脚本

### 单个脚本（备用方案）

#### `fetch-rss.py` - RSS 源获取脚本
```bash
python3 scripts/fetch-rss.py [--defaults DIR] [--config DIR] [--hours 48] [--output FILE] [--verbose]
```
- 并行获取数据（使用 10 个线程），具有重试机制和回退策略；支持 feedparser 和正则表达式解析
- 每个 RSS 源的超时时间为 30 秒，支持 ETag/Last-Modified 缓存

#### `fetch-twitter.py` - Twitter/X KOL 监控脚本
```bash
python3 scripts/fetch-twitter.py [--defaults DIR] [--config DIR] [--hours 48] [--output FILE] [--backend auto|official|twitterapiio]
```
- 自动检测后端：如果设置了 `TWITTERAPI_IO_KEY`，则使用 twitterapi.io；如果设置了 `X_BEARER_TOKEN`，则使用官方 X API v2
- 处理请求速率限制，记录互动指标，并具有重试机制

#### `fetch-web.py` - 网页搜索引擎脚本
```bash
python3 scripts/fetch-web.py [--defaults DIR] [--config DIR] [--freshness pd] [--output FILE]
```
- 自动检测 Brave API 的请求速率限制：付费计划支持并行查询，免费计划则按顺序执行
- 如果没有 API，则为代理生成搜索界面

#### `fetch-github.py` - GitHub 仓库更新脚本
```bash
python3 scripts/fetch-github.py [--defaults DIR] [--config DIR] [--hours 168] [--output FILE]
```
- 并行获取数据（使用 10 个线程），超时时间为 30 秒
- 认证优先级：`$GITHUB_TOKEN` → 自动生成的 GitHub 应用程序令牌 → `gh` CLI → 未经认证的请求（每小时 60 次）

#### `fetch-reddit.py` - Reddit 帖子获取脚本
```bash
python3 scripts/fetch-reddit.py [--defaults DIR] [--config DIR] [--hours 48] [--output FILE]
```
- 并行获取数据（使用 4 个线程），使用公共的 JSON API（无需认证）
- 支持过滤特定子版块的帖子

#### `merge-sources.py` - 质量评分与去重脚本
```bash
python3 scripts/merge-sources.py --rss FILE --twitter FILE --web FILE --github FILE --reddit FILE
```
- 进行质量评分，去除重复标题（相似度超过 85% 的标题会被剔除），并对文章进行排序

#### `validate-config.py` - 配置验证脚本
```bash
python3 scripts/validate-config.py [--defaults DIR] [--config DIR] [--verbose]
```
- 验证 JSON 数据结构，检查主题引用，检测重复的 ID

#### `generate-pdf.py` - PDF 报告生成脚本
```bash
python3 scripts/generate-pdf.py --input report.md --output digest.pdf [--verbose]
```
- 将 Markdown 格式的摘要内容转换为带有中文排版的 A4 PDF 文件（使用 Noto Sans CJK SC 字体）
- 支持表情符号、页眉/页脚设计，采用蓝色主题风格；需要 `weasyprint` 工具

#### `sanitize-html.py` - 安全的 HTML 电子邮件转换脚本
```bash
python3 scripts/sanitize-html.py --input report.md --output email.html [--verbose]
```
- 将 Markdown 内容转换为安全的 HTML 格式，适用于电子邮件发送
- 支持 URL 白名单（仅限 http/https），并对文本内容进行 HTML 转义

#### `source-health.py` - 数据源健康检查脚本
```bash
python3 scripts/source-health.py --rss FILE --twitter FILE --github FILE --reddit FILE --web FILE [--verbose]
```
- 跟踪每个数据源在 7 天内的成功/失败记录
- 报告失败率超过 50% 的数据源

#### `summarize-merged.py` - 合并数据总结脚本
```bash
python3 scripts/summarize-merged.py --input merged.json [--top N] [--topic TOPIC]
```
- 生成便于人类阅读的合并数据摘要，供大型语言模型（LLM）使用
- 显示每个主题下的热门文章及其评分和指标

## 用户自定义

### 工作区配置覆盖
将自定义配置文件放在 `workspace/config/` 目录下，以覆盖默认设置：

- **数据源**：添加新的数据源；通过设置 `"enabled": false` 来禁用默认数据源
- **主题**：覆盖主题定义、搜索查询和显示设置
- **合并逻辑**：
  - 如果数据源的 `id` 相同，则使用用户自定义的配置
  - 如果数据源的 `id` 新增，则将其添加到默认配置中
  - 如果主题的 `id` 相同，则完全替换默认配置

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
- 使用项目符号列表格式，并省略链接 `<link>`
- 适用于移动设备显示，包含表情符号
- 遵循 2000 字符的限制

### 电子邮件模板 (`references/templates/email.md`)
- 包含丰富的元数据和技术统计信息，以及归档链接
- 提供执行摘要和热门文章部分
- 支持 HTML 格式显示

### PDF 模板 (`references/templates/pdf.md`)
- 使用 A4 页面布局和 Noto Sans CJK SC 字体
- 支持表情符号、页眉/页脚以及页码显示
- 通过 `scripts/generate-pdf.py` 生成（需要 `weasyprint` 工具）

## 默认数据源（共 138 个）

- **RSS 源（49 个）**：AI 实验室、技术博客、加密货币新闻、中文科技媒体
- **Twitter/X KOL（48 个）**：AI 研究人员、加密货币领域领导者、科技高管
- **GitHub 仓库（28 个）**：主要的开源项目（如 LangChain、vLLM、DeepSeek、Llama 等）
- **Reddit（13 个）**：r/MachineLearning、r/LocalLLaMA、r/CryptoCurrency、r/ChatGPT、r/OpenAI 等子版块
- **网页搜索（4 个主题）**：LLM、AI 代理、加密货币、前沿科技

所有数据源都预先配置了相应的主题标签和优先级。

## 依赖项

```bash
pip install -r requirements.txt
```

**推荐但非强制安装的依赖项**：
- `feedparser>=6.0.0` - 更优秀的 RSS 解析功能（如果 `feedparser` 无法使用，可回退到正则表达式解析）
- `jsonschema>=4.0.0` - 用于配置验证

**所有脚本均仅支持 Python 3.8 及更高版本的标准库。**

## 监控与操作

### 健康检查
```bash
# Validate configuration
python3 scripts/validate-config.py --verbose

# Test RSS feeds
python3 scripts/fetch-rss.py --hours 1 --verbose

# Check Twitter API
python3 scripts/fetch-twitter.py --hours 1 --verbose
```

### 归档管理
- 摘要内容会自动归档到 `<workspace>/archive/tech-news-digest/` 目录
- 使用之前的摘要标题来检测重复内容
- 过期的归档文件会自动清理（保留时间超过 90 天）

### 错误处理
- **网络故障**：采用指数级重试策略进行重试
- **请求速率限制**：自动重试并设置适当的延迟
- **无效内容**：优雅地处理错误，并详细记录日志
- **配置错误**：进行配置验证，并提供有用的错误信息

## API 密钥与环境设置

请将相关密钥设置到 `~/.zshenv` 或类似的文件中：
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

- **Twitter**：推荐使用 `TWITTERAPI_IO_KEY`（每月费用 3-5 美元）；`X_BEARER_TOKEN` 作为备用方案；`auto` 模式优先使用 twitterapi.io
- **网页搜索**：在 `auto` 模式下推荐使用 Tavily；如果 `TAVILY_API_KEY` 无法使用，则使用 Brave 的 Web 搜索功能
- **GitHub**：如果未设置 `$GITHUB_TOKEN`，则会自动生成 GitHub 应用程序令牌；如果未设置令牌，则使用未经认证的请求方式（每小时 60 次请求）
- **Reddit**：无需 API 密钥（使用公开的 JSON API）

## Cron / 定时任务集成

### OpenClaw Cron 配置（推荐使用）

Cron 脚本中 **不应** 直接编写流程步骤。应参考 `references/digest-prompt.md` 文件，并仅传递配置参数。这样可以确保流程逻辑始终保存在技能仓库中，并在所有安装环境中保持一致。

#### 每日摘要任务配置
```
Read <SKILL_DIR>/references/digest-prompt.md and follow the complete workflow to generate a daily digest.

Replace placeholders with:
- MODE = daily
- TIME_WINDOW = past 1-2 days
- FRESHNESS = pd
- RSS_HOURS = 48
- ITEMS_PER_SECTION = 3-5
- BLOG_PICKS_COUNT = 2-3
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

#### 每周摘要任务配置
```
Read <SKILL_DIR>/references/digest-prompt.md and follow the complete workflow to generate a weekly digest.

Replace placeholders with:
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
- EMAIL = (optional)
- LANGUAGE = English
- TEMPLATE = discord

Follow every step in the prompt template strictly. Do not skip any steps.
```

#### 为什么采用这种模式？
- **单一的真相来源**：流程逻辑集中在 `digest-prompt.md` 文件中，不会分散在多个 Cron 配置文件中
- **便携性**：在不同 OpenClaw 实例上可以重复使用该技能，只需更改路径和频道 ID 即可
- **易维护性**：更新技能配置后，所有 Cron 任务会自动更新
- **避免错误**：不要将流程步骤直接写入 Cron 脚本中，否则可能导致配置不一致

#### 多渠道推送限制
OpenClaw 实施了 **跨提供者隔离** 规则：一个会话只能向一个提供者发送消息（例如，只能向 Discord 或 Telegram 发送摘要）。如果需要向多个平台推送摘要，需要为每个平台创建单独的 Cron 任务：

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
请将 `DISCORD_CHANNEL_ID` 替换为目标平台的相应值。

这是一个安全机制，旨在防止数据在不同平台之间意外泄露。

## 安全注意事项

### 执行模型
该技能采用 **提示模板模式**：代理程序会读取 `digest-prompt.md` 文件并按照其中的指示执行操作。这是 OpenClaw 的标准执行模型——代理程序会解析来自技能文件的结构化指令。所有指令都包含在技能包中，并在安装前可以进行审核。

### 网络访问
Python 脚本会向以下地址发送请求：
- RSS 源地址（在 `tech-news-digest-sources.json` 中配置）
- Twitter/X API（`api.x.com` 或 `api.twitterapi.io`）
- Brave 搜索 API（`api.search.brave.com`）
- Tavily 搜索 API（`api.tavily.com`）
- GitHub API（`api.github.com`）
- Reddit JSON API（`reddit.com`）

不会向其他任何地址发送数据。所有 API 密钥都从技能元数据中指定的环境变量中获取。

### Shell 安全性
- 电子邮件发送功能使用 `send-email.py` 工具，该工具会构建包含 HTML 正文和可选 PDF 附件的 MIME 多部分消息
- 主题格式固定为 `Daily Tech Digest - YYYY-MM-DD`
- PDF 生成使用 `generate-pdf.py` 和 `weasyprint` 工具
- 提示模板明确禁止在 Shell 命令中插入不可信的内容（如文章标题、推文文本等）
- 电子邮件地址和主题必须是静态的占位符

### 文件访问权限
脚本仅读取 `config/` 目录中的文件，并将结果写入 `workspace/archive/` 目录。不会访问工作区之外的文件

## 支持与故障排除

### 常见问题
1. **RSS 源获取失败**：检查网络连接是否正常；可以使用 `--verbose` 参数获取更多详细信息
2. **Twitter 请求速率限制**：减少数据源的数量或增加请求间隔
3. **配置错误**：运行 `validate-config.py` 可以排查具体问题
4. **找不到文章**：检查时间范围（通过 `--hours` 参数设置）和数据源是否启用

### 调试模式
所有脚本都支持 `--verbose` 参数，用于启用详细日志记录和故障排除

### 性能优化
- **并行处理**：根据系统配置调整 `MAX_WORKERS` 变量
- **超时设置**：对于网络速度较慢的情况，增加 `TIMEOUT` 值
- **文章数量限制**：根据需要调整 `MAX_ARTICLES_PER_feed` 变量

## 安全考虑

### Shell 执行方式
摘要生成脚本通过 Shell 命令来执行 Python 脚本。所有脚本路径和参数都是预先定义好的，不会接受用户输入
- `run-pipeline.py` 脚本负责协调其他数据获取脚本（都在 `scripts/` 目录中）
- `fetch-github.py` 脚本包含两个 `subprocess` 调用：
  1. `openssl dgst -sha256 -sign` 用于生成 JWT 签名（仅在设置了 `GH_APP_*` 环境变量时使用；生成的 JWT 不包含用户提供的内容）
  2. `gh auth token` CLI 调用（仅在安装了 `gh` 工具时使用；从 `gh` 的认证系统中获取令牌）

所有用户提供的内容或获取的数据都不会被插入到脚本的执行参数中。电子邮件发送使用 `send-email.py` 工具构建 MIME 消息；PDF 生成使用 `generate-pdf.py` 和 `weasyprint` 工具。电子邮件主题是静态字符串，不会根据外部数据动态生成。

### 凭据与文件访问权限
脚本不会直接读取 `~/.config/` 或 `~/.ssh/` 目录中的文件。所有 API 密钥都从技能元数据中指定的环境变量中获取：
- `GITHUB_TOKEN` 环境变量用于控制令牌的来源
- 如果设置了 `GH_APP_ID`、`GH_APP_INSTALL_ID` 和 `GH_APP_KEY_FILE`，则会自动生成 GitHub 应用程序令牌（使用 `openssl` 命令行工具进行签名）
- 如果未设置这些变量，则使用未经认证的请求方式（每小时 60 次请求）

如果您不希望自动获取凭证，只需设置 `$GITHUB_TOKEN`，脚本将直接使用该令牌，而不会执行额外的认证步骤。

### 依赖项安装
该技能不自动安装任何第三方包。`requirements.txt` 文件中列出的依赖项（`feedparser`、`jsonschema`）仅供参考。所有脚本均支持 Python 3.8 及更高版本的标准库。用户可以根据需要在使用虚拟环境（virtualenv）中安装这些依赖项；技能本身不会自动执行 `pip install` 命令。

### 输入内容处理
- URL 解析时会过滤非 HTTP(S) 协议的链接（如 javascript:、data: 等）
- RSS 数据解析使用简单的正则表达式，避免 DoS 攻击
- 所有获取的数据仅用于显示目的，不会被进一步处理

### 网络访问
脚本会向配置好的 RSS 源地址、Twitter API、GitHub API、Reddit JSON API 和 Tavily 搜索 API 发送请求，但不会建立任何入站连接或监听器。