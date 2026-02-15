---
name: linkedin-autopilot
description: 您的代理会在您睡觉时帮助您建立和维护在 LinkedIn 上的形象。它可以自动安排帖子的发布时间，与目标账户进行互动，发送个性化的私信，确保不会错过任何交流机会。它还能处理连接请求、访问目标用户资料的行为，以及后续的互动流程，并且会通过合理的频率控制（throttling）和类似人类的行为模式来确保互动的顺利进行。您可以配置目标用户、定义互动规则，让您的代理全天候自动执行这些任务。无论是在设置 LinkedIn 自动化流程、管理发布计划、开展互动活动，还是构建由代理驱动的 LinkedIn 客户开发工作流时，这个工具都非常实用。
metadata:
  clawdbot:
    emoji: "🤝"
    requires:
      browser: true
      env:
        - LINKEDIN_EMAIL
        - LINKEDIN_PASSWORD
---

# LinkedIn Autopilot — 24/7智能助手，助力您的职业网络建设

**您在休息时，LinkedIn却在不断成长。**

LinkedIn Autopilot将您的“职业助手”转变为一个全天候的LinkedIn管理工具。它能够自动安排帖子发布、与目标账户互动、发送个性化私信，并在您专注于实际工作期间帮助您拓展人脉。再也不用为“应该多发些帖子”而烦恼，也不用错过任何互动机会，更无需手动发送连接请求了。

**它的独特之处：** 这不是一个简单的机器人——它使用真实的浏览器自动化技术，模拟人类的行为模式。它会有随机的延迟、自然的互动方式、安全的发送频率控制，以及智能的目标定位功能。此外，它还能根据条件逻辑执行多日的互动序列，并能跨会话跟踪您的操作状态，同时提供详细的报告，展示哪些策略有效。

## 解决的问题

❌ **“我每天在LinkedIn上花费2小时，却毫无收获”**  
✅ 您的助手会自动处理所有的互动、私信发送和人脉建立工作。

❌ **“我的帖子发布不规律，导致影响力下降”**  
✅ 它会按照最佳时间表自动发布帖子——绝不会忘记任何一次。

❌ **“我看到有互动的机会，但太忙了”**  
✅ 它会自动在目标账户的帖子下发表个性化的评论。

❌ **“跟进流程太繁琐，导致线索丢失”**  
✅ 它会执行多步骤的私信序列，并根据条件逻辑进行自动跟进。

❌ **“我想拓展人脉，但发送连接请求显得像垃圾信息”**  
✅ 它会发送带有个性化备注的定向连接请求，并严格控制发送频率。

## 设置步骤

1. 运行 `scripts/setup.sh` 以初始化配置和数据目录。
2. 编辑 `~/.config/linkedin-autopilot/config.json` 文件，设置目标账户、互动序列和发布计划。
3. 将LinkedIn账号信息存储在 `~/.clawdbot/secrets.env` 文件中：
   ```bash
   LINKEDIN_EMAIL=your-email@example.com
   LINKEDIN_PASSWORD=your-password
   ```
4. 使用 `scripts/engage.sh --dry-run` 命令进行测试。

## 配置文件

所有配置信息都保存在 `~/.config/linkedin-autopilot/config.json` 文件中。请参考 `config.example.json` 了解完整的配置结构。

**关键配置项：**
- **identity**：您的LinkedIn个人资料信息（用于个性化操作）
- **targets**：要互动的对象（公司、个人或关键词）
- **posting**：发布计划、内容队列和最佳发布时间
- **engagement**：自动点赞/评论规则、目标帖子选择策略
- **outreach**：连接请求策略和私信发送流程
- **safety**：发送频率限制、延迟设置、预热期和禁售时段

## 脚本说明

| 脚本 | 功能 |
|--------|---------|
| `scripts/setup.sh` | 初始化配置和数据目录 |
| `scripts/post.sh` | 从队列中按计划发布内容 |
| `scripts/engage.sh` | 自动在目标帖子下点赞、评论或分享 |
| `scripts/dm-sequence.sh` | 管理私信发送序列 |
| `scripts/connect.sh` | 向目标账户发送连接请求 |
| `scripts/report.sh` | 生成分析报告（互动情况、增长数据等）

