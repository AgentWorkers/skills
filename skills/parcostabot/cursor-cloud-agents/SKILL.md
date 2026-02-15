---
name: cursor-cloud-agents
description: "将 Cursor AI 代理部署到 GitHub 仓库中。利用您现有的 Cursor 订阅服务，自动编写代码、生成测试用例、创建文档，并提交 Pull Request（PR）。"
requirements:
  env:
    - CURSOR_API_KEY
  binaries:
    - bash
    - curl
    - jq
    - base64
  files:
    read:
      - ~/.openclaw/.env
      - ~/.openclaw/.env.local
      - .env
      - ~/.cursor/config.json
    write:
      - ~/.cache/cursor-api/
security:
  notes: |
    This skill reads CURSOR_API_KEY from multiple locations for convenience:
    environment variable, ~/.openclaw/.env, ~/.openclaw/.env.local, .env, 
    and ~/.cursor/config.json. Cache at ~/.cache/cursor-api/ is unencrypted.
    See SECURITY.md for full details.
---

# Cursor Cloud Agents 技能

## ⚡ 快速参考

**最常见的命令和模式：**

```bash
# Launch an agent (uses default model: gpt-5.2)
cursor-api.sh launch --repo owner/repo --prompt "Add tests for auth module"

# Check agent status
cursor-api.sh status <agent-id>

# Get conversation history
cursor-api.sh conversation <agent-id>

# Send follow-up message
cursor-api.sh followup <agent-id> --prompt "Also add edge case tests"

# List all agents
cursor-api.sh list

# Check usage/quota
cursor-api.sh usage
```

**常用选项：**
- `--model <名称>` - 指定模型（默认：gpt-5.2）
- `--branch <名称>` - 目标分支
- `--no-pr` - 不自动创建 Pull Request (PR)
- `--no-cache` - 绕过缓存
- `--verbose` - 显示详细调试信息
- `--background` - 在后台模式下运行代理

**后台任务：**
```bash
cursor-api.sh launch --repo owner/repo --prompt "..." --background
cursor-api.sh bg-list
cursor-api.sh bg-status <task-id>
cursor-api.sh bg-logs <task-id>
```

**后台任务的最大运行时间：**
```bash
# Default is 24 hours
 cursor-api.sh launch --repo owner/repo --prompt "..." --background

# Custom max runtime (2 hours)
cursor-api.sh launch --repo owner/repo --prompt "..." --background --max-runtime 7200

# Unlimited runtime (not recommended)
cursor-api.sh launch --repo owner/repo --prompt "..." --background --max-runtime 0

# Set default via environment variable
export CURSOR_BG_MAX_RUNTIME=43200  # 12 hours
cursor-api.sh launch --repo owner/repo --prompt "..." --background
```

**简短命令（别名）：**

为了更快捷的日常使用，可以引用 `cca-aliases.sh` 文件：
```bash
source scripts/cca-aliases.sh
```

然后使用 `cca` 代替 `cursor-api.sh`：
```bash
cca list                    # List agents
cca launch --repo ...       # Launch agent
cca status <id>             # Check status
cca conversation <id>       # Get conversation
cca followup <id> --prompt  # Send followup
cca delete <id>             # Delete agent
```

**退出代码：** 0=成功，1=API 错误，2=身份验证失败，3=达到速率限制，4=仓库访问失败，5=参数无效

---

## 概述

此技能封装了 Cursor Cloud Agents 的 HTTP API，允许 OpenClaw 向 Cursor 的云代理分发编码任务、监控它们的进度并整合结果。

### 适用场景

当您需要执行以下操作时，请使用此技能：
- 将编码任务委托给在 GitHub 仓库中运行的 Cursor 代理
- 在现有代码库上生成代码、测试或文档
- 异步执行重构或功能实现
- 对代码更改获取“第二意见”

### 不适用场景

- 对于不需要修改代码的简单问题
- 需要实时响应的情况（请使用本地 Cursor CLI）
- 适用于非 GitHub 仓库的任务

## 身份验证

该技能会自动从以下位置查找您的 Cursor API 密钥（按顺序）：
1. **环境变量：** `CURSOR_API_KEY`
2. **OpenClaw 环境文件：** `~/.openclaw/.env`
3. **OpenClaw 本地环境：** `~/.openclaw/.env.local`
4. **项目环境文件：** 当前目录下的 `.env`
5. **Cursor 配置文件：** `~/.cursor/config.json`

