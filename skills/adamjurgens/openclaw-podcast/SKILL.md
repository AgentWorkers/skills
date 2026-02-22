---
name: openclaw-podcast
description: 将您的 OpenClaw 工作空间转变为个性化的 AI 驱动的播客简报系统。每天通过 8 种引人入胜的音频风格接收关于您的工作、优先事项和战略的更新——从纪录片旁白到战略顾问的声音。该系统可直接连接到您的代理的记忆和文件中。使用 Superlore.ai API 密钥，您可以免费生成 3 小时的播客内容。您可以安排早晨、中午或晚上的简报，让您无需查看屏幕即可随时了解最新信息。
metadata:
  openclaw:
    requires:
      env:
        - name: SUPERLORE_API_KEY
          description: "API key from superlore.ai — get one free at https://superlore.ai or use the setup wizard's email OTP flow"
          required: true
    permissions:
      - network: "HTTPS requests to superlore-api.onrender.com (official Superlore API hosted on Render)"
      - filesystem: "Reads workspace files (memory/*.md, JOBS.md, HEARTBEAT.md, MEMORY.md). Setup wizard optionally appends env var to ~/.zshrc or ~/.bashrc (user-confirmed)."
      - cron: "Setup wizard outputs openclaw cron commands for scheduling. Runs them only with explicit user confirmation."
---
# openclaw-podcast

**根据您的 OpenClaw 代理的记忆生成个性化的每日播客简报。**

