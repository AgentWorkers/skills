---
name: sec-daily-digest
version: "0.2.0"
description: "Use when asked to generate a cybersecurity daily digest from CyberSecurityRSS OPML feeds and Twitter/X KOL accounts, with provider selection, recent-window filtering, archive dedup, vulnerability merging, source health monitoring, and markdown output."
env:
  # AI providers (one required for non-dry-run)
  OPENAI_API_KEY: OpenAI provider key
  GEMINI_API_KEY: Google Gemini provider key
  ANTHROPIC_API_KEY: Anthropic Claude provider key
  OLLAMA_BASE_URL: Ollama base URL (optional, defaults to http://localhost:11434)
  # Twitter/X sources (optional; at least one enables KOL section)
  TWITTERAPI_IO_KEY: twitterapi.io API key (preferred)
  X_BEARER_TOKEN: Official Twitter API v2 bearer token
  TWITTER_API_BACKEND: "twitterapiio|official|auto" (default: auto)
  # State directory
  SEC_DAILY_DIGEST_HOME: Custom state root (default: ~/.sec-daily-digest)
---

# 每日网络安全摘要

本工具会从CyberSecurityRSS的OPML源以及Twitter/X安全领域的KOL账号中生成每日网络安全摘要，供研究人员使用。
触发命令：`/sec-digest`。

## 使用场景

- 用户需要每日或最新的网络安全摘要。
- 用户希望同时获取来自RSS源和Twitter/X安全KOL的资讯。
- 用户希望合并漏洞事件（优先显示CVE漏洞，同时进行非CVE漏洞的分类整理）。
- 用户可以指定使用特定的AI服务提供商（`openai`、`gemini`、`claude`、`ollama`），或选择仅进行规则-based的测试（`--dry-run`）。

## 不适用场景

- 用户需要一次性生成特定文章的摘要（请使用直接摘要功能）。
- 用户期望能够随意切换输出语言。

## 快速入门

```bash
# Basic (RSS only, no AI scoring)
bun scripts/sec-digest.ts --dry-run --output ./output/digest.md

# With AI scoring + Twitter KOLs
TWITTERAPI_IO_KEY=your-key bun scripts/sec-digest.ts \
  --provider claude --opml tiny --hours 48 --output ./output/digest.md

# Weekly mode (168h window)
bun scripts/sec-digest.ts --mode weekly --provider openai --output ./output/weekly.md

# With email delivery (requires gog)
bun scripts/sec-digest.ts --provider claude --email me@example.com --output ./output/digest.md

# With full text enrichment
bun scripts/sec-digest.ts --provider claude --enrich --output ./output/digest.md
```

## CLI参数说明

| 参数 | 说明 | 默认值 |
|------|-------------|---------|
| `--provider <id>` | AI服务提供商：`openai`、`gemini`、`claude`、`ollama` | `openai` |
| `--opml <profile>` | OPML数据源配置：`tiny`或`full` | `tiny` |
| `--hours <n>` | 数据收集时间窗口（以小时为单位） | `48` |
| `--mode <daily`/`weekly>` | 运行模式：daily表示48小时周期，weekly表示168小时周期 | `daily` |
| `--top-n <n>` | 最多显示的文章数量 | `20` |
| `--output <path>` | 输出Markdown文件的路径 | `./output/sec-digest-YYYYMMDD.md` |
| `--dry-run` | 仅进行规则判断（不使用AI服务） | `false` |
| `--no-twitter` | 禁用Twitter/X安全KOL信息的获取 | `false` |
| `--email <addr>` | 通过`gog`将摘要发送到指定邮箱 | `` |
| `--enrich` | 获取文章的完整文本 | `false` |
| `--help` | 显示帮助信息 | `` |

## 相关文件及路径

- 入口脚本：`scripts/sec-digest.ts`
- 处理流程脚本：`src/pipeline/run.ts`
- 配置文件根目录：`~/.sec-daily-digest/`
- 配置文件：`~/.sec-daily-digest/config.yaml`
- 数据源配置文件：`~/.sec-daily-digest/sources.yaml`
- 系统健康检查文件：`~/.sec-daily-digest/health.json`
- 档案存储目录：`~/.sec-daily-digest/archive/`
- OPML缓存文件（简化版）：`~/.sec-daily-digest/opml/tiny.opml`
- OPML缓存文件（完整版）：`~/.sec-daily-digest/opml/CyberSecurityRSS.opml`

## 必须遵循的规则

1. 在解析数据源之前，必须先检查OPML数据的远程更新状态。
2. 如果远程检查失败且本地没有缓存数据，则仅使用本地缓存；如果两者都失败，则直接报错（提示“没有可用的缓存数据且远程更新检查失败”）。
3. AI服务提供商默认为`openai`；可以通过`--provider`参数进行更改。
4. 综合评估时，安全信息和AI分析的权重各占50%。
5. 输出内容必须包含“AI发展”、“安全动态”和“漏洞专报”三个部分。
6. 虽然配置文件中设置了`output_language`参数，但目前实现固定为双语格式的Markdown输出；运行时不会自动切换语言。
7. 只有在成功获取Twitter/KOL的推文时，才会显示“🔐 安全KOL更新”部分。
8. 如果未提供Twitter访问凭据，系统会自动跳过Twitter数据的获取（不会导致程序崩溃）。

## Twitter/X安全KOL配置

Twitter安全KOL的账号信息存储在`~/.sec-daily-digest/sources.yaml`文件中（首次运行时会自动添加15个默认账号）。

### 默认KOL列表

Taviso、GossiTheDog、SwiftOnSecurity、MalwareTechBlog、briankrebs、JohnLaTwC等。

### sources.yaml文件格式

```yaml
sources:
  - id: taviso
    type: twitter
    name: "Tavis Ormandy / Google Project Zero"
    handle: taviso
    enabled: true
    priority: true
    topics:
      - security

  # Disable a default source:
  - id: thegrugq
    enabled: false

  # Add a new custom source:
  - id: myresearcher
    type: twitter
    name: "My Researcher"
    handle: myresearcher
    enabled: true
    priority: false
    topics:
      - security
```

## 后端服务选择

| 环境变量 | 使用的后端服务 |
|-------------|-------------|
| `TWITTERAPI_IO_KEY` | twitterapi.io（推荐，支持5个并发请求） |
| `X_BEARER_TOKEN` | 官方Twitter API v2（支持5个并发请求） |
| 两者都使用 | twitterapi.io |
| 两者都不使用 | 禁用Twitter服务（不显示相关内容） |
| `TWITTER_API_BACKEND=official` | 强制使用官方API |

## 档案管理

过去7天内出现过的文章会被标记为低优先级（分数减5分），但不会被删除。档案文件保存在`~/.sec-daily-digest/archive/YYYY-MM-DD.json`中，并在90天后自动清理。

## 源站健康检查

每次运行都会记录每个数据源的获取情况。如果某个数据源的失败率超过50%（且检查次数大于2次），该数据源会被标记为“⚠️ 数据源健康警告”。健康检查数据保存在`~/.sec-daily-digest/health.json`中。

## 电子邮件发送（使用gog）

`--email`参数可以通过`gogcli`（https://github.com/steipete/gogcli）发送摘要内容。

```bash
# Install (macOS)
brew install steipete/tap/gogcli
gog auth login   # one-time OAuth setup

# Send digest
bun scripts/sec-digest.ts --provider claude \
  --email me@example.com --output /tmp/digest.md
```

## 日志输出

```
[sec-digest] email=sent to me@example.com
# or
[sec-digest] email=failed: gog not found in PATH. Install: ...
```

## 完整文本获取

`--enrich`参数会在AI分析前获取文章的完整文本，从而提高分类和摘要的质量。该选项会跳过需要付费访问的网站（如Twitter、Reddit、GitHub、YouTube、NYT、Bloomberg、WSJ、FT）。

## 定时任务集成

```bash
# Daily at 07:00
0 7 * * * cd /path/to/sec-daily-digest && \
  bun scripts/sec-digest.ts --mode daily --output ~/digests/sec-$(date +\%Y\%m\%d).md \
  2>&1 | tee -a ~/.sec-daily-digest/cron.log

# Weekly on Monday at 08:00
0 8 * * 1 cd /path/to/sec-daily-digest && \
  bun scripts/sec-digest.ts --mode weekly --output ~/digests/weekly-$(date +\%Y\%m\%d).md \
  2>&1 | tee -a ~/.sec-daily-digest/cron.log
```

## 常见错误

1. 未设置选定AI服务提供商的API密钥（`OPENAI_API_KEY`、`GEMINI_API_KEY`、`ANTHROPIC_API_KEY`均为必填项）。
2. 误解了备用方案的作用：OPML数据的备用机制依赖于缓存，并非无条件使用。
3. 在没有提供AI服务提供商的凭据时，忘记使用`--dry-run`参数。
4. 未设置`TWITTERAPI_IO_KEY`或`X_BEARER_TOKEN`，却期望系统能获取Twitter/KOL的信息。

## 成功标志

- 日志中会显示`[sec-digest] provider=...`、`[sec-digest] cache_fallback=true|false`、`[sec-digest] output=...`、`[sec-digest] stats feeds=... articles=... recent=... selected=... vuln_events=... twitter_kols=...`等信息。
- 输出的Markdown文件包含“AI发展”、“安全动态”和“漏洞专报”三个部分，并附有漏洞参考信息。
- 每次运行后，`~/.sec-daily-digest/archive/YYYY-MM-DD.json`文件会被更新。
- `~/.sec-daily-digest/health.json`文件也会随之更新。

## 更多信息

有关完整安装和详细使用说明，请参阅`README.md`和`README.zh-CN.md`。