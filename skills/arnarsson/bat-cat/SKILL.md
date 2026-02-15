---
name: bat-cat
description: 一个具备语法高亮、行号显示以及 Git 集成功能的文本编辑器克隆版——它是 `cat` 的现代替代品。
homepage: https://github.com/sharkdp/bat
metadata: {"clawdbot":{"emoji":"🦇","requires":{"bins":["bat"]},"install":[{"id":"brew","kind":"brew","formula":"bat","bins":["bat"],"label":"Install bat (brew)"},{"id":"apt","kind":"apt","package":"bat","bins":["bat"],"label":"Install bat (apt)"}]}}
---

# bat - 更优秀的 `cat` 工具

`bat` 提供了语法高亮显示、行号显示以及与 Git 的集成功能。

## 快速入门

### 基本用法
```bash
# View file with syntax highlighting
bat README.md

# Multiple files
bat file1.js file2.py

# With line numbers (default)
bat script.sh

# Without line numbers
bat -p script.sh
```

### 查看模式
```bash
# Plain mode (like cat)
bat -p file.txt

# Show non-printable characters
bat -A file.txt

# Squeeze blank lines
bat -s file.txt

# Paging (auto for large files)
bat --paging=always file.txt
bat --paging=never file.txt
```

## 语法高亮显示

### 语言检测
```bash
# Auto-detect from extension
bat script.py

# Force specific language
bat -l javascript config.txt

# Show all languages
bat --list-languages
```

### 主题样式
```bash
# List available themes
bat --list-themes

# Use specific theme
bat --theme="Monokai Extended" file.py

# Set default theme in config
# ~/.config/bat/config: --theme="Dracula"
```

## 行号显示
```bash
# Show specific lines
bat -r 10:20 file.txt

# From line to end
bat -r 100: file.txt

# Start to specific line
bat -r :50 file.txt

# Multiple ranges
bat -r 1:10 -r 50:60 file.txt
```

## Git 集成
```bash
# Show Git modifications (added/removed/modified lines)
bat --diff file.txt

# Show decorations (Git + file header)
bat --decorations=always file.txt
```

## 输出控制
```bash
# Output raw (no styling)
bat --style=plain file.txt

# Customize style
bat --style=numbers,changes file.txt

# Available styles: auto, full, plain, changes, header, grid, numbers, snip
bat --style=header,grid,numbers file.txt
```

## 常见用法

- **快速预览文件内容：**
```bash
bat file.json
```

- **以语法高亮方式查看日志：**
```bash
bat error.log
```

- **可视化比较文件差异：**
```bash
bat --diff file1.txt
bat file2.txt
```

- **编辑前预览文件内容：**
```bash
bat config.yaml && vim config.yaml
```

- **在管道中替代 `cat` 命令：**
```bash
bat -p file.txt | grep "pattern"
```

- **查看特定函数内容：**
```bash
bat -r 45:67 script.py  # If function is on lines 45-67
```

## 与其他工具的集成

- **作为 man 页面的翻页器：**
```bash
export MANPAGER="sh -c 'col -bx | bat -l man -p'"
man grep
```

- **与 ripgrep 的集成：**
```bash
rg "pattern" -l | xargs bat
```

- **与 fzf 的集成：**
```bash
fzf --preview 'bat --color=always --style=numbers {}'
```

- **与 diff 的集成：**
```bash
diff -u file1 file2 | bat -l diff
```

## 配置

在 `~/.config/bat/config` 文件中配置默认设置：

```
# Set theme
--theme="Dracula"

# Show line numbers, Git modifications and file header, but no grid
--style="numbers,changes,header"

# Use italic text on terminal
--italic-text=always

# Add custom mapping
--map-syntax "*.conf:INI"
```

## 性能提示

- 在管道中使用 `-p` 选项以获取纯文本输出。
- 当输出结果需要被程序处理时，使用 `--paging=never` 选项。
- `bat` 会缓存已解析的文件内容，以提高后续访问速度。

## 其他提示

- **别名：** 可将 `cat` 别名为 `bat -p`，以便直接替换 `cat` 命令。
- **作为翻页器使用：** 通过 `export PAGER="bat"` 将 `bat` 设置为系统默认的翻页器。
- **在 Debian/Ubuntu 系统上：** 可使用 `batcat` 代替 `bat`。
- **自定义语法样式：** 将自定义语法规则添加到 `~/.config/bat/syntaxes/` 文件中。
- **处理大文件时：** 使用 `bat --paging=never` 或直接使用 `cat`。

## 常见参数

- `-p` / `--plain`：纯文本模式（不显示行号和装饰性元素）。
- `-n` / `--number`：仅显示行号。
- `-A` / `--show-all`：显示所有字符（包括不可打印字符）。
- `-l` / `--language`：设置语法高亮的语言。
- `-r` / `--line-range`：仅显示指定范围内的行。

## 文档资料

GitHub: https://github.com/sharkdp/bat
man 页面: `man bat`
自定义设置: https://github.com/sharkdp/bat#customization