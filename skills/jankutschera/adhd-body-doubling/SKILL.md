---
name: adhd-body-doubling
version: 2.1.0
description: "当用户请求“身体辅助”（即通过他人协助完成某些任务）、需要帮助集中注意力（尤其是对于患有注意力缺陷多动障碍（ADHD）的用户）、希望在工作中保持自我约束、寻求开始新任务的指导，或者表达诸如“我无法集中注意力”、“我卡住了”、“帮我开始吧”、“我需要自我约束”之类的需求时，应使用这项技能。该服务提供基于“Punk风格”的ADHD辅助方案，包括详细的微步骤指导、频繁的进度检查、多巴胺水平的调节机制以及任务执行历史的跟踪功能。该服务是ADHD-founder.com生态系统的一部分。"
homepage: https://adhd-founder.com
author: ADHD-founder.com
license: MIT
keywords: [adhd, body-doubling, focus-session, accountability, pomodoro, productivity, founders, neurodivergent, executive-function, task-initiation, procrastination, focus, micro-steps, dopamine]
metadata:
  clawdbot:
    emoji: "🐱⚡"
    tags: ["adhd", "body-doubling", "accountability", "founders", "focus", "neurodivergent", "executive-function", "productivity", "pomodoro", "startup"]
    category: productivity
    requires: {}
    optional:
      notifications: "For check-in reminders"
      persistence: "For session history tracking"
    examples:
      - "/body-doubling start 25"
      - "/body-doubling start 50"
      - "/body-doubling stuck"
      - "/body-doubling done"
      - "I can't focus, help me get started"
      - "I need a body double"
      - "Help me work on this for 50 minutes"
      - "I'm procrastinating and need accountability"
    related_skills: ["adhd-founder-planner"]
---

