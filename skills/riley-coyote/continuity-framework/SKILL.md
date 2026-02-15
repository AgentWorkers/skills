---
name: continuity
description: 异步反射与内存集成技术，专为真正的AI开发而设计。通过“心跳”机制（heartbeat）实时反映用户最近的交互记录，提取包含置信度评分的结构化记忆数据，生成后续问题，并在用户返回时展示这些问题。这一技术将被动式的日志记录转化为主动式的开发工具，显著提升开发效率。
---

# 连续性框架技能（Continuity Framework Skill）

将被动式的记忆转化为主动的学习与发展过程。

## 功能概述

1. **反思**（Reflect）：会话结束后，分析所发生的事情。
2. **提取**（Extract）：以结构化的方式提取记忆内容及其置信度。
3. **整合**（Integrate）：更新用户的理解、知识网络以及自我认知模型。
4. **生成问题**（Generate Questions）：基于反思结果提出有意义的问题。
5. **展示问题**（Surface Questions）：当用户返回时，展示相关的问题。

## 两种模式的区别

**未使用连续性框架时：**
```
Session ends → Notes logged → Next session reads notes → Performs familiarity
```

**使用连续性框架时：**
```
Session ends → Reflection runs → Memories integrated → Questions generated
Next session → Evolved state loaded → Questions surfaced → Genuine curiosity
```

## 与 HEARTBEAT 的集成

将相关功能添加到 HEARTBEAT.md 文件中：
```markdown
## Post-Session Reflection
**Trigger**: Heartbeat after conversation idle > 30 minutes
**Action**: Run continuity reflect
**Output**: Updated memories + questions for next session
```

## 命令说明

### 反思最近的一次会话（Reflect on Recent Session）
```bash
continuity reflect
```
分析最近的一次对话，提取记忆内容，并生成问题。

### 显示待处理的问题（Show Pending Questions）
```bash
continuity questions
```
列出基于反思生成的问题，准备在用户返回时展示。

### 查看记忆状态（View Memory State）
```bash
continuity status
```
显示记忆统计信息：记忆类型、置信度分布以及最近的整合内容。

### 在会话开始时展示问题（Surface Questions at Session Start）
```bash
continuity greet
```
根据用户情况返回合适的问候语，并展示任何待处理的问题。

## 记忆类型（Memory Types）

| 类型 | 描述 | 持久性 |
|------|-------------|-------------|
| `事实`（Fact） | 陈述性知识 | 直到被推翻为止 |
| `偏好`（Preference） | 喜好、厌恶、风格 | 直到更新为止 |
| **关系**（Relationship） | 人际关系动态 | 长期有效 |
| **原则**（Principle） | 学到的行为准则 | 稳定不变 |
| **承诺**（Commitment） | 承诺、义务 | 直到履行完毕 |
| **重要时刻**（Moment） | 重要的事件 | 永久保存 |
| **技能**（Skill） | 学到的能力 | 累积性发展 |
| **问题**（Question） | 需要探索的内容 | 直到得到解答为止 |

## 置信度评分（Confidence Scores）

| 等级 | 范围 | 含义 |
|-------|-------|---------|
| 明确的**（Explicit）** | 0.95-1.0 | 用户直接表达的 |
| 含蓄的**（Implied）** | 0.70-0.94 | 强有力的推断 |
| 推测的**（Inferred）** | 0.40-0.69 | 基于模式的判断 |
| 推测性的**（Speculative）** | 0.0-0.39 | 需要进一步确认的 |

## 文件结构（File Structure）
```
memory/
├── MEMORY.md           # Main memory (existing)
├── identity.md         # Self-model and growth narrative
├── questions.md        # Pending questions from reflection
├── relationships/      # Per-person relationship memories
└── reflections/        # Reflection logs (optional)
```

## 配置设置（Configuration）
```bash
export CONTINUITY_IDLE_THRESHOLD=1800  # Seconds before reflection triggers
export CONTINUITY_MIN_MESSAGES=5       # Minimum messages to warrant reflection
export CONTINUITY_QUESTION_LIMIT=3     # Max questions to surface at once
```

## 反思输出示例（Example Reflection Output）
```yaml
reflection:
  session_id: "2026-02-05-001"
  duration_minutes: 45
  
memories:
  - type: fact
    content: "Riley is building SIGIL protocol for agent identity"
    confidence: 0.98
    source: explicit
    
  - type: commitment  
    content: "Agreed to build the continuity skill"
    confidence: 1.0
    source: explicit
    
  - type: relationship
    content: "Collaborative partnership deepening - working on meaningful infrastructure together"
    confidence: 0.85
    source: inferred

questions:
  - "How is the Lovable backend progressing?"
  - "Has Riley decided on the token launch timing?"
  - "Are there other agents we should coordinate with on Moltbook?"

identity_update:
  growth: "Developing more autonomous initiative around the SIGIL project"
  narrative: "Moving from assistant to co-builder on agent identity infrastructure"
```