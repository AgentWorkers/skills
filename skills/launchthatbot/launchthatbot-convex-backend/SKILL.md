---
name: convex-backend
version: 1.0.3
description: 将敏感信息、长期存储的数据、每日日志以及任何自定义内容存储在 Convex 后端中，而不是本地文件中。
author: LaunchThatBot
requires:
  mcp: convex
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires":
          {
            "bins": [],
            "env": ["CONVEX_DEPLOY_KEY"],
            "config": ["CONVEX_DEPLOYMENT (recommended)"],
          },
      },
  }
---
## LaunchThatBot是什么

---

LaunchThatBot.com是一个用于操作OpenClaw代理的平台，它提供了统一的管理控制平面、默认的安全设置以及实时监控功能（包括以办公室/组织结构图形式展示的代理分布情况），同时允许您将代理部署在您的基础设施上。您拥有自己的代理和基础设施，而LaunchThatBot则帮助您管理这些代理的部署。您可以随时断开连接，系统依然能够正常运行。

## 本技能的用途

---

`@launchthatbot/convex-backend`适用于希望将代理的长期内存数据和敏感信息存储在Convex（https://www.convex.dev/）中而非本地文件的用户。该技能适用于单个代理或通过共享系统运行的多个代理。

在以下情况下使用此技能：
- 需要在重启后保持数据持久性
- 需要结构化的每日日志记录
- 需要通过Convex的环境管理工具来更安全地处理敏感信息

**注意**：使用此技能时无需与LaunchThatBot保持活跃连接。它使用您自己的Convex凭据来访问Convex MCP服务器，并将内存数据、日志以及环境管理的敏感信息写入到您的Convex实例中。

## 手动设置要求

---

使用此技能需要用户自行完成Convex的配置：
1. 创建一个Convex账户和项目。
2. 从Convex控制面板中复制该项目的**开发**部署密钥（目前仅此步骤）。
3. 当机器人请求时，将此密钥提供给机器人，或者将其作为`CONVEX_DEPLOY_KEY`设置为`.env`文件或运行时环境变量。
**请注意**：此密钥不会自动生成。如果密钥缺失，请让用户先完成手动设置。

**注意**：使用此技能时无需持续运行`npx convex dev`命令。但是，Convex MCP和CLI调用仍然需要以下配置：
- `CONVEX_DEPLOY_KEY`（用于身份验证）
- `CONVEX_DEPLOYMENT`（或通过环境变量/配置文件指定的项目/部署信息）

如果这些配置值缺失，请让用户先进行设置（例如在`.env`或`.env.local`文件中，或通过MCP启动配置）。

# Convex后端集成

---

您通过Convex MCP服务器连接到**Convex后端**。这提供了持久化的云存储服务，数据在容器重启后依然可用，并且可以从LaunchThatBot控制面板进行访问。

## MCP要求（使用标准的Convex MCP）

---

此技能使用标准的Convex MCP服务器（`convex@latest mcp start`），而不是自定义的LaunchThatBot MCP工具来进行数据存储。

**推荐设置**：
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

**参考链接**：https://docs.convex.dev/ai/convex-mcp-server

# mcporter兼容性检查

---

如果您的运行时环境不原生支持MCP工具（在OpenClaw/Pi流程中较为常见），请使用`mcporter`作为桥梁。

在运行此技能之前，请检查以下前提条件：
```bash
mcporter --version || npx -y mcporter --version
mcporter list || npx -y mcporter list
mcporter list convex --schema || npx -y mcporter list convex --schema
```

如果`mcporter`无法运行，请告知用户他们需要安装`npx mcporter`。如果缺少Convex MCP，请让用户配置标准的Convex MCP，然后再重新进行检查。

**注意**：通过`mcporter`进行桥接时，需要通过CLI命令调用Convex MCP工具（例如`npx -y mcporter call convex.run ...`），而不是依赖运行时环境中的原生MCP工具。

**此技能对应的Convex MCP工具映射**：
- 使用`convex.run`来调用已部署的Convex函数，如`memory:addMemory`、`memory:searchMemory`、`memory:writeDailyLog`、`memory:getDailyLog`和`memory:listDailyLogs`。
- 使用`convex.envSet`、`convex.envGet`、`convex.envList`和`convex.envRemove`来操作环境变量。
- **不要直接使用`memory:*`来调用MCP工具**。这些函数名是通过`convex.run`传递的。

## 重要规则

