---
name: fzf-fuzzy-finder
description: 命令行模糊查找工具，支持交互式过滤和选择功能，可与 shell、vim 等工具集成使用。
homepage: https://github.com/junegunn/fzf
metadata: {"clawdbot":{"emoji":"🔮","requires":{"bins":["fzf"]},"install":[{"id":"brew","kind":"brew","formula":"fzf","bins":["fzf"],"label":"Install fzf (brew)"},{"id":"apt","kind":"apt","package":"fzf","bins":["fzf"],"label":"Install fzf (apt)"}]}}
---

# fzf - 模糊查找工具（Fuzzy Finder）

这是一个交互式的命令行工具，具备强大的集成能力，可用于快速查找文件和目录。

## 基本用法

### 简单过滤
```bash
# Pipe list to fzf
ls | fzf

# Select file
find . -type f | fzf

# Multi-select (Tab to select, Shift+Tab to deselect)
ls | fzf -m

# Preview files while selecting
ls | fzf --preview 'cat {}'

# With bat for syntax highlighting
ls | fzf --preview 'bat --color=always {}'
```

### 与 Shell 的集成
```bash
# After installing, add to ~/.bashrc or ~/.zshrc:
# source /path/to/fzf/shell/completion.bash
# source /path/to/fzf/shell/key-bindings.bash

# Key bindings:
# Ctrl+R - Command history
# Ctrl+T - File search
# Alt+C  - Directory navigation

# Use in command line
vim **<TAB>      # File completion
cd **<TAB>       # Directory completion
kill -9 **<TAB>  # Process completion
```

## 常见用法

### 文件选择
```bash
# Open file in vim
vim $(fzf)

# Edit with preview
vim $(fzf --preview 'bat --color=always --line-range :500 {}')

# Select and copy
fzf | xargs -I {} cp {} /destination/

# Delete selected files
fzf -m | xargs rm
```

### 目录导航
```bash
# CD to selected directory
cd $(find . -type d | fzf)

# Alias for quick nav
alias cdf='cd $(find . -type d | fzf)'

# Or use Alt+C keybinding
```

### Git 集成
```bash
# Checkout branch
git branch | fzf | xargs git checkout

# Show commit
git log --oneline | fzf | awk '{print $1}' | xargs git show

# Add files interactively
git status -s | fzf -m | awk '{print $2}' | xargs git add

# Fuzzy git log browser
alias gll='git log --oneline | fzf --preview "git show {1}"'
```

### 进程管理
```bash
# Kill process
ps aux | fzf | awk '{print $2}' | xargs kill

# Kill multiple processes
ps aux | fzf -m | awk '{print $2}' | xargs kill -9
```

## 高级功能

### 预览窗口
```bash
# Preview on the right
fzf --preview 'cat {}'

# Preview position and size
fzf --preview 'cat {}' --preview-window=right:50%

# Preview with bat
fzf --preview 'bat --color=always --style=numbers --line-range=:500 {}'

# Toggle preview with Ctrl+/
fzf --preview 'cat {}' --bind 'ctrl-/:toggle-preview'

# Preview directory contents
find . -type d | fzf --preview 'ls -la {}'
```

### 自定义快捷键
```bash
# Execute action on selection
fzf --bind 'enter:execute(vim {})'

# Multiple bindings
fzf --bind 'ctrl-e:execute(vim {})' \
    --bind 'ctrl-o:execute(open {})'

# Reload on key press
fzf --bind 'ctrl-r:reload(find . -type f)'

# Accept non-matching input
fzf --print0 --bind 'enter:print-query'
```

### 过滤选项
```bash
# Case-insensitive (default)
fzf -i

# Case-sensitive
fzf +i

# Exact match
fzf -e

# Inverse match (exclude)
fzf --query='!pattern'

# OR operator
fzf --query='py$ | js$'  # .py or .js files

# AND operator
fzf --query='test .py'  # Contains both 'test' and '.py'
```

## 集成示例

### 与 ripgrep 的集成
```bash
# Search content and open in vim
rg --line-number . | fzf | awk -F: '{print "+"$2, $1}' | xargs vim

# Search and preview matches
rg --line-number . | fzf --delimiter : \
  --preview 'bat --color=always {1} --highlight-line {2}' \
  --preview-window +{2}-/2
```

### 与 fd 的集成
```bash
# Find and preview files
fd --type f | fzf --preview 'bat --color=always {}'

# Find files modified today
fd --changed-within 1d | fzf --preview 'bat {}'
```

