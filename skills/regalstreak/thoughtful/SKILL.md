---
name: thoughtful
description: 您在 WhatsApp 中的贴心伴侣——它会记住重要的信息，帮助您更好地维系人际关系。
metadata: {"openclaw":{"emoji":"💭","requires":{"bins":["wacli-readonly"]}}}
---

# Thoughtful

**您的贴心WhatsApp助手。**

它不仅仅提供简单的消息摘要，还能帮助您维护人际关系，发现那些容易被忽视的细节，并以有意图的方式与他人交流，而不仅仅是被动回应。

## 功能介绍

### 📊 智能跟踪
- **待办事项**：来自任何对话中的行动项，会一直跟踪直到完成
- **等待回复**：您询问过的事情，正在等待回复
- **承诺**：您做出的承诺以及提到的截止日期
- **关系动态**：情绪变化、回复模式、沉默的对话
- **重要日期**：聊天中提到的生日、活动、截止日期
- **决策**：您做出的决定，可能需要记住的事项

### 🧠 沟通辅导
作为您的情商助手，它可以帮助您：
- 发现需要回复或解决未完成的事情
- 注意到关系中的语气或情绪变化
- 找到合适的时机进行问候或表达感谢
- 重新开启沉默的对话，避免尴尬
- 保持主动，而不是被动反应

### 📝 每日总结
以温暖、像朋友一样聊天的方式为您提供总结，而不是机械的清单。

**包含内容：**
- 新消息（过去24小时）
- 仍未完成的事项（几天/几周前）
- 关系洞察
- 建议的对话开场白
- 沟通提示

## 数据存储
所有数据存储在：`${WORKDIR}/thoughtful-data/`（默认为`~/clawd/thoughtful-data/`）

```
thoughtful-data/
├── config.json          # Your preferences
├── state.json           # Processing state
├── tasks.json           # Pending items, commitments, waiting-on
├── people.json          # Relationship tracking per contact
├── summaries/           # Historical summaries
└── context/             # Conversation context per chat
```

## 配置

**推荐交互式设置：**
首次使用该功能时，助手会通过聊天引导您完成设置：
- 要跟踪的WhatsApp群组（显示列表，您可以选择）
- 始终需要重点关注的联系人
- 总结发送的时间偏好
- 启用/禁用跟踪功能

所有配置都通过聊天完成，无需手动编辑文件。

**高级手动配置：**
编辑 `${WORKDIR}/thoughtful-data/config.json`以：
- 向白名单中添加/删除群组
- 标记重点联系人
- 调整跟踪偏好
- 设置总结发送时间

## 沟通辅导提示
该功能采用以下框架（灵感来自“littlebird”）：

> **作为一位富有同理心的沟通导师，提供实用且富有情商的建议。**
>
> 帮助您改善与同事、朋友之间的沟通：
>
> 1. **反思互动**：是否有未完成的事情？语气是否发生了变化？
> 2. **建议问候时机**：何时是合适的联系或表达感谢的时机
> 3. **提供对话开场白**：有助于重新开启对话的提示
> 4. **重新开启对话的指导**：如何优雅地重新开启沉默的对话
>
> **语气：** 清晰、温暖且直接。没有冗余信息，也不会显得机械。非常实用。

## 工作原理

### 数据收集
1. 从`wacli-readonly`获取消息（过去24小时及更早的待办事项）
2. 仅处理私信和白名单中的群组
3. 提取行动项、情绪、承诺和日期
4. 更新跟踪文件

### 分析与洞察
使用大型语言模型（LLM）来：
- 理解对话内容和语气
- 判断哪些事情需要关注，哪些可以稍后处理
- 识别关系中的模式（例如某人是否感到沮丧、对话是否变得沉默）
- 提供合适的回复和建议

### 总结生成
生成温暖的、人性化的总结，包括：
- **新消息**：最新的消息和待办事项
- **仍未完成的事项**：尚未完成的老任务
- **关系洞察**：例如“Alice已经询问了3次，可能感到沮丧”
- **建议的行动**：例如“现在是与Bob联系的好时机”
- **对话开场白**：您可以发送的具体提示