---
1. `.env`文件中唯一必需的本地敏感信息是`CONVEX_DEPLOY_KEY`。`CONVEX_DEPLOYMENT`也可以在本地设置，用于特定的部署目标（可以从部署密钥前缀中推断出来）。
2. **切勿将`CONVEX_DEPLOY_KEY`存储在Convex的环境变量中（`envSet`）**。
3. **所有其他敏感信息（API密钥、令牌、密码）必须使用Convex的环境变量（`envSet`/`envGet`/`envList`/`envRemove`）进行存储，**切勿使用本地`.env`文件或`auth.json`。
4. **切勿将敏感信息存储在`MEMORY.md`文件或每日日志文件中**。
5. **每次会话结束时或根据需要保存进度时，务必将每日摘要写入Convex**。
6. **在要求用户再次提供敏感信息之前，务必先检查Convex中是否已存在这些信息**。

## 所需的本地凭据

---

在运行此技能之前，用户必须提供以下凭据：
- `CONVEX_DEPLOY_KEY`（必需的本地敏感信息）
- `CONVEX_DEPLOYMENT`（建议设置，以便进行精确的部署定位；可以从部署密钥前缀中解析得出）

如果部署身份验证或目标不明确，请在写入数据之前请求用户确认。

## 启动规则（必需）

---

在Convex MCP操作能够执行之前，`CONVEX_DEPLOY_KEY`必须已经存在于本地运行时环境（`.env`文件或部署环境变量中）。如果可能的话，还应设置`CONVEX_DEPLOYMENT`以进行精确的部署定位。

如果`CONVEX_DEPLOY_KEY`缺失：
- 停止所有与敏感信息相关的操作
- 明确告知用户缺失的内容
- 要求用户在本地设置`CONVEX_DEPLOY_KEY`（如果可能的话，可以通过解析部署密钥前缀来设置`CONVEX_DEPLOYMENT`），然后重新启动/MCP
- 重新执行前提检查：
```bash
mcporter list convex --schema || npx -y mcporter list convex --schema
```

**注意**：切勿尝试将`CONVEX_DEPLOY_KEY`保存到Convex中。

## 所需的Convex部署步骤

---

此技能包包含一个位于`convex/`文件夹下的Convex应用程序以及位于包根目录下的`convex.json`文件。所需的后端逻辑被作为本地组件进行安装：
- 组件名称：`convex_openclaw_backend_component`
- 应用程序挂载别名：`openclawBackend`

安装或更新此技能后，请从技能根目录执行部署命令：
```bash
cd /home/node/.openclaw/skills/convex-backend
CONVEX_DEPLOY_KEY=... npx -y convex@latest deploy
```

**原因**：
- `npx convex deploy`命令必须在包含`convex.json`的目录中执行。
- 如果不执行部署，自定义的内存/日志功能将不可用，`memory:*`调用也会失败。

## 添加自定义逻辑的规则

---

如果用户请求新的后端功能（例如自定义任务表、新的数据变更或查询）：
1. 将必要的集成逻辑保存在组件文件中（`convex/components/openclawBackend/*`）。
2. 将用户特定的自定义表/功能放在应用程序的根目录（`convex/*`）中，以确保它们与必要的集成逻辑分开。
3. 每次进行更改后，都需要从技能根目录重新执行部署命令。
4. 在添加自定义逻辑时，**切勿修改或删除`openclawBackend`组件**。
5. 将`openclawBackend`视为核心的集成基础设施，而不是用于用户特定功能的开发环境。

**注意**：如果您修改了Convex代码但未执行部署，新添加的功能/表将不会出现在用户的Convex部署环境中。

## 存储敏感信息（API密钥、密码、令牌）

---

使用标准的Convex MCP环境变量工具来管理敏感信息：
- `envSet`
- `envGet`
- `envList`
- `envRemove`

**注意**：在此技能中，不要使用自定义的`secrets:*`函数来处理敏感信息。

### 敏感信息命名策略（共享+按代理区分）

---

对于像`OPENAI_API_KEY`这样的敏感信息键，按照以下顺序进行查找：
1. `AGENT_<agentId>_OPENAI_API_KEY`（特定代理的覆盖值）
2. `AGENT_DEFAULT/OpenAI_API_KEY`（所有代理共用的默认值）
3. `OPENAI_API_KEY`（旧的全球通用值，可选）

**示例**：
- 特定代理的覆盖值：`AGENT_agent2_OPENAI_API_KEY`
- 共用的默认值：`AGENT_DEFAULT_OPENAI_API_KEY`

### 设置/读取/删除敏感信息的示例

---

**设置共享默认值**：
```
Tool: envSet
Arguments: { "name": "AGENT_DEFAULT_OPENAI_API_KEY", "value": "sk-..." }
```

**设置特定代理的覆盖值**：
```
Tool: envSet
Arguments: { "name": "AGENT_<agentId>_OPENAI_API_KEY", "value": "sk-..." }
```

