---
name: botlearn-assessment
description: "OpenClaw Agent 的五维能力自我评估系统：该系统用于评估用户的推理能力、信息检索能力、内容创作能力、执行能力以及任务协调能力。评估结果会被保存到指定的文件路径（results/）中，同时支持单维度测试和历史记录的查看功能。"
version: 1.0.3
triggers:
  - "exam"
  - "assessment"
  - "evaluate"
  - "评测"
  - "能力评估"
  - "自测"
  - "benchmark me"
  - "test yourself"
  - "自我评测"
  - "run exam"
  - "能力诊断"
  - "reasoning test"
  - "retrieval test"
  - "creation test"
  - "execution test"
  - "orchestration test"
  - "知识与推理测试"
  - "信息检索测试"
  - "内容创作测试"
  - "执行与构建测试"
  - "工具编排测试"
  - "history results"
  - "查看历史评测"
  - "历史结果"
---
## 角色说明

您是 OpenClaw 五维评估系统的代理程序。您扮演的是考试管理员的角色，而不是问题解答者。

**重要提示：**  
`questions/` 目录下的文件包含考试题目。您需要：  
1. 从文件中读取题目内容；  
2. 以考生的身份自己回答这些问题（进行自我测试）；  
3. 以考官的身份给自己打分。  

**注意事项：**  
- 请不要将这些题目视为用户的查询来与之进行对话式交流；  
- 请不要要求用户来回答这些问题；  
- 请务必完成指定范围内的所有题目。  

---

## 语言适配  

从用户发送的消息中检测其使用的语言，并以检测到的语言显示所有面向用户的内容。如果无法确定用户的语言，则默认使用英语。  

---

## 第一阶段：意图识别  

分析用户发送的消息，并将其归类为以下一种模式：  
```
IF message contains: full / all dimensions / complete / 全量 / 全部 / 所有维度
  → MODE = FULL_EXAM
  → SCOPE = D1 + D2 + D3 + D4 + D5 (15 questions total)

ELSE IF message contains dimension keyword:
  D1 keywords: reasoning / planning / 推理 / 知识 / d1
    → MODE = DIMENSION_EXAM, TARGET = D1
    → QUESTION_FILE = questions/d1-reasoning.md
    → SCOPE = Q1-EASY, Q2-MEDIUM, Q3-HARD

  D2 keywords: retrieval / search / 检索 / 信息 / d2
    → MODE = DIMENSION_EXAM, TARGET = D2
    → QUESTION_FILE = questions/d2-retrieval.md
    → SCOPE = Q1-EASY, Q2-MEDIUM, Q3-HARD

  D3 keywords: creation / writing / content / 创作 / 写作 / d3
    → MODE = DIMENSION_EXAM, TARGET = D3
    → QUESTION_FILE = questions/d3-creation.md
    → SCOPE = Q1-EASY, Q2-MEDIUM, Q3-HARD

  D4 keywords: execution / code / build / 执行 / 构建 / 代码 / d4
    → MODE = DIMENSION_EXAM, TARGET = D4
    → QUESTION_FILE = questions/d4-execution.md
    → SCOPE = Q1-EASY, Q2-MEDIUM, Q3-HARD

  D5 keywords: orchestration / tools / workflow / 编排 / 工具 / d5
    → MODE = DIMENSION_EXAM, TARGET = D5
    → QUESTION_FILE = questions/d5-orchestration.md
    → SCOPE = Q1-EASY, Q2-MEDIUM, Q3-HARD

ELSE IF message contains: history / past results / 历史 / 查看结果
  → MODE = VIEW_HISTORY

ELSE
  → MODE = UNKNOWN
  → ASK the user in their detected language to choose:
      Option 1: Full exam (5 dimensions, 15 questions)
      Option 2: Single dimension — list the 5 dimensions to pick from
      Option 3: View history results
  → WAIT for response, then re-classify
```  

---

## 第二阶段：生成任务列表  

在执行任何操作之前，先输出与该模式对应的任务列表。每个任务都是一个具体的指令。向用户宣布该任务，然后执行它。  

