---
name: openclaw-cheatsheet
description: >
  **OpenClaw CLI 命令、子命令及参数的快速参考**  
  当用户询问 OpenClaw CLI 的使用方法（如代理、消息、配置、网关、定时任务、钩子、模型、通道、目录、会话、技能、代理、内存、健康状况、状态、诊断工具、日志等），需要命令示例，或在执行命令前验证相关参数时，可参考本文档。  
  **主要内容涵盖：**  
  - 所有 OpenClaw CLI 命令  
  - 各命令的子命令  
  - 各命令的可选参数（flag）  
  **使用说明：**  
  - 本文档以简洁明了的方式解释了每个命令的用途和参数含义。  
  - 包含详细的命令示例，帮助用户更好地理解命令的实际操作。  
  - 适用于所有与 OpenClaw CLI 相关的场景。  
  **示例：**  
  - `openclaw agent`：用于管理代理。  
  - `openclaw message`：用于发送消息。  
  - `openclaw config`：用于配置系统设置。  
  - `openclaw gateway`：用于配置网关。  
  - `openclaw cron`：用于设置定时任务。  
  - `openclaw hooks`：用于配置事件触发器。  
  - `openclaw models`：用于管理模型。  
  - `openclaw channels`：用于管理通信通道。  
  - `openclaw directory`：用于操作目录。  
  - `openclaw sessions`：用于管理会话。  
  - `openclaw skills`：用于管理技能。  
  - `openclaw agents`：用于管理代理实例。  
  - `openclaw memory`：用于查询系统内存信息。  
  - `openclaw health`：用于查看系统健康状况。  
  - `openclaw status`：用于获取系统状态。  
  - `openclaw doctor`：用于执行系统诊断。  
  - `openclaw logs`：用于查看系统日志。  
  **注意事项：**  
  - 请确保在运行命令前仔细阅读文档中的参数说明，以避免错误操作。  
  - 如有特定命令或参数的详细说明，请参考相应的文档或官方文档。  
  **更多信息：**  
  如需了解更多关于 OpenClaw CLI 的信息，请访问 [OpenClaw 官方文档](https://www.openclaw.org/docs/)。
---
# OpenClaw 快速参考指南

主要参考文档：`references/openclaw-cheatsheet.md`

## 适用场景

- 当用户询问 OpenClaw 的命令、参数列表或使用示例时。
- 当用户需要了解如何发送消息、管理定时任务（cron jobs）、配置频道/模型、运行网关（gateway）等操作时。
- 在进行任何操作性更改之前（如 `config set`、`gateway restart`、`cron add/edit`、`channels add/remove`、`models set`、`hooks install/enable` 等）。
- 当用户要求查看快速参考指南或询问某个参数的用途时。

## 规则

1. 在回答与 OpenClaw 相关的命令行（CLI）问题之前，务必先阅读 `references/openclaw-cheatsheet.md`；切勿随意猜测参数的用途。
2. 如果快速参考指南中未涵盖某个参数的用法，请使用 `openclaw <command> --help` 来查询其详细信息。
3. 在执行任何可能破坏系统状态或数据的命令（如 `config set`、`gateway restart`、`cron rm`、`channels remove`、`reset`、`uninstall`）之前，务必先征得用户的确认。
4. 回答要简洁明了，仅提供与用户问题相关的信息。

## 回答格式

1. 从快速参考指南中提取相关内容。
2. 根据用户的实际情况，提供 1-3 个可直接复用的示例。
3. 对于可能具有危险性的操作（如重启、更新、配置更改、删除、卸载），在命令前添加警告提示。
4. 如果用户是新手，需简要说明每个参数的用途。

## 快速参考指南的内容结构（各章节包含的子命令）

| 章节 | 主要子命令 |
|---------|-----------------|
| 全局选项 | `--dev`, `--profile`, `--no-color`, `-V` |
| 代理（Agent） | `agent`（运行单个代理） |
| 消息（Message） | `send`, `read`, `edit`, `delete`, `search`, `broadcast`, `react`, `reactions`, `thread`, `pin/unpin/pins`, `poll`, `ban/kick/timeout`, `permissions`, `emoji`, `sticker`, `event`, `member`, `role`, `channel`, `voice` |
| 配置（Config） | `get`, `set`, `unset`, `wizard` |
| 会话（Sessions） | `sessions`（列出会话、按活跃状态筛选/保存会话） |
| 网关（Gateway） | `run`, `status`, `start/stop/restart`, `install/uninstall`, `discover`, `call`, `probe`, `usage-cost` |
| 守护进程（Daemon） | 用于管理网关服务的旧称 |
| 技能（Skills） | `list`, `info`, `check` |
| 代理（Agents） | `list`, `add`, `delete`, `set-identity` |
| 内存（Memory） | `search`, `index`, `status` |
| 定时任务（Cron） | `add`, `edit`, `list`, `rm`, `run`, `runs`, `status`, `enable/disable` |
| 事件触发器（Hooks） | `list`, `info`, `enable/disable`, `install`, `check`, `update` |
| 模型（Models） | `list`, `set`, `scan`, `status`, `aliases`, `auth`, `fallbacks/image-fallbacks` |
| 频道（Channels） | `list`, `add`, `login/logout`, `remove`, `status`, `capabilities`, `resolve`, `logs` |
| 目录（Directory） | `self`, `peers list`, `groups list`, `groups members` |
| 系统健康/状态/诊断/日志（Health/Status/Doctor/Logs） | 系统诊断及日志查看 |
| Obsidian（相关功能） | `create`, `print`, `search`, `search-content`, `delete` |

## 参考文档

- `references/openclaw-cheatsheet.md`：官方发布的快速参考指南，内容会随着 OpenClaw 的更新而更新（最新版本：2026.2.17+）。