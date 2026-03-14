---
name: openclaw-continuous-learning
slug: openclaw-continuous-learning
version: 1.2.1
description: >
  基于本能的学习系统，专为 OpenClaw 设计。该系统能够分析用户会话数据、识别行为模式、生成具有置信度评分的学习成果，并提出优化建议，以促进 AI 代理的自我进化。
  该系统与代理的自我改进机制协同工作，实现全面的学习过程：结合内部会话数据分析和外部用户反馈来提升代理的性能。
  适用场景：当你希望 AI 代理能够从自身行为中学习、持续改进、发现优化机会，或构建一个具备自我进化能力的自动化系统时，可以使用该系统。
  不适用场景：当需要代理保持静态行为（即行为模式不随时间变化）时，不建议使用该系统。
triggers:
  - continuous learning
  - self improving agent
  - agent evolution
  - pattern detection
  - session analysis
  - ai learning
  - agent optimization
  - automation improvement
  - self evolution
metadata:
  openclaw:
    emoji: "🧠"
    requires:
      bins: ["node"]
---
# 人工智能代理的持续学习机制

这是一种基于直觉的学习系统，通过观察和模式识别帮助人工智能代理不断提升自身能力。

## 该技能的功能

- **分析会话历史**：回顾代理的交互行为及输出结果。
- **检测模式**：识别重复出现的行为、偏好和工作流程。
- **生成学习策略**：生成带有置信度评分的学习建议。
- **提出优化方案**：基于观察到的行为模式提出改进措施。
- **实现自我进化**：将分析结果转化为实际的改进方案。

## 适用场景

- **适用于构建能够自我提升的人工智能代理**。
- **希望代理能够从交互中学习**。
- **希望发现优化机会**。
- **需要创建具有适应性的自动化系统**。
- **需要追踪行为模式**。

## 不适用场景

- **当需要稳定的、不变的行为模式时**。
- **没有会话历史数据时**。
- **仅适用于简单、确定性的工作流程时**。

## 架构

```
~/.openclaw/agents/ (session .jsonl files)
        │
        ▼
┌───────────────────────────────────────────┐
│ analyze.mjs                                │
│ • Reads session history                   │
│ • Extracts tool calls & errors             │
│ • Detects patterns                         │
└───────────────────────────────────────────┘
        │
        ▼
┌───────────────────────────────────────────┐
│ memory/learning/                           │
│ • instincts.jsonl (atomic learnings)       │
│ • patterns.json (aggregated)              │
│ • optimizations.json (suggestions)         │
└───────────────────────────────────────────┘
```

## 外部反馈（子技能）

该技能与 **agent-self-improvement**（ClawHub）配合使用，以收集外部用户的反馈：
- **内部学习**：由该技能负责会话分析。
- **外部学习**：通过 `SKILL:agent-self-improvement` 收集用户反馈。

### 综合使用方法

```
# Nightly: Internal analysis
SKILL:openclaw-continuous-learning --analyze

# After any output: Capture feedback
SKILL:agent-self-improvement --job <task> --feedback "<user response>"

# Daily: Generate combined improvements
SKILL:agent-self-improvement --improve all
```

### 反馈流程

```
User Response → agent-self-improvement → Directive Hints
        ↓
Session Analysis → openclaw-continuous-learning → Internal Patterns
        ↓
Combined Insights → Agent Optimization
```

这两个技能会将学习结果存储在 `memory/learning/` 目录中，并可以相互引用数据。

## 置信度评分机制

| 评分 | 含义 | 行为 |
|-------|---------|----------|
| 0.3 | 借鉴性建议 | 建议性措施，但不强制执行 |
| 0.5 | 中等可靠性 | 在适用情况下自动执行 |
| 0.7 | 高可靠性 | 自动批准执行 |
| 0.9 | 核心行为 | 必须始终执行 |

**置信度评分会提高的情况**：
- 观察到的行为模式反复出现。
- 用户未对行为进行纠正。
- 多次观察结果一致。

**置信度评分会降低的情况**：
- 用户明确表示反对该行为。
- 最近未观察到该行为模式。
- 出现与该模式矛盾的证据。

