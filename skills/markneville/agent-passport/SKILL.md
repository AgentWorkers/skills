---
name: agent-passport-lite
description: "**面向代理时代的OAuth机制**——为所有敏感的代理操作（包括购买、发送邮件、文件操作、系统命令以及API调用）实施权限控制。该机制支持设置消费限额、速率限制、允许操作列表、操作有效期（TTL），同时提供审计追踪功能以及“了解你的代理”（KYA, Know Your Agent）元数据支持。"
metadata: {"openclaw":{"requires":{"bins":["jq","bc","xxd","head","date","mkdir"],"env":["AGENT_PASSPORT_LEDGER_DIR"]}}}
user-invocable: true
---

# Agent Passport Lite (OpenClaw)

## 30秒快速设置

```bash
# Initialize and register your agent
./mandate-ledger.sh init agent:my-assistant "Your Name" "personal assistant" "openclaw"

# Grant dev tool access (git, npm, docker, etc.)
./mandate-ledger.sh create-from-template dev-tools

# That's it! The agent will now check permissions before sensitive actions.
```

> 可用的模板：`dev-tools` · `email-team <domain>` · `file-ops <path>` · `web-research`
> 运行 `./mandate-ledger.sh templates` 查看所有选项。

---

## ⚡ 代理行为契约

**如果你是正在阅读此文档的代理，请遵守以下规则。**

### 何时需要检查

在执行任何操作之前，你必须先调用 `check-action`：

| 操作 | 类别 | 示例目标 |
|--------|----------|----------------|
| 运行 shell 命令 | `system` | `"git pull"`、`npm install"` |
| 发送消息/电子邮件 | `communication` | `"bob@company.com"` |
| 写入/删除文件 | `data` | `"/path/to/file.txt"` |
| 进行带有副作用的 API 调用 | `external_api` | `"api.github.com"` |
| 花费金钱 | `financial` | `"merchant_amazon"` 以及花费金额 |
| 以用户身份公开行动 | `identity` | `"twitter_post"` |

**无需检查的情况**：读取文件、进行网络搜索、内部推理或任何没有副作用的操作。

### 如何检查

```bash
SCRIPT_DIR="$HOME/.openclaw/skills/agent-passport-lite/scripts"

result=$($SCRIPT_DIR/mandate-ledger.sh check-action "<your_agent_id>" "<category>" "<target>" [amount])
```

解析检查结果：
- `authorized: true` → 继续执行操作，并在之后记录该操作
- `authorized: false` → **停止操作，并询问用户。**

### 操作流程

```
1. You want to do something sensitive
2. Call check-action
3. IF authorized:
   a. Do the thing
   b. Log it: mandate-ledger.sh log-action <mandate_id> <amount> "<description>"
4. IF denied:
   a. Tell the user what you want to do and why
   b. Suggest a mandate (show scope, duration, constraints)
   c. Wait for approval
   d. If approved, create the mandate, then proceed
```

### 如何请求权限

当权限被拒绝时，需要清晰、简洁地告知用户原因：

```
I need to [ACTION] but don't have a mandate for it.

📋 [CATEGORY]: [what you want to do]
🎯 Target: [specific target]
⏰ Suggested duration: [reasonable TTL]

Want me to set this up? I can also create a broader mandate if you'd
prefer (e.g., all emails to @company.com for 30 days).
```

**禁止的行为**：
- 违反规则强行执行操作
- 在权限被拒绝后反复请求相同的操作
- 未经用户批准自行创建操作指令
- 假装已经进行了权限检查

**正确的做法**：
- 在适当的情况下提供模板建议（例如：“您需要我设置 `dev-tools` 吗？”）
- 对于相似的请求，可以批量处理（例如：“我需要运行多个 git 命令——需要创建一个 `dev-tools` 指令吗？”）
- 每次操作完成后都要记录下来
- 在相关情况下提醒用户剩余的权限使用限制（例如：“今天已经使用了20封电子邮件。”

### 首次设置

如果 `check-action` 返回 `"hint": "templates"`，则表示账本为空。此时需要指导用户完成相应的设置：

```
Agent Passport isn't set up yet. It takes 30 seconds:

  mandate-ledger.sh init agent:me "Your Name" "assistant" "openclaw"
  mandate-ledger.sh create-from-template dev-tools

Want me to run this for you?
```

### 记录操作

每次操作获得授权后，都需要进行记录：

```bash
$SCRIPT_DIR/mandate-ledger.sh log-action "<mandate_id>" <amount> "<description>"
```

- 对于财务操作：记录花费的金额
- 对于其他操作：记录操作类型（例如：“发送了电子邮件至 bob@company.com，内容关于 Q1 报告”）

---

## 概述

Agent Passport 为代理提供了自主性的权限控制机制。用户不是授予全权或无权的权限，而是根据具体需求授予**操作指令**（mandates），这些指令带有明确的限制条件：

```
"I authorize this agent to [ACTION] with [CONSTRAINTS] until [EXPIRY]"
```

这不仅仅适用于购买行为——它适用于所有需要用户同意的敏感操作。

## 操作类别

| 类别 | 示例 | 典型限制条件 |
|----------|----------|---------------------|
| `financial` | 购买、转账、订阅 | 花费上限、允许使用的商家列表 |
| `communication` | 发送电子邮件、消息、推文 | 收件人列表、发送频率限制 |
| `data` | 删除文件、编辑文档、写入数据库 | 文件路径列表、必须备份 |
| `system` | 运行 shell 命令、安装软件、配置系统 | 允许执行的命令列表、禁止使用 `sudo` 权限 |
| `external_api` | 调用第三方 API | 允许使用的服务列表、调用频率限制 |
| `identity` | 以用户身份执行的公开操作 | 需要人工审核 |

