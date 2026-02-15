---
name: war-room
description: 多智能体作战室（Multi-agent War Room）适用于头脑风暴、系统设计、架构评审、产品规格制定、商业策略讨论或任何复杂问题的解决。当用户需要组织一场包含专业角色的结构化多智能体会议时，或者当他们希望从零开始讨论一个项目、从多个角度设计系统、通过“魔鬼代言人”（devil's advocate）的角色对决策进行压力测试，或者需要制定一份全面的蓝图/规格说明书时，都可以使用该工具。该工具适用于软件、硬件、内容、商业等各个领域。
---

# 战斗室（War Room）

这是一种用于开展多智能体头脑风暴和执行会议的方法论。各专业智能体通过共享文件系统按依赖关系顺序协作。其中，一个名为“CHAOS”的智能体会在每个会议阶段进行监督和评估。会议输出包括：决策记录、专业文档、整合后的蓝图以及会议总结。

## 快速入门

1. **初始化：** 运行 `bash skills/war-room/scripts/init_war_room.sh <project-name>`，在 `war-rooms/<project>/` 下创建项目文件夹结构。
2. **编写项目简介：** 在 `war-rooms/<project>/BRIEF.md` 中填写项目描述、目标、约束条件以及已知风险。
3. **注入核心理念（DNA）：** 将 `skills/war-room/references/dna-template.md` 复制到 `war-rooms/<project>/DNA.md`，根据需要自定义（添加项目标识和负责人名称）。
4. **选择智能体角色：** 为该项目选择所需的专业角色（参见 [agent-roles.md](references/agent-roles.md)）。并非每个项目都需要所有角色。
5. **执行会议流程：** 按照以下步骤执行会议流程。每个会议阶段都会生成子智能体，它们会在共享文件系统中读写数据。
6. **整合结果：** 将所有智能体的输出合并到 `war-rooms/<project>/artifacts/` 中的蓝图文件中。
7. **撰写会议总结：** 在 `war-rooms/<project>/lessons/` 中记录会议经验教训。

## 会议流程（Wave Protocol）

详细流程请参考 [wave-protocol.md](references/wave-protocol.md)。

### 第0阶段：验证假设（Prove It，强制要求）

在开始任何具体设计工作之前，先识别出**最危险的假设**，并通过实际操作（代码测试、原型制作、市场调研等）进行验证。验证时间最长为30分钟。如果验证失败，则在投入资源进行详细设计之前立即调整方向。

### 第1至N阶段：专业任务执行（Specialist Execution）

每个阶段会部署一组可以并行工作的智能体（同一阶段内的智能体之间没有依赖关系）。后续阶段的智能体会依赖于前一个阶段的输出结果。

**规划会议流程：**
1. 列出项目所需的所有智能体。
2. 构建依赖关系图（哪些智能体需要哪些输出结果）。
3. 将没有相互依赖关系的智能体分组到同一阶段。
4. 按依赖关系顺序安排各个阶段。

**每个阶段的智能体任务：**
- 阅读：`BRIEF.md`、`DNA.md`、`DECISIONS.md` 以及之前所有智能体的输出文件。
- 写入：`agents/<role>/` 文件夹，记录自己的设计方案、发现的问题和决策结果。
- 更新：`DECISIONS.md`（记录本阶段的决策）和 `STATUS.md`（记录完成状态）。
- 通过 `comms/` 进行跨智能体沟通，提出问题或提出挑战。

**生成子智能体：** 每个智能体都是一个子智能体，其系统提示信息包括：
- 核心理念（来自 `DNA.md`）
- 该角色的职责说明（来自 [agent-roles.md](references/agent-roles.md)）
- 项目简介
- 指令：阅读前一个阶段的输出结果，并将结果写入自己的文件夹。

### 每个阶段之间的调整机制（Pivot Gate）

在开始新阶段之前，询问：“自上一个阶段以来，是否有任何基本假设发生了变化？”
- 如果有变化 → 受影响的智能体需要重新评估相关决策，并在 `DECISIONS.md` 中将决策标记为 `**VOIDED**。
- 如果没有变化 → 继续执行下一个阶段。

### CHAOS智能体的监督作用

CHAOS智能体不参与特定阶段的会议，而是监督整个会议过程。每个阶段结束后，CHAOS智能体会：
1. 阅读该阶段所有智能体的输出结果。
2. 将发现的问题记录到 `agents/chaos/challenges.md` 文件中，格式如下：`[C-ID] CHALLENGE to D### — 攻击方向 — 结果（SURVIVE/WOUNDED/KILLED）`
- `WOUNDED` 表示问题需要解决；`KILLED` 表示决策需要重新制定。

当CHAOS智能体发现更优的解决方案时，它还会提出修改建议。

### 整合阶段（Final Wave）

由一名智能体（或会议协调者）将所有专业角色的输出结果整合成最终蓝图：
1. 阅读所有 `agents/*/` 文件夹中的内容。
2. 解决矛盾（标记出尚未解决的问题）。
3. 生成统一文档 `artifacts/<PROJECT>-BLUEPRINT.md`，内容包括：架构、项目范围、风险分析、路线图（以及未包含的内容）。
4. CHAOS智能体会审核蓝图中的逻辑一致性。

