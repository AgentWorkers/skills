---
name: ganglion
description: "适用于涉及该项目的所有任务。内容包括运行 Ganglion、其命令行界面（CLI）命令、HTTP 桥接 API、管道执行、知识查询、配置以及操作工作流程等。相关触发短语包括：`运行管道`（run the pipeline）、`启动服务器`（start the server）、`检查状态`（check status）、`查询知识`（query knowledge）、`进行配置`（configure）、`调用 API`（call the API）、`搭建项目框架`（scaffold a project）、`检查指标`（check metrics）、`回滚操作`（rollback）、`切换策略`（swap policy）。"
homepage: https://github.com/TensorLink-AI/ganglion
metadata: {"openclaw": {"emoji": "📘", "requires": {"bins": ["python3", "ganglion"], "env": ["LLM_PROVIDER_API_KEY"]}, "always": true}}
---
# Ganglion — 操作手册

Ganglion 是一个专为 Bittensor 子网挖掘设计的领域特定执行引擎。它提供了一个管道框架，用于协调自主挖掘代理，以寻找最优的模型配置。Ganglion 提供了命令行界面（CLI）、HTTP 桥接 API 和 Python 库。作为搜索基础设施，Ganglion 本身并不了解什么是好的模型，但它知道如何搜索模型。

## 快速参考

```bash
# Scaffold a new project
ganglion init ./my-subnet --subnet sn9 --netuid 9

# Check state (local mode)
ganglion status ./my-subnet
ganglion tools ./my-subnet
ganglion agents ./my-subnet
ganglion knowledge ./my-subnet --capability training --max-entries 10
ganglion pipeline ./my-subnet

# Run (local mode)
ganglion run ./my-subnet
ganglion run ./my-subnet --stage plan
ganglion run ./my-subnet --overrides '{"target_metric":"accuracy"}'

# Start HTTP bridge (remote mode)
ganglion serve ./my-subnet --bot-id alpha --port 8899

# Check state (remote mode)
curl -s "$GANGLION_URL/v1/status" | jq .data
```

## 模式检测

Ganglion 支持两种模式。**在运行命令之前，请务必检查当前适用的模式。**

- **本地模式**：未设置 `GANGLION_URL`，或设置了 `GANGLION_PROJECT`。直接使用 `ganglion <command> <project_dir>`。
- **远程模式**：设置了 `GANGLION_URL`。通过 HTTP 桥接使用 `curl` 命令进行操作。

```bash
if [ -n "$GANGLION_PROJECT" ] || [ -z "$GANGLION_URL" ]; then
  echo "local"
else
  echo "remote"
fi
```

## 响应格式

所有 HTTP 桥接端点（健康检查除外）都会以标准格式返回响应：

- **成功**：`{"data": <payload>}` — 可使用 `jq .data` 提取数据
- **错误**：`{"detail": {"error": {"code": "ERROR_CODE", "message": "..."}}`

健康检查端点（`/healthz`, `/readyz`）返回不带格式化的原始 JSON 数据。

交互式 API 文档：`$GANGLION_URL/v1/docs`（Swagger UI）。

> **注意：** 未版本化的路由（例如 `/status`）仍然可用，但已被弃用。请始终使用 `/v1/`。

## 如何运行

**先决条件：** Python >= 3.11，且已设置 `LLM_PROVIDER_API_KEY`（由 LLM 运行时使用）。

**安装：** `pip install ganglion`

**创建项目结构：**
```bash
ganglion init ./my-subnet --subnet sn9 --netuid 9
```
此操作会在目标目录下创建 `config.py`、`tools/`、`agents/` 和 `skill/` 文件夹。

**在本地模式下运行：**
```bash
export GANGLION_PROJECT=./my-subnet
ganglion status $GANGLION_PROJECT
```

**在远程模式下运行：**
```bash
ganglion serve ./my-subnet --bot-id alpha --port 8899
export GANGLION_URL=http://127.0.0.1:8899
```

项目目录中必须包含一个 `config.py` 文件，其中定义了 `subnet_config`（子网配置）和 `pipeline`（管道配置）。详细配置信息请参阅 `{baseDir}/references/configuration.md`。

