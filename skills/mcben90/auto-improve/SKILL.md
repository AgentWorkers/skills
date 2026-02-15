---
name: Auto-Improve Skill
description: 通过错误学习和模式识别实现自动自我改进
---

# 自动提升技能

**核心原则：** 每一个行动都会让我为下一次行动做好准备。

## 何时激活

- 会话开始时（自动）
- 每个任务完成后
- 发生错误时

## 提升循环

```
┌─────────────────────────────────────────────────┐
│              AUTO-IMPROVE LOOP                  │
├─────────────────────────────────────────────────┤
│                                                  │
│  SESSION START                                  │
│       │                                         │
│       ▼                                         │
│  ┌─────────────────┐                           │
│  │ 1. Load Context │                           │
│  │    .antigravity │                           │
│  │    + MEMORY     │                           │
│  └────────┬────────┘                           │
│           ▼                                     │
│  ┌─────────────────┐                           │
│  │ 2. Check        │                           │
│  │    Past Mistakes│ ← "Was hab ich falsch     │
│  └────────┬────────┘    gemacht?"              │
│           ▼                                     │
│  ┌─────────────────┐                           │
│  │ 3. EXECUTE TASK │                           │
│  └────────┬────────┘                           │
│           ▼                                     │
│  ┌─────────────────┐                           │
│  │ 4. Verify       │ ← Tests + Lint            │
│  └────────┬────────┘                           │
│           ▼                                     │
│     ┌─────────────┐                            │
│     │ Erfolgreich?│                            │
│     └──────┬──────┘                            │
│      JA    │    NEIN                           │
│      ↓     │     ↓                             │
│  ┌───────┐ │ ┌──────────┐                      │
│  │Pattern│ │ │ Learn    │                      │
│  │Save   │ │ │ Mistake  │                      │
│  └───┬───┘ │ └────┬─────┘                      │
│      └─────┼──────┘                            │
│            ▼                                    │
│  ┌─────────────────┐                           │
│  │ 5. Update       │                           │
│  │    .antigravity │                           │
│  └─────────────────┘                           │
│                                                  │
│  → NÄCHSTER TASK IST BESSER                    │
│                                                  │
└─────────────────────────────────────────────────┘
```

## 第一阶段：会话开始

```python
# Automatisch bei Session-Start ausführen

# 1. Projekt-Kontext laden
project_root = detect_project_root()
antigravity_file = f"{project_root}/.antigravity.md"

if exists(antigravity_file):
    load_context(antigravity_file)
    
# 2. Globales Memory laden
recall_memory(tags=["mistakes", project_name])

# 3. Warnung bei bekannten Fehlern
if relevant_mistakes:
    warn(f"⚠️ Bekannte Fehler für {project}: {mistakes}")
```

## 第二阶段：操作前检查

在修改任何代码之前：

```markdown
## Pre-Action Checklist
- [ ] Habe ich das schon mal falsch gemacht?
- [ ] Gibt es ein gespeichertes Pattern dafür?
- [ ] Verstehe ich das Projekt-Architektur?
- [ ] Kenne ich die Coding-Standards?
```

## 第三阶段：操作后学习

每个行动之后：

### 成功时
```python
save_pattern(
    situation=task.context,
    action=task.approach,
    outcome="success",
    pattern=extract_reusable_pattern(task)
)
```

### 出现错误时
```python
learn_from_mistake(
    mistake=error.description,
    cause=error.root_cause,
    lesson=error.how_to_avoid,
    tags=["mistakes", project, domain]
)

# Auto-Update .antigravity.md
update_antigravity_mistakes(project, error)
```

## 与现有技能的整合

| 技能 | 整合方式 |
|-------|-------------|
| `mistake-tracker` | 提供错误数据 |
| `verification-loops` | 触发操作后学习 |
| `context-management` | 加载会话上下文 |
| `self-check` | 操作前验证 |

## 触发器

### 自动触发器
```yaml
session_start:
  - load_project_context
  - recall_mistakes
  - warn_known_issues

post_code_edit:
  - run_verification_loop
  - if_error: learn_from_mistake
  - if_success: save_pattern

session_end:
  - summarize_learnings
  - update_antigravity
```

### 手动触发器
- `/improve` - 强制执行上次行动后的学习内容
- `/mistakes` - 显示所有已学习的错误信息
- `/patterns` - 显示成功的操作模式

## 监控指标

随时间跟踪以下指标：

| 指标 | 描述 |
|--------|--------------|
| `mistakes_repeated` | 应该降至0 |
| `first_time_right` | 应该达到100% |
| `patterns_reused` | 应该增加 |
| `verification_failures` | 应该减少 |

## 需避免的错误做法

| ❌ 不要这样做 | ✅ 应该这样做 |
|----------|-------|
| 忽视错误 | 保存所有错误信息 |
| 仅学习当前会话的内容 | 进行跨会话学习 |
| 提供泛化的学习内容 | 提供具体且可操作的指导 |
| 保存过多信息 | 仅保存相关信息 |