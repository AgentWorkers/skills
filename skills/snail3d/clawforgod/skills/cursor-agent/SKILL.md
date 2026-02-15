---
name: cursor-agent
version: 2.1.0
description: 这是一项关于如何使用 Cursor CLI 工具来执行各种软件工程任务的全面技能指南（已更新至 2026 年的新功能，包含 tmux 自动化使用方法）。
author: Pushpinder Pal Singh
---

# Cursor CLI Agent 技能

本技能提供了关于如何使用 Cursor CLI 工具的全面指南和工作流程，涵盖了 2026 年 1 月更新后的所有功能。

## 安装

### 标准安装（macOS、Linux、Windows WSL）

```bash
curl https://cursor.com/install -fsS | bash
```

### 使用 Homebrew（仅限 macOS）

```bash
brew install --cask cursor-cli
```

### 安装后的配置

**macOS:**
- 将 Cursor CLI 添加到 `~/.zshrc`（zsh）或 `~/.bashrc`（bash）中的 PATH 环境变量中：
  ```bash
  export PATH="$HOME/.local/bin:$PATH"
  ```
- 重新启动终端或执行 `source ~/.zshrc`（或 `~/.bashrc`）
- 需要 macOS 10.15 或更高版本
- 支持 Intel 和 Apple Silicon Mac

**Linux/Ubuntu:**
- 重新启动终端或加载 shell 配置文件
- 通过 `agent --version` 命令验证安装是否成功

**两个平台通用:**
- 主要命令：`agent` 和 `cursor-agent`（`cursor-agent` 为向后兼容的旧命令）
- 通过 `agent --version` 或 `cursor-agent --version` 命令验证安装情况

## 认证

- 通过浏览器进行认证：
  ```bash
agent login
```

- 或使用 API 密钥进行认证：
  ```bash
export CURSOR_API_KEY=your_api_key_here
```

## 更新

确保您的 CLI 工具始终保持最新状态：
```bash
agent update
# or
agent upgrade
```

## 命令

### 交互式模式

- 启动与代理的交互式会话：
  ```bash
agent
```

- 进入初始提示界面：
  ```bash
agent "Add error handling to this API"
```

**向后兼容性说明：** `cursor-agent` 仍然可用，但 `agent` 是当前推荐的主要命令。

### 模型切换

- 列出所有可用模型：
  ```bash
agent models
# or
agent --list-models
```

- 使用特定模型：
  ```bash
agent --model gpt-5
```

- 在会话中切换模型：
  ```
/models
```

### 会话管理

- 管理代理会话：
  - **列出所有会话：`agent ls`
  - **恢复最近会话：`agent resume`
  - **恢复特定会话：`agent --resume="[chat-id]"`

### 上下文选择

- 在对话中包含特定的文件或文件夹：
  ```
@filename.ts
@src/components/
```

### 命令行操作

- 在交互式会话中可使用的命令：
  - `/models` - 交互式切换 AI 模型
  - `/compress` - 总结对话内容并释放上下文窗口空间
  - `/rules` - 直接通过 CLI 创建和编辑规则
  - `/commands` - 创建和修改自定义命令
  - `/mcp enable [server-name]` - 启用 MCP 服务器
  - `/mcp disable [server-name]` - 禁用 MCP 服务器

### 键盘快捷键

- **`Shift+Enter`** - 为多行提示添加换行符
- **`Ctrl+D`** - 退出 CLI（为安全起见，需按两次）
- **`Ctrl+R`** - 查看更改内容（按 `i` 查看说明，使用箭头键导航）
- **`ArrowUp`** - 查看上一条消息

### 非交互式模式 / CI 模式

- 以非交互式模式运行代理，适用于 CI/CD 流程：
  ```bash
agent -p 'Run tests and report coverage'
# or
agent --print 'Refactor this file to use async/await'
```

**输出格式:**
```bash
# Plain text (default)
agent -p 'Analyze code' --output-format text

# Structured JSON
agent -p 'Find bugs' --output-format json

# Real-time streaming JSON
agent -p 'Run tests' --output-format stream-json --stream-partial-output
```

**强制模式（自动应用更改，无需确认）:**
```bash
agent -p 'Fix all linting errors' --force
```

**媒体支持:**
```bash
agent -p 'Analyze this screenshot: screenshot.png'
```

### ⚠️ 与 AI 代理/自动化工具配合使用（需要 tmux）

**重要提示：** 当从自动化环境（如 AI 代理、脚本或子进程调用）中运行 Cursor CLI 时，必须使用真实的 TTY（终端）。直接执行会导致程序无限挂起。

**解决方案：使用 tmux:**
```bash
# 1. Install tmux if not available
sudo apt install tmux  # Ubuntu/Debian
brew install tmux      # macOS

# 2. Create a tmux session
tmux kill-session -t cursor 2>/dev/null || true
tmux new-session -d -s cursor

# 3. Navigate to project
tmux send-keys -t cursor "cd /path/to/project" Enter
sleep 1

# 4. Run Cursor agent
tmux send-keys -t cursor "agent 'Your task here'" Enter

# 5. Handle workspace trust prompt (first run)
sleep 3
tmux send-keys -t cursor "a"  # Trust workspace

# 6. Wait for completion
sleep 60  # Adjust based on task complexity

# 7. Capture output
tmux capture-pane -t cursor -p -S -100

# 8. Verify results
ls -la /path/to/project/
```

**原因：**
- tmux 提供了一个持久的伪终端（PTY）
- Cursor 的图形用户界面（TUI）需要交互式终端的支持
- 从子进程或执行命令中直接调用 `agent` 时，如果没有 TTY 会导致程序挂起

**注意事项：**  
```bash
# ❌ These will hang indefinitely:
agent "task"                    # No TTY
agent -p "task"                 # No TTY  
subprocess.run(["agent", ...])  # No TTY
script -c "agent ..." /dev/null # May crash Cursor
```

## 规则与配置

代理会自动从以下文件加载规则：
- `.cursor/rules`
- `AGENTS.md`
- `CLAUDE.md`

- 可通过 `/rules` 命令直接在 CLI 中创建和编辑规则。

## MCP 集成

MCP 服务器会从 `mcp.json` 配置文件中自动加载。

- 可实时启用或禁用 MCP 服务器：
  ```
/mcp enable server-name
/mcp disable server-name
```

**注意：** 支持包含空格的服务器名称。

## 工作流程

### 代码审查

- 对当前更改或特定分支进行代码审查：
  ```bash
agent -p 'Review the changes in the current branch against main. Focus on security and performance.'
```

### 代码重构

- 重构代码以提高可读性或性能：
  ```bash
agent -p 'Refactor src/utils.ts to reduce complexity and improve type safety.'
```

### 调试

- 分析日志或错误信息以找出问题根源：
  ```bash
agent -p 'Analyze the following error log and suggest a fix: [paste log here]'
```

### Git 集成

- 结合上下文信息自动化 Git 操作：
  ```bash
agent -p 'Generate a commit message for the staged changes adhering to conventional commits.'
```

### 批量处理（CI/CD）

- 在 CI/CD 流程中自动执行检查：
  ```bash
# Set API key in CI environment
export CURSOR_API_KEY=$CURSOR_API_KEY

# Run security audit with JSON output
agent -p 'Audit this codebase for security vulnerabilities' --output-format json --force

# Generate test coverage report
agent -p 'Run tests and generate coverage report' --output-format text
```

### 多文件分析

- 使用上下文选择功能分析多个文件：
  ```bash
agent
# Then in interactive mode:
@src/api/
@src/models/
Review the API implementation for consistency with our data models
```