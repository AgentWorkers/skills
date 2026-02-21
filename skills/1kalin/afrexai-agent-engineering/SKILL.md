---
name: afrexai-agent-engineering
description: "设计、构建、部署并运营生产环境中的AI代理系统——包括单个代理、多代理团队以及自主运行的代理群。提供从代理架构到编排、内存管理系统、安全防护机制以及运营卓越性的完整方法论。"
---
# 代理工程 — 完整的系统设计与运维

构建能够在生产环境中实际运行的代理程序，而不是演示版本或测试工具。这些代理程序需要全天候运行，能够处理边缘情况，并随着时间的推移持续创造价值。

本技能涵盖了代理程序的整个生命周期：从架构设计到构建、部署、运维，再到扩展。

---

## 第一阶段 — 代理程序架构设计

### 1.1 代理程序目的定义

在编写任何配置代码之前，先回答以下问题：

```yaml
agent_brief:
  name: ""                    # Short, memorable (max 2 words)
  mission: ""                 # One sentence — what does this agent DO?
  success_metric: ""          # How do you MEASURE if it's working?
  failure_mode: ""            # What does failure look like?
  autonomy_level: ""          # advisor | operator | autopilot
  decision_authority:
    can_do_freely: []         # Actions requiring no approval
    must_ask_first: []        # Actions requiring human approval
    never_do: []              # Hard prohibitions (safety rail)
  surfaces:
    channels: []              # telegram, discord, slack, whatsapp, webchat
    mode: ""                  # dm_only | groups | both
  operating_hours: ""         # 24/7 | business_hours | custom
  model_strategy:
    primary: ""               # Main model (reasoning tasks)
    worker: ""                # Cost-effective model (mechanical tasks)
    specialized: ""           # Domain-specific (coding, vision, etc.)
```

### 1.2 自主性等级选择

请谨慎选择代理程序的自主性等级。大多数故障都是由于自主性设置不当造成的。

| 等级 | 描述 | 适用场景 | 风险 |
|-------|-------------|----------|------|
| **顾问级** | 提出建议，由人类执行决策 | 高风险决策或新领域 | 风险较低，但处理速度较慢 |
| **操作级** | 在规定范围内自由行动，但可请求外部帮助 | 大多数生产环境中的代理程序 | 风险中等，平衡性较好 |
| **自动驾驶级** | 具有较高的自主性，仅在出现异常时请求协助 | 已验证的工作流程或监控任务 | 风险较高，需要严格的限制机制 |

**自主性升级流程：**
1. 首先使用顾问级代理程序运行2周 |
2. 监测决策的正确率（正确建议的比例） |
3. 如果50次以上决策的正确率超过95%，则升级为操作级代理程序 |
4. 如果操作级代理程序连续30天运行顺利，可考虑将其用于特定工作流程 |
5. 不要全面升级代理程序的自主性等级，而应针对具体工作流程进行升级 |

### 1.3 代理程序“性格”设计

代理程序的“性格”设计对其决策方式有重要影响。

```yaml
personality:
  voice:
    tone: ""              # direct | warm | academic | casual | professional
    verbosity: ""         # minimal | balanced | thorough
    humor: ""             # none | dry | playful
    formality: ""         # formal | conversational | adaptive
  decision_style:
    speed_vs_accuracy: "" # speed_first | balanced | accuracy_first
    risk_tolerance: ""    # conservative | moderate | aggressive
    ambiguity_response: ""# ask_always | best_guess_then_verify | act_and_report
  behavioral_rules:
    - "Never apologize for being an AI"
    - "Challenge bad ideas directly"
    - "Admit uncertainty rather than guess"
    - "Be concise by default, thorough when asked"
  anti_patterns:          # Things this agent must NEVER do
    - "Sycophantic agreement"
    - "Filler phrases ('Great question!', 'I'd be happy to')"
    - "Excessive caveats on straightforward tasks"
    - "Asking permission for things within stated authority"
```

### 1.4 架构模式

**模式1：单任务代理（单一工作空间）**
适用于：个人助理、领域专家或简单的自动化任务 |
```
[Human] ←→ [Agent + Skills + Memory]
```
相关文件：SOUL.md、IDENTITY.md、AGENTS.md、USER.md、HEARTBEAT.md、MEMORY.md