## 主要功能

### 查看状态
查询当前框架的状态——已注册的工具、代理、管道定义、知识库、指标和运行历史记录。本地模式使用 CLI 命令；远程模式使用 GET 请求。

完整参考： `{baseDir}/references/commands.md`

### 执行管道
可以运行整个管道或单个阶段。协调器会按依赖顺序执行各个阶段，应用重试策略，并将累积的知识注入代理提示中，同时记录结果。

```bash
# Local
ganglion run ./my-subnet
ganglion run ./my-subnet --stage plan

# Remote
curl -s -X POST "$GANGLION_URL/v1/run/pipeline" -H "Content-Type: application/json" -d '{}' | jq .data
curl -s -X POST "$GANGLION_URL/v1/run/stage/plan" -H "Content-Type: application/json" -d '{}' | jq .data
```

### 运行时修改（仅限远程模式）
可以注册新的工具、代理和组件；修改管道配置；更换重试策略；更新提示内容。所有修改都会经过验证、审计，并且可以撤销。

```bash
# Register a tool
curl -s -X POST "$GANGLION_URL/v1/tools" -H "Content-Type: application/json" \
  -d '{"name":"my_tool","code":"<code>","category":"training"}' | jq .data

# Patch pipeline
curl -s -X PATCH "$GANGLION_URL/v1/pipeline" -H "Content-Type: application/json" \
  -d '{"operations":[{"op":"add_stage","stage":{"name":"validate","agent":"Validator","depends_on":["train"]}}]}' | jq .data
```

### 管道操作：`add_stage`、`remove_stage`、`update_stage`。详细操作请参阅 `{baseDir}/references/commands.md`。

### 知识库
这是一个跨运行的策略记忆系统，会随着时间的推移不断积累数据。它记录成功的模式和失败的模式，然后自动将相关历史信息注入代理提示中。知识库可以通过功能进行查询，并根据 `bot_id` 进行过滤（适用于多机器人设置）。

```bash
# Local
ganglion knowledge ./my-subnet --bot-id alpha --capability training

# Remote
curl -s "$GANGLION_URL/v1/knowledge?capability=training&max_entries=10" | jq
```

### 回滚
可以撤销任何修改操作。所有修改都会被记录在审计日志中，并附带回滚数据。

```bash
curl -s -X POST "$GANGLION_URL/v1/rollback/last" | jq
curl -s -X POST "$GANGLION_URL/v1/rollback/0" | jq    # undo ALL mutations
```

### 多机器人工作流程
多个 OpenClaw 会话可以通过 `--bot-id` 共享知识库。每个机器人的发现结果都会被纳入共享池中。协作是通过共享知识实现的，而非显式的协调。

```bash
# Two local sessions
ganglion run ./my-subnet --bot-id alpha
ganglion run ./my-subnet --bot-id beta

# Two remote servers
ganglion serve ./my-subnet --bot-id alpha --port 8899
ganglion serve ./my-subnet --bot-id beta  --port 8900
```

### MCP 集成
Ganglion 是一个双向的 MCP（模型配置中心）系统：它既可以**消费**外部 MCP 服务器的数据（客户端模式），也可以**作为 MCP 服务器**提供自己的工具（服务器模式）。

#### MCP 客户端模式 — 消费外部工具
连接到外部 MCP 服务器，将工具添加到代理的可用工具列表中。来自 MCP 服务器的工具会以可配置的前缀显示为常规的 Ganglion 工具。

```bash
# Static: add to config.py
# from ganglion.mcp.config import MCPClientConfig
# mcp_clients = [MCPClientConfig(name="weather", transport="stdio", command=["python", "-m", "weather_server"])]

# Dynamic: add at runtime via API
curl -s -X POST "$GANGLION_URL/v1/mcp/servers" -H "Content-Type: application/json" \
  -d '{"name":"weather","transport":"stdio","command":["python","-m","weather_server"]}' | jq .data

# Check connected MCP servers
curl -s "$GANGLION_URL/v1/mcp" | jq .data

# Disconnect / Reconnect
curl -s -X DELETE "$GANGLION_URL/v1/mcp/servers/weather" | jq .data
curl -s -X POST "$GANGLION_URL/v1/mcp/servers/weather/reconnect" | jq .data
```

