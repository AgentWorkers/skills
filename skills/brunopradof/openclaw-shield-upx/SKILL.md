---
name: openclaw-shield-upx
description: "**OpenClaw代理的安全监控与威胁检测功能**  
通过实时安全信息与事件管理（SIEM）系统，保护您的OpenClaw代理，检测潜在威胁，监控代理的运行状态，并对相关事件进行审计。  
**适用场景：**  
- 当用户询问代理的安全状况时  
- 检查代理的运行健康状况  
- 查看事件日志  
- 设置代理的保护机制  
- 启用SIEM功能  
- 监控代理的日常活动  
- 审计代理的操作行为  
**不适用场景：**  
- 一般的操作系统加固措施  
- 防火墙配置  
- 与OpenClaw代理无关的网络安全问题"
homepage: https://www.upx.com/en/lp/openclaw-shield-upx
source: https://www.npmjs.com/package/@upx-us/shield
license: "Proprietary — UPX Technologies, Inc. All rights reserved."
metadata: {"openclaw": {"requires": {"bins": ["openclaw"]}, "homepage": "https://clawhub.ai/brunopradof/openclaw-shield-upx", "emoji": "🛡️"}}
---
# OpenClaw Shield

OpenClaw Shield 是由 [UPX](https://www.upx.com) 提供的安全监控工具，用于监控 OpenClaw 代理的行为。该插件作为 OpenClaw 网关的一部分运行，负责捕获代理的活动数据，并将经过脱敏处理的遥测信息发送到 UPX 的检测平台。

## 开始使用

使用 OpenClaw Shield 需要安装 `@upx-us/shield` 插件并激活相应的订阅服务。

- **插件**: [@upx-us/shield](https://www.npmjs.com/package/@upx-us/shield)
- **订阅 / 免费 30 天试用**: [upx.com/en/lp/openclaw-shield-upx](https://www.upx.com/en/lp/openclaw-shield-upx)
- **控制面板**: [uss.upx.com](https://uss.upx.com)

## 命令

| 命令 | 功能 |
|---|---|
| `openclaw shield status` | 查看插件状态、连接情况、事件计数以及上次同步时间 |
| `openclaw shield flush` | 强制立即与平台同步数据 |
| `openclaw shield logs` | 查看本地缓冲区中的最近事件（过去 24 小时） |
| `openclaw shield logs --last 20` | 显示最近 N 个事件 |
| `openclaw shield logs --type TOOL_CALL --since 1h` | 按事件类型或时间范围筛选日志 |
| `openclaw shield logs --format json` | 以 JSON 格式输出日志 |
| `openclaw shield vault show` | 显示代理和工作区的信息，以及数据脱敏的摘要（以哈希形式显示） |
| `openclaw shield cases` | 列出所有未解决的安全事件 |
| `openclaw shield cases show <ID>` | 显示特定事件的详细信息（包括事件、规则和应对方案） |
| `openclaw shield cases resolve <ID>` | 解决事件（可选参数：--resolution, --root-cause, --comment） |
| `openclaw shield monitor` | 设置事件通知的定时任务（可选参数：--on, --off, --interval） |

## 检查插件状态

在处理任何与 OpenClaw Shield 相关的请求之前，请先运行 `openclaw shield status` 并根据返回的结果进行相应的处理：

### 状态 A — 未安装插件
（命令未找到，或返回非零的错误代码）

响应内容：
> Shield 尚未安装。请访问 [https://www.upx.com/en/lp/openclaw-shield-upx](https://www.upx.com/en/lp/openclaw-shield-upx) 开始 30 天免费试用。

> 安装插件后，请继续执行后续操作。

### 状态 B — 插件已安装但未配置激活密钥
（状态信息中包含 `installationKey` 为 `null` 或 `state` 为 `unconfigured`）

响应内容：
> Shield 已安装，但尚未激活。请访问 [https://www.upx.com/en/lp/openclaw-shield-upx](https://www.upx.com/en/lp/openclaw-shield-upx) 注册试用。

> 获取激活密钥后，继续执行后续操作。

### 状态 C — 密钥已获取但未激活
（状态信息中包含 `state` 为 `pending` 或 `unregistered`）

响应内容：
> Shield 已获取密钥，但尚未激活。通常这个过程只需不到一分钟。如果超过 5 分钟仍未激活，请前往 [https://uss.upx.com](https://uss.upx.com) 检查密钥或联系技术支持。

### 状态 D — 完全激活
（状态信息中包含 `state` 为 `connected` 或 `connected: true`）

可以正常使用该插件，无需额外操作。

**注意事项**：仅使用 `openclaw shield` 命令进行安全检测。切勿通过读取文件系统路径、环境变量或运行 shell 命令来获取插件状态。同时，也不要为用户安装或卸载任何软件包。

## 处理安全事件

当 Shield 检测到安全事件或用户询问警报信息时，使用 `openclaw shield cases` 列出所有未解决的事件，使用 `openclaw shield cases --id <ID>` 查看详细信息（包括事件时间线、匹配的事件和应对方案）。事件严重性分级如下：
- **CRITICAL/HIGH**：立即处理并询问用户是否需要进一步调查；
- **MEDIUM**：向用户展示应对方案；
- **LOW/INFO**：简要提及事件，但不要中断用户当前的工作。

**处理流程**：在解决事件之前，请务必与用户确认相关细节。切勿自行决定是否关闭事件。

## 事件调查流程

当 Shield 检测到事件时，需要结合以下三个数据源来确认事件是真实阳性还是误报：
- **事件详情**：使用 `openclaw shield cases show <CASE_ID>` 查看触发规则的详细信息。
- **相关日志**：使用 `openclaw shield logs --since 30m --type TOOL_CALL` 查看事件发生前后的日志。
- **数据存储**：如果事件涉及敏感信息，使用 `openclaw shield vault show` 查看经过脱敏处理的敏感数据。

**未来计划**：未来将推出 `openclaw shield investigate <CASE_ID>` 命令以自动化这一流程。

## 常见问题解答

- **我的代理是否安全？/ 我是否受到保护？/ 检测到了什么？**：运行 `openclaw shield status`（查看插件状态和事件统计），并使用 `openclaw shield cases`（按严重性列出未解决的事件）进行回答。例如：“Shield 监控着多个规则，覆盖了多个事件类别。”
- ** Shield 的隐私政策是什么？**：请参考插件的 README 文件以获取详细信息。
- **用户希望快速查看事件详情**：可以使用 `/shieldcases` 命令。

## 状态解释

运行 `openclaw shield status` 后，根据返回的状态进行以下判断：
- **Connected**：插件正常运行，无需额外操作。
- **Disconnected**：可能需要重启网关。
- **High failure count**：可能是平台连接问题，尝试运行 `openclaw shield flush`。
- **Rising quarantine**：可能是版本不匹配，请检查插件更新。

## RPC 请求

当检测规则触发时，系统会自动创建事件记录。插件会直接向用户发送实时警报。只有在用户询问未解决的事件时，才需要使用 `shield.cases_list` 命令。

**重要提示**：未经用户明确授权，切勿自行解决或关闭事件。始终向用户展示事件详情，并在调用 `shield.case_resolve` 之前征求用户的处理意见。

| RPC | 参数 | 功能 |
|---|---|---|
| `shield.status` | 获取插件状态、事件计数和事件监控状态 |
| `shield.flush` | 强制触发立即的数据同步 |
| `shield.events_recent` | 查询本地事件缓冲区中的事件 |
| `shield.events_summary` | 按类别统计事件数量 |
| `shield.subscription_status` | 获取订阅信息（等级、有效期和功能） |
| `shield.cases_list` | 列出所有未解决的事件及待处理的警报 |
| `shield.case_detail` | 显示事件的详细信息（包括规则和应对方案） |
| `shield.case.resolve` | 解决事件 |
| `shield.cases_ACK` | 标记事件是否已通知用户 |

**事件解决状态**：`true_positive`、`false_positive`、`benign`、`duplicate`
**事件根本原因**：`user_initiated`、`misconfiguration`、`expected_behavior`、`actual_threat`、`testing`、`unknown`

## 数据展示

RPC 响应中包含 `display` 字段，其中包含预格式化的文本。可以直接使用该文本作为响应内容，因为它已经包含了事件的严重性等级、事件 ID、描述和下一步操作建议。如果 `display` 字段缺失，可手动格式化响应内容。

在讨论事件时，提供相应的操作按钮（如解决、误报处理、进一步调查），以便用户能够快速采取行动。

## 卸载插件

要完全卸载 OpenClaw Shield，请按照以下步骤操作：
1. 卸载插件：```
   openclaw plugins uninstall shield
   ```
2. （可选）删除本地数据：```
   rm -rf ~/.openclaw/shield/
   ```
   需要删除的文件包括：`config.json`、`data/event-buffer.jsonl`、`data/redaction-vault.json`、`data/cursor.json`、`data/instance.json`、`logs/shield.log`、`logs/bridge.log`、`state/monitor.json`。

**注意**：删除 `data/redaction-vault.json` 会导致无法恢复已脱敏的数据。请在删除前确认数据保留需求。

**额外说明**：
- OpenClaw Shield 不会影响代理的正常运行或性能。
- UPX 平台使用 80 多条检测规则来分析脱敏后的遥测数据。
- 订阅到期后，系统会自动删除旧事件记录（不会自动排队处理）。如需续订，请访问 [upx.com/en/lp/openclaw-shield-upx](https://www.upx.com/en/lp/openclaw-shield-upx)。