您的人工智能代理已经了解了您今天的工作内容——包括您的记忆文件、项目进度、指标以及所做出的决策。此功能会通过 [Superlore.ai](https://superlore.ai) 将这些信息转化为专业的播客简报，无需任何手动输入。

**使用您的 API 密钥，可免费生成 3 小时的播客内容。**

## 设置

最快捷的开始方式是使用 **设置向导**——无需预先提供 API 密钥：

```bash
node scripts/setup-crons.js
```

设置向导会引导您完成 7 个步骤，并处理所有相关事宜，包括通过电子邮件创建账户：

1. **连接您的账户**——只需使用您的电子邮件（系统会发送 6 位验证码到您的收件箱）进行注册或登录，或粘贴现有的 API 密钥。
2. **选择您的风格**——从 8 种内置的简报风格中选择一种。
3. **自定义风格**——可选地自定义简报的内容、语气和声音。
4. **背景音乐**——选择背景音乐或仅使用语音。
5. **安排时间**——为每种风格设置播放时间（早晨/中午/晚上/每周/自定义定时器）。
6. **预览剧集**——生成实际的播客内容，以便您立即听取质量。
7. **激活**——输出 `openclaw cron add` 命令；也可以选择由系统自动执行这些命令。

**已经拥有 API 密钥吗？** 向导也支持这种情况——只需在提示时选择 “选项 A” 并粘贴您的现有密钥即可。

**手动设置（可选）：**

如果您希望跳过向导并手动进行设置：

1. 在 [superlore.ai](https://superlore.ai) 注册，然后进入 “账户” → “API 密钥”。
2. 设置环境变量：
   ```bash
   export SUPERLORE_API_KEY=your-api-key-here
   ```
   将此变量添加到您的 `~/.zshrc` 或 `~/.bashrc` 文件中，以便在会话之间保持设置。

## 快速入门

```bash
# Run the setup wizard (recommended — handles account + scheduling)
node scripts/setup-crons.js

# Or jump straight to generating a briefing if you already have an API key
node scripts/generate-episode.js

# Try different styles
node scripts/generate-episode.js --style "The Advisor"
node scripts/generate-episode.js --style "10X Thinking"

# Preview the prompt without creating an episode
node scripts/generate-episode.js --dry-run
```

## 60 秒内生成第一期播客

最快的方法是使用设置向导：

```bash
node scripts/setup-crons.js
# → Enter your email
# → Check inbox for 6-digit code
# → Paste the code — your API key is created automatically
# → Wizard generates a preview episode so you can hear the quality
```

或者，如果您已经拥有 API 密钥：

```bash
export SUPERLORE_API_KEY=your-key-here
node scripts/generate-episode.js --dry-run    # Preview what gets sent
node scripts/generate-episode.js              # Generate your first episode!
```

您的播客将在大约 2 分钟后准备好，具体地址会在输出中显示。就这样，您的代理已将您今天的工作转化为了播客内容。

## 功能介绍

该功能会读取您的 OpenClaw 工作区文件：
- `memory/YYYY-MM-DD.md` — 日常活动日志
- `JOBS.md` — 项目进度和任务列表
- `HEARTBEAT.md` — 当前优先事项和即将进行的工作
- `MEMORY.md` — 长期工作背景信息（可选）

然后，它会将这些数据预处理成结构化的简报内容（包括已完成的任务、指标、阻碍因素以及即将进行的工作），并通过 Superlore 的 API 生成专业的播客剧集。

## 隐私与数据流

您的工作区包含敏感信息。以下是该功能如何保护这些信息的详细说明：

### 生成简报时的处理过程

```
Your Machine (private)              Superlore API (remote)
┌─────────────────────┐             ┌──────────────────┐
│ 1. Agent reads your │             │                  │
│    workspace files  │             │ 4. GPT writes    │
│                     │             │    podcast script │
│ 2. Script extracts  │             │                  │
│    work summaries   │   ONLY      │ 5. Kokoro TTS    │
│                     │  ──────►    │    generates      │
│ 3. Secrets stripped │  briefing   │    audio          │
│    (keys, emails,   │   text      │                  │
│    IPs, paths, DBs) │             │ 6. Private episode│
│                     │             │    stored         │
└─────────────────────┘             └──────────────────┘
```

### 实际发送的内容
- 经过处理的简报摘要（约 3,000 个字符的工作描述）
- 风格设置指令（例如：“采用纪录片旁白风格”）
- 语音/语速偏好设置

### 绝对不会发送的内容
- ❌ 您的原始工作区文件
- ❌ API 密钥、令牌、密码或凭证
- ❌ 电子邮件地址
- ❌ IP 地址或内部主机名
- ❌ 数据库连接字符串
- ❌ 系统中的文件路径
- ❌ SSH 凭据
- ❌ 代理配置（模型路由、定时器设置等）

### 如何保护敏感信息

脚本采用了 **三层安全处理机制**：

1. **段落过滤**——在提取数据之前，会排除 `MEMORY.md` 中包含操作细节（如凭证、模型路由、定时器配置）的段落。
2. **行过滤**——删除任何提及 API 密钥、密码、令牌、数据库 URL 或服务 ID 的行。
3. **模式过滤**——对整个简报内容进行正则表达式检查，以删除任何看起来像敏感信息的元素：长令牌（`sk_*`、`ghp_*`、`rpa_*`）、数据库 URL（`postgres://`）、电子邮件地址、内部 IP 地址、Base64 编码的数据以及绝对文件路径。

### 自行验证

运行 `--dry-run` 命令，查看实际会发送到 Superlore 的内容——没有任何隐藏信息：

```bash
node scripts/generate-episode.js --dry-run
```

该命令会显示完整的输出内容。如果您发现任何敏感信息，请 [向我们报告](https://github.com/openclaw/openclaw/issues)，以便我们改进安全规则。

### 播客的可见性

所有简报的可见性都被设置为 “私有”（`visibility: private`）。这是脚本中的硬编码设置，无法通过任何标志或配置进行更改。只有您自己可以访问这些简报。

### Superlore 的处理流程

Superlore 的 API 接收简报文本，通过 GPT 生成脚本内容，并使用 Kokoro TTS 生成音频。播客会存储在 Superlore 的基础设施中，与您的账户关联。Superlore 无法访问您的文件系统、OpenClaw 代理或您发送的简报之外的任何文件。

## 简报风格

从 8 种不同的视角中选择一种风格——每种风格都能为您提供不同的工作视角：

1. **The Briefing** — 个人纪录片风格。专业的旁白会为您讲述当天的成就、关键指标、遇到的障碍以及接下来的工作计划。内容清晰、结构化且全面。
2. **Opportunities & Tactics** — 发现您可能忽略的成长机会、战略角度和战术措施。适合需要新想法的时候。
3. **10X Thinking** — 挑战您的思维局限，促使您以更大的视角思考问题。当您陷入渐进式思维模式时，这个风格非常有用。
4. **The Advisor** — 来自经验丰富的导师的坦诚反馈。不加掩饰，直接指出哪些方法有效、哪些无效，以及应该如何改进。这是您值得信赖的顾问。
5. **Focus & Priorities** — 剔除干扰，明确区分真正重要的事情和只是忙于表面工作的内容。帮助您拒绝无关事务，专注于关键任务。
6. **Growth & Scale** — 专注于数字指标：收入、用户数量、转化路径和增长趋势。通过业务指标和可扩展性来分析您的工作。
7. **Week in Review** — 回顾一周的工作，总结趋势、经验教训以及下周的目标。建议在周五或周日晚上收听。
8. **The Futurist** — 将您的日常工作与 3 个月、6 个月和 12 个月的目标联系起来。帮助您在快速前进的同时保持与长期目标的同步。

更多关于每种风格的定义和提示模板，请参阅 `references/styles.md`。

## 语音选项

为您的播客提供了三种精选的语音：

| 语音 | 特点 | 适合的风格 |
|-------|-----------|----------|
| **Luna** (`af_heart-80_af_sarah-15_af_nicole-5`) | 温暖、平衡的语调——适合女性听众 | The Briefing、The Advisor、Week in Review |
| **Michael** (`am_michael-60_am_eric-40`) | 丰富、富有感染力的语调——适合男性听众 | Opportunities、10X Thinking、Growth & Scale |
| **Heart** (`af_heart`) | 轻柔、亲切的语调——适合女性听众 | Focus & Priorities、The Futurist |

Luna 是 Superlore 的标志性语音，适合各种类型的播报内容。Michael 适合需要权威性和战略指导的风格。Heart 则是最具个人化特色的语音，适合需要直接交流的风格。

## 自定义风格

不限于这 8 种默认风格！您可以在工作区的 `podcast-styles/` 目录中上传 JSON 文件来创建自己的播客风格：

```json
// podcast-styles/my-style.json
{
  "name": "My Custom Style",
  "description": "Brief description",
  "voice": "af_heart-80_af_sarah-15_af_nicole-5",
  "speed": 0.95,
  "targetMinutes": 6,
  "instructions": "Detailed instructions for the AI narrator..."
}
```

自定义风格的语音选项：
- `"af_heart-80_af_sarah-15_af_nicole-5"` — **Luna**（温暖、平衡的语调）
- `"am_michael-60_am_eric-40"` — **Michael**（丰富、权威的语调）
- `"af_heart"` — **Heart**（轻柔、亲切的语调）

使用方法如下：
```bash
node scripts/generate-episode.js --style "My Custom Style"
node scripts/generate-episode.js --custom "my-style"  # matches filename
node scripts/generate-episode.js --list-styles  # see all available
```

示例自定义风格包括：**Founder Debrief**（创始人之间的非正式对话）和 **Competitor Watch**（竞争情报视角）。

## 安排定时

使用 `setup-crons.js` 配置每日自动播报：

```bash
node scripts/setup-crons.js
```

设置向导会引导您完成 7 个步骤：

1. **连接您的账户**——通过电子邮件或 OTP（6 位验证码）注册或登录；验证密钥并显示剩余的可用时间。
2. **选择您的风格**——从 8 种内置风格中选择一种（例如，早晨使用 “The Briefing”，晚上使用 “The Advisor”）。
3. **自定义风格**——可选地自定义简报的内容、语气和声音。
4. **背景音乐**——选择背景音乐或仅使用语音。
5. **安排时间**——为每种风格设置播放时间（早晨/中午/晚上/每周/自定义定时器）。
6. **预览剧集**——生成实际的播客内容，以便您立即听取质量。
7. **激活**——输出 `openclaw cron add` 命令；也可以选择由系统自动执行这些命令。

每种内置风格都配有预设的语音：
- **Luna** 适用的风格：The Briefing、The Advisor、Week in Review
- **Michael** 适用的风格：Opportunities & Tactics、10X Thinking、Growth & Scale
- **Heart** 适用的风格：Focus & Priorities、The Futurist

示例输出：
```bash
# The script will generate commands like:
/cron create "0 8 * * *" agent:run node scripts/generate-episode.js --style "The Briefing" --time-of-day morning

# Just copy-paste these into your OpenClaw chat to activate
```

设置完成后，播报将自动生成，并在您指定的时间准备好播放。系统会发送包含剧集链接的通知。

## 配置选项

脚本使用默认设置，但也支持以下参数：

- `--style <name>` — 简报风格（默认：The Briefing）
- `--time-of-day <morning|midday|evening>` — 影响问候语和语气
- `--date YYYY-MM-DD` — 为特定日期生成简报（默认：今天）
- `--dry-run` — 预览实际会发送的内容（没有任何隐藏信息）
- `--no-memory` — 完全忽略 MEMORY.md 文件（仅使用日常文件）
- `--api-url <url>` — 替换 Superlore 的 API 地址
- `--device-id <id>` — 可选的设备标识符（用于使用分析，无需用于身份验证）
- `--channel <channel>` — 当播报准备好时，将链接发送到指定渠道（例如 Telegram、Discord）

## 所需条件

- 拥有包含记忆文件的 OpenClaw 工作区
- Superlore.ai API 密钥（可在 [superlore.ai](https://superlore.ai) 获取）
- 网络连接（播报内容通过 Superlore API 生成）
- 使用 API 密钥可免费生成 3 小时的播客内容

## 更多信息

- **Superlore.ai** — [https://superlore.ai](https://superlore.ai)
- **API 参考** — `references/api.md`
- **风格指南** — `references/styles.md`

## 使用建议

- 先从 **"The Briefing"** 风格开始，熟悉播报格式。
- 当您需要关于工作的坦诚反馈时，使用 **"The Advisor"**。
- 当您感到思维僵化或需要挑战自己的假设时，尝试使用 **"10X Thinking"**。
- **"Week in Review"** 适合在周五或周日晚上收听。
- 使用 `--dry-run` 命令在创建播报前测试提示内容。
- 早晨的简报侧重于当天的工作安排；晚上的简报则回顾当天的成就。

## 示例

```bash
# Morning briefing with advisor style
node scripts/generate-episode.js --style "The Advisor" --time-of-day morning

# Weekly review for Friday
node scripts/generate-episode.js --style "Week in Review" --time-of-day evening

# Preview what a growth-focused briefing would look like
node scripts/generate-episode.js --style "Growth & Scale" --dry-run

# Generate and deliver the episode link to Telegram when ready
node scripts/generate-episode.js --channel telegram
```

---

**此功能由 OpenClaw 社区用心制作，由 Superlore.ai 提供技术支持。**