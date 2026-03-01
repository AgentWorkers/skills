# Teleskopiq 技能

这是一个 YouTube 内容创作平台，支持通过 GraphQL API 生成 AI 脚本、元数据以及缩略图。

## 设置

请设置环境变量：
```bash
export TELESKOPIQ_API_KEY="tsk_..."
export TELESKOPIQ_ENDPOINT="https://teleskopiq.com/api/graphql"  # optional, this is the default
```

## 脚本内容格式

脚本内容采用 **Markdown** 格式，并包含一些特殊的制作标签。在编写脚本时请务必使用这些标签。

### 结构

```markdown
## Section Title
### Sub-section

Your spoken narration goes here. Write as you'd actually say it aloud.
```

### 制作标签

这些标签在 Teleskopiq 编辑器中会以不同的颜色显示，并在导出为 PDF 时保留下来。请务必使用它们来标记非语音部分的指令：

| 标签 | 语法 | 用途 | 颜色 |
|---|---|---|---|
| B-Roll | `[B-ROLL: 视频片段描述]` | 用于插入视频片段 | 青色 |
| Visual Cue | `[VISUAL: 道具、动作或摄像机移动]` | 屏幕上的动作或道具 | 紫色 |
| Graphic | `[GRAPHIC: 文本叠加或底部三分之一显示]` | 文本叠加或标题卡 | 黄色 |
| Music | `[MUSIC: 音乐名称或氛围]` | 背景音乐提示 | 粉色 |
| SFX | `[SFX: 音效描述]` | 音效或环境音 | 红色 |

### 完整示例

```markdown
## Hook

What happens when you give an AI agent full control of your computer?

[B-ROLL: terminal window running automated scripts, fast-forward timelapse]

I tried it for 24 hours. Here's what I learned.

## The Setup

[GRAPHIC: "OpenClaw — AI Agent Framework"]

OpenClaw gives your AI access to your machine — calendar, email, terminal, browser.

[VISUAL: screen recording of OpenClaw dashboard]

Today I set it completely loose.

## What It Did Well

[MUSIC: upbeat lo-fi background]

- Scheduled my week automatically
- Organized 3 months of project files

[B-ROLL: clean desktop, organized folders]

## Where It Got Weird

[SFX: error chime]

It tried to commit code without asking.

[VISUAL: shocked face, zoom in]

## Call to Action

Would you let an AI run your computer for a day? Drop your answer in the comments.

[GRAPHIC: Subscribe button animation]
```

---

## CLI 脚本

该脚本位于 `scripts/teleskopiq.py` 文件中（相对于当前技能目录）。

```bash
SKILL_DIR="$HOME/.openclaw/workspace/skills/teleskopiq"
python3 "$SKILL_DIR/scripts/teleskopiq.py" <command> [options]
```

## 在编写脚本之前

在开始编写脚本之前，请先使用 `get-style` 命令获取频道风格配置，并将其包含在代理简报中。这样可以确保脚本的编写风格与频道的要求一致，包括词汇、节奏和结构。

```bash
python3 "$SKILL_DIR/scripts/teleskopiq.py" get-style
```

在使用 `ai-write` 命令或手动编写内容之前，请确保已将输出结果整合到脚本中。

---

### 命令

| 命令 | 描述 |
|---|---|
| `get-style` | 获取并显示频道的风格配置 |
| `list-scripts` | 列出所有脚本及其状态和计划安排 |
| `create-script --title "..." [--content "..."]` | 创建脚本，并打印脚本 ID |
| `generate-metadata --script-id ID` | 启动元数据生成任务，持续轮询直至完成，然后打印结果 |
| `generate Thumbnails --script-id ID` | 为所有脚本生成缩略图 |
| `auto-schedule --script-id ID` | 自动安排脚本到下一个可用的发布时间 |
| `schedule --script-id ID [--date YYYY-MM-DD] [--time HH:MM] [--status ReadyToShoot]` | 安排脚本发布时间（省略 `--date` 选项可自动安排） |
| `ai-write --title "..." [--prompt "..."]` | 使用 Teleskopiq 的 AI 生成脚本内容 |
| `full-flow --title "..." --content "..." --date YYYY-MM-DD]` | 同时生成脚本、元数据和缩略图，并自动安排发布 |
| `full-flow --title "..." --ai-write [--prompt "..."]` | 与 `ai-write` 类似，但由 AI 完成脚本编写 |

---

## AI 写作

### `ai-write` 命令

该命令会创建一个新的脚本，并通过 WebSocket 订阅方式让 Teleskopiq 的 AI 代为编写脚本内容：

