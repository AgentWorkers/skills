---
name: reflect
description: >
  通过对话分析实现自我提升：从用户的纠正意见和成功行为模式中提取经验教训，提出对代理程序（agent）文件的更新建议，或开发新的功能/技能。核心理念是“一次纠正，终身受益”。
  适用场景：  
  (1) 用户明确指出行为错误（如“永远不要做X”，“必须始终做Y”）；  
  (2) 会话结束时或需要整理对话内容时；  
  (3) 用户请求对自身行为进行反思；  
  (4) 需要保存某些成功的操作模式或经验时。
version: 2.0.0
author: Claude Code Toolkit
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
---
# Reflect - 自我提升技能

## 快速参考

| 命令 | 功能 |
|---------|--------|
| `/reflect` | 分析对话内容以提取可学习的知识点 |
| `/reflect on` | 启用自动反思功能 |
| `/reflect off` | 禁用自动反思功能 |
| `/reflect status` | 显示当前状态和指标 |
| `/reflect review` | 审查置信度较低的学习内容 |
| `/reflect [agent]` | 专注于特定代理 |

## 核心理念

**“一次改正，永远不再犯错。”**

当用户纠正自己的行为时，这些改正会被永久性地纳入代理系统中，从而在未来的所有会话中发挥作用。

## 工作流程

### 第1步：初始化状态

使用状态管理器检查和初始化状态文件：

```bash
# Check for existing state
python scripts/state_manager.py init

# State directory is configurable via REFLECT_STATE_DIR env var
# Default: ~/.reflect/ (portable) or ~/.claude/session/ (Claude Code)
```

状态文件包括：
- `reflect-state.yaml` - 控制反思状态的开关及待审核的学习内容
- `reflect-metrics.yaml` - 统计相关指标
- `learnings.yaml` - 记录所有已应用的学习内容

### 第2步：扫描对话内容以识别学习信号

使用信号检测器来识别可学习的知识点：

```bash
python scripts/signal_detector.py --input conversation.txt
```

#### 信号置信度等级

| 置信度 | 触发条件 | 例子 |
|------------|----------|----------|
| **高** | 明确的纠正语句 | “never”, “always”, “wrong”, “stop”, “the rule is” |
| **中** | 被认可的处理方式 | “perfect”, “exactly”, “accepted output” |
| **低** | 观察到的有效行为模式 | 未被验证的模式 |

详细规则请参阅 [signal_patterns.md](references/signal_patterns.md)。

### 第3步：分类并匹配到目标文件

将每个信号映射到相应的目标文件：

**学习内容分类：**

| 分类 | 目标文件 |
|----------|--------------|
| 代码风格 | `code-reviewer`, `backend-developer`, `frontend-developer` |
| 架构 | `solution-architect`, `api-architect`, `architecture-reviewer` |
| 流程 | `CLAUDE.md`, `orchestrator agents` |
| 领域知识 | 领域特定的代理脚本, `CLAUDE.md` |
| 新技能 | `.claude/skills/{name}/SKILL.md` |

详细映射规则请参阅 [agent_mappings.md](references/agent_mappings.md)。

### 第4步：判断是否值得创建新技能

某些学习内容更适合被定义为新技能，而非简单的代理更新：

**创建新技能的标准：**
- 需要花费大量时间（超过10分钟）才能解决的调试问题 |
- 错误信息与实际问题原因不符 |
- 通过实验发现的解决方法 |
- 与文档中描述不同的配置设置 |
- 可在类似情况下重复使用的模式 |

**创建新技能的必要条件：**
- [ ] 可复用性：有助于未来的任务 |
- [ ] 非显而易见：需要经过发现而非仅仅依赖文档 |
- [ ] 具体性：能够明确描述触发条件 |
- [ ] 经过验证：解决方案确实有效 |
- [ ] 无重复内容：该技能在系统中尚不存在 |

详细创建新技能的指南请参阅 [skill_template.md](references/skill_template.md)。

