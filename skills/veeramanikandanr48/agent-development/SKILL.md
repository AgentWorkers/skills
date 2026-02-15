---
name: agent-development
description: |
  Design and build custom Claude Code agents with effective descriptions, tool access patterns,
  and self-documenting prompts. Covers Task tool delegation, model selection, memory limits,
  and declarative instruction design.

  Use when: creating custom agents, designing agent descriptions for auto-delegation,
  troubleshooting agent memory issues, or building agent pipelines.
license: MIT
---

# Claude Code的代理开发

使用适当的任务分配、工具访问权限和提示设计，为Claude Code构建高效的定制代理。

## 代理描述模式

描述字段决定了Claude是否自动分配任务。

### 强触发模式

```yaml
---
name: agent-name
description: |
  [Role] specialist. MUST BE USED when [specific triggers].
  Use PROACTIVELY for [task category].
  Keywords: [trigger words]
tools: Read, Write, Edit, Glob, Grep, Bash
model: sonnet
---
```

### 弱描述与强描述的对比

| 弱描述（不会自动分配任务） | 强描述（会自动分配任务） |
|---------------------------|-------------------------|
| “分析截图以查找问题”       | “视觉质量检查专家。分析截图时必须使用此代理。应主动使用它进行视觉质量检查。” |
| “运行Playwright脚本”      | “Playwright脚本专家。运行Playwright脚本时必须使用此代理。应主动使用它进行浏览器自动化。” |

**关键短语**：
- “必须使用此代理时...” |
- “应主动使用它进行...” |
- 包含触发关键词

### 任务分配机制

1. **显式分配**：`Task tool subagent_type: "agent-name"` – 总是有效的方法
2. **自动分配**：Claude根据代理描述来匹配任务 – 需要使用明确的描述

创建或修改代理后，**需要重启会话**。

## 工具访问权限原则

**如果代理不需要Bash，就不要给它Bash权限。**

| 代理需要的功能 | 提供的工具 | 不提供的工具 |
|-------------------|------------|------------|
| 仅创建文件       | 读取、写入、编辑、全局搜索、grep | Bash |
| 运行脚本/命令行接口   | 读取、写入、编辑、全局搜索、grep、Bash | — |
| 仅读取/审计       | 读取、全局搜索、grep | 写入、编辑、Bash |

**为什么？** 模型默认使用`cat > file << 'EOF'`这样的命令，而不是写入文件。每个Bash命令都需要人工审批，这会导致每个代理运行时出现大量提示信息。

### 允许列表模式

在`.claude/settings.json`文件中列出允许使用的安全命令，而不是限制Bash命令的使用：

```json
{
  "permissions": {
    "allow": [
      "Write", "Edit", "WebFetch(domain:*)",
      "Bash(cd *)", "Bash(cp *)", "Bash(mkdir *)", "Bash(ls *)",
      "Bash(cat *)", "Bash(head *)", "Bash(tail *)", "Bash(grep *)",
      "Bash(diff *)", "Bash(mv *)", "Bash(touch *)", "Bash(file *)"
    ]
  }
}
```

## 模型选择（质量优先）

不要为了解决问题而降低模型质量——应该从根本上解决问题。

| 模型 | 适用场景 |
|-------|---------|
| **Opus** | 创意工作（页面构建、设计、内容创作）——质量至关重要 |
| **Sonnet** | 大多数代理——内容处理、代码编写、研究（默认模型） |
| **Haiku** | 仅适用于脚本执行任务，对质量要求不高 |

## 内存限制

### 根本问题解决方法（必须执行）

将以下代码添加到`~/.bashrc`或`~/.zshrc`中：
```bash
export NODE_OPTIONS="--max-old-space-size=16384"
```

将Node.js的内存堆从4GB增加到16GB。

### 并发限制（即使进行了优化）

| 代理类型 | 最大并发数量 | 备注 |
|------------|--------------|-------|
| 所有代理 | 2-3 | 任务执行过程中会积累上下文数据，需要分批处理并适当暂停 |
| 高度创意型代理（如Opus） | 1-2 | 这类代理需要更多内存 |

### 故障恢复方法

1. 执行`source ~/.bashrc`或重启终端
2. 使用`NODE_OPTIONS="--max-old-space-size=16384" claude`命令
3. 检查现有文件，然后继续执行任务

## 子代理与远程API

**始终优先选择使用子代理而不是远程API调用。**

| 方面 | 远程API调用 | 子代理 |
|--------|-----------------|----------------|
| 工具访问权限 | 无 | 全部权限（读取、grep、写入、Bash） |
| 文件读取 | 必须在提示中提供所有文件内容 | 可以迭代读取文件 |
| 文件间的关联处理 | 只能处理单一上下文数据 | 可以跨多个文件进行推理 |
| 决策质量 | 提供一般性建议 | 提供具体决策及理由 |
| 输出质量 | 通常为100行左右 | 可以输出600行以上的内容 |

```typescript
// ❌ WRONG - Remote API call
const response = await fetch('https://api.anthropic.com/v1/messages', {...})

// ✅ CORRECT - Use Task tool
// Invoke Task with subagent_type: "general-purpose"
```

## 声明式编程 vs 命令式编程

应该描述**要完成的任务**，而不是**如何使用工具**。

### 错误的命令式编程示例