所有脚本都支持 `--dry-run` 选项，允许在不实际发布或互动的情况下进行测试。

## 发布流程

按照计划（例如每天定时执行）运行 `scripts/post.sh` 脚本。该脚本会：
1. 检查配置中的发布队列。
2. 确认发布时间是否符合LinkedIn的规则（避开禁售时段和发送频率限制）。
3. 通过浏览器自动化登录LinkedIn。
4. 以预设的格式发布内容。
5. 记录发布效果并更新队列状态。

**发布队列示例：**
```json
"posts": [
  {
    "content": "5 lessons from building AI agents in production:\n\n1. ...",
    "scheduled_time": "2024-01-28T09:00:00Z",
    "status": "pending",
    "media": null
  }
]
```

## 互动流程

每天运行 `scripts/engage.sh` 3-4次。该脚本会：
1. 搜索符合目标条件的帖子（关键词、账户或标签）。
2. 评估帖子的相关性（内容匹配度、作者影响力、互动程度）。
3. 对热门帖子进行互动（点赞、发表有意义的评论或分享）。
4. 避免重复互动。
5. 遵守发送频率限制（每次运行最多20-30次互动）。

**目标选择策略：**
- 来自特定公司/个人的帖子。
- 包含特定关键词/标签的帖子。
- 您联系人发布的帖子。
- 行业内的热门帖子。

**互动方式：**
- **点赞**：快速且不显眼的互动方式。
- **评论**：根据帖子内容自动生成的评论（不会显得像垃圾信息）。
- **分享**：在分享时附上您的观点或评论。

## 私信发送流程

每天运行 `scripts/dm-sequence.sh` 脚本。该脚本会：
1. 检查当前激活的私信发送序列。
2. 按顺序发送下一条消息（遵循预设的延迟时间）。
3. 检测回复情况并相应地调整发送策略。
4. 处理不同的回复情况（已回复或未回复）。
5. 提供发送频率的统计报告。

**私信发送序列示例：**
```json
{
  "name": "consulting-intro",
  "trigger": "new_connection",
  "steps": [
    {
      "delay_hours": 24,
      "message": "Hey {first_name}! Thanks for connecting. I help {title}s with {pain_point}. Are you currently working on anything in this space?",
      "condition": null
    },
    {
      "delay_hours": 72,
      "message": "Following up — I saw your post about {topic}. Would love to chat about {offering}. Free for a quick call this week?",
      "condition": "no_reply"
    }
  ]
}
```

## 连接请求流程

每周运行 `scripts/connect.sh` 脚本（LinkedIn限制每天发送次数）。该脚本会：
1. 搜索目标账户（职位标题、公司名称或关键词）。
2. 过滤掉已有的联系人和待处理的请求。
3. 生成个性化的连接请求备注。
4. 控制发送频率（每周最多20-30次）。
5. 记录请求的接受率。

**目标选择标准：**
```json
"connection_targets": [
  {
    "query": "AI consultant OR automation specialist",
    "companies": ["Microsoft", "Google", "OpenAI"],
    "exclude_titles": ["Recruiter"],
    "note_template": "Hey {first_name}, I'm building AI tools for {industry} and saw your work at {company}. Would love to connect!"
  }
]
```

## 安全与频率限制

LinkedIn Autopilot严格遵守发送频率限制，以避免账户被标记为机器人：

| 功能 | 限制 | 时间安排 |
|--------|-------|--------|
| **发布帖子** | 每天1-2次 | 最佳时间（上午9点至11点、下午2点至4点） |
| **互动** | 每天80-100次 | 分散在3-4次发送中 |
| **连接请求** | 每周20-30次 | 前两周逐步增加发送频率 |
| **私信** | 每天30-50条 | 发送之间有5-15分钟的随机延迟 |
| **页面浏览** | 每天50-80次 | 保持自然的浏览行为 |

**预热期：** 前两周以50%的发送频率运行，以建立正常的互动模式。

**禁售时段：** 夜间和周末不进行任何操作（可配置）。

**随机延迟：** 每次操作之间有3-8秒的延迟，不同任务之间有5-15分钟的间隔。

**模拟人类行为：** 互动时间随机变化，偶尔会暂停操作，保持自然的语言风格。

## 状态跟踪