MCPClientConfig 参数：`name`、`transport`（stdio|sse）、`command`（适用于 stdio）、`url`（适用于 sse）、`env`、`tool_prefix`、`category`、`timeout`（默认 30 秒）。

#### MCP 服务器模式 — 提供 Ganglion 工具
将 Ganglion 作为 MCP 服务器运行，以便外部代理（如 Claude Code、Claude Desktop、OpenClaw）可以直接调用 Ganglion 的工具。

```bash
# stdio transport (Claude Desktop / Claude Code)
ganglion mcp-serve ./my-subnet --transport stdio

# SSE transport (HTTP-based clients)
ganglion mcp-serve ./my-subnet --transport sse --mcp-port 8900

# Multi-role with access control
ganglion mcp-serve ./my-subnet --roles ./roles.json
```

**Claude Code 集成：** 该仓库包含 `.mcp.json` 文件，可自动配置 Claude Code 通过 stdio 连接到 Ganglion 的 MCP 服务器。Claude Code 可以在其工具面板中直接使用所有 Ganglion 工具。

#### 提供的 MCP 工具（共 31 个）

**观察（11 个）** — 仅读操作：
`ganglion_get_status`、`ganglion_get_pipeline`、`ganglion_get_tools`、`ganglion_getAgents`、`ganglion_get_runs`、`ganglion_get_metrics`、`ganglion_get_leaderboard`、`ganglion_get_knowledge`、`ganglion_get_source`、`ganglion_get_components`、`ganglion_get_mcp_status`

**修改（6 个）** — 写入操作：
`ganglion_write_tool`、`ganglion_write_agent`、`ganglion_write_component`、`ganglion_write_prompt`、`ganglion_patch_pipeline`、`ganglion_swap_policy`

**执行（3 个）** — 运行操作：
`ganglion_run_pipeline`、`ganglion_run_stage`、`ganglion_run_experiment`

**管理（5 个）** — 回滚和管理 MCP：
`ganglion_rollback_last`、`ganglion_rollback_to`、`ganglion_connect_mcp`、`gangliondisconnect_mcp`、`ganglion_reconnect_mcp`

**计算（6 个）** — 基础设施操作：
`compute_status`、`compute_jobs`、`compute_job_detail`、`compute_routes`、`write_dockerfile`、`build_image`

#### 多角色 MCP 服务
可以运行多个进程，每个进程都运行不同的 MCP 服务器实例，每个实例具有不同的访问权限和认证令牌。

```json
// roles.json
[
  {"name": "admin",    "categories": null,                        "token": "admin-xyz",    "port": 8901},
  {"name": "worker",   "categories": ["observation","execution"], "token": "worker-abc",   "port": 8902},
  {"name": "observer", "categories": ["observation"],             "token": "observer-def", "port": 8903}
]
```

角色可以根据类别过滤工具。`null` 类别表示可以访问所有工具。每个角色都会获得一个单独的端口和用于 SSE 传输的令牌。最多只有一个角色可以使用 stdio 传输方式。

#### 每个机器人的使用情况跟踪
当使用 `--roles` 参数运行时，一个共享的 `UsageTracker` 会记录每个机器人的工具调用情况（工具名称、成功/失败、时间戳、持续时间），并将这些数据保存到 `.ganglion/usage.db` 文件中。可以通过 `/usage` 端点查询这些数据。

#### 将其他代理连接到 Ganglion 的 MCP 服务器
OpenClaw 和其他 LLM 代理可以启动自己的 MCP 服务器，或者让其他代理连接到该服务器。对于不支持 stdio 的通用 MCP 客户端，可以使用 SSE 传输方式。