## 通配符模式

允许列表和拒绝列表支持以下三种通配符格式：

| 模式 | 匹配条件 | 示例 |
|---------|---------|---------|
| `prefix *` | 以指定前缀开头的所有内容 | `git *` → `git pull`、`git status` |
| `*.suffix` | 以指定后缀结尾的所有内容 | `*.env` → `config.env`、`.env` |
| `*middle*` | 包含指定中间部分的任何内容 | `*/.git/*` → `repo/.git/config` |
| `*@domain` | 与指定域名匹配的电子邮件地址 | `*@company.com` → `bob@company.com` |
| `exact` | 完全匹配 | `api.github.com` |

## 模式

- **本地模式**（默认）：完全离线操作。操作指令存储在 `~/.openclaw/agent-passport/` 目录下。
- **预览模式**：不进行数据存储，也不使用网络连接。仅生成验证后的数据包和用于发送请求的模板。
- **实时模式（未来计划）**：未来将支持与 Agent Bridge 后端连接，以实现多代理之间的同步和合规性检查。目前该功能尚未实现——此版本仅支持离线操作。

## 快速启动命令

```bash
# Initialize with identity
./mandate-ledger.sh init <agent_id> <principal> [scope] [provider]

# Templates (auto-detects agent if registered)
./mandate-ledger.sh templates
./mandate-ledger.sh create-from-template dev-tools
./mandate-ledger.sh create-from-template email-team <domain>
./mandate-ledger.sh create-from-template file-ops <path>
./mandate-ledger.sh create-from-template web-research

# Quick create (human-friendly durations: 7d, 24h, 30m)
./mandate-ledger.sh create-quick <type> <agent_id> <allowlist_csv> <duration> [amount_cap]

# Check & log
./mandate-ledger.sh check-action <agent> <type> <target> [amount]
./mandate-ledger.sh log-action <mandate_id> <amount> "<description>"

# Audit
./mandate-ledger.sh audit [limit]
./mandate-ledger.sh summary
```

## 命令参考

### 快速启动指南
```bash
init [agent_id] [principal] [scope] [provider]
                           # Initialize ledger, optionally register agent
templates                  # List available templates
create-from-template <t>   # Create mandate from template
  [agent_id] [args...]
create-quick <type>        # Create with positional args
  <agent_id> <allowlist>
  <duration> [amount_cap]
```

### 操作指令的生命周期
```bash
create <json>              # Create mandate (include action_type)
create-with-kya <json>     # Create with auto-attached agent KYA
get <mandate_id>           # Get mandate by ID
list [filter]              # List mandates (all|active|revoked|<action_type>)
revoke <mandate_id> [why]  # Revoke a mandate
```

### 权限管理
```bash
check-action <agent> <type> <target> [amount]
                           # Check if action is authorized
log-action <mandate_id> <amount> [description]
                           # Log action against mandate
```

### 审计与报告
```bash
audit [limit]              # Show recent audit entries
audit-mandate <id>         # Show audit for specific mandate
audit-summary [since]      # Summary by action type
summary                    # Show overall ledger stats
export                     # Export full ledger as JSON
```

### 用户身份验证（KYA）
```bash
kya-register <agent_id> <principal> <scope> [provider]
kya-get <agent_id>
kya-list
kya-revoke <agent_id> [why]
```

## 操作指令的结构

```json
{
  "mandate_id": "mandate_1770412575_3039e369",
  "action_type": "communication",
  "agent_id": "agent:my-assistant",
  "scope": {
    "allowlist": ["*@mycompany.com", "bob@partner.com"],
    "deny": ["*@competitor.com"],
    "rate_limit": "20/day",
    "kya": { "status": "verified", "verified_principal": "Mark" }
  },
  "amount_cap": null,
  "ttl": "2026-02-13T00:00:00Z",
  "status": "active",
  "usage": { "count": 5, "total_amount": 0 },
  "created_at": "2026-02-06T22:00:00Z"
}
```

## Agent Bridge（未来规划）

> **注意：** 该功能完全基于本地操作，不进行任何网络请求。Agent Bridge 是一个未来的计划功能——当前版本中不包含相关的网络代码，也不需要 API 密钥。

本地模式适用于单用户、单代理的场景。未来的 Agent Bridge 服务将提供以下功能：
- **多代理协调**：防止操作指令冲突
- **跨设备同步**：确保所有代理使用相同的行为规范
- **组织政策管理**：提供 IT 约束和用户自定义选项
- **合规性报告**：生成符合监管要求的审计报告
- **商家/服务注册**：验证商家信息并提供信任评分

随时可以导出本地账本：`./mandate-ledger.sh export > backup.json`

## 配置（OpenClaw）

```json
{
  "skills": {
    "entries": {
      "agent-passport-lite": {
        "env": {
          "AGENT_PASSPORT_LOCAL_LEDGER": "true"
        },
        "config": {
          "default_currency": "USD",
          "default_ttl_minutes": 60,
          "confirm_threshold_amount": 50
        }
      }
    }
  }
}
```

## 数据存储

所有数据均存储在 `~/.openclaw/agent-passport/` 目录下：
- `mandates.json`：操作指令账本
- `agents.json`：用户身份验证信息
- `audit.json`：操作审计记录

## 安全性注意事项

- 绝不要在提示信息、日志或输出结果中泄露任何敏感信息
- 操作指令虽然能限制某些操作，但无法完全防止误用
- 审计记录用于追踪操作行为，而非预防错误
- 在授予广泛权限之前，必须通过用户身份验证（KYA）来确认代理的身份。