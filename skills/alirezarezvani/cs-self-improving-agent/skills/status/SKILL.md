---
name: "status"
description: "内存健康状况仪表板，显示行数、主题文件数量、存储容量、过时条目以及相关建议。"
command: /si:status
---
# /si:status — 内存健康状况仪表盘

该工具可快速查看您项目中所有内存系统的内存使用情况。

## 使用方法

```
/si:status                    # Full dashboard
/si:status --brief            # One-line summary
```

## 报告内容

### 第一步：查找所有内存文件

```bash
# Auto-memory directory
MEMORY_DIR="$HOME/.claude/projects/$(pwd | sed 's|/|%2F|g; s|%2F|/|; s|^/||')/memory"

# Count lines in MEMORY.md
wc -l "$MEMORY_DIR/MEMORY.md" 2>/dev/null || echo "0"

# List topic files
ls "$MEMORY_DIR/"*.md 2>/dev/null | grep -v MEMORY.md

# CLAUDE.md
wc -l ./CLAUDE.md 2>/dev/null || echo "0"
wc -l ~/.claude/CLAUDE.md 2>/dev/null || echo "0"

# Rules directory
ls .claude/rules/*.md 2>/dev/null | wc -l
```

### 第二步：分析内存容量

| 指标        | 健康    | 警告    | 危险    |
|------------|--------|--------|--------|
| MEMORY.md 文件行数 | < 120   | 120-180 | > 180   |
| CLAUDE.md 文件行数 | < 150   | 150-200 | > 200   |
| 主题文件数量   | 0-3     | 4-6     | > 6     |
| 过期条目数量   | 0      | 1-3     | > 3     |

### 第三步：快速检查过期条目

对于每个引用文件路径的 MEMORY.md 条目，系统会进行如下检查：
```bash
# Verify referenced files still exist
grep -oE '[a-zA-Z0-9_/.-]+\.(ts|js|py|md|json|yaml|yml)' "$MEMORY_DIR/MEMORY.md" | while read f; do
  [ ! -f "$f" ] && echo "STALE: $f"
done
```

### 第四步：输出结果

```
📊 Memory Status

  Auto-Memory (MEMORY.md):
    Lines:        {{n}}/200 ({{bar}}) {{emoji}}
    Topic files:  {{count}} ({{names}})
    Last updated: {{date}}

  Project Rules:
    CLAUDE.md:    {{n}} lines
    Rules:        {{count}} files in .claude/rules/
    User global:  {{n}} lines (~/.claude/CLAUDE.md)

  Health:
    Capacity:     {{healthy/warning/critical}}
    Stale refs:   {{count}} (files no longer exist)
    Duplicates:   {{count}} (entries repeated across files)

  {{if recommendations}}
  💡 Recommendations:
    - {{recommendation}}
  {{endif}}
```

### 简化模式

```
/si:status --brief
```

输出示例：
```
📊 内存使用情况：{{n}}/200 行 | 共 {{count}} 条规则 | 状态：{{status_emoji}}（{{status_word}})
```

## 解释说明：
- **绿色（< 60%）**：内存空间充足，自动内存管理功能运行正常。
- **黄色（60-90%）**：内存即将满，请考虑运行 `/si:review` 命令来优化内存使用。
- **红色（> 90%）**：内存接近满载状态，系统可能会开始删除较旧的条目，请立即运行 `/si:review`。

## 使用建议：
- 可随时使用 `/si:status --brief` 进行快速检查。
- 如果内存使用率达到黄色或红色警告级别，请运行 `/si:review` 以识别需要优化的文件。
- 过期条目会占用不必要的空间，请删除对已不存在文件的引用。
- 主题文件是正常的——Claude 会自动创建这些文件以保持 MEMORY.md 文件的行数在 200 行以内。
```