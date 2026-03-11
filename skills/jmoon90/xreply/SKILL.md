---
name: xreply
description: 使用人工智能以你的声音生成、安排并发布推文。浏览热门内容，管理个人偏好设置，并追踪账单信息。
slug: xreply
version: 0.1.0
license: MIT-0
homepage: https://xreplyai.com
metadata: {"openclaw":{"emoji":"✨","requires":{"anyBins":["mcporter","npx"],"env":["XREPLY_TOKEN"]},"primaryEnv":"XREPLY_TOKEN","install":[{"id":"mcporter","kind":"node","package":"mcporter","bins":["mcporter"],"label":"Install mcporter (node)"}]}}
---
# XReply — 人工智能推文生成工具

使用人工智能生成、安排并发布推文，模拟用户的语气。您可以浏览热门内容以获取灵感，管理待发布的推文队列，并跟踪费用和使用情况。

## 认证

所有工具都需要一个 `XREPLY_TOKEN` 环境变量——该变量是从 XreplyAI 设置中获取的 JWT 令牌。当您在 OpenClaw 配置中设置该令牌后，OpenClaw 会自动将其注入系统。

## MCP 服务器

XReply MCP 服务器在 npm 上的发布地址为 `@xreplyai/mcp`。您可以通过 `mcporter` 命令来调用这些工具：

```
mcporter call 'npx @xreplyai/mcp' <tool_name> [param:value ...]
```

要查看所有可用的工具及其参数，请执行以下命令：

```
mcporter list 'npx @xreplyai/mcp' --all-parameters
```

## 工具

### 内容发现

#### xreply_viral_library

浏览点赞数超过 100 的热门推文以获取灵感。支持按主题、关键词和时间范围进行筛选。需要 Pro 订阅或 BYOK 订阅计划。

```
mcporter call 'npx @xreplyai/mcp' xreply_viral_library
mcporter call 'npx @xreplyai/mcp' xreply_viral_library niche:ai sort:top_engaged
mcporter call 'npx @xreplyai/mcp' xreply_viral_library niche:saas query:pricing time_range:7d
mcporter call 'npx @xreplyai/mcp' xreply_viral_library niche:startups sort:recent page:2
```

参数：
- `niche`（可选）：`ai` | `saas` | `marketing` | `productivity` | `startups` | `growth`
- `sort`（可选）：`top_engaged`（默认）| `recent`
- `query`（可选）：在推文文本中搜索关键词
- `time_range`（可选）：`7d` | `30d`
- `page`（可选）：页码，每页显示 20 条推文（默认：1）

---

### 内容生成

#### xreply_posts_generate

以用户的语气生成一条推文，并将其保存为草稿。返回生成的推文内容及保存后的推文 ID。此操作会消耗每日配额（免费用户每天 5 条，Pro 用户每天 100 条）。

```
mcporter call 'npx @xreplyai/mcp' xreply_posts_generate
mcporter call 'npx @xreplyai/mcp' xreply_posts_generate topic:"my SaaS hit 1000 users"
mcporter call 'npx @xreplyai/mcp' xreply_posts_generate topic:"lessons from year 1" angle:story_arc
mcporter call 'npx @xreplyai/mcp' xreply_posts_generate angle:one_liner
```

参数：
- `topic`（可选）：推文的主题或提示（最多 280 个字符）
- `angle`（可选）：`one_liner` | `list` | `question` | `story_arc` | `paragraph` | `my_voice`

#### xreply_posts_generate_batch

一次性生成多条推文。每条推文都会消耗每日配额——如果担心配额问题，请先检查费用情况。免费账户最多只能生成 9 条推文。

```
mcporter call 'npx @xreplyai/mcp' xreply_posts_generate_batch category:personalized count:5
mcporter call 'npx @xreplyai/mcp' xreply_posts_generate_batch category:trending count:3
mcporter call 'npx @xreplyai/mcp' xreply_posts_generate_batch category:viral count:9
```

参数：
- `category`（必选）：`personalized` | `trending` | `viral`
- `count`（必选）：要生成的推文数量（1–9 条，不能超过剩余的每日配额）

---

### 推文管理

#### xreply_posts_list

列出队列中的所有推文——包括草稿、已安排的推文和最近发布的推文。返回推文 ID、内容、状态和预定发布时间。

```
mcporter call 'npx @xreplyai/mcp' xreply_posts_list
```

无需参数。

#### xreply_posts_create

保存推文草稿。推文只有在调用 `xreply_posts_publish` 后才会实际发布。

```
mcporter call 'npx @xreplyai/mcp' xreply_posts_create body:"Your tweet text here"
mcporter call 'npx @xreplyai/mcp' xreply_posts_create body:"Tweet text" auto_rt_hours:24
```

参数：
- `body`（必选）：推文内容（最多 280 个字符）
- `auto_rt_hours`（可选）：发布后自动转发的时间（例如：`24` 小时）

#### xreply_posts_edit

编辑推文的内容、预定发布时间或自动转发设置。无法编辑正在处理或已发布的推文。

```
mcporter call 'npx @xreplyai/mcp' xreply_posts_edit id:123 body:"Updated tweet text"
mcporter call 'npx @xreplyai/mcp' xreply_posts_edit id:123 'scheduled_at:2026-03-15T09:00:00Z'
mcporter call 'npx @xreplyai/mcp' xreply_posts_edit id:123 body:"New text" auto_rt_hours:48
```

参数：
- `id`（必选）：推文 ID（整数）
- `body`（可选）：新的推文内容（最多 280 个字符）
- `scheduled_at`（可选）：ISO 8601 格式的日期时间字符串——省略则保持不变；如需取消调度，请省略此字段，推文将恢复为草稿状态
- `auto_rt_hours`（可选）：发布后自动转发的时间（省略则保持不变）

