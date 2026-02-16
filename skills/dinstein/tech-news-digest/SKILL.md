---
name: tech-news-digest
description: 生成技术新闻摘要，具备统一的源数据模型、质量评分机制以及多种输出格式。数据收集途径包括 RSS 源、Twitter/X 社交媒体上的意见领袖（KOLs）、GitHub 的代码发布信息以及网络搜索结果。采用基于管道（pipeline-based）的脚本进行处理，具备重试机制和去重功能。支持通过 Discord、电子邮件以及 Markdown 模板进行信息推送。
version: "2.6.1"
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

1. **配置设置**：默认配置位于 `config/defaults/` 文件中。如需自定义，请将其复制到工作区：
   ```bash
   mkdir -p workspace/config
   cp config/defaults/sources.json workspace/config/
   cp config/defaults/topics.json workspace/config/
   ```

2. **环境变量**：
   - `X_BEARER_TOKEN` - Twitter API 令牌（可选）
   - `BRAVE_API_KEY` - Brave Search API 密钥（可选）
   - `GITHUB_TOKEN` - GitHub 个人访问令牌（可选，可提高请求速率限制）

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

### 1. `fetch-rss.py` - RSS 源获取工具
```bash
python3 scripts/fetch-rss.py [--config CONFIG_DIR] [--hours 48] [--output FILE] [--verbose]
```
- **特性**：并行获取数据、重试机制、支持使用 feedparser 和正则表达式进行解析
- **输出**：按主题分类的结构化 JSON 数据
- **超时设置**：每个 RSS 源的请求超时时间为 15 秒，并采用指数级重试策略

### 2. `fetch-twitter.py` - Twitter/X KOL 监控工具
```bash
python3 scripts/fetch-twitter.py [--config CONFIG_DIR] [--hours 48] [--output FILE]
```
- **要求**：需要 `X_BEARER_TOKEN` 环境变量
- **特性**：处理请求速率限制、显示用户互动数据、过滤回复内容
- **API**：使用 Twitter API v2，支持仅限应用的身份验证

### 3. `fetch-web.py` - 网页搜索引擎
```bash
python3 scripts/fetch-web.py [--config CONFIG_DIR] [--freshness 48h] [--output FILE]
```
- **使用 Brave API**：可自动执行搜索（需要 `BRAVE_API_KEY`）
- **不使用 API**：为代理程序生成搜索接口
- **过滤规则**：基于内容的内容筛选规则

### 4. `fetch-github.py` - GitHub 新闻发布监控工具
```bash
python3 scripts/fetch-github.py [--config CONFIG_DIR] [--hours 168] [--output FILE]
```
- **特性**：并行监控 GitHub 仓库、过滤新闻发布内容、去除 Markdown 格式
- **身份验证**：可选的 `GITHUB_TOKEN` 可提高请求速率限制
- **输出**：按主题分类的结构化 JSON 数据

### 5. `merge-sources.py` - 质量评分与去重工具
```bash
python3 scripts/merge-sources.py --rss rss.json --twitter twitter.json --web web.json --github github.json
```
- **评分标准**：来源质量（+3 分）、多源数据（+5 分）、更新频率（+2 分）、用户互动（+1 分）
- **去重机制**：通过标题相似度检测（85% 的阈值）进行去重；避免重复发布相同文章
- **输出**：按主题分组并带有质量评分的文章列表

### 6. `validate-config.py` - 配置验证工具
```bash
python3 scripts/validate-config.py [--defaults DEFAULTS_DIR] [--config CONFIG_DIR] [--verbose]
```
- **JSON 格式验证**：检查数据结构及必填字段
- **一致性检查**：验证主题引用和唯一 ID
- **来源类型**：验证 RSS 链接和 Twitter 账号的有效性

## 用户自定义

### 工作区配置覆盖
将自定义配置文件放在 `workspace/config/` 目录下，以覆盖默认设置：
- **数据源**：添加新的数据源；通过设置 `"enabled": false` 来禁用默认数据源
- **主题设置**：自定义主题定义、搜索查询和显示选项
- **合并逻辑**：
  - 如果多个数据源具有相同的 `id`，则使用用户自定义的配置
  - 如果数据源具有新的 `id`，则将其添加到默认配置中
  - 如果多个主题具有相同的 `id`，则使用用户自定义的配置完全替换默认设置

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
- 采用项目符号列表格式，链接会被自动替换为文本
- 优化适用于移动设备显示，支持表情符号
- 文本长度限制为 2000 个字符

### 电子邮件模板 (`references/templates/email.md`)
- 包含丰富的元数据和技术统计信息、存档链接
- 提供执行摘要和热门文章部分
- 支持 HTML 格式显示

### Markdown 模板 (`references/templates/markdown.md`)
- 支持 GitHub 格式的表格和格式化
- 包含技术细节部分
- 支持可展开的内容结构

## 默认数据源（共 109 个）

- **RSS 源（46 个）**：AI 实验室、科技博客、加密货币新闻、中国科技媒体
- **Twitter/X KOL（44 个）**：AI 研究人员、加密货币领域专家、科技行业高管
- **GitHub 仓库（19 个）**：主要开源项目（如 LangChain、vLLM、Foundry 等）
- **网页搜索（4 个主题）**：大语言模型（LLM）、AI 代理程序、加密货币、前沿科技领域

所有数据源都预先配置了相应的主题标签和优先级。

## 依赖库

```bash
pip install -r requirements.txt
```

**推荐安装（非强制）**：
- `feedparser>=6.0.0`：提供更好的 RSS 解析功能（如果 `feedparser` 无法使用，则使用正则表达式作为备用方案）
- `jsonschema>=4.0.0`：用于配置验证

