---
name: gcalcli
description: 通过 `gcalcli` 与 Google 日历进行交互
---

# 日历参考

本文档提供了使用 `gcalcli` 查看和管理日历事件的详细信息。

## 安装

`gcalcli` 是一个用于 Google 日历的 Python 命令行工具（CLI），它通过 `uvx` 实现一次性执行功能。

**重要提示：** 请始终使用支持附件功能的自定义版本：
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli
```

此自定义版本会在 TSV 和 JSON 格式中输出附件信息，这对于查看会议记录和其他事件附件至关重要。

## 认证

首次运行 `gcalcli` 时，它会：
1. 打开浏览器进行 Google OAuth 认证
2. 将凭证缓存以供后续使用
3. 请求日历读取权限

## 常用命令

### 查看即将发生的日程

**推荐格式：** JSON 格式（包含完整信息及附件）：
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com --details all --json
```

**备用格式：** TSV 格式（以制表符分隔，便于解析）：
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com --details all --tsv
```

**人类可读格式（可能会截断长描述）：**
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com --details all
```

**基本日程视图（仅显示基本信息）：**
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com
```

### 日期范围

**重要提示：** 默认情况下，`gcalcli agenda` 仅显示从当前时间开始的日历事件。**

例如，当您在下午 2 点运行 `gcalcli agenda "today"` 时，它将显示当天及以后的事件；今天早些时候的事件将不会显示。

**指定日期范围：**
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com "tomorrow" "2 weeks"
```

**仅显示今天（从当前时间开始）：**
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com "today"
```

**查看今天早些时候的事件（使用绝对日期）：**
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com "2025-10-07" "2025-10-07"
```

**查看下周的事件：**
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com "monday" "friday"
```

### 搜索日历

**按文本搜索事件：**
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli search --calendar smcdonal@redhat.com "MCP Server"
```

### 访问会议附件和 Gemini 笔记

**重要提示：** 自定义版本的 `gcalcli` 会在 JSON/TSV 输出中包含 `attachments` 数组。**

每个事件的 `attachments` 数组包含以下对象：
- `attachment_title`：附件的标题（例如：“Gemini 生成的笔记”、“录音”、“聊天记录”）
- `attachment_url`：附件在 Google Drive 或 Google Doc 中的直接链接

**常见的附件类型：**
- **“Gemini 生成的笔记”**：来自 Google Meet 的智能生成会议笔记
- **录音**：会议录音文件
- **聊天记录**：会议聊天记录
- **共享文档**：日程安排、计划文档、演示文稿

**按附件类型搜索事件：**
```bash
# Find all events with Gemini notes
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli search "MCP" --calendar smcdonal@redhat.com --details all --json | jq '.[] | select(.attachments[]? | .attachment_title | contains("Notes by Gemini")) | {title, attachments: [.attachments[] | select(.attachment_title | contains("Notes by Gemini"))]}'

# Get just the titles and Gemini note URLs
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli search "MCP" --calendar smcdonal@redhat.com --details all --json | jq -r '.[] | select(.attachments[]? | .attachment_title | contains("Notes by Gemini")) | "\(.title): \(.attachments[] | select(.attachment_title | contains("Notes by Gemini")) | .attachment_url)"'
```

**按附件类型过滤事件：**
```bash
# Events with recordings
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com --json | jq '.[] | select(.attachments[]? | .attachment_title | contains("Recording"))'

# Events with any attachments
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com --json | jq '.[] | select(.attachments | length > 0)'
```

**使用 gcmd 导出 Gemini 笔记：**

- 单个会议的附件导出：
```bash
# 1. Find meeting with Gemini notes
GEMINI_URL=$(uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli search "MCP proposals" --calendar smcdonal@redhat.com --json | jq -r '.[0].attachments[] | select(.attachment_title | contains("Notes by Gemini")) | .attachment_url' | head -1)

# 2. Export to markdown using gcmd
cd /var/home/shanemcd/github/shanemcd/gcmd
uv run gcmd export "$GEMINI_URL" -o ~/Downloads/
```

- 从搜索结果中批量导出所有 Gemini 笔记（并行处理）：
```bash
# Extract Gemini note URLs and export in parallel (8 concurrent processes)
cd /var/home/shanemcd/github/shanemcd/gcmd
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli search "MCP" --calendar smcdonal@redhat.com --details all --json "2 months ago" "today" | jq -r '.[] | select(.attachments[]? | .attachment_title | contains("Notes by Gemini")) | .attachments[] | select(.attachment_title | contains("Notes by Gemini")) | .attachment_url' | sort -u | xargs -P 8 -I {} sh -c 'uv run gcmd export "{}" -o ~/Downloads/meeting-notes/'
```

该流程具有以下优点：
- 高效地搜索符合查询条件的会议
- 仅筛选包含 Gemini 笔记的会议
- 并行导出所有笔记到指定目录
- 使用直接管道（无需中间文件）
- 通过 `sort -u` 命令去除重复的 URL

