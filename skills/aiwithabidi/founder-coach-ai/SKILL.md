---
name: founder-coach
description: AI founder coaching system — daily decision journal, accountability tracking, weekly strategy reviews, and AI-era specific questions on moat, commoditization risk, and outcome-based pricing. Not generic startup advice. Use for founder productivity, decision tracking, and strategic reflection.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: OpenClaw agent with cron jobs
metadata: {"openclaw": {"emoji": "\ud83c\udfaf", "homepage": "https://www.agxntsix.ai"}}
---

# 创始人教练 🎯  
**专为人工智能时代的创始人设计的责任管理体系。**  
这套系统为创始人提供了结构化的辅导框架，包括每日检查、决策记录、每周战略回顾以及责任追踪——所有内容都存储在您的智能助手（agent）的记忆中。  

## 快速入门  
```bash
# Morning check-in
python3 {baseDir}/scripts/founder_checkin.py morning

# Evening reflection
python3 {baseDir}/scripts/founder_checkin.py evening

# Weekly review
python3 {baseDir}/scripts/founder_checkin.py weekly

# View stats
python3 {baseDir}/scripts/founder_checkin.py stats

# View recent entries
python3 {baseDir}/scripts/founder_checkin.py history --days 7
```  

---

## 🌅 早晨简报模板  
每天早晨使用此模板来规划您的一天：  

### 1. 昨天回顾  
- 我昨天承诺了什么？  
- 实际完成了哪些任务？（完成率）  
- 哪些任务延续到了今天，原因是什么？  

### 2. 今天的三大优先事项  
| 序号 | 优先级 | 重要性 | 时间安排 |  
| --- | --- | --- | --- |  
| 1 | | | |  
| 2 | | | |  
| 3 | | | |  

**规则：** 如果你今天只能完成一件事，那就选择这件事作为优先事项（即第1项）。  

### 3. 人工智能时代创始人的每日思考问题  
选择其中一个问题进行反思：  
- “有哪些手动流程可以由人工智能来替代？”  
- “我们的竞争优势在哪里？是数据、工作流程、分销渠道，还是品牌？”  
- “我们的每用户成本是多少？如何将其减半？”  
- “我们正在开发的产品或功能，是否会被GPT等AI工具在下一个季度取代？”  
- “如果是一家拥有10名员工的、完全基于人工智能的公司，他们会如何做？”  

---

## 🌙 晚间反思模板  
### 成功之处  
- 今天有哪些事情做得好？  
- 我为哪些成果感到自豪？  

### 失败之处  
- 有哪些事情没有实现？原因是什么？  
- 如果再做一次，我会怎么做不同？  

### 明天的计划  
- 明天的三大优先事项  
- 需要停止做的事情  
- 需要开始做的事情  

### 能量评估  
用1-5分评估自己的精力、专注度和动力水平：  

---

## 📊 每周战略回顾  
每周日或周一进行，耗时30-60分钟。  

### 绩效评估  
- 本周的承诺：___  
- 履行的承诺：___（完成率：___%）  
- 与上周相比：上升 / 不变 / 下降  

### 关键指标  
| 指标 | 上周 | 本周 | 目标 |  
| --- | --- | --- | --- |  
| 收入 | | | |  
| 用户/客户数量 | | | |  
| 关键功能进展 | | | |  
| 每用户成本 | | | |  

### 战略性问题  
#### 竞争优势分析  
- **数据优势**：我们是否积累了独有的数据？  
- **工作流程优势**：我们是否融入了客户的工作流程？  
- **分销渠道优势**：我们是否拥有自己的销售渠道、社区或品牌？  
- **执行速度优势**：我们的交付速度是否比竞争对手更快？  

#### 商品化风险  
- 我们的技术栈中哪些部分正在变得容易被复制？  
- 如果GPT-5、Claude 4或Gemini 3等AI工具出现，我们会受到什么影响？  
- 我们是否依赖于可能成为竞争对手的API？  

#### 人工智能时代的经济学  
- **每用户成本**：服务一位客户需要多少成本？  
- **基于成果的定价**：我们能否根据实际成果收费？  
- **边际成本**：第1000位客户的成本是否与第1位客户相同？  
- **人工智能带来的效率提升**：人工智能在哪些方面能帮助我们提高效率10倍？  