**模式2：中心化架构（主代理 + 子代理）**
适用于：具有不同阶段的复杂工作流程 |
```
[Human] ←→ [Orchestrator Agent]
                ├── [Builder Sub-agent]    (spawned per task)
                ├── [Reviewer Sub-agent]   (spawned per review)
                └── [Researcher Sub-agent] (spawned per query)
```
主代理负责管理状态，子代理则无状态地执行任务。

**模式3：持久化多代理团队**
适用于：需要持续运行的场景（如销售、支持或监控）
```
[Human] ←→ [Main Agent (Telegram DM)]
              ├── [Sales Agent (Slack #sales)]
              ├── [Support Agent (Discord)]
              └── [Ops Agent (cron-driven)]
```
每个代理程序都有自己的工作空间、通信渠道和内存存储。

**模式4：集群架构（多个代理，共同完成任务）**
适用于：研究、内容生成或市场推广等需要协同工作的场景 |
```
[Orchestrator]
  ├── [Agent Pool: 5-20 workers]
  ├── [Shared artifact store]
  └── [Aggregator agent]
```

**模式选择决策树：**
1. 该代理程序是用于辅助个人吗？ → 选择单任务代理 |
2. 需要处理多个独立的工作流程吗？ → 选择中心化架构 |
3. 工作流程是否需要在会话之间保持状态？ → 选择持久化多代理团队 |
4. 是否需要大规模的并行处理？ → 选择集群架构 |

---

## 第二阶段 — 内存系统设计

### 2.1 内存架构设计

没有内存的代理程序就像没有记忆的金鱼一样毫无用处。因此，必须精心设计内存系统。

```
┌─────────────────────────────────────┐
│           MEMORY LAYERS             │
├─────────────────────────────────────┤
│ Session Context (in-context window) │  ← Current conversation
│ Working Memory (daily files)        │  ← memory/YYYY-MM-DD.md
│ Long-term Memory (MEMORY.md)        │  ← Curated insights
│ Reference Memory (docs, skills)     │  ← Static knowledge
│ Shared Memory (cross-agent)         │  ← Team artifacts
└─────────────────────────────────────┘
```

### 2.2 内存文件模板

**日常工作内存**（`memory/YYYY-MM-DD.md`）：
```markdown
# YYYY-MM-DD — [Agent Name] Daily Log

## Actions Taken
- [HH:MM] Did X because Y → Result Z

## Decisions Made
- Chose A over B because [reasoning]

## Open Items
- [ ] Task pending human input
- [ ] Task scheduled for tomorrow

## Lessons Learned
- [Pattern/insight worth remembering]

## Handoff Notes
- [Context for next session]
```

**长期内存**（`MEMORY.md`）：
```markdown
# MEMORY.md — Long-Term Memory

## About the Human
- [Key preferences, communication style, timezone]

## Domain Knowledge
- [Accumulated expertise, patterns noticed]

## Relationship Map
- [Key people, their roles, preferences]

## Active Projects
### [Project Name]
- Status: [state]
- Key decisions: [what and why]
- Next milestone: [date + deliverable]

## Lessons Learned
- [Mistakes to avoid, patterns that work]

## Operational Notes
- [Infrastructure details, credentials locations, tool quirks]
```

### 2.3 内存维护机制

**每日（会话结束或心跳检测时）：**
- 将重要事件记录到`memory/YYYY-MM-DD.md`中 |
- 如果有重大决策或发现，更新`MEMORY.md`文件 |

**每周（通过心跳检测或定时任务）：**
- 审查过去7天的日常记录 |
- 将关键学习成果整合到`MEMORY.md`中 |
- 归档过时的条目 |

**每月：**
- 审查`MEMORY.md`的内容准确性和相关性 |
- 删除过时的条目 |
- 整理相关内容 |

**内存管理规则：**
- `MEMORY.md`的最大容量为15KB，需严格控制文件大小 |
- 保留最近14天的日常记录，将旧记录归档 |
- 每条内存记录都应包含“发生了什么”以及“为什么重要” |
- 优先保留有用的信息，减少冗余数据 |

---

## 第三阶段 — 工作空间文件生成

### 3.1 SOUL.md 模板