**建议：** 将 API 密钥添加到 `~/.openclaw/.env` 中：
```bash
CURSOR_API_KEY=your_cursor_api_key_here
```

获取 API 密钥的步骤：
1. 打开 Cursor IDE
2. 转到设置 → 通用
3. 复制您的 API 密钥

**验证其是否有效：**
```bash
cursor-api.sh me
```

## 工作流程模式

### 模式 A：一次性执行

启动代理并让其独立运行，之后再进行检查。

```bash
# Launch agent (uses default model: gpt-5.2)
cursor-api.sh launch --repo owner/repo --prompt "Add comprehensive tests for auth module"

# Launch with specific model
cursor-api.sh launch --repo owner/repo --prompt "Add tests" --model claude-4-opus

# Response: {"id": "agent_123", "status": "CREATING", ...}

# Later - check status
cursor-api.sh status agent_123
```

**注意：** 如果未指定 `--model`，将自动使用默认模型（`gpt-5.2`）。系统会显示正在使用的模型。

**适合场景：** 不需要立即关注的任务、探索性工作

### 模式 B：监督式执行

启动代理、监控并在完成后报告结果。

```bash
# 1. Launch
cursor-api.sh launch --repo owner/repo --prompt "Implement user authentication"

# 2. Poll for completion (check every 60 seconds)
while true; do
    status=$(cursor-api.sh status agent_123)
    if [[ $(echo "$status" | jq -r '.status') == "FINISHED" ]]; then
        break
    fi
    sleep 60
done

# 3. Get results
cursor-api.sh conversation agent_123 | jq -r '.messages[] | select(.role == "assistant") | .content'
```

**适合场景：** 需要报告完成情况的重要任务

### 模式 C：迭代协作

启动代理、审查结果后发送后续指令以完善工作。

```bash
# 1. Launch initial task
cursor-api.sh launch --repo owner/repo --prompt "Add login page"

# 2. Review conversation
cursor-api.sh conversation agent_123

# 3. Send follow-up
cursor-api.sh followup agent_123 --prompt "Also add form validation and error handling"

# 4. Final review when done
cursor-api.sh conversation agent_123
```

**适合场景：** 需要多次迭代的复杂任务

### 模式 D：后台模式

对于长时间运行的任务，在后台模式下启动代理，并在之后进行检查。

```bash
# Launch in background
result=$(cursor-api.sh launch --repo owner/repo --prompt "Refactor entire codebase" --background)
task_id=$(echo "$result" | jq -r '.background_task_id')
echo "Task started: $task_id"

# List active background tasks
cursor-api.sh bg-list

# Check specific task status
cursor-api.sh bg-status $task_id

# View logs
cursor-api.sh bg-logs $task_id

# List all tasks including completed ones
cursor-api.sh bg-list --all
```

后台任务会自动被监控，日志会保存在 `~/.cache/cursor-api/background-tasks/` 目录下。

**适合场景：** 长时间运行的任务（超过 10 分钟）、批量操作、CI/CD 集成

## 命令参考

### 列出代理

```bash
cursor-api.sh list
```

返回所有代理的信息，包括状态、仓库和创建时间。

### 启动代理

```bash
cursor-api.sh launch --repo owner/repo --prompt "Your task description" [--model model-name] [--branch branch-name] [--no-pr] [--background]
```

选项：
- `--repo`（必选）：仓库地址（格式为 `owner/repo`）
- `--prompt`（必选）：代理的初始指令
- `--model`（可选）：要使用的模型（未指定时默认为 `gpt-5.2`）
- `--branch`（可选）：目标分支名称（省略时自动生成）
- `--no-pr`（可选）：不自动创建 Pull Request
- `--background`（可选）：在后台模式下运行代理

**注意：** 如果未指定 `--model`，系统会自动使用 `gpt-5.2` 并显示正在使用的模型。

**后台模式：** 使用 `--background` 时，命令会立即返回一个 `background_task_id`。可以使用 `bg-list`、`bg-status` 和 `bg-logs` 命令来监控进度。

### 检查状态

```bash
cursor-api.sh status <agent-id>
```

