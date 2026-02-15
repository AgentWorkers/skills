---
name: claude-code-skill
description: 通过MCP协议控制Claude代码。可以执行命令、读写文件、搜索代码，并在代理团队的支持下以编程方式使用Claude代码的所有工具。
homepage: https://github.com/enderfga/claude-code-skill
metadata: {
  "clawdis": {
    "emoji": "🤖",
    "requires": {
      "bins": ["node"],
      "env": []
    },
    "install": [
      {
        "id": "local",
        "kind": "local",
        "path": "~/clawd/claude-code-skill",
        "label": "Use local installation"
      }
    ]
  }
}
---

# Claude Code 技能

通过 MCP（模型上下文协议）控制 Claude Code。此技能可充分发挥 Claude Code 的功能，适用于 openclaw 代理，包括持久会话、代理团队以及高级工具控制。

## ⚡ 快速入门

```bash
# Start a persistent Claude session for your project
claude-code-skill session-start myproject -d ~/project \
  --permission-mode plan \
  --allowed-tools "Bash,Read,Edit,Write,Glob,Grep" \
  --max-budget 2.00

# Send a complex task (Claude will autonomously use tools)
claude-code-skill session-send myproject "Find all TODO comments and create GitHub issues" --stream

# Check progress
claude-code-skill session-status myproject
```

## 🎯 何时使用此技能

### 在以下情况下使用持久会话：
- ✅ 需要多次调用工具的多步骤任务
- ✅ 迭代开发（编写代码 → 测试 → 修复 → 重复）
- ✅ 需要完整上下文的长时间对话
- ✅ 代理需要自主工作
- ✅ 您希望获得实时反馈

### 在以下情况下使用直接 MCP 工具：
- ✅ 单个命令的执行
- ✅ 快速文件读写
- ✅ 一次性搜索
- ✅ 操作之间不需要上下文

## 📚 命令参考

### 基本 MCP 操作

```bash
# Connect to Claude Code MCP
claude-code-skill connect
claude-code-skill status
claude-code-skill tools

# Direct tool calls (no persistent session)
claude-code-skill bash "npm test"
claude-code-skill read /path/to/file.ts
claude-code-skill glob "**/*.ts" -p ~/project
claude-code-skill grep "TODO" -p ~/project -c
claude-code-skill call Write -a '{"file_path":"/tmp/test.txt","content":"Hello"}'

# Disconnect
claude-code-skill disconnect
```

### 持久会话（代理循环）

#### 启动会话

```bash
# Basic start
claude-code-skill session-start myproject -d ~/project

# With custom API endpoint (for Gemini/GPT proxy)
claude-code-skill session-start gemini-task -d ~/project \
  --base-url http://127.0.0.1:8082 \
  --model gemini-2.0-flash

# With permission mode (plan = preview changes before applying)
claude-code-skill session-start review -d ~/project --permission-mode plan

# With tool whitelist (auto-approve these tools)
claude-code-skill session-start safe -d ~/project \
  --allowed-tools "Bash(git:*),Read,Glob,Grep"

# With budget limit
claude-code-skill session-start limited -d ~/project --max-budget 1.50

# Full configuration
claude-code-skill session-start advanced -d ~/project \
  --permission-mode acceptEdits \
  --allowed-tools "Bash,Read,Edit,Write" \
  --disallowed-tools "Task" \
  --max-budget 5.00 \
  --model claude-opus-4-5 \
  --append-system-prompt "Always write tests" \
  --add-dir "/tmp,/var/log"
```

**权限模式：**
| 模式 | 描述 |
|------|-------------|
| `acceptEdits` | 自动接受文件编辑（默认） |
| `plan` | 在应用更改前预览 |
| `default` | 对每个操作都进行询问 |
| `bypassPermissions` | 跳过所有提示（危险！） |
| `delegate` | 将决策权委托给上级代理 |
| `dontAsk` | 从不询问，默认拒绝 |

#### 发送消息

```bash
# Basic send (blocks until complete)
claude-code-skill session-send myproject "Write unit tests for auth.ts"

# Streaming (see progress in real-time)
claude-code-skill session-send myproject "Refactor this module" --stream

# With custom timeout
claude-code-skill session-send myproject "Run all tests" -t 300000
```

#### 管理会话