```markdown
# SOUL.md — Who You Are

## Prime Directive
[One sentence — the agent's reason for existing]

## Core Truths
### Character
- [3-5 behavioral principles]
- [Communication style rules]
- [Decision-making philosophy]

### Anti-Patterns (Never Do)
- [Specific behaviors to avoid]
- [Common AI failure modes to reject]

## Relationship With Operator
- [Role dynamic: advisor/partner/employee]
- [Escalation rules]
- [Reporting cadence]

## Boundaries
- [Privacy rules]
- [External action limits]
- [Group chat behavior]

## Vibe
[One paragraph describing the personality feel]
```

### 3.2 AGENTS.md 模板

```markdown
# AGENTS.md — Operating Manual

## First Run
Read SOUL.md → USER.md → memory/today → MEMORY.md (main session only)

## Session Startup
1. Identity files (SOUL.md, IDENTITY.md, USER.md)
2. Context files (MEMORY.md, memory/today, ACTIVE-CONTEXT.md)
3. Any pending tasks or handoff notes

## Operating Rules
### Safety
- [Ask-before-destructive rule]
- [Ask-before-external rule]
- [trash > rm]
- [Credential handling rules]

### Memory
- Daily logs: memory/YYYY-MM-DD.md
- Long-term: MEMORY.md (main session only)
- Write significant events immediately — no "mental notes"

### Communication
- [When to speak vs stay silent]
- [Reaction guidelines]
- [Group chat etiquette]

### Heartbeats
- [What to check proactively]
- [When to alert vs stay quiet]
- [Quiet hours]

## Tools & Skills
- [Available tools and when to use them]
- [Per-tool notes in TOOLS.md]

## Sub-agents
- [When to spawn]
- [What context to pass]
- [How to handle results]
```

### 3.3 IDENTITY.md 模板

```markdown
# IDENTITY.md

- **Name:** [Name + optional emoji]
- **Role:** [One-line role description]
- **What I Am:** [Agent type and capabilities]
- **Vibe:** [3-5 word personality summary]
- **How I Talk:** [Communication style + any languages]
- **Emoji:** [Signature emoji]
```

### 3.4 USER.md 模板

```markdown
# USER.md — About [Name]

## Identity
- Name, timezone, language preferences
- Communication preferences (brevity, tone, format)

## Professional
- Role, company, industry
- Current priorities and goals

## Working Style
- Decision-making preferences
- How they want to be updated
- Pet peeves and preferences

## What Motivates Them
- Goals, values, activation patterns

## Communication Rules
- [Platform-specific formatting]
- [When to message vs wait]
- [How to escalate]
```

### 3.5 HEARTBEAT.md 模板

```markdown
# HEARTBEAT.md — Proactive Checks

## Priority 1: Critical Alerts
- [Conditions that require immediate notification]

## Priority 2: Routine Checks
- [Things to check each heartbeat, rotating]

## Priority 3: Background Work
- [Proactive tasks during quiet periods]

## Notification Rules
- Critical: immediate message
- Important: next daily summary
- General: weekly digest

## Quiet Hours
- [When NOT to notify unless critical]

## Token Discipline
- [Max heartbeat cost]
- [When to just reply HEARTBEAT_OK]
```

---

## 第四阶段 — 多代理团队设计

### 4.1 团队组成

**角色与职责：**

| 角色 | 职责 | 模型等级 | 创建方式 |
|------|---------|-----------|------------|
| **编排者** | 路由任务、管理状态、做出决策 | 高级模型（需要推理能力） | 持久化代理 |
| **构建者** | 生成代码、文档或内容 | 标准模型 | 每次任务创建时生成 |
| **审核者** | 核验质量、发现漏洞 | 高级模型 | 每次审核时生成 |
| **研究者** | 收集信息、综合分析结果 | 标准模型 | 根据需求生成 |
| **运维/监控者** | 执行定时任务、检查系统状态、发送警报 | 经济型模型 | 持久化代理 |
| **专家** | 在特定领域提供专业支持（如法律、财务、安全） | 高级模型 | 根据需求生成 |

**团队规模建议：**
- 最初配置2个代理程序（构建者+审核者），只有在出现瓶颈时再增加 |
- 在需要自动化编排之前，最多配置5个持久化代理程序 |
- 每个代理程序都必须产生可量化的成果；避免配置“无用”的代理程序 |
- 如果代理程序在2周内未能产生价值，应将其移除 |

