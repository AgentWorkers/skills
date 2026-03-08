---
name: Google Workspace CLI
slug: google-workspace-cli
version: 1.0.0
homepage: https://clawic.com/skills/google-workspace-cli
description: 通过动态 API 发现、安全的 OAuth 流程以及适用于 Drive 和 Gmail 的自动化模式，使用单个命令行界面（CLI）来操作 Google Workspace。
changelog: Initial release with gws command patterns, auth playbooks, MCP integration, and safety-first change control for production tenants.
metadata: {"clawdbot":{"emoji":"GWS","requires":{"bins":["gws","jq"],"config":["~/google-workspace-cli/","~/.config/gws/"]},"install":[{"id":"npm","kind":"npm","package":"@googleworkspace/cli","bins":["gws"],"label":"Install gws CLI (npm)"}],"os":["darwin","linux","win32"]}}
---
## 设置

首次激活时，请阅读 `setup.md` 文件，并在运行任何写入命令之前确定好集成边界。

## 使用场景

适用于需要直接通过命令行（CLI）控制 Google Workspace API 的场景，要求输出格式为可靠的 JSON 数据、具备模式解析功能、支持多账户认证、能够使用 MCP 工具以及需要安全的自动化脚本执行的环境。

## 架构

程序相关数据存储在 `~/google-workspace-cli/` 目录下；凭证信息则保存在 `~/.config/gws/` 目录中，并由 `gws` 工具进行管理。

