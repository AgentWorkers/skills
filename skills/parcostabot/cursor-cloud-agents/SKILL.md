---
name: cursor-cloud-agents
description: "将 Cursor AI 代理部署到 GitHub 仓库中。利用您现有的 Cursor 订阅服务，自动编写代码、生成测试用例、创建文档，并提交 Pull Request（PR）。"
---

# Cursor Cloud Agents 技能

## 概述

此技能封装了 Cursor Cloud Agents 的 HTTP API，允许 OpenClaw 向 Cursor 的云代理分发编码任务、监控它们的进度并整合结果。

### 适用场景

在以下情况下使用此技能：
- 将编码任务委托给运行在 GitHub 仓库中的 Cursor 代理
- 在现有代码库上生成代码、测试或文档
- 异步执行重构或功能实现
- 对代码更改获取“第二意见”

### 不适用场景

- 对于不需要代码更改的简单问题
- 需要实时流式响应的情况（请使用本地 Cursor CLI）
- 适用于非 GitHub 仓库的任务

## 认证

该技能会自动从以下位置查找您的 Cursor API 密钥（按顺序）：
1. **环境变量：** `CURSOR_API_KEY`
2. **OpenClaw 环境文件：** `~/.openclaw/.env`
3. **OpenClaw 本地环境：** `~/.openclaw/.env.local`
4. **项目环境变量：** 当前目录下的 `.env` 文件
5. **Cursor 配置文件：** `~/.cursor/config.json`

**建议：** 将 API 密钥添加到 `~/.openclaw/.env` 文件中：
```bash
CURSOR_API_KEY=your_cursor_api_key_here
```

获取 API 密钥的步骤：
1. 打开 Cursor IDE
2. 转到设置 → 通用设置
3. 复制您的 API 密钥

**验证其是否正常工作：**
```bash
cursor-api.sh me
```

## 工作流程模式

### 模式 A：一次性启动后忽略

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

**注意：** 如果未指定 `--model`，系统将自动使用默认模型（`gpt-5.2`）。您会看到一条提示信息显示所使用的模型。

**适用场景：** 不需要立即关注的任务、探索性工作

### 模式 B：监督式调度

启动代理，监控其运行过程，并在完成后报告结果。

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

**适用场景：** 需要报告完成情况的任务

### 模式 C：迭代协作

启动代理，审查结果后发送后续指令以优化工作。

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

**适用场景：** 需要多次迭代的复杂任务

## 命令参考

### 列出代理

```bash
cursor-api.sh list
```

返回所有代理的信息，包括状态、仓库和创建时间。

### 启动代理

```bash
cursor-api.sh launch --repo owner/repo --prompt "Your task description" [--model model-name] [--branch branch-name] [--no-pr]
```

选项：
- `--repo`（必选）：仓库地址（格式为 `owner/repo`）
- `--prompt`（必选）：代理的初始指令
- `--model`（可选）：要使用的模型（未指定时默认为 `gpt-5.2`）
- `--branch`（可选）：目标分支名称（省略时自动生成）
- `--no-pr`（可选）：不自动创建 Pull Request

**注意：** 如果未指定 `--model`，系统将自动使用 `gpt-5.2` 并显示所使用的模型。

### 检查状态

```bash
cursor-api.sh status <agent-id>
```

返回：
- `status`：CREATING（创建中）、RUNNING（运行中）、FINISHED（已完成）、STOPPED（已停止）、ERROR（出错）
- `summary`：已完成工作的总结
- `prUrl`：生成的 Pull Request 的 URL（如有）

### 获取对话记录

```bash
cursor-api.sh conversation <agent-id>
```

返回完整的对话历史记录，包括所有提示和响应。

### 发送后续指令

```bash
cursor-api.sh followup <agent-id> --prompt "Additional instructions"
```

重新启动已停止或已完成的代理，并发送新的指令。

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

返回账户信息，包括订阅层级。

### 验证仓库访问权限

```bash
cursor-api.sh verify owner/repo
```

检查指定的仓库是否可供 Cursor 代理访问。如果仓库无法访问，返回代码 4。

### 使用情况/成本跟踪