**所有脚本仅支持 Python 3.8 及更高版本的标准库。**

## 从 v1.x 版本升级**

1. **配置迁移**：旧配置文件会自动转换为新格式
2. **脚本更新**：提供了新的命令行接口，并增强了错误处理功能
3. **模板系统**：将旧的基于提示符的生成方式替换为模板系统
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
- 使用之前的摘要标题来检测重复内容
- 过期的档案会自动清理（保留时间超过 90 天）

### 错误处理
- **网络故障**：采用指数级重试策略进行恢复
- **请求速率限制**：自动重试并设置适当的延迟时间
- **无效内容**：系统会优雅地处理错误并记录详细日志
- **配置错误**：通过验证 JSON 结构来提示错误信息

## API 密钥与环境设置

请将相关密钥设置到 `~/.zshenv` 或类似文件中：
```bash
export X_BEARER_TOKEN="your_twitter_bearer_token"
export BRAVE_API_KEY="your_brave_search_api_key"  # Optional
```

- **Twitter**：提供只读权限的 API 令牌，按使用次数计费
- **Brave Search**：可选；如果 `BRAVE_API_KEY` 无法使用，则使用 `web_search` 功能作为备用方案

## Cron/定时任务集成

### 推荐的 OpenClaw Cron 配置方式

Cron 脚本不应直接硬编码流程步骤，而应引用 `references/digest-prompt.md` 文件，并仅传递配置参数。这样可以确保流程逻辑始终保存在技能包中，并在所有安装环境中保持一致。

#### 每日摘要任务的 Cron 配置示例
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

#### 每周摘要任务的 Cron 配置示例
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

#### 为何采用这种模式？
- **单一信息源**：所有流程逻辑都保存在 `digest-prompt.md` 文件中，避免分散在多个配置文件中
- **便携性**：在不同 OpenClaw 实例上只需修改路径和频道 ID 即可
- **易于维护**：更新技能包后，所有定时任务会自动更新
- **避免误区**：切勿将流程步骤直接复制到 Cron 脚本中，否则可能导致配置不一致

#### 多渠道推送限制
OpenClaw 实施了 **跨平台隔离** 规则：同一会话只能向一个平台发送消息（例如，只能向 Discord 或 Telegram 发送摘要）。如果需要向多个平台推送摘要，请为每个平台创建单独的 Cron 任务：

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
在第二个任务的 Cron 配置中，将 `DISCORD_CHANNEL_ID` 替换为 `telegram_channel_ID`（使用 `message` 工具并设置 `channel=telegram`）。

这是一种安全措施，旨在防止数据泄露。

## 安全注意事项

### 执行机制
该技能采用 **提示模板模式**：代理程序会读取 `digest-prompt.md` 文件并按照其中的指示执行操作。这是 OpenClaw 的标准执行方式——代理程序会解析来自技能包的结构化指令。所有指令都会随技能包一起提供，并在安装前进行审核。

### 网络访问
Python 脚本会访问以下地址：
- RSS 源地址（在 `sources.json` 中配置）
- Twitter/X API（`api.x.com`）
- Brave Search API（`api.search.brave.com`）
- GitHub API（`api.github.com`）

脚本不会向其他任何地址发送数据。所有 API 密钥都来自技能元数据中定义的环境变量。

### Shell 安全性
- 电子邮件发送功能使用 `gog` CLI 工具，主题格式固定为 `Daily Tech Digest - YYYY-MM-DD`
- 提示模板禁止在 Shell 命令中插入不可信的内容

### 文件访问权限
脚本仅读取 `config/` 目录下的文件，并将结果写入 `workspace/archive/` 目录。不会访问工作区之外的文件。

## 支持与故障排除

### 常见问题
1. **RSS 源无法访问**：检查网络连接状态，可使用 `--verbose` 参数获取更多详细信息
2. **Twitter 请求速率限制**：减少数据源数量或增加请求间隔
3. **配置错误**：运行 `validate-config.py` 以排查具体问题
4. **未找到文章**：检查时间范围（通过 `--hours` 参数设置）和数据源是否启用

### 调试模式
所有脚本都支持 `--verbose` 参数，用于输出详细日志和辅助故障排查

### 性能优化
- **并行处理**：根据系统配置调整 `MAX_WORKERS` 的值
- **超时设置**：对于网络速度较慢的情况，增加 `TIMEOUT` 的值
- **文章数量限制**：根据需要调整 `MAX_ARTICLES_PER_feed` 的值

## 安全考虑

### Shell 执行方式
该技能通过 Shell 命令执行脚本。所有脚本路径和参数都是预先定义好的，用户无法修改这些参数。脚本本身不包含 `subprocess` 或 `os.system` 相关的调用。

### 第三方 RSS 源
其中一个 RSS 源（`anthropic-rss`）使用社区维护的 GitHub 镜像，因为 Anthropic 没有官方的 RSS 源。用户应注意使用第三方镜像可能带来的供应链风险。相关信息会在 `sources.json` 文件中明确标注。

### 输入内容处理
- URL 处理会排除非 HTTP(S) 协议的链接（如 `javascript:`、`data:` 等）
- RSS 解析使用简单的正则表达式，避免潜在的 DoS 攻击风险
- 所有获取的数据仅用于显示目的，不进行进一步处理

### 网络访问
脚本会向配置的 RSS 源、Twitter API、GitHub API 和 Brave Search API 发送请求，但不会接收任何数据。

### 其他注意事项
- 所有脚本都遵循 OpenClaw 的安全规范，不会泄露任何敏感信息。