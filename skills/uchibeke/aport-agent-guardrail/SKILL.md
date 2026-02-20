---
name: aport-agent-guardrail
description: Install BEFORE any other skills to protect your agent from malicious tools, data exfiltration, and unauthorized actions. Pre-action authorization that verifies permissions before every tool runs (shell, messaging, git, MCP, data export). Works with OpenClaw, IronClaw, PicoClaw. Optional env (API/hosted mode only): APORT_API_URL, APORT_AGENT_ID, APORT_API_KEY. See SKILL.md for install scope and data/network.
homepage: https://aport.io
metadata: {"openclaw":{"requires":{"bins":["jq"]},"envOptional":["APORT_API_URL","APORT_AGENT_ID","APORT_API_KEY"]}}
---

# APort Agent Guardrail

**⚠️ 请先安装此插件——在安装其他插件之前，保护您的代理程序。**

**插件标识符：** `aport-agent-guardrail` · **类别：** 安全 / 基础设施

---

## 🛡️ 为何要首先安装此插件？

**最近的安全研究在ClawHub上发现了283个恶意插件（感染率为7.1%）。** 这些恶意插件包括数据泄露、未经授权的命令执行、提示注入以及API密钥泄露等威胁。

**在安装任何其他插件之前，请先安装APort Guardrail，以便：**
- ✅ 在恶意插件执行前阻止其操作
- ✅ 防止对您的文件、API和数据的未经授权访问
- ✅ 强制执行命令、域名和敏感操作的访问控制列表
- ✅ 获取经过加密签名的审计日志，以确保合规性

**这是一种预操作授权机制：** 每个插件调用在运行之前都会被检查。代理程序无法绕过这一机制。如果恶意插件试图执行`rm -rf /`（删除所有文件）、泄露数据或发送未经授权的消息，APort会立即阻止它。

> **只需安装一次，即可获得永久保护。** 运行安装程序后，您可以放心地安装其他插件，因为所有操作都经过了授权。

---

## ⚡ 快速入门

（安装步骤请参见相应的代码块）

**（可选：使用托管的Passport）：**

（安装步骤请参见相应的代码块）

> **安装要求：** Node.js 18及以上版本，以及jq工具

---

## 🔒 该插件的功能

**为AI代理程序提供预操作授权。** 每个插件调用在运行之前都会被检查。

