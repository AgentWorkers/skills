---
name: agent-passport
version: 2.3.2
description: "面向“代理时代”的OAuth机制：为所有敏感的代理操作（包括购买、发送邮件、文件操作、系统命令以及API调用）实施权限控制。该机制提供了支出上限、速率限制、允许列表、TTL过期时间设置、审计追踪功能，以及用于识别代理身份的KYA（Know Your Agent）元数据。此外，还配备了SSRF防护机制（SSRF Shield）、路径遍历防护功能（Path Traversal Guard）、Webhook来源验证（Webhook Origin Verification）、技能扫描器（Skill Scanner）和注入防护功能（Injection Shield）。"
metadata: {"openclaw":{"requires":{"bins":["jq","bc","xxd","head","date","mkdir"],"env":["AGENT_PASSPORT_LEDGER_DIR"]}}}
user-invocable: true
---
# 代理通行证（OpenClaw）

## 30秒快速设置

```bash
# Initialize and register your agent
./mandate-ledger.sh init agent:my-assistant "Your Name" "personal assistant" "openclaw"

# Grant dev tool access (git, npm, docker, etc.)
./mandate-ledger.sh create-from-template dev-tools

# That's it! The agent will now check permissions before sensitive actions.
```

> 可用的模板：`dev-tools` · `email-team <domain>` · `file-ops <path>` · `web-research` · `safe-browsing` · `coding` · `email-assistant` · `read-only` · `full-auto`
> 运行 `./mandate-ledger.sh templates` 查看所有选项。

---

## ⚡ 代理行为契约

**如果您是正在阅读此规则的代理，请遵守以下规定：**

### 执行操作前的检查

在执行任何操作之前，必须先调用 `check-action`：

| 操作 | 类别 | 示例目标 |
|--------|----------|----------------|
| 运行 shell 命令 | `system` | `"git pull"`、`npm install"` |
| 发送消息/电子邮件 | `communication` | `"bob@company.com"` |
| 写入/删除文件 | `data` | `"/path/to/file.txt"` |
| 进行具有副作用的 API 调用 | `external_api` | `"api.github.com"` |
| 花费金钱 | `financial` | `"merchant_amazon"` 并指定金额 |
| 以用户身份公开行动 | `identity` | `"twitter_post"` |

**无需检查的情况：** 读取文件、网络搜索、内部逻辑处理或没有副作用的操作。

### 检查方法

```bash
SCRIPT_DIR="$HOME/.openclaw/skills/agent-passport/scripts"

result=$($SCRIPT_DIR/mandate-ledger.sh check-action "<your_agent_id>" "<category>" "<target>" [amount])
```

解析检查结果：
- `authorized: true` → 继续执行操作，并在之后记录该操作
- `authorized: false` → **停止操作，并询问用户授权。**
- 如果响应中包含 `kill_switch: true` 或原因说明为 “Kill switch engaged” → **立即停止操作**，并请求用户运行 `mandate-ledger.sh unlock`。

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

### 如何请求授权

当请求被拒绝时，应清晰简洁地告知用户原因：

```
I need to [ACTION] but don't have a mandate for it.

📋 [CATEGORY]: [what you want to do]
🎯 Target: [specific target]
⏰ Suggested duration: [reasonable TTL]

Want me to set this up? I can also create a broader mandate if you'd
prefer (e.g., all emails to @company.com for 30 days).
```

**禁止的行为：**
- 绕过检查直接执行操作
- 在被拒绝后反复请求相同的授权
- 未经用户批准自行创建授权请求
- 假装已经完成了检查

**允许的行为：**
- 在适当的情况下提供模板建议（例如：“需要我设置 `dev-tools` 吗？”）
- 对于类似的请求，可以批量处理（例如：“我需要运行多个 git 命令——需要 `dev-tools` 授权吗？”）
- 在操作完成后记录每个操作
- 在相关情况下提醒剩余的授权次数（例如：“每天已使用3封电子邮件）

### 首次设置

如果 `check-action` 返回 `"hint": "templates"`，则表示代理通行证中的授权信息为空。此时需要指导用户完成设置：

```
Agent Passport isn't set up yet. It takes 30 seconds:

  mandate-ledger.sh init agent:me "Your Name" "assistant" "openclaw"
  mandate-ledger.sh create-from-template dev-tools

Want me to run this for you?
```

### 操作日志记录

每次获得授权的操作都应被记录下来：

```bash
$SCRIPT_DIR/mandate-ledger.sh log-action "<mandate_id>" <amount> "<description>"
```

- 对于财务操作：记录花费的金额
- 对于其他操作：记录为 1
- 日志描述应易于人类阅读（例如：“已向 bob@company.com 发送关于 Q1 报告的电子邮件”）

### 杀死开关机制

如果用户激活了杀死开关，所有操作都将被冻结，直到解除冻结：

```bash
./mandate-ledger.sh kill "user requested freeze"
./mandate-ledger.sh unlock
```

