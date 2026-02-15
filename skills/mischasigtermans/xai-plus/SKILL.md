---
name: xai-plus
description: |
  Search X/Twitter and the web, chat with Grok models (text + vision), and analyze X content using xAI's API.
  Use when: searching X posts/threads, web research via Grok, chatting with Grok, analyzing voice patterns,
  researching trends, or checking post quality. Triggers: grok, xai, search x, search twitter, x search,
  ask grok, grok chat, analyze voice, x trends.
metadata:
  openclaw:
    emoji: "🔎"
    requires:
      bins: ["node"]
      env: ["XAI_API_KEY"]
    primaryEnv: "XAI_API_KEY"
---

# xAI 技能

使用 xAI 的 API 在 X（Twitter）上搜索、浏览网页、与 Grok 模型进行聊天（包括图像分析），并分析 X 平台上的内容模式。

## 功能

- **X 搜索**：可按日期或用户名筛选帖子、话题和账号进行搜索。
- **网页搜索**：通过 Grok 的网页搜索工具在互联网上搜索。
- **聊天**：与 Grok 模型进行文本聊天或图像分析。
- **内容分析**：分析语音模式、研究趋势、检查帖子的质量。
- **模型管理**：查看可用的 xAI 模型列表。

## 设置

### API 密钥

