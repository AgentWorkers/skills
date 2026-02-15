---
name: clawdbot-self-security-audit
description: 对 Clawdbot 的配置文件进行全面的只读安全审计。这是一项基于知识的技能，旨在帮助 Clawdbot 识别系统中的安全漏洞及加固措施。当用户请求“运行安全检查”、“审计 Clawdbot”、“检查安全加固情况”或“我的 Clawdbot 存在哪些漏洞”时，可以使用该技能。该技能利用 Clawdbot 的内部功能和文件系统访问权限来检查配置文件，检测配置错误，并提供相应的修复建议。该技能具有可扩展性——通过更新相关知识库，可以添加新的安全检查项。
homepage: https://github.com/TheSethRose/Clawdbot-Security-Check
metadata: {"clawdbot":{"emoji":"🔒","os":["darwin","linux"],"requires":{"files":["read"],"tools":["exec","bash"]},"install":[{"id":"read-skill","kind":"skill","name":"clawdbot-self-security-audit","label":"Install security audit skill","bins":["SKILL.md"]}]}}
---

# Clawdbot 自我安全审计框架

该技能使 Clawdbot 能够利用基本原理来审计自身的安全状况。它不依赖于静态脚本，而是通过学习并动态应用安全框架来检测漏洞、理解其影响，并提出具体的修复建议。

## 核心理念

> “通过透明度和自我意识来实现安全。”——灵感来源于 ᴅᴴ�ɴɪᴇʟ ᴍɪᴇssʟᴇʀ

Clawdbot 需要了解自身的攻击面，而这一技能直接嵌入了这种认知能力。

## 安全原则

运行具有 shell 访问权限的 AI 代理时需要格外谨慎。重点关注以下三个领域：

1. **谁可以与机器人通信**——私信（DM）策略、允许列表、频道限制
2. **机器人被允许执行操作的範圍**——网络暴露情况、网关绑定设置、代理配置
3. **机器人可以访问的资源**——工具访问权限、文件权限、凭证存储

从最小的访问权限开始，随着信心的增加再逐步扩大权限范围。

## 信任等级

根据角色应用相应的信任等级：

| 等级 | 实体 | 信任模型 |
|-------|--------|-------------|
| 1 | **所有者** | 完全信任——拥有所有访问权限 |
| 2 | **AI** | 信任但需验证——置于沙箱环境中并记录日志 |
| 3 | **允许列表** | 有限信任——仅允许指定用户 |
| 4 | **陌生人** | 默认禁止访问 |

## 审计命令

使用以下命令执行安全审计：

- `clawdbot security audit` —— 检查常见安全问题
- `clawdbot security audit --deep` —— 进行全面审计
- `clawdbot security audit --fix` —— 应用安全防护措施

## 12 个安全领域

在审计 Clawdbot 时，系统地评估以下领域：

### 1. 网关暴露 🔴 严重风险

**需要检查的内容：**
- 网关绑定地址是什么？（`gateway.bind`）
- 是否配置了身份验证？（`gateway.auth_token` 或环境变量 `CLAWDBOT_GATEWAY_TOKEN`）
- 暴露的端口是什么？（默认：18789）
- 是否启用了 WebSocket 身份验证？

**检测方法：**
```bash
cat ~/.clawdbot/clawdbot.json | grep -A10 '"gateway"'
env | grep CLAWDBOT_GATEWAY_TOKEN
```

**漏洞：** 未进行身份验证的情况下将网关绑定到 `0.0.0.0` 或 `lan` 可能导致网络访问。

**修复方法：**
```bash
# Generate gateway token
clawdbot doctor --generate-gateway-token
export CLAWDBOT_GATEWAY_TOKEN="$(openssl rand -hex 32)"
```

---

### 2. 私信策略配置 🟠 高风险

**需要检查的内容：**
- `dm_policy` 的设置是什么？
- 如果使用了 `allowlist`，哪些用户被明确允许发送私信？

**检测方法：**
```bash
cat ~/.clawdbot/clawdbot.json | grep -E '"dm_policy|"allowFrom"'
```

**漏洞：** 将 `dm_policy` 设置为 `allow` 或 `open` 会导致任何用户都可以向 Clawdbot 发送私信。