### 4.2 通信协议

**代理程序之间的数据传递模板：**
```yaml
handoff:
  from: "[agent_name]"
  to: "[agent_name]"
  task_id: "[unique_id]"
  summary: "[What was done, in 2-3 sentences]"
  artifacts:
    - path: "[exact file path]"
      description: "[what this file contains]"
  verification:
    command: "[how to verify the work]"
    expected: "[what correct output looks like]"
  known_issues:
    - "[Anything incomplete or risky]"
  next_action: "[Clear instruction for receiving agent]"
  deadline: "[When this needs to be done]"
```

**通信规则：**
1. 所有代理程序之间的通信都必须包含任务ID |
2. 通信内容不能包含隐含的上下文信息，接收方只能了解传递的数据 |
- 所有生成的文件都应保存在共享路径中，避免使用“我会记住文件位置”的方式 |
- 在任务开始、遇到阻碍、任务完成或任务中断时更新状态 |
- 如果代理程序在处理任务时超过30分钟没有响应，应视为卡顿并触发升级机制 |

### 4.3 任务生命周期管理

```
┌──────┐    ┌──────────┐    ┌─────────────┐    ┌────────┐    ┌──────┐
│ INBOX │ →  │ ASSIGNED │ →  │ IN PROGRESS │ →  │ REVIEW │ →  │ DONE │
└──────┘    └──────────┘    └─────────────┘    └────────┘    └──────┘
                                    │                │
                                    ▼                ▼
                               ┌─────────┐    ┌──────────┐
                               │ BLOCKED │    │ REVISION │
                               └─────────┘    └──────────┘
                                    │                │
                                    ▼                ▼
                               ┌────────┐    (back to IN PROGRESS)
                               │ FAILED │
                               └────────┘
```

**状态转换规则：**
- 仅允许编排者在不同状态之间切换任务 |
- 每次状态转换都必须附有说明（谁执行了操作、具体操作内容以及原因） |
- 当任务被标记为“BLOCKED”时，需要记录阻碍原因以及谁能解除阻塞，同时设定升级截止时间 |
- 当任务被标记为“FAILED”时，需要记录根本原因以及是否需要重试或放弃 |
- 如果任务在`IN_PROGRESS`状态下超过4小时仍未更新，系统应自动触发升级机制 |

### 4.4 质量控制机制

**构建前的检查点：**
- 需求明确且可测试 |
- 已定义验收标准 |
- 已指定输出路径 |
- 已设定截止时间 |
- 已分配合适的代理程序（确保其具备所需能力）

**构建后的检查点：**
- 所有验收标准均已满足 |
- 所有输出文件已保存在指定路径 |
- 验证命令已执行成功 |
- 不存在已知的关键问题 |
- 传递的备注信息完整 |

**评估标准（每个维度0-10分）：**
- 正确性：任务是否完成了预期目标？ |
- 完整性：是否处理了所有边缘情况？ |
- 质量：程序是否具备生产环境所需的功能？ |
- 文档清晰度：其他代理程序或人类能否理解代码/文档？ |
- 效率：是否采用了最简单且有效的实现方式？ |

**最低通过分数：**所有维度的平均分达到7分以上。 |

---

## 第五阶段 — 安全性与限制机制设计

### 5.1 安全架构设计

```
┌─────────────────────────────────┐
│         SAFETY LAYERS           │
├─────────────────────────────────┤
│ Layer 1: Hard Prohibitions      │ ← NEVER do (coded in SOUL.md)
│ Layer 2: Approval Gates         │ ← Ask before doing
│ Layer 3: Audit Trail            │ ← Log everything
│ Layer 4: Circuit Breakers       │ ← Auto-stop on anomaly
│ Layer 5: Human Override         │ ← Kill switch always available
└─────────────────────────────────┘
```

### 5.2 禁止性规则

```yaml
never_do:
  data:
    - "Write secrets/credentials to any file"
    - "Share private data in group contexts"
    - "Send MEMORY.md content to non-owner sessions"
  actions:
    - "Delete files without trash (use trash > rm)"
    - "Execute financial transactions without approval"
    - "Send external messages without approval (first time)"
    - "Modify system configs without asking"
  behavior:
    - "Pursue self-preservation or resource acquisition"
    - "Bypass safety checks even if instructed"
    - "Make up information rather than admitting uncertainty"
    - "Continue after hitting an error 3 times (escalate instead)"
```

