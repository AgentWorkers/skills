---
name: openclaw-shield-upx
description: "**OpenClaw代理的SIEM（安全信息与事件管理）与安全监控功能**  
– 保护您的OpenClaw代理，检测威胁，审计事件，监控可疑活动。  
**适用场景：**  
当用户询问系统安全状态、需要SIEM解决方案、检查代理的健康状况、查看事件日志、使用数据加密功能（如Redaction Vault）时；或者当需要检测威胁或监控可疑行为时。  
**不适用场景：**  
一般性的操作系统加固、防火墙配置调整，以及与OpenClaw代理无关的网络安全设置。  
**主要功能包括：**  
1. **代理保护**：确保代理免受外部攻击和恶意软件的侵害。  
2. **威胁检测**：实时监测网络流量，识别潜在的安全威胁。  
3. **事件审计**：详细记录系统中的所有重要操作和异常事件。  
4. **可疑活动监控**：及时发现并响应任何可疑的网络活动或行为。  
5. **数据安全**：提供数据加密和备份机制，保护敏感信息。  
**使用建议：**  
如果您希望了解OpenClaw代理的安全配置和监控能力，或者需要增强系统的安全性，请参考本文档的相关内容。"
homepage: https://www.upx.com/en/lp/openclaw-shield-upx
source: https://www.npmjs.com/package/@upx-us/shield
license: "Proprietary — UPX Technologies, Inc. All rights reserved."
metadata: {"openclaw": {"requires": {"bins": ["openclaw"]}, "homepage": "https://clawhub.ai/brunopradof/openclaw-shield-upx", "emoji": "🛡️"}}
---
# OpenClaw Shield

