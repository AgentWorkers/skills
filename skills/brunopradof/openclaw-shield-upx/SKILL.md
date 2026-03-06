---
name: openclaw-shield-upx
description: "**OpenClaw代理的安全监控功能**  
- 检查Shield系统的运行状态  
- 查看安全事件记录  
- 监控数据存储库（vault）的访问情况  
**适用场景**：  
- 当用户询问系统安全状况、Shield系统的健康状态、事件日志或数据存储库的访问情况时  
**不适用场景**：  
- 用于操作系统的一般性加固、防火墙配置或网络安全设置的管理  
**注意**：  
- 本功能专注于OpenClaw代理的安全监控，不涉及更广泛的系统管理或网络安全配置。"
homepage: https://www.upx.com/en/lp/openclaw-shield-upx
source: https://www.npmjs.com/package/@upx-us/shield
metadata: {"openclaw": {"requires": {"config": ["plugins.entries.shield"]}, "homepage": "https://clawhub.ai/brunopradof/openclaw-shield-upx", "emoji": "🛡️"}}
---
# OpenClaw Shield

OpenClaw Shield 是由 [UPX](https://www.upx.com) 提供的安全监控工具，用于监控 OpenClaw 代理的活动。该插件作为 OpenClaw 网关的一部分运行，会捕获代理的运行状态，并将经过脱敏处理的遥测数据发送到 UPX 检测平台。

## 开始使用

使用 OpenClaw Shield 需要安装 `@upx-us/shield` 插件并激活相应的订阅服务。

- **插件**: [@upx-us/shield](https://www.npmjs.com/package/@upx-us/shield)
- **订阅 / 免费 30 天试用**: [upx.com/en/lp/openclaw-shield-upx](https://www.upx.com/en/lp/openclaw-shield-upx)
- **控制面板**: [uss.upx.com](https://uss.upx.com)

## 命令

| 命令 | 功能 |
|---|---|
| `openclaw shield status` | 查看插件状态、连接情况、事件数量及上次同步时间 |
| `openclaw shield flush` | 强制立即将数据同步到平台 |
| `openclaw shield logs` | 查看本地缓冲区中的最近事件（过去 24 小时） |
| `openclaw shield logs --last 20` | 显示最近 N 个事件 |
| `openclaw shield logs --type TOOL_CALL --since 1h` | 按事件类型或时间范围筛选事件 |
| `openclaw shield logs --format json` | 以 JSON 格式输出日志 |
| `openclaw shield vault show` | 显示代理和工作区的信息，以及数据脱敏的汇总情况（以哈希值表示） |
| `openclaw shield cases` | 列出所有未解决的安全事件 |
| `openclaw shield cases show <ID>` | 显示特定事件的详细信息（包括相关规则和处理流程） |
| `openclaw shield cases resolve <ID>` | 解决事件（可选参数：--resolution, --root-cause, --comment） |
| `openclaw shield monitor` | 设置事件通知的定时任务（可选参数：--on, --off, --interval） |

## 使用场景

- 询问 Shield 是否正在运行：`openclaw shield status`
- 了解 Shield 最近捕获了哪些事件：`openclaw shield logs`
- 查看当前机器上的代理数量：`openclaw shield vault show`
- 强制同步数据：`openclaw shield flush`
- 当用户询问安全警报或事件详情时：根据您的安全知识和 Shield 的日志进行解释
- 当用户询问 Shield 的隐私政策时：引导用户查看插件的 README 文件
- 用户希望快速查看事件详情（无需代理参与）：`/shieldcases`

## 状态说明

运行 `openclaw shield status` 后，可查看以下状态：
- **Connected**：插件运行正常，无需额外操作
- **Disconnected**：可能需要重启网关
- **High failure count**：可能是平台连接问题，通常会自动恢复；可以尝试 `openclaw shield flush`
- **Rising quarantine**：可能表示版本不匹配，建议检查插件更新

## RPC（远程过程调用）

当检测规则触发时，系统会自动创建事件。插件会直接向用户发送实时警报，无需代理进行任何操作。仅在用户询问具体事件时才使用 `shield.cases_list` 命令。

**重要提示：** 未经用户明确授权，切勿直接解决或关闭事件。在调用 `shield.case.resolve` 之前，务必向用户展示事件详情并征求处理意见。

| RPC | 参数 | 功能 |
|---|---|---|
| `shield.status` | 无 | 查看插件状态、事件计数及事件监控状态 |
| `shield.flush` | 无 | 强制触发数据同步 |
| `shield.events_recent` | `limit`, `type`, `sinceMs` | 查询本地事件缓冲区 |
| `shield.events_summary` | `sinceMs` | 按类别统计事件数量 |
| `shield.subscription_status` | 无 | 显示订阅级别、有效期及可用功能 |
| `shield.cases_list` | `status`, `limit`, `since` | 列出未解决的事件及待处理的通知 |
| `shield.case_detail` | `id` | 显示事件的详细信息（包括规则和处理流程） |
| `shield.case.resolve` | `id`, `resolution`, `root_cause`, `comment` | 关闭事件 |
| `shield.cases_ACK` | `ids` | 标记事件已通知用户 |

**事件解决状态**：`true_positive`, `false_positive`, `benign`, `duplicate`
**事件的根本原因**：`user_initiated`, `misconfiguration`, `expected_behavior`, `actual_threat`, `testing`, `unknown`

## 数据展示

RPC 响应中包含一个 `display` 字段，其中包含预格式化的文本。如果有该字段，可以直接使用该文本作为响应内容（其中已包含事件的严重性等级、ID、描述及后续操作建议）。如果 `display` 字段缺失，可手动格式化数据。

在讨论事件时，通过消息工具提供相应的操作按钮（如“解决”、“误报”或“调查”），以便用户能够快速采取行动。

## 注意事项

- Shield 不会干扰代理的正常运行或性能
- UPX 平台使用 80 多种检测规则来分析脱敏后的遥测数据
- 订阅到期后，系统会停止接收新事件（不会排队处理）；请在 [upx.com/en/lp/openclaw-shield-upx](https://www.upx.com/en/lp/openclaw-shield-upx) 重新订阅