从 [console.x.ai](https://console.x.ai) 获取您的 xAI API 密钥。

```bash
# Via clawdbot config (recommended)
clawdbot config set skills.entries.xai-plus.apiKey "xai-YOUR-KEY"

# Or environment variable
export XAI_API_KEY="xai-YOUR-KEY"
```

脚本会按以下顺序查找 API 密钥：
1. `XAI_API_KEY` 环境变量
2. `~/.clawdbot/clawdbot.json` 文件中的 `env.XAI_API_KEY`
3. `~/.clawdbot/clawdbot.json` 文件中的 `skills.entries.xai-plus.apiKey`
4. `~/.clawdbot/clawdbot.json` 文件中的 `skills.entries["grok-search"].apiKey`（备用选项）

### 默认模型（可选）

您可以覆盖默认模型（`grok-4-1-fast`）：

```bash
# Via config
clawdbot config set skills.entries.xai-plus.model "grok-3"

# Or environment variable
export XAI_MODEL="grok-3"
```

模型优先级：
1. 命令行参数 `--model`（最高优先级）
2. `XAI_MODEL` 环境变量
3. `~/.clawdbot/clawdbot.json` 文件中的 `env.XAI_MODEL`
4. `~/.clawdbot/clawdbot.json` 文件中的 `skills.entries.xai-plus.model`
5. 默认值：`grok-4-1-fast`

## 搜索

### X 搜索

您可以使用可选的筛选条件在 X 上搜索帖子和话题。

**基本搜索：**
```bash
node {baseDir}/scripts/grok_search.mjs "query" --x
```

**按日期筛选：**
```bash
# Last 7 days
node {baseDir}/scripts/grok_search.mjs "Claude AI" --x --days 7

# Specific date range
node {baseDir}/scripts/grok_search.mjs "AI agents" --x --from 2026-01-01 --to 2026-01-31
```

**按用户名筛选：**
```bash
# Only from specific accounts
node {baseDir}/scripts/grok_search.mjs "AI news" --x --handles @AnthropicAI,@OpenAI

# Exclude accounts
node {baseDir}/scripts/grok_search.mjs "GPT" --x --exclude @spam1,@spam2
```

**输出格式：**
```bash
# JSON (default, agent-friendly)
node {baseDir}/scripts/grok_search.mjs "query" --x

# Links only
node {baseDir}/scripts/grok_search.mjs "query" --x --links-only

# Human-readable text
node {baseDir}/scripts/grok_search.mjs "query" --x --text
```

**JSON 输出格式：**
```json
{
  "query": "search query",
  "mode": "x",
  "results": [
    {
      "title": "@handle",
      "url": "https://x.com/handle/status/123",
      "snippet": "Post text...",
      "author": "@handle",
      "posted_at": "2026-01-15T10:30:00Z"
    }
  ],
  "citations": ["https://x.com/..."]
}
```

### 网页搜索

通过 Grok 在互联网上搜索。

```bash
node {baseDir}/scripts/grok_search.mjs "TypeScript best practices 2026" --web
```

**JSON 输出格式：**
```json
{
  "query": "search query",
  "mode": "web",
  "results": [
    {
      "title": "Page title",
      "url": "https://example.com/page",
      "snippet": "Description...",
      "author": null,
      "posted_at": null
    }
  ],
  "citations": ["https://example.com/..."]
}
```

### 搜索选项

| 标志 | 描述 | 示例 |
|------|-------------|---------|
| `--x` | 在 X/Twitter 上搜索 | 必需用于 X 搜索 |
| `--web` | 在网页上搜索 | 必需用于网页搜索 |
| `--days N` | 过去 N 天内的内容 | `--days 7` |
| `--from YYYY-MM-DD` | 开始日期 | `--from 2026-01-01` |
| `--to YYYY-MM-DD` | 结束日期 | `--to 2026-01-31` |
| `--handles a,b` | 仅搜索这些账号的帖子 | `--handles @user1,@user2` |
| `--exclude a,b` | 排除这些账号的帖子 | `--exclude @spam` |
| `--max N` | 最多显示 N 条结果 | `--max 20` |
| `--model ID` | 指定使用哪个模型 | `--model grok-3` |
| `--json` | 以 JSON 格式输出 | - |
| `--links-only` | 仅显示链接 | - |
| `--text` | 以人类可读格式输出 | - |
| `--raw` | 包含调试信息 | - |

有关高级查询模式和优化技巧，请参阅 [references/search-patterns.md]。

## 聊天

### 文本聊天

您可以向 Grok 提出任何问题。

```bash
node {baseDir}/scripts/chat.mjs "What is quantum computing?"
```

**使用指定模型：**
```bash
node {baseDir}/scripts/chat.mjs --model grok-3 "Explain transformers in ML"
```

**JSON 输出：**
```bash
node {baseDir}/scripts/chat.mjs --json "What is TypeScript?"
```

**JSON 格式：**
```json
{
  "model": "grok-4-1-fast",
  "prompt": "What is TypeScript?",
  "text": "TypeScript is...",
  "citations": ["https://..."]
}
```

### 图像聊天

使用 Grok 分析图片。

```bash
node {baseDir}/scripts/chat.mjs --image ./screenshot.png "What's in this image?"
```

**支持格式**：JPG、PNG、WebP、GIF

### 聊天选项

| 标志 | 描述 | 示例 |
|------|-------------|---------|
| `--model ID` | 使用的模型 | `--model grok-2-vision-1212` |
| `--image PATH` | 附加图片（可重复添加） | `--image ./pic.jpg` |
| `--json` | 以 JSON 格式输出 | - |
| `--raw` | 包含调试信息 | - |

有关模型比较和功能的详细信息，请参阅 [references/models.md]。

## 内容分析

分析 X 平台上的内容，包括语音模式、趋势和帖子质量。

### 语音分析

分析账号的语音和写作风格。

```bash
node {baseDir}/scripts/analyze.mjs voice @username
```

**自定义日期范围：**
```bash
# Last 60 days
node {baseDir}/scripts/analyze.mjs voice @username --days 60
```

**JSON 输出格式：**
```json
{
  "handle": "@username",
  "analyzed_posts": 150,
  "voice": {
    "tone": "casual, technical",
    "personality": ["curious", "direct", "helpful"],
    "perspective": "practitioner sharing lessons",
    "energy_level": "medium"
  },
  "patterns": {
    "sentence_structure": ["short declarative", "occasional fragments"],
    "vocabulary": ["technical", "accessible"],
    "formatting_quirks": ["line breaks for emphasis", "minimal punctuation"],
    "recurring_phrases": ["here's the thing", "turns out"]
  },
  "topics": ["AI", "software engineering", "startups"],
  "best_posts": [
    {
      "url": "https://x.com/username/status/123",
      "text": "Post text...",
      "why": "Authentic voice, specific example"
    }
  ],
  "anti_patterns": ["never uses em-dashes", "avoids numbered lists"]
}
```

### 趋势研究

研究某个主题的讨论趋势。

```bash
node {baseDir}/scripts/analyze.mjs trends "AI agents"
```

**JSON 输出格式：**
```json
{
  "topic": "AI agents",
  "trends": [
    {
      "pattern": "Shift from chatbots to autonomous agents",
      "description": "Discussion focuses on...",
      "example_posts": ["https://x.com/..."]
    }
  ],
  "perspectives": [
    {
      "viewpoint": "Agents will replace most SaaS",
      "supporters": ["@user1", "@user2"]
    }
  ],
  "hashtags": ["#AIAgents", "#AutonomousAI"],
  "key_accounts": ["@researcher1", "@founder2"],
  "posting_angles": [
    {
      "angle": "Practical implementation challenges",
      "hook": "Everyone talks about AI agents. Nobody talks about...",
      "target_audience": "Engineers building with AI"
    }
  ]
}
```

### 帖子安全检查

检查草稿或已发布的帖子中是否存在人工智能生成的信号或平台标记。

**检查草稿：**
```bash
node {baseDir}/scripts/analyze.mjs post "Your draft post text here"
```

**检查已发布的帖子：**
```bash
node {baseDir}/scripts/analyze.mjs post --url "https://x.com/user/status/123"
```

**JSON 输出格式：**
```json
{
  "post_text": "Your post...",
  "ai_detection_score": 3,
  "ai_signals": [
    "Contains em-dash",
    "Ends with engagement bait question"
  ],
  "platform_flag_score": 2,
  "platform_risks": [
    "Generic question could trigger spam filter"
  ],
  "quality_score": 7,
  "suggestions": [
    "Replace em-dash with period or comma",
    "Remove 'What do you think?' closer",
    "Add specific personal detail"
  ]
}
```

**评分标准：**
- **人工智能检测**：0-10 分（10 分表示完全由人工智能生成）
- **平台风险**：0-10 分（10 分表示高垃圾信息风险）
- **质量**：0-10 分（10 分表示质量优秀）

### 分析选项

| 标志 | 描述 | 示例 |
|------|-------------|---------|
| `--days N` | 分析的日期范围 | `--days 60` |
| `--url URL` | 分析特定帖子 | `--url https://x.com/...` |
| `--model ID` | 指定使用哪个模型 | `--model grok-3` |
| `--json` | 以 JSON 格式输出 | - |
| `--raw` | 包含调试信息 | - |

有关详细的提示结构和评分标准，请参阅 [references/analysis-prompts.md]。

## 模型

查看可用的 xAI 模型列表。

```bash
node {baseDir}/scripts/models.mjs
```

**输出格式：**
```
grok-2-vision-1212
grok-3
grok-4-1-fast
grok-4-fast
```

**JSON 输出：**
```bash
node {baseDir}/scripts/models.mjs --json
```

模型对比：

| 模型 | 执行速度 | 分析质量 | 图像分析能力 | 适用场景 |
|-------|-------|---------|--------|----------|
| grok-4-1-fast | 快速 | 良好 | 无图像分析能力 | 基本搜索、聊天、内容分析 |
| grok-4-fast | 快速 | 良好 | 无图像分析能力 | 替代快速模型 |
| grok-3 | 较慢 | 最适合复杂分析和详细分析 | 有图像分析能力 |
| grok-2-vision-1212 | 中等速度 | 良好 | 有图像分析能力 | 图像分析 |

有关模型详细信息和使用场景，请参阅 [references/models.md]。

## 高级用法

### 引用去重

在 X 搜索中，工具会自动去除重复的 tweet URL，优先显示标准的 `/@handle/status/id` 格式。

### 自定义模型选择

您可以为任何操作指定不同的模型：

```bash
# Search with grok-3 for better quality
node {baseDir}/scripts/grok_search.mjs "complex query" --x --model grok-3

# Chat with vision model
node {baseDir}/scripts/chat.mjs --model grok-2-vision-1212 --image pic.jpg "Describe"

# Analysis with grok-3 for deeper insights
node {baseDir}/scripts/analyze.mjs voice @username --model grok-3
```

### 调试

在命令后添加 `--raw` 选项可查看完整的 API 响应：

```bash
node {baseDir}/scripts/grok_search.mjs "query" --x --raw
```

## 参考文档

- [API 参考](references/api-reference.md) - xAI API 的端点和参数
- [搜索模式](references/search-patterns.md) - 查询模式、筛选条件和优化技巧
- [模型](references/models.md) - 模型比较和功能
- [分析提示](references/analysis-prompts.md) - 结构化的提示和评分标准
- [X 算法](references/x-algorithm.md) - 排名算法、参与度权重、垃圾信息检测

## 示例

### 研究某个主题
```bash
# Find recent discussions
node {baseDir}/scripts/grok_search.mjs "Claude Sonnet 4.5" --x --days 3

# Get trend analysis
node {baseDir}/scripts/analyze.mjs trends "Claude Sonnet 4.5"
```

### 在发布前分析语音
```bash
# Study the target account
node {baseDir}/scripts/analyze.mjs voice @target_account --days 30

# Check your draft
node {baseDir}/scripts/analyze.mjs post "Your draft here"
```

### 多模态分析
```bash
# Search web for context
node {baseDir}/scripts/grok_search.mjs "TypeScript 5.7 features" --web

# Ask follow-up
node {baseDir}/scripts/chat.mjs "What are the key TypeScript 5.7 improvements?"

# Analyze screenshot
node {baseDir}/scripts/chat.mjs --image ./code.png "Review this code"
```

## 错误处理

**常见错误及解决方法：**

- **缺少 API 密钥**：
  → 设置 `XAI_API_KEY` 环境变量或将其添加到 `~/.clawdbot/clawdbot.json` 文件中。
- **无效的搜索模式**：
  → 在搜索命令中添加 `--web` 或 `--x` 标志。
- **图片格式错误**：
  → 仅支持 JPG、PNG、WebP 或 GIF 格式的图片。
- **API 错误**：
  → 确保 API 密钥有效且处于激活状态。

## 提示

- 默认模型 `grok-4-1-fast` 性能较快，适用于大多数任务。
- 对于需要复杂分析或对质量要求较高的场景，建议使用 `grok-3`。
- X 搜索受时间限制（由 xAI 的搜索工具决定）。
- 网页搜索的效果取决于查询的精确性。
- 语音分析需要足够的帖子历史数据（建议至少 30 条帖子）。
- 帖子安全检查仅供参考，最终决策需自行判断。
- JSON 格式适合机器人或脚本使用。
- 文本格式更便于在终端或人类阅读。

## 故障排除

- **X 搜索无结果**：
  - 尝试使用更宽泛的查询条件或更长的时间范围。
- 确认要搜索的账号是否存在且为公开账号。
- 减少过于严格的筛选条件。
- **语音分析不完整**：
  - 增加 `--days` 参数以获取更多帖子数据。
- 确认账号是否为公开账号且活跃。
- 检查用户名是否正确（包括前缀 @）。
- **API 速率限制**：
  - xAI 对每个 API 密钥有使用频率限制。
- 如果达到限制，请分散请求时间。
- 如需更高频率的访问权限，可以考虑升级 xAI 订阅计划。

## 内容创作流程

使用这些分析工具来提升您的 X 平台内容：

```bash
# Research before writing
node {baseDir}/scripts/analyze.mjs trends "your topic"
node {baseDir}/scripts/grok_search.mjs "your topic" --x --days 7

# Study voice patterns
node {baseDir}/scripts/analyze.mjs voice @target_account

# Check draft before posting
node {baseDir}/scripts/analyze.mjs post "$(cat draft.txt)"
```

您可以使用 JSON 输出结果：
- 研究当前的讨论热点和发布方向。
- 学习行业内的优秀内容创作方式。
- 在发布前检测是否存在人工智能生成的帖子或平台标记。