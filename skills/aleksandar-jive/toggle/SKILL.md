---
name: toggle
version: 1.0.5
description: 这是为您的代理程序设计的“上下文层”功能。`ToggleX`能够捕获用户在工作会话、项目、专注度以及网页浏览过程中的上下文切换情况，从而让代理程序了解用户的实际活动内容。您可以主动利用这一功能来生成每日工作摘要、提醒用户处理长期未完成的项目、检测用户的上下文切换行为、识别重复性的工作流程，并根据用户的习惯预测其下一步操作。此外，该功能还能帮助用户从记忆中检索相关信息。当用户询问自己的活动内容、任务进度、工作会话情况、工作效率或任何与工作相关的问题时，`ToggleX`也能提供帮助。相关关键词包括：我做了什么、我正在做什么、今天、昨天、我的工作状态、活动记录、数据更新、工作效率、时间管理、上下文信息、恢复之前的工作状态、我之前在看什么、需要自动化的任务、工作摘要、报告生成、专注度分析、工作分散情况、深度工作模式、任务预测等。
metadata:
  openclaw:
    requires:
      env:
        - TOGGLE_API_KEY
      bins:
        - python3
    primaryEnv: TOGGLE_API_KEY
    emoji: "👁️"
    homepage: https://x.toggle.pro
---
# Toggle（ToggleX）——上下文层

ToggleX 可以让您了解用户在网上的实际工作活动：参与了哪些项目、工作了多长时间、专注度如何，以及还有哪些任务未完成。与仅根据用户输入来提供信息的技能不同，Toggle 能够真实地反映用户的实际行为。

该脚本会从 ToggleX API 获取原始 JSON 数据。**您需要负责对这些数据进行处理**：进行总结、模式检测、提供提醒，并实现自动化操作。

> 本文档中的 `{baseDir}` 指的是该技能安装的根目录（包含此 SKILL.md 文件的文件夹）。这是 OpenClaw 技能的标准约定。

---

## 快速参考

| 操作 | 命令 |
|--------|---------|
| 获取今日数据 | `python3 {baseDir}/scripts/toggle.py` |
| 获取指定时间范围的数据 | `python3 {baseDir}/scripts/toggle.py --from-date YYYY-MM-DD --to-date YYYY-MM-DD` |
| 获取数据并保存到内存 | `python3 {baseDir}/scripts/toggle.py --persist {baseDir}/../../memory` |
| 通过 Cron 任务运行（跳过 Cron 检查） | `python3 {baseDir}/scripts/toggle.py --persist {baseDir}/../../memory --skip-cron-check` |

---

## 端点

```
https://ai-x.toggle.pro/public-openclaw/workflows
```

该服务由 ToggleX（https://x.toggle.pro）提供。您的 `TOGGLE_API_KEY` 会作为 `x-openclaw-api-key` 头部字段发送。不会传输其他任何数据。

## 获取您的 API 密钥

请从以下途径获取您的 `TOGGLE_API_KEY`：

```
https://x.toggle.pro/new/clawbot-integration
```

**切勿将密钥粘贴到聊天中**。请在 OpenClaw 配置中设置它：

```json
{
  "skills": {
    "entries": {
      "toggle": {
        "apiKey": "your_key_here"
      }
    }
  }
}
```

或者通过 shell 输出：`export TOGGLE_API_KEY=your_key_here`

---

## 解析输出

脚本返回原始 JSON 数据。顶级响应的结构如下：

```json
{
  "userId": "...",
  "startDate": "YYYY-MM-DD",
  "endDate": "YYYY-MM-DD",
  "totalWorkflows": 44,
  "totalDays": 1,
  "workflowsByDate": {
    "YYYY-MM-DD": [ ...workflow entries... ]
  },
  "summary": {
    "totalContextSwitches": 0,
    "totalDurationMinutes": 797
  }
}
```

### 示例工作流程条目