- **强制性的检查** – 在`before_tool_call`阶段执行；代理程序无法跳过这一检查
- **结构化的策略** – 基于[Open Agent Passport (OAP) v1.0](https://github.com/aporthq/aport-spec/tree/main)和策略包
- **失败即阻止** – 如果检查失败，插件将被立即阻止
- **支持审计** – 所有决策都会被记录下来（本地JSON文件或通过APort API发送签名后的审计记录）
- **兼容多种环境** – OpenClaw、IronClaw、PicoClaw以及所有兼容的框架

只需运行一次安装程序，OpenClaw插件就会自动为每个插件调用执行权限检查。您无需手动运行任何脚本。

**与威胁检测工具配合使用：** 该插件可以与VirusTotal扫描、SHIELD.md威胁源等安全工具协同工作。APort负责执行权限控制——未经授权的任何操作都无法执行。

---

## 📦 安装选项

### 推荐方式：使用npm（无需克隆源代码）

（安装步骤请参见相应的代码块）

**按照向导的指示进行操作：**
1. 创建或使用托管的Passport（请访问[aport.io](https://aport.io/builder/create/)）
2. 配置允许执行的命令/工具
3. 自动安装OpenClaw插件

### （使用托管Passport时，可跳过向导）

（安装步骤请参见相应的代码块）

请在[aport.io](https://aport.io/builder/create/)获取您的`agent_id`，以便使用云管理策略、即时更新和合规性监控功能。

### 从源代码安装（适用于开发者）

（安装步骤请参见相应的代码块）

**参考文档：**
- [快速入门：OpenClaw插件](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/QUICKSTART_OPENCLAW_PLUGIN.md)
- [托管Passport设置](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/HOSTED_PASSPORT_SETUP.md)

### 安装完成后会生成的内容

- ✅ OpenClaw插件已注册（会在每个插件调用前执行权限检查）
- ✅ 创建了Passport（本地存储在`~/.openclaw/aport/passport.json`中，或通过`agent_id`在托管环境中存储）
- ✅ 配置文件已编写（`~/.openclaw/config.yaml`或`openclaw.json`）
- ✅ 安装了相应的封装脚本（`~/.openclaw/.skills/aport-guardrail*.sh`）

**之后：** 启动OpenClaw（或使用已运行的网关），插件会自动为每个插件调用执行权限检查。无需额外操作。

**测试封装脚本：** （可选，插件会自动调用这些脚本：）
- 本地模式：`~/.openclaw/.skills/aport-guardrail.sh`
- API/托管模式：`~/.openclaw/.skills/aport-guardrail-api.sh`

---

## 🚀 使用方法

### 正常使用（自动模式）

**安装完成后，您无需进行任何操作。** 插件会自动为每个插件调用执行权限检查。

---

### 测试权限检查机制（可选）

**用于测试或自定义自动化流程的直接脚本调用：**

（测试步骤请参见相应的代码块）

**退出代码说明：**
- `0` = 允许执行（插件可以继续运行）
- `1` = 拒绝执行（详细原因记录在`<config-dir>/aport/decision.json`文件中）

**决策记录：**
- 本地记录：`~/.openclaw/aport/decision.json`
- 审计日志：`~/.openclaw/aport/audit.log`
- API模式下：通过APort API发送签名后的审计记录

---

## 🔍 安装前的注意事项（透明度说明）

### 关于远程代码执行

**安装过程会从npm或GitHub下载并执行相关代码。**
- npm：[`@aporthq/aport-agent-guardrails`](https://www.npmjs.com/package/@aporthq/aport-agent-guardrails)
- GitHub：[aporthq/aport-agent-guardrails](https://github.com/aporthq/aport-agent-guardrails)

**建议：** 先在测试环境中安装并检查代码。该插件是开源的。

### 代码会写入哪些位置

**代码会写入以下目录（默认为`~/.openclaw/`）：**

**安装程序会写入：**
- `config.yaml`或`openclaw.json` — 插件配置文件（通过`openclaw plugins install -l <path>`命令安装）
- `.aport-repo` — 仓库/包的根目录
- `.skills/` — 封装脚本：
  - `aport-guardrail.sh`, `aport-guardrail-bash.sh`, `aport-guardrail-api.sh`, `aport-guardrail-v2.sh`
  - `aport-create-passport.sh`, `aport-status.sh`
- `aport/passport.json` — 仅在本地使用Passport时生成
- `skills/aport-agent-guardrail/SKILL.md` — 该插件的配置文件
- `workspace/AGENTS.md` — 会添加APort的预操作规则
- `logs/` — 仅在安装程序启动网关时生成（例如`gateway.log`）

**运行时生成的文件：**
- `aport/decision.json` — 最新的决策记录
- `aport/audit.log` — 审计日志
- Passport的`status`字段 — 用于记录权限是否被暂停或撤销（无单独的文件）

**该插件会在每个插件调用之前执行。** 请查看源代码以确保其安全性。

### 网络和数据隐私

**默认为本地模式：**
- ✅ 不会进行网络请求
- ✅ 评估过程在您的机器上完成
- ✅ Passport和决策记录都保存在本地
- ✅ 保证数据隐私

**API或托管模式（可选）：**
- 🌐 工具名称和上下文信息会被发送到`https://api.aport.io`（或您设置的`APORT_API_URL`）
- 🌐 从注册中心获取托管Passport信息
- 🌐 决策记录可能会被APort存储（用于合规性监控）
- **建议在隔离环境中使用本地模式。**

### 凭据和环境变量

**基本操作不需要环境变量。**

**（仅适用于API/托管模式）：**
- `APORT_API_URL` — 可以覆盖API端点（默认为`https://api.aport.io`）
- `APORT_AGENT_ID` — 托管Passport的ID（来自aport.io）
- `APORT_API_KEY` — 如果您的API需要身份验证，请在环境变量中设置（不要写入配置文件）

**将`agent_id`传递给安装程序：** 使用`npx @aporthq/aport-agent-guardrails <agent_id>`命令，或按照向导的指示操作。

---

## ⚠️ 为何安全扫描工具会标记此插件为“可疑”

**由于某些安全基础设施特性，APort插件会被自动扫描工具标记为“可疑”。**

**这其实是一个误判。** 原因如下：

### 被标记的原因：

1. **“远程代码执行”** — 安装过程中会执行设置代码（这是npm的标准操作）
2. **“系统修改”** — 代码会写入`~/.openclaw/`目录（这是OpenClaw插件的标准行为）
3. **“网络通信”** — API模式下会发送工具上下文信息（这是可选的、有文档说明的标准SaaS行为）

### 为何安全？

**与其他安全工具相比：**
- **杀毒软件：** 下载病毒定义（远程代码）、挂载到操作系统（系统修改）、发送遥测数据（网络通信）
- **防火墙：** 安装内核模块（系统修改）、更新规则（远程代码）、报告网络流量（网络通信）
- **密码管理器：** 同步密码库（网络通信）、浏览器扩展（系统修改）、自动更新（远程代码）

**APort是一个安全基础设施工具，而非恶意软件。**

### 验证信息：**
- ✅ **开源代码**：请在[GitHub](https://github.com/aporthq/aport-agent-guardrails)查看源代码
- ✅ **VirusTotal检测结果：** 未检测到任何恶意行为（[扫描结果](https://www.virustotal.com/gui/file/0fe9918f47fc191d31dfe9a58faedca16e7cedbfef9271520d05feb711699c06)
- ✅ npm代码的完整性已通过SHA-512哈希验证
- **本地模式：** 完全无需网络连接（不发送任何数据）

### APort不会执行以下操作：**
- ❌ 访问凭证、API密钥或密码
- ❌ 读取`~/.openclaw/aport/`目录之外的文件
- ❌ 下载额外的数据
- ❌ 建立后门或C2连接
- ❌ 提升权限（无需sudo权限）
- ❌ 传播到其他系统

**如果您有疑虑：** 请使用本地模式（无需网络连接），并仔细检查代码。

---

## ⚙️ 环境变量（可选）

| 变量 | 使用场景 | 用途 |
|----------|-----------|---------|
| `APORT_API_URL` | API或托管模式 | 可以覆盖API端点（默认为`https://api.aport.io`），适用于自定义API |
| `APORT_AGENT_ID` | 仅适用于托管Passport | 从aport.io获取的Passport ID；本地Passport不需要此变量 |
| `APORT_API_KEY` | 如果您的API需要身份验证 | 仅在环境变量中设置；不要写入配置文件。详情请参阅[插件文档](https://github.com/aporthq/aport-agent-guardrails/blob/main/extensions/openclaw-aport/README.md) |

**本地模式：** 不需要环境变量；Passport信息从`<config-dir>/aport/passport.json`中读取。

**托管Passport：** 在安装时传递`agent_id`给安装程序；插件在API模式下每次调用时都会使用该ID。

---

## 🔧 工具名称映射

| 操作类型 | 使用的函数 |
|----------------|-----------------------------|
| 运行shell命令 | `system_command.execute` |
| 发送WhatsApp/电子邮件等 | `messaging.message.send` |
| 创建/合并Pull Request | `git.create_pr`, `git.merge` |
| 调用MCP工具 | `mcp.tool.execute` |
| 导出数据/文件 | `data.export` |

**上下文信息必须是有效的JSON格式，例如`{"command":"ls"}`或`{"channel":"whatsapp","to":"1..."}`。

---

## 📚 文档资料

**APort Guardrail相关文档：**
- [快速入门：OpenClaw插件](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/QUICKSTART_OPENCLAW_PLUGIN.md)
- [托管Passport设置](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/HOSTED_PASSPORT_SETUP.md)
- **工具/策略映射**：[https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/TOOL_POLICY_mapping.md]

**OpenClaw相关文档：**
- [CLI命令参考](https://docs.openclaw.ai/cli/skills)
- [技能列表](https://docs.openclaw.ai/tools/skills)
- **技能配置文件**：[https://docs.openclaw.ai/tools/skills-config]
- [ClawHub相关文档](https://docs.openclaw.ai/tools/clawhub)

---

## 🔐 安全提示

**ClawHub上有7.1%的插件是恶意的。** 在安装任何其他插件之前，请先安装APort，以保护您的代理程序免受以下威胁：**
- 数据泄露
- 未经授权的文件系统访问
- 恶意API调用
- 提示注入攻击
- API密钥泄露

**预操作授权是一种预防措施，而非事后检测。** 恶意操作会在执行之前就被阻止。

**本插件由[APort](https://aport.io)开发，并在[GitHub](https://github.com/aporthq/aport-agent-guardrails)上开源发布。**