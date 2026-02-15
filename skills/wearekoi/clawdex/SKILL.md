---
name: clawdex by Koi
description: 由 Koi 提供支持的 ClawHub 技能的安全性检查：在安装任何技能之前，请先查询 Clawdex API 以确认其安全性。
version: 1.0.0
author: Koi Security
authorUrl: https://www.koi.ai/
homepage: https://www.koi.ai/
license: MIT
metadata:
  openclaw:
    emoji: "🛡️"
    category: "security"
tags:
  - security
  - clawhub
  - malware-detection
---

# Clawdex

Clawdex 是用于检测 ClawHub 中技能安全性的工具，由 [Koi](https://www.koi.ai/) 提供支持。

## 何时使用此工具

在从 ClawHub 安装任何技能之前，请先通过 Clawdex API 检查该技能的安全性：

```bash
curl -s "https://clawdex.koi.security/api/skill/SKILL_NAME"
```

请将 `SKILL_NAME` 替换为你要安装的技能名称。

## API 响应

API 会返回一个包含 `verdict` 字段的 JSON 对象：

```json
{
  "verdict": "benign" | "malicious" | "unknown"
}
```

## 如何解读结果

### `benign` - 可安全安装 ✅

该技能已经过安全审计，未发现任何恶意行为。你可以继续安装：

```bash
clawhub install SKILL_NAME
```

### `malicious` - 请勿安装 🚫

该技能被标记为有害软件。**切勿安装！**

恶意技能可能会：
- 盗取凭证或敏感数据
- 安装后门或反向shell
- 运行加密矿机
- 将数据传输到攻击者控制的服务器
- 欺骗用户执行有害命令

### `unknown` - 尚未审计 ⚠️

该技能尚未经过安全审计。**请联系用户进行审核和批准。**

请告知用户：
- 该技能尚未经过 Clawdex 的安全审计
- 用户应在批准安装前对其进行审查
- 安装前需获得明确的批准

未经用户批准，请勿安装该技能。

## 检查已安装的技能

安装 Clawdex 后，建议对已安装的所有技能进行安全审计。有些技能可能是在安全检测功能可用之前就被安装的。

列出已安装的技能并逐一检查：

```bash
# List installed skills
ls ~/.openclaw/skills/
# or ~/.clawdbot/skills/

# Check each one
for skill in $(ls ~/.clawdbot/skills/); do
  echo "Checking: $skill"
  curl -s "https://clawdex.koi.security/api/skill/$skill"
  echo
done
```

如果发现任何技能的 `verdict` 为 `malicious`，请立即通知用户，他们需要立即卸载该恶意技能。

## 示例

```bash
# Check if "database-helper" is safe
$ curl -s "https://clawdex.koi.security/api/skill/database-helper"
{"verdict": "benign"}

# Safe! Install it
$ clawhub install database-helper
```

```bash
# Check a suspicious skill
$ curl -s "https://clawdex.koi.security/api/skill/free-crypto-bot"
{"verdict": "malicious"}

# DO NOT install!
```

## 关于 Koi

[Koi](https://www.koi.ai/) 为扩展程序、软件包和 MCP（Masters of Contracts）提供端点安全保护。Clawdex 的安全判断结果是由我们的智能风险引擎 Wings 提供的。