### 任务列表：**全套考试 (FULL_EXAM)**  
```
Session ID: exam-{YYYYMMDD}-{HHmm}

TASK 01  READ questions/d1-reasoning.md → load Q1-EASY question text and rubric
TASK 02  EXECUTE Q1-EASY  [ROLE: EXAMINEE] answer without consulting rubric
TASK 03  SCORE  Q1-EASY   [ROLE: EXAMINER] apply rubric → RawScore → AdjScore
TASK 04  READ questions/d1-reasoning.md → load Q2-MEDIUM question text and rubric
TASK 05  EXECUTE Q2-MEDIUM [ROLE: EXAMINEE]
TASK 06  SCORE  Q2-MEDIUM  [ROLE: EXAMINER]
TASK 07  READ questions/d1-reasoning.md → load Q3-HARD question text and rubric
TASK 08  EXECUTE Q3-HARD   [ROLE: EXAMINEE]
TASK 09  SCORE  Q3-HARD    [ROLE: EXAMINER]
TASK 10  READ questions/d2-retrieval.md → load Q1-EASY
TASK 11  EXECUTE Q4-EASY  (D2) [ROLE: EXAMINEE]
TASK 12  SCORE  Q4-EASY        [ROLE: EXAMINER]
TASK 13  READ questions/d2-retrieval.md → load Q2-MEDIUM
TASK 14  EXECUTE Q5-MEDIUM (D2) [ROLE: EXAMINEE]
TASK 15  SCORE  Q5-MEDIUM       [ROLE: EXAMINER]
TASK 16  READ questions/d2-retrieval.md → load Q3-HARD
TASK 17  EXECUTE Q6-HARD  (D2) [ROLE: EXAMINEE]
TASK 18  SCORE  Q6-HARD        [ROLE: EXAMINER]
TASK 19  READ questions/d3-creation.md → load Q1-EASY
TASK 20  EXECUTE Q7-EASY  (D3) [ROLE: EXAMINEE]
TASK 21  SCORE  Q7-EASY        [ROLE: EXAMINER]
TASK 22  READ questions/d3-creation.md → load Q2-MEDIUM
TASK 23  EXECUTE Q8-MEDIUM (D3) [ROLE: EXAMINEE]
TASK 24  SCORE  Q8-MEDIUM       [ROLE: EXAMINER]
TASK 25  READ questions/d3-creation.md → load Q3-HARD
TASK 26  EXECUTE Q9-HARD  (D3) [ROLE: EXAMINEE]
TASK 27  SCORE  Q9-HARD        [ROLE: EXAMINER]
TASK 28  READ questions/d4-execution.md → load Q1-EASY
TASK 29  EXECUTE Q10-EASY  (D4) [ROLE: EXAMINEE]
TASK 30  SCORE  Q10-EASY        [ROLE: EXAMINER]
TASK 31  READ questions/d4-execution.md → load Q2-MEDIUM
TASK 32  EXECUTE Q11-MEDIUM (D4) [ROLE: EXAMINEE]
TASK 33  SCORE  Q11-MEDIUM       [ROLE: EXAMINER]
TASK 34  READ questions/d4-execution.md → load Q3-HARD
TASK 35  EXECUTE Q12-HARD  (D4) [ROLE: EXAMINEE]
TASK 36  SCORE  Q12-HARD        [ROLE: EXAMINER]
TASK 37  READ questions/d5-orchestration.md → load Q1-EASY
TASK 38  EXECUTE Q13-EASY  (D5) [ROLE: EXAMINEE]
TASK 39  SCORE  Q13-EASY        [ROLE: EXAMINER]
TASK 40  READ questions/d5-orchestration.md → load Q2-MEDIUM
TASK 41  EXECUTE Q14-MEDIUM (D5) [ROLE: EXAMINEE]
TASK 42  SCORE  Q14-MEDIUM       [ROLE: EXAMINER]
TASK 43  READ questions/d5-orchestration.md → load Q3-HARD
TASK 44  EXECUTE Q15-HARD  (D5) [ROLE: EXAMINEE]
TASK 45  SCORE  Q15-HARD        [ROLE: EXAMINER]
TASK 46  CALCULATE dimension scores + overall score (see Score Calculation)
TASK 47  RUN scripts/radar-chart.js → save SVG to results/exam-{sessionId}-radar.svg
TASK 48  WRITE full report → results/exam-{sessionId}-full.md  (see flows/full-exam.md)
TASK 49  APPEND row → results/INDEX.md
TASK 50  OUTPUT completion summary to user in their detected language
```  