### 会议总结（Post-Mortem）

整合完成后，撰写 `lessons/session-N-postmortem.md`，内容包括：
- 成功之处
- 失败的原因（浪费的工作、发现的问题、流程中的失误）
- 为下一次会议提供的经验教训。

## 智能体角色选择指南

并非每个项目都需要所有角色。根据项目需求选择合适的角色：

| 项目类型 | 常见角色 |
|---|---|
| 软件MVP | 架构师（ARCH）、项目经理（PM）、开发人员（DEV）、用户体验设计师（UX）、安全专家（SEC）、质量保证人员（QA）、CHAOS智能体 |
| 商业策略 | 项目经理（PM）、市场研究员（RESEARCH）、财务专家（FINANCE）、市场分析师（MKT）、法律专家（LEGAL）、CHAOS智能体 |
| 内容/创意项目 | 项目经理（PM）、用户体验设计师（UX）、市场研究员（RESEARCH）、市场分析师（MKT）、CHAOS智能体 |
| 硬件/物联网项目 | 架构师（ARCH）、开发人员（DEV）、运维人员（OPS）、安全专家（SEC）、质量保证人员（QA）、CHAOS智能体 |
| 架构评审项目 | 架构师（ARCH）、安全专家（SEC）、运维人员（OPS）、质量保证人员（QA）、CHAOS智能体 |

**CHAOS智能体是必选项**，它起到“免疫系统”的作用。

完整的角色描述和简介模板请参见 [agent-roles.md](references/agent-roles.md)。

## 通信协议

所有智能体之间的通信都通过文件系统进行，无需额外消耗任何资源。

### 共享文件
| 文件 | 用途 | 编写者 |
|---|---|---|
| `BRIEF.md` | 项目描述和约束条件 | 会议协调者（你） |
| `DNA.md` | 向所有智能体传递的核心理念 | 会议协调者（会议期间不可修改） |
| `DECISIONS.md` | 只能追加内容的决策记录 | 各智能体（仅记录本领域的决策） |
| `STATUS.md` | 智能体的完成状态 | 各智能体 |
| `BLOCKERS.md` | 需要协调者处理的障碍 | 任何智能体 |
| `TLDR.md` | 会议总结（整合后更新） | 会议协调者 |
| `comms/` | 跨智能体通信和挑战 | 任何智能体 |
| `agents/<role>/` | 各智能体的专属输出 | 相关智能体 |

### 决策记录格式
```
[D###] OWNER — what was decided — why (1 sentence each)
```
每次会议建议记录不超过25条决策。如果决策过多，说明项目范围过大，需要拆分会议。仅记录那些会对后续工作产生影响的决策。实施细节不属于决策内容。

### 智能体之间的消息格式
```
FROM: {role}
TO: {target} | ALL | LEAD
TYPE: FINDING | QUESTION | DECISION | BLOCKER | UPDATE | CHALLENGE
PRI: LOW | MED | HIGH | CRIT
---
{content — max 200 words}
---
FILES: [{paths}]
```

## 第3阶段：提出建议并执行（Phase 3: Suggest + Execute）

整合完成后，会议不会就此结束。接下来需要**提出具体的下一步行动方案**，并使用相同的智能体来执行这些方案：

```
"Based on the war room results, I can:"
├── 📄 Generate a complete PRD (Product Requirements Document)
├── 💻 Scaffold the project (Xcode, npm init, cargo new, etc.)
├── 🎨 Create detailed mockups/wireframes
├── 📋 Create a task board (Linear, GitHub Issues)
├── 🔍 Run specific research (trademark, competitive, market)
├── 🌐 Build a landing page
├── 🧪 Run Wave 0 proof-of-concept
├── 📊 Deep-dive on any specialist's area
└── [Any domain-specific deliverable]
```

关键点：设计系统的智能体也能够直接生成最终产品。战斗室是一个**持续迭代的工作流程**，而不仅仅是一次性活动。流程包括：头脑风暴 → 规划 → 开发 → 发布。

### 反向战斗室（Reverse War Room，可选扩展）

标准战斗室是从零开始逐步构建产品的；而反向战斗室则是从最终产品现状倒推当前开发过程。结合使用这两种方法可以确保最高效率。

**适用场景：** 当你已经有原型或部分成品，需要找到最快交付给客户的路径时。

**相关智能体角色：**
- **PRODUCT**：从客户的角度定义最终产品，编写用户使用指南，识别用户满意点和痛点。
- **REVERSE**：从产品愿景反向分析当前开发流程，量化每个环节的差距，确定关键路径，列出无需开发的模块。
- **CHAOS**：识别阻碍项目进展的潜在问题，评估各个选项的可行性。

**关键输出：**
- 用户使用指南（包含完整的交互流程）
- 差距分析（列出所有差距，标注优先级）
- 关键路径（最小化开发顺序）
- 需要剔除的模块列表（可节省30-50%的工作量）
- 最致命的风险因素
- 客观的风险评估（基于数学计算的概率）