**常见工作流程：** 查看最近的会议笔记：
```bash
# Search for recent meetings on a topic
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli search "ANSTRAT-1567" --calendar smcdonal@redhat.com --json

# Filter to show only events with Gemini notes
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli search "ANSTRAT-1567" --calendar smcdonal@redhat.com --json | jq '.[] | select(.attachments[]? | .attachment_title | contains("Notes by Gemini")) | {title, date: .s, gemini_notes: [.attachments[] | select(.attachment_title | contains("Notes by Gemini")) | .attachment_url]}'

# Export the most recent Gemini notes for review
# (extract URL, then use gcmd export)
```

## 输出格式

### --json （JSON 格式） **推荐使用**
- 结构化的 JSON 输出，包含所有事件详细信息
- 包含每个附件的标题和文件链接
- 所有事件字段均被保留
- 可用 `jq` 或 Python 简单解析
- 无任何字段被截断
- 最适合查看会议笔记和附件

### --tsv （以制表符分隔的格式）
- 每行显示一个事件
- 制表符分隔的字段包括：
  - id
  - start_date, start_time
  - end_date, end_time
  - html_link
  - hangout_link
  - conference_details
  - title
  - location
  - description （完整内容，无截断）
  - calendar
  - email
  - attachments （以管道符号分隔：title|url|title|url...）
  - action

- 适合使用标准 Unix 工具（如 `grep`、`awk`、`cut`）进行解析
- 不包含 ANSI 颜色代码或格式化信息

### 默认格式
- 人类可读的彩色输出
- 显示时间、标题和基本信息
- 长描述可能会被截断，并用 “...” 表示

### --details all
- 显示完整描述
- 显示所有参与者及其响应状态
- 包含会议链接和位置信息
- 附件以人类可读格式显示

## 使用场景

### 1. 早晨回顾
查看当天的日程安排（仅显示从当前时间开始的事件）：
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com --json "today"
```

**注意：** 此格式仅显示从当前时间开始的事件。如需查看当天的全部事件，请使用指定日期：**
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com --json "2025-10-07" "2025-10-07"
```

### 2. 周期性规划
查看下周的日程安排，以便安排工作时间：
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com --json "monday" "friday"
```

### 3. 会议准备
查看即将召开的会议详情：
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com --details all --json "today" "tomorrow"
```

### 4. 查找会议链接和笔记
获取会议的链接和笔记：
```bash
# Using JSON (recommended for accessing attachments)
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com --details all --json | jq '.[] | select(.title | contains("Meeting Name"))'

# Using TSV
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com --details all --tsv | grep "Meeting Name"
```

### 5. 工作前的准备工作
在开始处理某个功能之前，检查是否有相关的同步会议：
```bash
uvx gcalcli search --calendar smcdonal@redhat.com "ANSTRAT-1673"
```

## 与工作跟踪工具的集成

**基于日历的规划**

在规划每日日程时：
1. 查看即将召开的关联会议
2. 注意是否有在重要截止日期之前的会议（例如，在发布前 2 天进行同步会议）
3. 规划工作内容以准备讨论
4. 找到适合专注工作的时间段（会议间隙）

### 示例

**ANSTRAT-1673 场景：**
- 10 月 8 日：与 Demetrius Lima 进行同步会议
- 10 月 10 日：预计发布 llama-stack
- 行动：查看日历以确认时间，并准备讨论要点

**会议前的准备工作：**
```bash
# See what's coming up this week with attachments
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com --json "monday" "friday"

# Check specific meeting details
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli search --calendar smcdonal@redhat.com --json "ANSTRAT"
```

## 提示

1. **始终使用支持附件功能的自定义版本**：请使用 `uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0"` 来启用附件支持
2. **始终使用 `--json` 标志**：默认使用 JSON 格式以获取结构化数据
3. **使用 `jq` 进行数据解析**：JSON 输出非常适合使用 `jq` 进行过滤和数据提取
4. **会议开始前查看日历**：这是标准工作流程的一部分
5. **安排工作时间**：寻找会议之间的空档
6. **准备同步会议**：在重要会议前 1-2 天查看日历
7. **访问会议笔记**：使用 `jq` 过滤 Gemini 笔记，然后使用 `gcmd` 导出
8. **导出前进行搜索**：使用 `gcalcli search` 查找相关会议，再过滤附件
9. **理解日期范围**：`"today"` 表示从当前时间开始，而非全天

## 限制

- 仅支持读取操作（无法通过 CLI 创建或修改事件）
- 需要 OAuth 认证
- 可能需要定期重新认证
- 如果使用多个日历，则需要分别使用 `--calendar` 标志

## 其他命令

- **列出所有日历**：
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli list
```

- **以日历格式查看（月视图）：**
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli calm
```

- **快速查看（接下来 5 个事件，格式为 JSON）：**
```bash
uvx --from "git+https://github.com/shanemcd/gcalcli@attachments-in-tsv-and-json" --with "google-api-core<2.28.0" gcalcli agenda --calendar smcdonal@redhat.com --json | jq '.[0:5]'
```

## 参考资料

- 官方 `gcalcli` 文档：https://github.com/insanum/gcalcli
- 支持附件功能的自定义版本：https://github.com/shanemcd/gcalcli/tree/attachments-in-tsv-and-json
- 使用 Google 日历 API v3
- 支持多种输出格式（JSON、TSV、文本）