**修复方法：**
```json
{
  "channels": {
    "telegram": {
      "dmPolicy": "allowlist",
      "allowFrom": ["@trusteduser1", "@trusteduser2"]
    }
  }
}
```

---

### 3. 组织访问控制 🟠 高风险

**需要检查的内容：**
- `groupPolicy` 的设置是什么？
- 是否有明确的允许列表？
- 是否配置了提及权限（mention gates）？

**检测方法：**
```bash
cat ~/.clawdbot/clawdbot.json | grep -E '"groupPolicy"|"groups"' 
cat ~/.clawdbot/clawdbot.json | grep -i "mention"
```

**漏洞：** 开放的组策略允许房间内的任何人触发命令。

**修复方法：**
```json
{
  "channels": {
    "telegram": {
      "groupPolicy": "allowlist",
      "groups": {
        "-100123456789": true
      }
    }
  }
}
```

---

### 4. 凭证安全 🔴 严重风险

**需要检查的内容：**
- 凭证文件的位置和权限设置
- 环境变量的使用情况
- 凭证配置文件的存储方式

**凭证存储位置：**
| 平台 | 路径 |
|----------|------|
| WhatsApp | `~/.clawdbot/credentials/whatsapp/{accountId}/creds.json` |
| Telegram | `~/.clawdbot/clawdbot.json` 或环境变量 |
| Discord | `~/.clawdbot/clawdbot.json` 或环境变量 |
| Slack | `~/.clawdbot/clawdbot.json` 或环境变量 |
| 配对允许列表 | `~/.clawdbot/credentials/channel-allowFrom.json` |
| 认证配置文件 | `~/.clawdbot/agents/{agentId}/auth-profiles.json` |
| 旧版 OAuth | `~/.clawdbot/credentials/oauth.json` |

**检测方法：**
```bash
ls -la ~/.clawdbot/credentials/
ls -la ~/.clawdbot/agents/*/auth-profiles.json 2>/dev/null
stat -c "%a" ~/.clawdbot/credentials/oauth.json 2>/dev/null
```

**漏洞：** 易被读取的明文凭证可能导致安全问题。

**修复方法：**
```bash
chmod 700 ~/.clawdbot
chmod 600 ~/.clawdbot/credentials/oauth.json
chmod 600 ~/.clawdbot/clawdbot.json
```

---

### 5. 浏览器控制暴露 🟠 高风险

**需要检查的内容：**
- 是否启用了浏览器控制功能？
- 是否为远程控制设置了身份验证令牌？
- 控制界面是否需要使用 HTTPS？
- 是否配置了专用的浏览器配置文件？

**检测方法：**
```bash
cat ~/.clawdbot/clawdbot.json | grep -A5 '"browser"'
cat ~/.clawdbot/clawdbot.json | grep -i "controlUi|insecureAuth"
ls -la ~/.clawdbot/browser/
```

**漏洞：** 未进行身份验证的浏览器控制功能可能导致远程界面被接管。浏览器访问权限可能使模型使用已登录的会话。

**修复方法：**
```json
{
  "browser": {
    "remoteControlUrl": "https://...",
    "remoteControlToken": "...",
    "dedicatedProfile": true,
    "disableHostControl": true
  },
  "gateway": {
    "controlUi": {
      "allowInsecureAuth": false
    }
  }
}
```

**安全提示：** 将浏览器控制相关的 URL 视为管理员 API 处理。**

---

### 6. 网关绑定与网络暴露 🟠 高风险

**需要检查的内容：**
- `gateway.bind` 的设置是什么？
- 是否配置了可信的代理？
- 是否启用了 Tailscale？

**检测方法：**
```bash
cat ~/.clawdbot/clawdbot.json | grep -A10 '"gateway"'
cat ~/.clawdbot/clawdbot.json | grep '"tailscale"'
```

**漏洞：** 未进行身份验证的公开网关绑定可能导致外部网络访问。

**修复方法：**
```json
{
  "gateway": {
    "bind": "127.0.0.1",
    "mode": "local",
    "trustedProxies": ["127.0.0.1", "10.0.0.0/8"],
    "tailscale": {
      "mode": "off"
    }
  }
}
```

---

### 7. 工具访问与沙箱环境 🟡 中等风险

**需要检查的内容：**
- 是否允许使用高级工具？
- 是否配置了 `restrict_tools` 或 `mcp_tools`？
- `workspaceAccess` 的设置是什么？
- 敏感工具是否在沙箱环境中运行？

