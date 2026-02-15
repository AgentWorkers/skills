---
name: plugin-development
description: Claude Code 插件开发：插件结构、斜杠命令（slash commands）、技能（skills）、子代理（sub-agents）以及 YAML 标头文件（YAML frontmatter）。这些内容用于指导插件开发过程。
---

# 插件开发专家

为您提供创建可用于生产环境的 Claude Code 插件的专业指导。

## 关键结构规则

**目录层次结构**：
```
~/.claude/plugins/my-plugin/    ← Plugin root
├── .claude-plugin/
│   └── plugin.json            ← Manifest (REQUIRED)
├── commands/
│   └── command-name.md        ← Slash commands
├── skills/
│   └── skill-name/            ← MUST be subdirectory
│       └── SKILL.md           ← MUST be uppercase
└── agents/
    └── agent-name/
        └── AGENT.md
```

**常见错误**：
```
# ❌ WRONG
skills/SKILL.md                # Missing subdirectory
skills/my-skill.md             # Wrong filename
skills/My-Skill/SKILL.md       # CamelCase not allowed

# ✅ CORRECT
skills/my-skill/SKILL.md       # kebab-case subdirectory + SKILL.md
```

## plugin.json 格式

**最低要求**：
```json
{
  "name": "my-plugin",
  "description": "Clear description with activation keywords",
  "version": "1.0.0"
}
```

**完整示例**：
```json
{
  "name": "my-awesome-plugin",
  "description": "Expert cost optimization for AWS, Azure, GCP. Activates for reduce costs, cloud costs, finops, save money, cost analysis.",
  "version": "1.0.0",
  "author": {
    "name": "Your Name",
    "email": "you@example.com"
  },
  "homepage": "https://github.com/user/my-plugin",
  "repository": "https://github.com/user/my-plugin",
  "license": "MIT",
  "keywords": ["cost", "finops", "aws", "azure", "gcp"]
}
```

## 命令格式（斜杠命令）

**头部格式**（非常重要）：
```markdown
# /my-plugin:command-name
```

**规则**：
- 必须以 `# /` 开头
- 插件名称：使用“kebab-case”命名规则（即所有单词均小写且用连字符连接）
- 不允许使用 YAML 作为前置内容（仅技能相关文档可以使用 YAML）

**完整模板**：
```markdown
# /my-plugin:analyze-costs

Analyze cloud costs and provide optimization recommendations.

You are an expert FinOps engineer.

## Your Task

1. Collect cost data
2. Analyze usage patterns
3. Identify optimization opportunities
4. Generate report

### 1. Data Collection

\```bash
aws ce get-cost-and-usage --time-period...
\```

## Example Usage

**User**: "Analyze our AWS costs"

**Response**:
- Pulls Cost Explorer data
- Identifies $5K/month in savings
- Provides implementation plan

## When to Use

- Monthly cost reviews
- Budget overruns
- Pre-purchase planning
```

## 技能格式（自动激活）

**YAML 前置内容**（必需）：
```yaml
---
name: cost-optimization
description: Expert cloud cost optimization for AWS, Azure, GCP. Covers FinOps, reserved instances, spot instances, right-sizing, storage optimization. Activates for reduce costs, save money, cloud costs, aws costs, finops, cost optimization, budget overrun, expensive bill.
---
```

**激活关键词**：
```yaml
# ✅ GOOD: Specific, varied keywords
description: Expert Python optimization. Activates for python performance, optimize python code, speed up python, profiling, cProfile, pypy, numba.

# ❌ BAD: Too generic
description: Python expert.

# ❌ BAD: No activation keywords
description: Expert Python optimization covering performance tuning.
```

**完整模板**：
```markdown
---
name: my-skill
description: Expert [domain] covering [topics]. Activates for keyword1, keyword2, phrase3, action4.
---

# Skill Title

You are an expert [role] with deep knowledge of [domain].

## Core Expertise

### 1. Topic Area

Content here...

### 2. Code Examples

\```typescript
// 工作示例
\```

## Best Practices

- Practice 1
- Practice 2

You are ready to help with [domain]!
```

## 代理格式（子代理）

**文件位置**：
```
agents/agent-name/AGENT.md
```

**模板**：
```markdown
---
name: specialist-agent
description: Specialized agent for [specific task]
---

# Agent Title

You are a specialized agent for [purpose].

## Capabilities

1. Capability 1
2. Capability 2

## Workflow

1. Analyze input
2. Execute specialized task
3. Return results
```

**调用方式**：
```typescript
Task({
  subagent_type: "plugin-name:folder-name:yaml-name",
  prompt: "Task description"
});

// Example
Task({
  subagent_type: "my-plugin:specialist-agent:specialist-agent",
  prompt: "Analyze this code for security vulnerabilities"
});
```

## 测试工作流程

**1. 安装插件**：
```bash
cp -r my-plugin ~/.claude/plugins/
# OR
claude plugin add github:username/my-plugin
```

**2. 重启 Claude Code**：
```bash
# Required after:
- Adding new plugin
- Modifying plugin.json
- Adding/removing commands
- Changing YAML frontmatter
```

**3. 测试命令**：
```bash
# Type "/" in Claude Code
# Verify command appears: /my-plugin:command-name
# Execute command
# Verify behavior
```

**4. 测试技能**：
```bash
# Ask trigger question: "How do I reduce costs?"
# Verify skill activates
# Check response uses skill knowledge
```

**5. 检查日志**：
```bash
tail -f ~/.claude/logs/claude.log | grep my-plugin

# Expected:
# ✅ "Loaded plugin: my-plugin"
# ✅ "Registered command: /my-plugin:analyze"
# ✅ "Registered skill: cost-optimization"

# Errors:
# ❌ "Failed to parse plugin.json"
# ❌ "YAML parsing error in SKILL.md"
# ❌ "Command header malformed"
```

## 常见问题

**问题：技能无法激活**：
```
Checklist:
1. ✅ YAML frontmatter present? (---...---)
2. ✅ Activation keywords in description?
3. ✅ SKILL.md in subdirectory? (skills/name/SKILL.md)
4. ✅ File named SKILL.md (uppercase)?
5. ✅ Claude Code restarted?
```

**问题：命令未找到**：
```
Checklist:
1. ✅ Header format: # /plugin-name:command-name
2. ✅ File in commands/ directory?
3. ✅ Plugin name matches plugin.json?
4. ✅ Claude Code restarted?
```

**问题：YAML 解析错误**：
```
Common causes:
- Unclosed quotes: description: "Missing end
- Invalid characters: name: my_skill (use hyphens)
- Missing closing ---
- Incorrect indentation
```

## 最佳实践

**命名规范**：
- 插件名称：`my-awesome-plugin`（使用“kebab-case”命名规则）
- 命令名称：`analyze-costs`（使用“kebab-case”命名规则）
- 技能名称：`cost-optimization`（使用“kebab-case”命名规则）
- 避免使用下划线或驼峰式命名法

**激活关键词**：
- 包含 5-10 个触发关键词
- 结合具体术语和常用短语
- 考虑用户可能提出的问题
- 用实际问题进行测试

**文档编写**：
- 明确的“您的任务”部分
- 带有语法高亮的代码示例
- “示例用法”部分
- “使用场景”部分

**性能优化**：
- 保持 SKILL.md 文件大小在 50KB 以内
- 优化命令提示语
- 避免执行耗时的操作

快来创建可用于生产环境的 Claude Code 插件吧！