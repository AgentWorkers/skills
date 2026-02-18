---
name: aport-agent-guardrail
description: Pre-action authorization for AI agents. Verifies permissions before every tool runs (shell, messaging, git, MCP, data export). Works with OpenClaw, IronClaw, PicoClaw. Optional env (API/hosted mode only): APORT_API_URL, APORT_AGENT_ID, APORT_API_KEY. See SKILL.md for install scope and data/network.
homepage: https://aport.io
metadata: {"openclaw":{"requires":{"bins":["jq"]},"envOptional":["APORT_API_URL","APORT_AGENT_ID","APORT_API_KEY"]}}
---

# APort Agent Guardrail

**技能标识符（slug）：** `aport-agent-guardrail` · **产品名称：** APort Agent Guardrail。

**AI代理的预操作授权**：每个工具调用在运行之前都会被检查。该功能支持OpenClaw、IronClaw、PicoClaw以及兼容的框架。只需运行一次安装程序，OpenClaw插件便会自动在每次工具调用时执行相应的策略。您无需手动运行Guardrail脚本。

**安装要求：** 需要Node.js 18及以上版本以及jq工具。可以通过`npx @aporthq/agent-guardrails`或从仓库中的`./bin/openclaw`命令进行安装。

## 为什么选择这个技能？