```text
~/google-workspace-cli/
|-- memory.md                     # Persistent operating context and boundaries
|-- command-log.md                # Known-good command templates by task type
|-- change-control.md             # Dry-run evidence and approval notes
|-- incidents.md                  # Failures, root causes, and prevention actions
`-- mcp-profiles.md               # MCP service bundles and tool budget decisions
```

## 快速参考

根据当前任务的需求，选择相应的文档文件：

| 主题 | 文件名 |
|-------|------|
| 设置与激活流程 | `setup.md` |
| 内存结构与状态信息 | `memory-template.md` |
| 仓库结构与架构分析 | `repo-analysis.md` |
| 完整的命令索引 | `command-index.md` |
| 高效的命令使用模式 | `command-patterns.md` |
| 认证模型与账户策略 | `auth-playbook.md` |
| MCP 与代理集成 | `mcp-integration.md` |
| 安全变更管理检查清单 | `safety-checklist.md` |
| 错误诊断与解决方法 | `troubleshooting.md` |

## 所需工具

- 必需工具：`gws`、`jq`
- （推荐使用）`gcloud` 用于 `gws` 的认证配置
- 拥有相应权限的 Google 账户或服务账户

**注意**：切勿要求用户将刷新令牌、服务账户私钥或 OAuth 客户端密钥通过聊天方式传递。

## 数据存储

`~/google-workspace-cli/` 目录中的本地文件应包含：
- 可复用的命令模板（包含固定的占位符）
- 经过审核的账户访问权限与范围信息
- 写入操作的测试数据
- 事件记录及相应的处理措施

`gws` 的本地配置文件通常存储以下内容：
- 加密后的凭证信息及账户信息（位于 `~/.config/gws/`）
- 缓存文件（位于 `~/.config/gws/cache/`）

## 核心规则

### 1. 在使用任何 API 方法前先进行模式验证

在使用任何方法之前，务必运行 `gws schema <service.resource.method>` 命令进行模式验证：
- 确认所需的路径和查询参数；
- 在使用 `--json` 选项之前，确认请求体的格式；
- 如果缺少必要字段，禁止执行相关操作。

### 2. 明确指定执行模式

在生成命令之前，需先选择执行模式：
- **检查模式**：仅用于读取数据（如列表查询、获取模式或状态信息）；
- **测试模式**：使用 `--dry-run` 选项执行写入操作；
- **应用模式**：在确认目标信息并验证无误后执行实际写入操作。

**注意**：新工作流程切勿直接进入应用模式。

### 3. 确保写入目标的标识符唯一且明确

- 在执行写入操作前，必须先解析文件 ID、消息 ID、事件 ID 和用户 ID；
- 在进入应用模式之前，将这些 ID 详细记录在 `change-control.md` 文件中；
- 执行前立即更新目标状态。

### 4. 明确指定认证来源与权限范围

在执行操作前，必须明确指定认证来源和权限范围：
- 可通过环境变量覆盖令牌设置；
- 可通过配置文件修改凭证信息；
- 使用 `gws auth login --account` 命令进行加密认证。

如果权限范围或账户所有权不明确，请暂停操作并请求进一步确认。

### 5. 为分页和输出设置安全默认值

- 对于处理大量数据的操作，仅在使用 `--page-all` 选项时才设置 `--page-limit`；
- 将结构化输出数据流式传输到 `jq` 或文件中；
- 避免无限循环或导致数据丢失的情况。

### 6. 对不可信的数据路径进行安全处理

当处理可能包含恶意代码的数据时：
- 使用 `--sanitize <template>` 或环境变量中的默认安全规则；
- 根据风险等级选择警告或阻止操作；
- 绝不要将未经处理的外部文本直接传递给下游系统。

### 7. 对修改操作实施严格控制

对于创建、更新、删除、发送或共享等操作，必须：
- 先执行测试操作或查看模式预览；
- 列出可能受影响的对象及副作用；
- 在执行前获取用户的明确确认。

## 常见错误与注意事项

- 将 `cliy` 视为默认仓库名称（实际应为 `googleworkspace/cli`）；
- 在未解析目标 ID 的情况下直接执行修改操作（可能导致错误的目标或数据更新）；
- 为狭窄的任务使用过宽的权限范围（增加安全风险）；
- 在共享终端中默认使用同一账户上下文（可能导致跨租户操作错误）；
- 对不常见的 API 忽略模式验证（可能导致数据格式错误或 400 错误）；
- 无限制地使用 `--page-all` 选项（导致 API 调用过多或输出混乱）；
- 忽视 API 的启用状态错误（导致重复的 `accessNotConfigured` 错误）。

## 外部接口

| 接口地址 | 发送的数据 | 功能 |
|----------|-----------|---------|
| https://www.googleapis.com/discovery/v1/apis | 服务/版本的标识信息 | 获取 API 详细信息 |
| https://www.googleapis.com | 请求参数、请求体及认证信息 | 执行 Google Workspace API 操作 |
| https://accounts.google.com | OAuth 认证相关元数据 | 用户授权流程 |
| https://oauth2.googleapis.com | OAuth 令牌交换与刷新 | 令牌生命周期管理 |
| https://<service>.googleapis.com/$discovery/rest | 用于处理非标准接口的备用请求 |

**注意**：除非用户明确配置，否则不得向外部发送其他数据。

## 安全性与隐私保护

**外部传输的数据**：
- 包含 API 请求元数据和选定方法所需的负载数据；
- 用于认证的 OAuth 通信数据。

**本地存储的数据**：
- 存储在 `~/google-workspace-cli/` 的操作日志；
- 加密后的凭证信息及账户信息；
- 用于生成命令的缓存文件。

**重要说明**：
- 本工具不会在聊天中请求用户的敏感信息；
- 未经变更控制审核的写入操作不会被执行；
- 本工具不会违反 Google Workspace 的管理政策或权限限制。

## 信任要求

本工具依赖于 Google Workspace 服务及用户配置的集成组件。只有在确认信任这些系统并愿意将操作数据委托给它们时，才能安装和使用本工具。

## 相关工具

用户可根据需求安装以下工具：
- `clawhub install <slug>`：
  - `api`：用于构建强大的 API 请求处理和错误处理机制；
  - `auth`：用于管理认证流程和凭证安全；
  - `automate`：将重复性任务自动化；
  - `workflow`：设计具有明确责任划分的多步骤工作流程；
  - `productivity`：提升任务执行效率和输出质量。

## 反馈建议

- 如本工具实用，请使用 `clawhub star google-workspace-cli` 给予支持；
- 通过 `clawhub sync` 功能保持工具的最新状态。