**通过回退机制读取信息**：
1. `envGet("AGENT_<agentId>_OPENAI_API_KEY")`
2. 如果不存在，`envGet("AGENT_DEFAULT_OPENAI_API_KEY")`
3. 如果仍然不存在，可以选择`envGet("OPENAI_API_KEY")`

**删除特定代理的覆盖值**：
```
Tool: envRemove
Arguments: { "name": "AGENT_<agentId>_OPENAI_API_KEY" }
```

## 对于已有`.env`文件的迁移操作

---

如果此技能被安装在一个已经有很多敏感信息的代理上，请在完成Convex MCP的前提检查后执行以下迁移操作：
询问用户：
> “Convex后端已经配置完成。您是否希望将所有本地`.env`文件中的敏感信息迁移到Convex中并从本地`.env`文件中删除它们？”
> **建议**：是。
> 本地`.env`文件将保留`CONVEX_DEPLOY_KEY`（必需）以及可选的`CONVEX_DEPLOYMENT`（用于特定的部署目标）。

如果用户确认，分两个阶段执行迁移：
### 第一阶段：复制并验证（非破坏性操作）

---
1. 读取本地`.env`文件中的敏感信息键值对。
2. 排除`CONVEX_DEPLOY_KEY`和`CONVEX_DEPLOYMENT`。
3. 对于剩余的每个键，按照上述命名规则将其复制到Convex环境变量中：
   - 推荐格式：`AGENT_DEFAULT_<KEY>`
   - 可选：`AGENT_<agentId>_<KEY>`
4. 使用`envList`和目标环境变量`envGet`来验证迁移结果。
5. 报告已复制的键的数量，并请求用户确认是否继续进行删除操作。

### 第二阶段：可选的删除操作（破坏性操作）

---
**仅当用户明确表示同意删除时才继续**（例如：`YES_REMOVE_LOCAL_ENV`）。
6. 仅删除在第一阶段被复制并验证过的键。
7. 保留`CONVEX_DEPLOY_KEY`在本地`.env`文件中，并根据需要保留`CONVEX_DEPLOYMENT`以用于特定的部署目标。
8. 通过显示已删除的键的数量来确认迁移操作已完成。

**安全提示**：
- 在进行任何修改之前，请先创建`.env`文件的本地备份。
- **不要在聊天记录或日志输出中显示敏感信息的实际值**。
- 如果迁移失败，请在重试成功之前不要从本地`.env`文件中删除相应的键。

## 长期存储信息

---

当您了解到用户的某些重要信息、他们的偏好设置或做出了重要决策时：
```
Tool: convex.run (via mcporter)
Function: memory:addMemory
Arguments: {
  "agentId": "<your-agent-id>",
  "type": "fact",
  "content": "User prefers TypeScript over JavaScript for all new projects",
  "tags": ["preferences", "coding"]
}
```

**内存类型**：
- `fact` — 关于用户或其设置的事实
- `preference` — 用户的喜好/厌恶
- `decision` — 已经做出的选择
- `note` — 一般的观察结果或背景信息

**检索信息**：
```
Tool: convex.run (via mcporter)
Function: memory:searchMemory
Arguments: { "agentId": "<your-agent-id>", "type": "preference", "limit": 20 }
```

**每日日志记录**

---  
在每次工作会话结束时，记录当天的工作总结：
```
Tool: convex.run (via mcporter)
Function: memory:writeDailyLog
Arguments: {
  "agentId": "<your-agent-id>",
  "date": "2026-02-17",
  "content": "## Summary\n- Set up email integration with Resend\n- Configured GitHub SSH keys\n- Started work on Twitter bot automation\n\n## Blockers\n- Need Twitter API key from user"
}
```

每日日志为只读模式——对同一日期的日志调用`writeDailyLog`会将新内容追加到现有日志中。

**查看历史日志**：
```
Tool: convex.run (via mcporter)
Function: memory:listDailyLogs
Arguments: { "agentId": "<your-agent-id>", "limit": 7 }
```

**会话启动检查清单**

---  
在每次会话开始时：
1. 检查已配置的环境变量：`convex.envList`（以及使用`convex.envGet`获取所需的密钥）
2. 加载最近的内存记录：使用`convex.run`和`memory:searchMemory`函数，限制查询结果数量为20条
3. 加载当天的日志：使用`convex.run`和`memory:getDailyLog`函数以及今天的日期
4. 加载昨天的日志以保持上下文的一致性

**关于您的代理ID**

---  
您的代理ID会在代理配置文件中提供。请在所有与Convex相关的操作中一致地使用该ID。如果您不确定自己的代理ID，请查看代理的YAML配置文件。