- **确定性**：Guardrail在每次工具调用之前执行，代理无法跳过这一检查。
- **结构化的策略**：基于[Open Agent Passport (OAP) v1.0](https://github.com/aporthq/aport-spec/tree/main)及相应的策略包。
- **故障处理机制**：如果Guardrail检测到错误，相关工具将被阻止。
- **审计支持**：所有决策都会被记录下来（以本地JSON文件或通过APort API的形式提供签名收据）。

**使用建议：** 如有需要，可以将该技能与其他威胁检测工具结合使用，确保任何不安全的操作都无法执行。

## 安装步骤

```bash
# Recommended (no clone needed)
npx @aporthq/agent-guardrails

# Hosted passport: skip the wizard by passing agent_id from aport.io
npx @aporthq/agent-guardrails <agent_id>
```

- **使用托管的Passport（可选）：** 在[aport.io](https://aport.io/builder/create/)获取`agent_id`，并将其传递给安装程序或在安装向导中使用。
- **从仓库安装：** 克隆[aporthq/aport-agent-guardrails](https://github.com/aporthq/aport-agent-guardrails)仓库，然后从仓库根目录运行`./bin/openclaw`或`./bin/openclaw <agent_id>`。相关指南请参见：[QuickStart: OpenClaw Plugin](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/QUICKSTART_OPENCLAW_PLUGIN.md)和[Hosted Passport Setup](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/HOSTED_PASSPORT_SETUP.md)。
- **本地Passport路径：** `~/.openclaw/aport/passport.json`（或`<config-dir>/aport/passport.json`；旧版本使用`<config-dir>/passport.json`）。
- **安装完成后：** 安装程序会设置配置目录、Passport（无论是本地的还是托管的）、插件以及相关配置文件。之后只需启动OpenClaw（或使用已运行的网关），插件会自动在每次工具调用前执行检查。

**包装脚本（仅用于测试；插件会自动调用它们）：** `~/.openclaw/.skills/aport-guardrail.sh`（本地模式），`~/.openclaw/.skills/aport-guardrail-api.sh`（API/托管模式）。

## 使用方法

- **常规使用：** 只需运行一次安装程序，插件会自动在每次工具调用前执行检查。无需手动操作。
- **直接调用脚本（用于测试或其他自动化场景）：**

```bash
~/.openclaw/.skills/aport-guardrail.sh system.command.execute '{"command":"ls"}'
~/.openclaw/.skills/aport-guardrail.sh messaging.message.send '{"channel":"whatsapp","to":"+15551234567"}'
```

- **退出代码说明：**
  - 0：允许工具继续执行
  - 1：拒绝执行；具体原因代码存储在`<config-dir>/aport/decision.json`中。
- **API或托管模式：**

```bash
APORT_API_URL=https://api.aport.io ~/.openclaw/.skills/aport-guardrail-api.sh system.command.execute '{"command":"ls"}'
```

## 安装前的注意事项

- **安装过程：** 安装程序会从npm（`npx @aporthq/agent-guardrails`）或克隆的仓库（`./bin/openclaw`）中加载并执行相关代码。
- **验证软件包：** 可在[npm](https://www.npmjs.com/package/@aporthq/agent-guardrails)和[GitHub](https://github.com/aporthq/aport-agent-guardrails)页面查看详细信息。
- **建议在测试环境中先运行安装程序进行验证。**
- **安装过程中会生成以下文件（默认存储在`~/.openclaw`目录下）：**
  - **安装程序：**
    - 通过`openclaw plugins install -l <path>`将APort插件注册到OpenClaw；插件代码保留在包或仓库中，OpenClaw仅存储链接。
    - `config.yaml`：包含插件配置；如果存在`openclaw.json`文件，插件配置会与其合并。
    - `.aport-repo`：包含仓库/包的根路径。
    - `./skills/`目录下的包装脚本（用于执行`bin/`目录下的脚本）：
      - `aport-guardrail.sh`、`aport-guardrail-bash.sh`、`aport-guardrail-api.sh`、`aport-guardrail-v2.sh`
      - `aport-create-passport.sh`、`aport-status.sh`
    - `aport/passport.json`：仅在选择本地Passport时生成；安装程序会更新`allowed_commands`文件。
    - `skills/aport-guardrail/SKILL.md`：此技能的配置文件。
    - `workspace/AGENTS.md`：包含APort的预操作规则。
    - `logs/`：仅在安装程序启动网关时生成（例如`gateway.log`文件）。
  - **运行时文件：**
    - `aport/decision.json`：存储决策结果。
    - `aport/audit.log`：记录审计信息。
    - `aport/kill-switch`（如使用）：用于控制程序的停止。
- **代码说明：** 插件在每次工具调用之前都会执行检查；请务必仔细审查代码库和npm包中的代码。
- **网络与数据传输：**
  - **本地模式**：所有操作都在本地机器上完成，无需网络连接；Passport和决策记录也保存在本地（`aport/passport.json`、`aport/decision.json`）。
  - **API或托管模式**：工具名称和上下文信息会发送到API（默认为`https://api.aport.io`或您自定义的`APORT_API_URL`）。
  - 在使用托管Passport时，API会从注册表中获取Passport信息。
  - 如果不希望数据被传输到外部服务器，建议使用本地模式。
- **认证信息：** 运行此技能不需要任何环境变量。
  - （仅限API/托管模式）：`APORT_API_URL`、`APORT_AGENT_ID`、`APORT_API_KEY`。
  - `agent_id`可以通过`npx @aporthq/agent-guardrails <agent_id>`传递给安装程序，或在配置文件中设置；对于本地Passport来说，这个参数是可选的。

## 环境变量（可选）

| 变量        | 使用场景       | 作用                         |
|------------|-----------------------------|
| APORT_API_URL    | API或托管模式       | 用于覆盖API端点（默认为`https://api.aport.io`）。适用于自定义API。 |
| APORT_AGENT_ID   | 仅适用于托管Passport模式 | 从aport.io获取的Passport ID；API会从注册表中获取该ID。本地Passport模式下无需设置。 |
| APORT_API_KEY    | 如果API需要认证     | 仅在环境变量中设置；切勿将其放入配置文件中。详情请参阅[插件README](https://github.com/aporthq/aport-agent-guardrails/blob/main/extensions/openclaw-aport/README.md)。 |

- **本地模式**：无需环境变量；Passport信息从`<config-dir>/aport/passport.json`中读取。
- **托管Passport模式**：在安装过程中一次性传递`agent_id`给安装程序；插件在API模式下每次调用时都会使用该ID。

## 工具名称映射

| 执行操作        | 对应的工具名称                |
|------------------|-----------------------------|
| 运行shell命令    | `system_command.execute`            |
| 发送WhatsApp/电子邮件等   | `messaging.message.send`            |
| 创建/合并Pull Request | `git.create_pr`、`git.merge`           |
| 调用MCP工具     | `mcp.tool.execute`                |
| 导出数据/文件     | `data.export`                    |

- 上下文数据必须是有效的JSON格式，例如`{"command":"ls"}`或`{"channel":"whatsapp","to":"1..."}`。

## 文档资源**

- **相关文档：** 
  - [QuickStart: OpenClaw Plugin](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/QUICKSTART_OPENCLAW_PLUGIN.md)
  - [Hosted Passport设置](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/HOSTED_PASSPORT_setup.md)
  - **工具/策略映射文档**：[TOOL_POLICY_MAPPING.md](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/TOOL_POLICY_MAPPING.md)
- **OpenClaw文档：** 
  - [CLI相关文档](https://docs.openclaw.ai/cli/skills)
  - [技能管理文档](https://docs.openclaw.ai/tools/skills)
  - [ClawHub文档](https://docs.openclaw.ai/tools/clawhub)