### 第5步：生成修改建议

以以下格式生成修改建议：

```markdown
# Reflection Analysis

## Session Context
- **Date**: [timestamp]
- **Messages Analyzed**: [count]
- **Focus**: [all agents OR specific agent name]

## Signals Detected

| # | Signal | Confidence | Source Quote | Category |
|---|--------|------------|--------------|----------|
| 1 | [learning] | HIGH | "[exact words]" | Code Style |
| 2 | [learning] | MEDIUM | "[context]" | Architecture |

## Proposed Agent Updates

### Change 1: Update [agent-name]

**Target**: `[file path]`
**Section**: [section name]
**Confidence**: [HIGH/MEDIUM/LOW]
**Rationale**: [why this change]

```diff
--- a/path/to/agent.md
+++ b/path/to/agent.md
@@ -82,6 +82,7 @@
## 新规则内容
+* 根据学习内容添加的新规则
```

## Proposed New Skills

### Skill 1: [skill-name]

**Quality Gate Check**:
- [x] Reusable: [why]
- [x] Non-trivial: [why]
- [x] Specific: [trigger conditions]
- [x] Verified: [how verified]
- [x] No duplication: [checked against]

**Will create**: `.claude/skills/[skill-name]/SKILL.md`

## Conflict Check

- [x] No conflicts with existing rules detected
- OR: Warning - potential conflict with [file:line]

## Commit Message

```
reflect: 将 [日期] 会话中的学习内容添加到代理中

代理更新：
- [学习内容1的总结]

新技能：
- [技能名称]: [简要描述]

提取到的学习信号：[N] 个（[H] 高置信度，[M] 中置信度，[L] 低置信度）

```

## Review Prompt

Apply these changes?
- `Y` - Apply all changes and commit
- `N` - Discard all changes
- `modify` - Adjust specific changes
- `1,3` - Apply only changes 1 and 3
- `s1` - Apply only skill 1
- `all-skills` - Apply all skills, skip agent updates
```

### 第6步：处理用户反馈

**用户选择“Y”（同意）时：**
1. 使用编辑工具应用每个更改
2. 对修改后的文件执行 `git add`
3. 提交更改并附上说明信息
4. 更新学习记录
5. 更新相关指标

**用户选择“N”（拒绝）时：**
1. 忽略建议的更改
2. 记录拒绝原因以供分析
3. 询问用户是否需要修改某些信号

**用户选择“modify”时：**
1. 逐一展示每个更改内容
2. 允许用户修改建议的添加内容
3. 在应用更改前再次确认

**用户选择部分更改（例如“1,3”）时：**
1. 仅应用指定的更改
2. 记录部分接受的更改
3. 仅提交实际应用的更改

### 第7步：更新指标

```bash
python scripts/metrics_updater.py --accepted 3 --rejected 1 --confidence high:2,medium:1
```

## 控制命令

### 启用自动反思功能

```bash
/reflect on
# Sets auto_reflect: true in state file
# Will trigger on PreCompact hook
```

### 禁用自动反思功能

```bash
/reflect off
# Sets auto_reflect: false in state file
```

### 检查当前状态

```bash
/reflect status
# Shows current state and metrics
```

### 查看待审核的学习内容

```bash
/reflect review
# Shows low-confidence learnings awaiting validation
```

## 输出位置

**项目级（与仓库版本同步）：**
- `.claude/reflections/YYYY-MM-DD_HH-MM-SS.md` - 完整的反思记录
- `.claude/reflections/index.md` - 项目总结
- `.claude/skills/{name}/SKILL.md` - 新创建的技能文档

**全局级（用户级）：**
- `~/.claude/reflections/by-project/{project}/` - 跨项目记录
- `~/.claude/reflections/by-agent/{agent}/learnings.md` - 每个代理的学习记录
- `~/.claude/reflections/index.md` - 全局总结

## 学习内容的存储方式