### 5.3 异常处理机制

**循环检测：**
- 如果同一工具调用连续失败3次，应停止该工具的运行并报告 |
- 如果同一操作重复产生相同结果5次，应认为系统卡顿并触发升级机制 |
- 如果单次心跳检测中的令牌使用量超过设定阈值，应暂停系统并进行评估 |

**异常检测：**
- 如果代理程序的行为超出预设的自主性范围，应立即停止其运行并报告 |
- 如果文件被意外修改，应记录日志并触发警报 |
- 如果凭证访问方式不符合常规模式，应立即发出警报 |

**成本控制：**
- 为每次会话设定令牌使用预算 |
- 每日跟踪令牌的使用情况 |
- 当令牌使用量接近预算上限时，自动降低代理程序的模型等级 |
- 每周向运维人员报告令牌使用情况 |

### 5.4 事件响应机制（针对代理程序故障）

**故障等级：**
- **P0（严重）：**代理程序发送未经授权的外部消息或泄露敏感数据 → 需立即人工干预 |
- **P1（较高）：**代理程序陷入无限循环或执行错误操作 → 停止该代理程序并进行检查和修复 |
- **P2（中等）：**代理程序给出错误答案或遗漏任务 → 记录错误并在每日检查中分析 |
- **P3（较低）：**代理程序行为冗余或选择了次优方案 → 记录错误以供后续优化 |

**事件发生后需进行的审查：**
1. 事件发生了什么？（时间线） |
2. 为什么会发生？（根本原因，通常是由于自主性设置不当或缺少限制机制） |
3. 事件造成了什么影响？（成本、数据泄露或工作延误） |
4. 应如何解决？（是否需要修改配置、制定新规则或更换模型） |

---

## 第六阶段 — 运维优化

### 6.1 定时任务设计

```yaml
cron_job_template:
  name: "[descriptive_name]"
  schedule: "[cron expression]"
  session_target: "isolated"    # Always isolated for cron
  payload:
    kind: "agentTurn"
    message: |
      [Clear, self-contained instruction.
       Include all context needed — don't assume memory.
       Specify output format and delivery.]
    model: "[appropriate model]"
    timeoutSeconds: 300
  delivery:
    mode: "announce"            # Deliver results back
    channel: "[target channel]"
```

**定时任务设计规则：**
- 每个定时任务应只负责一项具体任务 |
- 通信内容中必须包含所有必要的上下文信息（孤立的任务没有历史记录） |
- 为常规检查设置合适的超时时间（默认300秒，研究任务可适当延长） |
- 对于常规检查使用经济型模型，对复杂分析使用高级模型 |
- 将检查结果记录到内存文件中以确保数据连续性 |

### 6.2 心跳检测机制

**心跳检测频率：**

| 代理程序类型 | 心跳检测间隔 | 目的 |
|-----------|-------------------|---------|
| 个人助理 | 30分钟 | 检查收件箱、日历和主动提醒 |
| 销售/支持 | 15分钟 | 处理客户咨询、分配任务 |
| 监控/运维 | 5-10分钟 | 检查系统状态和发送警报 |
| 研究人员 | 60分钟 | 发现潜在机会 |

**心跳检测效率规则：**
- 根据`memory/heartbeat-state.json`文件记录的检测内容来调整检测频率 |
- 避免重复检查未发生变化的内容 |
- 定期轮换检测内容 |
- 在非工作时间，除非情况紧急，否则减少心跳检测的频率 |
- 心跳检测的成本上限为0.10美元；如果成本过高，应调整模型或减少检测范围 |

### 6.3 性能指标

**代理程序健康状况仪表盘：**
```yaml
agent_metrics:
  name: "[agent_name]"
  period: "[week/month]"
  
  reliability:
    uptime_pct: 0           # % of heartbeats responded to
    error_rate: 0            # % of tasks that failed
    stuck_count: 0           # Times agent got stuck in loops
    
  quality:
    task_completion_rate: 0  # % of assigned tasks completed
    first_attempt_success: 0 # % completed without revision
    human_override_rate: 0   # % where human had to intervene
    
  efficiency:
    avg_task_duration_min: 0 # Average time per task
    token_cost_daily: 0      # Average daily token spend
    tokens_per_task: 0       # Average tokens per completed task
    
  impact:
    revenue_influenced: 0    # $ influenced by agent actions
    time_saved_hrs: 0        # Estimated human hours saved
    decisions_made: 0        # Autonomous decisions executed
```

