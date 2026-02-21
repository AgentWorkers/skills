---
name: tech-news-digest
description: 生成技术新闻摘要，具备统一的源模型、质量评分功能以及多种输出格式。数据收集渠道包括 RSS 源、Twitter/X 的意见领袖（KOLs）、GitHub 的代码发布信息、Reddit 网站以及网络搜索结果。采用基于管道（pipeline）的脚本进行处理，支持重试机制和数据去重功能。同时支持通过 Discord、电子邮件以及 Markdown 模板进行内容分发。
version: "3.6.0"
homepage: https://github.com/draco-agent/tech-news-digest
source: https://github.com/draco-agent/tech-news-digest
metadata:
  openclaw:
    requires:
      bins: ["python3"]
    optionalBins: ["mail", "msmtp", "gog", "gh", "openssl"]
env:
  - name: X_BEARER_TOKEN
    required: false
    description: Twitter/X API bearer token for KOL monitoring
  - name: BRAVE_API_KEY
    required: false
    description: Brave Search API key for web search layer
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
    - <workspace>/archive/tech-news-digest/: Saved digest archives
---
# 技术新闻摘要系统

这是一个自动化的技术新闻摘要系统，采用统一的数据源模型、质量评分流程以及基于模板的输出生成方式。

## 快速入门

1. **配置设置**：默认配置位于 `config/defaults/` 文件中。您可以将这些配置复制到工作区进行自定义：
   ```bash
   mkdir -p workspace/config
   cp config/defaults/sources.json workspace/config/
   cp config/defaults/topics.json workspace/config/
   ```

2. **环境变量**：
   - `X_BEARER_TOKEN` - Twitter API 令牌（可选）
   - `BRAVE_API_KEY` - Brave Search API 密钥（可选）
   - `GITHUB_TOKEN` - GitHub 个人访问令牌（可选，可提升请求速率限制）

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

4. **使用模板**：您可以将生成的摘要内容应用到 Discord、电子邮件或 Markdown 格式中。

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

### `run-pipeline.py` - 统一的脚本流程（推荐使用）
```bash
python3 scripts/run-pipeline.py \
  --defaults config/defaults [--config CONFIG_DIR] \
  --hours 48 --freshness pd \
  --archive-dir workspace/archive/tech-news-digest/ \
  --output /tmp/td-merged.json --verbose --force
```
- **特点**：并行执行所有 5 个数据获取步骤，然后进行合并、去重和评分
- **输出**：最终合并后的 JSON 数据，可用于生成报告（总耗时约 30 秒）
- **元数据**：将每个步骤的耗时和执行次数保存到 `*.meta.json` 文件中
- **GitHub 认证**：如果未设置 `$GITHUB_TOKEN`，系统会自动生成 GitHub 应用程序令牌
- **备用方案**：如果此步骤失败，系统将单独运行以下脚本

### 单个脚本（备用方案）

#### `fetch-rss.py` - RSS 源获取脚本
```bash
python3 scripts/fetch-rss.py [--defaults DIR] [--config DIR] [--hours 48] [--output FILE] [--verbose]
```
- 并行获取数据（使用 10 个线程），采用退避策略进行重试；支持使用 feedparser 和正则表达式进行解析
- 每个 RSS 源的超时时间为 30 秒；支持 ETag/Last-Modified 的缓存机制

#### `fetch-twitter.py` - Twitter/X KOL 监控脚本
```bash
python3 scripts/fetch-twitter.py [--defaults DIR] [--config DIR] [--hours 48] [--output FILE]
```
- 需要 `X_BEARER_TOKEN`；支持处理请求速率限制；提供参与度指标

#### `fetch-web.py` - 网页搜索引擎脚本
```bash
python3 scripts/fetch-web.py [--defaults DIR] [--config DIR] [--freshness pd] [--output FILE]
```
- 自动检测 Brave API 的请求速率限制：付费用户可使用并行查询；免费用户则采用顺序查询方式
- 如果没有 Brave API，系统会为代理生成搜索接口

#### `fetch-github.py` - GitHub 发布信息监控脚本
```bash
python3 scripts/fetch-github.py [--defaults DIR] [--config DIR] [--hours 168] [--output FILE]
```
- 并行获取数据（使用 10 个线程），超时时间为 30 秒
- 认证优先级：优先使用 `$GITHUB_TOKEN` 生成的令牌；如果未设置，则使用 GitHub 应用程序令牌或 `gh` CLI；未设置令牌时，每小时最多发送 60 次请求

#### `fetch-reddit.py` - Reddit 帖子获取脚本
```bash
python3 scripts/fetch-reddit.py [--defaults DIR] [--config DIR] [--hours 48] [--output FILE]
```
- 并行获取数据（使用 4 个线程），使用公开的 JSON API（无需认证）
- 支持从 13 个 subreddit 中筛选文章

