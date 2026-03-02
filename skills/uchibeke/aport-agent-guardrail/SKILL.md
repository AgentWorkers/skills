---
name: aport-agent-guardrail
description: AI代理的事前授权机制：在工具执行之前强制执行相关策略，阻止未经授权的命令、数据泄露以及恶意行为。该机制可通过 `before_tool_call` 钩子与 OpenClaw、IronClaw、PicoClaw 等工具协同工作，确保代理无法绕过这些安全策略。此外，还支持可选的 API 模式（通过 `APORT_API_URL`、`APORT_AGENT_ID`、`APORT_API_KEY` 参数进行配置），以支持托管的认证服务及签名验证功能。
homepage: https://aport.io
metadata: {"openclaw":{"requires":{"bins":["jq"]},"envOptional":["APORT_API_URL","APORT_AGENT_ID","APORT_API_KEY"]}}
---
# APort Agent Guardrail

**技能标识符：** `aport-agent-guardrail` · **类别：** 安全 / 基础设施

---

## 🛡️ 该技能的功能

**对AI代理进行预操作授权。** 在执行任何工具调用之前，系统会根据代理的“护照”（包括身份信息、能力限制等）和相应的策略进行评估。如果评估结果为“拒绝”，则该工具将无法运行。

**主要特点：**
- ✅ **确定性执行**：在 `before_tool_call` 钩子中执行授权检查；代理无法绕过此检查
- ✅ **阻止恶意行为**：防止未经授权的命令执行、数据泄露以及API滥用
- ✅ **结构化策略**：基于 [Open Agent Passport (OAP) v1.0](https://github.com/aporthq/aport-spec/tree/main) 标准
- ✅ **默认情况下，失败会导致工具执行失败**：优先考虑安全性而非工具的可用性
- ✅ **审计追踪**：所有决策都会被记录下来，并附有防篡改的哈希值
- ✅ **兼容多种运行时环境**：OpenClaw、IronClaw、PicoClaw等

**它如何保护您：**
- **防止脚本注入**：代理无法绕过基于钩子的授权检查
- **拦截恶意操作**：无论来源如何，所有工具调用都会被监控
- **限制未经授权的命令**：支持允许列表和多种被禁止的命令模式（如 `rm -rf`、`sudo` 等）
- **控制数据泄露**：限制文件访问、消息传递和网络请求
- **防止资源耗尽**：实施速率限制和文件大小限制

**只需安装一次，即可获得永久保护。** 该插件会在每次工具调用时自动运行。

---

## ⚡ 快速入门

```bash
# Install APort guardrails (one-time setup)
npx @aporthq/aport-agent-guardrails

# Follow wizard to create passport and configure policies
# Plugin auto-registers with OpenClaw

# Now your agent is protected
# All tool calls checked before execution
```

**使用托管的护照（可选）：**
```bash
# Get agent_id from aport.io
npx @aporthq/aport-agent-guardrails <agent_id>
```

**系统要求：** Node.js 18.0及以上版本，以及 `jq` 工具

---

## 📦 安装

### 方法 1：使用 npm（推荐）

```bash
npx @aporthq/aport-agent-guardrails
```

**安装过程：**
1. 创建或加载护照文件（可以是本地文件，也可以从 [aport.io](https://aport.io) 获取）
2. 配置代理的能力和限制
3. 自动安装 OpenClaw 插件
4. 设置相应的包装脚本

**安装完成后：** 插件会在每次工具调用前自动执行授权检查。无需额外操作。

### 方法 2：使用托管的护照

```bash
npx @aporthq/aport-agent-guardrails <agent_id>
```

您可以在 [aport.io](https://aport.io/builder/create/) 获取 `agent_id`，以便：
- 获得经过加密签名的授权决策
- 在所有系统上实现全局暂停功能（最长暂停时间 <200 毫秒）
- 查看集中式的审计和合规性报表
- 进行团队协作

### 方法 3：从源代码安装

```bash
git clone https://github.com/aporthq/aport-agent-guardrails
cd aport-agent-guardrails
./bin/openclaw
```

**相关文档：**
- [OpenClaw 插件快速入门](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/QUICKSTART_OPENCLAW_PLUGIN.md)
- [托管护照设置指南](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/HOSTED_PASSPORT_SETUP.md)

---

## 🚀 使用方法

### 自动执行（默认设置）

**安装完成后，插件会自动运行：**

```bash
# Your agent uses tools normally
agent> run git status
# ✅ APort: passport checked → policy evaluated → ALLOW → tool executes

agent> run rm -rf /
# ❌ APort: passport checked → blocked pattern detected → DENY → tool blocked
```

**您无需进行任何操作。** 插件会在后台自动执行每次工具调用时的授权检查。

### 测试安全机制（可选）

**用于测试或自动化的直接脚本调用：**

```bash
# Test allowed command
~/.openclaw/.skills/aport-guardrail.sh system.command.execute '{"command":"ls"}'
# Exit 0 = ALLOW

# Test blocked command
~/.openclaw/.skills/aport-guardrail.sh system.command.execute '{"command":"rm -rf /"}'
# Exit 1 = DENY

# Test messaging
~/.openclaw/.skills/aport-guardrail.sh messaging.message.send '{"channel":"whatsapp","to":"+15551234567"}'
```

**返回的退出码：**
- `0` = 允许执行
- `1` = 拒绝执行（具体原因记录在 `decision.json` 文件中）

**日志记录位置：**
- 最新的授权决策：`~/.openclaw/aport/decision.json`
- 审计记录：`~/.openclaw/aport/audit.log`
- 在 API 模式下，授权决策会通过 APort API 以签名形式返回

---

## 🔍 工作原理

### 预操作授权流程

1. **用户发起请求**（例如：“部署到生产环境”）
2. **代理决定使用某个工具**（例如：通过 `git push` 执行命令）
3. **OpenClaw 触发 `before_tool_call` 钩子**
4. **APort 进行评估：**
   - 加载代理的护照信息（身份、能力、限制等）
   - 将工具与相应的策略进行匹配（使用 `exec.run` 函数）
   - 检查是否在允许列表中，以及是否存在被禁止的命令模式
5. **做出授权决策**：允许或拒绝
6. **记录审计日志**：包含决策时间、策略详情和拒绝原因

**代理无法绕过此授权机制。** 此钩子由 OpenClaw 自动注册，不受用户提示的影响。

### 安装内容

**安装的组件：**
- 在 OpenClaw 配置文件中添加插件，以确保在每次工具调用前执行授权检查
- 在 OpenClaw 启动时加载 TypeScript/JavaScript 插件

**生成的文件（位于 `~/.openclaw/` 目录下）：**
- `config.yaml` 或 `openclaw.json`：插件配置文件
- `.skills/aport-guardrail*.sh`：用于本地或 API 调用的包装脚本
- `aport/passport.json`：代理的护照信息（仅适用于本地模式）
- `aport/decision.json`：最新的授权决策记录
- `aport/audit.log`：审计记录文件

**总磁盘占用量：** 约 100KB（包含脚本和护照数据）

**代码仓库：** [GitHub](https://github.com/aporthq/aport-agent-guardrails)

---

## 🌐 网络与隐私设置

### 本地模式（默认设置）

- **无需网络连接**：所有评估都在本地机器上完成
- **护照信息存储在本地**，确保隐私安全
- **完全离线可用**，适用于开发或个人使用场景

### API 模式（可选）

- **网络请求流程：**
  - 通过 APort API 根据工具名称和上下文信息进行策略评估
  - 如果使用 `agent_id`，则从注册中心获取托管的护照信息
  - 所有的授权决策都会附带加密签名（Ed25519 算法）

**优势：**
- **所有决策都会被加密签名**，确保安全性
- **提供符合法律要求的审计记录**
- **支持全局暂停功能**，可在所有系统上统一应用
- **提供集中式的合规性管理界面**
- **无法篡改本地护照信息**

**API 端点：** `https://api.aport.io`（或通过 `APORT_API_URL` 自定义）

**发送的数据：**
- 工具名称（例如：`system_command.execute`）
- 上下文信息（例如：`{"command": "ls"}`）

**不发送的数据：**
- 文件内容
- 环境变量
- API 密钥或凭证
- 与任务无关的系统信息

**验证方式：** 可以使用本地模式（无需网络连接），或查看源代码以确认实现细节。

---

## ⚙️ 环境变量配置

| 变量          | 使用场景          | 用途                          |
|-----------------|-----------------------------|-----------------------------------------|
| `APORT_API_URL`     | API 模式          | 自定义 API 端点（默认：`https://api.aport.io`）             |
| `APORT_AGENT_ID`     | 托管护照模式        | 从 aport.io 获取的代理 ID                   |
| `APORT_API_KEY`     | 需要身份验证时使用       | 设置在环境变量中（不在配置文件中）                   |

**本地模式：** 不需要设置环境变量。护照信息直接从 `~/.openclaw/aport/passport.json` 读取。

**托管模式：** 在安装过程中提供 `agent_id`，或通过配置文件设置 `APORT_AGENT_ID`。

---

## 🔧 工具与策略的映射关系

| 代理调用方式       | 对应工具名称         | 相关策略                        |
|------------------|------------------|--------------------------------------------|
| Shell 命令         | `system_command.execute`    | 允许执行的命令列表和禁止的命令模式           |
| WhatsApp/Email/Slack      | `messaging.message.send`    | 消息发送的速率限制和接收者列表                |
| 创建/合并 Pull Request | `git.create_pr`, `git.merge`    | Pull Request 的大小和分支限制                |
| MCP 工具         | `mcp.tool.execute`      | 服务器或工具的访问权限设置                   |
| 数据导出         | `data.export`       | 数据导出的规则和 PII（个人身份信息）过滤            |
| 文件读写         | `data.file.read`, `data.file.write` | 文件路径的访问限制                   |
| 网络请求        | `web.fetch`, `web.browser`     | 允许访问的域名和 SSRF（跨站请求伪造）保护           |

**上下文数据格式：** 有效的 JSON 格式，例如：`{"command":"ls"}` 或 `{"channel":"whatsapp","to":"1..."}`

---

## 📋 开箱即用的安全保护机制

**Shell 命令（`system_command.execute.v1`）：**
- 仅允许列表中的命令执行
- 禁止的命令模式包括：`rm -rf`, `sudo`, `chmod 777`, `dd if=`, `mkfs` 等
- 某些解释器可以绕过某些限制（例如：`python -c`, `node -e`, `base64` 编码）

**消息发送（`messaging.message.send.v1`）：**
- 设置消息发送的速率限制（每分钟/每天发送的消息数量）
- 控制消息接收者的列表
- 限制消息发送的渠道

**文件访问（`data.file.read/write.v1`）：**
- 限制文件访问的路径（例如：`/etc`, `/bin`, 系统目录）
- 防止 `.env` 文件和 SSH 密钥被篡改

**网络请求（`web.fetch/browser.v1`）：**
- 控制允许访问的域名
- 提供 SSRF（跨站请求伪造）保护
- 实施速率限制

**Git 操作（`code.repository.merge.v1`）：**
- 限制 Pull Request 的大小
- 约束可以使用的分支
- 需要满足的审核要求

**更多策略详情：** [https://aport.io/policy-packs](https://aport.io/policy-packs)

---

## 🔐 安全模型

### APort 提供的保护措施

- **防止恶意行为：**
  - 通过钩子机制防止脚本注入
  - 阻止恶意第三方工具的运行
  - 禁止未经授权的命令执行
  - 防止通过文件、消息或网络请求进行数据泄露
  - 实施速率和文件大小限制

**信任模型：**

**APort 在应用程序层进行权限控制**（位于代理决策和工具执行之间）。

**您需要信任的组件：**
- 操作系统（确保文件权限设置正确，进程隔离）
- OpenClaw 的运行环境（钩子能够正确执行）
- APort 的源代码（开源，可验证）

**本地模式还额外提供：**
- 确保文件系统的完整性（防止护照文件被篡改）

**API 模式还具备以下优势：**
- 防止本地护照文件被篡改（数据来自外部 API）
- 所有的授权决策都会被加密签名，确保不可篡改

**不在 APort 范围内的安全问题：**
- 文件系统被入侵
- OpenClaw 的安全漏洞
- 网络攻击（如中间人攻击、DNS 欺骗）
- 供应链攻击

**这属于常见的应用程序层授权机制**（类似于 OAuth、IAM 或政策引擎的实现方式）

---

## 🎯 使用场景**

- **防止恶意工具的攻击：** 在添加新工具之前，先安装 APort
- 所有工具的调用都会经过安全检查
- 可以在执行前拦截恶意行为

**合规性和审计：**
- 提供详细的审计记录
- 提供符合法律要求的审计日志（API 模式支持 Ed25519 签名）
- 支持 SOC 2、HIPAA 和 SOX 等安全标准

**团队协作：**
- 所有系统使用相同的护照信息，实现全局权限控制
- 支持集中式的策略更新

**离线环境：**
- 采用本地模式（无需网络连接）
- 所有评估都在本地完成
- 支持自定义的策略配置

## 📚 文档资源**

- **APort Guardrail 相关文档：**
  - [OpenClaw 插件快速入门](https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/QUICKSTART_OPENCLAW_PLUGIN.md)
  - **安全模型与信任机制**：[https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/SECURITY_MODEL.md]
  - **托管护照设置指南**：[https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/HOSTED_PASSPORT_setup.md]
  - **工具与策略的映射关系**：[https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/TOOL_policy_MAPPING.md]
  - **验证方法（本地模式 vs API 模式）**：[https://github.com/aporthq/aport-agent-guardrails/blob/main/docs/VERIFICATION_METHODS.md]

**OpenClaw 相关文档：**
- **CLI 使用指南**：[https://docs.openclaw.ai/cli/skills]
- **技能文档**：[https://docs.openclaw.ai/tools/skills]
- **技能配置指南**：[https://docs.openclaw.ai/tools/skills-config]
- **ClawHub 相关文档**：[https://docs.openclaw.ai/tools/clawhub]

**安全相关文档：**
- [安全配置文件](https://github.com/aporthq/aport-agent-guardrails/blob/main/SECURITY.md)（包含关于脚本注入的防护措施）
- [Open Agent Passport 规范](https://github.com/aporthq/aport-spec/tree/main)（相关技术标准）

## 🤝 支持与社区资源**

- **GitHub 仓库：** [aporthq/aport-agent-guardrails](https://github.com/aporthq/aport-agent-guardrails)
- **官方网站：** [aport.io](https://aport.io)
- **问题反馈：** [GitHub 问题跟踪页](https://github.com/aporthq/aport-agent-guardrails/issues)

**开源许可：** Apache 2.0 许可证
**代码公开：** 所有代码均可公开查看

---

## ❓ 常见问题解答**

**Q：这会降低代理的运行效率吗？**
**A：** 开销非常小。API 模式下的延迟约为 60-100 毫秒；本地模式下的延迟低于 300 毫秒。插件与代理的运行是并行进行的。

**Q：可以在离线环境下使用吗？**
**A：** 可以。本地模式完全不需要网络连接。

**Q：如果需要自定义策略怎么办？**
**A：** API 模式：在请求中传递自定义的策略 JSON 数据；本地模式：修改相应的 Bash 脚本或使用 API 模式。

**Q：如何暂停代理的运行？**
**A：** 本地模式：将代理的状态设置为“暂停”；托管模式：登录 aport.io 并执行暂停操作。

**Q：我的数据会被发送到 APort 服务器吗？**
**A：** 本地模式：不会。API 模式：仅发送工具名称和上下文信息，不会发送任何敏感数据。

**Q：代理可以绕过这个安全机制吗？**
**A：** 无法绕过。授权检查在平台的 `before_tool_call` 钩子中执行，不受用户提示的影响。

**Q：如果 APort 出现故障会怎样？**
**A：** 默认情况下，受影响的工具会被立即阻止。可以通过配置文件中的 `failClosed` 设置来调整这一行为。

---

**由 [APort](https://aport.io) 开发，基于开源技术（[GitHub](https://github.com/aporthq/aport-agent-guardrails) 提供，采用 Apache 2.0 许可证）**