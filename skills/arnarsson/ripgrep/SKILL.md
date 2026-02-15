---
name: ripgrep
description: 这款文本搜索工具速度极快，能够递归地在目录中搜索符合正则表达式（regex）的模式，同时还会考虑 `gitignore` 规则的设置。
homepage: https://github.com/BurntSushi/ripgrep
metadata: {"clawdbot":{"emoji":"🔎","requires":{"bins":["rg"]},"install":[{"id":"brew","kind":"brew","formula":"ripgrep","bins":["rg"],"label":"Install ripgrep (brew)"},{"id":"apt","kind":"apt","package":"ripgrep","bins":["rg"],"label":"Install ripgrep (apt)"}]}}
---

# ripgrep (rg)

一个快速、智能的递归搜索工具。默认情况下会尊重 `.gitignore` 文件中的排除规则。

## 快速入门

### 基本搜索
```bash
# Search for "TODO" in current directory
rg "TODO"

# Case-insensitive search
rg -i "fixme"

# Search specific file types
rg "error" -t py       # Python files only
rg "function" -t js    # JavaScript files
```

### 常用搜索模式
```bash
# Whole word match
rg -w "test"

# Show only filenames
rg -l "pattern"

# Show with context (3 lines before/after)
rg -C 3 "function"

# Count matches
rg -c "import"
```

## 高级用法

### 文件类型过滤
```bash
# Multiple file types
rg "error" -t py -t js

# Exclude file types
rg "TODO" -T md -T txt

# List available types
rg --type-list
```

### 搜索修饰符
```bash
# Regex search
rg "user_\d+"

# Fixed string (no regex)
rg -F "function()"

# Multiline search
rg -U "start.*end"

# Only show matches, not lines
rg -o "https?://[^\s]+"
```

### 路径过滤
```bash
# Search specific directory
rg "pattern" src/

# Glob patterns
rg "error" -g "*.log"
rg "test" -g "!*.min.js"

# Include hidden files
rg "secret" --hidden

# Search all files (ignore .gitignore)
rg "pattern" --no-ignore
```

## 替换操作
```bash
# Preview replacements
rg "old_name" --replace "new_name"

# Actually replace (requires extra tool like sd)
rg "old_name" -l | xargs sed -i 's/old_name/new_name/g'
```

## 性能技巧
```bash
# Parallel search (auto by default)
rg "pattern" -j 8

# Skip large files
rg "pattern" --max-filesize 10M

# Memory map files
rg "pattern" --mmap
```

## 常见使用场景

- **在代码中查找待办事项（TODOs）：**
  ```bash
rg "TODO|FIXME|HACK" --type-add 'code:*.{rs,go,py,js,ts}' -t code
```

- **在特定分支中搜索：**
  ```bash
git show branch:file | rg "pattern"
```

- **查找包含多个模式的文件：**
  ```bash
rg "pattern1" | rg "pattern2"
```

- **带上下文和颜色显示搜索结果：**
  ```bash
rg -C 2 --color always "error" | less -R
```

## 与 grep 的比较

- **更快**：通常比 `grep` 快 5-10 倍
- **更智能**：会尊重 `.gitignore` 文件的规则，跳过二进制文件
- **更好的默认设置**：支持递归搜索、彩色输出以及显示行号
- **更易使用**：对于常见任务，语法更简洁

## 使用技巧

- `rg` 通常比 `grep -r` 更快
- 使用 `-t` 选项进行文件类型过滤，而不是 `--include`
- 可以与其他工具结合使用：`rg pattern -l | xargs tool`
- 可以在 `~/.ripgreprc` 文件中自定义文件类型
- 使用 `--stats` 选项查看搜索性能

## 文档资料

GitHub: https://github.com/BurntSushi/ripgrep
用户指南: https://github.com/BurntSushi/ripgrep/blob/master/GUIDE.md