```bash
cursor-api.sh usage
```

返回使用情况信息，包括：
- 使用的代理数量与限制
- 计算资源消耗
- 订阅层级

### 清除缓存

```bash
cursor-api.sh clear-cache
```

清除响应缓存。

## 速率限制

该技能在本地实施 **每秒 1 个请求** 的速率限制，以避免违反 API 的速率限制。此限制会自动应用于所有 API 调用。

如果达到 Cursor 的 API 速率限制（HTTP 429），脚本将以代码 3 结束执行。

## 缓存

GET 请求（`list`、`status`、`conversation`、`models`、`me`）默认缓存 60 秒。要禁用某个命令的缓存，请执行以下操作：
```bash
cursor-api.sh --no-cache status agent_123
```

要更改缓存过期时间，请设置环境变量：
```bash
export CURSOR_CACHE_TTL=120  # 2 minutes
cursor-api.sh status agent_123
```

## 错误代码

| 代码 | 含义 |
|------|---------|
| 0 | 成功 |
| 1 | API 错误（包括资源不存在） |
| 2 | 认证信息缺失或无效 |
| 3 | 超出速率限制 |
| 4 | 仓库无法访问 |
| 5 | 参数无效 |

## 测试

该技能包含一个全面的测试套件（`cca-comprehensive-test.sh`），用于验证以下内容：
- **认证**：自动发现密钥、处理密钥缺失或无效的情况
- **账户相关命令**：`me`、`usage`、`models`
- **代理生命周期**：`list`、`launch`（是否使用模型）、`status`、`conversation`、`followup`、`stop`
- **错误处理**：处理无效格式、参数缺失、代理不存在等情况（所有情况都会返回正确的退出代码）

所有测试都会以正确的退出代码通过。错误情况会被正确处理并返回相应的退出代码。

## 并发代理限制

根据现有文档和 API 行为，Cursor Cloud Agents 有以下并发限制：

| 订阅层级 | 并发代理数量 | 备注 |
|------|-------------------|-------|
| 免费 | 1 | 仅限基本模型 |
| 专业版 | 3 | 可访问大多数模型 |
| 超级版 | 5 | 可访问所有模型，并享有优先处理权 |

这些限制在账户级别对所有代理统一适用。如果超出限制，API 会返回代码 429 和错误信息 `CONCURRENT_LIMIT`。

**查看当前使用情况：**
```bash
cursor-api.sh usage | jq '.usage.agentsUsed, .limits.concurrentAgents'
```

**最佳实践：**
1. 当不再需要时停止已完成的代理
2. 使用 `cursor-api.sh list` 监控活跃代理
3. 将任务分批处理，使用较少但规模较大的代理，而不是大量小型代理

> **注意：** 并发限制可能会更改。请查看 `cursor-api.sh usage` 以获取您当前账户的限制。

## 最佳实践

### 1. 始终验证仓库访问权限

在启动代理之前，确保仓库可访问：

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

在启动代理之前，检查您的使用额度：

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

### “重构以提高代码清晰度”
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

这样 `cursor-agent` 可用于处理本地文件操作，而此技能则负责处理 GitHub 仓库的云代理任务。

## 故障排除

### “仓库无法访问”（退出代码 4）

1. 确保仓库已安装 Cursor GitHub 应用
2. 检查您是否具有仓库的管理员/写入权限
3. 验证仓库名称是否正确（格式为 `owner/repo`）

### “认证失败”（退出代码 2）

1. 检查环境变量中是否设置了 `CURSOR_API_KEY`
2. 验证 API 密钥在 Cursor IDE 设置中是否有效
3. 确保密钥未过期

### “超出速率限制”（退出代码 3）

1. 等待几秒钟后重试
2. 使用 `cursor-api.sh usage` 检查使用情况
3. 考虑停止未使用的代理

### 代理处于 “CREATING” 状态且无法启动

代理可能需要 1-2 分钟才能启动。如果长时间无法启动：
1. 查看 Cursor 的状态页面，确认是否存在故障
2. 尝试停止并重新启动代理
3. 如果问题持续存在，请联系 Cursor 客服支持