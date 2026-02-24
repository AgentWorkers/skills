---
name: opencode
description: "OpenCode AI——一款由人工智能驱动的代码编辑器/集成开发环境（IDE），是Cursor/Windsurf的CLI（命令行接口）和TUI（图形用户界面）版本。适用场景包括：  
(1) 需要人工智能辅助的编码任务；  
(2) 利用AI进行代码重构；  
(3) 在GitHub上进行代码审查或修复；  
(4) 需要上下文信息的多文件编辑；  
(5) 在代码库上运行AI代理程序。  
**不适用场景**：  
- 简单的单行代码编辑（请使用专门的编辑工具）；  
- 文件内容阅读（请使用专门的文件阅读工具）。"
metadata:
  {
    "openclaw": { "emoji": "🤖", "requires": { "bins": ["opencode"] } },
  }
---
# OpenCode AI - 人工智能代码编辑器

OpenCode是一款**原生支持人工智能的代码编辑器**，可在终端中直接使用。你可以将其视为Cursor或Windsurf的升级版，但它是一个命令行界面（CLI）或图形用户界面（TUI）工具。

**版本**：1.2.10（通过Homebrew安装）
**平台**：macOS Darwin x64

## 先决条件

**重要提示**：OpenCode需要`sysctl`命令来检测系统架构。请确保`/usr/sbin`在系统的`PATH`环境变量中：

```bash
export PATH="/usr/sbin:/usr/bin:/sbin:/bin:$PATH"
```

如果`sysctl`命令不存在，OpenCode将无法正常运行，会出现如下错误：
```
Executable not found in $PATH: "sysctl"
```

请将以下内容永久添加到用户的`.zshrc`配置文件中：
```bash
echo 'export PATH="/usr/sbin:/usr/bin:/sbin:/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## 何时使用OpenCode

✅ **适用场景**：
- 在多个文件中进行复杂的代码重构
- 在AI的帮助下实现新功能
- 审查GitHub的Pull Request（PR）并自动修复代码问题
- 探索和理解不熟悉的代码库
- 在有上下文的情况下执行多步骤的编码任务
- 通过会话方式继续之前的工作

❌ **不适用场景**：
- 进行简单的单行编辑（使用`edit`命令）
- 读取文件内容（使用`read`命令）
- 非编码任务

---

## 核心命令

### 1. 快速操作（一次性完成）

```bash
# Run a single AI command on a project
opencode run "Add input validation to the login form"

# With specific directory
opencode run --dir ~/path/to/project "Refactor this code to use async/await"

# With specific model
opencode run -m openai/gpt-4o "Optimize the database queries"

# Attach files for context
opencode run -f src/auth.js -f src/database.js "Fix the authentication bug"

# Continue last session
opencode run --continue

# Continue specific session
opencode run --session abc123 --fork
```

### 2. 交互式TUI模式

```bash
# Start TUI in current directory
opencode

# Start TUI in specific project
opencode ~/path/to/project

# Start with specific model
opencode -m anthropic/claude-sonnet-4
```

### 3. 用户认证

```bash
# List configured providers
opencode auth list

# Login to a provider (e.g., OpenCode, OpenAI, Anthropic)
opencode auth login [url]

# Logout
opencode auth logout
```

### 4. 模型管理

```bash
# List all available models
opencode models

# List models for specific provider
opencode models openai

# List with cost metadata
opencode models --verbose

# Refresh model cache
opencode models --refresh
```

### 5. 会话管理

```bash
# List all sessions
opencode session list

# Delete a session
opencode session delete <sessionID>

# Export session data
opencode export [sessionID]

# Import session from file
opencode import <file>
```

### 6. 与GitHub集成

```bash
# Fetch and checkout a PR, then run OpenCode
opencode pr 123

# Manage GitHub agent
opencode github --help
```

### 7. MCP服务器（模型上下文协议）

```bash
# List MCP servers
opencode mcp list

# Add an MCP server
opencode mcp add

# Authenticate with OAuth MCP server
opencode mcp auth [name]

# Debug OAuth connection
opencode mcp debug <name>
```

### 8. 代理管理

```bash
# List all agents
opencode agent list

# Create a new agent
opencode agent create
```

### 9. 服务器模式

```bash
# Start headless server
opencode serve

# Start server and open web interface
opencode web

# Start ACP (Agent Client Protocol) server
opencode acp
```

### 10. 统计信息

```bash
# Show token usage and costs
opencode stats
```

---

## 常用选项（全局配置）

| 选项 | 描述 |
|------|---------|
| `-m, --model` | 要使用的模型（格式：`provider/model`） |
| `-c, --continue` | 继续上一次的会话 |
| `-s, --session` | 继续特定的会话 |
| `--fork` | 在继续会话时创建一个新的分支 |
| `--agent` | 使用特定的代理 |
| `--dir` | 编码操作的目录 |
| `--format` | 输出格式：`default` 或 `json` |
| `--thinking` | 显示模型的思考过程 |
| `--variant` | 模型的推理难度（`high`, `max`, `minimal`） |

---

## 常见使用场景

### 场景1：代码重构

```bash
opencode run "Refactor this function to be more readable and add error handling"
```

### 场景2：添加新功能

```bash
opencode run "Add a new API endpoint for user registration with email verification"
```

### 场景3：修复错误

```bash
opencode run -f error.log -f src/auth.js "Fix the authentication bug described in the error log"
```

### 场景4：代码审查

```bash
opencode run "Review this code for security vulnerabilities and suggest improvements"
```

### 场景5：GitHub PR工作流程

```bash
# Auto-fix a PR
opencode pr 123
```

### 场景6：继续之前的工作

```bash
# Continue last session
opencode run --continue

