---
name: review
description: "分析自动内存管理情况，以识别适合晋升的候选人、过时的条目、整合机会以及系统健康指标。"
command: /si:review
---
# /si:review — 分析自动记忆功能

该工具会对 Claude 代码中的自动记忆功能进行全面审计，并提出可执行的改进建议。

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

如果内存目录不存在，系统会提示自动记忆功能可能已被禁用。建议使用 `/memory` 命令进行检查。

### 第二步：读取并分析 `MEMORY.md` 文件

1. 读取整个 `MEMORY.md` 文件，统计行数并确认其是否超过了 200 行的文件长度限制。
2. 对文件中的每一条记录进行分析：
   - **重复性指标**：
     - 相同的概念以不同的表述方式多次出现。
     - 包含 “again”（再次）、”still”（仍然） 或 “keeps happening”（持续发生） 等关键词的描述。
     - 在多个主题文件中重复出现的记录。
   - **过时性指标**：
     - 引用了已不存在的文件（需使用 `find` 命令进行验证）。
     - 提及过时的工具、版本或命令。
     - 与当前的 `CLAUDE.md` 规则相矛盾的记录。
   - **整合机会**：
     - 关于同一主题的重复记录（例如，关于测试的记录有多条）。
     - 可以合并为简洁规则的重复条目。
   - **推荐优化条目**（满足所有条件的条目）：
     - 在多个开发会话中出现过（需检查表述模式）。
     - 不属于特定项目的通用知识（具有广泛实用性）。
     - 可以被具体化为规则的形式。
     - 未收录在 `CLAUDE.md` 或 `.claude/rules/` 目录中的条目。

### 第三步：阅读主题文件

如果 `MEMORY.md` 文件中引用了其他文件（如 `debugging.md`、`patterns.md` 等），则需要阅读这些文件：
- 检查是否存在与 `MEMORY.md` 中重复的条目。
- 判断这些条目应归入 `MEMORY.md`（通用内容）还是相应的主题文件（详细信息）。

### 第四步：与 `CLAUDE.md` 进行对比

1. 读取项目的 `CLAUDE.md` 文件（如果存在），并检查以下内容：
   - `MEMORY.md` 中是否有与 `CLAUDE.md` 规则重复的条目？（如有的话，应将其从自动记忆列表中删除）。
   - `MEMORY.md` 中是否有与 `CLAUDE.md` 规则相矛盾的条目？（如有，应标记为冲突）。
   - `MEMORY.md` 中是否有尚未收录到 `CLAUDE.md` 中的实用模式？（符合条件的条目应被推荐加入 `CLAUDE.md`）。
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
- 当 `/si:status` 显示 `MEMORY.md` 文件长度超过 150 行时。
- 在项目开发活跃期间（每周进行一次）。
- 在新团队成员入职前（帮助他们了解项目的最佳实践）。

## 使用建议

- 经常运行 `/si:review --quick` 命令（开销较低）。
- 当 `MEMORY.md` 文件内容变得过于冗长时，进行全面审查尤为重要。
- 对被推荐优化的条目要尽快采取行动——这些条目已被证明是有效的实践方案。
- 如有过时的条目，请毫不犹豫地删除它们——系统会在需要时重新学习这些内容。