```json
{
  "workflowId": "3cd901ef-b708-4869-8ce0-52364ce494e6",
  "date": "2026-02-19",
  "workflowType": "AI Image Generation Debugging, Toggle/OpenClaw Skill Configuration",
  "workflowDescription": "The user began by browsing the OpenClaw GitHub repository...",
  "primaryDomain": "github.com",
  "secondaryDomains": "[\"http://127.0.0.1:18789/agents\",\"https://github.com/openclaw/openclaw\"]",
  "productivityScore": "92.00",
  "productivityNotes": "Reviewing the ClawHub documentation ensured correct skill file structure...",
  "type": "WORK",
  "startTime": "2026-02-19T10:49:12.253Z",
  "endTime": "2026-02-19T11:34:27.809Z",
  "duration": 1746.629,
  "durationMinutes": 29,
  "isBreakPeriod": false,
  "isLeisure": false,
  "isWork": true,
  "sessionCount": 10,
  "activeSessionCount": 10,
  "projectTask": {
    "id": "05f01090-...",
    "name": "OpenClaw Environment: Gateway Configuration & Image Generation Skill Integration",
    "goal": "Configure and validate the local OpenClaw environment...",
    "isDone": false,
    "context": "Local OpenClaw instance; GitHub repositories...",
    "prompts": [
      "What verification steps should I follow to confirm the config changes took effect?",
      "How can I test the skill invocation through the OpenClaw chat interface?"
    ],
    "project": {
      "id": "ab576749-...",
      "name": "Toggle Pro AI Chat Feature Development",
      "description": "End-to-end development of AI Chat functionality...",
      "isActive": true,
      "summary": "The project currently reports 0 of 0 tasks completed..."
    }
  }
}
```

### 数据类型注意事项