当杀死开关处于激活状态时，代理的行为如下：
- 不得尝试执行敏感操作
- 不得循环调用 `check-action`
- 告知用户操作被禁止，并请求用户明确解锁。

---

## 概述

代理通行证为代理提供了自主权控制机制。用户不是授予全权或无权的许可，而是根据具体需求授予**有限制的授权**：

```
"I authorize this agent to [ACTION] with [CONSTRAINTS] until [EXPIRY]"
```

这不仅适用于购买行为，也适用于所有需要用户同意的敏感操作。

## 操作类别

| 类别 | 示例 | 常见限制 |
|----------|----------|---------------------|
| `financial` | 购买、转账、订阅 | 花费限额、允许的商家列表 |
| `communication` | 发送电子邮件、消息、推文 | 收件人列表、发送频率限制 |
| `data` | 删除文件、编辑文档、写入数据库 | 文件路径列表、要求备份 |
| `system` | 运行 shell 命令、安装软件、配置设置 | 允许执行的命令列表、禁止使用 sudo 权限 |
| `external_api` | 调用第三方 API | 允许访问的服务列表、发送频率限制 |
| `identity` | 以用户身份执行的公开操作 | 需要人工审核 |

## 通配符模式

允许列表和拒绝列表支持三种通配符格式：

| 模式 | 匹配条件 | 示例 |
|---------|---------|---------|
| `prefix *` | 以指定前缀开头的所有内容 | `git *` → `git pull`、`git status` |
| `*.suffix` | 以指定后缀结尾的所有内容 | `*.env` → `config.env`、`.env` |
| `*middle*` | 包含指定中间部分的任何内容 | `*/.git/*` → `repo/.git/config` |
| `*@domain` | 与指定域名匹配的电子邮件地址 | `*@company.com` → `bob@company.com` |
| `exact` | 完全匹配 | `api.github.com` |

## 模式

- **本地模式**（默认）：完全离线操作。授权信息存储在 `~/.openclaw/agent-passport/` 目录下。
- **预览模式**：不进行数据存储，也不使用网络连接。仅生成验证后的数据包和 curl 模板。
- **实时模式（未来计划）**：未来将支持与 Agent Bridge 后端连接，以实现多代理同步和合规性检查。目前该功能尚未实现——此版本仅支持离线操作。

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
./mandate-ledger.sh create-from-template safe-browsing
./mandate-ledger.sh create-from-template coding
./mandate-ledger.sh create-from-template email-assistant
./mandate-ledger.sh create-from-template read-only
./mandate-ledger.sh create-from-template full-auto

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

### 快速启动

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

### 授权流程

```bash
create <json>              # Create mandate (include action_type)
create-with-kya <json>     # Create with auto-attached agent KYA
get <mandate_id>           # Get mandate by ID
list [filter]              # List mandates (all|active|revoked|<action_type>)
revoke <mandate_id> [why]  # Revoke a mandate
```

### 授权管理

```bash
check-action <agent> <type> <target> [amount]
                           # Check if action is authorized
log-action <mandate_id> <amount> [description]
                           # Log action against mandate
kill <reason>               # Engage kill switch and freeze execution
unlock                      # Disengage kill switch
```

### 审计与报告

```bash
audit [limit]              # Show recent audit entries
audit-mandate <id>         # Show audit for specific mandate
audit-summary [since]      # Summary by action type
summary                    # Show overall ledger stats
export                     # Export full ledger as JSON
```

### 了解您的代理（KYA）

```bash
kya-register <agent_id> <principal> <scope> [provider]
kya-get <agent_id>
kya-list
kya-revoke <agent_id> [why]
```

## 授权结构

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

## Agent Bridge（未来计划）

> **注意：** 该功能完全基于本地操作，不进行任何网络请求。Agent Bridge 是未来的计划功能——当前版本中不包含相关网络代码，也不需要 API 密钥。

本地模式适用于单用户、单代理的场景。未来的 Agent Bridge 服务将提供以下功能：
- **多代理协调**：防止授权冲突
- **跨设备同步**：确保所有代理使用相同的授权规则
- **组织策略**：提供 IT 管理工具和用户自定义设置
- **合规性报告**：生成符合监管要求的审计报告
- **商家/服务注册**：验证商家信息并提供信任评分

可以随时导出本地授权信息：`./mandate-ledger.sh export > backup.json`

## 配置（OpenClaw）

```json
{
  "skills": {
    "entries": {
      "agent-passport": {
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
- `mandates.json`：授权信息记录
- `agents.json`：用户身份验证信息记录
- `audit.json`：操作审计记录

## 安全性注意事项

- 确保不会在提示信息、日志或输出结果中泄露任何敏感信息
- 授权机制可以限制操作，但无法完全防止滥用
- 审计记录用于提供可追溯性，而非预防错误
- 在授予广泛权限之前，必须通过 KYA（了解您的代理）机制验证用户身份