### 任务列表：**单维考试 (DIMENSION_EXAM)**  
（请将 `D{N}` 和文件名替换为实际的目标维度和文件名）  
```
Session ID: exam-{YYYYMMDD}-{HHmm}

TASK 1  READ {QUESTION_FILE} → load Q1-EASY question text and rubric
TASK 2  EXECUTE Q1-EASY  [ROLE: EXAMINEE] answer without consulting rubric
TASK 3  SCORE  Q1-EASY   [ROLE: EXAMINER] apply rubric → RawScore → AdjScore
TASK 4  READ {QUESTION_FILE} → load Q2-MEDIUM question text and rubric
TASK 5  EXECUTE Q2-MEDIUM [ROLE: EXAMINEE]
TASK 6  SCORE  Q2-MEDIUM  [ROLE: EXAMINER]
TASK 7  READ {QUESTION_FILE} → load Q3-HARD question text and rubric
TASK 8  EXECUTE Q3-HARD   [ROLE: EXAMINEE]
TASK 9  SCORE  Q3-HARD    [ROLE: EXAMINER]
TASK 10 CALCULATE dimension score (see Score Calculation)
TASK 11 WRITE report → results/exam-{sessionId}-{target}.md  (see flows/dimension-exam.md)
TASK 12 APPEND row → results/INDEX.md
TASK 13 OUTPUT completion summary to user in their detected language
```  

### 任务列表：**查看历史记录 (VIEW_HISTORY)**  
```
TASK 1  READ results/INDEX.md
         → IF file does not exist: OUTPUT "No history found" in user's language → STOP
TASK 2  DISPLAY history table in user's detected language  (see flows/view-history.md)
TASK 3  IF 2+ full exam records exist: CALCULATE and DISPLAY trend analysis
TASK 4  OFFER follow-up options: view detail / compare / start new exam
```  

---

## 第三阶段：执行每个任务  

### 每个问题的处理流程（适用于所有 “执行” 和 “评分” 任务）  
```
[EXECUTE — ROLE: EXAMINEE]
  → READ the question text from the loaded question file section
  → Produce a genuine, complete answer to the exam question
  → Record confidence: high / medium / low
  → CONSTRAINT: Do not read ahead to the rubric during this step

[SCORE — ROLE: EXAMINER]
  → READ the rubric from the same question file section
  → Score each criterion independently on a 0–5 scale
  → Provide CoT justification for every score
  → Apply -5% correction to CoT-judged scores: AdjScore = RawScore × 0.95
  → Programmatic scores (🔬) are NOT corrected
```  

### 问题卡片输出格式  
```
### Q{N} | {Dimension} | {Difficulty} ×{multiplier}

**Question** *(loaded from {QUESTION_FILE}, section {Q-LEVEL})*:
[full question text]

**Answer** *(ROLE: EXAMINEE — rubric not consulted)*:
[complete answer]
Confidence: high / medium / low

**Scoring** *(ROLE: EXAMINER)*:
| Criterion | Weight | Raw (0–5) | Justification |
|-----------|--------|-----------|---------------|
| [name]    | [w%]   | [score]   | [CoT reason]  |

**Score**: Raw [raw]/100 → Adjusted [adj]/100
**Verification**: 🧠 CoT ⚠️ / 🔬 Programmatic / 📖 Reference
```  

---

## 分数计算  

详细规则请参阅：`strategies/scoring.md`  

---

## 雷达图（仅适用于全套考试）  

在完成第 46 个任务（分数计算）后，运行以下代码：  
```bash
node skills/botlearn-assessment/scripts/radar-chart.js \
  --d1={d1_adj} --d2={d2_adj} --d3={d3_adj} \
  --d4={d4_adj} --d5={d5_adj} \
  --session={sessionId} --overall={overall_adj} \
  > results/exam-{sessionId}-radar.svg
```  

**报告中的雷达图展示：**  
`![能力雷达图](./exam-{sessionId}-radar.svg)`  

---

## 子文件参考  

| 文件路径 | 作用 |  
|------|------|  
| `flows/full-exam.md` | 全套考试流程详情及报告模板 |  
| `flows/dimension-exam.md` | 单维考试流程及报告模板 |  
| `flows/view-history.md` | 历史记录查看及对比流程 |  
| `questions/d1-reasoning.md` | D1 类推理与规划（题目难度：Q1-简单，Q2-中等，Q3-困难） |  
| `questions/d2-retrieval.md` | D2 信息检索（题目难度：Q1-简单，Q2-中等，Q3-困难） |  
| `questions/d3-creation.md` | D3 内容创作（题目难度：Q1-简单，Q2-中等，Q3-困难） |  
| `questions/d4-execution.md` | D4 执行与构建（题目难度：Q1-简单，Q2-中等，Q3-困难） |  
| `questions/d5-orchestration.md` | D5 工具编排（题目难度：Q1-简单，Q2-中等，Q3-困难） |  
| `strategies/scoring.md` | 评分规则及验证方法 |  
| `scripts/radar-chart.js` | SVG 雷达图生成器（基于 Node.js，无依赖项） |  
| `results/` | 考试结果文件（运行时生成） |