返回：
- `status`：CREATING（创建中）、RUNNING（运行中）、FINISHED（已完成）、STOPPED（已停止）、ERROR（出错）
- `summary`：已完成工作的总结
- `prUrl`：创建的 Pull Request 的 URL（如果有的话）

### 获取对话记录

```bash
cursor-api.sh conversation <agent-id>
```

返回完整的消息历史记录，包括所有提示和响应。

### 发送后续指令

```bash
cursor-api.sh followup <agent-id> --prompt "Additional instructions"
```

恢复已停止或完成的代理，并发送新的指令。

### 停止代理

```bash
cursor-api.sh stop <agent-id>
```

优雅地停止正在运行的代理。

### 删除代理

```bash
cursor-api.sh delete <agent-id>
```

永久删除代理及其对话记录。

### 列出可用模型

```bash
cursor-api.sh models
```

返回可用于代理任务的模型列表。

### 账户信息

```bash
cursor-api.sh me
```

返回账户信息，包括订阅等级。

### 验证仓库

```bash
cursor-api.sh verify owner/repo
```

检查指定的仓库是否可以被 Cursor 代理访问。

如果仓库无法访问，退出代码为 4。

### 使用情况/成本跟踪

```bash
cursor-api.sh usage
```

返回使用情况信息，包括：
- 使用的代理数量与限制
- 计算资源消耗
- 订阅等级

### 清除缓存

```bash
cursor-api.sh clear-cache
```

清除响应缓存。

### 后台任务命令

```bash
cursor-api.sh bg-list [--all]
```
列出所有后台任务。默认情况下，排除已完成的任务。使用 `--all` 可以包含已完成的任务。

```bash
cursor-api.sh bg-status <task-id>
```
获取后台任务的详细状态，包括当前代理的状态。

```bash
cursor-api.sh bg-logs <task-id>
```
显示后台任务的日志。日志包括状态变化和生成的 Pull Request URL。

## 速率限制

该技能在本地实施每秒 1 次请求的速率限制，以避免 API 速率限制。此限制会自动应用于所有 API 调用。

如果您达到了 Cursor 的 API 速率限制（HTTP 429），脚本将以代码 3 退出。

## 缓存

GET 请求（`list`、`status`、`conversation`、`models`、`me`）默认会缓存 60 秒。要禁用缓存，请执行以下操作：

```bash
cursor-api.sh --no-cache status agent_123
```

要更改缓存过期时间，请设置环境变量：

```bash
export CURSOR_CACHE_TTL=120  # 2 minutes
cursor-api.sh status agent_123
```

## 退出代码

| 代码 | 含义 |
|------|---------|
| 0 | 成功 |
| 1 | API 错误（包括资源不存在） |
| 2 | 身份验证失败或无效 |
| 3 | 达到速率限制 |
| 4 | 仓库无法访问 |
| 5 | 参数无效 |

## 测试

该技能包含一个全面的测试套件（`cca-comprehensive-test.sh`），用于验证以下内容：
- **身份验证**：自动发现、密钥缺失、密钥无效的处理
- **账户相关命令**：`me`、使用情况、模型
- **代理生命周期**：列出代理、启动（是否使用模型）、状态、对话记录、发送后续指令、停止代理
- **错误处理**：格式错误、参数缺失、代理不存在（所有情况都会返回正确的退出代码）

所有测试都会以正确的退出代码通过。错误情况会被正确处理并返回相应的退出代码。

## 并发代理限制

根据现有文档和 API 行为，Cursor Cloud Agents 有以下限制：

| 订阅等级 | 并发代理数量 | 备注 |
|------|-------------------|-------|
| 免费 | 1 | 仅限基本模型 |
| 专业版 | 3 | 可访问大多数模型 |
| 超级版 | 5 | 可访问所有模型，并具有优先处理权 |

这些限制在账户级别对所有代理生效。如果超出限制，API 会返回 HTTP 429 和代码 `CONCURRENT_LIMIT`。

**查看当前使用情况：**
```bash
cursor-api.sh usage | jq '.usage.agentsUsed, .limits.concurrentAgents'
```

**最佳实践：**
1. 当不再需要时，停止已完成的代理
2. 使用 `cursor-api.sh list` 命令监控活跃代理
3. 将任务分批处理，使用较少但规模较大的代理，而不是大量小型代理

