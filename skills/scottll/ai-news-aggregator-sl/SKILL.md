---
name: ai-news-aggregator-sl
description: 从 RSS 源、Tavily 搜索引擎、Twitter 和 YouTube 中获取人工智能与科技新闻（默认设置）或任何自定义主题（如加密货币、地缘政治等）的相关内容。利用 DeepSeek AI 生成英文编辑摘要，并将其发布到 Discord 上。支持选择不同的时间范围（今日、过去 3 天、过去一周）。当用户请求新闻、摘要、热门话题或特定主题的 YouTube 更新时，系统会自动触发相应操作。
version: 1.4.2

metadata:
  openclaw:
    emoji: 🦞
    os: [linux, mac, windows]
    primaryEnv: DEEPSEEK_API_KEY
    requires:
      env:
        - DEEPSEEK_API_KEY
        - DISCORD_WEBHOOK_URL
      optionalEnv:
        - TAVILY_API_KEY
        - TWITTERAPI_IO_KEY
        - YOUTUBE_API_KEY
      anyBins:
        - uv
    # Python dependencies are declared inline in news_aggregator.py (PEP 723).
    # `uv run news_aggregator.py` installs them automatically — no install spec needed.
---
# 🦞 人工智能新闻聚合器

该工具可收集任何主题的新闻，通过 DeepSeek AI 生成英文摘要，并将其发布到 Discord 上。

**默认主题（人工智能相关）：** TechCrunch · The Verge · NYT Tech（RSS）+ 精选的 AI 相关 YouTube 频道  
**自定义主题：** Tavily 新闻搜索 + YouTube 主题搜索（不包含短视频，按观看次数排序）

---

## 网络端点

| 端点 | 功能 | 条件 |
|---------|--------|---------|
| `https://api.deepseek.com/chat/completions` | 人工智能新闻摘要生成 | 必需 |
| `https://discord.com/api/webhooks/...` | 将摘要发布到 Discord | 必需 |
| `https://techcrunch.com/.../feed/` | RSS 新闻（人工智能主题） | 仅限默认主题 |
| `https://www.theverge.com/rss/...` | RSS 新闻（人工智能主题） | 仅限默认主题 |
| `https://www.nytimes.com/svc/collections/...` | RSS 新闻（人工智能主题） | 仅限默认主题 |
| `https://api.tavily.com/search` | 自定义主题新闻搜索 | 仅当设置了 `TAVILY_API_KEY` 时 |
| `https://api.twitterapi.io/twitter/tweet/advanced_search` | Twitter 搜索 | 仅当设置了 `TWITTERAPI_IO_KEY` 时 |
| `https://www.googleapis.com/youtube/v3/...` | YouTube 搜索 | 仅当设置了 `YOUTUBE_API_KEY` 时 |

该脚本 **不** 会访问 OpenAI 的端点。`openai` 包仅用作指向 `https://api.deepseek.com` 的 HTTP 客户端。在脚本启动时，`OPENAI_API_KEY` 会被从环境变量中移除。

---

## 使用示例

- “获取今天的 AI 新闻”
- “收集关于加密货币的新闻”
- “上周关于气候变化的新闻”
- “今天 AI 领域的热门新闻是什么？”
- “获取过去 3 天的加密货币新闻”
- “显示最近的比特币相关 YouTube 视频”
- “AI 新闻预览”（不发布到 Discord）
- “测试我的 Discord Webhook”

---

## 所需的 API 密钥

