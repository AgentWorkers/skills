---
name: clawdbot-self-security-audit
description: 对 Clawdbot 的配置文件进行全面的只读安全审计。这是一项基于知识的技能，旨在帮助 Clawdbot 识别系统中的安全加固机会。当用户请求“运行安全检查”、“审计 Clawdbot”、“检查安全加固情况”或“我的 Clawdbot 有哪些漏洞”时，可以使用此技能。该技能利用 Clawdbot 的内部功能和文件系统访问权限来检查配置文件，检测配置错误，并提供相应的修复建议。该技能具有可扩展性——通过更新相关知识库，可以添加新的安全检查项。
homepage: https://github.com/TheSethRose/Clawdbot-Security-Check
metadata: {"clawdbot":{"emoji":"🔒","os":["darwin","linux"],"requires":{"files":["read"],"tools":["exec","bash"]},"install":[{"id":"read-skill","kind":"skill","name":"clawdbot-self-security-audit","label":"Install security audit skill","bins":["SKILL.md"]}]}}
---

# Clawdbot 自我安全审计框架

该技能使 Clawdbot 能够利用基本原理来审计自身的安全状况。Clawdbot 不依赖静态脚本，而是学习并动态应用这一框架来检测漏洞、了解其影响，并提出具体的修复建议。

## 核心理念

> “通过透明度和自我意识来实现安全。”

Clawdbot 应该清楚自身的攻击面，而这一技能直接嵌入了这种认知能力。

## 安全原则

运行具有 shell 访问权限的 AI 代理需要格外谨慎。重点关注以下三个方面：

1. **谁可以与机器人通信** - 私信（DM）策略、群组允许列表、频道限制
2. **机器人被允许执行操作的范围** - 网络暴露情况、网关绑定设置、代理配置
3. **机器人可以访问的资源** - 工具访问权限、文件权限、凭证存储

从最小的访问权限开始，随着信心的增加再逐步扩大权限范围。

## 信任层级

| 级别 | 实体 | 信任模型 |
|-------|--------|-------------|
| 1 | **所有者** | 完全信任 - 拥有所有访问权限 |
| 2 | **AI** | 信任但需验证 - 存在于沙箱环境中，并记录操作日志 |
| 3 | **允许列表** | 有限信任 - 仅允许指定用户 |
| 4 | **陌生人** | 无信任 - 默认情况下被阻止 |

## 审计命令

使用以下命令来执行安全审计：

- `clawdbot security audit` - 对常见问题进行标准审计
- `clawdbot security audit --deep` - 进行全面审计，包含所有检查项
- `clawdbot security audit --fix` - 应用安全防护措施

## 12 个安全领域

在审计 Clawdbot 时，系统地评估以下领域：

### 1. 网关暴露（严重级别）

**需要检查的内容：**
- 网关绑定地址在哪里？（`gateway.bind`）
- 是否配置了身份验证？（`gateway.auth_token` 或环境变量 `CLAWDBOT/GateWAY_TOKEN`）
- 暴露的端口是什么？（默认为 18789）
- 是否启用了 WebSocket 身份验证？

**检测方法：**
```bash
cat ~/.clawdbot/clawdbot.json | grep -A10 '"gateway"'
env | grep CLAWDBOT_GATEWAY_TOKEN
```

**漏洞：** 未进行身份验证的情况下将网关绑定到 `0.0.0.0` 或 `lan` 会导致网络访问。

**修复措施：**
```bash
clawdbot doctor --generate-gateway-token
export CLAWDBOT_GATEWAY_TOKEN="$(openssl rand -hex 32)"
```

### 2. 私信策略配置（高风险）

**需要检查的内容：**
- `dm_policy` 的设置是什么？
- 如果设置了 `allowlist`，那么哪些用户被明确允许发送私信？

**检测方法：**
```bash
cat ~/.clawdbot/clawdbot.json | grep -E '"dm_policy|"allowFrom"'
```

**漏洞：** 将 `dm_policy` 设置为 `allow` 或 `open` 会导致任何用户都可以向 Clawdbot 发送私信。

**修复措施：**
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

### 3. 群组访问控制（高风险）

**需要检查的内容：**
- `groupPolicy` 的设置是什么？
- 是否有明确的群组允许列表？
- 是否配置了提及（mention）功能？

**漏洞：** 开放的群组策略允许房间内的任何人触发命令。

### 4. 凭证安全（严重级别）

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

**修复措施：**
```bash
chmod 700 ~/.clawdbot
chmod 600 ~/.clawdbot/credentials/oauth.json
chmod 600 ~/.clawdbot/clawdbot.json
```