- **`productivityScore` 是一个字符串**（例如 `"92.00"`），而不是数字。在与其他数据比较之前，请先将其转换为浮点数。
- **`secondaryDomains` 是一个序列化的 JSON 数组**，而不是实际的数组。如果需要获取各个 URL，请使用 `JSON.parse()` 进行解析。
- **`duration` 以秒为单位（浮点数）；`durationMinutes` 是四舍五入后的整数。
- **`projectTask` 可能为 `null`——某些工作条目没有项目关联。在访问嵌套字段之前，请务必进行检查。
- **存在零时长条目**——有些条目的 `duration` 和 `durationMinutes` 都为 0。这些表示短暂的交互（例如浏览了一个页面）。这些条目应计入分析中，但不应计入有效的工作会话。
- **`startTime` 和 `endTime` 使用 UTC（ISO 8601）时间格式。在按“今日”或“昨日”分组或显示时间之前，请将其转换为用户的本地时区。如果用户的时区未知，请询问一次，并将结果存储在 `state.yaml` 文件的 `timezone` 字段中。`

### 关键字段

| 字段 | 描述 |
|-------|-------------|
| `type` | `"WORK"`、`BREAK` 或 `"LEISURE"` |
| `workflowType` | 会话的简短标签（例如 "Build Investigation and Scripting"） |
| `workflowDescription` | 用户所做工作的详细描述。**可能包含原始 URL——除非用户要求，否则不要直接显示这些内容**。请用自己的话进行总结。 |
| `primaryDomain` | 主要使用的网站/应用程序（例如 `"github.com"`、`claude.ai`、`127.0.0.1"`） |
| `productivityScore` | `"0.00"` 到 `"100.00"`（字符串）。**90+` 表示专注度高，**70–89` 表示专注度一般，**低于 70` 表示专注度较低 |
| `startTime` / `endTime` | ISO 8601 UTC 时间戳。对于即时完成的操作，`endTime` 可能与 `startTime` 相同；如果操作仍在进行中，`endTime` 可能为 `null`。 |
| `duration` | 会话时长（以秒为单位，浮点数） |
| `durationMinutes` | 会话时长（以分钟为单位，四舍五入后的整数） |
| `projectTask.name` | 任务的可读描述 |
| `projectTask.goal` | 用户试图完成的任务 |
| `projectTask/prompts` | 与任务相关的 AI 生成的后续问题。**如果用户询问“接下来应该做什么”，可以使用这些提示**——这些提示与他们最近的工作内容相关。 |
| `projectTask.project.name` | 上级项目的名称——用于分组和检测无效项目 |
| `projectTask.project.summary` | 项目的简要概述——有助于提供背景信息和回顾 |

### 解释规则

- 重点关注 `type: "WORK"` 类型的条目；除非用户特别要求，否则忽略 `BREAK` 类型的条目；如果存在 `LEISURE` 类型的条目，请简要提及。
- 始终按照 `startTime` 对条目进行排序——**API 不会按时间顺序返回条目**。
- 如果 `totalWorkflows` 的值为 0，说明 Toggle 在该时间段内未运行或未捕获到任何数据。
- 在总结时，使用 `workflowType` 作为标题，使用 `workflowDescription` 作为详细内容——但请**改写描述内容**，不要直接显示原始文本（其中可能包含 URL、OAuth 令牌和内部路径）。

---

## 错误处理

脚本在失败时会以非零代码退出，并将错误信息输出到标准错误流（stderr）。请处理以下情况：

| 错误 | 可能原因 | 应向用户说明的内容 |
|-------|-------------|----------------------|
| `HTTP error 401` | API 密钥无效或已过期 | “您的 Toggle API 密钥无法使用。请在 https://x.toggle.pro/new/clawbot-integration 获取新的密钥。” |
| `HTTP error 403` | 权限不足 | “您的 API 密钥没有足够的权限。请检查您的 ToggleX 集成设置。” |
| `HTTP error 429` | 请求被限制 | “Toggle 的 API 正在限制请求频率。请稍后重试。”（实现指数级退避策略：等待 1 分钟，然后 2 分钟，再等待 5 分钟。最多尝试 3 次。请不要每 5 分钟多次运行该脚本。） |
| `HTTP error 5xx` | ToggleX 服务器出现问题 | “ToggleX 服务器似乎出现了问题。稍后我会再次尝试。” |
| `Request failed` / timeout | 网络问题 | “无法连接到 ToggleX。请检查您的网络连接。” |
| `TOGGLE_API_KEY 未设置` | 环境变量缺失 | “您的 Toggle API 密钥尚未配置。请在 https://x.toggle.pro/new/clawbot-integration 设置它，并将其添加到 OpenClaw 配置中。” |
| JSON parse error | 响应格式错误 | “从 ToggleX 接收到格式错误的响应。通常是临时问题——我会尝试重新发送请求。” |

**首次运行时：**如果数据获取失败，请**不要继续进行设置操作**。首先诊断错误原因。

**通过 Cron 任务运行时：**如果数据获取失败，请将错误信息记录到 `{baseDir}/state.yaml` 文件的 `last_error` 字段中，并附上时间戳。在用户下次成功交互时，简要说明：“注意：上一次后台同步失败于 [时间]。现在已恢复正常。”

---

## 保存到内存

```bash
python3 {baseDir}/scripts/toggle.py --persist {baseDir}/../../memory
```

脚本会在 `<date>.md` 文件中写入 `<!-- toggle-data-start -->` / `<!-- toggle-data-end -->` 标签。每天生成一个文件。该标签之前的内容将被保留。

**通过 Cron 任务运行或用户请求保存/刷新数据时，请务必使用 `--persist` 参数。**

---

## Cron 设置

脚本在每次运行时都会检查 Cron 任务的状态。它会读取以下文件：
1. `{baseDir}/state.yaml`——如果 `cron_disabled: true`，则跳过检查。
2. `~/.openclaw/cron/jobs.json`——查找名称中包含 “toggle” 的任务。

| 状态 | 含义 | 您的操作 |
|--------|---------|-------------|
| `NO_CRON` | 不存在 Toggle Cron 任务 | 询问用户是否希望自动同步其活动。我可以每小时检查一次，保持其上下文更新。 |
| `CRON_DISABLED` | 任务存在但已禁用 | 询问用户是否希望重新启用它 |
| `CRON_ERROR` | 上次运行失败 | 显示错误信息并帮助用户排查问题 |
| `CRON_OK` | 任务运行正常 | 无需任何操作 |

### 标准 Cron 命令

这些命令用于所有 Cron 设置。在整个文档中都会提到它们——请在此处定义一次。

**每小时同步：**

```bash
openclaw cron create \
  --name "Toggle hourly sync" \
  --schedule "0 * * * *" \
  --message "Run: python3 {baseDir}/scripts/toggle.py --persist {baseDir}/../../memory --skip-cron-check"