#### `merge-sources.py` - 质量评分与去重脚本
```bash
python3 scripts/merge-sources.py --rss FILE --twitter FILE --web FILE --github FILE --reddit FILE
```
- 对文章进行质量评分；根据相似度去除重复内容（去除 85% 的重复项）；对重复的文章进行降分处理
- 输出结果按评分排序，按主题分组显示

#### `validate-config.py` - 配置验证脚本
```bash
python3 scripts/validate-config.py [--defaults DIR] [--config DIR] [--verbose]
```
- 验证 JSON 数据的结构；检查主题引用是否正确；检测重复的 ID

## 用户自定义

### 工作区配置覆盖
将自定义配置文件放置在 `workspace/config/` 目录下，以覆盖默认配置：
- **数据源**：添加新的数据源；通过设置 `"enabled": false` 来禁用默认数据源
- **主题**：覆盖主题定义、搜索查询规则和显示设置
- **合并逻辑**：
  - 如果数据源的 ID 相同，则使用用户自定义的配置
  - 如果数据源的 ID 新增，则将其添加到默认配置中
  - 如果主题的 ID 相同，则完全替换默认配置

### 示例工作区配置覆盖
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
- 采用项目符号列表格式；链接会自动被替换为实际的链接地址
- 适合移动设备显示；支持使用表情符号
- 总长度限制为 2000 个字符

### 电子邮件模板 (`references/templates/email.md`)
- 包含丰富的元数据和技术统计信息；提供文章链接
- 包含执行摘要和热门文章部分
- 支持 HTML 格式

### Markdown 模板 (`references/templates/markdown.md`)
- 支持 GitHub 标准的表格格式
- 包含技术细节部分
- 支持可扩展的内容结构

## 默认数据源（共 133 个）

- **RSS 源（49 个）**：AI 实验室、技术博客、加密货币新闻、中文科技媒体
- **Twitter/X KOL（49 个）**：AI 研究人员、加密货币领域专家、科技行业高管
- **GitHub 仓库（22 个）**：主要的开源项目（如 LangChain、vLLM、DeepSeek、Llama 等）
- **Reddit（13 个）**：r/MachineLearning、r/LocalLLaMA、r/CryptoCurrency、r/ChatGPT、r/OpenAI 等板块
- **网页搜索（4 个主题）**：LLM、AI 代理、加密货币、前沿科技相关内容

所有数据源都预先配置了相应的主题标签和优先级。

## 依赖项

```bash
pip install -r requirements.txt
```

**推荐安装（虽然非强制）**：
- `feedparser>=6.0.0`：提供更好的 RSS 解析功能（如果 `feedparser` 无法使用，系统会使用正则表达式进行解析）
- `jsonschema>=4.0.0`：用于配置验证

**所有脚本仅支持 Python 3.8 及更高版本的标准库。**

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
- 摘要内容会自动归档到 `<workspace>/archive/tech-news-digest/` 目录中
- 使用之前的摘要标题来检测重复内容
- 过期的档案会自动清理（保留时间超过 90 天）

### 错误处理
- **网络故障**：采用指数级退避策略进行重试
- **请求速率限制**：自动重试，并设置适当的延迟时间
- **内容无效**：系统会优雅地处理错误，并记录详细的日志
- **配置错误**：系统会验证配置文件，并提供相应的错误提示

## API 密钥与环境设置

请将相关 API 密钥设置到 `~/.zshenv` 或类似的文件中：
```bash
export X_BEARER_TOKEN="your_twitter_bearer_token"
export BRAVE_API_KEY="your_brave_search_api_key"  # Optional
```

- **Twitter**：提供只读权限的令牌；采用按使用次数计费的模式
- **Brave Search**：可选；如果 `feedparser` 无法使用，系统会使用 `web_search` 脚本作为备用方案

## Cron/定时任务集成

### 推荐使用 OpenClaw 的 Cron 任务

Cron 任务中 **不应** 直接编写脚本的执行逻辑。请参考 `references/digest-prompt.md` 文件，仅传递配置参数。这样可以确保脚本逻辑始终保存在技能仓库中，并在所有安装环境中保持一致。

#### 每日摘要任务的 Cron 语法
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

#### 每周摘要任务的 Cron 语法
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

#### 为何采用这种设计？
- **单一的配置来源**：所有脚本逻辑都保存在 `digest-prompt.md` 文件中，避免分散在多个配置文件中
- **便携性**：在不同版本的 OpenClaw 中只需更改路径和频道 ID 即可
- **易于维护**：更新技能配置后，所有 Cron 任务会自动更新
- **避免错误**：切勿将脚本逻辑直接写入 Cron 任务中，否则可能导致配置不一致