### 本周做出的决策  
| 决策 | 背景 | 考虑的选项 | 选择 | 是否可撤销？ |  
| --- | --- | --- | --- | --- |  
| | | | | |  

### 下周计划  
- 第1优先事项（必须完成）：  
- 第2优先事项（应该完成）：  
- 第3优先事项（可选择性完成）：  
- 一个值得尝试的实验：  

---

## 📓 决策记录格式  
对于重要的决策，请使用以下格式进行记录：  
```
## Decision: [Title]
Date: YYYY-MM-DD
Stakes: Low / Medium / High / Critical

### Context
What's the situation? Why does this decision need to be made now?

### Options
1. **Option A:** [description]
   - Pro: ...
   - Con: ...
   - Cost: ...

2. **Option B:** [description]
   - Pro: ...
   - Con: ...
   - Cost: ...

### Decision
Chose: [Option X]
Reasoning: [Why]
Reversible: Yes/No
Review date: [When to check if this was right]

### Outcome (fill in later)
Date reviewed:
Result:
Lesson:
```  

---

## 📈 责任管理体系  
### 运作方式  
1. **早晨**：设定3项承诺。  
2. **晚上**：标记任务的完成情况，并附上备注。  
3. **每周**：回顾完成情况并分析规律。  
4. **每月**：识别系统性问题。  

### 评分标准  
- **完成率90-100%**：表现优异或目标设定过于简单。  
- **70-89%**：处于合理范围内。  
- **50-69%**：可能过度承诺或执行存在问题。  
- **低于50%**：需要暂停，减少承诺数量，专注完成1-2项任务。  

### 需要注意的规律  
- **第3项任务总是未完成**：可能是因为过度承诺，或者这些任务并不重要（应予以剔除）。  
- **同一任务反复出现**：要么是因为其重要性较低（应削减），要么是因为你在刻意回避它（原因是什么？）  
- **完成率高但无进展**：可能是因为忙于无关紧要的事情，导致效率低下——需要重新调整优先级。  
- **精力始终较低**：可能存在职业倦怠的风险，需及时休息。  

---

## 🤖 人工智能时代创始人问题库  
在早晨简报中轮流讨论这些问题：  

### 产品与竞争优势  
1. 如果人工智能能完成80%的工作，我们的业务会变成什么样？  
2. 我们是否只是API的简单包装？如何创造真正的价值？  
3. 我们创造了哪些独有的数据或反馈循环？  
4. 如果OpenAI在明天开发了我们的功能，哪些部分仍会属于我们？  

### 经济学方面  
5. 我们的每用户成本是多少？未来趋势如何？  
6. 我们能否根据实际成果收费，而不仅仅是按使用次数收费？  
7. 当AI成本每年下降10倍时，我们的利润来源在哪里？  
8. 在规模扩大10倍的情况下，我们的单位经济效益如何？  

### 竞争分析  
9. 一家只有3名员工的、完全基于人工智能的初创公司能在3个月内开发出什么具有竞争力的产品？  
10. 我们在哪些方面拥有新进入者没有的优势？  
11. 我们建立了哪些让客户难以替代的分销渠道？  

### 个人发展  
12. 我是在建立一家公司，还是在做一个项目？  
13. 我有什么独特的优势，是AI难以复制的？  
14. 我是否把时间浪费在低效的任务上（比如每小时10美元的任务）？  
15. 如果我有10倍的资源，我会做什么？如果只有1/10的资源，又会怎么做？  

---

## 数据存储  
所有记录都存储在 `memory/founder-journal/` 目录中：  
```
memory/founder-journal/
├── 2026-02-15.md       # Daily entries
├── 2026-02-16.md
├── weekly/
│   └── 2026-W07.md     # Weekly reviews
└── decisions/
    └── 2026-02-15-decision-name.md
```  

## 致谢  
由[M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。  
[YouTube频道](https://youtube.com/@aiwithabidi) | [GitHub仓库](https://github.com/aiwithabidi)  
本工具是**AgxntSix Skill Suite**的一部分，专为OpenClaw智能助手设计。  

📅 **需要帮助为您的企业设置OpenClaw吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)