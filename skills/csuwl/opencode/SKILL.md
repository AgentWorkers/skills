---
name: opencode
description: "OpenCode AI——一款由人工智能驱动的代码编辑器/集成开发环境（IDE），提供命令行（CLI）和图形用户界面（TUI）两种使用方式。适用场景包括：  
(1) 需要人工智能辅助的编码任务；  
(2) 利用人工智能进行代码重构；  
(3) 在 GitHub 上审查和修改代码提交（PR）；  
(4) 需要上下文信息的多文件编辑；  
(5) 在代码库上运行人工智能辅助工具。  
**不适用场景**：  
- 简单的单行代码编辑（请使用专门的编辑工具）；  
- 仅用于读取文件内容（请使用专门的文件读取工具）。"
metadata:
  {
    "openclaw": { "emoji": "🤖", "requires": { "bins": ["opencode"] } },
  }
---
# OpenCode AI - 人工智能代码编辑器

OpenCode 是一款 **原生支持人工智能的代码编辑器**，可在终端中直接使用。你可以将其视为 Cursor 或 Windsurf 的升级版，但它更适合通过命令行界面（CLI）或图形用户界面（TUI）进行操作。

**版本**: 1.2.10（通过 Homebrew 安装）
**平台**: macOS Darwin x64

## 先决条件

**重要提示**: OpenCode 需要 `sysctl` 命令来检测系统架构。请确保 `/usr/sbin` 在你的 PATH 环境变量中：

```bash
export PATH="/usr/sbin:/usr/bin:/sbin:/bin:$PATH"
```

如果缺少 `sysctl`，OpenCode 将无法正常运行，会出现如下错误：
```
Executable not found in $PATH: "sysctl"
```

请将以下内容永久添加到你的 `~/.zshrc` 文件中：
```bash
echo 'export PATH="/usr/sbin:/usr/bin:/sbin:/bin:$PATH"' >> ~/.zshrc
source ~/.zshrc
```

---

## 何时使用 OpenCode

✅ **适用场景**：
- 在多个文件中进行复杂的代码重构
- 在 AI 的辅助下实现新功能
- 审查 GitHub 的 Pull Request 并自动修复代码问题
- 探索和理解不熟悉的代码库
- 在有上下文的情况下执行多步骤的编码任务
- 通过会话模式继续之前的工作

❌ **不适用场景**：
- 进行简单的单行编辑（使用 `edit` 工具）
- 读取文件内容（使用 `read` 工具）
- 非编码任务

---

## 核心操作（TUI 命令）

在 **TUI 模式** 下运行 OpenCode 时，你可以使用以下命令来控制 AI 的工作流程：

### /sessions - 会话管理
```
/sessions
```
- 打开会话选择器
- 选择继续现有的会话
- 创建新会话（需要用户确认）
- 建议：为当前项目选择现有的会话

### /agents - 代理（模式）控制
```
/agents
```
可用代理：
- **plan** - 规划模式（分析并设计代码）
- **build** - 编码模式（实现代码）
- **explore** - 探索模式（理解代码库）
- **general** - 提供通用帮助

**最佳实践**：始终先选择 **plan** 模式，确认后切换到 **build** 模式。

### /models - 模型选择
```
/models
```
- 打开模型选择器
- 按提供者过滤模型（如 OpenAI、Anthropic、Google、Z.AI 等）
- 为任务选择合适的模型
- 如果需要认证，请按照提示链接进行登录

### 代理工作流程

#### 规划代理行为
- 让 OpenCode 分析任务
- 请求详细的步骤计划
- 允许 OpenCode 提出问题以获取更多信息
- 仔细审查计划
- 如果计划不完整，请求修改
- **在 Plan 模式下不允许生成代码**

#### 编码代理行为
- 使用 `/agents` 切换到 Build 模式
- 让 OpenCode 实现已批准的计划
- 如果 OpenCode 有疑问，返回 Plan 模式
- 回答问题并确认计划，然后继续编码

#### Plan → Build 循环
1. 使用 `/agents` 选择 **plan** 代理
2. 描述任务
3. 审查并批准计划
4. 使用 `/agents` 切换到 **build** 代理
5. 实现计划
6. 重复此过程直到满意

**关键规则**：
- 绝不要跳过 Plan 模式
- 在 Build 模式下不要回答问题（先返回 Plan 模式）
- 始终在输出中明确显示所有命令

### 其他有用命令
- **/title** - 更改会话标题
- **/summary** - 生成会话摘要
- **/compaction** - 压缩对话记录

---

## 核心命令

### 1. 快速任务（一次性操作）

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

### 2. 交互式 TUI 模式

```bash
# Start TUI in current directory
opencode

# Start TUI in specific project
opencode ~/path/to/project

# Start with specific model
opencode -m anthropic/claude-sonnet-4
```

### 3. 认证

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

### 6. GitHub 集成

```bash
# Fetch and checkout a PR, then run OpenCode
opencode pr 123

# Manage GitHub agent
opencode github --help
```

### 7. MCP 服务器（模型上下文协议）

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

## 全局选项

