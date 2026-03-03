---
name: manifest
description: >
  **安装并使用 Manifest：**  
  Manifest 是一个开源的 LLM（Large Language Model）路由器和可观测性插件，专为 OpenClaw 设计。当用户需要安装 Manifest、配置成本跟踪、设置 LLM 路由、监控代理成本/令牌使用情况、了解 Manifest 的具体功能、检查插件状态、排查插件故障，或希望降低 OpenClaw 的运行成本时，都可以使用该插件。此外，该插件还会在以下操作发生时被触发：  
  - “设置 Manifest”  
  - “安装 Manifest”  
  - “我的花费是多少？”  
  - “跟踪我的成本”  
  - “路由到更便宜的模型”  
  - “Manifest 控制面板”  
  - “Manifest 帮助文档”
metadata: {"openclaw":{"requires":{"bins":["openclaw"],"credentials":["mnfst_* API key (cloud mode only)"]},"configPaths":["~/.openclaw/openclaw.json","~/.openclaw/manifest/"]}}
---
# Manifest — OpenClaw的LLM路由与可观测性插件

Manifest是一款OpenClaw插件，具备以下功能：

- **通过23维评分算法为每个请求分配最经济的模型**（延迟小于2毫秒）；
- **在实时仪表板上跟踪成本和令牌使用情况**；
- **设置费用限制，并在达到限制时发送电子邮件提醒**。