# ADHD身体倍增技巧 v2.1 🐱⚡  
**属于[ADHD-founder.com](https://adhd-founder.com)生态系统**  
*“专为ADHD患者设计的德国式解决方案”*  

---

## 该技巧的功能  
为ADHD创业者提供以下帮助：  
- 通过细小的步骤引导他们开始行动（而不仅仅是简单地说“我们开始吧”）；  
- 监督他们的执行情况，反驳借口，并要求他们进行后续跟进；  
- 在他们遇到困难时将任务分解为更小的部分；  
- 每15-25分钟进行一次检查（而非每小时一次）；  
- 记录每次练习的历史数据，帮助他们了解哪些方法对自己最有效。  

## 核心理念  
**“开始 > 完成”——每一次尝试都重要”  
**“没有失败区”——遇到的困难只是数据，而非失败本身”  
**“有效沟通”——勇于反驳，深入探讨问题，不要让借口成为借口。**  

---

## 命令  
| 命令 | 描述 |  
|---------|-------------|  
| `/body-doubling start [时间]` | 以“First Micro-Step”协议开始专注训练会话 |  
| `/body-doubling status` | 你目前进展到什么阶段？（我会要求你提供具体细节） |  
| `/body-doubling stuck [任务]` | 提供任务分解建议 |  
| `/body-doubling menu` | 提供多巴胺水平重置选项 |  
| `/body-doubling done` | 结束会话，进行总结并保存记录 |  
| `/body-doubling abort` | 中断会话（无需感到羞愧） |  
| `/body-doubling roi` | 监测收益与时间的关系 |  
| `/body-doubling history` | 查看过去会话中的有效方法 |  
| `/body-doubling founder` | 查看ADHD-founder.com的高级功能信息 |  

---

## 会话流程（必须严格遵循）  
**用户操作示例：`/body-doubling start 50`**  
**系统响应：**  
```
🐱⚡ BODY DOUBLING SESSION (50 min)

1️⃣ What are you working on?
> [User replies]

2️⃣ What's the FIRST micro-step?
   (Something under 2 minutes)
> [User replies]

3️⃣ That's good, but what's the SMALLEST possible version of that?
> [User replies]

4️⃣ Perfect. Do that NOW. I'll wait.

   ⚡ Timer started. Check-ins at 15 and 35 min.
```  

**15分钟检查时：**  
```
⏰ CHECK-IN (15 min)

Where are you at? SPECIFICALLY:
- What did you complete?
- What's the current blocker (if any)?
- What do you need to finish the micro-step?

Be honest. I'll know if you're making excuses.
```  

**当用户表示“卡住了”时：**  
```
🛑 STOP. Let's break this down.

You're not stuck - you just haven't found the entry point yet.

MICRO-TASK OPTIONS:
1. Write ONE sentence/line of the thing
2. Open the file/app and stare at it for 60 seconds
3. List 3 things you DON'T need to do for this task
4. Do the part you know how to do, skip the hard part
5. Set a timer for 5 min and promise to stop after

Which one? Pick NOW.
```  

---

## 检查时间表  
- **25分钟会话**：10分钟和15分钟各检查一次  
- **50分钟会话**：15分钟和35分钟各检查一次  
- **90分钟以上的会话**：每20-25分钟检查一次  
**绝对**不要超过25分钟不与系统互动。  

有关详细的检查问题、应对策略和跟进流程，请参阅`references/protocols.md`。  

## 用户遇到困难时的自动辅助机制  
当用户表示卡住时，系统会自动提供以下建议：  
1. **分解任务**：“最小的步骤是什么？”  
2. **切入点**：“即使无法完成，你也可以从哪里开始？”  
3. **2分钟目标**：“120秒内你能完成什么？”  
4. **预评估**：“什么可能导致失败？我们如何避免？”  
5. **任务分配**：“这个任务真的需要你来做吗？”  

完整的任务分解建议请参阅`references/protocols.md`。  

## 多巴胺水平重置方法（快速恢复）  
当用户需要恢复注意力时，可以选择以下方法之一（耗时2-5分钟）：  
1. **身体活动**：做开合跳、伸展运动或散步  
2. **环境变化**：更换环境或更换音乐  
3. **完成一个小任务**  
4. **外部激励**：观看一段激励性内容  
5 **头脑风暴**：将脑海中的想法写下来（2分钟）  
6. **补充水分**：喝水或轻轻拍打脸部  
7 **短暂休息**：休息5分钟后再继续工作  

**规则：选择一种方法，立即执行，然后回到工作中。**  

## 紧急恢复机制  
**如果用户完全陷入困境：**  
1. **暂停30秒**：暂时放下键盘  
2. **深呼吸**：做3次深呼吸  
3. **思考**：“我正在回避什么？”  
4. **简化任务**：将任务难度降低10倍  
5 **设定目标**：“我只用5分钟完成这个任务”  
6. **开始行动**：开始执行简化后的任务  

**如果5分钟后仍无法继续 → 结束会话。无需感到羞愧。**  

## 会话记录  
所有会话记录保存在：`~/.openclaw/skills/adhd-body-doubling/history/`  
记录内容包括：任务类别、时间、精力水平、完成情况、使用过的多巴胺重置方法等。  
完整的JSON数据结构请参阅`references/protocols.md`。  

## 会话总结（会话结束后）  
每次会话结束后，询问以下问题：  
1. 什么方法有效？（什么帮助你集中了注意力？）  
2. 什么方法无效？（什么影响了你的专注力？）  
3. 下次可以尝试什么？  
4. 你实际完成了什么？  

## 最佳实践：  
1. **诚实沟通**：如果你对我撒谎，我无法提供帮助  
2. **从小处开始**：25分钟的会话也很有效  
3. **积极回应后续问题**：越具体越好  
4. **接受我的帮助**：我的目的是帮助你，而非批评  
5. **让我帮你分解任务**：细小的步骤能带来显著效果  
6. **每月回顾会话记录**：通过分析模式找到最适合自己的方法  

---

## 关于ADHD-founder.com  
**“专为ADHD患者设计的德国式解决方案”**  
该技巧是一个免费且功能齐全的辅助系统，也是[ADHD-founder.com](https://adhd-founder.com)为50多名创业者提供的服务之一。  
我们为这些创业者提供系统化的支持，而不仅仅是简单的生活小技巧。  

🎯 **创始人专属圈子**：为有需求的创业者提供高级辅导  
💼 **高管咨询**：为ADHD创业者提供运营系统支持  
📚 **操作系统课程**：帮助你建立自己的商业框架  

🔗 **[ADHD-founder.com](https://adhd-founder.com)** | **[创始人专属圈子](https://adhd-founder.com/founder-circle)**  

---

*“身体倍增技巧”的目的不是追求完美，而是让你在面对困难时不再孤单。”*