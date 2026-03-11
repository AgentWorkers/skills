---
name: skill-to-agent
description: 将 OpenClaw 中的技能（Skills）转换为配置正确的代理（Agents），并确保工作区（Workspace）的设置、绑定（Binding）以及协调（Orchestration）都符合要求。这可以解决常见的代理创建问题（如线程绑定错误、工作区隔离问题、会话生成异常等）。在从技能创建代理时，或在遇到代理绑定错误时，可以使用此方法。
---
# 将 OpenClaw 技能转换为功能完备的代理（Skill to Agent）

本指南介绍如何将 OpenClaw 技能转换为具有完整工作空间配置和会话管理的代理程序。这可以解决一些常见的问题，例如 “`thread=true` 无法使用” 或 “`mode="session"` 需要 `thread=true` 等情况。

## 快速入门

1. **分析技能** - 阅读 SKILL.md 文件以了解需求。
2. **准备工作空间** - 在 `~/.openclaw/agents/` 目录下创建代理目录。
3. **配置代理** - 设置代理的身份信息、所需工具和内存策略。
4. **根据通道类型选择正确的绑定方式** - 选择合适的运行模式。

## 工作流程

### 第 1 阶段：技能分析
- 从 SKILL.md 文件中提取元数据（名称、描述、触发条件）。
- 确定所需的工具和依赖项。
- 判断代理类型：独立运行（isolated）、基于线程运行（thread-bound）或常规运行模式（run-mode）。

### 第 2 阶段：工作空间设置
- 创建具有正确结构的工作空间目录。
- 复制技能相关的文件（如参考文件、脚本等）。
- 配置 AGENTS.md、TOOLS.md 和 USER.md 文件。

### 第 3 阶段：代理配置
- 创建 SOUL.md 和 IDENTITY.md 文件，以定义代理的属性和功能。
- 将技能所需的工具与代理的功能对应起来。
- 设置内存策略（参考 MEMORY.md 和 memory/ 目录）。

### 第 4 阶段：代理注册
- 将代理添加到 OpenClaw 的 `agents.list` 配置文件中。
- 使用 `gateway` 工具和 `config.patch` 命令进行配置更新。
- 提供代理的 ID、名称、工作空间路径（workspace）和代理目录（agentDir）。
- OpenClaw 的网关（gateway）会自动重启以应用新的配置。

### 第 5 阶段：代理启动
- 根据通道的属性选择合适的启动策略（基于线程的启动、独立运行或常规运行模式）。
- **重要提示：** **务必将 `cwd` 设置为代理的工作空间目录**。
- 验证代理是否能够正常启动以及是否可以访问所需的工具。

## 参考资料

有关详细指导，请参阅以下文档：
- **使用指南** - [usage-guide.md](references/usage-guide.md) - 包含完整的工作流程和示例。
- **故障排除** - [troubleshooting.md](references/troubleshooting.md) - 常见问题及解决方法。
- **实战示例** - [war-room-example.md](references/war-room-example.md) - 具体的转换示例。

## 脚本

- `scripts/skill_to_agent.js` - 主要的转换脚本。

## 绑定策略

| 通道类型 | 运行模式 | 是否需要线程 | 适用场景 |
|--------|---------|-----------|---------|
| Discord/Telegram | session | 是         | 需要多线程处理的群组讨论 |
| WebChat/控制界面 | run      | 否         | 单次性任务 |
| 独立处理 | session     | 否         | 后台任务 |
| 定时任务（Cron） | run      | 否         | 自动化任务 |

**决策流程**：
- 该通道支持多线程吗？ → 如果支持 → 设置 `thread=true` 和 `mode=session`。
- 需要独立处理吗？ → 如果需要 → 设置 `thread=false` 和 `mode=session`。
- 否则 → 设置 `thread=false` 和 `mode=run`。

## 常见错误及解决方法

**错误 1：`thread=true` 无法使用**
- 解决方案：使用 `mode="run"` 并禁用线程绑定。
- 先检查通道是否支持多线程。

**错误 2：`mode="session" 需要 thread=true`**
- 解决方案：使用独立会话模式（`mode="session"`，同时设置 `thread=false` 和 `runtime="subagent"`。

**错误 3：代理无法访问工具**
- 解决方案：检查 TOOLS.md 文件中列出的工具是否正确。
- 更新代理的工作空间配置。

**错误 4：无法访问工作空间文件**
- 解决方案：在启动代理时设置 `cwd` 参数。
- 代理的工作空间路径必须与 `cwd` 参数匹配。
- 确保代理具有对该工作空间的读写权限。

**错误 5：代理无法找到身份文件**
- 解决方案：始终将 `cwd` 设置为代理的工作空间目录。
- 代理会从当前目录读取 IDENTITY.md、SOUL.md 等文件。
- 用简单的 `read` 命令测试文件是否可读。

**错误 6：OpenClaw 系统无法识别代理**
- 解决方案：将代理注册到 `agents.list` 配置文件中。
- 使用 `gateway` 工具和 `config.patch` 命令进行配置更新。
- 配置更改后需要重启网关。
- 确认代理已出现在配置列表中。

## 关键点：工作空间目录（cwd）

在启动代理时，**务必将 `cwd` 参数设置为代理的工作空间目录**：
```javascript
sessions_spawn({
  task: "Agent instructions...",
  label: "agent-name",
  runtime: "subagent",
  mode: "session", // or "run"
  cwd: "/Users/nimbletenthousand/.openclaw/agents/agent-name",
  timeoutSeconds: 300
});
```

如果不设置 `cwd`，代理将无法找到其身份文件（IDENTITY.md、SOUL.md 等），从而导致无法正常运行。

## 关键点：代理注册

创建代理工作空间后，**必须将其注册到 OpenClaw 的配置文件中**：
```javascript
gateway({
  action: "config.patch",
  raw: JSON.stringify({
    agents: {
      list: [
        {
          id: "agent-name",
          name: "Agent Display Name",
          workspace: "/Users/nimbletenthousand/.openclaw/workspace",
          agentDir: "/Users/nimbletenthousand/.openclaw/agents/agent-name"
        }
      ]
    }
  }),
  note: "Added [agent-name] to agents configuration"
});
```

网关会自动重启以应用新的配置。如果未完成注册，代理将不会被系统识别为已配置的代理。

## 快速命令

```bash
# Check skill structure
node scripts/skill_to_agent.js --analyze --skill /path/to/skill

# Create agent workspace
node scripts/skill_to_agent.js --create --skill /path/to/skill --agent agent-name

# Spawn agent with correct binding
node scripts/skill_to_agent.js --spawn --agent agent-name --mode session --cwd /path/to/agent-workspace
```

## 最佳实践
1. **保持简洁** - 只复制必要的技能文件。
2. **先测试绑定方式** - 确认通道是否支持所需的运行模式。
3. **定期检查代理状态** - 定期查看 `sessions_list` 文件。
4. **及时清理** - 删除不再使用的代理工作空间。
5. **记录转换过程** - 保存配置信息以备后续参考。

## 下一步操作
创建代理后：
1. 确认代理是否已出现在 `sessions_list` 中。
2. 测试代理是否能访问所需的工具。
3. 如有需要，配置心跳检测功能。
4. 与父代理进行协同工作（如果适用）。

有关高级用法和完整示例，请参阅相关参考文件。