来源：[github.com/mnfst/manifest](https://github.com/mnfst/manifest) — 使用MIT许可证。官网：[manifest.build](https://manifest.build)

## 设置（云端环境 — 默认配置）

无需编写代码，只需执行三个命令：

```bash
openclaw plugins install manifest
openclaw config set plugins.entries.manifest.config.apiKey "mnfst_YOUR_KEY"
openclaw gateway restart
```

1. 在[app.manifest.build](https://app.manifest.build)获取API密钥；
2. 创建一个账户；
3. 创建一个代理，并复制`mnfst_`密钥。

重启后，插件会自动完成以下配置：
- 将`manifest/auto`设置为默认模型；
- 将`manifest`提供者添加到`~/.openclaw/openclaw.json`配置文件中；
- 开始将OTLP遥测数据导出到`app.manifest.build`；
- 提供三个代理工具：`manifest_usage`、`manifest_costs`、`manifest_health`。

仪表板位于[app.manifest.build](https://app.manifest.build)，遥测数据会在10-30秒内传输到该地址（数据以批量形式发送）。

### 验证连接

```bash
openclaw manifest
```

该插件会显示以下信息：
- 模式（Simple/Standard/Complex/Reasoning）；
- 终端是否可访问；
- 身份验证是否有效；
- 代理名称。

## 设置（本地环境 — 离线模式）

仅在数据必须完全保留在本地机器上的情况下使用本地模式。

```bash
openclaw plugins install manifest
openclaw config set plugins.entries.manifest.config.mode local
openclaw gateway restart
```

仪表板可通过`http://127.0.0.1:2099`访问。数据存储在`~/.openclaw/manifest/manifest.db`文件中，无需账户或API密钥。

若要通过Tailscale平台共享数据（需在两台设备上都安装Tailscale），请执行`tailscale serve --bg 2099`命令。

## Manifest提供的信息

通过仪表板或代理工具，您可以获取关于OpenClaw代理的以下信息：

**费用与预算**
- 今天/本周/本月共花费了多少？
- 各模型的费用分布情况如何？
- 哪个模型占用了最大预算比例？
- 我是否接近费用限制？

**令牌使用情况**
- 代理使用了多少令牌（输入/输出）？
- 令牌使用量与上期相比有何变化？
- 代理读取/写入的缓存数据量是多少？

**活动与性能**
- 代理进行了多少次LLM调用？
- LLM调用的延迟是多少？
- 是否出现错误或速率限制？错误信息是什么？
- 正在运行的技能/工具有哪些，使用频率如何？

**路由策略**
- 每个请求被分配到了哪个路由层级（Simple/Standard/Complex/Reasoning）？
- 选择特定层级的理由是什么？
- 所有提供者提供的模型价格信息有哪些？

**连接状态**
- Manifest是否正常连接？
- 遥测数据是否能够正确传输？

## 代理工具

代理可以通过以下工具获取相关信息：

| 工具                | 触发语句                                      | 返回信息                                                                                   |
| ------------------ | ----------------------------------------------- | --------------------------------------------------------------------------- |
| `manifest_usage`   | "how many tokens", "token usage", "consumption"     | 今日/本周/本月的总令牌数、输入令牌数、输出令牌数、缓存读取令牌数及操作次数 |
| `manifest_costs`   | "how much spent", "costs", "money burned"       | 今日/本周/本月的模型费用明细（以美元计）                                      |
| `manifest_health`    | "is monitoring working", "connectivity test"     | 终端是否可访问、身份验证是否有效、代理名称及状态                                        |

这些工具都接受`period`参数（`today`、`week`或`month`），用于指定查询时间范围。

所有工具均为只读模式，仅查询代理自身的使用数据，不会发送任何消息内容。

## LLM路由策略

当模型设置为`manifest/auto`时，插件会从23个维度对每次对话进行评分，并将其分配到四个层级之一：

| 路由层级              | 使用场景                                      | 示例                                                                                   |
| ------------------ | --------------------------------------- | ------------------------------------------------------- |
| **Simple**           | 问候语、确认信息、简单查询                         | "hi", "yes", "what time is it"                                      |
| **Standard**          | 常规任务、平衡质量和成本                         | "summarize this", "write a test"                                      |
| **Complex**          | 多步骤推理、复杂分析                               | "compare these architectures", "debug this stack trace"                         |
| **Reasoning**         | 形式化逻辑、证明、关键决策                         | "prove this theorem", "design a migration strategy"                         |

每个层级对应特定的模型。默认模型由系统自动分配，但您也可以在仪表板的**Routing**设置中进行更改。

**快捷规则**：
- 如果消息长度小于50个字符且未使用任何工具，则自动分配到**Simple**层级；
- 包含形式化逻辑关键词的消息会自动分配到**Reasoning**层级；
- 如果使用了特定工具，则自动分配到**Standard**层级；
- 如果消息长度超过50,000个令牌，则自动分配到**Complex**层级。

## 仪表板页面

| 页面名称            | 显示内容                                                                                   |
| ------------------ | ----------------------------------------------------------------------------- |
| **工作空间**           | 所有连接的代理以卡片形式显示，附带活动趋势图表                        |
| **概览**           | 显示每个代理的费用、令牌使用情况以及趋势图表                         |
| **消息记录**           | 全部消息记录（可分页查看），支持按状态、模型和费用范围过滤           |
| **路由设置**           | 设置模型路由策略、启用/禁用路由功能                         |
| **费用限制**           | 设置费用限制（每小时/每天/每周/每月的令牌或费用上限）                   |
| **设置**           | 修改代理名称、删除代理、管理OTLP密钥                         |
| **模型价格**           | 显示所有提供者的300多种模型价格（可排序）                         |

**支持的提供者**：
Anthropic、OpenAI、Google Gemini、DeepSeek、xAI、Mistral AI、Qwen、MiniMax、Kimi、Amazon Nova、Z.ai、OpenRouter、Ollama。总计超过300种模型。

## 卸载插件

```bash
openclaw plugins uninstall manifest
openclaw gateway restart
```

卸载插件后会移除插件文件、提供者配置及身份验证信息。卸载后请重新设置默认模型。

## 常见问题解决方法**

- **遥测数据未显示**：gateway每隔10-30秒批量传输OTLP数据。请稍等片刻，然后检查`openclaw manifest`以确认连接状态。
- **云端模式下的身份验证错误**：请确认API密钥以`mnfst_`开头，并与仪表板**Settings → Agent setup**中显示的密钥相匹配。
- **本地模式下的端口冲突**：如果端口2099已被占用，插件会检查是否存在名为Manifest的进程并重新使用该端口。如需更改端口，请执行`openclaw config set plugins.entries.manifest.config.port <PORT>`。
- **插件冲突**：Manifest与内置的`diagnostics-otel`插件可能存在冲突。在启用Manifest之前，请先禁用后者。
- **后端重启后**：务必同时重启gateway（`openclaw gateway restart`），因为OTLP数据传输流程不会自动恢复。

## 隐私政策

**OTLP遥测数据（发送至终端）**：
每次LLM调用会收集以下字段：会话键、代理名称、模型名称、提供者名称、令牌使用量（输入/输出/缓存读取/写入）、工具名称、工具执行结果（成功/失败）、工具执行时间、错误信息（仅保留分类信息，不包含具体内容）、消息通道和服务元数据。

**关于路由策略的注意事项（仅适用于`manifest/auto`模式）**：
当模型设置为`manifest/auto`时，系统会将最近10条非系统消息（包括消息内容）发送到`POST /api/v1/routing/resolve`进行复杂度评分。此操作属于独立的REST请求，不属于OTLP遥测数据的一部分。如需避免发送消息内容，请在仪表板中禁用路由功能并使用固定模型。

**本地模式**：
所有数据仅保存在本地机器上，不会发送任何外部请求。

**产品分析**：
匿名使用数据会发送至PostHog（仅记录哈希后的机器ID，不包含个人身份信息）。如需禁用数据分析，请在`~/.openclaw/manifest/config.json`中设置`MANIFEST_TELEMETRY_OPTOUT=1`或`"telemetryOptOut": true`。