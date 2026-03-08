---
name: cursor-agent-cli
description: >
  **Cursor Agent CLI集成**  
  – 一款基于人工智能的终端编程辅助工具。当用户提及“Cursor Agent”、“Agent CLI”、“AI编程”、“代码生成”、“代码重构”或“交互式编程会话”时，请使用该工具。
metadata:
  openclaw:
    requires:
      bins: ["agent", "cursor"]
    optional:
      bins: ["git", "gh"]
  version: "1.0.0"
  author: "OpenClaw Community"
  license: "MIT"
  tags: ["cursor", "cursor-agent", "ai-coding", "automation", "developer-tools"]
---
# Cursor CLI集成技能

🤖 **Cursor Agent**——一种基于AI的编码助手，直接集成在您的终端中。

## 什么是Cursor CLI？

Cursor提供了两个CLI工具：

1. **`cursor`**——代码编辑器启动器（类似于VS Code中的`code`命令）
2. **`agent`** ⭐——具有完整工具访问权限的交互式AI编码助手

## 安装

```bash
# macOS, Linux, WSL
curl https://cursor.com/install -fsS | bash

# Windows PowerShell
irm 'https://cursor.com/install?win32=true' | iex

# Verify installation
agent --version
```

## 快速入门

### 交互式模式

```bash
# Start interactive session
agent

# Start with initial prompt
agent "refactor the auth module to use JWT tokens"

# Resume latest session
agent resume

# Continue previous session
agent --continue

# List all sessions
agent ls
```

### 非交互式模式（脚本/持续集成）

```bash
# Run with specific prompt
agent -p "find and fix performance issues" --model "gpt-5.2"

# Code review
agent -p "review these changes for security issues" --output-format text

# JSON output for parsing
agent -p "analyze this codebase structure" --output-format json
```

## 模式

| 模式 | 描述 | 使用方法 |
|------|-------------|-------|
| **Agent** | 具有完整的代码修改权限 | 默认模式 |
| **Plan** | 仅用于读取和规划代码 | 使用`--plan`或 `/plan`命令 |
| **Ask** | 提供问答功能，但不修改代码 | 使用`--mode=ask`或 `/ask`命令 |

### 在对话过程中切换模式

```
/plan        # Switch to plan mode
/ask         # Switch to ask mode
Shift+Tab    # Toggle plan mode
```

## 云代理（后台执行）

在您离开时，可以在云端运行任务：

```bash
# Start in cloud mode
agent -c "refactor the auth module and add comprehensive tests"

# Send to cloud mid-conversation
& refactor the auth module and add comprehensive tests
```

