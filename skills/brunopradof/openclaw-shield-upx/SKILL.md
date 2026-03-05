---
name: openclaw-shield-upx
description: "**OpenClaw代理的安全监控功能**  
- 检查Shield系统的运行状态  
- 查看安全事件日志  
- 监控数据存储库（vault）的访问情况  
**适用场景**：  
- 当用户询问系统安全状态、Shield系统的运行状况或事件日志时  
- 需要审查或管理数据存储库中的敏感信息时  
**不适用场景**：  
- 用于操作系统的一般性安全加固、防火墙配置调整或网络安全设置  
**使用说明**：  
这些功能专为OpenClaw代理设计，用于帮助管理员监控系统的安全状况和数据保护措施。  
**注意事项**：  
- 请确保仅在这些特定场景下使用这些功能，以避免干扰系统的正常运行或引入额外的安全风险。"
metadata: {"openclaw": {"requires": {"config": ["plugins.entries.shield"]}, "homepage": "https://clawhub.ai/brunopradof/openclaw-shield-upx", "emoji": "🛡️"}}
---
# OpenClaw Shield

OpenClaw Shield 是由 [UPX](https://www.upx.com) 提供的安全监控工具，用于监控 OpenClaw 代理的运行状态。该插件作为 OpenClaw 网关的扩展组件运行，负责捕获代理的活动数据，并将经过脱敏处理的遥测信息发送至 UPX 检测平台。

## 开始使用

使用 OpenClaw Shield 需要安装 `@upx-us/shield` 插件并订阅相应的服务（提供 30 天免费试用）。  
- **插件（npm）**：[@upx-us/shield](https://www.npmjs.com/package/@upx-us/shield)  
- **订阅 / 免费试用**：[upx.com/pt/lp/openclaw-shield-upx](https://www.upx.com/pt/lp/openclaw-shield-upx)  
- **控制面板**：[uss.upx.com](https://uss.upx.com)

## 命令

| 命令 | 功能 |
|---|---|
| `openclaw shield status` | 显示插件状态、连接情况、事件统计信息及上次同步时间 |
| `openclaw shield flush` | 强制立即将数据同步到 UPX 平台 |
| `openclaw shield activate <KEY>` | 使用安装密钥进行一次性激活 |
| `openclaw shield logs` | 查看本地缓冲区中的最近事件（过去 24 小时） |
| `openclaw shield logs --last 20` | 显示最近 N 个事件 |
| `openclaw shield logs --type TOOL_CALL --since 1h` | 按事件类型或时间范围筛选日志 |
| `openclaw shield logs --format json` | 以 JSON 格式输出日志 |
| `openclaw shield vault show` | 显示代理和工作区的信息（使用哈希标识符） |
| `openclaw shield vault redactions` | 查看数据脱敏的详细信息（包括脱敏类别和数量） |
| `openclaw shield cases` | 列出所有未解决的安全事件 |
| `openclaw shield cases show <ID>` | 查看特定事件的详细信息（包括相关规则和操作流程） |
| `openclaw shield cases resolve <ID>` | 解决事件（可选参数：--resolution, --root-cause, --comment） |

## 使用场景

- 询问 Shield 是否正在运行：`openclaw shield status`  
- 了解 Shield 最近捕获了哪些事件：`openclaw shield logs`  
- 查看当前机器上运行的代理数量：`openclaw shield vault show`  
- 强制同步数据：`openclaw shield flush`  
- 当用户询问安全警报或事件详情时：结合安全知识和 Shield 的数据进行分析  
- 询问 Shield 的隐私政策：所有数据在传输前都会在设备上进行脱敏处理，原始数据不会离开设备  

## 状态解释

运行 `openclaw shield status` 后，可查看以下状态：  
- **Connected**：插件运行正常，无需额外操作  
- **Disconnected**：可能需要重启网关  
- **High failure count**：可能存在平台连接问题，通常可自行恢复；尝试 `openclaw shield flush`  
- **Rising quarantine**：可能表示版本不匹配，建议检查插件更新  

## 事件处理

当检测规则触发时，系统会自动创建事件记录。您可以通过 `shield.cases_list` 命令查看这些事件：  
- 如果 `pending_count > 0`，请通知用户，并使用 `shield.cases_ack` 命令标记事件已被处理。  

**RPC 方法及参数说明**：  
| 方法 | 参数 | 用途 |
|---|---|---|
| `shield.cases_list` | `status`, `limit`, `since` | 列出所有未解决的事件及待处理的通知 |
| `shield.case_detail` | `id` | 显示事件的详细信息（包括规则和操作流程） |
| `shield.case.resolve` | `id`, `resolution`, `root_cause`, `comment` | 关闭事件 |
| `shield.cases_ack` | `ids` | 标记事件已处理 |

**事件解决状态**：`true_positive`, `false_positive`, `benign`, `duplicate`  
**根本原因**：`user_initiated`, `misconfiguration`, `expected_behavior`, `actual_threat`, `testing`, `unknown`