### 与 docker 的集成
```bash
# Select and enter container
docker ps | fzf | awk '{print $1}' | xargs -I {} docker exec -it {} bash

# Remove selected images
docker images | fzf -m | awk '{print $3}' | xargs docker rmi

# View logs
docker ps | fzf | awk '{print $1}' | xargs docker logs -f
```

### 与 kubectl 的集成
```bash
# Select pod
kubectl get pods | fzf | awk '{print $1}' | xargs kubectl describe pod

# Get logs
kubectl get pods | fzf | awk '{print $1}' | xargs kubectl logs -f

# Delete pods
kubectl get pods | fzf -m | awk '{print $1}' | xargs kubectl delete pod
```

## 有用的别名

将以下别名添加到您的 Shell 配置中：
```bash
# Fuzzy file search and open in vim
alias fv='vim $(fzf --preview "bat --color=always --style=numbers {}")'

# Fuzzy directory change
alias fcd='cd $(find . -type d | fzf)'

# Fuzzy git checkout
alias gco='git branch | fzf | xargs git checkout'

# Fuzzy process kill
alias fkill='ps aux | fzf | awk "{print \$2}" | xargs kill -9'

# Fuzzy history search (Ctrl+R is built-in)
alias fh='history | fzf | awk "{print \$2}" | xargs -I {} sh -c "{}"'

# Find and edit
alias fe='fd --type f | fzf --preview "bat --color=always --style=numbers {}" | xargs -r $EDITOR'
```

## 配置

### 环境变量
```bash
# Default options
export FZF_DEFAULT_OPTS='
  --height 40%
  --layout=reverse
  --border
  --inline-info
  --preview "bat --style=numbers --color=always --line-range :500 {}"
'

# Use fd instead of find
export FZF_DEFAULT_COMMAND='fd --type f --hidden --follow --exclude .git'

# For Ctrl+T
export FZF_CTRL_T_COMMAND="$FZF_DEFAULT_COMMAND"

# For Alt+C
export FZF_ALT_C_COMMAND='fd --type d --hidden --follow --exclude .git'
```

### 颜色方案
```bash
export FZF_DEFAULT_OPTS='
  --color=bg+:#313244,bg:#1e1e2e,spinner:#f5e0dc,hl:#f38ba8
  --color=fg:#cdd6f4,header:#f38ba8,info:#cba6f7,pointer:#f5e0dc
  --color=marker:#f5e0dc,fg+:#cdd6f4,prompt:#cba6f7,hl+:#f38ba8
'
```

## 高级工作流程

### 项目文件浏览器
```bash
# Smart file browser with preview
fzf \
  --preview 'bat --color=always --style=numbers --line-range=:500 {}' \
  --preview-window='right:60%:wrap' \
  --bind 'enter:execute(vim {})' \
  --bind 'ctrl-y:execute-silent(echo {} | pbcopy)+abort' \
  --header 'Enter: edit | Ctrl+Y: copy path'
```

### 多用途搜索
```bash
# Search in files and navigate to line
rg --line-number --no-heading . | \
  fzf --delimiter=: \
      --preview 'bat --color=always --style=numbers --highlight-line {2} {1}' \
      --preview-window='+{2}-/2' \
      --bind 'enter:execute(vim {1} +{2})'
```

### Docker 容器管理器
```bash
#!/bin/bash
# docker-fzf.sh
container=$(docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Image}}" | fzf --header-lines=1 | awk '{print $1}')
if [ -n "$container" ]; then
    docker exec -it "$container" bash
fi
```

## 提示

- 使用 `--preview` 选项可查看文件预览内容
- 结合 `bat`、`rg`、`fd` 等工具可构建强大的工作流程
- 在 fzf 中按 `?` 键可查看快捷键设置
- 使用 `Tab` 键进行多选
- 使用 `Ctrl+/` 切换预览模式（如果已启用）
- 使用 `Ctrl+K` / `Ctrl+J` 进行导航
- 使用 `'` 开始精确匹配查询
- 使用 `!` 开始排除某些文件或目录
- 使用 `|` 表示“或”关系，空格表示“与”关系
- 通过设置 `FZF_DEFAULT_OPTS` 可保存配置

## 性能优化
```bash
# For large file lists, use fd or rg
export FZF_DEFAULT_COMMAND='fd --type f'

# Limit depth for faster results
export FZF_DEFAULT_COMMAND='fd --type f --max-depth 5'

# Use parallel preview
fzf --preview 'bat {}' --preview-window 'hidden'
```

## 文档资料

GitHub: https://github.com/junegunn/fzf
Wiki: https://github.com/junegunn/fzf/wiki
示例：https://github.com/junegunn/fzf/wiki/examples