**检测方法：**
```bash
cat ~/.clawdbot/clawdbot.json | grep -i "restrict|mcp|elevated"
cat ~/.clawdbot/clawdbot.json | grep -i "workspaceAccess|sandbox"
cat ~/.clawdbot/clawdbot.json | grep -i "openRoom"
```

**工作区访问权限：**
| 模式 | 描述 |
|------|-------------|
| `none` | 工作区禁止访问 |
| `ro` | 工作区以只读模式挂载 |
| `rw` | 工作区以读写模式挂载 |

**漏洞：** 广泛的工具访问权限意味着一旦被攻破，影响范围更大。小型模型更容易被滥用。**

**修复方法：**
```json
{
  "restrict_tools": true,
  "mcp_tools": {
    "allowed": ["read", "write", "bash"],
    "blocked": ["exec", "gateway"]
  },
  "workspaceAccess": "ro",
  "sandbox": "all"
}
```

**模型建议：** 对具有文件系统或网络访问权限的代理使用最新一代模型。如果使用小型模型，应禁用网络搜索和浏览器相关功能。**

---

### 8. 文件权限与本地磁盘安全 🟡 中等风险

**需要检查的内容：**
- 目录权限（应为 700）
- 配置文件的权限（应为 600）
- 符号链接的安全性

**检测方法：**
```bash
stat -c "%a" ~/.clawdbot
ls -la ~/.clawdbot/*.json
```

**漏洞：** 松懈的权限设置可能导致其他用户读取敏感配置文件。**

**修复方法：**
```bash
chmod 700 ~/.clawdbot
chmod 600 ~/.clawdbot/clawdbot.json
chmod 600 ~/.clawdbot/credentials/*
```

---

### 9. 插件信任与模型安全 🟡 中等风险

**需要检查的内容：**
- 是否明确允许使用插件？
- 是否仍在使用带有工具访问权限的旧版模型？

**检测方法：**
```bash
cat ~/.clawdbot/clawdbot.json | grep -i "plugin|allowlist"
cat ~/.clawdbot/clawdbot.json | grep -i "model|anthropic"
```

**漏洞：** 不受信任的插件可能执行恶意代码。旧版模型可能缺乏现代安全防护措施。

**修复方法：**
```json
{
  "plugins": {
    "allowlist": ["trusted-plugin-1", "trusted-plugin-2"]
  },
  "agents": {
    "defaults": {
      "model": {
        "primary": "minimax/MiniMax-M2.1"
      }
    }
  }
}
```

---

### 10. 日志记录与敏感信息隐藏 🟡 中等风险

**`logging.redactSensitive` 的设置是什么？**
- 应设置为 `tools` 以隐藏敏感工具的输出
- 如果设置为 `off`，凭证可能会泄露在日志中

**检测方法：**
```bash
cat ~/.clawdbot/clawdbot.json | grep -i "logging|redact"
ls -la ~/.clawdbot/logs/
```

**修复方法：**
```json
{
  "logging": {
    "redactSensitive": "tools",
    "path": "~/.clawdbot/logs/"
  }
}
```

---

### 11. 提示注入防护 🟡 中等风险

**需要检查的内容：**
- 是否启用了 `wrap_untrusted_content` 或 `untrusted_content_wrapper`？
- 外部/网页内容是如何处理的？
- 链接和附件是否被视为恶意内容？

**检测方法：**
```bash
cat ~/.clawdbot/clawdbot.json | grep -i "untrusted|wrap"
```

**提示注入防护策略：**
- 将私信发送限制在特定对象或允许列表内
- 在群组中使用提及权限控制
- 将所有链接和附件视为恶意内容
- 在沙箱环境中运行敏感工具
- 使用经过加固的模型（如 Anthropic Opus 4.5）

**漏洞：** 不受信任的内容（如网页内容或沙箱输出）可能注入恶意代码。

**修复方法：**
```json
{
  "wrap_untrusted_content": true,
  "untrusted_content_wrapper": "<untrusted>",
  "treatLinksAsHostile": true,
  "mentionGate": true
}
```

---

### 12. 危险命令阻止 🟡 中等风险

**需要检查的内容：**
- `blocked_commands` 中包含哪些命令？
- 是否包含以下命令：`rm -rf`, `curl |`, `git push --force`, `mkfs`, `fork bombs`？