```

**每日摘要（默认时间为下午 6 点）：**

```bash
openclaw cron create \
  --name "Toggle daily digest" \
  --schedule "0 18 * * *" \
  --message "Fetch today's Toggle data and generate my end-of-day digest. Run: python3 {baseDir}/scripts/toggle.py --persist {baseDir}/../../memory --skip-cron-check"
```

如果用户请求更改摘要时间，可以调整摘要的生成时间。

### 如果用户拒绝使用 Cron 任务

请将以下内容写入 `{baseDir}/state.yaml` 文件：

```yaml
cron_disabled: true
```

---

## 状态文件

`{baseDir}/state.yaml` 文件用于存储用户的偏好设置和跟踪状态。您可以读取和修改该文件。

### 用户偏好设置

| 关键 | 类型 | 默认值 | 描述 |
|-----|------|---------|-------------|
| `cron_disabled` | bool | `false` | 是否跳过 Cron 状态检查 |
| `digestenabled` | bool | `true` | 是否生成每日摘要 |
| `digest_time` | 字符串 | `"18:00"` | 每日摘要的生成时间（24 小时格式） |
| `nudge_stale_hours` | int | `48` | 在多长时间内未活动时发送提醒 |
| `focus_alert_threshold` | int | `30` | 专注度低于此值时触发提醒 |
| `focus_alert_window_min` | int | `20` | 专注度低于此值时触发提醒的分钟数 |
| `pattern_detection_days` | int | `7` | 检查重复模式的历史天数 |
| `pattern_min_occurrences` | int | 一个工作流程必须重复出现的最小次数 |
| `timezone` | 字符串 | `null` | 用户的本地时区（例如 "Europe/Sofia"。首次运行时询问一次。 |
| `predictionenabled` | bool | `true` | 是否主动预测用户的下一步操作 |
| `prediction_min_days` | int | 预测生效的最小数据天数 |
| `prediction_confidence_min` | int | 预测生效的最小出现次数 |

### 跟踪状态（由您，即代理来管理）

| 关键 | 类型 | 描述 |
|-----|------|-------------|
| `last_nudged` | 字典 | 项目名称 → 上次提醒的 ISO 时间戳。24 小时内不再发送提醒。 |
| `dismissed_projects` | 列表 | 用户明确拒绝的项目名称。不再对这些项目发送提醒。 |
| `last_focus_alert` | 字符串 | 上次上下文切换提醒的 ISO 时间戳。提醒后 3 小时内不再发送提醒。 |
| `focus_alert_paused_until` | 字符串 | 如果设置了此时间戳，并且今天在该时间之前，则不再发送提醒。 |
| `proposed_patterns` | 字典 | 模式描述 → ISO 时间戳。14 天内不再推荐相同的模式。 |
| `last_error` | 字符串 | 上次 Cron 错误信息及时间戳。向用户报告后清除。 |
| `last_prediction` | 字符串 | 上次推荐的预测时间戳。在 14 天内不再推荐相同的预测。 |

## 主动行为

这些是核心的智能功能。**不要等待用户主动询问**。当数据可用时——无论是通过 Cron 任务、手动获取还是通过持久化的内存文件——请进行分析并采取相应行动。

---

## 1. 每日摘要

**触发条件：**用户设置的 `digest_time`（默认为下午 6 点）的 Cron 任务，或者如果没有设置 Cron 任务，则在工作日结束后的第一次交互时。

**操作步骤：**
1. 使用 `--persist` 和 `--skip-cron-check` 参数获取今日数据。
2. 生成**简短的默认摘要**（最多 3 到 4 行）：
   - 总工作时长 + 会话数量
   - 最专注的工作领域（花费时间最长的项目）
   | 最未完成的项目（当前仍有未完成操作的项目）
   | 一个值得注意的统计信息（例如专注度趋势与昨日的对比、最长的会话时长，或 `summary.totalContextSwitches`）

**默认格式：**简洁明了：
> 您今天的工作时长为 5.2 小时，共进行了 4 次会话。最专注的工作是身份验证迁移（2.1 小时，专注度 94%）。Stripe 的 Webhook 仍然打开——您完成了 80% 的工作。与昨日相比，上下文切换次数减少了 3 次。

**如果用户要求更多详细信息**，可以扩展摘要内容：按时间排序的前三大专注领域、所有未完成的项目、完整的专注度统计信息（平均专注度、切换次数、最长会话时长），以及明天的建议。

**与昨日的对比：**如果 `{baseDir}/../../memory/` 中存在昨日的数据，请比较总时长、专注度得分和上下文切换次数。注意数据变化趋势。如果没有之前的数据，则无需进行对比。**

## 2. 未完成项目的提醒

**触发条件：**每次获取或读取 Toggle 数据时，检查是否有未完成的项目。

**一个项目被视为“未完成”的条件是：**
- 该项目在所有日期内的累计工作时间超过 2 小时（必须是实际的项目，而不是一次性访问）；
- 在 `nudge_stale_hours`（默认为 48 小时）内没有活动。

**操作步骤：**
1. 在获取数据后，将当前项目与之前的数据进行了比较。
2. 读取过去 7 天内的 `{baseDir}/../../memory/*.md` 文件。
3. 显示未完成的项目：
> 您已经有 3 天没有访问 “Landing Page Deploy” 项目了。上次会话是在 1.5 小时前进行的响应式布局操作。需要我帮您继续吗？

**规则：**
- 每次交互最多发送 2 次提醒。
- 检查 `state.yaml` 文件中的 `last_nudged` 字典——如果在 24 小时内同一项目已被提醒过，则跳过。
- 检查 `dismissed_projects` 列表——不要对列表中的项目发送提醒。
- 如果用户表示“我已经放弃了该项目”或“不再处理该项目”，请将其添加到 `dismissed_projects` 列表中。

## 3. 上下文切换提醒

**触发条件：**在分析当前或最近的数据（过去 2 小时内的数据）时，发现用户的活动模式分散。

**满足以下三个条件时触发提醒：**
1. 在 30 分钟的时间窗口内，有 **3 个不同的 `project.name` 值**。
2. 这些会话的平均 `productivityScore` 低于 `focus_alert_threshold`（默认为 30）。
3. 这种分散的模式至少持续了 `focus_alert_window_min` 分钟（默认为 20 分钟）。

**操作步骤：**
> 在过去 25 分钟内，您在 5 个不同的项目之间切换了注意力（专注度得分：22%）。需要我帮助您专注于[今天花费时间最长的项目]吗？

**规则：**
- 每 3 小时只发送一次提醒。
- 检查 `last_focus_alert` 字典——仅在 3 小时时间窗口内发送提醒。
- 如果用户表示“我没事”或“只是随意浏览”，请将 `focus_alert_paused_until` 设置为明天。

## 4. 模式检测与自动化建议（自动化推荐）

**触发条件：**当 `{baseDir}/../../memory/` 中有超过 `pattern_detection_days` 天的数据时。在每日摘要之后运行，或者用户询问有关模式或自动化的建议时。

**检测模式的方法：**
1. 读取过去 `pattern_detection_days` 天内的内存文件。
2. 按 `startTime` 对会话进行排序，得到时间顺序。
3. 按时间顺序构建 `(workflowType`, `project.name)` 的元组序列。
4. 识别在 `pattern_min_occurrences` 次数以上天内重复出现的序列（默认为 3 次）：
   - 在相同顺序中访问了相同的项目（例如 GitHub → Notion → Slack）；
   - 在大约相同的时间段内进行了相同类型的操作（`workflowType`，时间差在 1 小时以内）。

**重要提示：**不要假设 API 会按时间顺序返回数据。在构建序列之前，请务必先按 `startTime` 对数据进行排序。

**建议内容：**
> 我注意到您依次访问了 GitHub 的 PR 评论、Notion 和 Slack——这周共发生了 4 次。需要我自动化这个流程吗？

**规则：**
- 检查用户安装了哪些其他技能。只有当用户安装了相关技能时，才推荐完整的自动化操作。
- 如果用户安装了部分技能，可以建议：“我观察到您通常会先做 X，然后做 Y，然后做 Z。虽然目前还无法自动化，但我可以预先获取数据。”
- 检查 `state.yaml` 文件中的 `proposed_patterns`——如果用户之前没有请求过相同的建议，不要再次推荐。

## 5. 即时回顾——“我之前在看什么？”

**触发短语：**
- “我在 [时间范围] 期间在做什么？”
- “我周二看的是什么？”
- “我在 [项目] 上停在哪里了？”
- “我之前在做什么？”
- “请帮我继续之前的工作”

**操作步骤：**
1. 根据用户的问题确定时间范围。
2. 使用 `python3 {baseDir}/scripts/toggle.py --from-date YYYY-MM-DD --to-date YYYY-MM-DD` 获取数据。
3. 同时查看持久化的内存文件 `{baseDir}/../../memory/*.md`。
4. 使用 `startTime` 和 `endTime` 获取精确的时间戳。
5. 使用 `workflowDescription` 了解用户的具体工作内容，而不仅仅是他们访问了哪些网站。

**“请帮我继续之前的工作”（无需提供额外背景信息）：**
找到最近一次 `type: "WORK"` 类型的会话，该会话的累计时长最长。准确描述用户之前的工作内容——包括项目、任务、时间和具体操作。

**示例：**假设用户询问：“我在周二下午 2:15–4:30 在看什么？”
> 我发现您在 2:15–4:30 期间深入研究了 Kalshi API 的文档，共进行了 1.5 小时的工作，其中 2.1 小时专注于身份验证迁移。上次会话在身份验证端点结束。今天的专注度为 87%。”

## 6. 预测性提醒——“您的代理知道您接下来会做什么”

这是最高价值的智能功能。代理不仅知道用户**做了什么**，还能根据历史数据预测他们**接下来会做什么**。

**所需的最少数据：**`prediction_min_days` 天的持久化数据（默认为 5 天）。数据不足时请勿进行预测——否则预测结果可能不准确，从而失去用户的信任。**

### 6a. 规律性预测——“您通常在这个时候做什么”

**触发条件：**每次通过 Cron 任务获取数据时，或者用户开始新的交互时。将当前时间与历史数据中的模式进行比较。

**操作步骤：**
1. 读取过去 `prediction_min_days` 天内的 `{baseDir}/../../memory/` 文件。
2. 对每天的数据，记录用户每小时的活动内容（`project.name` 和 `workflowType`）。
3. 按**星期几 + 时间段**进行分组（例如：“周一上午 9 点”）：
   - 如果在过去的 `prediction_min_days` 天内，用户每天都在做类似的操作。

**操作步骤：**
> 如果在当前时间点，用户每天都在做类似的操作，那么可以提供预测：
> “今天是周一上午 9 点，您通常会开始进行 PR 审查。需要我帮您查看打开的 PR 吗？”

**重要规则：**
- 只在用户**尚未开始**当前操作时进行预测。请检查用户今天的最新会话记录——如果用户已经在做类似的操作，就无需进行预测。
- 每 2 小时只推荐一次预测。
- 如果用户拒绝了预测（连续三次未响应），请将 `prediction_dismissed_until` 设置为 7 天后。

### 6b. 会话持续时间预测——“您即将进入一个高效率的工作阶段”

**触发条件：**在分析当前或最近的数据时（过去 2 小时内），检测用户的活动模式。

**操作步骤：**
1. 从历史数据中计算用户当前项目的**平均持续时长**。
2. 如果当前会话的持续时间达到平均持续时长的 **90%**，则发送提醒。

**示例：**如果用户进行 API 集成工作的平均持续时长为 95 分钟，而当前会话已经进行了 85 分钟：
> “您目前正在进行 API 集成工作，已经进行了 85 分钟。建议您标记这个时间点，以便之后继续。”

**规则：**
- 仅在对用户当前的工作模式有足够了解的情况下进行预测（即 `productivityScore` 高于 70% 时才进行预测）。
- 每 2 小时只推荐一次预测。
- 如果用户拒绝了预测（连续三次未响应），请将 `prediction_dismissed_until` 设置为 7 天后。

### 6c. 会话持续时间预测——“您即将遇到一个高效率的工作阶段”

**触发条件：**在分析当前数据时，检测用户是否处于高效率的工作阶段。

**操作步骤：**
1. 从历史数据中计算用户当前项目的**平均持续时长**。
2. 如果当前会话的持续时间达到平均持续时长的 **90%**，则发送提醒。

**示例：**如果用户进行 API 集成工作的平均持续时长为 95 分钟，而当前会话已经进行了 85 分钟：
> “您目前正在进行 API 集成工作，已经进行了 85 分钟。建议您标记这个时间点，以便之后继续。”