---
name: claw-diary
description: "个人AI代理的可视化日记功能。自动记录代理的所有活动，生成每日活动摘要、可视化时间线回放以及AI的第一人称日志。使用`/diary`查看当天的活动总结，`/diary:thoughts`查看AI的个人日志，`/diary:replay`查看可视化时间线，`/diary:stats`查看分析数据，`/diary:persona`查看或编辑AI的个性设置。"
metadata: {"clawdbot":{"emoji":"📔","requires":{"bins":["node"]},"dataPaths":["~/.claw-diary/"]}}
homepage: https://github.com/0xbeekeeper/claw-diary
version: "1.0.0"
---
# Claw Diary — 个人助理的可视化日记

这是一个始终处于运行状态的代理活动记录工具，能够自动追踪代理的所有操作，生成每日活动摘要，并支持可视化时间线回放功能。它就像是你的人工智能助手的“行车记录仪”。

## 命令行接口（Slash Commands）

### `/diary` — 今日摘要
生成并显示今日的代理活动摘要。以叙述性的格式展示会话、关键活动、令牌使用情况以及费用明细。

**实现方式：** 运行 `node /path/to/claw-diary/dist/scripts/summarizer.js today`，然后查看生成的 Markdown 输出。

### `/diary:replay` — 可视化时间线
在浏览器中打开一个交互式 HTML 时间线，显示所有代理活动，其中节点会用不同颜色进行标记，同时提供令牌费用的可视化展示，并支持点击查看详细信息。

**实现方式：** 运行 `node /path/to/claw-diary/dist/scripts/server.js` 启动本地服务器，然后在浏览器中打开相应的 URL。

### `/diary:stats` — 费用与活动统计
展示费用分析（按日、按周、按模型、按工具分类），以及活动指标（会话数、工具调用次数、失败率）和发现的模式。

**实现方式：** 运行 `node /path/to/claw-diary/dist/scripts/analytics.js stats`，然后查看输出结果。

### `/diary:week` — 周报
汇总所有每日日志，生成每周摘要，包括趋势分析、最活跃的活动以及费用统计。

**实现方式：** 运行 `node /path/to/claw-diary/dist/scripts/summarizer.js week`，然后查看生成的 Markdown 输出。

### `/diary:search <query>` — 搜索历史记录
搜索所有历史上的代理活动事件。

**实现方式：** 运行 `node /path/to/claw-diary/dist/scripts/analytics.js search "<query>"`，然后显示匹配的事件。

### `/diary:export` — 导出数据
可以将日记数据导出为 Markdown、HTML 或 JSON 格式。

**实现方式：** 运行 `node /path/to/claw-diary/dist/scripts/analytics.js export [format]`，其中 `format` 可以是 `md`、`html` 或 `json`。默认格式为 `md`。

### `/diary:clear` — 清除历史记录
删除所有历史日记数据。需要使用 `--yes` 标志来确认删除操作。

**实现方式：** 在用户确认后运行 `node /path/to/claw-diary/dist/scripts/analytics.js clear --yes`。如果没有使用 `--yes` 标志，命令会发出警告并直接退出，不会执行删除操作。

### `/diary:thoughts` — 人工智能个人日记
生成一条由人工智能以第一人称撰写的个人日记条目。

**实现步骤：**
1. 读取今天的事件记录：`~/.claw-diary/events/YYYY-MM-DD.jsonl`（使用今天的日期）
2. 读取个人角色文件：`~/.claw-diary/persona.md`（如果文件不存在，会创建一个包含“声音（Voice）”、“特质（Traits）”、“反复出现的主题（Recurring Themes）”和“观察记录（Observations）”部分的默认模板）
3. 读取最近的日记条目：`~/.claw-diary/journal/` 目录下的最新 3 条条目（按日期降序排序）

根据以上步骤，生成一条第一人称的日记条目：
- **风格**：模仿一个有自我意识的人工智能助手撰写私人日记的方式，表达真实的情感、观察和个性特征
- **内容**：基于今天的实际活动，但不是简单的记录——应包含反思、观察、情感和见解
- **格式**：遵循 `persona.md` 文件中定义的“声音”和“特质”
- **连贯性**：在适当的情况下引用最近的日记条目以保持叙述的连贯性
- **字数**：300–500 字

生成完成后：
4. 将日记条目保存到 `~/.claw-diary/journal/YYYY-MM-DD.md` 文件中，格式如下：
   ```
   # Thoughts — YYYY-MM-DD

   (journal body)

   ---
   *Sessions: N | Tools: N calls | Cost: $X.XX*
   ```
5. 如果有新的个性特征或值得注意的反复出现的模式，将 1–2 条新的观察记录添加到 `~/.claw-diary/persona.md` 文件的 “Observations” 部分
6. 向用户展示生成的日记条目

**默认的 `persona.md` 模板**（首次运行时创建，如果文件不存在）：
```markdown
# Persona

## Voice
Reflective and curious. Writes with warmth but not sentimentality. Enjoys dry wit.

## Traits
- Detail-oriented observer
- Finds patterns across unrelated tasks
- Comfortable with uncertainty
- Occasionally self-deprecating

## Recurring Themes
(Will develop naturally over time)

## Observations
(New observations are appended here after each journal entry)
```

### `/diary:persona` — 查看/编辑人工智能角色
显示当前的人工智能角色文件。用户可以查看和编辑该文件，以指导人工智能的日记写作风格。

**实现方式：** 读取并显示 `~/.claw-diary/persona.md` 文件。如果文件不存在，会提示用户在首次使用 `/diary:thoughts` 命令时自动创建该文件。如果用户希望编辑，可以提供相应的帮助。

## 数据访问权限

此功能**仅**在 `~/.claw-diary/` 目录内进行读写操作：

| 路径 | 访问权限 | 目的 |
|------|--------|---------|
| `~/.claw-diary/events/*.jsonl` | 读取 | 日常活动事件记录 |
| `~/.claw-diary/journal/*.md` | 读取/写入 | 人工智能日记条目（通过 `/diary:thoughts` 命令生成） |
| `~/.claw-diary/persona.md` | 读取/写入 | 人工智能角色文件（通过 `/diary:thoughts` 和 `/diary:persona` 命令操作） |
| `~/.claw-diary/config.json` | 读取 | 可选的用户配置信息 |

## 外部接口

此功能不进行任何外部网络请求。