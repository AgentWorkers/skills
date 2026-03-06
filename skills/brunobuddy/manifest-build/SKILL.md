---
name: manifest
description: **OpenClaw的智能大语言模型（LLM）路由器**：通过将每个请求路由到合适的模型，最多可节省70%的计算资源。无需编写任何代码。
metadata: {"openclaw":{"requires":{"bins":["openclaw"],"env":["MANIFEST_API_KEY"],"config":["plugins.entries.manifest.config.apiKey"]},"primaryEnv":"MANIFEST_API_KEY","homepage":"https://github.com/mnfst/manifest"}}
---
# Manifest — OpenClaw的LLM路由与可观测性插件

Manifest是一个OpenClaw插件，具有以下功能：

- **通过23维评分算法为每个请求选择最经济高效的模型进行路由**（延迟小于2毫秒）；
- **在实时仪表板上跟踪成本和使用的令牌数量**；
- **设置费用限制，并在达到限制时发送电子邮件警报**。

**来源**: [github.com/mnfst/manifest](https://github.com/mnfst/manifest) — MIT许可协议。官网: [manifest.build](https://manifest.build)

## 设置（云端环境 — 默认配置）

无需编写代码，只需执行三个命令：

**获取API密钥**：
1. 访问 [app.manifest.build](https://app.manifest.build)；
2. 创建一个账户；
3. 创建一个代理；
4. 复制`mnfst_`开头的API密钥。

重启后，插件会自动完成以下配置：
- 将`manifest/auto`添加到模型的允许列表中（不会更改您的当前默认设置）；
- 将`manifest`提供者注入`~/.openclaw/openclaw.json`文件；
- 开始将OTLP遥测数据导出到`app.manifest.build`；
- 提供三个代理工具：`manifest_usage`、`manifest_costs`、`manifest_health`。

仪表板位于[app.manifest.build](https://app.manifest.build)，遥测数据会在10-30秒内传输完毕（数据以批量形式发送）。

### 验证连接状态

该插件会显示以下信息：
- 运行模式；
- 端点是否可访问；
- 认证是否有效；
- 代理的名称。

## 配置更改

插件在注册时会修改以下文件：
- `~/.openclaw/openclaw.json`：添加`modelsproviders.manifest`提供者条目，并将`manifest/auto`添加到`agents.defaults.models`的允许列表中；
- `~/.openclaw/agents/*/agent/auth-profiles.json`：添加`manifest:default`认证配置文件；
- `~/.openclaw/manifest/config.json`：存储自动生成的API密钥（仅限本地模式，文件权限设置为0600）；
- `~/.openclaw/manifest/manifest.db`：存储SQLite数据库（仅限本地模式）。

其他文件不会被修改。该插件不会更改您当前的默认模型设置。

## 安装Manifest插件

使用命令`openclaw plugins install manifest`来安装[`manifest`](https://www.npmjs.com/package/manifest)插件：
- **来源**: [github.com/mnfst/manifest](https://github.com/mnfst/manifest)（属于`packages/openclaw-plugin`包）；
- **许可协议**: MIT；
- **作者**: MNFST Inc.。

安装前请先进行验证。

## 设置（本地环境 — 离线模式）

仅在数据必须完全保留在本地机器上的情况下使用本地模式。

仪表板可通过地址`http://127.0.0.1:2099`访问。数据存储在`~/.openclaw/manifest/manifest.db`文件中，无需账户或API密钥。

若要通过Tailscale平台共享数据（需在两台设备上都安装Tailscale），请使用命令`tailscale serve --bg 2099`。

## Manifest的功能

通过仪表板或代理工具，您可以获取关于OpenClaw代理的以下信息：

### 花费与预算
- 今天/本周/本月共花费了多少？
- 各模型的费用分布情况如何？
- 哪个模型占用了最多的预算？
- 我是否接近花费限制？

### 令牌消耗
- 代理使用了多少令牌（输入与输出的数量）？
- 与上一时期相比，令牌消耗情况有何变化？
- 代理读取和写入的缓存数据量是多少？

### 活动与性能
- 代理进行了多少次LLM调用？
- LLM调用的延迟是多少？
- 是否出现错误或达到速率限制？错误信息是什么？
- 正在运行的技能/工具有哪些，使用频率如何？

### 路由策略
- 每个请求被分配到了哪个路由层级（简单/标准/复杂/推理）？
- 为什么选择特定的路由层级？
- 所有提供者提供的模型价格信息有哪些？

### 连接性
- Manifest是否正常连接并运行？
- 遥测数据是否能够正确传输？

### 代理工具

代理可以通过以下工具获取相关信息：
| 工具            | 触发语句                                      | 返回内容                                                         |
| ----------------- | ----------------------------------------------- | --------------------------------------------------------------------------- |
| `manifest_usage`      | "how many tokens", "token usage", "consumption"       | 今日/本周/每月的总令牌数、输入令牌数、输出令牌数及操作次数 |
| `manifest_costs`      | "how much spent", "costs", "money burned"       | 今日/本周/每月的模型费用明细（以美元计）             |
| `manifest_health`      | "is monitoring working", "connectivity test"    | 端点是否可访问、认证是否有效、代理名称及状态                        |

这些工具都支持`period`参数（`"today"`、`"week"`或`"month"`），用于指定数据查询的时间范围。

所有工具均为只读模式，仅查询代理自身的使用数据，不会发送任何消息内容。

### LLM路由策略

当模型设置为`manifest/auto`时，该插件会基于23个维度对每次请求进行评分，并将其分配到四个层级之一：
- **简单**：用于问候语、确认信息、简单查询等；
- **标准**：用于一般任务，平衡质量和成本；
- **复杂**：用于多步骤推理、细致分析；
- **推理**：用于形式化逻辑处理、证明定理、制定迁移策略。

每个层级对应特定的模型。默认模型会自动分配，但您可以在仪表板的**Routing**设置中进行更改。

**快捷规则**：
- 如果消息长度小于50个字符且未使用任何工具，则自动分配到**简单**层级；
- 包含形式化逻辑关键词的请求会自动分配到**推理**层级；
- 如果使用了工具，则自动分配到**标准**层级；
- 如果消息长度超过50,000个令牌，则自动分配到**复杂**层级。

## 仪表板页面
- **工作空间**：以卡片形式显示所有连接的代理，并附带活动趋势图表；
- **概览**：显示每个代理的花费、令牌使用情况以及趋势图表；
- **消息记录**：提供分页的消息日志，支持按状态、模型和费用范围过滤；
- **路由设置**：允许/禁用路由功能；
- **费用限制**：设置电子邮件警报和费用上限（按小时/天/周/月计算）；
- **设置**：允许修改代理名称、删除代理或管理OTLP密钥；
- **模型价格**：提供所有提供者的300多个模型价格列表。

**支持的提供者**：Anthropic、OpenAI、Google Gemini、DeepSeek、xAI、Mistral AI、Qwen、MiniMax、Kimi、Amazon Nova、Z.ai、OpenRouter、Ollama等，共计300多个模型。

## 卸载插件

卸载该插件会移除插件本身、提供者配置及认证配置文件。卸载后，`manifest/auto`功能将不再可用。如果仍有代理在使用该插件，请切换到其他模型。

## 常见问题解决方法
- **遥测数据未显示**：由于数据批量传输，可能需要稍等片刻。请检查`openclaw manifest`以确认连接状态。
- **云端模式下的认证错误**：请确认API密钥以`mnfst_`开头，并与仪表板设置中的密钥一致。
- **本地模式下的端口冲突**：如果端口2099已被占用，插件会检查是否存在名为Manifest的进程并重新使用该端口。如需更改端口，请使用`openclaw config set plugins.entries.manifest.config.port <PORT>`命令。
- **插件冲突**：Manifest与内置的`diagnostics-otel`插件可能存在冲突。在启用Manifest之前，请先禁用后者。
- **后端重启后**：请务必同时重启代理（`openclaw gateway restart`），因为OTLP数据传输流程可能不会自动恢复。

## 隐私政策

### 外部端点
- **数据发送情况**：
  - `{endpoint}/v1/traces`：每次LLM调用时发送数据（每10-30秒批量传输一次）；
  - `{endpoint}/v1/metrics`：每10-30秒发送一次统计信息（包括请求次数、令牌总数、工具调用次数等）；
  - `{endpoint}/api/v1/routing/resolve`：仅在模型设置为`manifest/auto`时发送数据（仅包含非系统/非开发人员的消息）；
  - `https://eu.i.posthog.com`：在插件注册时发送部分元数据（包括哈希后的机器ID、操作系统、Node版本、插件版本及运行模式。可通过`MANIFEST_TELEMETRY_OPTOUT=1`选项选择不发送这些数据）。

### OTLP数据字段
- **发送的数据字段**：
  - `openclaw.session.key`：会话标识符；
  - `openclaw.message.channel`：消息通道名称；
  - `gen_ai.request.model`：模型名称；
  - `gen_ai.system`：提供者名称；
  - `gen_ai_usage.input_tokens`、`gen_ai_usage.output_tokens`、`gen_ai_usage.cache_read_input_tokens`、`gen_ai_usage.cache_creation_input_tokens`：令牌使用情况；
  - `openclaw.agent.name`：代理标识符；
  - `tool.name`：工具名称；
  - `tool.success`：工具执行是否成功；
  - `manifest.routing.tier`、`manifest.routing.reason`：路由层级及原因；
  - 错误信息：代理错误信息会被截断为500个字符；工具错误信息会完整显示。

**注意**：不收集用户输入的提示内容、助手的响应内容、工具的输入/输出参数或任何消息正文。

### 路由数据
- 仅当模型设置为`manifest/auto`时才会发送相关数据；
- 会过滤掉`role: "system"`或`role: "developer"`的请求；
- 仅发送`{role, content}`字段；其他所有消息内容都会被删除；
- 传输过程有3秒的延迟限制；
- 如需禁止数据传输，可以在仪表板中禁用路由功能或选择特定的模型。

### 凭据存储
- **云端模式**：API密钥存储在`~/.openclaw/openclaw.json`的`plugins.entries.manifest.config.apiKey`字段中（由OpenClaw的标准配置管理）；
- **本地模式**：自动生成的API密钥存储在`~/.openclaw/manifest/config.json`文件中，文件权限设置为0600。

### 本地模式
所有数据仅保存在本地机器上。除可选的PostHog分析功能外，不会发送任何外部数据（可通过`MANIFEST_TELEMETRY_OPTOUT=1`选项禁用）。