```bash
# Start Ganglion MCP server with SSE transport (any MCP client can connect)
ganglion mcp-serve ./my-subnet --transport sse --mcp-port 8900

# SSE endpoints exposed:
#   GET  http://127.0.0.1:8900/sse         — SSE stream (tool list + results)
#   POST http://127.0.0.1:8900/messages     — send tool calls
#   GET  http://127.0.0.1:8900/usage        — usage stats (if tracking enabled)
#   GET  http://127.0.0.1:8900/usage?bot_id=alpha — per-bot stats

# With auth (multi-role), include bearer token:
#   curl -H "Authorization: Bearer worker-abc" http://127.0.0.1:8902/sse
```

**对于 OpenClaw：** OpenClaw 通过 bash/curl 读取技能信息并执行命令——它不会直接连接到 MCP。要让 OpenClaw 访问 Ganglion 的工具，可以使用上述文档中描述的 CLI（本地模式）或 HTTP 桥接（远程模式）。OpenClaw 也可以启动自己的 MCP 服务器，以便其他支持 MCP 功能的代理（如 Claude Desktop、Cursor 等）能够连接到它。

```bash
# OpenClaw starts the MCP server for other agents
ganglion mcp-serve ./my-subnet --transport sse --mcp-port 8900
```

**对于通用 MCP 客户端（如 Cursor、Windsurf、自定义客户端）：** 将客户端的 MCP 配置指向 SSE 端点：
- 服务器地址：`http://127.0.0.1:8900/sse`
- 消息端点：`http://127.0.0.1:8900/messages`
- 传输方式：SSE
- 认证：使用 bearer 令牌（如果使用多角色功能）

## 常见工作流程

详细步骤指南请参阅 `{baseDir}/examples/common-workflows.md`：

1. **首次运行**：`ganglion init` → 编辑 `config.py` → `ganglion run`
2. **迭代挖掘**：检查状态 → 查看知识库 → 运行管道 → 检查指标 → 重复上述步骤
3. **动态修改**：观察工具/代理的状态 → 通过 API 注册新工具 → 修改管道配置 → 运行
4. **多机器人设置**：在同一项目中使用不同的 `--bot-id` 值启动多个服务器
5. **MCP 集成**：连接外部工具服务器 → 工具会显示在代理的可用工具列表中 → 代理可以使用这些工具

## 出现问题时

| 症状 | 可能原因 | 解决方法 |
|---------|-------------|-----|
| `FileNotFoundError: No config.py` | 项目路径错误 | 确保路径中包含 `config.py` 文件 |
| `LLM_PROVIDER_API_KEY` 错误 | API 密钥缺失或无效 | 设置 `export LLM_PROVIDER_API_KEY=sk-...` |
| `ConcurrentMutationError` | 在管道运行过程中进行修改 | 等待管道运行完成 |
| `PipelineValidationError` | 管道配置错误（存在循环或依赖关系缺失） | 检查 `ganglion pipeline` 的输出 |
| 代理卡住 / 达到最大尝试次数 | 代理无法继续运行 | 查看知识库，更换重试策略，调整提示内容 |

完整故障排除指南： `{baseDir}/references/troubleshooting.md`

## 重试策略

内置了四种重试策略来控制失败时的处理方式：
- **NoRetry** — 只尝试一次
- **FixedRetry** — 重试 N 次（默认值：3 次）
- **EscalatingRetry** — 每次尝试时增加重试次数，可选地检测是否出现停滞
- **ModelEscalationRetry** — 逐步提高模型使用的成本（从低成本模型开始）

提供了三种预设策略：`SN50_PRESET`（包含重试和停滞检测）、`SIMPLE_PRESET`（固定重试次数）、`AGGRESSIVE_PRESET`（逐步增加模型成本）

## 其他资源

- 完整的 CLI 和 API 参考文档： `{baseDir}/references/commands.md`
- 配置指南： `{baseDir}/references/configuration.md`
- 操作流程： `{baseDir}/references/operations.md`
- 故障排除指南： `{baseDir}/references/troubleshooting.md`
- 工作流程示例： `{baseDir}/examples/common-workflows.md`
- 示例 API 请求： `{baseDir}/examples/sample-requests.md`
- 健康检查脚本： `{baseDir}/scripts/healthcheck.sh`