更多信息请访问：[cursor.com/agents](https://cursor.com/agents)

## 模型

```bash
# List available models
agent --list-models

# Use specific model
agent --model "gpt-5.2"
agent --model "sonnet-4"
agent --model "sonnet-4-thinking"
```

## 高级选项

### 强制模式（自动批准）

```bash
# Auto-approve all commands
agent --force "build the feature"
agent --yolo "build the feature"  # Alias
```

### 沙箱控制

```bash
# Enable/disable sandbox
agent --sandbox enabled
agent --sandbox disabled

# Interactive sandbox menu
/sandbox
```

### 工作区与工作树

```bash
# Specify workspace
agent --workspace /path/to/project

# Start in isolated git worktree
agent -w feature-branch
agent --worktree feature-branch --worktree-base main
```

### 自定义头部信息与API密钥

```bash
# Set API key
export CURSOR_API_KEY="your-key"
agent --api-key "your-key"

# Add custom headers
agent -H "X-Custom-Header: value"
```

## 输出格式

```bash
# Text output (default)
agent -p "analyze code" --output-format text

# JSON output
agent -p "list functions" --output-format json

# Streaming JSON
agent -p "generate code" --output-format stream-json --stream-partial-output
```

## 认证

```bash
# Login
agent login

# Check status
agent status
agent whoami

# Logout
agent logout
```

## 会话管理

```bash
# Create new empty chat
agent create-chat

# Resume specific chat
agent --resume="chat-id-here"

# Resume latest
agent resume
agent --continue
```

## Cursor规则生成

```bash
# Interactive rule generation
agent generate-rule
agent rule
```

## MCP（模型上下文协议）管理

```bash
# Manage MCP servers
agent mcp

# Auto-approve MCP servers
agent --approve-mcps
```

## Shell集成

```bash
# Install shell integration
agent install-shell-integration

# Uninstall
agent uninstall-shell-integration
```

## 使用场景

### 1. 代码重构

```bash
agent "refactor the authentication module to use modern patterns"
```

### 2. 错误修复

```bash
agent -p "find and fix the memory leak in server.js"
```

### 3. 新功能开发

```bash
agent "implement user profile editing with validation"
```

### 4. 代码审查

```bash
# Review uncommitted changes
git diff | agent -p "review these changes for security issues"

# Review specific file
agent "review api/auth.js for security vulnerabilities"
```

### 5. 文档编写

```bash
agent "add comprehensive JSDoc comments to all functions"
```

### 6. 测试

```bash
agent "generate unit tests for the auth module with 90% coverage"
```

### 7. 性能优化

```bash
agent "analyze and optimize database queries in user-service.js"
```

### 8. 代码迁移

```bash
agent "migrate from Express to Fastify maintaining all functionality"
```

## 持续集成/持续交付（CI/CD）集成

```bash
#!/bin/bash
# .github/workflows/code-review.yml

# Automated code review on PR
agent -p "review changed files for security and performance issues" \
  --output-format json \
  --trust \
  > review-report.json
```

## 最佳实践

### ✅ 建议：
- 对于复杂的代码更改，先使用`--plan`模式进行规划。
- 在批准更改之前，请先审查修改内容。
- 使用`--workspace`命令指定项目目录。
- 保存重要的会话（系统会自动保存会话）。
- 仅在可信赖的环境中使用`--force`模式。

### ❌ 不建议：
- 在生产环境中直接使用`--yolo`模式进行代码修改，而无需先进行审查。
- 不要分享您的API密钥。
- 不要在不可信赖的工作环境中使用`--trust`选项。
- 请勿忽略任何安全警告。

## OpenClaw集成

### 从OpenClaw调用代理

```javascript
// Interactive session
exec({ command: "agent 'refactor auth module'", pty: true })

// Non-interactive
exec({ command: "agent -p 'analyze code' --output-format json" })
```

### 在子代理中使用Cursor Agent

在创建编码代理时，您可以将Cursor Agent作为替代方案使用：

```javascript
sessions_spawn({
  runtime: "acp",
  agentId: "cursor",  // If configured
  task: "Refactor authentication module"
})
```

## 故障排除

### 检查版本

```bash
agent --version
```

### 升级到最新版本

```bash
agent update
```

### 查看系统信息

```bash
agent about
```

### 认证问题

在无头模式下，如果系统提示关于工作区信任的问题，请按照提示操作：

```bash
agent --trust -p "your prompt"
```

## 配置

Cursor Agent的配置文件位于：
- `~/.cursor/` – 配置文件和缓存数据
- `~/.cursor/worktrees/` – Git工作树目录
环境变量：
- `CURSOR_API_KEY`
- `NO_OPEN_browser`

## 键盘快捷键（交互式模式）

| 快捷键 | 功能 |
|----------|--------|
| `Shift+Tab` | 切换到规划模式 |
| `/plan` | 切换到规划模式 |
| `/ask` | 切换到问答模式 |
| `/sandbox` | 打开沙箱菜单 |
| `/max-mode on` | 启用高级模式 |
| `& <prompt>` | 将代码发送到云代理 |

## 资源

- 📖 官方文档：https://cursor.com/docs/cli/overview
- 🌐 云代理：https://cursor.com/agents
- 💬 社区论坛：https://forum.cursor.com

## 版本信息

**当前版本**：2026.02.27-e7d2ef6

查看更新信息：`agent update`

---

## 示例

### 示例1：交互式代码重构

```bash
$ agent "refactor the user authentication system"
```

代理将：
1. 分析当前的代码结构。
2. 提出重构方案。
3. 显示文件变更内容。
4. 请求您的批准。
5. 执行代码变更。

### 示例2：自动化测试

```bash
$ agent -p "generate comprehensive tests for src/api/*.js" --force
```

非交互式模式，自动生成测试用例。

### 示例3：持续集成中的代码审查

```yaml
# .github/workflows/review.yml
- name: AI Code Review
  run: |
    agent -p "review changes for security issues" \
      --output-format json \
      --trust \
      > review.json
```

### 示例4：云端后台任务

```bash
$ agent -c "implement payment gateway integration with Stripe"
# Go do other work, check back later at cursor.com/agents
```

---

**小贴士**：经常使用`agent ls`命令来查看和恢复之前的会话记录。会话间的上下文信息会被保留！