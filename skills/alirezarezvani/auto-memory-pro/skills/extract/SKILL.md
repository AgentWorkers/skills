---
name: extract
description: "将一个经过验证的模式或调试解决方案转化为一个独立的、可重用的技能，通过 SKILL.md 文件、参考文档和示例来实现。"
command: /si:extract
---
# /si:extract — 从模式中创建技能

该工具可将重复出现的调试模式或解决方案转化为独立的、可移植的技能，以便在任何项目中使用。

## 使用方法

```
/si:extract <pattern description>                  # Interactive extraction
/si:extract <pattern> --name docker-m1-fixes       # Specify skill name
/si:extract <pattern> --output ./skills/            # Custom output directory
/si:extract <pattern> --dry-run                     # Preview without creating files
```

## 何时提取技能

当满足以下任意一条条件时，就可以将该学习内容提取为技能：

| 条件 | 信号 |
|---|---|
| **重复出现** | 在两个或多个项目中出现相同的问题 |
| **不易发现** | 需要通过实际调试才能找到解决方案 |
| **广泛适用** | 不局限于特定的代码库 |
| **解决方案复杂** | 需要多个步骤才能解决，且容易忘记 |
| **用户提出请求** | 用户表示“将此内容保存为技能”或“我想重复使用它” |

## 工作流程

### 第一步：识别模式

阅读用户的描述，并在自动记忆系统中搜索相关记录：

```bash
MEMORY_DIR="$HOME/.claude/projects/$(pwd | sed 's|/|%2F|g; s|%2F|/|; s|^/||')/memory"
grep -rni "<keywords>" "$MEMORY_DIR/"
```

如果在自动记忆系统中找到相关记录，使用这些记录作为素材；如果没有找到，则直接使用用户的描述。

### 第二步：确定技能的范围

提出以下问题（最多两个）：
- “这个技能能解决什么问题？”（如果问题不明确）
- “是否需要包含代码示例？”（如果适用）

### 第三步：生成技能名称

命名规则：
- 使用小写字母，并用连字符连接单词
- 名称应具有描述性且简洁（2-4个词）
- 例如：`docker-m1-fixes`、`api-timeout-patterns`、`pnpm-workspace-setup`

### 第四步：创建技能文件

启动 `skill-extractor` 代理来生成实际的技能文件。

该代理会创建以下文件：

```
<skill-name>/
├── SKILL.md            # Main skill file with frontmatter
├── README.md           # Human-readable overview
└── reference/          # (optional) Supporting documentation
    └── examples.md     # Concrete examples and edge cases
```

### 第五步：SKILL.md 的结构

生成的 SKILL.md 文件必须遵循以下格式：

```markdown
---
name: <skill-name>
description: "<one-line description>. Use when: <trigger conditions>."
---

# <Skill Title>

> One-line summary of what this skill solves.

## Quick Reference

| Problem | Solution |
|---------|----------|
| {{problem 1}} | {{solution 1}} |
| {{problem 2}} | {{solution 2}} |

## The Problem

{{2-3 sentences explaining what goes wrong and why it's non-obvious.}}

## Solutions

### Option 1: {{Name}} (Recommended)

{{Step-by-step with code examples.}}

### Option 2: {{Alternative}}

{{For when Option 1 doesn't apply.}}

## Trade-offs

| Approach | Pros | Cons |
|----------|------|------|
| Option 1 | {{pros}} | {{cons}} |
| Option 2 | {{pros}} | {{cons}} |

## Edge Cases

- {{edge case 1 and how to handle it}}
- {{edge case 2 and how to handle it}}
```

### 第六步：质量检查

在最终确定之前，请验证以下内容：
- SKILL.md 文件是否包含有效的 YAML 标头，其中包含 `name` 和 `description` 字段
- `name` 是否与文件夹名称匹配（使用小写字母和连字符）
- 描述中是否包含“使用场景”等触发条件
- 解决方案是否独立完整（无需依赖外部环境）
- 代码示例是否完整且可以直接复制粘贴
- 文件中是否没有特定于某个项目的硬编码值（如路径、URL、凭据）
- 是否没有不必要的依赖项

### 第七步：提交报告

```
✅ Skill extracted: {{skill-name}}

Files created:
  {{path}}/SKILL.md          ({{lines}} lines)
  {{path}}/README.md         ({{lines}} lines)
  {{path}}/reference/examples.md  ({{lines}} lines)

Install: /plugin install (copy to your skills directory)
Publish: clawhub publish {{path}}

Source: MEMORY.md entries at lines {{n, m, ...}} (retained — the skill is portable, the memory is project-specific)
```

## 示例

### 提取一个调试模式

```
/si:extract "Fix for Docker builds failing on Apple Silicon with platform mismatch"
```

生成的 `docker-m1-fixes/SKILL.md` 文件包含：
- 平台不匹配的错误信息
- 三种解决方案（构建命令、Dockerfile、docker-compose）
- 相关的权衡分析
- 关于 Rosetta 2 模拟的性能说明

### 提取一个工作流程模式

```
/si:extract "Always regenerate TypeScript API client after modifying OpenAPI spec"
```

生成的 `api-client-regen/SKILL.md` 文件包含：
- 说明为何需要手动重新生成资源
- 具体的命令序列
- 集成到持续集成（CI）系统的代码片段
- 常见的问题及解决方法

## 提示：
- 选择能够在其他项目中节省时间的模式进行提取
- 每个技能只解决一个具体问题
- 包含用户可能会搜索的错误信息
- 在没有原始上下文的情况下测试该技能——其内容是否清晰易懂？