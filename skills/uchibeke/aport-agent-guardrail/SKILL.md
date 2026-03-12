---
name: aport-agent-guardrail
description: AI代理的预操作授权机制：在工具调用（tool_call）之前，系统会安装一个名为OpenClaw的插件，并通过`before_tool_call`钩子来检查每次工具调用的合法性。该机制会依据预设的“护照”（passport）和策略（policy）来验证操作，确保只有符合要求的命令才能被执行。该系统能够阻止未经授权的命令执行、数据泄露以及策略违规行为。同时支持本地（离线）和托管（API）两种“护照”管理模式。系统运行需要Node.js 18及以上版本以及npx工具。
metadata:
  author: uchibeke
  version: 1.1.11
  tags: security, guardrails, authorization, ai-agent, openclaw, aport, policy-enforcement
---
# APort Agent Guardrail

这是一个用于为AI代理提供预操作授权的解决方案。它会在调用任何工具之前，通过OpenClaw的`before_tool_call`钩子对代理的身份信息（包括权限和限制）以及相关策略进行验证。如果策略拒绝该请求，工具将不会被执行。

本文档提供了该解决方案的配置指南。具体的执行逻辑来自开源的[npm包@aporthq/aport-agent-guardrails](https://github.com/aporthq/aport-agent-guardrails)，遵循Apache 2.0许可证，允许在安装前进行审计。

## 适用场景

- 用户希望为他们的AI代理设置安全防护机制。
- 用户希望防止未经授权的工具调用。
- 用户需要对OpenClaw、IronClaw或PicoClaw代理实施预操作授权。
- 用户需要记录AI代理的操作日志以供审计。

## 工作原理

1. 代理决定使用某个工具（例如运行shell命令）。
2. OpenClaw触发`before_tool_call`钩子。
3. APort加载代理的身份信息（passport），将其与相应的策略进行匹配，并检查允许的操作和限制。
4. 根据策略判断是否允许该工具执行（允许或拒绝）。
5. 执行结果会被记录到审计日志中。

该安全机制在OpenClaw的钩子层中实现，而不是在代理的交互界面中。然而，像所有应用程序层的安全控制一样，其有效性依赖于运行时环境（操作系统、OpenClaw以及文件系统的完整性）。详细的安全模型请参阅[Security Model](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/SECURITY_MODEL.md)。

## 先决条件

在开始安装之前，请确保满足以下要求：
- **Node.js 18.0或更高版本**以及`npx`工具（运行`node -v`可确认版本）。
- **OpenClaw**或兼容的运行环境（该插件需要作为OpenClaw的插件进行注册）。

## 安装流程

### 快速安装（推荐）

安装过程会自动完成以下步骤：
- 创建或加载代理的身份信息文件（本地文件或从aport.io获取）。
- 配置代理的权限和限制。
- 注册OpenClaw插件（该插件会添加`before_tool_call`钩子）。
- 在`~/.openclaw/`目录下生成相应的包装脚本。

安装完成后，每次调用工具时，该钩子都会自动执行。

### 使用托管的身份信息文件（可选）

您可以在[aport.io](https://aport.io/builder/create/)获取代理ID，以实现签名决策、全局操作暂停以及集中式审计功能。

### 从源代码安装

如果您希望自定义配置，可以参考[源代码文档](https://github.com/aporthq/aport-agent-guardrails)。

## 安装后效果

安装完成后，每次调用工具时，`before_tool_call`钩子都会自动执行相应的安全检查。

### 手动测试钩子功能

您可以参考[相关文档](...)来手动测试钩子的功能。

## 各种运行模式

- **本地模式**（默认）：所有验证都在本地完成，不涉及网络请求。代理的身份信息文件存储在`~/.openclaw/aport/passport.json`中，支持离线使用。注意：需要保护本地文件不被篡改。
- **API模式**（可选）：代理的身份信息存储在aport.io的注册服务中，支持签名验证（使用Ed25519算法），提供全局操作暂停功能以及集中式合规性监控。该模式会向API发送工具名称和上下文信息，但不会传输文件内容、环境变量或凭据。

## 环境变量

以下环境变量为可选配置：
- `APORT_API_URL`（API模式）：用于指定API的地址（默认值：`https://api.aport.io`）。
- `APORT_AGENT_ID`（托管身份信息模式）：从aport.io获取的代理ID。
- `APORT_API_KEY`（API模式）：用于API认证的密钥。

## 默认的安全保护规则：

- **Shell命令**：基于允许列表进行控制，禁止某些命令（如`rm -rf`、`sudo`、`chmod 777`等），并检测是否尝试绕过解释器安全机制。
- **消息传递**：限制发送消息的频率和接收者范围。
- **文件访问**：限制文件访问路径，禁止访问`.env`文件和系统目录。
- **Web请求**：控制域名访问、防止SSRF攻击，并限制请求频率。
- **Git操作**：限制Pull Request的大小和分支操作。

## 工具与策略的映射关系

不同的代理操作对应不同的工具名称和策略检查规则，具体如下：

| 代理操作          | 工具名称                | 策略检查项                          |
|------------------|------------------|---------------------------------------------|
| Shell命令            | `system_command.execute`       | 允许的操作列表、禁止的命令模式                |
| 消息传递（WhatsApp/Email/Slack） | `messaging.message.send`     | 发送消息的频率和接收者范围                |
| Pull Request        | `git.create_pr`、`git.merge`       | Pull Request的大小和分支限制                |
| MCP工具            | `mcp.tool.execute`       | 服务器或工具的访问权限                    |
| 文件读写            | `data.file.read`、`data.file.write`    | 文件访问路径                        |
| Web请求            | `web.fetch`、`web.browser`       | 访问的域名范围                        |

## 常见问题及解决方法

- 如果插件未生效，请检查`openclaw plugin list`中是否包含`aport-guardrail`插件。
- 如果在API模式下连接失败，请确认`APORT_API_URL`是否可访问。
- 如果工具被意外阻止，请查看`~/.openclaw/aport/decision.json`文件以获取拒绝原因。
- 如果无法找到`npx`，请安装Node.js 18.0或更高版本（安装地址：https://nodejs.org）。

## 相关文档

- [源代码](https://github.com/aporthq/aport-agent-guardrails)（Apache 2.0许可证）
- [快速安装指南](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/QUICKSTART_OPENCLAW_PLUGIN.md)
- [安全模型与信任边界](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/SECURITY_MODEL.md)
- [托管身份信息文件的设置指南](https://github.com/aport-q/aport-agent-guardrails/blob/main/docs/HOSTED_PASSPORT_SETUP.md)
- [OAP规范](https://github.com/aporthq/aport-spec/tree/main)