#### xreply_posts_delete

删除推文。无法删除正在处理或已发布的推文。

```
mcporter call 'npx @xreplyai/mcp' xreply_posts_delete id:123
```

参数：
- `id`（必选）：推文 ID（整数）

---

### 发布

#### xreply_posts_publish

将推文发布到 X 或 Twitter。需要连接 X 账户。发布时间取决于您的订阅计划。

```
mcporter call 'npx @xreplyai/mcp' xreply_posts_publish id:123
mcporter call 'npx @xreplyai/mcp' xreply_posts_publish id:123 'scheduled_at:2026-03-15T09:00:00Z'
```

参数：
- `id`（必选）：推文 ID（整数）
- `scheduled_at`（可选）：预定的发布时间（ISO 8601 格式的日期时间）；省略则立即发布

---

### 信息查询

#### xreplybilling_status

查询订阅级别（免费/BYOK/Pro）、配额使用情况、每日限制和订阅详情。

```
mcporter call 'npx @xreplyai/mcp' xreply_billing_status
```

无需参数。

#### xreply_voice_status

查询语音配置的状态——包括语音是否已分析完成、推文数量、配置的 AI 提供者以及写作风格摘要。

```
mcporter call 'npx @xreplyai/mcp' xreply_voice_status
```

无需参数。

#### xreply_preferences_get

获取当前的推文生成偏好设置——如语气、表情符号使用情况和默认结构。

```
mcporter call 'npx @xreplyai/mcp' xreply_preferences_get
```

无需参数。

#### xreply_preferences_set

更新推文生成偏好设置。仅输入您想要更改的参数。

```
mcporter call 'npx @xreplyai/mcp' xreply_preferences_set tone:witty
mcporter call 'npx @xreplyai/mcp' xreply_preferences_set tone:professional include_emoji:false
mcporter call 'npx @xreplyai/mcp' xreply_preferences_set structure:story_arc
```

参数：
- `tone`（可选）：`auto` | `casual` | `professional` | `witty` | `empathetic`
- `include_emoji`（可选）：`true` | `false`
- `structure`（可选）：`one_liner` | `paragraph` | `question` | `list` | `story_arc`

#### xreply_rules_list

列出生成推文时应用的自定义规则（例如：“禁止使用标签”）。需要 Pro 订阅或 BYOK 订阅计划。

```
mcporter call 'npx @xreplyai/mcp' xreply_rules_list
```

无需参数。

---

## 工作流程示例

### 生成并安排一条推文

```
1. mcporter call 'npx @xreplyai/mcp' xreply_posts_generate topic:"ship fast, learn faster" angle:story_arc
   → returns { body: "...", post: { id: 42, ... } }
2. mcporter call 'npx @xreplyai/mcp' xreply_posts_publish id:42 'scheduled_at:2026-03-12T09:00:00Z'
```

### 浏览热门内容以获取灵感，然后生成推文

```
1. mcporter call 'npx @xreplyai/mcp' xreply_viral_library niche:saas sort:top_engaged
   → review viral tweet formats
2. mcporter call 'npx @xreplyai/mcp' xreply_posts_generate topic:"inspired by those formats" angle:list
```

### 规划一周的推文内容

```
1. mcporter call 'npx @xreplyai/mcp' xreply_billing_status
   → check remaining quota before a large batch
2. mcporter call 'npx @xreplyai/mcp' xreply_posts_generate_batch category:personalized count:7
   → generates 7 drafts
3. mcporter call 'npx @xreplyai/mcp' xreply_posts_list
   → review the queue
4. mcporter call 'npx @xreplyai/mcp' xreply_posts_edit id:101 'scheduled_at:2026-03-11T09:00:00Z'
   mcporter call 'npx @xreplyai/mcp' xreply_posts_edit id:102 'scheduled_at:2026-03-12T09:00:00Z'
   → schedule each post
```

### 编辑并发布现有的草稿

```
1. mcporter call 'npx @xreplyai/mcp' xreply_posts_list
   → find the draft ID
2. mcporter call 'npx @xreplyai/mcp' xreply_posts_edit id:55 body:"Revised tweet text"
3. mcporter call 'npx @xreplyai/mcp' xreply_posts_publish id:55
```

---

## 错误处理

**令牌过期：** 如果工具返回 401 错误，说明 `XREPLY_TOKEN` 已过期（令牌有效期为 30 天）。请让用户从 XreplyAI 设置中获取新的令牌，并更新 OpenClaw 配置。

**配额不足：** 如果生成推文时出现配额错误（例如：“每日生成配额已用完”），请调用 `xreplybilling_status` 检查配额情况并通知用户。配额会在午夜重置。

**批量生成超出配额：** 如果 `xreply_posts_generate_batch` 返回 `quota_insufficient: true`，请将 `count` 减少到响应中显示的可用数量，或让用户确认是否继续生成。

**安排时间超出范围：** 如果安排推文时出现错误，说明请求的时间超出了订阅计划的限制。请调用 `xreplybilling_status` 检查 `max_schedule_days` 并建议调整时间。

**无法编辑/删除已发布的推文：** 状态为 `processing` 或 `posted` 的推文无法被编辑或删除。请调用 `xreply_posts_list` 查看当前状态。

**热门内容功能需 Pro 订阅：** 如果 `xreply_viral_library` 或 `xreply_rules_list` 返回 403 错误，说明这些功能需要 Pro 订阅或 BYOK 订阅计划。