## 关键概念

### 学习策略（Instincts）

学习策略是指通过学习获得的小型行为规则。

```yaml
id: prefer-simplicity
trigger: "when solving problems"
confidence: 0.7
domain: problem_solving
---
# Prefer Simple Solutions

## Action
Always choose the simplest solution that meets requirements.

## Evidence
- Observed preference for minimal code
- User corrected over-engineered approaches
```

### 行为模式（Patterns）

按类别汇总的观察结果：
- 代码风格（code_style）
- 测试（testing）
- 版本控制（git）
- 调试（debugging）
- 工作流程（workflow）
- 交流方式（communication）

### 优化措施（Optimizations）

根据行为模式制定的可执行改进方案。

## 使用案例

### 1. 代理自我提升（Agent Self-Improvement）

```
Agent observes its own sessions:
- What works consistently?
- What gets corrected?
- What patterns emerge?

Creates instincts → Applies high-confidence patterns
```

### 2. 学习用户偏好（Learning User Preferences）

```
Learn user preferences from interactions:
- Coding style preferences
- Communication preferences
- Workflow preferences

Adapt behavior accordingly
```

### 3. 性能优化（Performance Optimization）

```
Detect performance patterns:
- Slow operations
- Bottlenecks
- Optimization opportunities

Suggest improvements
```

### 4. 错误模式检测（Error Pattern Detection）

```
Track error patterns:
- Common failures
- Resolution strategies
- Prevention approaches

Build error-handling instincts
```

## 快速入门指南

```bash
# Analyze sessions (reads agent .jsonl files from ~/.openclaw/agents/)
cd ~/.openclaw/workspace/skills/openclaw-continuous-learning
node scripts/analyze.mjs

# List learned instincts
node scripts/analyze.mjs instincts

# Show optimizations
node scripts/analyze.mjs list

# Show error patterns
node scripts/analyze.mjs errors
```

## 设置步骤

### 1. 创建存储目录

```bash
mkdir -p ~/.openclaw/workspace/memory/learning
```

### 2. 安排定期分析

通过 cron 任务定期执行分析：

```json
{
  "id": "continuous-learning",
  "schedule": "0 22 * * *"
}
```

### 3. 与每日优化建议集成

将分析结果整合到每日优化建议中。

## 文件结构

```
~/.openclaw/workspace/
└── memory/
    └── learning/
        ├── instincts.jsonl    # Atomic learnings
        ├── patterns.json      # Aggregated patterns
        └── optimizations.json # Suggestions
```

## 示例输出

```
🧠 Learning Report

Patterns Detected:
- prefer-simplicity (0.7) ↑2
- test-first (0.5) ↑1
- commit-often (0.3) new

Confidence Changes:
- minimal-code: 0.5 → 0.7

Suggested:
1. Prioritize simple solutions
2. Add pre-commit hooks
3. Enable stricter typing
```

## 最佳实践

1. **从简单场景开始**：先处理少量模式，初始置信度较低。
2. **频繁验证**：定期检查模式的有效性。
3. **审慎应用建议**：不要自动执行所有建议。
4. **动态调整置信度**：根据分析结果更新评分。
5. **导出/分享**：整理常见行为模式，形成知识库。

## 常见问题解答

**这与传统的内存系统有何不同？**
传统的内存系统用于存储事实数据，而该系统则用于学习行为模式和用户偏好。

**需要多长时间才能看到效果？**
效果取决于会话数据量。通常需要 1-2 周才能识别出有意义的行为模式。

**自动执行建议安全吗？**
仅对置信度较高的建议（0.7 分以上）进行自动执行。务必先审核建议内容。

## 相关技能

- **skill-engineer**：负责技能的质量管理和开发流程。
- **compound-engineering**：负责会话分析和学习过程。
- **memory-setup**：负责配置内存系统。
- **openclaw-daily-tips**：提供每日优化建议。

---

**版本：1.1.0**  
**灵感来源：** Anthropic 的持续学习机制以及 Claude Code 的相关技术。