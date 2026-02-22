---
name: openclaw-podcast
description: 将您的 OpenClaw 工作空间转变为个性化的、由 AI 驱动的播客简报系统。每天接收关于您的工作、优先事项和战略的音频更新，这些更新采用 8 种不同的风格呈现（从纪录片旁白到战略顾问的风格）。该系统可直接与您的代理的记忆和文件进行交互。使用 Superlore.ai API 密钥，您可以免费生成 3 小时的播客内容。您可以安排早晨、中午或晚上的简报时间，让您无需查看屏幕即可随时了解最新信息。
---
# openclaw-podcast

**利用 OpenClaw 代理的记忆，生成个性化的每日播客简报。**

您的人工智能代理已经掌握了您今天的工作内容——包括您的记忆文件、项目进度、各项指标以及您所做的决策。此功能会通过 [Superlore.ai](https://superlore.ai) 将这些信息转化为专业的播客简报，无需任何手动输入。

**使用您的 API 密钥，可免费生成 3 小时的播客内容。**

## 设置

最快捷的开始方式是使用 **设置向导**——无需预先提供 API 密钥：

```bash
node scripts/setup-crons.js
```

向导会引导您完成 7 个步骤，并处理所有相关事宜，包括通过电子邮件创建账户：

1. **连接您的账户**——使用您的电子邮件（系统会发送 6 位验证码到您的邮箱）进行注册或登录，或粘贴现有的 API 密钥。
2. **选择样式**——从 8 种内置的简报样式中选择一个。
3. **自定义样式**——（可选）根据您的需求自定义简报的内容、语气和语音。
4. **背景音乐**——选择背景音乐或仅使用语音。
5. **安排时间**——为每种样式设置播放时间（早晨/中午/晚上/每周/自定义定时任务）。
6. **预览节目**——生成实际的播客内容，以便您立即试听质量。
7. **激活**——输出 `openclaw cron add` 命令；也可以选择由系统自动执行这些命令。

**已经拥有 API 密钥？** 向导也支持这种情况——在提示时选择 “选项 A” 并粘贴您的密钥即可。

**手动设置（可选）：**

如果您希望跳过向导并手动进行设置：

1. 在 [superlore.ai](https://superlore.ai) 注册账户，然后进入 “账户” → “API 密钥”。
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

您的播客将在大约 2 分钟后准备好，具体链接会在输出中显示。就这样，您的代理已经将今天的工作转化为了播客内容。

## 功能介绍

该功能会读取您的 OpenClaw 工作区文件：
- `memory/YYYY-MM-DD.md` — 日常活动日志
- `JOBS.md` — 项目进度和任务列表
- `HEARTBEAT.md` — 当前优先事项和即将进行的工作
- `MEMORY.md` — 长期工作背景信息（可选）

然后，它会将这些数据预处理成结构化的简报内容（包括成就、指标、阻碍因素以及即将进行的工作），并通过 Superlore 的 API 生成专业的播客节目。

## 隐私与数据传输

您的工作区包含敏感信息。以下是该功能如何保护这些信息的详细说明：

### 生成简报时的处理流程

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

### 传输的内容
- 经过处理的简报摘要（约 3,000 个字符的工作描述）
- 风格设置指令（例如：“采用纪录片旁白风格”）
- 语音/语速偏好设置

### 绝对不会传输的内容
- ❌ 您的原始工作区文件
- ❌ API 密钥、令牌、密码或凭证
- ❌ 电子邮件地址
- ❌ IP 地址或内部主机名
- ❌ 数据库连接字符串
- ❌ 系统中的文件路径
- ❌ SSH 凭据
- ❌ 代理配置（模型路由、定时任务配置等）

### 如何保护敏感信息

脚本采用了 **三层安全处理机制**：

1. **章节过滤**——在提取数据之前，会排除 `MEMORY.md` 中包含操作细节（如凭证、模型路由、定时任务配置）的章节。
2. **行过滤**——会删除任何提及 API 密钥、密码、令牌、数据库 URL 或服务 ID 的行。
3. **模式过滤**——会对整个简报内容进行正则表达式检查，以移除任何可能被视为敏感的信息：长格式令牌（`sk_*`、`ghp_*`、`rpa_*`）、数据库 URL（`postgres://`）、电子邮件地址、内部 IP 地址、Base64 编码的数据以及绝对文件路径。

### 自行验证

运行 `--dry-run` 命令，查看实际会传输到 Superlore 的内容——没有任何隐藏的信息：

```bash
node scripts/generate-episode.js --dry-run
```

该命令会显示完整的输出内容。如果您发现任何敏感信息，请 [向我们报告](https://github.com/openclaw/openclaw/issues)，以便我们改进安全规则。

### 播客的可见性

所有简报的可见性都被设置为 “私有”（`visibility: private`）。这是脚本中的硬编码设置，无法通过任何标志或配置进行更改。只有您自己可以访问这些简报。

### Superlore 的处理流程

Superlore 的 API 会接收简报文本，通过 GPT 生成脚本内容，并使用 Kokoro TTS 生成音频。播客内容会存储在 Superlore 的基础设施中，且仅与您的账户关联。Superlore 无法访问您的文件系统、OpenClaw 代理或您发送的简报之外的任何文件。

## 简报样式

您可以从 8 种不同的视角中选择一种风格，每种风格都能为您提供不同的工作视角：

1. **The Briefing** — 个人纪录片风格。专业的旁白会为您讲述今天的成就、关键指标、遇到的障碍以及接下来的工作计划。内容清晰、结构化且全面。
2. **Opportunities & Tactics** — 发现您可能忽略的成长机会、战略角度和战术措施。适合需要新想法的时候。
3. **10X Thinking** — 挑战您的思维定势，帮助您跳出常规思维模式，进行更深入的思考。
4. **The Advisor** — 来自经验丰富的导师的坦诚反馈。直接指出哪些方法有效、哪些无效，以及应如何改进。是您值得信赖的顾问。
5. **Focus & Priorities** — 剔除干扰，明确区分真正重要的事情和仅仅是忙碌的工作。帮助您拒绝无关事项，专注于关键任务。
6. **Growth & Scale** — 专注于数据（收入、用户数量、转化率等指标），通过业务指标和可扩展性分析您的工作。
7. **Week in Review** — 回顾一周的工作，总结趋势、经验教训以及下周的目标。适合在周五或周日晚上收听。
8. **The Futurist** — 将您的日常工作与 3 个月、6 个月和 12 个月的长期目标联系起来。帮助您在快速推进工作的同时保持目标方向。

更多样式定义和提示模板请参阅 `references/styles.md`。

## 语音选项

我们提供了三种精选的语音供您选择：

| 语音 | 特点 | 适合的风格 |
|-------|-----------|----------|
| **Luna** (`af_heart-80_af_sarah-15_af_nicole-5`) | 温暖、平衡的语调——适合女性听众 | The Briefing、The Advisor、Week in Review |
| **Michael** (`am_michael-60_am_eric-40`) | 深沉、富有共鸣的语调——适合男性听众 | Opportunities、10X Thinking、Growth & Scale |
| **Heart** (`af_heart`) | 轻柔、亲切的语调——适合女性听众 | Focus & Priorities、The Futurist |

Luna 是 Superlore 的标志性语音，适合各种类型的播报内容。Michael 适合需要权威性和战略指导的风格。Heart 则是最具个人化特色的语音，适合需要直接交流的风格。

## 自定义样式

您不仅限于这 8 种默认样式！您可以在工作区的 `podcast-styles/` 目录中上传 JSON 文件来创建自己的播客样式：

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

自定义样式的语音选项：
- `"af_heart-80_af_sarah-15_af_nicole-5"` — **Luna**（温暖、平衡的语调）
- `"am_michael-60_am_eric-40"` — **Michael**（深沉、权威的语调）
- `"af_heart"` — **Heart**（轻柔、亲切的语调）

使用方法如下：
```bash
node scripts/generate-episode.js --style "My Custom Style"
node scripts/generate-episode.js --custom "my-style"  # matches filename
node scripts/generate-episode.js --list-styles  # see all available
```

示例自定义样式包括：**Founder Debrief**（创始人之间的非正式对话）和 **Competitor Watch**（竞争情报视角）。

## 定时任务

使用 `setup-crons.js` 配置自动每日播报：

```bash
node scripts/setup-crons.js
```

设置向导会引导您完成 7 个步骤：

1. **连接您的账户**——使用电子邮件或 OTP（6 位验证码）进行注册或登录，或粘贴现有的 API 密钥；系统会验证密钥并显示剩余的可用时间。
2. **选择样式**——从 8 种内置样式中选择一个（例如：“The Briefing” 适合早晨，“The Advisor” 适合晚上）。
3. **自定义样式**——（可选）根据您的需求自定义简报的内容、语气和语音。
4. **背景音乐**——选择背景音乐或仅使用语音。
5. **安排时间**——为每种样式设置播放时间（早晨/中午/晚上/每周/自定义定时任务）。
6. **预览节目**——生成实际的播客内容，以便您立即试听质量。
7. **激活**——输出 `openclaw cron add` 命令；也可以选择由系统自动执行这些命令。

每种内置样式都配有预设的语音：
- **Luna** 的语音：The Briefing、The Advisor、Week in Review
- **Michael** 的语音：Opportunities & Tactics、10X Thinking、Growth & Scale
- **Heart** 的语音：Focus & Priorities、The Futurist

示例输出：
```bash
# The script will generate commands like:
/cron create "0 8 * * *" agent:run node scripts/generate-episode.js --style "The Briefing" --time-of-day morning

# Just copy-paste these into your OpenClaw chat to activate
```

设置完成后，播报将自动生成，并在您指定的时间准备好播放。系统会发送包含链接的通知。

## 配置选项

脚本使用默认设置，但也支持以下参数：

- `--style <name>` — 简报样式（默认：The Briefing）
- `--time-of-day <morning|midday|evening>` — 影响问候语和语气
- `--date YYYY-MM-DD` — 为特定日期生成简报（默认：今天）
- `--dry-run` — 预览实际会传输的内容（没有任何隐藏信息）
- `--no-memory` — 完全跳过 MEMORY.md 文件（仅使用日常文件）
- `--api-url <url>` — 替换 Superlore 的 API URL
- `--device-id <id>` — 可选的设备标识符（用于分析使用情况，但不是身份验证必需项）
- `--channel <channel>` — 在播报准备好后，将链接发送到指定渠道（例如 Telegram、Discord）

## 使用要求

- 需要拥有包含记忆文件的 OpenClaw 工作区。
- 需要 Superlore.ai 的 API 密钥（可在 [superlore.ai](https://superlore.ai) 获取）。
- 需要互联网连接（播报内容通过 Superlore API 生成）。
- 使用 API 密钥可免费生成 3 小时的播客内容。

## 更多信息

- **Superlore.ai** — [https://superlore.ai](https://superlore.ai)
- **API 参考文档** — `references/api.md`
- **样式指南** — `references/styles.md`

## 使用建议

- 先从 **"The Briefing"** 样式开始，熟悉播报格式。
- 当您需要关于工作的坦诚反馈时，可以使用 **"The Advisor"**。
- 当您感到思维僵化或需要挑战自己的假设时，可以尝试 **"10X Thinking"**。
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

**这份功能专为 OpenClaw 社区精心制作，由 Superlore.ai 提供支持。**