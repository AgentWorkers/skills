---
name: command-creator
model: fast
description: |
  WHAT: Create Claude Code slash commands - reusable markdown workflows invoked with /command-name.
  
  WHEN: User wants to create, make, or add a slash command. User wants to automate a repetitive workflow or document a consistent process for reuse.
  
  KEYWORDS: "create a command", "make a slash command", "add a command", "new command", "/command", "automate this workflow", "make this repeatable"
---

# 命令创建器

斜杠命令（slash commands）是位于 `.claude/commands/`（项目级）或 `~/.claude/commands/`（全局级）的 Markdown 文件，当被调用时会生成相应的提示信息。

## 命令结构

```markdown
---
description: Brief description for /help (required)
argument-hint: <required> or [optional] (if takes arguments)
---

# Command Title

[Instructions for agent to execute autonomously]
```

---

## 创建流程

### 第一步：确定命令位置

1. 检查是否在 Git 仓库中：`git rev-parse --is-inside-work-tree`
2. 默认位置：Git 仓库 → `.claude/commands/`；非 Git 仓库 → `~/.claude/commands/`
3. 如果用户明确指定为“全局”或“项目级”，则覆盖此规则。

在继续之前，需报告所选择的命令位置。

### 第二步：确定命令模式

加载 [references/patterns.md](references/patterns.md)，并展示可用的命令模式：

| 模式 | 结构 | 适用场景 |
|---------|-----------|----------|
| 工作流程自动化 | 分析 → 执行 → 报告 | 需要按特定顺序执行的多个步骤 |
| 迭代修复 | 运行 → 解析 → 修复 → 重复 | 用于持续修复问题的流程 |
| 代理任务分配 | 确定上下文 → 分配任务 → 迭代执行 | 复杂任务，需要用户审核 |
| 简单执行 | 解析 → 执行 → 返回结果 | 用于封装现有工具的功能 |

询问用户：“哪种模式最符合您的需求？”

### 第三步：收集信息

**A. 命令名称和用途**
- “这个命令应该叫什么名字？”（使用驼峰式命名法，例如：`my-command`）
- “它的功能是什么？”（用于填写命令描述）

**B. 参数**
- “这个命令是否需要参数？是必需的还是可选的？”
- 必需参数：`<placeholder>`  
- 可选参数：`[placeholder]`

**C. 执行步骤**
- “命令具体需要执行哪些步骤？”
- “命令需要使用哪些工具或命令？”

**D. 限制条件**
- “是否有特定的工具需要使用或避免使用？”
- “是否需要读取某些文件以获取上下文信息？”

### 第四步：生成命令文档

加载 [references/best-practices.md](references/best-practices.md)，以获取以下内容：
- 命令文档的模板结构
- 编写规范（使用祈使句形式）
- 质量检查清单

关键原则：
- 使用祈使句形式，例如：“运行 `make lint`”，而不是“你应该运行 `make lint`”
- 表达要执行的操作要明确，例如：“运行 `make lint` 来检查错误”
- 描述预期的执行结果
- 定义错误处理机制
- 明确成功的标准

### 第五步：创建命令文件

```bash
mkdir -p [directory-path]
```

编写命令文件，并记录以下内容：
- 文件的位置
- 命令的功能
- 使用方法：`/命令名称 [参数]`

### 第六步：测试（可选）

建议用户使用 `/命令名称 [参数]` 来测试命令。

根据用户的反馈进行迭代修改。

---

## 编写指南

**使用祈使句形式（动词在前）**：
- ✅ “运行 `git status`”
- ❌ “你应该运行 `git status`”

**描述要执行的操作要具体**：
- ✅ “运行 `make lint` 来检查错误”
- ❌ “检查错误”

**明确说明执行结果**：
- ✅ “运行 `git status` 后，应显示修改过的文件”
- ❌ “运行 `git status`”

**示例**：
- ✅ `git commit -m "添加 OAuth2 认证"`  
- ❌ `git commit -m "foo bar"`

---

## 命令模式快速参考

### 工作流程自动化
```markdown
1. Check for .PLAN.md
2. Analyze git status/diff
3. Perform actions
4. Report results
```

### 迭代修复
```markdown
1. Run make all-ci (max 10 iterations)
2. Parse errors by category
3. Apply targeted fixes
4. Repeat until success or stuck
```

### 代理任务分配
```markdown
1. Present context
2. Invoke subagent with Task tool
3. Iterate with user feedback
4. Save output after approval
```

更多命令示例请参见 [references/examples.md](references/examples.md)。

---

## 质量检查清单

在最终完成命令文档之前，请确保满足以下要求：
- [ ] 命令名称使用驼峰式命名法（例如：`my-command`，而不是 `my_command`）
- [ ] 命令描述具有明确的行为指向
- 执行步骤编号且具体明确
- 明确指定了使用的工具
- 定义了错误处理机制
- 明确了成功的标准
- 使用祈使句形式编写命令

---

**绝对禁止**：
- 在命令名称中使用下划线（请使用连字符）
- 编写模糊的指令（例如：“修复错误”）
- 忽略错误处理
- 使用第二人称（例如：“你应该...”）
- 在未进行测试的情况下创建命令
- 不定义成功标准