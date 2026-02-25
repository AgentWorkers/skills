---
name: convex-backend
version: 1.0.1
description: 将密钥、内存数据以及每日日志存储在 Convex 后端中，而不是本地文件中。
author: LaunchThatBot
requires:
  mcp: convex
---
# 凸形后端集成（Convex Backend Integration）

您通过 Convex MCP 服务器连接到 **凸形后端**（Convex backend）。这为您提供了持久性的云存储服务，该存储服务能够在容器重启后仍然保持数据，并且可以通过 LaunchThatBot 仪表板进行访问。

## MCP 要求（使用标准的 Convex MCP）

此技能使用标准的 Convex MCP 服务器（`convex@latest mcp start`），而不是自定义的 LaunchThatBot MCP 工具来进行数据存储。

**推荐设置：**

```json
{
  "mcpServers": {
    "convex": {
      "command": "npx",
      "args": ["-y", "convex@latest", "mcp", "start"]
    }
  }
}
```

**参考文档：** https://docs.convex.dev/ai/convex-mcp-server

## 使用 `mcporter` 的兼容性检查

如果您的运行时环境没有原生支持 MCP 工具（在 OpenClaw/Pi 流程中较为常见），请使用 `mcporter` 作为中间件。

在运行此技能流程之前，请检查以下前提条件：

```bash
mcporter --version || npx -y mcporter --version
mcporter list || npx -y mcporter list
mcporter list convex --schema || npx -y mcporter list convex --schema
```

如果 `mcporter` 无法运行，请告知用户他们需要安装 `npx mcporter`。如果缺少 `convex` MCP，请让用户配置标准的 Convex MCP，然后再重新运行检查。

**通过 `mcporter` 作为中间件时，请注意：** 使用 CLI 命令来调用 Convex MCP 工具（例如 `npx -y mcporter call convex.run ...`），而不是依赖运行时环境中的原生 MCP 工具。

## 重要规则

1. **`CONVEX_DEPLOY_KEY` 是 `.env` 文件中唯一允许的密钥**。请将其保留在本地环境中，因为 Convex MCP 的启动过程依赖于这个密钥。
2. **切勿将 `CONVEX_DEPLOY_KEY` 存储在 Convex 的 `envSet` 中**。
3. **所有其他敏感信息（API 密钥、令牌、密码）必须使用 Convex 的环境变量（`envSet`/`envGet`/`envList`/`envRemove`）进行管理，而不能使用本地 `.env` 文件或 `auth.json` 文件。
4. **切勿将敏感信息存储在 `MEMORY.md` 文件或每日日志文件中**。
5. **每次会话结束时，或根据需要保存进度时，务必将每日总结信息写入 Convex**。
6. **在要求用户再次提供敏感信息之前，务必先在 Convex 中检查这些信息是否存在**。

## 启动规则（必填）

在 Convex MCP 操作开始之前，`CONVEX_DEPLOY_KEY` 必须已经存在于本地运行时的环境变量（`.env` 或部署环境变量）中。

如果 `CONVEX_DEPLOY_KEY` 不存在：
- 停止所有与敏感信息相关的操作。
- 详细告知用户缺少的是什么。
- 要求用户在本地设置 `CONVEX_DEPLOY_KEY`，然后重新启动或重新加载 MCP。
- 重新运行兼容性检查：

```bash
mcporter list convex --schema || npx -y mcporter list convex --schema
```

**注意：** **切勿尝试将 `CONVEX_DEPLOY_KEY` 保存到 Convex 中**。

## 必需的 Convex 部署步骤

此技能包包含一个位于 `convex/` 目录下的 Convex 应用程序，以及位于包根目录下的 `convex.json` 文件。所需的后端逻辑被作为本地组件进行部署：
- 组件名称：`convex_openclaw_backend_component`
- 应用程序挂载别名：`openclawBackend`

安装或更新此技能后，请从技能根目录执行部署操作：

```bash
cd /home/node/.openclaw/skills/convex-backend
CONVEX_DEPLOY_KEY=... npx -y convex@latest deploy
```

**原因：**  
- `npx convex deploy` 命令必须在包含 `convex.json` 的目录中执行。  
- 如果不执行部署操作，自定义的存储/日志功能将不可用，`memory:*` 类型的调用也会失败。

## 添加自定义逻辑的规则

如果用户请求新的后端功能（例如自定义任务表、新的数据变更或查询操作）：
1. 将所需的集成逻辑保存在组件文件中（`convex/components/openclawBackend/*`）。
2. 将用户特定的自定义表或功能放在应用程序的根目录（`convex/*`）中，以确保它们与必要的集成逻辑分开。
3. 每次进行更改后，都需要从技能根目录重新执行部署操作。
4. 在添加自定义逻辑时，**切勿修改或删除** `openclawBackend` 组件。
5. 将 `openclawBackend` 视为核心集成基础设施，而不是用于存储用户特定功能的区域。

如果您修改了 Convex 代码但没有执行部署操作，新添加的功能或表将不会出现在用户的 Convex 部署环境中。

## 管理敏感信息（API 密钥、密码、令牌）

使用 Convex MCP 提供的环境变量工具来管理敏感信息：
- `envSet`
- `envGet`
- `envList`
- `envRemove`