### 5. 浏览器控制暴露（高风险）

**需要检查的内容：**
- 是否启用了浏览器控制功能？
- 是否为远程控制设置了身份验证令牌？
- 控制界面是否需要使用 HTTPS？
- 是否配置了专用的浏览器配置文件？

**漏洞：** 未进行身份验证的情况下允许使用浏览器控制功能会导致远程界面被接管。

### 6. 网关绑定与网络暴露（高风险）

**漏洞：** 未进行身份验证的公开网关绑定会导致互联网访问。

**修复措施：**
```json
{
  "gateway": {
    "bind": "127.0.0.1",
    "mode": "local",
    "trustedProxies": ["127.0.0.1", "10.0.0.0/8"]
  }
}
```

### 7. 工具访问与沙箱环境（中等风险）

**工作区访问权限：**
| 模式 | 描述 |
|------|-------------|
| `none` | 工作区禁止访问 |
| `ro` | 工作区以只读模式挂载 |
| `rw` | 工作区以读写模式挂载 |

**漏洞：** 广泛的工具访问权限意味着一旦被攻破，影响范围更大。

### 8. 文件权限与本地磁盘管理（中等风险）

**需要检查的内容：**
- 目录权限（应为 700）
- 配置文件权限（应为 600）

**修复措施：**
```bash
chmod 700 ~/.clawdbot
chmod 600 ~/.clawdbot/clawdbot.json
chmod 600 ~/.clawdbot/credentials/*
```

### 9. 插件信任与模型安全性（中等风险）

**漏洞：** 不受信任的插件可能执行代码。旧版模型可能缺乏现代的安全性。

### 10. 日志记录与数据保护（中等风险）

**修复措施：**
```json
{
  "logging": {
    "redactSensitive": "tools",
    "path": "~/.clawdbot/logs/"
  }
}
```

### 11. 提示注入防护（中等风险）

**提示注入防护策略：**
- 将私信接收限制在已配对的账户或允许列表内
- 在群组中使用提及功能进行控制
- 将所有链接和附件视为潜在威胁
- 在沙箱环境中运行敏感工具

### 12. 危险命令的阻止（中等风险）

**修复措施：**
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

## 高级审计检查清单

按照以下优先级处理审计结果：

1. **严重级别：** 如果启用了相关工具，请立即锁定私信和群组功能
2. **严重级别：** 立即修复公共网络暴露问题
3. **高风险：** 通过令牌和 HTTPS 保护浏览器控制功能
4. **高风险：** 修正凭证和配置文件的权限设置
5. **中等风险：** 仅加载受信任的插件
6. **中等风险：** 对具有工具访问权限的机器人使用现代模型**

## 事件响应

如果怀疑系统被入侵：

### 限制损害范围
1. **停止网关进程** - `clawdbot daemon stop`
2. **将网关绑定地址设置为本地地址** - `bind": "127.0.0.1"`
3. **禁用高风险私信和群组功能** - 将相关设置设置为 `disabled`

### 重新配置
1. **更换网关身份验证令牌** - `clawdbot doctor --generate-gateway-token`
2. **更新浏览器控制和钩子令牌**
3. **吊销并更换模型提供商的 API 密钥**

### 审查
1. **检查网关日志和会话记录** - `~/.clawdbot/logs/`
2. **审查最近的配置更改**
3. **使用 `--deep` 选项重新运行安全审计** - `clawdbot security audit --deep`

## 报告模板

```
CLAWDBOT SECURITY AUDIT
Timestamp: $(date -Iseconds)

SUMMARY
- Critical:  $CRITICAL_COUNT
- High:      $HIGH_COUNT
- Medium:    $MEDIUM_COUNT
- Passed:    $PASSED_COUNT

FINDINGS
[CRITICAL] $VULN_NAME
   Finding: $DESCRIPTION
   Fix: $REMEDIATION

[HIGH] $VULN_NAME
   ...

This audit was performed by Clawdbot's self-security framework.
No changes were made to your configuration.
```

## 遵循的原则

- **零修改** - 该技能仅用于读取配置，绝不修改任何设置
- **深度防御** - 多重检查可以捕捉不同的攻击方式
- **可操作的输出** - 每个发现的问题都附带具体的修复建议
- **可扩展的设计** - 新的检查功能可以轻松集成

**记住：** 该技能的目的是让 Clawdbot 自我了解自身的安全状况。请定期使用它，并根据需要扩展功能，切勿忽略任何审计环节。