所有操作都会被记录和跟踪：
```
~/.config/linkedin-autopilot/
├── config.json              # User configuration
├── posts-queue.json         # Scheduled posts
├── engagement-history.json  # Posts engaged with (dedup)
├── dm-sequences.json        # Active DM threads
├── connections.json         # Connection requests + status
├── analytics.json           # Performance metrics
└── activity-log.json        # Full audit trail
```

## 报告功能

`scripts/report.sh` 生成性能报告：

**每周总结：**
- 发布的帖子数量及 reach（曝光量）
- 执行的互动类型及数量
- 发送的连接请求（已发送、已接受、待处理）
- 私信发送序列（活跃状态、回复情况、转化结果）

**线索转化跟踪：**
- 私信回复 → 被视为合格线索。
- 连接请求被接受 → 成功的对话。
- 帖子互动 → 引起的兴趣。

## 示例使用场景

### 1. 建立行业意见领袖人脉
- 每天按计划发布一篇行业见解或经验分享。
- 自动与领域内的20-30个影响者互动。
- 分享他们的热门帖子，并附上您的评论。
- 分析哪些类型的内容能带来最多的页面浏览量。

### 2. 外部线索生成
- 每周与20-30个目标账户建立联系（例如A轮初创公司的CTO）。
- 对新联系人发送私信序列（介绍 → 价值主张 → 预约通话）。
- 在发送序列前自动与潜在客户的帖子互动。
- 报告回复率和预约成功率。

### 3. 人脉维护
- 对现有联系人发布的帖子进行点赞。
- 对关键账户的更新发表有意义的评论。
- 定期通过私信与他们保持联系（生日、工作纪念日、重要里程碑）。

## 遵守LinkedIn服务条款

**重要提示：** LinkedIn的服务条款禁止使用自动化工具。本工具仅用于：
1. **个人用途**，并在人类监督下使用（您需要审核和批准所有操作）。
2. **辅助工作流程**（助手提供建议，由人类最终决定）。
3 **批量调度**（批量准备内容，按计划发布）。

**推荐使用方法：**
- 使用 `--dry-run` 模式预览所有操作。
- 在启用自动发送前仔细检查队列中的内容。
- 设置合理的发送频率限制。
- 监控账户是否收到任何警告。
- 对于敏感操作，始终由人类参与决策。

本工具按现状提供，仅供学习用途，请谨慎使用。

## 数据文件

```
~/.config/linkedin-autopilot/
├── config.json              # Main configuration
├── posts-queue.json         # Scheduled content
├── engagement-history.json  # Activity dedup
├── dm-sequences.json        # Active conversations
├── connections.json         # Network building state
├── analytics.json           # Performance tracking
└── activity-log.json        # Full audit trail
```

## 浏览器自动化技术

该工具使用了Clawdbot内置的浏览器控制功能：
- 截取页面快照 → 执行操作 → 验证操作效果。
- 处理登录、二次验证（2FA）流程和会话管理。
- 在遇到发送频率限制时自动重试。
- 适应LinkedIn用户界面的变化。

## 高级功能

- **A/B测试**：测试不同的帖子内容，找出效果最好的方案。
- **智能调度**：基于机器学习推荐最佳发布时间。
- **回复检测**：在收到回复时暂停私信发送。
- **情感分析**：根据帖子的情感倾向调整互动策略。
- **人脉分析**：追踪哪些人会与您的内容互动（潜在的支持者）。

## 故障排除

**“LinkedIn安全检查触发”**  
→ 降低配置中的发送频率限制，延长发送间隔，手动完成安全验证。

**“帖子无法发布”**  
→ 检查 `activity-log.json` 文件中的错误信息，确认LinkedIn会话是否有效。

**“私信发送序列无法继续”**  
→ 确认回复检测功能是否正常工作，检查 `dm-sequences.json` 文件中的对话状态。

**“连接请求频繁被拒绝”**  
→ 提高备注的个性化程度，优化目标账户的选择，减少发送频率。

## 贡献建议

想要添加新功能？请参考 `references/linkedin-api.md` 了解浏览器自动化的相关技术，以及 `references/sequence-engine.md` 了解私信发送的逻辑实现。

---

**记住：** 这个工具是您的助力工具，而非替代真实的人际网络建设。利用它来处理繁琐的任务，让您能够专注于真正重要的对话和交流。