> **注意：** 并发代理数量可能会更改。请查看 `cursor-api.sh usage` 以获取您当前账户的限额。

## 最佳实践

### 1. 始终验证仓库访问权限

在启动代理之前，先验证仓库是否可访问：

```bash
if cursor-api.sh verify owner/repo >/dev/null 2>&1; then
    cursor-api.sh launch --repo owner/repo --prompt "..."
else
    echo "Repository not accessible. Install the Cursor GitHub App."
fi
```

### 2. 使用清晰、具体的指令

示例指令：
> “为 `src/auth/` 目录下的认证模块添加全面的单元测试，涵盖登录、登出和令牌刷新功能。使用 Jest 并模拟外部 API 调用。”

示例错误指令：
> “添加一些测试”

### 3. 启动前检查使用情况

在启动代理之前，先检查您的使用量：

```bash
cursor-api.sh usage | jq '.usage'
```

### 4. 清理不再需要的代理

删除不再需要的代理：

```bash
cursor-api.sh list | jq -r '.[] | select(.status == "FINISHED") | .id' | while read id; do
    cursor-api.sh delete "$id"
done
```

### 5. 为后台任务设置合适的最大运行时间

典型任务持续时间：
- 快速修复（拼写错误、小错误）：5-15 分钟 → `--max-runtime 900`
- 功能实现：30-60 分钟 → `--max-runtime 3600`
- 大规模重构：2-6 小时 → `--max-runtime 21600`
- 复杂迁移：6-24 小时 → `--max-runtime 86400`（默认值）

```bash
# Check remaining time
 cursor-api.sh bg-status <task-id> | jq '.remaining_seconds'

# Set custom max runtime
 cursor-api.sh launch --repo owner/repo --prompt "Migrate database schema" --background --max-runtime 43200  # 12 hours
```

### 5. 优雅地处理错误

始终检查脚本中的退出代码：

```bash
if ! response=$(cursor-api.sh launch --repo owner/repo --prompt "..." 2>&1); then
    case $? in
        2) echo "Authentication error - check CURSOR_API_KEY" ;;
        3) echo "Rate limited - try again later" ;;
        4) echo "Repository not accessible" ;;
        *) echo "API error: $response" ;;
    esac
fi
```

## 后续操作模板

使用以下模板处理常见的后续操作场景：

### “添加更多测试”
```
Also add tests for edge cases: empty input, null values, and maximum length limits.
```

### “修复实现”
```
The current implementation doesn't handle [specific case]. Please update it to [requirement].
```

### “添加文档”
```
Add comprehensive JSDoc comments to all public functions and a brief README section explaining the feature.
```

### “为了清晰度进行重构”
```
Refactor the code to use more descriptive variable names and extract complex logic into helper functions.
```

## 配置 CLI 后端

对于本地任务（非 GitHub 仓库），还需配置 Cursor Agent CLI 作为 `cliBackend`：

```json5
// In your OpenClaw config
{
  "cliBackends": {
    "cursor-agent": {
      "command": "agent",
      "args": ["-p", "--force", "--output-format", "text"],
      "output": "text",
      "input": "arg",
      "env": {
        "CURSOR_API_KEY": "${CURSOR_API_KEY}"
      }
    }
  }
}
```

这样 `cursor-agent` 可以作为本地文件操作的的后端，而此技能则负责处理 GitHub 仓库的云代理。

## 故障排除

### “仓库无法访问”（退出代码 4）

1. 确保仓库上安装了 Cursor GitHub 应用
2. 检查您是否具有仓库的管理员/写入权限
3. 验证仓库名称是否正确（格式为 `owner/repo`）

### “身份验证失败”（退出代码 2）

1. 检查环境变量中是否设置了 `CURSOR_API_KEY`
2. 验证 API 密钥在 Cursor IDE 设置中是否有效
3. 确保密钥未过期

### “达到速率限制”（退出代码 3）

1. 等几秒钟后重试
2. 使用 `cursor-api.sh usage` 命令检查使用情况
3. 考虑停止未使用的代理

### 代理处于 “CREATING” 状态

代理可能需要 1-2 分钟才能启动。如果长时间处于该状态：
1. 查看 Cursor 的状态页面以确认是否存在故障
2. 尝试停止并重新启动代理
3. 如果问题持续存在，请联系 Cursor 客服