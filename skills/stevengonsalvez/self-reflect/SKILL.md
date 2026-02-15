---
name: reflect
description: 通过对话分析实现自我提升：从错误修正和成功案例中提取经验教训，并将这些经验永久性地编码到代理（agent）的定义中。核心理念是“一次改正，终身受用”。
version: "2.0.0"
user-invocable: true
triggers:
  - reflect
  - self-reflect
  - review session
  - what did I learn
  - extract learnings
  - analyze corrections
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - Bash
metadata:
  clawdbot:
    emoji: "🪞"
    config:
      stateDirs: ["~/.reflect"]
---

# Reflect – 代理自我提升技能

将您的人工智能助手转变为一个持续改进的合作伙伴。每一次纠正都将成为一项永久性的改进，这些改进会在未来的所有会话中持续发挥作用。

## 快速参考

| 命令 | 动作 |
|---------|--------|
| `reflect` | 分析对话以获取学习内容 |
| `reflect on` | 启用自动反思功能 |
| `reflect off` | 关闭自动反思功能 |
| `reflect status` | 显示状态和指标 |
| `reflect review` | 查看待处理的学习内容 |

## 适用场景

- 完成复杂任务后 |
- 当用户明确指出行为错误时（例如：“永远不要做X”，“总是要做Y”） |
- 在会话结束或内容压缩之前 |
- 当成功的处理方式值得保留时 |

## 工作流程

### 第一步：扫描对话中的信号

分析对话中的纠正信号和学习机会。

**信号置信度等级：**

| 置信度 | 触发条件 | 例子 |
|------------|----------|----------|
| **高** | 明确的纠正语句 | “永远不要”，“总是”，“错误”，“停止”，“规则是” |
| **中** | 被认可的处理方式 | “完美”，“完全正确”，“就是这样” |
| **低** | 观察到的有效行为模式 | 虽有效但未得到明确验证 |

详细检测规则请参见 [signal_patterns.md](signal_patterns.md)。

### 第二步：分类并匹配目标文件

将每个信号映射到相应的目标文件：

| 类别 | 目标文件 |
|----------|--------------|
| 代码风格 | `code-reviewer`, `backend-developer`, `frontend-developer` |
| 架构 | `solution-architect`, `api-architect`, `architecture-reviewer` |
| 流程 | `CLAUDE.md`, `orchestrator-agents` |
| 领域 | 领域特定的代理程序，`CLAUDE.md` |
| 工具 | `CLAUDE.md`, 相关专家 |
| 新技能 | 创建新的技能文件 |

详细映射规则请参见 [agent_mappings.md](agentMappings.md)。

### 第三步：判断是否值得记录为技能

某些学习内容应该被记录为新的技能，而不仅仅是代理程序的更新：

**成为技能的条件：**
- 需要花费大量时间（超过10分钟）进行调试的问题 |
- 错误信息具有误导性（实际原因与显示的信息不同） |
- 通过实验发现了一种解决方法 |
- 提供了配置上的见解（与文档中的信息不同） |
- 可以在类似情况下重复使用的模式 |

**质量标准（必须全部满足）：**
- [ ] 可重复使用：对未来任务有帮助 |
- [ ] 非显而易见：需要通过探索才能发现 |
- [ ] 具体明确：能够描述具体的触发条件 |
- [ ] 经过验证：解决方案确实有效 |
- [ ] 无重复：该技能尚未存在 |

### 第四步：生成提案

以结构化格式呈现发现的内容：

```markdown
# Reflection Analysis

## Session Context
- **Date**: [timestamp]
- **Messages Analyzed**: [count]

## Signals Detected

| # | Signal | Confidence | Source Quote | Category |
|---|--------|------------|--------------|----------|
| 1 | [learning] | HIGH | "[exact words]" | Code Style |

## Proposed Changes

### Change 1: Update [agent-name]
**Target**: `[file path]`
**Section**: [section name]
**Confidence**: HIGH

```差异
+ 从学习中得出的新规则
```

## Review Prompt
Apply these changes? (Y/N/modify/1,2,3)
```

### 第五步：获得用户批准后应用更改

**用户选择“Y”（批准）时：**
1. 使用编辑工具应用每个更改 |
2. 提交更改并附上描述性信息 |
3. 更新相关指标 |

**用户选择“N”（拒绝）时：**
1. 放弃提出的更改 |
2. 记录拒绝原因以供分析 |

**用户选择“modify”（修改）时：**
1. 单独展示每个更改 |
2. 允许用户在应用前进行修改 |

**用户选择部分更改（例如“1,3”）时：**
1. 仅应用指定的更改 |
2. 提交部分更新内容 |

## 状态管理

状态信息存储在 `~/.reflect/` 文件夹中（可通过 `REFLECT_STATE_DIR` 配置）：

```yaml
# reflect-state.yaml
auto_reflect: false
last_reflection: "2026-01-26T10:30:00Z"
pending_reviews: []
```

### 指标跟踪

```yaml
# reflect-metrics.yaml
total_sessions_analyzed: 42
total_signals_detected: 156
total_changes_accepted: 89
acceptance_rate: 78%
confidence_breakdown:
  high: 45
  medium: 32
  low: 12
most_updated_agents:
  code-reviewer: 23
  backend-developer: 18
skills_created: 5
```

## 安全保障措施

### 人工干预机制
- 未经用户明确批准，严禁应用任何更改 |
- 应在应用更改前始终显示完整的差异内容 |
- 允许用户选择性地应用更改 |

### 增量更新
- 仅向现有部分添加新内容 |
- 禁止删除或重写现有规则 |
- 保持原始结构不变 |

### 冲突检测
- 检查新提出的规则是否与现有规则冲突 |
- 如果检测到冲突，提醒用户 |
- 提供解决方案建议 |

## 输出位置

**项目级（与代码库版本同步）：**
- `.claude/reflections/YYYY-MM-DD_HH-MM-SS.md` – 完整的反思记录 |
- `.claude/skills/{name}/SKILL.md` – 新技能文件 |

**全局级（用户级别）：**
- `~/.reflect/learnings.yaml` – 学习日志 |
- `~/.reflect/reflect-metrics.yaml` – 综合指标数据 |

## 示例

### 示例1：代码风格纠正

**用户建议**：“在TypeScript中永远使用`const`或`let`，而不要使用`var`”

**检测到的信号**：
- 置信度：高（明确的纠正语句）
- 类别：代码风格
- 目标文件：`frontend-developer.md`

**建议的更改**：
```diff
## Style Guidelines
+ * Use `const` or `let` instead of `var` in TypeScript
```

### 示例2：流程偏好

**用户建议**：“在提交代码之前务必运行测试”

**检测到的信号**：
- 置信度：高（明确的指令）
- 类别：流程
- 目标文件：`CLAUDE.md`

**建议的更改**：
```diff
## Commit Hygiene
+ * Run test suite before creating commits
```

### 示例3：通过调试发现的新技能

**背景**：花费30分钟时间调试React组件的渲染问题

**检测到的信号**：
- 置信度：高（需要深入调试）
- 类别：新技能
- 符合所有质量标准

**建议的新技能文件**：`react-hydration-fix/SKILL.md`

## 故障排除

**未检测到信号**：
- 可能是因为本次会话中没有出现需要纠正的情况 |
- 请检查是否使用了自然语言形式的纠正指令 |

**冲突警告**：
- 查看被引用的现有规则 |
- 决定新规则是否应该覆盖现有规则 |
- 可以在应用前对规则进行修改 |

**找不到对应的代理程序文件**：
- 检查代理程序的名称拼写是否正确 |
- 可能需要先创建相应的代理程序文件