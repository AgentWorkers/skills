---
name: openclaw-podcast
description: 将您的 OpenClaw 工作空间转变为个性化的、由 AI 提供支持的播客简报系统。每天通过音频获取关于您的工作内容、优先事项和战略信息的更新，共有 8 种不同的表达风格可供选择（从纪录片旁白风格到战略顾问风格）。该系统可直接连接到您的代理（agent）的记忆和文件系统中。使用 Superlore.ai 的 API 密钥，您可以免费获得 3 小时的播客生成服务。您可以安排早晨、中午或晚上的简报时间，让您无需查看屏幕即可随时了解最新情况。
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

**你的AI助手已经全面了解了你的工作内容，现在它可以为你提供工作汇报了。**

每天，OpenClaw助手都会收集各种信息——你的工作成果、各项指标、遇到的阻碍以及优先事项。然后，它会通过[Superlore.ai](https://superlore.ai)将这些信息转化为专业的播客形式，为你呈现出来。无需填写任何表格，也无需手动总结，只需点击播放即可。

**使用API密钥即可享受3小时的免费服务。设置过程仅需2分钟。**

---

## 🎧 亲自试听——8期样例节目

这些是由该功能为虚构角色生成的真实播客节目，每期都展示了不同的汇报风格。听听看：*如果AI了解你的工作内容，会是什么样的汇报呢？*

---

### 🎙️ 工作汇报
**Sarah Chen** — TaskFlow公司（B2B SaaS服务，B轮融资阶段）的工程副总裁

> “延迟从340毫秒降低到47毫秒，这不仅仅是一个性能上的提升——它表明我们的架构终于实现了设计初衷……”

Sarah的助手每晚都会读取她的冲刺板、代码合并历史记录、事件日志以及工程指标，并呈现出一份精心制作的报告——就像有一位已经在团队中工作了几个月的私人分析师一样。

🎧 **[收听：Sarah Chen的工作汇报](https://superlore.ai/episode/cmlyu95qm0006mvy4gue30cj6)**

---

### 📈 机会与策略
**Blake Rivera** — Lumière Skin公司的创始人（DTC护肤品，月收入31.2万美元）

> “你的现有客户群中隐藏着10万美元的月度订阅收入潜力。而且还有一个已经无人回应的 spa 链条合作请求……”

Blake的助手通过分析他的指标文件，发现了订阅转化率与行业平均水平（18-25%）之间的12%差距，计算出了错失的批发机会。

🎧 **[收听：机会与策略——Blake Rivera](https://superlore.ai/episode/cmlyu9al90008mvy46oxs4fvm)**

---

### 🚀 10倍思考
**Marcus Webb** — 独立开发者，Nexus AI框架的开发者（GitHub上有2,847个星标）

> “LangChain有8万个星标，而你只有2,847个。但这个比较可能并不准确。如果Nexus不是一个框架，而是一个行业标准呢？”

Marcus的助手会阅读他的GitHub活动记录、Discord交流记录以及技术笔记，然后挑战他对自身工作以及竞争对手的认知。

🎧 **[收听：10倍思考——Marcus Webb](https://superlore.ai/episode/cmlyu9f78000amvy4i27vek90)**

---

### 🧭 顾问
**Priya Nair** — SkillBridge公司的创始人（教育科技领域，Pre-Seed阶段）

> “我注意到你本月有40小时用于产品开发，8小时用于筹款。考虑到还有7个月的开发周期，以及8天后就要进行Pre-Seed阶段的演示，这种时间分配模式值得关注……”

Priya的助手会审查她的时间分配情况、项目进度以及交流记录，然后给出她可能在其他地方无法获得的坦诚建议。

🎧 **[收听：顾问——Priya Nair](https://superlore.ai/episode/cmlyu9jic000cmvy4dzqi4fmc)**

---

### 🎯 专注与优先级
**Alex Kim** — 一家年收入24亿美元的FAANG级公司的工程经理

> “4.5小时用于会议，2.5小时用于Slack交流，实际深入工作的时间只有1.5小时。这根本算不上工程领导力——这只是被动的管理方式。而且已经有两名工程师在悄悄考虑离职了……”

Alex的助手会分析他的日程记录、Slack使用情况以及公司整体环境，然后直接指出真正重要的事情和那些只是表面上看似紧急的事情。

🎧 **[收听：专注与优先级——Alex Kim](https://superlore.ai/episode/cmlyu9o3v000emvy4qi9rgzli)**

---

### 📊 成长与扩展
**Jordan Park** — Meridian Finance公司的增长负责人（YC W23阶段，拥有8.4万用户）

> “数据分析结果非常明确：在48小时内添加第二个银行账户的用户，90天的留存率提高了3.2倍。这个发现足以让你重新设计用户入职流程……”

Jordan的助手处理了30天的用户数据分析结果，找出了用户留存率的瓶颈，并确定了能够带来重大改变的关键指标。

🎧 **[收听：成长与扩展——Jordan Park](https://superlore.ai/episode/cmlyu9scx000gmvy45wozwrq7)**

---

### 📅 本周回顾
**Elena Vasquez** — ClearPath Health公司的首席技术官（A轮融资阶段，拥有31家医院客户）

> “周一解决了合规性问题，周二完成了技术发布，周三打开了一个价值18万美元的新业务机会，周四修复了系统故障，周五进一步优化了系统。这一周的工作成果非常显著……”

Elena的助手会将本周的工作成果、部署情况、客户交流以及各项指标整合成一个连贯的故事，让她能够从宏观角度审视整个工作过程。

🎧 **[收听：本周回顾——Elena Vasquez](https://superlore.ai/episode/cmlyu9wx7000imvy4unlzu3gn)**

---

### 🔮 未来主义者
**David Okonkwo** — Terravolt Energy公司的创始人（气候科技领域，种子轮融资420万美元）

> “43%的能源消耗减少不仅仅是一个试点项目的成果——这证明了AI能够释放美国电网中闲置的85吉瓦可再生能源。这就是我们正在努力的目标……”

David的助手会将今天的试点结果、临时专利申请以及能源部的资助申请与3个月到6个月的长期发展计划联系起来，帮助他在复杂的环境中保持对目标的清晰认识。

🎧 **[收听：未来主义者——David Okonkwo](https://superlore.ai/episode/cmlyua1c8000kmvy47l1f9b5a)**

---

## ✨ 这个功能的独特之处

大多数AI总结都是泛泛而谈的，它们只知道你在聊天框里输入了什么。而这个功能真正了解你的实际工作内容——因为它每天都会读取你的工作文件。

**实际应用中的区别：**

| 泛泛的AI总结 | OpenClaw播客 |
|---|---|
| “你今天完成了一些工程任务” | “延迟从340毫秒降低到47毫秒，为你期待了两个月的 enterprise 级产品发布铺平了道路” |
| “你应该专注于优先事项” | “你本月有40小时用于产品开发，8小时用于筹款——考虑到还有7个月的开发周期，这个比例需要调整” |
| “考虑增长机会” | “你的订阅转化率为12%，而行业平均水平是18-25%，这意味着你的现有客户群中隐藏着10万美元的月收入潜力” |

AI知道你的项目名称、各项指标、遇到的阻碍以及工作进度。所有这些信息，通常需要花费10分钟才能向顾问解释清楚——而你的助手已经掌握了这些信息。

**Superlore还提供了以下额外功能：**
- 📝 **笔记** — 将播客中的见解保存到你的个人资料库
- 🎵 **播客库** — 随时可以回听任何一期节目
- 🗣️ **高级语音合成** — 由Kokoro提供，音质自然
- 🎨 **AI封面设计** — 每期节目都会有独特的封面图片
- ⚡ **快速生成** — 播客文件大约2分钟内即可生成

---

## 设置

最快开始使用该功能的步骤是完成设置：

```bash
node scripts/setup-crons.js
```

设置向导会分7个步骤完成所有设置，只需提供你的电子邮件地址：
1. **连接你的账户** — 通过电子邮件注册或登录（输入6位验证码），或者粘贴现有的API密钥
2. **选择风格** — 从8种预设的汇报风格中选择
3. **自定义风格** — 可以自定义汇报的重点、语气和语音
4. **背景音乐** — 选择背景音乐或仅使用语音
5 **安排时间** — 为每种风格设置播放时间（早上/中午/晚上/每周/自定义定时）
6 **预览节目** — 生成一期实际节目，让你立即感受音质
7 **激活服务** — 生成`openclaw cron add`命令；可以选择自动执行这些命令

**已经拥有API密钥吗？** 可以手动完成设置：

```bash
export SUPERLORE_API_KEY=your-api-key-here
node scripts/generate-episode.js  # Your first episode in 2 minutes
```

---

## 8种汇报风格

| 风格 | 适用场景 | 语音 | 默认播放时间 |
|-------|----------|-------|--------------|
| **工作汇报** | 每日总结——工作成果、指标、下一步计划 | Luna | 早上或晚上 |
| **机会与策略** | 发现日常工作中的增长机会 | Michael | 晚上 |
| **10倍思考** | 打破常规思维模式 | Michael | 晚上 |
| **顾问** | 对工作模式和决策提供坦诚的建议 | Luna | 晚上 |
| **专注与优先级** | 剔除无意义的工作，找出最重要的任务 | Heart | 早上 |
| **成长与扩展** | 从收入、用户数量等角度分析业务指标 | Michael | 早上 |
| **本周回顾** | 每周总结、趋势分析、下周目标 | Luna | 星期五晚上 |
| **未来主义者** | 将当前工作与长期发展目标联系起来 | Heart | 晚上 |

---

## 语音选项

| 语音 | 人物特征 | 适用风格 |
|-------|-----------|--------|
| **Luna** (`af_heart-80_af_sarah-15_af_nicole-5`) | 温暖、平衡、专业 | 工作汇报、顾问、本周回顾 |
| **Michael** (`am_michael-60_am_eric-40`) | 丰富、权威、策略性强 | 机会与策略、10倍思考、成长与扩展 |
| **Heart** (`af_heart`) | 亲切、直接、个性化 | 专注与优先级、未来主义者 |

---

## 自定义风格

你可以在`podcast-styles/`目录下创建自己的汇报风格：

```json
{
  "name": "Investor Lens",
  "description": "Frame every decision through how it affects the fundraising narrative",
  "voice": "am_michael-60_am_eric-40",
  "speed": 0.92,
  "targetMinutes": 6,
  "instructions": "Your detailed style instructions..."
}
```

这里有两个示例：**Founder Debrief**（适合创始人使用的轻松风格）和**Competitor Watch**（用于竞争情报分析）。

---

## 定时播放

你可以设置自动化的每日播报：

```bash
node scripts/setup-crons.js
# → Outputs openclaw cron add commands
# → Optionally runs them for you
```

以下是一个早上播报和晚上顾问汇报的定时示例：

```
/cron create "0 8 * * 1-5" agent:run node scripts/generate-episode.js --style "The Briefing" --time-of-day morning
/cron create "0 19 * * 1-5" agent:run node scripts/generate-episode.js --style "The Advisor" --time-of-day evening
```

---

## 隐私保护

你的工作文件**永远不会被发送到Superlore**。具体流程如下：
1. 在本地读取你的工作文件
2. 提取结构化的工作总结（约3,000个字符，包括工作成果、指标和阻碍）
3. 去除所有敏感信息（API密钥、令牌、电子邮件地址、IP地址、数据库链接、文件路径）
4. 仅将处理后的报告文本发送给Superlore的API

所有播客默认设置为私密状态。运行`--dry-run`命令可以查看实际发送的内容。

---

## 快速操作命令

```bash
# Setup wizard (recommended)
node scripts/setup-crons.js

# Generate an episode
node scripts/generate-episode.js
node scripts/generate-episode.js --style "The Advisor"
node scripts/generate-episode.js --style "10X Thinking" --time-of-day morning

# Weekly review (best on Fridays)
node scripts/generate-episode.js --style "Week in Review"

# Preview without creating
node scripts/generate-episode.js --dry-run

# List all available styles
node scripts/generate-episode.js --list-styles

# Deliver episode link to a channel when ready
node scripts/generate-episode.js --channel telegram
```

---

## 使用要求

- 需要一个包含工作记录的OpenClaw工作空间文件（格式为`memory/YYYY-MM-DD.md`）
- 需要Superlore.ai的API密钥——可在[superlore.ai](https://superlore.ai)免费获取
- **包含3小时的免费播客生成服务**

---

**我们用心为您打造这款产品，专为OpenClaw社区设计。技术支持来自[Superlore.ai](https://superlore.ai)。**