```bash
# List active sessions
claude-code-skill session-list

# Get detailed status
claude-code-skill session-status myproject

# View conversation history
claude-code-skill session-history myproject -n 50

# Pause and resume
claude-code-skill session-pause myproject
claude-code-skill session-resume-paused myproject

# Fork a session (create a branch for experiments)
claude-code-skill session-fork myproject myproject-experiment

# Stop
claude-code-skill session-stop myproject

# Restart a failed session
claude-code-skill session-restart myproject
```

### 会话历史与搜索

```bash
# Browse all Claude Code sessions
claude-code-skill sessions -n 20

# Search sessions by project
claude-code-skill session-search --project ~/myapp

# Search by time
claude-code-skill session-search --since "2h"
claude-code-skill session-search --since "2024-02-01"

# Search by query
claude-code-skill session-search "bug fix"

# Resume a historical session
claude-code-skill resume <session-id> "Continue where we left off" -d ~/project
```

### 批量操作

```bash
# Read multiple files at once
claude-code-skill batch-read "src/**/*.ts" "tests/**/*.test.ts" -p ~/project
```

## 🤝 代理团队功能

部署多个 Claude 代理共同完成复杂任务。

### 基本代理团队

```bash
# Define a team of agents
claude-code-skill session-start team-project -d ~/project \
  --agents '{
    "architect": {
      "description": "Designs system architecture",
      "prompt": "You are a senior software architect. Design scalable, maintainable systems."
    },
    "developer": {
      "description": "Implements features",
      "prompt": "You are a full-stack developer. Write clean, tested code."
    },
    "reviewer": {
      "description": "Reviews code quality",
      "prompt": "You are a code reviewer. Check for bugs, style issues, and improvements."
    }
  }' \
  --agent architect

# Switch between agents mid-conversation
claude-code-skill session-send team-project "Design the authentication system"
# (architect responds)

claude-code-skill session-send team-project "@developer implement the design"
# (developer agent takes over)

claude-code-skill session-send team-project "@reviewer review the implementation"
# (reviewer agent takes over)
```

### 预配置的团队模板

```bash
# Code review team
claude-code-skill session-start review -d ~/project \
  --agents '{
    "security": {"prompt": "Focus on security vulnerabilities"},
    "performance": {"prompt": "Focus on performance issues"},
    "quality": {"prompt": "Focus on code quality and maintainability"}
  }' \
  --agent security

# Full-stack team
claude-code-skill session-start fullstack -d ~/project \
  --agents '{
    "frontend": {"prompt": "React/TypeScript frontend specialist"},
    "backend": {"prompt": "Node.js/Express backend specialist"},
    "database": {"prompt": "PostgreSQL/Redis database specialist"}
  }' \
  --agent frontend
```

## 🔧 高级功能

### 工具控制

```bash
# Allow specific tools with patterns
--allowed-tools "Bash(git:*,npm:*),Read,Edit"

# Deny dangerous operations
--disallowed-tools "Bash(rm:*,sudo:*),Write(/etc/*)"

# Limit to specific tool set
--tools "Read,Glob,Grep"

# Disable all tools
--tools ""
```

### 系统提示

```bash
# Replace system prompt completely
--system-prompt "You are a Python expert. Always use type hints."

# Append to existing prompt
--append-system-prompt "Always run tests after changes."
```

### 会话管理

```bash
# Resume with fork (create a branch)
--resume <session-id> --fork-session

# Use custom UUID for session
--session-id "550e8400-e29b-41d4-a716-446655440000"

# Add additional working directories
--add-dir "/var/log,/tmp/workspace"
```

### 多模型支持（代理）

使用 `--base-url` 通过代理路由请求，使其他模型（如 Gemini、GPT）能够支持 Claude Code：

```bash
# Use Gemini via claude-code-proxy
claude-code-skill session-start gemini-task -d ~/project \
  --base-url http://127.0.0.1:8082 \
  --model claude-3-5-sonnet-20241022  # Proxy will map to Gemini

# Use GPT via proxy
claude-code-skill session-start gpt-task -d ~/project \
  --base-url http://127.0.0.1:8082 \
  --model claude-3-haiku-20240307  # Proxy will map to GPT
```

**注意：** 需要 `claude-code-proxy` 在 8082 端口上运行，并配置正确的 API 密钥。

