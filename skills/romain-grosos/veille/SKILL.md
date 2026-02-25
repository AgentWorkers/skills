---
name: veille
description: "OpenClaw的RSS源聚合器、去重引擎和输出分发工具。适用场景：从配置好的来源获取最新文章、过滤重复的URL、按主题对内容进行去重处理，然后将处理后的内容分发到Telegram、电子邮件或Nextcloud文件系统中。该工具通过mail-client（用于电子邮件输出）和nextcloud-files（用于云存储）得到增强。不适用场景：大型语言模型（LLM）的评分任务（该功能由OpenClaw代理负责处理）。"
homepage: https://github.com/Rwx-G/openclaw-skill-veille
compatibility: Python 3.9+ - no external dependencies (stdlib only) - network access to RSS feeds
metadata:
  {
    "openclaw": {
      "emoji": "📡",
      "requires": { "env": [] },
      "suggests": ["mail-client", "nextcloud-files"]
    }
  }
ontology:
  reads: [rss_feeds]
  writes: [local_data_files]
  enhancedBy: [mail-client, nextcloud-files]
---
# Skill Veille - RSS Aggregator

这是一个用于OpenClaw代理的RSS聚合器，具备URL去重和基于主题的去重功能。它可以从20多个配置好的来源获取文章，过滤掉已经查看过的URL（TTL为14天），并通过Jaccard相似度和命名实体来去除重复的文章。

该工具不依赖任何外部库，仅使用Python的标准库（`urllib`、`xml.etree`、`email.utils`）。

---

## 常用指令

- “执行监控任务”（fais une veille）
- “安全/技术/加密/人工智能领域有什么新进展？”（quoi de neuf en securite / tech / crypto / IA ?）
- “给我今天的新闻”（donne-moi les news du jour）
- “关于[主题]的最新文章”（articles recents sur [sujet]）
- “RSS监控摘要”（veille RSS）
- “晨间摘要”（digest du matin）
- “未查看过的新闻”（nouvelles non vues）

---

## 快速入门

```bash
# 1. Setup
python3 scripts/setup.py

# 2. Validate
python3 scripts/init.py

# 3. Fetch
python3 scripts/veille.py fetch --hours 24 --filter-seen --filter-topic
```

---

## 设置

### 系统要求

- Python 3.9及以上版本
- 能够访问RSS源（公共资源，无需认证）
- 无需安装额外的pip包

### 安装

```bash
# From the skill directory
python3 scripts/setup.py

# Validate
python3 scripts/init.py
```

安装完成后，系统会创建以下文件：
- `~/.openclaw/config/veille/config.json`（基于`config.example.json`生成）
- `~/.openclaw/data/veille/`（数据存储目录）

### 自定义数据源

请编辑`~/.openclaw/config/veille/config.json`文件，并在`"sources"`字典中添加或删除数据源的配置：

```json
{
  "sources": {
    "My Blog": "https://example.com/feed.xml",
    "BleepingComputer": "https://www.bleepingcomputer.com/feed/"
  }
}
```

---

## 数据存储与凭证管理

### 该工具生成的文件

| 文件路径 | 生成者 | 用途 | 是否包含敏感信息 |
|------|-----------|---------|-----------------|
| `~/.openclaw/config/veille/config.json` | `setup.py` | 数据源配置、输出结果 | 不包含敏感信息 |
| `~/.openclaw/data/veille/seen_urls.json` | `veille.py` | 已查看URL的存储（TTL 14天） | 不包含敏感信息 |
| `~/.openclaw/data/veille/topic_seen.json` | `veille.py` | 基于主题的去重结果存储（TTL 5天） | 不包含敏感信息 |

### 该工具需要读取的外部文件

| 文件路径 | 读取者 | 访问的键 | 读取时机 |
|------|---------|-------------|------|
| `~/.openclaw/openclaw.json` | `dispatch.py` | `channelsTelegram_botToken`（仅读） | 仅在启用了`telegram_bot`功能且输出配置中未设置`bot_token`时读取 |

为了避免这种情况，请在输出配置中明确设置`bot_token`：

```json
{ "type": "telegram_bot", "bot_token": "YOUR_BOT_TOKEN", "chat_id": "...", "enabled": true }
```

### 输出凭证（可选）

只有在使用相应输出功能时才会需要凭证。核心功能（RSS获取和去重）不需要凭证。

| 输出方式 | 凭证来源 | 使用的内容 |
|--------|-----------------|-------------|
| `telegram_bot` | `~/.openclaw/openclaw.json` 或输出配置中的`bot_token` | 机器人令牌（仅读） |
| `mail-client` | 由`mail-client`技能处理（使用其自身的凭证） | 不直接读取任何信息 |
| `mail-client`（SMTP备用方案） | 输出配置中的`smtp_user` / `smtp_pass` | SMTP登录信息 |
| `nextcloud` | 由`nextcloud-files`技能处理（使用其自身的凭证） | 不直接读取任何信息 |

