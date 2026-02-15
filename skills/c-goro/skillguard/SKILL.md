---
name: skillguard
description: **AgentSkill包的安全扫描器**  
该工具用于在安装AgentSkill包之前，检测其中可能存在的漏洞，如凭证窃取、代码注入、提示框篡改、数据泄露以及逃避安全检测的机制。在从ClawHub或其他不可信来源获取技能时，强烈建议使用该扫描器进行安全检查。
metadata: {"openclaw": {"requires": {"bins": ["node"]}}}
---

# SkillGuard — 代理安全扫描工具

当需要检查、审计或扫描某个技能的安全性时，请使用 SkillGuard。

## 命令

### 扫描本地的技能目录
```bash
node /home/claw/.openclaw/workspace/skillguard/src/cli.js scan <path>
```

### 以简洁格式输出扫描结果（适用于聊天）
```bash
node /home/claw/.openclaw/workspace/skillguard/src/cli.js scan <path> --compact
```

### 检查文本中是否存在提示注入（prompt injection）的尝试
```bash
node /home/claw/.openclaw/workspace/skillguard/src/cli.js check "<text>"
```

### 批量扫描多个技能
```bash
node /home/claw/.openclaw/workspace/skillguard/src/cli.js batch <directory>
```

### 根据技能的唯一标识符（slug）扫描 ClawHub 上的技能
```bash
node /home/claw/.openclaw/workspace/skillguard/src/cli.js scan-hub <slug>
```

## 分数解释
- 80-100 ✅ 低风险 — 可以安全安装
- 50-79 ⚠️ 中等风险 — 安装前请查看扫描结果
- 20-49 🟠 高风险 — 存在严重的安全问题
- 0-19 🔴 极高风险 — 未经人工审核切勿安装

## 输出格式
- 默认：完整文本报告
- `--compact`：适合聊天的简洁摘要
- `--json`：机器可读的完整报告
- `--quiet`：仅显示分数和判断结果