#### 多渠道推送限制
OpenClaw 限制同一会话只能向一个平台发送消息（例如，只能通过 Discord 或 Telegram 发送摘要）。如果需要向多个平台推送摘要，请为每个平台创建单独的 Cron 任务：

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
在第二个 Cron 任务的配置中，将 `DISCORD_CHANNEL_ID` 替换为 Telegram 的通道 ID（使用 `message` 命令，并设置 `channel=telegram`）。

这是出于安全考虑的设计，防止数据在不同平台之间意外泄露。

## 安全注意事项

### 执行机制
该技能采用 **提示模板模式**：代理程序会读取 `digest-prompt.md` 文件并按照其中的指令执行操作。这是 OpenClaw 的标准执行机制——代理程序会解析来自技能文件的结构化指令。所有指令都会随技能包一起提供，并在安装前进行审核。

### 网络访问
Python 脚本会向以下地址发送请求：
- RSS 源地址（在 `sources.json` 中配置）
- Twitter/X API（`api.x.com`）
- Brave Search API（`api.search.brave.com`）
- GitHub API（`api.github.com`）

系统不会向其他任何地址发送数据。所有 API 密钥都来自技能元数据中定义的环境变量。

### Shell 安全性
- 电子邮件发送功能支持两种命令行工具：`mail`（msmtp）和 `gog`（备用方案）。这两种工具都使用固定的邮件主题格式（`Daily Tech Digest - YYYY-MM-DD`），并从临时文件 `/tmp/td-email.html` 中读取邮件正文。提示模板明确禁止在 Shell 命令中插入不可信的内容（如文章标题、推文文本等）。
- 邮件地址和主题必须是静态的占位符。

### 文件访问权限
脚本会从 `config/` 目录读取数据，并将结果写入 `workspace/archive/` 目录。系统不会访问工作区之外的文件。

## 支持与故障排除

### 常见问题
1. **RSS 源无法获取数据**：检查网络连接是否正常；可以使用 `--verbose` 参数获取更多调试信息
2. **Twitter 请求速率限制**：减少数据源的数量或增加数据获取的间隔时间
3. **配置错误**：运行 `validate-config.py` 命令以检查配置问题
4. **未找到文章**：检查设置的时间范围（`--hours` 参数）和数据源是否已启用

### 调试模式
所有脚本都支持 `--verbose` 参数，用于输出详细的日志信息以便排查问题。

### 性能优化
- **并行处理**：根据系统配置调整 `MAX_WORKERS` 的值
- **超时设置**：对于网络速度较慢的情况，可以增加 `TIMEOUT` 的值
- **文章数量限制**：根据需要调整 `MAX_ARTICLES_PER_FEED` 的值

## 安全性考虑

### Shell 执行方式
该技能通过 Shell 命令来执行脚本。所有脚本的路径和参数都是预先定义好的，用户无法修改这些参数。其中两个脚本使用了 `subprocess` 模块：
- `run-pipeline.py` 负责协调其他数据获取脚本的运行（所有脚本都在 `scripts/` 目录下）
- `fetch-github.py` 包含两个 `subprocess` 调用：
  1. `openssl dgst -sha256 -sign` 用于生成 JWT 签名（仅在设置了 `GH_APP_*` 环境变量的情况下使用；生成的 JWT 不包含用户提供的内容）
  2. `gh auth token` CLI（仅在安装了 `gh` 工具的情况下使用；从 `gh` 的认证系统中获取令牌）

系统不会将用户提供的内容或获取的数据插入到 `subprocess` 的参数中。在发送电子邮件时，系统会将 HTML 内容写入临时文件 `/tmp/td-email.html`，然后再通过 `mail`（msmtp）或 `gog` CLI 发送。邮件主题也是静态的占位符，不会根据获取的数据动态生成。

### 凭据管理
脚本不会直接读取 `~/.config/` 或 `~/.ssh/` 目录中的配置文件。所有 API 密钥都来自技能元数据中定义的环境变量：
- `$GITHUB_TOKEN`：用户需要自行设置
- GitHub 应用程序令牌的生成：仅在设置了 `GH_APP_ID`、`GH_APP_INSTALL_ID` 和 `GH_APP_KEY_FILE` 时使用；使用 `openssl` CLI 进行 JWT 签名
- `gh auth token` CLI：使用 `gh` 自带的认证系统

### 依赖项的安装
该技能本身不安装任何第三方包。`requirements.txt` 文件中列出的依赖项（`feedparser`、`jsonschema`）仅供参考。用户可以在虚拟环境中安装这些依赖项；该技能本身不执行 `pip install` 命令。

### 输入数据的安全处理
- 系统会过滤非 HTTP(S) 协议的 URL
- RSS 数据的解析使用简单的正则表达式，避免潜在的 DoS 攻击
- 所有获取的数据仅用于显示目的，不会被进一步处理

### 网络访问
脚本会向配置好的 RSS 源、Twitter API、GitHub API 和 Reddit JSON API 发送请求。系统不会建立任何入站连接或监听器。