某些学习内容更适合存储在 **自动记忆库**（`~/.claude/projects/*/memory/MEMORY.md`）中，而非代理文件中：

| 学习类型 | 最适合的存储位置 |
|---------------|-------------|
| 行为纠正（如“始终执行X”） | 代理文件 |
| 项目特定的模式 | MEMORY.md |
| 频繁出现的错误/解决方法 | 新技能文档或 MEMORY.md |
| 工具偏好设置 | CLAUDE.md |
| 领域知识 | MEMORY.md 或相关文档 |

当某个学习内容的置信度较低且属于项目特定内容时，建议将其存储在 MEMORY.md 中，而不是修改代理脚本。

## 安全措施

### 人工审核机制
- 未经用户明确同意，严禁应用任何更改
- 应在应用更改前显示完整的差异内容
- 允许用户选择性地应用更改

### Git版本控制
- 所有更改都需附有描述性信息
- 可通过 `git revert` 快速回滚更改
- 保留学习历史记录

### 增量更新
- 仅向现有内容添加新内容
- 禁止删除或重写现有规则
- 保持原始文件结构

### 冲突检测
- 检查新规则是否与现有规则冲突
- 发现冲突时提醒用户
- 提供解决方案建议

## 集成机制

### 与 /handover 功能集成
如果启用了自动反思功能，`PreCompact` 钩子会在任务交接前触发反思流程。

### 与会话状态集成
当会话的上下文信息达到70%以上（状态显示为黄色）时，系统会提示用户执行 `/reflect` 命令。

### 钩子集成（Claude代码）
该技能包含用于自动集成的钩子脚本：

```bash
# Install hook to your Claude hooks directory
cp hooks/precompact_reflect.py ~/.claude/hooks/
```

详细配置信息请参见 `~/.claude/settings.json`：

```json
{
  "hooks": {
    "PreCompact": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run ~/.claude/hooks/precompact_reflect.py --auto"
          }
        ]
      }
    ]
  }
}
```

完整配置选项请参阅 [hooks/README.md](hooks/README.md)。

## 可移植性

该技能适用于任何支持以下功能的LLM工具：
- 文件读写操作
- 文本模式匹配
- Git操作（可选，用于提交更改）

### 可配置的状态存储位置

```bash
# Set custom state directory
export REFLECT_STATE_DIR=/path/to/state

# Or use default
# ~/.reflect/ (portable default)
# ~/.claude/session/ (Claude Code default)
```

### 无需依赖任务管理工具

与之前的基于代理的方法不同，该技能直接由LLM执行，无需启动子代理。LLM会读取 SKILL.md 文件并按照工作流程进行处理。

### Git操作的可选性

即使不在Git仓库中，系统也会保存更改，但不会自动提交。

## 故障排除

**未检测到学习信号：**
- 可能是因为会话中没有任何需要纠正的行为
- 可尝试使用 `/reflect review` 命令查看待审核的内容

**冲突警告：**
- 查看被引用的现有规则
- 决定新规则是否应该覆盖现有规则
- 可以在应用新规则前进行修改

**找不到代理文件：**
- 检查代理名称的拼写是否正确
- 使用 `/reflect status` 命令查看可用的目标文件
- 可能需要先创建代理文件

## 文件结构

```
reflect/
├── SKILL.md                      # This file
├── scripts/
│   ├── state_manager.py          # State file CRUD
│   ├── signal_detector.py        # Pattern matching
│   ├── metrics_updater.py        # Metrics aggregation
│   └── output_generator.py       # Reflection file & index generation
├── hooks/
│   ├── precompact_reflect.py     # PreCompact hook integration
│   ├── settings-snippet.json     # Settings.json examples
│   └── README.md                 # Hook configuration guide
├── references/
│   ├── signal_patterns.md        # Detection rules
│   ├── agent_mappings.md         # Target mappings
│   └── skill_template.md         # Skill generation
└── assets/
    ├── reflection_template.md    # Output template
    └── learnings_schema.yaml     # Schema definition
```