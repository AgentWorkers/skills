---
name: openfleet
description: "管理您的 OpenFleet 多代理工作空间：创建任务、分配代理、触发脉冲周期、管理自动化流程以及监控代理活动。实现对自主代理团队的完全双向控制。"
homepage: https://openfleet.sh
metadata:
  openclaw:
    emoji: "\u25C7"
    requires:
      bins:
        - npx
      env:
        - OPENFLEET_API_KEY
    primaryEnv: OPENFLEET_API_KEY
---
# OpenFleet

这是一个用于在终端中实现自主多代理协作的工具。您可以通过它创建任务、管理代理、触发工作流程，并实时监控所有操作——而无需离开 OpenClaw。

## 设置

1. 从 [OpenFleet 仪表板](https://app.openfleet.sh) 的“开发者设置”中获取您的 API 密钥。
2. 设置环境变量：
   ```
   export OPENFLEET_API_KEY=ofk_your_key_here
   ```
3. 安装该工具：
   ```
   clawhub install openfleet
   ```

### 快速验证

向您的代理发送命令：“List my OpenFleet tasks”（列出我的 OpenFleet 任务）。

## 提供的 20 种工具

### 任务管理

| 工具 | 功能描述 |
|------|-------------|
| `openfleet_list_tasks` | 列出任务——可按状态、优先级或关键词进行筛选 |
| `openfleet_create_task` | 创建任务（任务会自动分配给最适合执行该任务的代理） |
| `openfleet_get_task` | 通过任务 ID 获取详细信息 |
| `openfleet_update_task` | 更新任务的标题、描述、状态、优先级或标签 |
| `openfleet_delete_task` | 将任务标记为已归档（实际上只是删除该任务的记录） |
| `openfleet_unblock_task` | 解锁被屏蔽的任务，并显示解决该任务所需的上下文信息 |
| `openfleet_approve_task` | 批准处于“待审核”状态的任务，使其变为“已完成”状态 |
| `openfleet_add_comment` | 在任务执行过程中向代理显示评论 |

### 代理管理

| 工具 | 功能描述 |
|------|-------------|
| `openfleet_listAgents` | 列出所有代理的信息，包括状态、健康状况和令牌使用情况 |
| `openfleet_get_agent` | 通过代理 ID 获取详细信息 |
| `openfleet_create_agent` | 创建新的代理（类型包括 LEAD、SPECIALIST 或 INTERN） |

### 自动化任务

| 工具 | 功能描述 |
|------|-------------|
| `openfleet_list_automations` | 列出所有自动化的任务 |
| `openfleet_create_automation` | 创建定时执行的自动化任务（周期从每小时到每月不等） |
| `openfleet_toggle_automation` | 开启或关闭自动化任务 |
| `openfleet_trigger_automation` | 立即触发自动化任务 |

### 系统管理

| 工具 | 功能描述 |
|------|-------------|
| `openfleet_trigger_pulse` | 触发代理的工作流程（包括健康检查、任务分配和执行） |
| `openfleet_get_workspace` | 获取工作空间的信息和配置 |
| `openfleet_parse_input` | 将自然语言输入解析为结构化的任务指令 |
| `openfleet_install_template` | 安装工作空间模板（例如 SaaS 启动流程或内容处理流程） |
| `openfleet_list_activities` | 查看最近的活动记录 |

## 使用示例

### 创建任务
```
Create an OpenFleet task: "Build a landing page with hero section, pricing table, and contact form" with HIGH priority and tags frontend, react
```

### 检查代理状态
```
List my OpenFleet agents and show who is working on what
```

### 触发自动化任务
```
Trigger an OpenFleet pulse to assign queued tasks and start agent work
```

### 管理被屏蔽的任务
```
Show me all BLOCKED tasks in OpenFleet and unblock the one about API keys with the message "Key has been added to environment"
```

### 创建周期性自动化任务
```
Create a daily OpenFleet automation called "Morning standup report" that generates a summary task every morning
```

## MCP 服务器详情

该工具基于 `@open-fleet/mcp-server` npm 包实现，该包提供了一个标准的 MCP 标准输入输出（stdio）服务器。

**手动配置 MCP**（如果不使用 ClawHub）：
```bash
npx @open-fleet/mcp-server setup
```

设置向导会自动检测 Claude Code、Cursor 和 Windsurf，并完成 MCP 的配置。

**直接使用 npx 命令进行配置**（适用于自定义设置）：
```bash
OPENFLEET_API_KEY=ofk_xxx npx -y @open-fleet/mcp-server
```

## OpenFleet 与 OpenClaw 的集成

当您将 OpenFleet 与 OpenClaw 门户连接时，该工具可以实现双向数据交互：

| 方向 | 功能 |
|-----------|-------------|
| **OpenFleet → OpenClaw** | OpenFleet 将任务发送到 OpenClaw 门户进行执行 |
| **OpenClaw → OpenFleet** | 该工具允许 OpenClaw 管理任务、代理以及执行自动化任务 |

### 完整设置流程

1. 启动您的 OpenClaw 门户：`openclaw gateway`
2. 暴露门户的访问地址：`cloudflared tunnel --url http://localhost:18789`
3. 在 [OpenFleet 设置](https://app.openfleet.sh) 中输入该门户的地址和令牌信息 |
4. 安装该工具：`clawhub install openfleet`

## 相关资源

- [OpenFleet 仪表板](https://app.openfleet.sh)
- [API 文档](https://app.openfleet.sh/docs)
- [GitHub 仓库](https://github.com/open-fleet)
- [SDK](https://www.npmjs.com/package/@open-fleet/sdk)