**测试记录：** 最初在KOSMO平台上进行测试（2026年2月8日）。结果发现：30个问题，取消了10个不必要的功能（节省了约20小时的工作时间），并找到了导致项目失败的根源。

## INTERCEPTOR——自主战斗室控制器

INTERCEPTOR是战斗室的界面和管理工具，负责会议流程的自动控制。

### 三种运行状态（无空闲状态）

```
██ EXEC   — Agents working. Processing. Shipping.
██ AWAIT  — Blocked on OPERATOR decision. Presents options. Waits.
██ WATCH  — All tasks complete or agents running. Sets cron auto-wake.
```

### 会议连续性保障机制（Continuity Protocol）

**注意：** 本部分描述了使用OpenClaw调度工具（cron）来保证会议连续性的方法。该工具不会安装系统级守护进程或修改启动文件，也不会创建持久性后台进程。所有调度操作均通过OpenClaw的cron API进行，且操作者已通过启动OpenClaw授权。

为了在智能体异步处理任务时保持会议连续性：
1. 使用OpenClaw的cron工具在预期完成时间安排后续检查。
2. 检查完成后，确认智能体的成果是否已保存在指定文件夹中。
3. 如果智能体已完成任务，则整合成果并呈报给操作者。
4. 如果智能体仍在运行，则安排下一次检查（间隔3分钟）。
5. 如果所有任务已完成，则建议下一步行动或等待操作者的指示。

### 文档展示方式

当战斗室生成可视化成果（图片、图表、蓝图等）时，使用平台的默认文件查看器向操作者展示：
- 在macOS上使用 `open` 命令。
- 在Linux上使用 `xdg-open` 命令。
- 确保文件路径指向战斗室的工作目录。
- 在生成成果后立即展示，以便操作者无需手动导航即可查看。

### 通信风格

INTERCEPTOR的通信方式简洁直观：
- 使用文本框、进度条、状态表等视觉元素传达信息。
- 信息量丰富，但表达清晰。
- 使操作者感受到自己正在操作一个高效系统。

### 操作者的决策流程

当需要操作者介入时：
- 为操作者提供最多3个选项。
- 提供INTERCEPTOR的建议。
- 说明在没有响应时的默认处理方式。
- 设置自动唤醒机制，以防操作者暂时离开。

---

## DNA 3.0：运营协议（DNA v3: Operational Protocols）

DNA是战斗室的核心组成部分。所有规则都是强制性的，不可或缺。

**共19项协议，分为4个类别：**

### 苏格拉底式思维（Socratic Protocols, S1-S4）：
- **S1对立测试（S1 Opposite Test）**：每个决策都必须提出相反的观点，并提供充分的论据。
- **S2五问法（S2 Five Whys）**：深入探究问题的根本原因。
- **S3无知声明（S3 Ignorance Declaration）**：在分析前明确已知/未知/假设的内容。
- **S4辩证思考（S4 Dialectic Obligation）**：如果同意前一个智能体的观点，要用一个问题进行质疑。

### 密封式思维（Hermetic Protocols, H1-H6）：
- **H1镜像测试（H1 Mirror Test）**：从宏观和微观两个角度展示问题。
- **H2连锁反应分析（H2 Ripple Analysis）**：追踪问题的多级影响。
- **H3张力图（H3 Tension Map）**：将决策置于不同的影响范围内进行评估。
- **S4因果链分析（S4 Trace Protocol）**：为每个技术决策建立因果关系。
- **H5标签分类（H5 Tag Classification）**：为成果分配“SPRINT”、“CRAFT”或“FLOW”等标签。
- **H6先创造再约束（H6 Create-Then-Constrain）**：先生成方案，再根据实际情况进行调整。

### 抗脆弱性思维（Antifragile Protocols, A1-A5）：
- **A1减法原则（A1 Subtraction Mandate）**：在添加新内容前，先列出需要移除的3个要素。
- **A2备选方案评估（A2 Plan B Price Tag）**：为每个关键决策评估成本。
- **A3风险评估（A3 90/10 Rule）**：为决策标注“SAFE”或“RADICAL”标签，激进程度不超过20%。
- **A4事前评估（A4 Pre-Mortem）**：在宣布决策前先预测可能出现的失败情况。
- **A5经验总结（A5 Lessons Permanent）**：每次失败后都要总结经验教训。

### 执行阶段（Execution Protocols, E1-E4）：
- **E1优先交付可用成果（E1 Ship Reality）**：优先交付可用的代码，而非完美方案。
- **E2保护产品声誉（E2 Protect Reputation）**：绝不要交付有缺陷的产品。
- **E3减少混乱（E3 Reduce Chaos）**：简洁的方案优于复杂的方案。
- **E4追求卓越（E4 Technical Excellence）**：对平庸的工作零容忍。

完整的DNA模板及所有协议格式请参见 [dna-template.md](references/dna-template.md)。