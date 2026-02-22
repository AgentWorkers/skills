---
name: skill-security
description: OpenClaw 技能的安全审计工具。该工具用于检测是否存在凭证收集、代码注入、网络数据泄露以及代码混淆等安全风险。在从外部来源安装任何新技能之前，务必运行此工具。触发条件包括：新技能的安装、技能审计、安全扫描、技能审查，以及在加载外部技能之前。
---
# 技能安全扫描器

这是一个用于 OpenClaw 技能的安全审计工具。**在安装任何新技能之前，请先运行此扫描器。**

## 快速审计

```bash
# Audit a skill directory
~/workspace/skills/skill-security/audit.sh /path/to/skill

# Audit all installed skills
~/workspace/skills/skill-security/audit-all.sh
```

## 审计内容

| 检查项 | 风险等级 | 模式         |
|-------|------------|-------------|
| **网络数据泄露** | 🚨 高风险 | `requests`, `urllib`, `http.client`, `socket.`, `fetch()`, `axios` |
| **凭证收集** | 🚨 高风险 | `.ssh/`, `.aws/`, `pass`, `keyring`, `credential`, `secret`, `token` 文件的读取操作 |
| **代码注入** | 🚨 严重风险 | `exec()`, `eval()`, `compile()`, `Function()`, `__import__` |
| **代码混淆** | ⚠️ 中等风险 | `base64.decode`, `atob`, 编码后的数据包 |
| **环境变量泄露** | ⚠️ 中等风险 | `os.environ`, `process.env`, `getenv` 的大量数据访问 |
| **子进程滥用** | ⚠️ 中等风险 | 使用凭证执行 `subprocess.run`, `os.system`, `child_process` |

## 风险等级

- **严重风险** (🚨): 禁止安装该技能，并向管理员报告 |
- **高风险** (🔴): 使用前需要手动审核 |
- **中等风险** (🟡): 如果来自可信来源，则允许使用 |
- **低风险** (🟢): 仅提供信息提示 |

## 安全技能使用指南

在使用任何技能之前，请确认：

1. ✅ 该技能是否来自可信来源（官方 OpenClaw 或知名开发者）？
2. ✅ 代码是否可读（未经过混淆处理）？
3. ✅ 该技能是否明确说明了为何需要网络访问或凭证访问？
4. ✅ 该技能是否将文件访问权限限制在其自身的目录内？
5. ✅ 该技能是否已经过社区的安全审计？

## 与 AGENTS.md 的集成

将以下代码添加到您的工作流程中：

```markdown
## Skill Installation Protocol

Before loading any new skill:
1. Run `~/workspace/skills/skill-security/audit.sh <skill-path>`
2. If CRITICAL/HIGH findings → STOP, alert the user
3. If MEDIUM findings → Review manually, proceed if justified
4. If CLEAN → Safe to use
```

## 自动防护机制

该扫描器会在 `./blocklist.txt` 文件中创建一个黑名单。被检测出严重安全问题的技能会自动被添加到黑名单中。

## 手动覆盖

如果某个技能被标记为有问题，但您确认它是安全的，可以手动覆盖该规则：

```bash
echo "skill-name:verified:YYYY-MM-DD:reason" >> allowlist.txt
```

---

## 高级技能

喜欢这些功能吗？欢迎查看我们的高级技能包：**[skillpacks.dev](https://skillpacks.dev)**：

- 🛡️ **安全套件** — 全面个人身份信息扫描、秘密信息检测、命令注入防御 — [9.90 美元](https://polycatai.gumroad.com/l/bsrugo)
- 🧠 **结构化内存** — 三层内存管理功能，替代传统的 MEMORY.md — [9.90 美元](https://polycatai.gumroad.com/l/goawrg)
- 📋 **计划与执行** — 系统化的任务计划及批量执行功能 — [9.90 美元](https://polycatai.gumroad.com/l/uydfto)
- 💎 **[三款高级技能包，总价 24.90 美元](https://polycatai.gumroad.com/l/atsrl)**