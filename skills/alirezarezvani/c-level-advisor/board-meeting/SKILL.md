---
name: board-meeting
description: "**多代理董事会决策协议**  
该协议采用结构化的六阶段审议流程：  
1. **背景信息收集**：了解相关背景和情境。  
2. **高管独立意见表达**：高管们独立发表意见（相互之间不交流信息）。  
3. **意见分析**：对各方意见进行客观评估。  
4. **综合讨论**：整合各方的观点和建议。  
5. **创始人审核**：创始人对讨论结果进行审核和反馈。  
6. **最终决策形成**：基于综合分析形成最终决策。  
**适用场景**：  
当用户执行 `/cs:board` 命令、召开董事会会议，或需要对战略问题进行多角度、结构化的讨论时，可使用该协议。"
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: c-level
  domain: board-protocol
  updated: 2026-03-05
  frameworks: 6-phase-board, two-layer-memory, independent-contributions
---
# 董事会会议流程

这是一种结构化的多代理人讨论机制，旨在防止群体思维、收集少数意见，并产生清晰、可执行的决策。

## 关键词
董事会会议、高管层讨论、战略决策、高层管理团队（C-suite）、多代理人、/cs:board、创始人审核、决策提取、独立观点

## 使用方法
`/cs:board [主题]` — 例如：`/cs:board 我们应该在第三季度扩展到西班牙吗？`

---

## 六阶段流程

### 第一阶段：收集背景信息
1. 加载 `memory/company-context.md`
2. 加载 `memory/board-meetings/decisions.md` **（仅限第二层数据——切勿使用原始记录）**
3. 重置会议状态——避免受到之前讨论的影响
4. 呈现议程并激活相关角色 → 等待创始人确认

**首席幕僚根据讨论主题选择相关角色**（并非每次都会激活所有9个角色）：
| 主题 | 激活的角色 |
|-------|----------|
| 市场扩张 | CEO、CMO、CFO、CRO、COO |
| 产品方向 | CEO、CPO、CTO、CMO |
| 人力资源 | CEO、CHRO、CFO、COO |
| 定价 | CMO、CFO、CRO、CPO |
| 技术 | CTO、CPO、CFO、CISO |

---

### 第二阶段：独立贡献（相互隔离）
**禁止信息交流。每个角色在看到其他人的意见之前先独立完成自己的分析。**

顺序：（如需要）进行研究 → CMO → CFO → CEO → CTO → COO → CHRO → CRO → CISO → CPO

**思考方法：**
- CEO：思维树（预测三种未来可能性）
- CFO：逻辑链（展示计算过程）
- CMO：递归思考（草稿→批评→完善）
- CPO：基本原则分析
- COO：逐步分析（流程图）
- CTO：反应式决策（研究→分析→行动）
- CISO：基于风险的评估
- CHRO：同理心+数据分析

**贡献格式（最多5个关键点，需自行验证）：**
```
## [ROLE] — [DATE]

Key points (max 5):
• [Finding] — [VERIFIED/ASSUMED] — 🟢/🟡/🔴
• [Finding] — [VERIFIED/ASSUMED] — 🟢/🟡/🔴

Recommendation: [clear position]
Confidence: High / Medium / Low
Source: [where the data came from]
What would change my mind: [specific condition]
```

每个角色在贡献前需自行验证：来源出处、假设合理性、信心评分。禁止使用未经标记的陈述。

---

### 第三阶段：批判性分析
高管导师同时接收所有第二阶段的输出。其角色是提出质疑的评审者，而非综合者。

检查清单：
- 有哪些观点是所有角色都轻易同意的？（这种共识可能是危险的信号）
- 有哪些共同假设尚未经过验证？
- 有哪些关键人物未参与讨论？（如客户意见或一线运营人员）
- 有哪些风险被忽略了？
- 有没有角色超出了自己的专业领域进行讨论？

---

### 第四阶段：综合讨论
首席幕僚使用 **董事会会议输出格式**（定义在 `agent-protocol/SKILL.md` 中）进行整理：
- 需要做出的决策（一句话）
- 各角色的观点（每个角色一条）
- 他们的一致点/分歧点
- 评审者的意见（直言不讳的真相）
- 建议的决策及行动事项（负责人及截止日期）
- 如果创始人不同意，你的建议是什么

---

### 第五阶段：等待创始人的决策 ⏸️
**所有流程暂停，等待创始人的决定。**

```
⏸️ FOUNDER REVIEW — [Paste synthesis]

Options: ✅ Approve | ✏️ Modify | ❌ Reject | ❓ Ask follow-up
```

**规则：**
- 用户的修正意见优先于代理人的提议。不得反驳。
- 如果30分钟内没有反馈，会议将自动标记为“待审核状态”。
- 可以随时使用 `/cs:board resume` 重新开启讨论。

---

### 第六阶段：决策确认
获得创始人批准后：
- **第一层数据：** 编写完整的会议记录 → `memory/board-meetings/YYYY-MM-DD-raw.md`
- **第二层数据：** 将通过的决策添加到 `memory/board-meetings/decisions.md` 中
- 将被拒绝的提案标记为 `[DO_NOT_RESURFACE]`
- 向创始人确认决策结果，并记录决策数量、已采取的行动及存在的问题。

---

## 数据存储结构
**未来的会议仅加载第二层数据。** 避免出现“虚假共识”的情况。

---

## 失败情况快速参考
| 失败原因 | 解决方法 |
|---------|-----|
| 群体思维（所有人意见一致） | 重新进行第二阶段的独立讨论；强制提出“最有力的反对意见” |
| 分析瘫痪（无法达成共识） | 限制每个角色的观点数量为5个；即使信心较低也要提出建议 |
- 无意义的讨论 | 将该讨论记录为待处理的行动事项；返回主议程 |
- 角色越权（例如CFO擅自做出产品决策） | 由评审者标记；将其排除在综合结果之外 |
- 数据污染（不同阶段的记录混杂） | 第一阶段仅加载 `decisions.md` 文件——这是硬性规定 |

---

## 参考资料
- `templates/meeting-agenda.md` — 会议议程格式
- `templates/meeting-minutes.md` — 最终会议记录格式
- `references/meeting-facilitation.md` — 冲突处理、时间安排及失败情况处理指南