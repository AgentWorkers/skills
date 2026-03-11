# 技能构建器 —— 用于创建新技能的元技能

## 元数据

```yaml
---
name: skill-builder
version: 1.0.0
description: |
  Helps create high-quality OpenClaw skills following Anthropic's best practices.
  Use when creating, updating, or auditing any skill in the workspace.
---

---

## When to Use This Skill

Trigger phrases:
- "create a new skill"
- "build a skill"
- "make a new capability"
- "add a skill for"
- "audit our skills"
- "improve this skill"
- "review our skill setup"

---

## The Skill Creation Workflow

### Phase 1: Use Case Definition (Before Writing Code)

Before creating any skill, define 2-3 concrete use cases:

For each use case, specify:
1. **Trigger** — What the user says that should activate this skill
2. **Sequence** — Step-by-step actions the skill performs
3. **Expected Result** — What the user gets at the end

**Example Use Case Template:**
```
用例 #1：[标题]
- 触发条件：用户会说“[特定短语]”
- 执行顺序：[步骤 1] → [步骤 2] → [步骤 3]
- 结果：[产生的结果]
```

### Phase 2: Skill Structure

Every skill must have:

```
skill-name/
├── SKILL.md           # 必需文件：主要使用说明
├── references/        # 可选文件：附加文档
├── scripts/           # 可选文件：可执行代码
├── assets/            # 可选文件：模板、配置文件
└── tests/            # 可选文件：测试用例
```

### Phase 3: SKILL.md Anatomy

```yaml
---
name: skill-name
description: |
  [该技能的功能]。当用户提到“[触发短语]”时使用。
  例如触发条件：“执行 X 操作”、“帮助处理 Y 问题”、“使用 [技能名称]”
---
```

**Critical: The description field is the most important part.**
- Must include WHAT the skill does
- Must include WHEN to use it
- Must include specific trigger phrases
- Bad: "Helps with projects" (never triggers)
- Good: "Manages project workflows including creation, tracking, and updates. Use when user mentions 'project', 'create task', or 'track progress'"

### Phase 4: Writing the Instructions

Structure SKILL.md as:

1. **Identity** — Name, role, primary function
2. **Responsibilities** — What it must handle
3. **Boundaries** — What it must NOT do
4. **Tool Access** — What tools/functions it can use
5. **Workflow** — How it handles tasks
6. **Examples** — 2-3 concrete usage examples

### Phase 5: Testing

Test each skill on three dimensions:

| Test Type | Purpose |
|-----------|---------|
| Triggering | Skill loads for relevant queries, NOT for unrelated ones |
| Functional | Skill produces correct outputs |
| Performance | Measures improvement over baseline |

---

## Quality Checklist

Before finalizing any skill, verify:

- [ ] Description includes "Use when..." clause
- [ ] At least 3 trigger phrases listed
- [ ] Clear responsibilities section
- [ ] Boundaries defined (what NOT to do)
- [ ] Tool permissions explicitly stated
- [ ] Workflow documented with examples
- [ ] Triggering test passed
- [ ] Functional test passed
- [ ] No overgeneralization (skill won't trigger on unrelated queries)

---

## Common Failure Modes

| Failure | Cause | Fix |
|---------|-------|-----|
| Skill never triggers | Vague description | Add specific trigger phrases |
| Skill triggers too often | Overly broad description | Narrow the use case definition |
| Skill produces bad output | Missing boundaries | Add explicit "never do X" rules |
| Skill conflicts with others | No scope definition | Add explicit scope/limits |

---

## OpenClaw-Specific Notes

When building OpenClaw skills:
- Use the existing skill format (`SKILL.md` in skill folder)
- Reference OpenClaw tools by their exact names
- Follow the workspace memory paths exactly
- Respect the agent delegation rules in AGENTS.md
- Include security considerations for sensitive operations

---

## Example: Well-Formed Skill Description

```yaml
---
name: github-pr-review
description: |
  用于审查 GitHub 提交请求的代码质量、安全性和格式一致性。
  当用户提到“审查 Pull Request”、“检查 Pull Request”、“查看 Pull Request #N”、“需要进行代码审查”时使用。
  该技能不负责批准合并请求、编写代码或修改现有的 Pull Request。
---
---

## 审查现有技能

在审查技能时，请检查以下内容：
1. 描述中是否包含明确的触发条件。
2. 技能的适用范围是否清晰明确。
3. 各技能之间是否存在冲突。
4. 所使用的工具是否在其指定的范围内使用。
5. 使用说明是否具有可操作性。

如果某个技能未通过审查，请按照以下流程更新其 SKILL.md 文件。