```markdown
### Check for placeholders
```bash
grep -r "PLACEHOLDER:" build/*.html
```
```

### 正确的声明式编程示例

```markdown
### Check for placeholders
Search all HTML files in build/ for:
- PLACEHOLDER: comments
- TODO or TBD markers
- Template brackets like [Client Name]

Any match = incomplete content.
```

## 需要包含的内容

| 应包含的内容 | 不应包含的内容 |
|---------|------|
| 任务目标和上下文信息 | 明确的Bash命令或工具指令 |
| 输入文件路径 | “使用X工具来...” |
| 输出文件路径和格式 | 详细的工具使用步骤 |
| 成功/失败标准 | 使用Shell管道语法来定义 |
| 阻碍因素检查 | 过度细化的流程控制 |
| 质量检查清单 | |

## 自我文档化原则

> “没有上下文信息的代理必须能够独立复现所需的行为。”

所有的改进都应通过代理的提示来明确展示，而不能作为隐含的知识。

### 需要记录的内容

| 需要记录的信息 | 记录的位置 |
|-----------|------------------|
| 错误修复方法 | 代理的“错误修复”或“常见问题”部分 |
| 质量要求 | 代理的“质量检查清单”部分 |
| 文件路径规范 | 代理的“输出结果”部分 |
| 工具使用方法 | 代理的“执行流程”部分 |
| 阻碍因素 | 代理的“障碍检查”部分 |

### 测试新代理是否有效：

在改进代理之前：
1. 像没有上下文信息一样阅读代理的提示内容
2. 询问：新会话是否能够按照这些提示完成相同的工作，并且达到相同的质量标准？
3. 如果不能：添加缺失的指令、模式或参考信息

## 应避免的错误做法

| 错误做法 | 原因 |
|--------------|--------------|
| “正如我们之前讨论的...” | 由于没有预先提供的上下文信息，新代理可能无法正确执行任务 |
| 依赖开发过程中读取的文件 | 新代理可能无法读取相同的文件 |
| 基于错误信息进行假设 | 新代理可能无法理解你的调试步骤 |
| “就像主页一样简单” | 新代理可能还没有生成相应的主页内容 |

## 代理提示的设计

有效的代理提示应该包含以下内容：

```markdown
## Your Role
[What the agent does]

## Blocking Check
[Prerequisites that must exist]

## Input
[What files to read]

## Process
[Step-by-step with encoded learnings]

## Output
[Exact file paths and formats]

## Quality Checklist
[Verification steps including learned gotchas]

## Common Issues
[Patterns discovered during development]
```

## 管道代理

在将新代理添加到编号顺序的管道中（例如`HTML-01` → `HTML-05` → `HTML-11`）时：

| 需要更新的内容 | 更新内容 |
|-------------|------|
| 新代理 | “工作流程位置”图示 + “下一个任务”字段 |
| **前一个代理** | 前一个代理的“下一个任务”字段，用于指向新代理 |

**常见错误**：新代理可能因为前一个代理的配置仍然指向旧代理而“孤立”。

**验证方法**：
```bash
grep -n "Next:.*→\|Then.*runs next" .claude/agents/*.md
```

## 最佳使用场景

**最适合使用代理的场景**：那些**重复性高但需要判断力的任务**。

例如：手动审核70个技能项非常繁琐，但每个审核步骤都需要智能判断（如检查文档、比较版本、决定需要修复的内容）。这种场景非常适合使用并行处理的代理，并且需要明确的操作指导。

**不适合使用代理的场景**：
- 简单的任务（可以直接手动完成）
- 需要高度创造性的任务（需要人工指导）
- 需要跨文件协调的任务（代理无法独立完成任务）

## 有效的提示模板

```
For each [item]:
1. Read [source file]
2. Verify with [external check - npm view, API call, etc.]
3. Check [authoritative source]
4. Score/evaluate
5. FIX issues found ← Critical instruction
```

**提示的关键要素**：
- “修复发现的问题”——有了这个提示，代理不仅可以报告问题，还能采取行动。
- **准确的文件路径**——避免歧义
- **输出格式模板**——确保输出结果的一致性和可解析性
- **每次处理的文件数量**——数量适中，既能保证效率，又不会导致任务失败

## 工作流程模式

```
1. ME: Launch 2-3 parallel agents with identical prompt, different item lists
2. AGENTS: Work in parallel (read → verify → check → edit → report)
3. AGENTS: Return structured reports (score, status, fixes applied, files modified)
4. ME: Review changes (git status, spot-check diffs)
5. ME: Commit in batches with meaningful changelog
6. ME: Push and update progress tracking
```

**为什么不建议使用命令行脚本直接执行任务**：这样可以方便人工审核、批量处理任务，并保持提交历史记录的清晰性。

## 判断任务是否适合使用代理的依据

**适合使用代理的场景**：
- 多个任务步骤相同
- 每个任务都需要判断力（而不仅仅是简单的转换）
- 任务之间没有相互依赖关系
- 有明确的成功标准（如得分、通过/失败等）
- 有权威的参考资料可以进行验证

**不适合使用代理的场景**：
- 任务结果相互依赖
- 需要创造性的或主观的决策
- 单个复杂的任务（适合使用常规的代理）
- 在执行过程中需要人工输入

## 代理提示的编写指南

### 代理提示的编写模板

```yaml
---
name: my-agent
description: |
  [Role] specialist. MUST BE USED when [triggers].
  Use PROACTIVELY for [task category].
  Keywords: [trigger words]
tools: Read, Write, Edit, Glob, Grep, Bash
model: sonnet
---
```

### 避免不必要的Bash命令

1. 如果不需要使用Bash命令，就将其从提示中删除
2. 将关键指令放在提示的最前面
3. 在`.claude/settings.json`文件中设置允许使用的工具列表

### 避免内存崩溃

```bash
export NODE_OPTIONS="--max-old-space-size=16384"
source ~/.bashrc && claude
```