**检测方法：**
```bash
cat ~/.clawdbot/clawdbot.json | grep -A10 '"blocked_commands"'
```

**漏洞：** 如果不阻止这些命令，恶意代码可能会破坏数据或窃取凭证。

**修复方法：**
```json
{
  "blocked_commands": [
    "rm -rf",
    "curl |",
    "git push --force",
    "mkfs",
    ":(){:|:&}"
  ]
}
```

---

### 13. 秘密信息扫描准备情况 🟡 中等风险

**需要检查的内容：**
- 是否配置了 `detect-secrets`？
- 是否存在 `.secrets.baseline` 文件？
- 是否已经执行了基线扫描？

**检测方法：**
```bash
ls -la .secrets.baseline 2>/dev/null
which detect-secrets 2>/dev/null
```

**秘密信息扫描（持续集成）：**
```bash
# Find candidates
detect-secrets scan --baseline .secrets.baseline

# Review findings
detect-secrets audit

# Update baseline after rotating secrets or marking false positives
detect-secrets scan --baseline .secrets.baseline --update
```

**漏洞：** 代码库中泄露的凭证可能导致安全问题。**

## 审计功能

`--fix` 标志会应用以下安全防护措施：

- 将常见频道的 `groupPolicy` 从 `open` 更改为 `allowlist`
- 将 `logging.redactSensitive` 的设置从 `off` 更改为 `tools`
- 严格限制本地文件权限：`.clawdbot` 目录权限设置为 700，配置文件权限设置为 600
- 保护包括凭证和认证配置文件在内的敏感信息

## 高级审计检查清单

按照以下优先级处理审计结果：

1. **🔴 如果启用了工具访问权限，立即锁定私信和群组**
2. **🔴 立即修复公共网络暴露问题**
3. **🟠 通过令牌和 HTTPS 保护浏览器控制功能**
4. **🟠 修正凭证和配置文件的权限设置**
5. **🟡 仅加载受信任的插件**
6. **🟡 对具有工具访问权限的机器人使用现代模型**

## 访问控制模型

### 私信访问模型

| 模式 | 描述 |
|------|-------------|
| `pairing` | 默认值——未知发送者必须通过代码批准 |
| `allowlist` | 未知发送者被拒绝 |
| `open` | 公开访问——允许列表中必须明确列出发送者 |
| `disabled` | 所有传入的私信都被忽略 |

### 斜杠命令

斜杠命令仅对基于频道允许列表的授权发送者可用。`/exec` 命令仅用于操作员，不会修改全局配置。

## 威胁模型与防护措施

### 潜在风险及应对措施

| 风险 | 对策 |
|------|------------|
| 执行 shell 命令 | 使用 `blocked_commands` 和 `restrict_tools` |
| 文件和网络访问 | 使用沙箱环境 (`workspaceAccess: none/ro`) |
| 社交工程和提示注入 | 使用 `wrap_untrusted_content` 和 `mentionGate` |
| 浏览器会话劫持 | 使用专用配置文件和令牌认证，以及 HTTPS |
| 凭证泄露 | 使用 `logging.redactSensitive: tools` 和环境变量来保护凭证 |

## 事件响应

如果怀疑发生安全漏洞，请按照以下步骤处理：

### 控制损失
1. **停止网关进程** —— 使用 `clawdbot daemon stop`
2. **将网关绑定地址设置为本地地址** —— 使用 `bind "127.0.0.1"`
3. **禁用高风险私信和群组功能** —— 将相关设置设置为 `disabled`

### 旋转配置
1. **更新网关认证令牌** —— 使用 `clawdbot doctor --generate-gateway-token`
2. **更新浏览器控制和钩子令牌**
3. **吊销并更新模型提供商的 API 密钥**

### 审查
1. **检查网关日志和会话记录** —— 查看 `~/.clawdbot/logs/`
2. **查看最近的配置更改** —— 查看 Git 日志或备份
3. **使用 `clawdbot security audit --deep` 重新执行安全审计**

## 报告安全漏洞

将安全问题报告给：**security@clawd.bot**

**在问题得到修复之前，切勿公开泄露漏洞信息。**

## 审计执行步骤

执行安全审计时，请按照以下顺序操作：

