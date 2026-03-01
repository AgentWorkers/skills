---
name: openclaw-skill-lazy-loader
description: 通过仅在需要时加载技能文件和上下文文件，大幅减少每次会话中的令牌使用量（即减少令牌的消耗）。该方案包括 SKILLS 目录的模式、AGENTS.md 文件的懒加载策略，以及一个 Python 辅助工具，该工具能够为特定任务推荐应加载的文件。该方案兼容所有 OpenClaw 代理，并可与令牌优化器（Token Optimizer）协同使用。
version: 1.0.0
homepage: https://github.com/Asif2BD/openclaw-skill-lazy-loader
source: https://github.com/Asif2BD/openclaw-skill-lazy-loader
author: Asif2BD
license: Apache 2.0
security:
  verified: true
  auditor: Oracle (Matrix Zion)
  audit_date: 2026-02-28
  scripts_no_network: true
  scripts_no_code_execution: true
  scripts_no_subprocess: true
  scripts_data_local_only: true
---
# OpenClaw 技能懒加载机制

在会话开始时，无需加载所有技能文件。只需在需要时加载所需的技能，从而将令牌使用量减少 40% 至 70%。

## 问题所在

大多数 OpenClaw 代理在启动时会加载整个技能库：

```markdown
# AGENTS.md (naive approach)
Read ALL of these before starting:
- skills/python/SKILL.md
- skills/git/SKILL.md
- skills/docker/SKILL.md
- skills/aws/SKILL.md
- skills/browser/SKILL.md
... (20 more)
```

每次会话仅为了加载可能永远不会被使用的上下文信息，就会消耗 **3,000 至 15,000 个令牌**。在大规模应用中，这成为了最大的成本开销。

## 解决方案：懒加载机制

代理不再预先加载所有技能，而是先检查一个 **技能目录**（一个轻量级的索引），仅在任务需要时才加载相应的技能文件。

**改进前：** 加载 20 个技能文件 = 每次会话约消耗 12,000 个令牌  
**改进后：** 首先加载技能目录（300 个令牌），然后根据任务需求加载 1 至 2 个相关技能（约 800 个令牌）= 每次会话约消耗 1,100 个令牌  
这样一来，仅上下文信息的加载成本就减少了 89%。

---

## 实施指南

### 第一步：创建技能目录

在代理工作区创建 `SKILLS.md` 文件，该文件包含所有可用技能的轻量级索引：

```markdown
# Available Skills

| Skill | File | Use When |
|-------|------|----------|
| Python | skills/python/SKILL.md | Writing/debugging Python code |
| Git | skills/git/SKILL.md | Git operations, PRs, branches |
| Docker | skills/docker/SKILL.md | Containers, images, compose |
| Browser | skills/browser/SKILL.md | Web scraping, UI automation |
| AWS | skills/aws/SKILL.md | Cloud deployments, S3, Lambda |
```

这个目录是唯一在会话开始时被加载的文件，因此仅需消耗约 200 至 400 个令牌，而不是 10,000 多个令牌。

请参考 `SKILLS.md.template` 以获取完整的模板。

### 第二步：更新 `AGENTS.md` 文件

将原有的批量加载方式替换为基于技能目录的加载方式：

```markdown
## Skills

At session start: Read SKILLS.md (the index only).
When a task needs a skill: Read the specific SKILL.md for that skill.
Never load all skills upfront.

### Loading Decision
Before loading any skill file:
1. Does the current task need it? (yes → load it, no → skip)
2. Has it already been loaded this session? (yes → skip, no → load once)
```

请参考 `AGENTS.md.template` 以获取完整的 `AGENTS.md` 文件模板。

### 第三步：使用上下文优化器（可选）

随附的 `context_optimizer.py` 可以分析任务描述，并推荐需要加载的技能：

```bash
python3 context_optimizer.py recommend "Write a Python script to push to S3"
# Output:
# Recommended skills to load:
#   - skills/python/SKILL.md  (confidence: high — Python task)
#   - skills/aws/SKILL.md     (confidence: high — S3 mentioned)
#   - skills/git/SKILL.md     (confidence: low  — skip unless pushing to GitHub)
```

### 第四步：同样适用于内存文件

这种懒加载机制也适用于内存文件和上下文文件：

```markdown
## Memory Loading (AGENTS.md)

At session start: Read MEMORY.md (summary only).
Load daily files (memory/YYYY-MM-DD.md) only when:
- User asks about past work
- Task references a specific date or project
- Debugging requires historical context
```

---

## 令牌节省计算示例

| 情况 | 改进前 | 改进后 | 节省的令牌数 |
|--------|--------|---------|
| 加载 5 个技能 | 约 3,000 个令牌 | 约 600 个令牌 | 80% |
| 加载 10 个技能 | 约 6,500 个令牌 | 约 750 个令牌 | 88% |
| 加载 20 个技能 | 约 13,000 个令牌 | 约 900 个令牌 | 93% |
| 加上内存文件（5 个） | 约 4,000 个令牌 | 约 400 个令牌 | 90% |

*基于平均每个 `SKILL.md` 文件大小约为 600 个令牌的计算结果；技能目录平均大小约为 150 个令牌。*

---

## 与令牌优化器的集成

该机制可与 [OpenClaw 令牌优化器](https://clawhub.ai/Asif2BD/openclaw-token-optimizer) 直接配合使用。懒加载机制负责处理上下文信息的加载成本，而令牌优化器则负责模型路由、心跳预算分配以及运行时成本的管理。两者共同覆盖了令牌使用的整个生命周期。

请同时安装这两个工具：
```bash
clawhub install openclaw-skill-lazy-loader
clawhub install openclaw-token-optimizer
```

---

## 本技能包包含的文件

| 文件名 | 用途 |
|------|---------|
| `SKILL.md` | 本使用指南 |
| `SKILLS.md.template` | 技能目录的起始模板 |
| `AGENTS.md.template` | 实现懒加载的 `AGENTS.md` 文件模板 |
| `context_optimizer.py` | 命令行工具——根据任务推荐需要加载的技能 |
| `README.md` | ClawHub 的产品描述文件 |
| `SECURITY.md` | 安全审计和脚本说明文件 |
| `.clawhubsafe` | 文件完整性验证文件 |

---

## 快速入门（5 分钟完成）

```bash
# 1. Install
clawhub install openclaw-skill-lazy-loader

# 2. Copy templates to your agent workspace
cp ~/.openclaw/skills/openclaw-skill-lazy-loader/SKILLS.md.template ~/my-agent/SKILLS.md
cp ~/.openclaw/skills/openclaw-skill-lazy-loader/AGENTS.md.template ~/my-agent/AGENTS.lazy.md

# 3. Edit SKILLS.md — fill in your actual skills
# 4. Merge AGENTS.lazy.md into your AGENTS.md
# 5. Test with context_optimizer.py
python3 ~/.openclaw/skills/openclaw-skill-lazy-loader/context_optimizer.py recommend "your next task"
```

---

*作者：M Asif Rahman (@Asif2BD) · 使用 Apache 2.0 编写 · 更多信息请访问：https://clawhub.ai/Asif2BD/openclaw-skill-lazy-loader*