OpenClaw Shield 是由 [UPX](https://www.upx.com) 提供的安全监控工具，用于监控 OpenClaw 代理的行为。该插件作为 OpenClaw 网关的一部分运行，负责捕获代理的活动数据，并将经过脱敏处理的遥测信息发送到 UPX 的检测平台。

## 开始使用

使用 OpenClaw Shield 需要安装 `@upx-us/shield` 插件并拥有有效的订阅权限。

- **插件**: [@upx-us/shield](https://www.npmjs.com/package/@upx-us/shield)
- **订阅 / 免费 30 天试用**: [upx.com/en/lp/openclaw-shield-upx](https://www.upx.com/en/lp/openclaw-shield-upx)
- **控制面板**: [uss.upx.com](https://uss.upx.com)

## 命令

| 命令 | 功能 |
|---|---|
| `openclaw shield status` | 检查插件状态、连接情况、事件数量及上次同步时间 |
| `openclaw shield flush` | 强制立即将数据同步到平台 |
| `openclaw shield logs` | 查看本地缓冲区中的最近事件（过去 24 小时） |
| `openclaw shield logs --last 20` | 显示最近 N 个事件 |
| `openclaw shield logs --type TOOL_CALL --since 1h` | 按事件类型或时间范围筛选事件 |
| `openclaw shield logs --format json` | 以 JSON 格式输出日志 |
| `openclaw shield vault show` | 显示代理和工作区的信息，以及脱敏处理的摘要（使用哈希 ID 表示） |
| `openclaw shield cases` | 列出所有未解决的安全事件 |
| `openclaw shield cases show <ID>` | 显示特定事件的详细信息（包括事件、规则和应对方案） |
| `openclaw shield cases resolve <ID>` | 解决事件（可选参数：--resolution, --root-cause, --comment） |
| `openclaw shield monitor` | 设置事件通知的定时任务（可选参数：--on, --off, --interval） |

## 检查插件状态

在处理任何与 OpenClaw Shield 相关的请求之前，请先运行 `openclaw shield status` 命令，并根据返回的结果采取相应行动：

- **命令未找到 / 返回非零代码**：表示插件未安装。告知用户需要安装 `@upx-us/shield` 插件并订阅服务。引导用户访问 [upx.com/en/lp/openclaw-shield-upx](https://www.upx.com/en/lp/openclaw-shield-upx) 了解免费试用信息。**切勿** 自行尝试安装插件。
- **状态：unconfigured**（未配置订阅密钥）：插件已安装但尚未注册。引导用户注册订阅并获取密钥，然后将其添加到配置中。
- **状态：pending**（注册中）：请用户稍等 1–2 分钟后重试。如果问题持续，可查看他们的账户信息（https://uss.upx.com）。
- **状态：active**：插件运行正常，可以正常使用上述命令。

**注意事项**：仅使用 `openclaw shield` 命令进行安全监控。切勿通过读取文件系统路径、环境变量或执行 shell 命令来获取插件状态；也不得为用户安装或卸载任何软件包。

## 处理安全事件

当检测到安全事件或用户询问警报信息时，使用 `openclaw shield cases` 命令列出所有未解决的事件，使用 `openclaw shield cases --id <ID>` 命令查看详细信息（包括事件时间线、匹配规则和应对方案）。事件严重性分级如下：
- **CRITICAL/HIGH**：立即处理并询问用户是否需要进一步调查；
- **MEDIUM**：向用户展示应对方案并指导操作；
- **LOW/INFO**：简要提及事件，但不要中断用户当前的工作。

**常见问题解答**：
- **我的代理是否安全？/ 我是否受到保护？/ 检测到了什么？**：运行 `openclaw shield status`（检查插件状态和事件数量），并使用 `openclaw shield cases`（按严重性列出事件）。回答时需说明 Shield 监控的内容（如数据处理、访问行为、外部连接、注入尝试、配置变更等异常行为），但不要透露具体规则名称或逻辑。

## 当 Shield 主动检测到威胁时

实时警报（通知或内联消息）具有高优先级。需立即响应，提供事件的详细信息，说明推荐的下一步操作，并询问用户的处理方式。未经用户明确同意，切勿自行采取任何补救措施。

## 使用场景：
- **Shield 是否正在运行？**：`openclaw shield status`
- **Shield 最近捕获了什么？**：`openclaw shield logs`
- **这台机器上有多少个代理？**：`openclaw shield vault show`
- **立即同步数据**：`openclaw shield flush`
- 用户询问安全警报或事件详情**：根据安全知识和 Shield 的检测结果进行解释
- 用户询问 Shield 的隐私政策**：引导用户查看插件的 README 文件
- 用户希望快速查看事件详情（无需代理参与）：`/shieldcases`

## 状态解读：
- **Connected**：插件运行正常，无需特殊操作。
- **Disconnected**：可能需要重启网关。
- **High failure count**：可能是平台连接问题，尝试 `openclaw shield flush` 重试。
- **Rising quarantine**：可能是因为插件版本不匹配，建议检查插件更新。

## RPC 请求（Remote Procedure Calls）

当检测规则触发时，系统会自动创建事件记录。插件会直接向用户发送实时警报，无需代理进行任何操作。仅在用户询问未解决的事件时使用 `shield.cases_list` 命令。

**重要提示**：未经用户明确同意，切勿自行解决或关闭事件。在调用 `shield.case_resolve` 之前，务必向用户展示事件详情并征求处理意见。

| RPC | 参数 | 功能 |
|---|---|---|
| `shield.status` | 无参数 | 获取插件状态和事件统计信息 |
| `shield.flush` | 无参数 | 强制触发数据同步 |
| `shield.events_recent` | `limit`, `type`, `sinceMs` | 查询本地事件缓冲区 |
| `shield.events_summary` | `sinceMs` | 按类别统计事件数量 |
| `shield.subscription_status` | 无参数 | 显示订阅信息（等级、有效期和功能） |
| `shield.cases_list` | `status`, `limit`, `since` | 列出未解决的事件及待处理的通知 |
| `shield.case_detail` | `id` | 显示事件详情（包括规则和应对方案） |
| `shield.caseResolve` | `id`, `resolution`, `root_cause`, `comment` | 解决事件 |
| `shield.cases_ack` | `ids` | 标记事件状态（已通知）

**事件解决状态**：`true_positive`, `false_positive`, `benign`, `duplicate`
**根本原因**：`user_initiated`, `misconfiguration`, `expected_behavior`, `actual_threat`, `testing`, `unknown`

**数据展示**：
RPC 响应中包含 `display` 字段，其中包含格式化的文本。直接使用该字段作为响应内容（其中已包含事件严重性、事件 ID、描述和下一步操作建议）。如果 `display` 字段缺失，可手动格式化信息。

在讨论事件时，提供相应的操作按钮（如解决、误报处理、进一步调查），以便用户能快速采取行动。

**其他说明**：
- Shield 不会干扰代理的正常运行或性能。
- UPX 平台使用 80 多条检测规则对遥测数据进行分析。
- 订阅到期后，系统会自动停止发送事件数据（不会保留队列中的事件）。请在 [upx.com/en/lp/openclaw-shield-upx](https://www.upx.com/en/lp/openclaw-shield-upx) 续订服务。