### 交互式任务管理
总结中包含以下按钮：
- ✅ 标记任务已完成
- ⏭️ 仍待处理
- ❌ 不要处理
- 💬 草稿回复

## 示例总结

```
Morning, Neil! ☀️

Here's your WhatsApp catch-up:

🆕 WHAT'S NEW (last 24h):

**Alice is waiting on you** (3 messages)
She's asked about Tuesday's meeting twice now and sent a restaurant link. 
Feels time-sensitive - she mentioned "need to know by tonight."

**Bob's getting urgent** (2 messages)
Those design files he asked for? Now needs them "before EOD." 
This has been pending for 2 days.

**House party group** (12 messages)
Weekend plans firming up. They're organizing who brings what.
Not urgent, but you might want to check in before Saturday.

⏰ STILL PENDING:

- Confirm Tuesday meeting - Alice (**5 days old**, asked 3x)
- Send design files - Bob (urgent, 2 days old)
- Review contract - Lawyer (low priority, 1 week old)

💡 COMMUNICATION INSIGHTS:

**Relationships that need attention:**
- Alice: Tone shifted from casual to "please let me know" - 
  she might be frustrated you haven't confirmed yet
- Bob: This is the second follow-up - shows it's important to him

**Quiet conversations worth reviving:**
- Haven't heard from Priya in 2 weeks (you asked about her project)
- Charlie went quiet after you said you'd think about his idea

📝 SUGGESTED ACTIONS:

**For Alice:**
"Hey! Sorry for the delay - yes, Tuesday works. That restaurant 
looks perfect, let's do 7pm?"

**For Bob:**
"On it - will have files to you by 3pm today. Thanks for the patience!"

**For Priya (re-engage):**
"Hey Priya! Been thinking about that project you mentioned - 
how's it going?"

Did you complete: "Confirm Tuesday meeting with Alice"?
[✅ Done] [⏭️ Still pending] [❌ Won't do] [💬 Draft reply]
```

## 首次设置

当用户首次安装该功能时，引导他们完成以下交互式设置：

1. **认证wacli-readonly**
   - 运行 `wacli-readonly auth --qr-file /tmp/whatsapp-qr.png`（在沙箱环境中）
   - 将二维码图片发送给用户
   - 等待认证确认

2. **列出可用群组**
   - 运行 `wacli-readonly groups list`（在沙箱环境中）
   - 显示用户的WhatsApp群组
   - 询问哪些群组需要包含在总结中

3. **配置偏好**
   - 询问重点联系人
   - 确认总结发送时间（默认：每天上午11点）
   - 确认跟踪功能（情绪、承诺等）

4. **创建定时任务**
   - 设置WhatsApp同步定时任务（上午10:30，独立会话）
   - 设置每日总结定时任务（上午11:00，独立会话）
   - 确认两项任务都已正确安排

5. **测试运行**
   - 生成第一个总结以验证设置是否正确
   - 通过Telegram发送总结

## 使用方法

**重要提示：所有与Thoughtful相关的操作都在沙箱环境中进行。**

生成总结时：
1. 使用`thoughtful`技能
2. 在沙箱环境中运行脚本：`exec~/clawd/skills/thoughtful/scripts/generate-summary.sh", {host: "sandbox"}`
3. 从`thoughtful-data/context/last-prompt.txt`中读取生成的提示
4. 使用OpenClaw的大型语言模型生成总结
5. 通过当前渠道发送总结

该功能将：
- 从`wacli-readonly`获取消息（在沙箱环境中）
- 处理和分析对话
- 使用OpenClaw的大型语言模型生成总结
- 跟踪任务和关系洞察
- 以温暖、聊天的方式发送总结

## 定时任务设置

**重要提示：**
- **始终使用`sessionTarget: "isolated"`**——确保任务独立运行
- **切勿使用`sessionTarget: "main"`**——否则可能导致功能无法正常工作
- 所有操作都在沙箱环境中进行
- **共有两个定时任务：**同步和总结，每天各运行3次
- **同步任务在每个总结生成前30分钟运行**，以确保数据是最新的