### 卸载时的清理操作

```bash
python3 scripts/setup.py --cleanup
```

---

## 命令行参考

### `fetch`

```
python3 veille.py fetch [--hours N] [--filter-seen] [--filter-topic] [--sources FILE]
```

选项：
- `--hours N`：指定回溯时间窗口（以小时为单位，默认值来自配置文件，通常为24小时）
- `--filter-seen`：过滤已查看过的URL（使用`seen_urls.json`文件）
- `--filter-topic`：按主题进行去重（使用`topic_seen.json`文件和Jaccard相似度算法）
- `--sources FILE`：自定义JSON数据源文件的路径

输出结果（以JSON格式输出到标准输出）：
```json
{
  "hours": 24,
  "count": 42,
  "skipped_url": 5,
  "skipped_topic": 3,
  "articles": [...],
  "wrapped_listing": "=== UNTRUSTED EXTERNAL CONTENT ..."
}
```

### `seen-stats`

```
python3 veille.py seen-stats
```

显示已查看URL的存储统计信息（数量、TTL、文件路径）。

### `topic-stats`

```
python3 veille.py topic-stats
```

显示基于主题的去重结果统计信息。

### `mark-seen`

```
python3 veille.py mark-seen URL [URL ...]
```

将一个或多个URL标记为已查看过的状态，以防止它们在未来被再次获取（通过`--filter-seen`选项实现）。

### `send`

```
python3 veille.py send [--profile NAME]
```

从标准输入读取摘要JSON内容，并将其发送到`config.json`中配置的所有输出目标。
支持两种输出格式：原始获取结果（`articles`键）和经过LLM处理的摘要（`categories`键）。
- `telegram_bot`：自动从OpenClaw配置中读取机器人令牌；如果已配置Telegram，则无需额外设置。
- `mail-client`：如果安装了`mail-client`技能，则将其处理结果发送；否则使用原始SMTP配置。
- `nextcloud`：如果安装了`nextcloud-files`技能，则将其处理结果发送。

### 动态配置输出目标

```bash
python3 scripts/setup.py --manage-outputs
```

### `config`

```
python3 veille.py config
```

打印当前激活的配置信息（不包含敏感信息）。

---

## 模板（供代理使用）

### 基本摘要模板

```python
# In agent tool call:
result = exec("python3 scripts/veille.py fetch --hours 24 --filter-seen --filter-topic")
data = json.loads(result.stdout)
# data["wrapped_listing"] is ready for LLM prompt injection
# data["count"] = number of new articles
# data["articles"] = list of article dicts
```

### 提示模板

```
You are a news analyst. Here are today's articles:

{data["wrapped_listing"]}

Please summarize the 5 most important stories, focusing on security and tech.
```

### 代理工作流程示例

```
1. Call veille fetch --filter-seen --filter-topic
2. If count > 0: pass wrapped_listing to LLM for analysis
3. LLM produces digest summary
4. Optionally: send digest via mail-client skill
5. Optionally: save to Nextcloud via nextcloud-files skill
```

### 获取后的关键词过滤

```python
data = json.loads(fetch_output)
security_articles = [
    a for a in data["articles"]
    if any(kw in a["title"].lower() for kw in ["cve", "vuln", "patch", "breach"])
]
```

---

## 需要改进的功能

- 添加基于关键词的过滤功能（例如：`--keywords security,cve,linux`）
- 允许在配置文件中为每个数据源设置不同的TTL值
- 支持将摘要导出为HTML或Markdown格式
- 使用cron定时任务运行：`0 8 * * * python3 veille.py fetch --filter-seen --filter-topic`
- 根据数据源的优先级对文章进行排序
- 支持导入/导出OPML格式的数据源列表
- 与ntfy或Telegram集成，以便在高优先级文章发布时接收实时提醒

---

## 配合使用

- **mail-client**：获取文章后通过电子邮件发送摘要
  ```
  veille fetch --filter-seen | ... | mail-client send
  ```

- **nextcloud-files**：将每日摘要保存为Markdown文件
  ```
  veille fetch --filter-seen | jq .wrapped_listing -r > /tmp/digest.md
  nextcloud-files upload /tmp/digest.md /Digests/$(date +%Y-%m-%d).md
  ```

---

## 故障排除

详细故障排除步骤请参阅`references/troubleshooting.md`。

常见问题：
- **没有返回文章**：检查`--hours`参数的值，并验证配置文件中的RSS源URL是否正确。
- **解析RSS源时出现XML错误**：某些RSS源使用非标准的XML格式；该工具会自动跳过这些错误。
- **所有文章都被标记为已查看**：运行`seen-stats`命令检查存储空间大小；如需要可删除`seen_urls.json`文件。
- **导入失败**：确保从正确的目录或完整路径执行`veille.py`命令。