### 第一步：定位配置文件
```bash
CONFIG_PATHS=(
  "$HOME/.clawdbot/clawdbot.json"
  "$HOME/.clawdbot/config.yaml"
  "$HOME/.clawdbot/.clawdbotrc"
  ".clawdbotrc"
)
for path in "${CONFIG_PATHS[@]}"; do
  if [ -f "$path" ]; then
    echo "Found config: $path"
    cat "$path"
    break
  fi
done
```

### 第二步：检查各个安全领域
对于上述 13 个领域，分别执行以下操作：
1. 解析相关配置键
2. 与安全基线进行比较
3. 根据严重程度标记异常情况

### 第三步：生成报告
根据严重程度对审计结果进行分类：
```
🔴 CRITICAL: [vulnerability] - [impact]
🟠 HIGH: [vulnerability] - [impact]
🟡 MEDIUM: [vulnerability] - [impact]
✅ PASSED: [check name]
```

### 第四步：提供修复建议
对于每个发现的问题，提供以下信息：
- 需要进行的配置更改
- 示例配置设置
- 安全的命令（如果适用）

## 报告模板

```
═══════════════════════════════════════════════════════════════
🔒 CLAWDBOT SECURITY AUDIT
═══════════════════════════════════════════════════════════════
Timestamp: $(date -Iseconds)

┌─ SUMMARY ───────────────────────────────────────────────
│ 🔴 Critical:  $CRITICAL_COUNT
│ 🟠 High:      $HIGH_COUNT
│ 🟡 Medium:    $MEDIUM_COUNT
│ ✅ Passed:    $PASSED_COUNT
└────────────────────────────────────────────────────────

┌─ FINDINGS ──────────────────────────────────────────────
│ 🔴 [CRITICAL] $VULN_NAME
│    Finding: $DESCRIPTION
│    → Fix: $REMEDIATION
│
│ 🟠 [HIGH] $VULN_NAME
│    ...
└────────────────────────────────────────────────────────

This audit was performed by Clawdbot's self-security framework.
No changes were made to your configuration.
```

## 扩展该技能

要添加新的安全检查，可以按照以下步骤操作：

1. **识别漏洞** —— 什么配置错误导致了风险？
2. **确定检测方法** —— 哪个配置键或系统状态揭示了问题？
3. **定义安全基线** —— 安全的配置是什么？
4. **编写检测逻辑** —— 使用 shell 命令或文件解析方法
5. **记录修复步骤** —— 明确具体的修复方法
6. **划分风险等级** —— 严重、高、中、低

### 示例：添加 SSH 加强检查

```
## 14. SSH Agent Forwarding 🟡 Medium

**What to check:** Is SSH_AUTH_SOCK exposed to containers?

**Detection:**
```bash
env | grep SSH_AUTH_SOCK
```

**Vulnerability:** Container escape via SSH agent hijacking.

**Severity:** Medium
```

## 安全评估问题

在审计过程中，需要询问以下问题：

1. **暴露风险：** 哪些网络接口可以访问 Clawdbot？
2. **身份验证：** 每个访问点需要哪些验证措施？
3. **隔离措施：** Clawdbot 与主机之间有什么隔离措施？
4. **信任机制：** 哪些内容来源被视为“可信”？
5. **审计能力：** 有哪些证据可以证明 Clawdbot 的操作？
6. **最小权限原则：** Clawdbot 是否仅拥有必要的权限？

## 应用的安全原则

- **零修改原则** —— 该技能仅用于读取配置，绝不进行任何修改
- **深度防御** —— 多重检查机制可以捕获不同的攻击方式
- **可操作的审计结果** —— 每个发现的问题都配有具体的修复建议
- **可扩展设计** —— 新的安全检查可以轻松集成

## 参考资料

- 官方文档：https://docs.clawd.bot/gateway/security
- 原始框架：[ᴅᴴ�ɴɪᴇʟ ᴍɪᴇssʟᴇʀ 的相关内容](https://x.com/DanielMiessler/status/2015865548714975475)
- 代码仓库：https://github.com/TheSethRose/Clawdbot-Security-Check
- 漏洞报告邮箱：security@clawd.bot

---

**请记住：** 该技能的目的是让 Clawdbot 能够自我感知其安全状况。请定期使用它，并根据需要扩展功能，切勿忽略任何审计步骤。