---
name: clawsec-nanoclaw
version: 0.0.1
description: >
  **使用场景：**  
  - 在安装新的 NanoClaw 技能之前，用于检查这些技能是否存在安全漏洞；  
  - 当收到与机器人相关的安全警告时，也可使用该工具进行核查。
---
# ClawSec for NanoClaw

ClawSec 是一款用于监控安全建议的工具，可保护您的 WhatsApp 机器人免受技能（skills）及其依赖项中已知漏洞的威胁。

## 概述

ClawSec 提供了一系列 MCP（Management and Control）工具，用于检查已安装的技能是否包含安全风险。该工具会阻止安装存在漏洞的技能，并在现有技能中发现问题时向您发出警报。

**核心原则：** 在安装之前进行检查；持续监控系统中的运行状态。

## 使用场景

在以下情况下使用 ClawSec 工具：
- 安装新技能时（先确认安全性）
- 用户询问“我的技能是否安全？”
- 调查可疑行为
- 进行定期安全审计
- 收到安全通知后

**不适用场景**：
- 代码审查（请使用其他工具）
- 性能问题（属于不同范畴）
- 一般性调试

## 可用的 MCP 工具

### 安装前检查

```typescript
// Before installing any skill
const safety = await tools.clawsec_check_skill_safety({
  skillName: 'new-skill',
  version: '1.0.0'  // optional
});

if (!safety.safe) {
  // Show user the risks before proceeding
  console.warn(`Security issues: ${safety.advisories.map(a => a.id)}`);
}
```

### 安全审计

```typescript
// Check all installed skills
const result = await tools.clawsec_check_advisories({
  skillsRoot: '/workspace/project/skills'  // optional
});

if (result.criticalCount > 0) {
  // Alert user immediately
  console.error('CRITICAL vulnerabilities found!');
}
```

### 浏览安全建议

```typescript
// List advisories with filters
const advisories = await tools.clawsec_list_advisories({
  platform: 'nanoclaw',    // optional: nanoclaw, openclaw, or both
  severity: 'critical'     // optional: critical, high, medium, low
});
```

## 快速参考

| 任务 | 工具 | 关键参数 |
|------|------|---------------|
| 安装前检查 | `clawsec_check_skill_safety` | `skillName` |
| 审计所有技能 | `clawsec_check_advisories` | `installRoot`（可选） |
| 浏览安全建议 | `clawsec_list_advisories` | `severity`, `type`（可选） |
| 验证包签名 | `clawsec_verify_skill_package` | `packagePath` |
| 刷新建议缓存 | `clawsec_refresh_cache` | （无） |
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
  prompt: "Check for security advisories using clawsec_check_advisories and alert if any critical issues found",
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
✅ No critical issues found.
- 2 low-severity advisories (not urgent)
- All skills up to date
```

## 常见错误

### ❌ 未进行检查即进行安装
```typescript
// DON'T
await installSkill('untrusted-skill');
```

### ❌ 忽略平台过滤规则
```typescript
// DON'T: Check OpenClaw advisories on NanoClaw
const advisories = await tools.clawsec_list_advisories({
  platform: 'openclaw'  // Wrong platform!
});
```

### ❌ 忽略严重性等级为“critical”的建议
```typescript
// DO: Use correct platform or let it auto-filter
const advisories = await tools.clawsec_list_advisories({
  platform: 'nanoclaw'  // Correct
});
```

### ❌ 跳过关键的安全建议
```typescript
// DON'T: Only check low severity
if (result.lowCount > 0) alert();
```

## 实现细节

- **安全建议来源**：https://clawsec.prompt.security/advisories/feed.json
- **更新频率**：每 6 小时自动更新一次
- **签名验证**：使用 Ed25519 签名来验证安全建议的完整性
- **缓存位置**：`/workspace/project/data/clawsec-cache.json`

有关安装说明，请参阅 [INSTALL.md](./INSTALL.md)；更多高级用法信息，请参阅 [docs/](./docs/)。

## 实际应用效果：
- 阻止安装存在远程代码执行（RCE）漏洞的技能
- 对依赖项中的供应链攻击发出警报
- 提供可操作的修复措施
- 确保零误报（仅使用经过筛选的安全建议）