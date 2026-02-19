---
name: research-reprompter
description: >
  将初步的研究问题转化为可执行的 USACF 研究任务。  
  适用于用户输入“进行研究”、“调查这个主题”、“深入研究”或提及某个研究课题的情况。该系统能够生成完整的多智能体集群配置方案，包括算法选择、Claude-Flow 命令以及对抗性评估流程。
compatibility: |
  Full features require Claude Code with claude-flow installed (npx claude-flow@alpha).
  Core prompt generation works on all Claude surfaces.
metadata:
  version: 2.0.0
---
# Researcher v2.0（USACF研究生成器）

> **Claude Code的语音到研究工程：将粗略的研究问题转化为可执行的USACF集群配置。**

## 更新日志

| 版本 | 变更内容 |
|---------|---------|
| **v2.0** | 完整集成USACF框架：算法选择、Claude-flow命令、对抗性审查、事实核查、命名空间管理 |
| v1.0 | 基于Reprompter v4.1的初始版本 |

## 使用目的

使用USACF框架将您粗略的研究问题转化为完整、可执行的多智能体研究提示。

**问题：**
- 研究问题通常模糊且缺乏结构
- 手动配置研究集群非常繁琐
- 缺乏对抗性审查会导致遗漏关键信息
- 没有系统的算法选择机制

**解决方案：**
通过智能对话流程，生成包含所有阶段、智能体和命令的USACF超级提示。

---

## 流程（4个步骤）

### 第1步：接收原始输入
接受用户提出的粗略研究问题（可以是口述的、输入混乱的或不完整的）。

**触发词：** `research`（研究）、`investigate`（调查）、`deep dive`（深入研究）、`analyze`（分析）、`research this`（研究这个）

### 第2步：复杂度检测
**自动检测问题复杂度以选择合适的算法：**
- 简单（<20个词，单一主题） → 使用Chain-of-Thought（CoT）算法，1-3个智能体
- 中等复杂度（有分支结构、需要比较） → 使用Tree-of-Thought（ToT）算法，4-8个智能体
- 复杂（涉及多个领域、需要全面分析） → 使用Graph-of-Thought（GoT）算法，9-15个智能体

### 第3步：智能对话（收集用户信息）
收集以下信息：
1. **研究标题**：本次研究的名称
2. **研究主题**：我们正在研究的内容
3. **主题类型**：产品/软件/业务/流程/组织
4. **研究类型**：竞争分析/市场调研/技术评估/尽职调查
5. **研究目标**：需要了解的信息（每条目标1-20个，逐条列出）
6. **限制条件**：研究重点或范围（可选）
7. **研究深度**：CoT/ToT/GoT
8. **研究输出形式**：简要报告/完整报告/行动计划/原始数据

### 第4步：生成USACF超级提示及评分
生成完整的可执行配置，包括：
- 初始化命令
- 所有阶段的智能体（发现、分析、对抗性评估、综合）
- 内存操作流程
- 最终报告生成器
- 质量评分结果

---

## 关键要求：必须生成完整的超级提示

**对话结束后，您必须立即执行以下操作：**
1. 根据问题的复杂度选择合适的算法（CoT/ToT/GoT）
2. 生成包含所有阶段的完整USACF超级提示
3. 为每个操作添加Claude-flow命令
4. 添加对抗性审查智能体（如“红队”角色、事实核查者）
5. 显示评分结果（对比前后差异）
6. 提供执行建议或提供生成的配置文件

```text
WRONG: Generate simple prompt without agents
RIGHT: Generate full USACF config with all phases, agents, memory ops
```

---

## 算法选择矩阵

| 复杂度 | 算法 | 算法结构 | 智体数量 | 适用场景 |
|------------|-----------|----------|--------|-------------|
| 简单 | Chain-of-Thought (CoT) | 星形结构 | 1-3个智能体 | 适用于单一主题的问题 |
| 中等 | Tree-of-Thought (ToT) | 层级结构 | 4-8个智能体 | 适用于需要比较的问题 |
| 复杂 | Graph-of-Thought (GoT) | 网状/蜂窝结构 | 9-15个以上智能体 | 适用于需要全面分析的问题 |

**复杂度判断标准：**
- 简单：单一主题、事实性问题、少于20个词
- 中等：包含“比较”、“对比”、“评估”等关键词
- 复杂：涉及多个领域、需要综合分析的问题

---

## USACF研究流程（所有阶段均为必选）

### 第0阶段：初始化
```bash
npx claude-flow@alpha init --force
npx claude-flow@alpha swarm init --topology {topology} --max-agents {N}
npx claude-flow@alpha memory store "session/config" '{...}' --namespace search
```

### 第0.5阶段：元分析
- 回顾研究原则和标准
- 自问自答（提出15-20个问题）
- 制定研究计划

