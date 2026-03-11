---
name: "review"
description: "分析自动内存管理机制，以识别适合晋升的候选人、过时的数据条目、整合的机会以及系统的健康状况指标。"
command: /si:review
---
# /si:review — 分析自动记忆功能

该工具会对 Claude 代码中的自动记忆功能进行全面审计，并提出可操作的改进建议。

## 使用方法

```
/si:review                    # Full review
/si:review --quick            # Summary only (counts + top 3 candidates)
/si:review --stale            # Focus on stale/outdated entries
/si:review --candidates       # Show only promotion candidates
```

## 功能概述

### 第一步：定位内存目录

```bash
# Find the project's auto-memory directory
MEMORY_DIR="$HOME/.claude/projects/$(pwd | sed 's|/|%2F|g; s|%2F|/|; s|^/||')/memory"

# Fallback: check common path patterns
# ~/.claude/projects/<user>/<project>/memory/
# ~/.claude/projects/<absolute-path>/memory/

# List all memory files
ls -la "$MEMORY_DIR"/
```

如果内存目录不存在，可能表示自动记忆功能已被禁用。建议使用 `/memory` 命令进行检查。

### 第二步：读取并分析 `MEMORY.md` 文件

1. 读取整个 `MEMORY.md` 文件，统计行数并确认其是否超过了 200 行的文件大小限制。
2. 对文件中的每一条记录进行分析，重点关注以下内容：
   - **重复出现的指标**：
     - 相同的概念以不同的表述方式多次出现。
     - 包含“again”、“still”或“keeps happening”等词汇的描述。
     - 在多个主题文件中重复出现的记录。
   - **过时的指标**：
     - 引用了已不存在的文件（需通过 `find` 命令验证）。
     - 提到过时的工具、版本或命令。
     - 与当前的 `CLAUEDE.md` 规则相矛盾的描述。
   - **整合的时机**：
     - 关于同一主题的重复记录（例如，关于测试的记录有多条）。
     - 可以合并为简洁规则的记录。
   - **推荐优化的记录**：
     - 在多个开发会话中出现过的记录（需检查表述模式）。
     - 具有普遍适用性的记录（非项目特定内容）。
     - 可以被具体化为规则的记录。
     - 尚未收录在 `CLAUEDE.md` 或 `.claude/rules/` 目录中的记录。

### 第三步：阅读主题文件

如果 `MEMORY.md` 文件中引用了其他文件（如 `debugging.md`、`patterns.md` 等），则需要阅读这些文件：
- 检查是否存在重复的记录。
- 判断这些记录应归入 `MEMORY.md`（通用内容）还是主题文件（详细信息）。

### 第四步：与 `CLAUEDE.md` 进行对照

阅读项目的 `CLAUEDE.md` 文件（如果存在），并比较以下内容：
- `MEMORY.md` 中是否有与 `CLAUEDE.md` 规则重复的记录？（→ 从自动记忆系统中删除这些记录）。
- `MEMORY.md` 中是否有与 `CLAUEDE.md` 规则相矛盾的记录？（→ 标记为冲突项）。
- `MEMORY.md` 中是否有尚未收录到 `CLAUEDE.md` 中的常用模式？（→ 提出优化建议）。
- 同时检查 `.claude/rules/` 目录中是否已经存在相关规则。

### 第五步：生成报告

报告的输出格式如下：

```
📊 Auto-Memory Review

Memory Health:
  MEMORY.md:        {{lines}}/200 lines ({{percent}}%)
  Topic files:      {{count}} ({{names}})
  CLAUDE.md:        {{lines}} lines
  Rules:            {{count}} files in .claude/rules/

🎯 Promotion Candidates ({{count}}):
  1. "{{pattern}}" — seen {{n}}x, applies broadly
     → Suggest: {{target}} (CLAUDE.md / .claude/rules/{{name}}.md)
  2. ...

🗑️ Stale Entries ({{count}}):
  1. Line {{n}}: "{{entry}}" — {{reason}}
  2. ...

🔄 Consolidation ({{count}} groups):
  1. Lines {{a}}, {{b}}, {{c}} all about {{topic}} → merge into 1 entry
  2. ...

⚠️ Conflicts ({{count}}):
  1. MEMORY.md line {{n}} contradicts CLAUDE.md: {{detail}}

💡 Recommendations:
  - {{actionable suggestion}}
  - {{actionable suggestion}}
```

## 使用场景

- 在完成重大功能开发或调试会话后。
- 当 `/si:status` 显示 `MEMORY.md` 文件的行数超过 150 行时。
- 在项目开发活跃期间（每周进行一次）。
- 在开始新的项目阶段之前。
- 在新团队成员加入项目后（帮助他们了解项目规范）。

## 使用建议

- 建议频繁运行 `/si:review --quick`（开销较低）。
- 当 `MEMORY.md` 文件内容过于臃肿时，进行全面审计会更有价值。
- 对于被推荐优化的记录，应尽快将其转化为具体规则。
- 对于过时的记录，可随时删除——必要时自动记忆系统会重新学习这些内容。