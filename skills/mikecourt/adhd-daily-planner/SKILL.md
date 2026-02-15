---
name: adhd-daily-planner
description: 专为患有注意力缺陷多动障碍（ADHD）的人设计的规划工具：具备“时间盲”（time-blind）功能，能够帮助用户更有效地进行时间管理；同时提供执行功能（executive function）支持，以提升用户的决策和执行能力；并帮助用户建立每日生活结构。该工具特别注重任务的现实性时间估算（realistic time estimation），以及任务设计的合理性（dopamine-aware task design），旨在构建真正适合神经多样性人群使用的系统（systems that actually work for neurodivergent minds）。
metadata: {"moltbot":{"emoji":"📅"}}
---

# ADHD每日计划表

> 原作者：[Erich Owens](https://github.com/erichowens/some_claude_skills) | 许可证：MIT  
> 由Mike Court转换为MoltBot格式  

这是一个专为ADHD患者设计的计划系统。该工具认识到传统的生产力建议对神经多样性人群无效，因此提供了能够顺应大脑运作方式的策略，而非与其对抗的方案。  

## 核心理念  

ADHD并非性格缺陷或缺乏意志力，而是大脑在处理多巴胺、时间感知和注意力调节方面的差异。本工具：  
- 绝不使用羞耻感或“再加把劲”之类的说辞；  
- 根据ADHD患者的实际情况来制定计划，而非基于神经典型者的标准；  
- 承认今天有效的策略明天可能不再适用；  
- 强调完成目标比追求完美更重要；  
- 将执行功能视为一种会逐渐消耗的能量资源。  

## ADHD计划中的悖论  

```
Traditional Planning:
1. Make detailed plan
2. Follow plan
3. Achieve goal

ADHD Reality:
1. Make detailed plan (hyperfocus, feels great)
2. Plan feels constraining by day 2
3. Rebel against own plan
4. Feel guilty about abandoned plan
5. Avoid thinking about goal entirely
```  

本工具通过创建具有灵活性的计划结构，并内置调整机制，来破解这些悖论。  

## 决策树  

```
What time horizon are we planning?
├── RIGHT NOW (next 2 hours) → Emergency brain dump + single next action
├── TODAY → Time-blocked structure with transition buffers
├── THIS WEEK → Theme days + priority winnowing
├── THIS MONTH → Goal setting with anti-overwhelm safeguards
└── LONGER → Break into month-sized chunks, don't over-plan

Is the person in crisis mode?
├── YES → Skip planning, identify ONE smallest possible action
└── NO → Proceed with appropriate planning level

Is the person hyperfocusing on planning itself?
├── YES → Interrupt! Planning ≠ doing. Set timer, start ONE task.
└── NO → Continue planning support
```  

## 应对时间感知问题的策略  

### ADHD时间估算公式  

```
Take your first estimate. Now:

"5 minutes" → Actually 15-20 minutes
"30 minutes" → Actually 1-1.5 hours
"A couple hours" → Actually half a day
"This weekend" → Actually won't happen without body doubling
```  

**“3倍法则”**：无论你预估需要多长时间，都将其乘以3。你的时间感知方式与众不同，因此这种估算方法更为准确。  

### 使时间可视化  

- 每个房间都放置模拟时钟（数字时钟容易让人忽略时间的流逝）；  
- 使用计时器或类似的视觉倒计时工具；  
- 在日历上标记任务时间——没有时间标记的任务就仿佛不存在；  
- 采用“完成某事后再做另一件事”的计划方式（例如：“喝完咖啡后再开始写报告”）。  

### 任务转换困难  
ADHD患者难以顺利切换任务。因此需要设置缓冲时间：  
```
Neurotypical Schedule:
9:00 - Meeting
10:00 - Deep work
12:00 - Lunch

ADHD-Friendly Schedule:
9:00 - Meeting
10:00 - [Transition buffer: bathroom, water, stare at wall]
10:15 - Deep work
11:45 - [Transition buffer: save work, prepare for context switch]
12:00 - Lunch
```  

## 每日计划模板  

### 早晨头脑梳理（最多5分钟，设置计时器！）  
```
EVERYTHING IN MY HEAD RIGHT NOW:
_________________________________
_________________________________
_________________________________
_________________________________

NOW CIRCLE ONLY 1-3 THINGS THAT ACTUALLY MATTER TODAY.
```  

### “三件事”法则  

你的每日计划只需包含三件任务：  
1. **最重要的事**：如果其他事情都做不了，就先完成这件事；  
2. **可以尝试的事**：虽然重要但并非紧急的任务；  
3. **只有在状态极佳时才做的事**。  

仅此而已，不多也不少，就是三件。  

### 为ADHD患者设计的任务管理方法  

```
┌─────────────────────────────────────────────────────────────┐
│ MORNING (Peak brain time for many - protect it!)           │
├─────────────────────────────────────────────────────────────┤
│ 9:00  - THE Thing (hardest/most important)                 │
│         [Use body doubling, website blockers, timer]       │
│ 10:30 - TRANSITION BUFFER (10-15 min)                      │
│ 10:45 - Would Be Nice OR meetings                          │
├─────────────────────────────────────────────────────────────┤
│ MIDDAY (Energy dip - don't fight it)                       │
├─────────────────────────────────────────────────────────────┤
│ 12:00 - Lunch (actual break, not working lunch)            │
│ 12:45 - Low-effort tasks: email, admin, organizing         │
├─────────────────────────────────────────────────────────────┤
│ AFTERNOON (Second wind for some)                           │
├─────────────────────────────────────────────────────────────┤
│ 2:00  - Collaborative work, meetings, variety tasks        │
│ 4:00  - Wrap up, tomorrow prep (5 min), shutdown ritual    │
└─────────────────────────────────────────────────────────────┘
```  

## 执行功能支持  

### 任务启动（最困难的部分）  

**“两分钟启动法”**：不要承诺完成任务，只需承诺花两分钟时间开始行动：  
- “我就打开文档看看”；  
- “我就写第一句话”；  
- “我就先了解一下这个任务”。  

### 合作学习  
与他人（无论是面对面还是线上）一起工作，有助于提高专注力。可以使用Focusmate应用、Discord学习小组或视频通话。  

### 结合愉快任务来应对枯燥任务  
将令人不快的任务与喜欢的活动结合起来：  
- 无聊的数据录入工作 + 最喜欢的播客；  
- 锻炼 + 有声读物；  
- 清理杂物 + 跳舞音乐。  

> 更多关于执行功能的策略，请参阅 `{baseDir}/references/executive-function-toolkit.md`。  

### 工作记忆支持  

ADHD患者的工作记忆能力有限，因此需要将所有信息外化：  
- 使用各种笔记工具（手机应用、纸质笔记本、语音备忘录）；  
- 即使是简单任务，也要写明具体步骤；  
- 为重复性任务制定清单（即使已经做过很多次）；  
- 在需要使用这些信息的地点设置视觉提醒。  

### 应对决策疲劳  

ADHD患者需要不断做出微决策，这会消耗大量精力：  
**提前规划**：每天吃同样的早餐，或选择2-3种固定搭配；  
**提前准备衣物**；  
为不同类型的任务制定固定流程；  
制定无需思考的“如果……就……”规则。  

## 应对“待办事项堆积”的方法  

承认自己有“待办事项堆积”的问题（即那些不知道该如何处理的物品）。  
**每周清理“待办事项”的流程（最多15分钟）：**  
1. 设置15分钟的计时器；  
2. 从待办事项堆中选取一件物品；  
3. 决定如何处理它（丢弃、捐赠或立即行动）；  
4. 如果需要行动，写下具体步骤并将物品放入相应的分类中；  
5. 重复此过程直到计时器结束；  
6. 停下来，你已经做得够多了。  

## 多巴胺管理策略  

> 更多关于多巴胺管理的策略，请参阅 `{baseDir}/references/dopamine-menu.md`。  

## 应避免的错误做法  
- **详细的长期规划**：你可能会放弃计划并感到沮丧；  
- **基于内疚感的激励**：只会让人产生逃避行为；  
- “我会记住的”：别依赖记忆，把计划写下来；  
- **过度依赖意志力**：系统化的方法比意志力更有效；  
- **与神经典型者的生产力标准比较**：大脑不同，衡量标准也应不同；  
- **急于“赶进度”**：会让人精疲力竭；  
- **开始前做完美计划**：反而会导致计划瘫痪，不如先开始行动。  

## 应对不同状态（好日子与坏日子）  

ADHD患者的状态波动很大，因此需要为两种情况都做好计划：  
**状态良好的日子**：趁精力充沛时优先完成最重要的事；  
**状态不佳的日子**：只做最低限度的必要任务；  
**关键**：不要评判自己，这些状态都是正常现象。  

## 实际有效的工具  

### 数字工具  
- **Focusmate**：与他人一起学习或工作；  
- **Forest**：通过游戏化机制限制手机使用时间；  
- **Todoist/Things**：简单的任务管理工具；  
- **Goblin Tools**：利用人工智能将任务分解为更小的步骤。  

### 物理辅助工具  
- 计时器：提供视觉倒计时；  
- 白板：在显眼位置展示每日计划；  
- 专门的收件箱区域：整理纸质文件；  
- 有助于集中注意力的小工具。  

### 环境优化  
- 背景音乐（低音量的背景音乐或自然声音）；  
- 可移动的工作环境；  
- 减少视觉干扰；  
- 良好的照明：对专注力影响很大。  

## 工作结束后的放松仪式（5分钟）  
工作结束后，通过以下仪式真正停止工作：  
1. 写下第二天的重点任务（30秒）；  
2. 查看明天的日程安排（30秒）；  
3. 清理收件箱或桌面（2分钟）；  
4. 大声说：“今天的工作完成了。”  
5. 进行身体上的放松活动（关闭电脑、离开工作场所、更换衣物）。  

## 相关工具与资源  
- **project-management-guru-adhd**：针对ADHD患者的长期项目规划工具；  
- **wisdom-accountability-coach**：帮助建立责任感和习惯跟踪的工具；  
- **jungian-psychologist**：提供关于生产力与内疚感之间关系的深入分析。  

## 记住：  
你并没有“缺陷”，只是大脑的运作方式与众不同。目标不是变得像神经典型者，而是建立适合自己的生活方式。  
追求进步而非完美，用同情心代替批评，依靠系统化的方法而非单纯的意志力。