### 第1阶段：发现（并行处理）
- 识别研究组件
- 分析系统架构
- 建立系统接口

### 第2阶段：分析（并行处理）
- 6个质量评估专家：评估系统质量、性能、安全性、可用性等
- 4个风险分析师：分析潜在风险（FMEA、边缘情况、漏洞等）

### 第2.5阶段：对抗性审查（关键步骤）
- “红队”专家：对所有发现提出质疑
- 事实核查者：通过网络搜索验证信息准确性
- 协调者：整合反馈并更新研究信心

### 第3阶段：综合（并行处理）
- 快速成果生成器（0-3个月完成）
- 战略规划生成器（3-12个月完成）
- 转型规划生成器（12-36个月完成）
- 帕累托优化器（多目标优化）

### 第4阶段：最终报告
- 极简版报告（3句话总结）
- 执行摘要
- 最重要的10项发现结果及置信度
- 根据时间节点推荐行动方案
- 列出研究限制和不确定性

---

## 命名空间管理规则

所有智能体的数据存储在具有命名空间的内存中：
```bash
# Session
session/config          # Research configuration

# Meta
meta/principles         # Core principles
meta/questions          # Decomposed questions
meta/research-plan      # Planned tasks

# Discovery
discovery/components    # Identified components
discovery/hierarchy     # Structural map
discovery/interfaces    # APIs/contracts
discovery/flows         # Data/control flows

# Gaps
gaps/quality            # Quality gaps
gaps/performance        # Performance gaps
gaps/security           # Security gaps

# Risks
risks/fmea              # Failure mode analysis
risks/edge-cases        # Edge cases
risks/vulnerabilities   # Security vulnerabilities

# Adversarial
adversarial/critiques   # Red team challenges
adversarial/fact-check  # Verified claims

# Opportunities
opportunities/quick-wins        # 0-3 month wins
opportunities/strategic         # 3-12 month plays
opportunities/transformational  # 12-36 month bets
opportunities/pareto-recommendation  # Optimal portfolio

# Output
output/final-report     # Comprehensive report
```

---

## 质量评分标准

**务必展示对比结果：**

| 评估维度 | 对比前 | 对比后 | 变化幅度 |
|-----------|--------|-------|--------|
| 清晰度 | X/10 | X/10 | +X% |
| 算法选择 | 0/10 | 10/10 | +∞ |
| 智体设计 | 0/10 | 9/10 | +∞ |
| 内存管理 | 0/10 | 10/10 | +∞ |
| 对抗性评估 | 0/10 | 9/10 | +∞ |
| 事实核查 | 0/10 | 8/10 | +∞ |
| **总体评分** | X/10 | 9+/10 | +2000%+ |

---

## 示例

**输入（粗略问题）：**  
> “研究Solana在AI领域的进展，以及我们如何与之竞争。”

**输出（生成的USACF超级提示）：**

```markdown
# USACF Research: Solana AI Competitive Analysis

## Configuration
- Algorithm: ToT (medium complexity - comparison)
- Topology: Hierarchical
- Agents: 8
- Output: Executive Brief

## Phase 0: Initialization
[claude-flow init commands]

## Phase 1: Discovery
[4 parallel agents with memory stores]

## Phase 2: Analysis
[Gap hunters + risk analysts]

## Phase 2.5: Adversarial
[Red team + fact checker]

## Phase 3: Synthesis
[Opportunity generators + pareto optimizer]

## Phase 4: Report
[Final report generator]

Quality: 1.2/10 → 9.3/10 (+675%)
```

---

## 优化建议：

- **明确指定竞争对手**：在输入中提及竞争对手的名称
- **提前说明限制条件**：例如“专注于Q1（特定问题）”
- **明确研究目标**：即使目标较为模糊，也要明确说明
- **请求详细信息**：对于简单问题，可以请求更详细的信息
- **选择快速方案**：对于简单研究，可以选择快速生成方案

---

## Reprompter与Researcher的对比

| 对比项 | Reprompter | Researcher |
|--------|------------|------------|
| **触发词** | “reprompt”（重复提示） | “research”（研究）/“researcher”（研究工具） |
| **用途** | 生成通用提示 | 生成具体的研究配置 |
| **输出结果** | 结构化提示 | 可执行的USACF集群配置 |
| **智能体数量** | 无 | 8-15个并行智能体 |
| **内存管理** | 无 | 全面命名空间管理系统 |
| **对抗性评估** | 无 | 包含“红队”和事实核查功能 |
| **算法选择** | 无 | 自动选择CoT/ToT/GoT算法 |

---

---

# 注意：此文档为技术文档，具体实现细节（如代码块）请参考源代码或相关文档。