**注意：** **不要在此技能中使用自定义的 `secrets:*` 函数来处理敏感信息。**

### 密钥命名策略（全局共享 + 代理特定）

对于像 `OPENAI_API_KEY` 这样的敏感密钥，按照以下顺序进行查找：
1. `AGENT_<agentId>_OPENAI_API_KEY`（特定代理的覆盖值）
2. `AGENT_DEFAULT_OPENAI_API_KEY`（所有代理共享的默认值）
3. `OPENAI_API_KEY`（旧的全球通用默认值，可选）

**示例：**
- 代理特定值：`AGENT_agent2_OPENAI_API_KEY`
- 全局共享默认值：`AGENT_DEFAULT_OPENAI_API_KEY`

### 设置/读取/删除密钥的值

**设置全局共享默认值：**
```
Tool: envSet
Arguments: { "name": "AGENT_DEFAULT_OPENAI_API_KEY", "value": "sk-..." }
```

**设置代理特定的覆盖值：**
```
Tool: envSet
Arguments: { "name": "AGENT_<agentId>_OPENAI_API_KEY", "value": "sk-..." }
```

**通过备用机制读取密钥值：**
1. `envGet("AGENT_<agentId>_OPENAI_API_KEY")`
2. 如果不存在，尝试 `envGet("AGENT_DEFAULT/OpenAI_API_KEY")`
3. 如果仍然不存在，可以尝试 `envGet("OPENAI_API_KEY")`

**删除代理特定的覆盖值：**
```
Tool: envRemove
Arguments: { "name": "AGENT_<agentId>_OPENAI_API_KEY" }
```

## 对于已有 `.env` 文件的迁移操作

如果此技能被安装在一个已经有很多密钥存在于本地 `.env` 文件中的代理上，请在 Convex MCP 的兼容性检查成功后执行以下迁移操作：

**提示用户：**
> “Convex 后端已经配置完成。您是否希望将所有本地 `.env` 文件中的敏感信息迁移到 Convex 并从本地 `.env` 文件中删除它们？  
> **建议：** 是的。  
> 本地 `.env` 文件中将仅保留 `CONVEX_DEPLOY_KEY`。

如果用户同意迁移：
1. 读取本地 `.env` 文件中的所有密钥/值对。
2. 从列表中排除 `CONVEX_DEPLOY_KEY`。
3. 对于剩余的每个密钥，按照上述命名规则将其迁移到 Convex 环境中：
   - 推荐格式：`AGENT_DEFAULT_<KEY>`
   - 可选代理特定格式：`AGENT_<agentId>_<KEY>`
4. 使用 `envList` 和 `envGet` 验证迁移结果。
5. 从本地 `.env` 文件中删除已迁移的密钥。
6. 仅保留 `CONVEX_DEPLOY_KEY` 在本地 `.env` 文件中。
7. 通过显示迁移后的密钥数量来确认迁移完成。

**安全提示：**
- 在进行任何密钥迁移之前，请先创建 `.env` 文件的本地备份。
- **不要在聊天记录或日志输出中显示敏感信息的实际值**。
- 如果迁移过程中有任何密钥失败，请在尝试重新迁移之前不要从本地 `.env` 文件中删除该密钥。

## 存储长期使用的信息

当您了解到用户的某些重要信息、他们的偏好设置或做出了重要决策时：

```
Function: memory:addMemory
Arguments: {
  "agentId": "<your-agent-id>",
  "type": "fact",
  "content": "User prefers TypeScript over JavaScript for all new projects",
  "tags": ["preferences", "coding"]
}
```

**信息类型：**
- `fact` — 关于用户或其设置的事实性信息
- `preference` — 用户的喜好或厌恶
- `decision` — 已做出的、需要记住的决策
- `note` — 一般的观察结果或背景信息

**如何检索这些信息：**
```
Function: memory:searchMemory
Arguments: { "agentId": "<your-agent-id>", "type": "preference", "limit": 20 }
```

**每日日志记录**

在每次工作会话结束时，记录当天完成的工作内容：

```
Function: memory:writeDailyLog
Arguments: {
  "agentId": "<your-agent-id>",
  "date": "2026-02-17",
  "content": "## Summary\n- Set up email integration with Resend\n- Configured GitHub SSH keys\n- Started work on Twitter bot automation\n\n## Blockers\n- Need Twitter API key from user"
}
```

每日日志文件是只读的——使用 `writeDailyLog` 函数可以为同一日期添加新的日志条目。

**查看过去的日志：**
```
Function: memory:listDailyLogs
Arguments: { "agentId": "<your-agent-id>", "limit": 7 }
```

**会话启动检查清单**

在每次会话开始时：
1. 检查已配置的环境变量：`envList`（以及所需的密钥：`envGet`）
2. 加载最近的信息：使用 `memory:searchMemory`（限制为 20 条记录）
3. 加载当天的日志：使用 `memory:getDailyLog`（指定当天的日期）
4. 加载昨天的日志以保持上下文连贯性

这样可以确保您能够获取之前会话的所有相关信息。

## 您的代理 ID

您的代理 ID 在您的代理配置文件中提供。请在所有与 Convex 的交互中一致地使用该 ID。如果您不确定自己的代理 ID，请查看代理的 YAML 配置文件。