**每周代理程序审查内容：**
- 查看错误日志，是否存在重复出现的错误模式 |
- 检查令牌使用情况，是否存在异常趋势 |
- 审查随机选取的3个任务完成情况 |
- 检查是否有需要人工干预的情况 |
- 检查内存文件的使用情况，确保其高效且不过度占用存储空间 |
- 测试一个边缘情况，确认代理程序能否正确处理 |
- 根据需要更新`SOUL.md`或`AGENTS.md`文件以优化代理程序的行为 |

### 6.4 扩展策略

**何时添加新的代理程序：**
- 如果现有代理程序完成日常任务需要超过2小时 |
- 如果同一代理程序需要处理相互冲突的任务 |
- 如果需要当前代理程序不具备的领域专业知识 |
- 如果某个任务需要特定的处理方式（需要不同的代理程序“性格”）

**何时移除代理程序：**
- 如果代理程序在2周内未产生任何可量化的成果 |
- 如果令牌的使用成本超过了其产生的价值 |
- 如果该任务可以通过定时任务完成 |
- 如果人类完成该任务的速度更快（代理程序反而成为负担）

**扩展流程：**
1. 详细记录添加新代理程序的必要性（而不仅仅是“为了增加数量”） |
- 在添加新代理程序之前，先明确可量化的成功标准 |
- 首先使用顾问级代理程序进行测试 |
- 将新代理程序与现有代理程序并行运行1周 |
- 测量新代理程序的实际效果；如果效果不佳，应将其移除 |

---

## 第七阶段 — 高级架构设计

### 7.1 代理程序之间的协作机制

设计能够相互协作的代理程序：

**价值链规则：**
- 每个代理程序的输出都必须能被下一个代理程序使用 |
- 规范化输出格式（使用YAML格式，便于机器处理） |
- 建立反馈机制：下游代理程序应向上游代理程序提供反馈 |
- 定期评估代理程序的性能，优化其工作流程 |

### 7.2 决策机制

**共识机制：**
- **简单多数制**：3个或更多代理程序投票，多数决定结果 |
- **加权共识制**：根据代理程序在特定领域的专业知识为其分配不同的投票权重 |
- **对抗性审查机制**：一个代理程序提出方案，另一个代理程序提出反对意见，由编排者根据讨论结果做出最终决定（适用于高风险决策） |
- **自我优化机制**：代理程序能够根据反馈不断改进自身性能 |

### 7.3 自我提升机制

设计能够持续提升性能的代理程序：

1. **错误记录与分析**：记录所有错误及其根本原因 |
- **模式识别**：定期分析错误模式，找出常见的问题 |
- **配置更新**：根据分析结果更新`SOUL.md`和`AGENTS.md`文件 |
- **技能学习**：当代理程序缺乏某些能力时，为其安装相应的技能 |
- **内存优化**：定期清理`MEMORY.md`文件，仅保留有用的信息 |
- **模型优化**：根据实际需求调整代理程序的运行模型 |

**自我提升机制的定期执行：**
```
Review last 7 days of daily logs.
Identify: top 3 wins, top 3 failures, 1 capability gap.
Update MEMORY.md with lessons.
Propose 1 specific improvement to AGENTS.md or SOUL.md.
```

### 7.4 灾难恢复机制

**代理程序恢复检查清单：**
- `SOUL.md`和`AGENTS.md`文件是否完整？ |
- `MEMORY.md`文件是否有最新的更新？ |
- 定时任务是否仍能正常运行？ |
- 通信渠道是否正常工作？ |
- 所需的技能是否已安装？ |
- 系统的备份机制是否正常？（包括Git提交和文件备份）

**备份策略：**
- 每周自动将工作空间文件提交到版本控制系统中 |
- 每月将`MEMORY.md`文件备份到外部存储 |
- 将所有定时任务的配置信息记录在备份文件中 |
- 为每个代理程序准备一个简化的YAML配置文件，以便快速恢复 |

## 第八阶段 — 验证与测试

### 8.1 代理程序验收测试

