---
name: clawsec-nanoclaw
version: 0.0.2
description: >
  **使用说明：**  
  在检查 NanoClaw 技能中的安全漏洞时、在安装新技能之前，或者收到与该机器人相关的安全警告时，请使用此方法。
---
# ClawSec for NanoClaw

ClawSec 是一款用于监控安全建议的工具，可保护您的 WhatsApp 机器人免受技能（skills）及其依赖项中已知漏洞的威胁。

## 概述

ClawSec 提供了一组 MCP（Management and Control）工具，用于检查已安装的技能是否存在安全问题。该工具会阻止安装存在漏洞的技能，并提供有关这些漏洞的可利用性信息（exploitability context），以便您及时处理问题。同时，它还会在现有技能中发现安全问题时向您发出警报。

**核心原则：** 在安装任何技能之前先进行安全检查；持续监控系统中的运行状态。

## 使用场景

在以下情况下使用 ClawSec 工具：
- 安装新技能时（先确认安全性）
- 用户询问“我的技能是否安全？”
- 调查可疑行为
- 进行定期安全审计
- 收到安全通知后

**不适用场景：**
- 代码审查（使用其他工具）
- 性能问题（属于不同范畴）
- 一般性调试

## 可用的 MCP 工具

### 安装前检查
```typescript
// Before installing any skill
const safety = await tools.clawsec_check_skill_safety({
  skillName: 'new-skill',
  skillVersion: '1.0.0'  // optional
});

if (!safety.safe) {
  // Show user the risks before proceeding
  console.warn(`Security issues: ${safety.advisories.map(a => a.id)}`);
}
```

### 安全审计
```typescript
// Check all installed skills (defaults to ~/.claude/skills in the container)
const result = await tools.clawsec_check_advisories({
  installRoot: '/home/node/.claude/skills'  // optional
});

if (result.matches.some((m) =>
  m.advisory.severity === 'critical' || m.advisory.exploitability_score === 'high'
)) {
  // Alert user immediately
  console.error('Urgent advisories found!');
}
```

### 浏览安全建议
```typescript
// List advisories with filters
const advisories = await tools.clawsec_list_advisories({
  severity: 'high',               // optional
  exploitabilityScore: 'high'     // optional
});
```

## 快速参考

| 任务 | 工具 | 关键参数 |
|------|------|---------------|
| 安装前检查 | `clawsec_check_skill_safety` | `skillName` |
| 审计所有技能 | `clawsec_check_advisories` | `installRoot`（可选） |
| 浏览安全建议列表 | `clawsec_list_advisories` | `severity`, `type`, `exploitabilityScore`（可选） |
| 验证软件包签名 | `clawsec_verify_skill_package` | `packagePath` |
| 刷新安全建议缓存 | `clawsecrefresh_cache` | （无） |
| 检查文件完整性 | `clawsec_check_integrity` | `mode`, `autoRestore`（可选） |
| 批准文件更改 | `clawsec_approve_change` | `path` |
| 查看基线状态 | `clawsec_integrity_status` | `path`（可选） |
| 验证审计日志 | `clawsec_verify_audit` | （无） |

## 常见使用模式

### 模式 1：安全安装技能
```typescript
// ALWAYS check before installing
const safety = await tools.clawsec_check_skill_safety({
  skillName: userRequestedSkill
});

if (safety.safe) {
  // Proceed with installation
  await installSkill(userRequestedSkill);
} else {
  // Show user the risks and get confirmation
  await showSecurityWarning(safety.advisories);
  if (await getUserConfirmation()) {
    await installSkill(userRequestedSkill);
  }
}
```

### 模式 2：定期安全检查
```typescript
// Add to scheduled tasks
schedule_task({
  prompt: "Check advisories using clawsec_check_advisories and alert when critical or high-exploitability matches appear",
  schedule_type: "cron",
  schedule_value: "0 9 * * *"  // Daily at 9am
});
```

### 模式 3：用户安全查询
```
User: "Are my skills secure?"

You: I'll check installed skills for known vulnerabilities.
[Use clawsec_check_advisories]

Response:
✅ No urgent issues found.
- 2 low-severity/low-exploitability advisories
- All skills up to date
```

## 常见错误

### ❌ 未进行安全检查就直接安装技能
```typescript
// DON'T
await installSkill('untrusted-skill');
```

### ❌ 忽略漏洞的可利用性信息
```typescript
// DON'T: Use severity only
if (advisory.severity === 'high') {
  notifyNow(advisory);
}
```

### ❌ 忽略严重等级为“critical”的安全问题
```typescript
// DON'T: Ignore high exploitability in medium severity advisories
if (advisory.severity === 'critical') alert();
```

### ❌ 跳过关键的安全检查步骤
```typescript
// DO: Prioritize exploitability and severity together
if (advisory.exploitability_score === 'high' || advisory.severity === 'critical') {
  // Alert immediately
}
```

## 实现细节

- **安全建议数据源**：https://clawsec.prompt.security/advisories/feed.json
- **更新频率**：每 6 小时自动更新一次
- **签名验证**：使用 Ed25519 算法对数据源进行签名验证
- **缓存位置**：`/workspace/project/data/clawsec-advisory-cache.json`

有关安装指南，请参阅 [INSTALL.md](./INSTALL.md)；如需了解高级用法，请参阅 [docs/](./docs/)。

## 实际应用效果：
- 防止安装存在远程代码执行（RCE）漏洞的技能
- 在依赖项中发现供应链攻击时发出警报
- 提供可操作的修复措施
- 保证零误报（仅使用经过筛选的安全建议数据）