| 选项 | 描述 |
|--------|-------------|
| `-m, --model` | 使用的模型（格式：`provider/model`） |
| `-c, --continue` | 继续上一个会话 |
| `-s, --session` | 继续特定的会话 |
| `--fork` | 在继续时会话时创建分支 |
| `--agent` | 使用特定的代理 |
| `--dir` | 运行目录 |
| `--format` | 输出格式：`default` 或 `json` |
| `--thinking` | 显示思考过程 |
| `--variant` | 模型的推理难度（`high`, `max`, `minimal`） |

---

## 常见使用场景

### 场景 1：代码重构

```bash
opencode run "Refactor this function to be more readable and add error handling"
```

### 场景 2：添加新功能

```bash
opencode run "Add a new API endpoint for user registration with email verification"
```

### 场景 3：修复错误

```bash
opencode run -f error.log -f src/auth.js "Fix the authentication bug described in the error log"
```

### 场景 4：代码审查

```bash
opencode run "Review this code for security vulnerabilities and suggest improvements"
```

### 场景 5：GitHub Pull Request 流程

```bash
# Auto-fix a PR
opencode pr 123
```

### 场景 6：继续之前的工作

```bash
# Continue last session
opencode run --continue

# Fork and continue (keeps original intact)
opencode run --continue --fork
```

---

## 基于会话的工作方式

OpenCode 会保存会话信息，以便在不同会话之间保持工作上下文：

```bash
# Start a new session
opencode run "Implement user authentication"

# Continue it later
opencode run --continue

# Or continue a specific session
opencode run --session session-abc123
```

### 会话生命周期
1. **创建会话**：运行 `opencode run "prompt"` 或 `opencode`
2. **继续会话**：使用 `--continue` 或 `--session <id>`
3. **分叉会话**：使用 `--fork` 创建会话分支
4. **导出会话**：将会话数据保存为 JSON 文件
5. **删除会话**：删除旧会话

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

### 查看可用模型

```bash
# All models
opencode models

# Provider-specific
opencode models openai
opencode models anthropic
```

### 模型推理难度设置

部分模型支持设置不同的推理难度级别：

```bash
opencode run --variant high "Solve this complex algorithm problem"
opencode run --variant max "Architect a distributed system"
opencode run --variant minimal "Quick code review"
```

---

## JSON 格式（用于自动化）

使用 `--format json` 可以获得机器可读的输出格式：

```bash
opencode run --format json "Refactor this code" | jq .
```

**适用场景**：
- 代码持续集成（CI/CD）集成
- 脚本编写
- 程序化解析结果

---

## Web 界面

如需图形用户界面（GUI），可以访问：

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

### “找不到 sysctl” 错误

**问题**：OpenCode 无法找到 `sysctl` 命令
**解决方法**：
```bash
export PATH="/usr/sbin:/usr/bin:/sbin:/bin:$PATH"
```

将相关命令添加到 `~/.zshrc` 文件中，使其成为系统配置的一部分。

### “无法切换目录” 错误

**问题**：OpenCode 将参数误认为是目录路径
**解决方法**：使用 `--version`、`--help` 或 `run` 等参数明确指定目录路径：
```bash
# Wrong
opencode version

# Right
opencode --version
```

### OpenCode 停滞或卡住

**问题**：交互式 TUI 界面等待用户输入
**解决方法**：按 `Ctrl+C` 退出程序，或使用 `run` 模式进行非交互式操作。

### 权限问题

**问题**：程序无法写入文件
**解决方法**：确保用户具有写入文件/目录的权限：
```bash
chmod +w ./path/to/file
```

---

## 与 OpenClaw 的集成

### 通过 exec 工具使用 OpenCode

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

1. **提供具体要求**：明确的任务描述有助于获得更好的结果
2. **附带相关文件**：使用 `-f` 选项上传相关文件以提供上下文信息
3. **迭代开发**：使用 `--continue` 选项在现有基础上继续工作
4. **安全地进行实验**：使用 `--fork` 分支尝试不同的方案
5. **谨慎选择模型**：不同模型适用于不同的任务
6. **监控使用情况**：使用 `opencode stats` 查看令牌使用情况
7. **利用会话功能**：会话可以帮助你在多次操作中保持工作上下文

---

## 与其他工具的比较

| 功能 | OpenCode | Cursor | Windsurf | Claude Code |
|---------|----------|--------|----------|-------------|
| 接口类型 | CLI/TUI | GUI | GUI | CLI |
| 终端原生支持 | ✅ | ❌ | ❌ | ✅ |
| 会话管理 | ✅ | ✅ | ✅ | ✅ |
| GitHub PR 集成 | ✅ | ✅ | ✅ | ✅ |
| 模型支持 | 多种模型 | 多种模型 | 多种模型 | 支持 Anthropic 模型 |
| MCP 协议支持 | ✅ | ❌ | ❌ | ❌ |

**选择 OpenCode 的理由**：
- 如果你更喜欢终端工作方式
- 需要代码持续集成（CI/CD）功能
- 需要无界面（headless）或服务器端运行模式
- 需要支持 MCP 协议

---

## 文档与资源

- **版本信息**：`opencode --version`
- **帮助文档**：`opencode --help` 或 `opencode <command> --help`
- **模型列表**：`opencode models --verbose`
- **会话管理**：`opencode session list`

---

*最后更新时间：2026-02-25*