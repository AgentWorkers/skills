---
name: fd-find
description: 一个比 `find` 更快速、更用户友好的替代工具——简单的语法、智能的默认设置，并且会尊重 `gitignore` 文件中的规则。
homepage: https://github.com/sharkdp/fd
metadata: {"clawdbot":{"emoji":"📂","requires":{"bins":["fd"]},"install":[{"id":"brew","kind":"brew","formula":"fd","bins":["fd"],"label":"Install fd (brew)"},{"id":"apt","kind":"apt","package":"fd-find","bins":["fd"],"label":"Install fd (apt)"}]}}
---

# fd - 快速文件查找工具

这是一个用户友好的 `find` 替代工具，具备智能的默认设置。

## 快速入门

### 基本搜索
```bash
# Find files by name
fd pattern

# Find in specific directory
fd pattern /path/to/dir

# Case-insensitive
fd -i pattern
```

### 常用搜索模式
```bash
# Find all Python files
fd -e py

# Find multiple extensions
fd -e py -e js -e ts

# Find directories only
fd -t d pattern

# Find files only
fd -t f pattern

# Find symlinks
fd -t l
```

## 高级用法

### 过滤
```bash
# Exclude patterns
fd pattern -E "node_modules" -E "*.min.js"

# Include hidden files
fd -H pattern

# Include ignored files (.gitignore)
fd -I pattern

# Search all (hidden + ignored)
fd -H -I pattern

# Maximum depth
fd pattern -d 3
```

### 执行方式
```bash
# Execute command on results
fd -e jpg -x convert {} {.}.png

# Parallel execution
fd -e md -x wc -l

# Use with xargs
fd -e log -0 | xargs -0 rm
```

### 正则表达式模式
```bash
# Full regex search
fd '^test.*\.js$'

# Match full path
fd --full-path 'src/.*/test'

# Glob pattern
fd -g "*.{js,ts}"
```

## 基于时间的过滤
```bash
# Modified within last day
fd --changed-within 1d

# Modified before specific date
fd --changed-before 2024-01-01

# Created recently
fd --changed-within 1h
```

## 基于文件大小的过滤
```bash
# Files larger than 10MB
fd --size +10m

# Files smaller than 1KB
fd --size -1k

# Specific size range
fd --size +100k --size -10m
```

## 输出格式化
```bash
# Absolute paths
fd --absolute-path

# List format (like ls -l)
fd --list-details

# Null separator (for xargs)
fd -0 pattern

# Color always/never/auto
fd --color always pattern
```

## 常见使用场景

- **查找并删除旧文件：**
```bash
fd --changed-before 30d -t f -x rm {}
```

- **查找大文件：**
```bash
fd --size +100m --list-details
```

- **将所有 PDF 文件复制到指定目录：**
```bash
fd -e pdf -x cp {} /target/dir/
```

- **统计所有 Python 文件的行数：**
```bash
fd -e py -x wc -l | awk '{sum+=$1} END {print sum}'
```

- **查找损坏的符号链接：**
```bash
fd -t l -x test -e {} \; -print
```

- **在特定时间窗口内进行搜索：**
```bash
fd --changed-within 2d --changed-before 1d
```

## 与其他工具的集成

- **与 ripgrep 集成：**
```bash
fd -e js | xargs rg "pattern"
```

- **与 fzf（模糊文件查找器）集成：**
```bash
vim $(fd -t f | fzf)
```

- **与 bat（cat 的替代工具）集成：**
```bash
fd -e md | xargs bat
```

## 性能提示

- `fd` 通常比 `find` 快得多。
- 默认情况下会尊重 `.gitignore` 文件（使用 `-I` 可禁用此功能）。
- 会自动使用并行扫描方式。
- 智能区分大小写：小写匹配不区分大小写，大写匹配区分大小写。

## 使用技巧

- 使用 `-t` 进行文件类型过滤（例如：`f` 表示文件，`d` 表示目录，`l` 表示符号链接，`x` 表示可执行文件）。
- 使用 `-e` 过滤文件扩展名比使用 `-g "*.ext"` 更简单。
- 在 `-x` 命令中，`{}` 表示找到的文件路径；`{.}` 会去掉文件扩展名；`/{/}` 会提取文件名（不包含扩展名）；`//` 会提取文件所在的目录。

## 文档资料

GitHub: https://github.com/sharkdp/fd
手册页：`man fd`