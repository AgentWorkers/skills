# 代理辩论技能（Agent Debate Skill）

该技能能够生成多个子代理来讨论不同的方案，并最终确定最佳解决方案。

## 概述  
该技能通过使用多个并行运行的子代理以及基于文件的协调机制来模拟对抗性辩论。每个子代理独立进行调查并撰写分析结果，随后由一个综合代理汇总所有观点并选出胜者。

## 适用场景：  
- 架构决策  
- 调试（尤其是当问题根源不明确时）  
- 交易策略评估  
- 安全性审查（采用“红队”模式）  
- 需要权衡复杂论点的场景  

### 工作原理：  
1. **负责人（Lead）** 提出问题，并生成2至4个辩论代理。  
2. 每个代理将自身的观点写入 `plans/debate-{id}/agent-{n}.md` 文件中。  
3. 综合代理会读取所有代理的观点并生成最终判断。  
4. 负责人根据综合代理的判断采取相应行动。  

### 文件结构：  
（文件结构部分使用 ````
plans/debate-{topic}/
├── question.md          # The question being debated
├── agent-1.md           # Agent 1's position
├── agent-2.md           # Agent 2's position
├── agent-3.md           # Agent 3's position (optional)
├── rebuttal-1.md        # Agent 1's rebuttal (round 2)
├── rebuttal-2.md        # Agent 2's rebuttal (round 2)
├── synthesis.md         # Final synthesis and verdict
└── decision.md          # Lead's final decision
```` 标识）  

### 使用方法：  
#### 单轮辩论（快速模式）：  
- 3个代理参与一轮辩论，耗时约5分钟。  

#### 两轮辩论（详细模式）：  
- 3个代理分别提出观点和反驳意见，耗时约10分钟。  

#### 对抗性模式（红队模式）：  
- 1个构建者（Builder）和1个攻击者（Attacker）进行辩论，适用于安全性评估。  

## 所需模型：  
- **辩论代理（Debate Agents）**：Opus 4.6（需具备深度推理能力）  
- **综合代理（Synthesis Agent）**：Opus 4.6（需能够权衡各种细微观点）  
- **简单观点的讨论**：Sonnet 4.5（适用于成本敏感且主题明确的场景）  

## 适用场景示例：  
- 需要评估多种可行架构方案的决策  
- 需要深入排查问题的调试过程  
- 交易策略的评估  
- 安全性审查（采用对抗性辩论模式）  
- 需要选择合适的技术解决方案的竞赛场景  

### 不适用场景：  
- 简单的实施任务  
- 有明显唯一答案的任务  
- 需要按顺序执行的依赖性较强的任务  

## 示例提示：  
- **架构辩论示例**：  
  （代码示例部分使用 ````
Question: "Should Nudge use Turso (SQLite) or Supabase (Postgres) for production?"
Agent 1: Argue for Turso — edge computing, simplicity, cost
Agent 2: Argue for Supabase — ecosystem, realtime, auth
Agent 3: Devil's advocate — what about a hybrid approach?
```` 标识）  

- **交易策略示例**：  
  （代码示例部分使用 ````
Question: "Is ETH undervalued at current levels given macro conditions?"
Agent 1: Bull case — on-chain metrics, upcoming catalysts
Agent 2: Bear case — macro headwinds, technical levels
Agent 3: Neutral — range-bound thesis with key levels to watch
```` 标识）  

- **调试示例**：  
  （代码示例部分使用 ````
Question: "App crashes on iOS 17 but not 18. What's the root cause?"
Agent 1: Investigate API deprecation changes
Agent 2: Investigate SwiftUI rendering pipeline differences
Agent 3: Investigate memory management changes
```` 标识）  

## 与Swarm平台的集成：  
该辩论机制可广泛应用于Swarm平台：  
- Sprint团队可用于讨论竞赛中的技术方案  
- Quant团队可进行牛市/熊市/中性市场分析  
- 架构师团队可评估设计模式  
- 任何代理在面临复杂决策时均可启动辩论流程  

## 未来展望：  
当OpenClaw原生支持Claude Code的代理团队功能时：  
- 各代理将能够直接相互通信（无需依赖文件协调）  
- 任务列表将取代基于文件的进度跟踪机制  
- 负责人无需亲自执行具体操作即可分配任务  
- 该技能将作为原生代理团队的轻量级辅助工具使用。