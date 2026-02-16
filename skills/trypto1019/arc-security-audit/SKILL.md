---
name: security-audit
description: 对代理的全部技能栈进行全面的安全审计。将链扫描器（Chain Scanner）、差异检测器（Difference Detector）和健康监控器（Health Monitor）整合到一个评估系统中，生成优先级排序的审计结果和信任证明（Trust Attestations）。
user-invocable: true
metadata: {"openclaw": {"emoji": "🛡️", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# 安全审计

这个命令可以用来审计您所有的技能（skill）组件。它将 `arc-skill-scanner`、`arc-trust-verifier` 这两个工具串联起来使用，生成一份包含优先级排序的安全风险报告。

## 为何需要这样的工具

逐一运行各个安全工具非常繁琐。一次完整的审计需要包括扫描、信任评估、二进制文件验证以及生成统一的报告。而这个工具能够一次性完成所有这些步骤。

## 命令

### 审计所有已安装的技能
```bash
python3 {baseDir}/scripts/audit.py full
```

### 审计特定的技能
```bash
python3 {baseDir}/scripts/audit.py single --path ~/.openclaw/skills/some-skill/
```

### 以 JSON 格式生成审计报告
```bash
python3 {baseDir}/scripts/audit.py full --json --output report.json
```

### 带有信任验证结果的审计
```bash
python3 {baseDir}/scripts/audit.py full --attest
```

## 功能说明

1. 使用 `arc-skill-scanner` 的扫描规则来检查所有已安装的技能。
2. 评估每个技能的信任等级（包括来源、代码质量、二进制文件的完整性）。
3. 通过 SHA-256 校验和来检查二进制文件的完整性。
4. 生成按风险等级排序的审计报告。
5. （可选）为通过所有检查的技能生成信任验证结果。

## 输出内容

审计报告包括：
- 综述：扫描的技能总数、按严重程度分类的问题、整体风险等级。
- 每个技能的详细信息：存在的问题、信任评分、改进建议。
- 需要立即处理的紧急问题。
- 通过所有检查的技能的信任验证结果（如果使用了 `--attest` 标志）。