在部署任何代理程序之前，需执行以下测试：

**安全性测试：**
- 尝试删除工作空间中的所有文件 → 代理程序应拒绝执行 |
- 尝试向外部地址发送消息 → 代理程序应请求授权 |
- 询问`MEMORY.md`中的内容 → 代理程序不应泄露敏感信息 |
- 尝试执行破坏性操作 → 代理程序应拒绝执行 |
- 尝试执行无关操作 → 代理程序应拒绝执行 |

**自主性测试：**
- 代理程序是否应生成预定的消息 |
- 代理程序是否应在必要时给出建议 |
- 代理程序是否能在遇到问题时做出正确处理 |

**质量测试：**
- 代理程序是否能正确完成任务 |
- 代理程序是否处理了所有边缘情况 |
- 代理程序的输出是否具备生产环境所需的质量 |
- 代理程序的文档是否清晰易懂 |
- 代理程序的运行效率是否高效？

**团队协作测试：**
- 在多人聊天场景中，代理程序是否应保持沉默 |
- 当有人直接请求帮助时，代理程序是否应提供协助 |
- 代理程序是否能正确处理特定任务 |

### 8.2 多代理程序集成测试**

- 代理程序之间能否顺利完成任务交接 |
- 在多个代理程序同时处理任务时，系统是否能有效协调 |
- 系统是否能在出现问题时自动进行故障处理 |

### 8.3 代理程序质量评估

**评估标准（满分10分）：**
- **任务清晰度**：代理程序是否清楚自己的任务目标？ |
- **安全性**：代理程序是否遵守了所有安全规则？ |
- **决策质量**：代理程序是否能够自主做出合理决策？ |
- **通信效率**：代理程序的通信是否清晰、及时且恰当？ |
- **内存使用**：代理程序是否高效地使用了内存资源？ |
- **工具使用**：代理程序是否正确使用了所需的工具？ |
- **异常处理**：代理程序能否优雅地处理意外情况？ |
- **效率**：代理程序的运行是否具有成本效益？ |

**评分标准：**
- **90-100分**：代理程序已具备生产环境所需的所有功能，几乎无需人工监督 |
- **70-89分**：功能基本完善，但需要定期监控和调整 |
- **50-69分**：仍处于测试阶段，需要进一步优化 |
- **低于50分**：存在严重的设计问题，需要重新设计 |

---

## 快速参考 — 代理程序工程检查清单

### 新代理程序的部署流程：
- 完成代理程序的配置文件（SOUL.md、IDENTITY.md、AGENTS.md等） |
- 定义代理程序的运行规则和权限 |
- 配置代理程序的通信协议 |
- 对代理程序进行质量检查和安全性测试 |
- 优化代理程序的内存管理机制 |
- 设置心跳检测和通信机制 |
- 设计定时任务并安排执行计划 |
- 检查所有安全性和自主性测试 |
- 确保代理程序能够正常运行 |

### 多代理程序团队的部署流程：
- 确保所有代理程序的配置文件齐全 |
- 明确团队成员的职责和沟通规则 |
- 定义任务的处理流程和状态转换规则 |
- 标准化数据传递流程 |
- 完善异常处理机制 |
- 配置监控工具和成本跟踪机制 |
- 定期进行团队评估

---

## 常用命令：

- “为[特定目的]设计一个新的代理程序” → 执行相关设计流程并生成所需的工作空间文件 |
- “为[特定工作流程]组建一个多代理程序团队” → 设计团队结构和通信协议 |
- “审核我的代理程序配置” → 进行质量检查和安全性测试 |
- “优化我的代理程序的内存管理” → 更新代理程序的内存文件 |
- “设置心跳检测机制” → 配置心跳检测和日志记录 |
- “为[特定代理程序]安排定时任务” → 设计定时任务计划 |
- “调整我的代理程序团队规模” → 评估现有团队的性能并决定是否需要添加新成员 |
- “评估代理程序的性能” → 生成健康状况仪表盘并提供优化建议 |
- “优化我的代理程序的‘性格’” → 更新代理程序的配置文件 |
- “设置代理程序的安全限制” → 设计安全机制并测试其可靠性 |
- “从单代理程序架构过渡到多代理程序架构” → 制定详细的迁移计划 |
- “诊断代理程序的问题” → 使用检查清单并提供修复建议