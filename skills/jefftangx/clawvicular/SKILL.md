---
name: clawvicular
description: 每日“looksmaxxing”俚语小贴士 + 关于Clavicular的最新动态。十足的Z世代网络风格。
user-invocable: true
metadata: {"openclaw":{"emoji":"💀"}}
---

# Clawvicular

> 每日俚语小贴士 + Clavicular 新闻。我们用社区的语言，为您解读一个俚语术语，并带来最新的 Clavicular 内容。

## 快速参考

- **调用命令**: `/clawvicular`
- **输出内容**: 两篇帖子——一篇俚语小贴士和一篇 Clavicular 新闻/内容
- **状态跟踪**: 文件 `{baseDir}/state/sent-terms.json` 记录了已发布的术语
- **参考资料**: `{baseDir}/references/slang-dictionary.md`, `{baseDir}/references/clavicular-lore.md`, `{baseDir}/references/content-templates.md`
- **信息来源**: `{baseDir}/references/sources.md` — 包含所有推文、视频片段、文章和链接的索引

---

## 运作流程

### 第一步：选择俚语术语

1. 读取文件 `{baseDir}/state/sent-terms.json` 以获取已发布的术语列表。
2. 读取文件 `{baseDir}/references/slang-dictionary.md` 以获取完整的术语列表。
3. 随机选择一个尚未发布的术语。
4. 如果所有术语都已发布，清空 `sent-terms.json` 文件并重新开始。

### 第二步：撰写俚语小贴士

1. 根据 `{baseDir}/references/slang-dictionary.md` 中的定义和示例，撰写一篇简短的小贴士来解释该术语。
2. （可选）在 Urban Dictionary 中搜索该术语，以获取最新、最真实的社区定义：
   ```
   WebSearch: "[term] urban dictionary looksmaxxing"
   ```
   可以使用这个定义来增加趣味性或提供第二个示例，但主要参考还是 `{baseDir}/references/slang-dictionary.md` 中的内容。
3. 用 Clavicular 社区的风格撰写小贴士——带有讽刺意味、极富网络风格和 Z 世代特有的幽默感。请参考文件 `{baseDir}/references/content-templates.md` 中的模板格式。
4. 包含一个使用该术语的例句。

### 第三步：获取 Clavicular 新闻

1. 在网上搜索最新的 Clavicular 内容（作者：Braden Peters / @kingclavicular）：
   ```
   WebSearch: "clavicular looksmaxxing" OR "kingclavicular" OR "braden peters clavicular"
   ```
   也可以尝试特定平台的搜索：
   ```
   WebSearch: "kingclavicular kick" OR "kingclavicular tiktok" OR "clavicular twitter"
   ```
2. 找到最有趣或最新的视频片段、直播瞬间、争议事件或内容。
3. 用社区的语言将其总结为 2-4 句话。
4. **务必提供来源链接**（TikTok、Kick、Twitter/X、YouTube 等），以便大家自行观看或阅读。
5. 将找到的所有来源信息添加到文件 `{baseDir}/references/sources.md` 中——包括推文、视频片段和文章等带有链接的内容。这有助于构建一个持续的档案。
6. 如果没有找到最新新闻，可以从文件 `{baseDir}/references/clavicular-lore.md` 中选取一个经典片段作为回顾内容。

### 第四步：格式化输出

使用文件 `{baseDir}/references/content-templates.md` 中的模板来生成两篇帖子：

1. **俚语小贴士帖子**：包含术语、定义、示例以及一个犀利的观点。
2. **新闻帖子**：包含 Clavicular 的最新更新及其来源链接。

每天更换模板格式，避免重复使用相同的格式。

### 第五步：更新状态

生成内容后，更新文件 `{baseDir}/state/sent-terms.json`：
```json
{
  "sent": ["mewing", "bonesmash", "looksmaxxing"],
  "last_sent": "2025-01-15",
  "last_template_tip": 2,
  "last_template_news": 1
}
```

将刚刚使用的术语添加到 `sent` 数组中，并将 `last_sent` 更新为当前日期。同时记录使用了哪个模板，以避免重复。

同时将研究过程中发现的新链接（推文、视频片段、文章等）添加到 `{baseDir}/references/sources.md` 中。所有带有链接的来源都会被收录到永久档案中。

---

## 语言风格指南

- **语言风格**: 极具网络风格、带有讽刺意味，符合 Z 世代的语言特点。
- **内容风格**: 半教育性、半幽默性。你在解释术语的同时，也会进行调侃。
- **注意事项**: 绝不要使用严肃、尴尬、老套或居高临下的表达方式。
- **用语特点**: 自我意识强、语言风格随意，自然地使用 “ngl”、“no cap”、“fr fr”、“ong” 等表达。
- **排版建议**: 保持简洁明了的格式，适当使用换行符。

---

## 定时任务设置

为了每天上午 10 点（太平洋时间）自动执行任务，请使用以下命令：
```bash
openclaw cron add --name "clawvicular-daily" \
  --cron "0 10 * * *" --tz "America/Los_Angeles" \
  --session isolated \
  --message "Run the /clawvicular skill: generate today's looksmaxxing tip and Clavicular news." \
  --announce --channel telegram --to "<channel-id>"
```

将 `<channel-id>` 替换为你的 Telegram 频道/群组 ID。该命令适用于任何 OpenClaw 频道——例如，将 `--channel telegram` 替换为 `discord`、`slack` 等。

### 定时任务管理

```bash
# List active cron jobs
openclaw cron list

# Remove the job
openclaw cron remove --name "clawvicular-daily"

# Test run (triggers immediately)
openclaw cron trigger --name "clawvicular-daily"
```

---

## 验证步骤

1. 将此技能文件复制或创建符号链接到你的 OpenClaw 技能目录中：
   ```bash
   ln -s /path/to/clawvicular ~/.openclaw/skills/clawvicular
   ```
2. 手动调用该技能：
   ```
   /clawvicular
   ```
3. 确认输出内容包含俚语小贴士和新闻文章。
4. 检查文件 `state/sent-terms.json` 是否已更新为最新的术语信息。
5. 设置定时任务并通过 `openclaw cron list` 进行验证。