```bash
python3 "$SKILL_DIR/scripts/teleskopiq.py" ai-write --title "My Video Title"
python3 "$SKILL_DIR/scripts/teleskopiq.py" ai-write --title "My Video Title" --prompt "Write a tutorial about..."
```

### `--ai-write` 选项

在 `full-flow` 命令中，可以使用 `--ai-write` 代替 `--content` 选项，让 AI 生成脚本内容，之后再处理元数据和缩略图生成及调度工作：

```bash
python3 "$SKILL_DIR/scripts/teleskopiq.py" full-flow --title "My Video Title" --ai-write
python3 "$SKILL_DIR/scripts/teleskopiq.py" full-flow --title "My Video Title" --ai-write --prompt "Focus on beginner tips"
```

### `--prompt` 选项

这是一个用于提供给 AI 编写器的自定义指令。如果省略该选项，系统会使用默认提示来要求用户提供正确的章节标题和制作标签。

---

## 直接使用 GraphQL

所有请求都需要发送到 `$TELESKOPIQ_ENDPOINT`，并在请求头中添加 `Authorization: Bearer $TELESKOPIQ_API_KEY`。

### 列出所有脚本
```graphql
{ scripts { id title status { name } scheduledFor } }
```

### 创建脚本
```graphql
mutation CreateScript($input: CreateScriptInput!) {
  createScript(input: $input) { id title status { name } }
}
# variables: { "input": { "title": "...", "content": "..." } }
```

### 读取脚本详细信息
```graphql
{ script(id: "...") {
    title status { name } scheduledFor
    metadata { titles description tags }
    thumbnailIdeas { text visual }
    thumbnails { url }
  }
}
```

### 异步生成元数据
```graphql
mutation { startMetadataJob(scriptId: "...", scriptContent: "...") { success } }
```
⚠️ **异步操作** — 每 5 秒轮询一次 `script(id)` 请求，直到元数据信息填充完成。
`generateScriptMetadata` 方法已被 **弃用** — 请始终使用 `startMetadataJob` 方法。

### 异步生成缩略图（每个脚本生成一个缩略图）
```graphql
mutation { startThumbnailJob(scriptId: "...", idea: "...", ideaIndex: 0) { success } }
```
每个脚本对应的缩略图生成任务仅执行一次。需要通过 `script(id)` 查询 `thumbnails` 数组来获取缩略图信息。

### 自动安排发布时间（服务器端操作，根据频道偏好设置）
```graphql
# Normal: finds next empty preferred slot
mutation { autoScheduleScript(scriptId: "...") { scriptId scheduledFor slotsChecked bumped } }

# Urgent: takes the very next preferred slot, bumps displaced scripts forward
mutation { autoScheduleScript(scriptId: "...", urgent: true) { scriptId scheduledFor slotsChecked bumped } }
```
- 默认设置（省略 `urgent` 或设置为 `false`）：寻找下一个尚未安排发布的优先日期。`bumped` 字段的值为 0。
- `urgent: true`：选择下一个可用的发布日期（即使该日期已有其他脚本安排）。如果该日期已有脚本安排，相关脚本会被推迟到下一个优先日期。`bumped` 字段会记录被推迟的脚本数量。
- 建议优先使用此方法，而非手动计算发布日期。

### 手动更新/安排脚本
```graphql
mutation { updateScript(input: { id: "...", scheduledFor: "2025-03-09T12:00:00-05:00", status: ReadyToShoot }) { success } }
```

**脚本状态枚举：** `Draft` | `InProgress` | `ReadyToShoot` | `Recorded` | `Editing` | `Ready` | `Published` | `OnIce`

---

## 异步任务轮询流程

1. 发起元数据生成或缩略图生成请求（`startMetadataJob` / `startThumbnailJob`）
2. 等待 5 秒
3. 查询 `script(id)` 以检查元数据或缩略图信息是否已生成
4. 重复此过程最多 6 次（总共等待 30 秒）
5. 如果仍未获取到结果，报告超时情况

---

## 提示

- 在编写脚本时请务必使用制作标签（如 `[B-ROLL: ...]`、`[GRAPHIC: ...` 等），这些标签会在编辑器中以可视化方式显示效果。
- 使用 `autoScheduleScript` 命令进行脚本安排，无需手动计算发布日期。
- 脚本内容采用纯 Markdown 格式；`##` 表示章节，`###` 表示子章节。
- `generateScriptMetadata` 方法已被 **弃用** — 请使用 `startMetadataJob` 方法代替。