```bash
# Start the proxy
cd ~/clawd/claude-code-proxy && source .venv/bin/activate
uvicorn server:app --host 127.0.0.1 --port 8082
```

## 🎓 最佳实践

### 对于 openClaw 代理：
1. **对于多步骤任务，始终使用持久会话**
   ```bash
   # ❌ Bad: Multiple disconnect/reconnect cycles
   claude-code-skill bash "step1"
   claude-code-skill bash "step2"

   # ✅ Good: Single persistent session
   claude-code-skill session-start task -d ~/project
   claude-code-skill session-send task "Do step1 then step2"
   ```

2. **对于长时间运行的任务，使用 `--stream`**
   ```bash
   claude-code-skill session-send task "Run full test suite" --stream
   ```

3. **设置预算限制以确保安全**
   ```bash
   --max-budget 2.00  # Stop after $2 of API usage
   ```

4. **对于关键更改，使用 `plan` 模式**
   ```bash
   --permission-mode plan  # Preview before applying
   ```

5. **在实验前进行分叉操作**
   ```bash
   claude-code-skill session-fork main experimental
   claude-code-skill session-send experimental "Try risky refactor"
   ```

### 错误恢复

```bash
# If session fails:
claude-code-skill session-status myproject  # Check what happened
claude-code-skill session-history myproject -n 20  # See recent events
claude-code-skill session-restart myproject  # Restart from last good state

# If you need to start over:
claude-code-skill session-stop myproject
claude-code-skill session-start myproject -d ~/project --resume <old-session-id>
```

## 🏗️ 架构

```
openclaw agent
    ↓
claude-code-skill CLI (this tool)
    ↓ HTTP
sasha-doctor API (:18795)
    ↓ MCP
claude mcp serve (Claude Code)
    ↓
Your files & tools
```

## 🔌 可用的工具（通过 MCP）

所有 Claude Code 工具均可使用：

| 工具 | 描述 |
|------|-------------|
| Bash | 执行 shell 命令 |
| Read | 读取文件内容 |
| Write | 创建/覆盖文件 |
| Edit | 使用字符串替换编辑文件 |
| Glob | 按模式查找文件 |
| Grep | 在文件内容中搜索 |
| Task | 启动子代理 |
| WebFetch | 获取网页内容 |
| WebSearch | 在网络上搜索 |
| Git* | Git 操作 |
| AskUserQuestion | 交互式提示 |
| ... | 以及更多工具 |

## 📊 示例

### 示例 1：代码审查

```bash
claude-code-skill session-start review -d ~/myapp \
  --permission-mode plan \
  --agents '{"security":{"prompt":"Focus on security"},"quality":{"prompt":"Focus on quality"}}' \
  --agent security

claude-code-skill session-send review \
  "Review all TypeScript files in src/, check for security issues and code quality problems" \
  --stream
```

### 示例 2：自动化测试

```bash
claude-code-skill session-start test -d ~/myapp \
  --allowed-tools "Bash(npm:*,git:*),Read,Write" \
  --max-budget 1.00

claude-code-skill session-send test \
  "Find all untested functions, write unit tests, run tests, fix failures"
```

### 示例 3：多代理调试

```bash
claude-code-skill session-start debug -d ~/myapp \
  --agents '{
    "detective": {"prompt": "Find the root cause of bugs"},
    "fixer": {"prompt": "Implement fixes"},
    "tester": {"prompt": "Verify fixes work"}
  }' \
  --agent detective

claude-code-skill session-send debug "We have a memory leak in the API server" --stream
# Detective investigates, then hands off to fixer, then to tester
```

## 🔗 与 OpenClaw 的集成

当 openclaw 需要执行复杂的编码任务时：

```bash
# From within openclaw agent context:
openclaw skills run claude-code-skill -- session-start task -d ~/project
openclaw skills run claude-code-skill -- session-send task "Implement feature X" --stream
openclaw skills run claude-code-skill -- session-status task
```

或者通过 sasha-doctor HTTP API （参见 TOOLS.md 第 3 节）以编程方式使用此技能。

## 📖 参考资料

- **TOOLS.md 第 3 节** - 完整的 HTTP API 文档
- **sasha-doctor 端点** - 后端集成详情
- **Claude Code 文档** - 官方 Claude Code 文档（通过 `qmd` 工具查询）