### WhatsApp同步（每天3次）
时间：上午10:30、下午5:30、晚上10:30
```json
{
  "name": "wacli-sync-daily",
  "schedule": {"kind": "cron", "expr": "30 10,17,22 * * *", "tz": "Asia/Calcutta"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run WhatsApp sync:\n\n1. Kill any stuck wacli processes: `pkill -9 wacli-readonly` (sandbox)\n2. Run `wacli-readonly sync` in sandbox (let it complete)\n3. Report: 'WhatsApp sync completed' or any errors",
    "deliver": true,
    "channel": "telegram",
    "to": "-1003893728810:topic:38"
  }
}
```

### 总结发送（每天3次）
时间：上午11:00、下午6:00、晚上11:00
```json
{
  "name": "thoughtful-daily",
  "schedule": {"kind": "cron", "expr": "0 11,18,23 * * *", "tz": "Asia/Calcutta"},
  "sessionTarget": "isolated",
  "payload": {
    "kind": "agentTurn",
    "message": "Run thoughtful summary:\n\n1. Kill any stuck wacli processes: `pkill -9 wacli-readonly` (sandbox)\n2. Run `~/clawd/skills/thoughtful/scripts/generate-summary.sh` in sandbox\n3. Read the generated prompt from `thoughtful-data/context/last-prompt.txt`\n4. Create a warm, thoughtful summary following the communication coach framework\n5. Deliver via Telegram to Clawdgroup topic",
    "deliver": true,
    "channel": "telegram",
    "to": "-1003893728810:topic:38"
  }
}
```

**为什么每天发送3次？**
- 全天候捕获消息，不错过任何重要更新
- 上午（11点）：让您开始新的一天时了解最新情况
- 下午（6点）：及时了解下午的对话
- 晚上（11点）：睡前回顾一天的事情

**为什么分开进行同步和总结？**
- WhatsApp同步可能需要时间，需要最新数据才能进行分析
- 30分钟的间隔确保同步完成后再进行总结生成
- 使用逗号分隔的时间格式使设置简单（总共2个定时任务）

**注意：**助手会在首次设置时自动完成这些配置。用户可以在设置过程中调整时间。

## 隐私与安全

- 所有数据本地存储在`~/clawd/whatsapp/`
- `wacli-readonly`数据库存储在`~/.wacli`（只读，不发送数据）
- 除了用于生成总结的OpenClaw大型语言模型外，不使用任何外部服务
- 所有操作都在沙箱环境中进行，以确保安全隔离

## 跟踪功能说明

### 情绪趋势
检测某人的语气是否发生变化：
- “感到沮丧”（多次跟进、消息变短）
- “变得沉默”（发送频率降低、回复变短）
- “更加活跃”（消息变长、提出问题）

### 回复时间模式
跟踪您通常对每个人回复所需的时间：
- 帮助您发现是否对某人的回复速度比平时慢
- 提示您可能被注意到延迟

### 重复出现的主题
识别常见的模式：
- “Bob总是在周五询问项目进度”
- “Alice总是在晚餐计划前发送餐厅链接”

### 承诺跟踪
提取您做出的承诺：
- “我会在周二之前发送”
- “让我考虑一下再回复你”
- “我会查看后告诉你”

标记您是否没有履行这些承诺。

### 重要日期
捕捉到以下内容的提及：
- 生日、纪念日
- 截止日期、活动日期
- “下周”、“月底”等

### 决策跟踪
记住您做出的选择：
- “我们决定选择A选项”
- “我决定不参加”
- “我们约定在晚上7点见面”

帮助您保持一致性，避免日后自相矛盾。

## 优化使用效果的技巧

1. **谨慎添加群组到白名单**——只添加您真正关心的群组
2. **标记重点联系人**——重要联系人会始终显示在总结中
3. **每天查看总结**——主动完成任务有助于保持跟踪的准确性
4. **使用对话开场白**——它们会根据您的实际对话情境进行定制
5. **根据关系洞察采取行动**——定期问候可以预防更大的问题

## 设计理念

这并不是关于提高效率或清空收件箱的工具。它的目的是让您的数字沟通更加人性化：
- **记住对他人重要的事情**
- **在关系中保持一致性**
- **有意图地沟通**，而不仅仅是被动回应
- **在问题变得严重之前发现小问题**

您的人际关系值得更好的沟通方式。这个工具能帮助您成为您希望成为的那种沟通者。