# Fork and continue (keeps original intact)
opencode run --continue --fork
```

---

## 基于会话的工作方式

OpenCode会维护会话，以便在不同运行之间保留代码的上下文：

```bash
# Start a new session
opencode run "Implement user authentication"

# Continue it later
opencode run --continue

# Or continue a specific session
opencode run --session session-abc123
```

### 会话生命周期

1. **创建会话**：运行`opencode run "prompt"`或`opencode`
2. **继续会话**：使用`--continue`或`--session <id>`
3. **分叉会话**：使用`--fork`创建新的会话分支
4. **导出会话数据**：将会话数据保存为JSON格式
5. **删除会话**：删除旧的会话

---

## 模型选择

### 模型格式

```
provider/model
```

示例：
- `openai/gpt-4o`
- `anthropic/claude-sonnet-4`
- `opencode/gpt-4o`
- `google/gemini-2.5-pro`

### 可用的模型列表

```bash
# All models
opencode models

# Provider-specific
opencode models openai
opencode models anthropic
```

### 模型推理难度设置

部分模型支持设置推理难度：
```bash
opencode run --variant high "Solve this complex algorithm problem"
opencode run --variant max "Architect a distributed system"
opencode run --variant minimal "Quick code review"
```

---

## JSON格式（用于自动化）

使用`--format json`选项可输出机器可读的JSON格式：

```bash
opencode run --format json "Refactor this code" | jq .
```

**适用场景**：
- 与持续集成/持续部署（CI/CD）系统集成
- 脚本编写
- 程序化解析结果

---

## Web界面

如需图形用户界面（GUI）体验，可以：

```bash
# Start server + open browser
opencode web

# Custom port
opencode web --port 8080

# Custom hostname
opencode web --hostname 0.0.0.0
```

---

## 常见问题及解决方法

### “找不到sysctl”错误

**问题**：OpenCode无法找到`sysctl`命令
**解决方法**：
```bash
export PATH="/usr/sbin:/usr/bin:/sbin:/bin:$PATH"
```

将`sysctl`命令的路径添加到用户的`.zshrc`配置文件中。

### “无法更改目录”错误

**问题**：OpenCode可能将命令参数误认为是目录路径
**解决方法**：明确使用`--version`、`--help`或`run`等选项来指定命令。

### OpenCode卡顿或冻结

**问题**：交互式TUI界面可能因用户输入延迟而卡住
**解决方法**：按`Ctrl+C`退出程序，或使用`run`模式进行非交互式操作。

### 权限问题

**问题**：程序无法写入文件
**解决方法**：确保用户具有相应的文件/目录写入权限：

```bash
chmod +w ./path/to/file
```

## 与OpenClaw的集成

### 通过exec工具使用OpenCode

```bash
# For simple tasks
bash command:"opencode run 'Add error handling'"

# For longer tasks (background)
bash background:true command:"opencode run 'Refactor entire codebase'"
```

### 查看当前会话

```bash
bash command:"opencode session list"
```

### 查看统计信息

```bash
bash command:"opencode stats"
```

---

## 使用技巧与最佳实践

1. **提供具体指令**：明确输入指令有助于获得更准确的结果。
2. **附加相关文件**：使用`-f`选项上传相关文件以提供上下文信息。
3. **迭代开发**：使用`--continue`选项在已有会话的基础上继续工作。
4. **安全地进行实验**：使用`--fork`选项尝试不同的模型或配置。
5. **合理选择模型**：不同模型适用于不同的任务。
6. **监控资源消耗**：使用`opencode stats`命令查看代码执行所需的资源（如API调用次数）。
7. **利用会话功能**：会话可以确保在不同操作之间保持代码的上下文一致性。

---

## 与其他工具的比较

| 功能 | OpenCode | Cursor | Windsurf | Claude Code |
|------|---------|--------|----------|-------------|
| 接口类型 | 命令行界面（CLI）/图形用户界面（TUI） | 图形用户界面（GUI） | 命令行界面（CLI） |
| 终端原生支持 | 支持 | 不支持 | 不支持 | 支持 |
| 会话管理 | 支持 | 支持 | 支持 | 支持 |
| 与GitHub PR集成 | 支持 | 支持 | 支持 | 支持 |
| 模型支持 | 多种模型 | 多种模型 | 多种模型 | 支持Anthropic模型 |
| MCP协议支持 | 支持 | 不支持 | 不支持 | 不支持 |

**推荐使用OpenCode的情况**：
- 偏好在终端中工作
- 需要与持续集成/持续部署系统集成
- 需要无界面的服务器端运行方式
- 需要使用MCP协议

---

## 文档与资源

- **版本信息**：`opencode --version`
- **帮助文档**：`opencode --help` 或 `opencode <命令> --help`
- **模型列表**：`opencode models --verbose`
- **会话管理**：`opencode session list`

---

*最后更新时间：2026-02-25*