| 密钥 | 是否必需 | 获取途径 |
|--------|---------|-------------------|
| `DEEPSEEK_API_KEY` | 是 | [platform.deepseek.com/api_keys](https://platform.deepseek.com/api_keys) |
| `DISCORD_WEBHOOK_URL` | 是 | Discord → 频道设置 → 集成 → Webhook → 复制 URL |
| `TAVILY_API_KEY` | （自定义主题所需） | [app.tavily.com](https://app.tavily.com) |
| `TWITTERAPI_IO_KEY` | 可选 | [twitterapi.io](https://twitterapi.io) |
| `YOUTUBE_API_KEY` | 可选 | [console.cloud.google.com](https://console.cloud.google.com) → YouTube 数据 API v3 |

---

## 实现步骤

**重要提示：** 必须按照以下步骤运行 `news_aggregator.py` 脚本。请勿手动搜索信息或自行编写响应代码——脚本会负责所有的数据获取、摘要生成以及 Discord 发布工作。

### 第 1 步：找到脚本

脚本包含在该技能包中。请找到它：

```bash
SKILL_DIR=$(ls -d ~/.openclaw/skills/ai-news-aggregator-sl 2>/dev/null || ls -d ~/.openclaw/skills/news-aggregator 2>/dev/null)
SCRIPT="$SKILL_DIR/news_aggregator.py"
echo "Script: $SCRIPT"
ls "$SCRIPT"
```

### 第 2 步：检查 `uv` 是否可用

```bash
which uv && uv --version || echo "uv not found"
```

如果未找到 `uv`，请用户通过系统包管理器或 [https://docs.astral.sh/uv/getting-started/installation/](https://docs.astral.sh/uv/getting-started/installation/) 安装它。切勿代表用户执行 `curl-pipe-sh` 命令。

### 第 3 步：API 密钥

环境变量 `DEEPSEEK_API_KEY` 和 `DISCORD_WEBHOOK_URL` 由 OpenClaw 从配置文件中自动传递。无需使用 `.env` 文件。

验证这些密钥是否已设置（请勿显示具体值）：

```bash
[[ -n "$DEEPSEEK_API_KEY" ]] && echo "DEEPSEEK_API_KEY: set" || echo "DEEPSEEK_API_KEY: MISSING"
[[ -n "$DISCORD_WEBHOOK_URL" ]] && echo "DISCORD_WEBHOOK_URL: set" || echo "DISCORD_WEBHOOK_URL: MISSING"
```

如果缺少任意一个密钥，请用户运行以下命令进行安装：

```
openclaw config set env.DEEPSEEK_API_KEY '<key>'
openclaw config set env.DISCORD_WEBHOOK_URL '<url>'
```

### 第 4 步：解析用户输入

从用户输入的内容中提取 `topic`（主题）和 `days`（搜索天数）：

| 用户输入 | --topic | --days |
|---------|---------|--------|
| “AI 新闻” / “科技新闻” / 无具体主题 | （省略 — 使用默认人工智能主题） | 1 |
| “加密货币新闻” | `--topic "crypto"` | 1 |
| “关于气候变化的新闻” | `--topic "climate change"` | 1 |
| “上周的加密货币新闻” | `--topic "crypto"` | 7 |
| “过去 3 天的比特币新闻” | `--topic "Bitcoin"` | 3 |
| “昨天的 AI 新闻” | （省略主题） | 1 |
| “本周的 AI 相关新闻” | （省略主题） | 7 |

对于报告类型，请选择相应的参数：

| 用户输入 | 需要添加的参数 |
|---------|-------------------|
| “新闻” / “文章” / “摘要” | `--report news` |
| “热门新闻” / “Twitter” / “YouTube” | `--report trending` |
| “预览” / “不发布” | `--dry-run` |
| “测试 Discord” | `--test-discord` |
| 其他选项 | （省略 — 运行所有功能） | |

### 第 5 步：使用 `uv` 运行脚本

`uv run` 会自动从脚本的元数据中安装所有依赖项，无需手动设置虚拟环境（`venv`）。

```bash
uv run "$SCRIPT" [--topic "TOPIC"] [--days N] [--report TYPE] [--dry-run]
```

### 示例

```bash
# AI news today (default)
uv run "$SCRIPT"

# Crypto news, last 7 days
uv run "$SCRIPT" --topic "crypto" --days 7

# Trending AI on Twitter and YouTube
uv run "$SCRIPT" --report trending

# Preview without posting to Discord
uv run "$SCRIPT" --topic "Bitcoin" --dry-run

# Test webhook connection
uv run "$SCRIPT" --test-discord
```

### 第 6 步：反馈结果

向用户告知已发布到 Discord 的内容、每个来源的新闻数量，以及未使用的来源（例如：“由于未设置 `YOUTUBE_API_KEY`，因此跳过了 YouTube 来源”）。