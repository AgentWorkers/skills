---
name: aport-guardrail
description: AI代理的预操作授权机制：在每个工具（如shell命令、消息传递、git操作、MCP、数据导出等）执行之前，系统会验证代理的权限。该机制支持与OpenClaw、IronClaw、PicoClaw配合使用。APort策略引擎能够明确地允许或拒绝代理对各个工具的调用；代理无法绕过这一授权流程。
homepage: https://aport.io
metadata: {"openclaw":{"requires":{"bins":["jq"]}}}
---
# APort Agent Guardrail

**AI代理的预操作授权机制**：每个工具调用在执行前都会被进行检查。该机制支持OpenClaw、IronClaw、PicoClaw以及兼容的框架。只需运行一次安装程序，OpenClaw插件便会自动在每次工具调用时执行相应的策略。您无需手动运行该防护脚本。

**系统要求：** Node.js 18.0及以上版本，以及jq工具。可以通过`npx @aporthq/agent-guardrails`或从仓库中的`./bin/openclaw`命令进行安装。

## 安装

在[aport.io](https://aport.io/builder/create/)创建账户并获取一个托管的Passport（`agent_id`）。**可选**。

**从仓库安装（请先克隆仓库）：** [github.com/aporthq/aport-agent-guardrails](https://github.com/aporthq/aport-agent-guardrails)  
然后从仓库根目录运行`./bin/openclaw`或`./bin/openclaw <agent_id>`。  
详细安装指南：  
- [快速入门：OpenClaw插件](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/QUICKSTART_OPENCLAW_PLUGIN.md)  
- [托管Passport设置](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/HOSTED_PASSPORT_setup.md)  

您可以在`~/.openclaw/aport/passport.json`文件中查看本地Passport的信息（如果使用了不同的配置目录，则为`<config-dir>/aport/passport.json`；旧版本可能使用`<config-dir>/passport.json`）。  

安装过程是交互式的：它会设置您的配置目录和Passport（本地或托管类型），安装APort OpenClaw插件，生成配置文件，并安装相应的封装脚本（wrapper）。安装完成后，无需再进行其他操作——只需启动OpenClaw（或使用已运行的代理服务器），插件会自动在每次工具调用前执行授权检查。

**封装脚本的位置（默认配置目录为`~/.openclaw`）：**  
- `~/.openclaw/.skills/aport-guardrail.sh`（用于本地环境）  
- `~/.openclaw/.skills/aport-guardrail-api.sh`（用于API/托管环境）  
除非进行测试，否则无需手动调用这些脚本。

## 使用方法

**常规使用：** 只需运行一次安装程序，之后无需再进行任何手动操作——插件会自动在每次工具调用前执行授权检查。

**可选（用于测试或其他自动化场景）：**  
- 程序退出代码：  
  - `0`：允许工具继续执行  
  - `1`：拒绝工具执行（具体原因代码请参见`<config-dir>/aport/decision.json`文件）  

**API模式/托管Passport的使用：**  

## 工具名称映射表  
| 操作类型          | 使用的函数                          |
|------------------|--------------------------------------------|  
| 运行Shell命令       | `system_command.execute`                |
| 发送WhatsApp/邮件等     | `messaging.message.send`                   |
| 创建/合并Pull Request   | `git.create_pr`, `git.merge`                   |
| 调用MCP工具       | `mcp.tool.execute`                      |
| 导出数据/文件       | `data.export`                        |

**注意事项：**  
提供的上下文数据必须是有效的JSON格式，例如`{"command":"ls"}`或`{"channel":"whatsapp","to":"1..."}`。

**为何选择这个工具？**  
- **确定性执行**：该机制在每次工具调用前都会被执行，代理无法跳过这一检查步骤。  
- **结构化的策略管理**：基于[Open Agent Passport (OAP) v1.0](https://github.com/aporthq/aport-spec/tree/main)及相应的策略包进行管理。  
- **异常处理机制**：如果防护机制检测到错误，相关工具将被立即阻止。  
- **审计支持**：所有决策记录都会被保存（以本地JSON文件或APort API的形式提供）。  

**扩展建议：**  
可根据需要将该工具与其他威胁检测工具结合使用，通过该防护机制确保不安全的操作无法执行。

**相关文档：**  
- [快速入门：OpenClaw插件](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/QUICKSTART_OPENCLAW_PLUGIN.md)  
- [托管Passport设置](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/HOSTED_PASSPORT_setup.md)  
- **工具与策略映射表](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/TOOL_POLICY_MAPPING.md)  

**更多信息：**  
- [OpenClaw官方文档](https://docs.openclaw.ai/cli/skills)  
- [技能管理相关文档](https://docs.openclaw.ai/tools/skills)  
- [技能配置指南](https://docs.openclaw.ai/tools/skills-config)  
- [ClawHub平台](https://docs.openclaw.ai/tools/clawhub)