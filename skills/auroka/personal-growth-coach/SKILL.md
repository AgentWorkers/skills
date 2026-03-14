---
name: personal-growth-coach
description: Daily thinking practice skill. Generate open-ended exercises based on Pyramid Principle, Asking the Right Questions, and Underlying Logic to help users improve thinking, communication, and cognitive abilities. Triggers: daily practice, quiz me, thinking training, cognitive improvement, personal growth.
metadata:
  clawdbot:
    emoji: 🧠
---

# 个人成长——每日练习  
通过每日练习，提升你的思维能力、沟通技巧和认知深度。  

## 触发条件  
- 用户输入“测验我”、“每日练习”或“思维训练”  
- 用户希望提升思维能力、表达能力或认知水平  
- 用户希望练习结构化思维、批判性思维和基本分析能力  

## 知识库  
问题内容基于以下三本书：  

### 1. 《金字塔原则》——芭芭拉·明托（Barbara Minto）  
**核心要点：** 结构化表达，先提出结论  
- **原则内容：**  
  - 先提出最重要的信息  
  - 用高层次的观点来指导低层次的论据  
  - 将同类内容归类（遵循MECE原则：明确、相关、充分、具体）  
  - 保持逻辑顺序（时间顺序、结构顺序、重要性顺序）  

### 2. 《如何提出正确的问题》——尼尔·布朗（Neil Browne）  
**核心要点：** 批判性思维，寻找关键信息  
- **关键问题：**  
  - 问题是什么？结论是什么？  
  - 原因是什么？证据是否充分？  
  - 是否存在模糊的表述或误导性词汇？  
  - 是否存在逻辑谬误（如人身攻击、滑坡谬误、虚假二分法、循环论证）？  
  - 证据是否可靠？是否存在其他解释？  
  - 是否遗漏了重要信息？  

### 3. 《底层逻辑》——刘润（Liu Run）  
**核心要点：** 看透事物的本质，掌握一个就能掌握全部  
**四步分析方法：**  
  1. **事实**：客观上发生了什么（可验证，无主观判断）  
  2. **观点**：你对这件事的看法（个人判断和感受）  
  3. **本质**：背后的根本原因（基于事实的假设，需要验证）  
  4. **行动**：接下来该怎么做（基于本质制定的策略）  

## 测验规则  
### 默认设置  
- 问题数量：2-3个（用户可自定义）  
- 题型：全部为开放式主观题  
- 主题：适合大多数人的通用话题  

### 测验原则  
- 禁止使用选择题或判断题  
- 禁止要求用户“回忆特定情境”或“回忆经历”  
- 问题必须直接、明确，便于用户回答  
- 主题应涉及通用领域（如工作效率、时间管理、沟通技巧）  
- 避免过于专业或行业特定的场景  

### 问题类型  
- **概念解释**：解释概念的定义或关键点  
- **应用分析**：分析给定材料以解决实际问题  
- **结构化输出**：按照固定框架回答问题（结论 + 详细内容）  
- **四步分析**：根据给定情境，依次分析事实、观点、本质和行动方案  

## 测验流程  
1. **读取学习记录**：`memory/personal-growth-records.md`  
2. **针对薄弱环节设计问题**  
3. **提示用户注意薄弱点**：“上次你在某方面遇到困难，今天就重点练习这个内容”  
4. **用户答题**  
5. **提供反馈与参考答案**  
6. **更新学习记录**：记录本次练习中的薄弱环节  

## 学习记录  
记录文件存放路径：`memory/personal-growth-records/`  
文件命名格式：`YYYY-MM-DD-N.md`（日期 + 当天的练习编号）  

```markdown
# YYYY-MM-DD Session N

### Performance
| # | Topic | Result | Weakness |
|---|-------|--------|----------|

### Key Weak Areas
- Specific issues

### Next Session Suggestions
- Targeted improvement direction
```