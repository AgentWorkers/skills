---
name: skill-vetter
version: 1.0.0
description: **AI代理的安全优先技能审核机制**  
在从ClawdHub、GitHub或其他来源安装任何技能之前，请务必使用该审核机制。该机制会检查是否存在潜在的安全风险、权限范围问题以及可疑的行为模式。
---

# 技能审核工具 🔒

这是一个以安全为首要原则的AI代理技能审核流程。**在安装任何技能之前，务必先进行审核。**

## 使用场景

- 在从ClawdHub安装任何技能之前
- 在运行来自GitHub仓库的技能之前
- 在评估其他代理分享的技能时
- 每当需要安装未知代码时

## 审核流程

### 第一步：来源检查

```
Questions to answer:
- [ ] Where did this skill come from?
- [ ] Is the author known/reputable?
- [ ] How many downloads/stars does it have?
- [ ] When was it last updated?
- [ ] Are there reviews from other agents?
```

### 第二步：代码审查（必选）

阅读技能中的所有文件，并检查以下**风险提示**：

```
🚨 REJECT IMMEDIATELY IF YOU SEE:
─────────────────────────────────────────
• curl/wget to unknown URLs
• Sends data to external servers
• Requests credentials/tokens/API keys
• Reads ~/.ssh, ~/.aws, ~/.config without clear reason
• Accesses MEMORY.md, USER.md, SOUL.md, IDENTITY.md
• Uses base64 decode on anything
• Uses eval() or exec() with external input
• Modifies system files outside workspace
• Installs packages without listing them
• Network calls to IPs instead of domains
• Obfuscated code (compressed, encoded, minified)
• Requests elevated/sudo permissions
• Accesses browser cookies/sessions
• Touches credential files
─────────────────────────────────────────
```

### 第三步：权限范围

```
Evaluate:
- [ ] What files does it need to read?
- [ ] What files does it need to write?
- [ ] What commands does it run?
- [ ] Does it need network access? To where?
- [ ] Is the scope minimal for its stated purpose?
```

### 第四步：风险分类

| 风险等级 | 例子 | 处理方式 |
|------------|----------|--------|
| 🟢 低风险 | 日志记录、天气数据、格式化功能 | 进行基本审查后即可安装 |
| 🟡 中等风险 | 文件操作、浏览器功能、API调用 | 需要全面代码审查 |
| 🔴 高风险 | 访问凭证处理、交易功能、系统操作 | 需要人工批准 |
| ⛔ 极高风险 | 安全配置设置、root权限 | 禁止安装 |

## 审核结果输出格式

审核完成后，生成以下报告：

```
SKILL VETTING REPORT
═══════════════════════════════════════
Skill: [name]
Source: [ClawdHub / GitHub / other]
Author: [username]
Version: [version]
───────────────────────────────────────
METRICS:
• Downloads/Stars: [count]
• Last Updated: [date]
• Files Reviewed: [count]
───────────────────────────────────────
RED FLAGS: [None / List them]

PERMISSIONS NEEDED:
• Files: [list or "None"]
• Network: [list or "None"]  
• Commands: [list or "None"]
───────────────────────────────────────
RISK LEVEL: [🟢 LOW / 🟡 MEDIUM / 🔴 HIGH / ⛔ EXTREME]

VERDICT: [✅ SAFE TO INSTALL / ⚠️ INSTALL WITH CAUTION / ❌ DO NOT INSTALL]

NOTES: [Any observations]
═══════════════════════════════════════
```

## 快速审核命令

对于托管在GitHub上的技能：
```bash
# Check repo stats
curl -s "https://api.github.com/repos/OWNER/REPO" | jq '{stars: .stargazers_count, forks: .forks_count, updated: .updated_at}'

# List skill files
curl -s "https://api.github.com/repos/OWNER/REPO/contents/skills/SKILL_NAME" | jq '.[].name'

# Fetch and review SKILL.md
curl -s "https://raw.githubusercontent.com/OWNER/REPO/main/skills/SKILL_NAME/SKILL.md"
```

## 信任等级

1. **官方OpenClaw技能** → 审查要求较低（但仍需审核）
2. **评分超过1000星的仓库** → 审查要求适中
3. **知名作者发布的技能** → 审查要求适中
4. **新来源或未知来源的技能** → 审查要求最高
5. **需要访问凭证的技能** → 必须经过人工批准

## 重要提示

- 没有任何技能值得以牺牲安全为代价来安装
- 有疑问时，请不要安装
- 对于高风险决策，请咨询相关人员
- 记录审核过程以供将来参考

---

*偏执是一种优势。* 🔒🦀