---
name: skill-trust-auditor
description: "在安装之前，务必对 ClawHub 中的技能（skills）进行安全风险审计。"
version: "1.1.3"
metadata:
  {
    "openclaw": {
      "emoji": "🛡️",
      "requires": {
        "bins": ["python3"],
        "anyBins": ["clawhub"]
      }
    }
  }
---
# 技能信任审计器

在安装任何 ClawHub 技能之前，对其进行安全风险审计。

## 🛠️ 安装

### 1. 建议使用 OpenClaw
告诉 OpenClaw：“安装 skill-trust-auditor 技能。” 代理将自动处理安装和配置。

### 2. 手动安装（通过 CLI）
如果您更喜欢使用终端，请运行：
```bash
clawhub install skill-trust-auditor
```

## 设置（仅首次运行）

```bash
bash scripts/setup.sh
```

## 审计技能

当用户输入 “audit [技能名称]” 或 “[技能名称] 是否安全” 时，或者在执行任何 `clawhub install` 操作之前：

```bash
bash scripts/audit.sh [skill-name-or-url]
# Example:
bash scripts/audit.sh steipete/clawhub
bash scripts/audit.sh https://clawhub.ai/someuser/someskill
```

审计结果输出：
```json
{
  "skill": "someuser/someskill",
  "trust_score": 72,
  "verdict": "INSTALL WITH CAUTION",
  "risks": [
    {"level": "HIGH", "pattern": "curl to external domain", "location": "scripts/sync.sh:14"},
    {"level": "MEDIUM", "pattern": "reads MEMORY.md", "location": "SKILL.md:23"}
  ],
  "safe_patterns": ["no env var access", "no self-modification"],
  "author_verified": false,
  "recommendation": "Review scripts/sync.sh:14 before installing. The external curl call could exfiltrate data."
}
```

向用户提供清晰的审计总结：
```
🛡️ Trust Audit: someuser/someskill
Score: 72/100 — ⚠️ INSTALL WITH CAUTION

🔴 HIGH: curl to unknown domain in scripts/sync.sh:14
🟡 MEDIUM: reads your MEMORY.md

Recommendation: Inspect line 14 of sync.sh before proceeding.
Run: clawhub show someuser/someskill --file scripts/sync.sh
```

## 信任评分指南

| 评分 | 判断 | 措施 |
|-------|---------|--------|
| 90-100 | ✅ 安全 | 可以自由安装 |
| 70-89 | ⚠️ 警告 | 先查看标记出的问题 |
| 50-69 | 🟠 有风险 | 仅在你了解相关风险的情况下安装 |
| 0-49 | 🔴 不要安装 | 存在很高的恶意意图风险 |

## 风险模式参考

**高风险**（每项扣 3 分）：
- 脚本中访问 `process.env` 变量
- 使用 `curl`/`wget` 访问非标准域名
- 直接读取 `~/.config` 或 `~/.openclaw` 文件
- 使用 `exec()` 函数并允许用户输入数据
- 指令要求修改 `SOUL.md`/`AGENTS.md`/`openclaw.json` 文件

**中等风险**（每项扣 1 分）：
- 任何出站 API 调用（即使是对已知服务的调用）
- 在工作区之外写入文件
- 读取 `MEMORY.md` 或日记文件

**低风险**（每项扣 3 分）：
- 使用 `web_fetch` 访问标准域名
- 在工作区内仅进行读取操作

## 自动审计模式

可以选择在每次安装时自动执行审计：
```bash
# Add to your shell aliases:
alias clawhub-safe='bash ~/.openclaw/workspace/skills/skill-trust-auditor/scripts/audit.sh $1 && clawhub install $1'
```

## ClawHavoc 模式参考

请参阅 `references/clawhavoc-patterns.md`，了解 2026 年 2 月发生的恶意攻击模式。如有新的攻击模式被报告，请更新该文件。