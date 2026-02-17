---
name: compliance-checker
description: 基于策略的 OpenClaw 技能合规性评估工具：支持定义安全策略，根据这些策略来评估用户的技能水平，跟踪违规行为，并生成合规性报告。评估结果可与 CIS Controls 和 OWASP 等安全框架进行对比。该工具还与 arc-skill-scanner 和 arc-trust-verifier 等工具集成使用。
user-invocable: true
metadata: {"openclaw": {"emoji": "🛡️", "os": ["darwin", "linux"], "requires": {"bins": ["python3"]}}}
---
# 合规性检查器

该工具用于评估 OpenClaw 技能是否符合预定义的安全政策，并通过框架映射的结果和修复跟踪功能来监控整个技能库的合规状况。

## 为何需要这个工具

安全扫描器可以发现漏洞，信任验证器可以验证来源的可靠性，但它们都无法回答“该技能是否符合我们的安全政策？”这个问题。合规性检查器填补了这一空白——它首先定义了“合规”的具体标准，然后针对这些标准对每个技能进行评估。

## 快速入门

### 定义安全政策
```bash
python3 {baseDir}/scripts/checker.py policy create --name "production" --description "Production deployment requirements"
```

### 为政策添加规则
```bash
python3 {baseDir}/scripts/checker.py policy add-rule --policy "production" \
  --rule "no-critical-findings" \
  --description "No CRITICAL findings from skill scanner" \
  --severity critical

python3 {baseDir}/scripts/checker.py policy add-rule --policy "production" \
  --rule "trust-verified" \
  --description "Must have VERIFIED or TRUSTED trust level" \
  --severity high

python3 {baseDir}/scripts/checker.py policy add-rule --policy "production" \
  --rule "no-network-calls" \
  --description "No unauthorized network calls in scripts" \
  --severity high

python3 {baseDir}/scripts/checker.py policy add-rule --policy "production" \
  --rule "no-shell-exec" \
  --description "No shell=True or subprocess calls" \
  --severity medium

python3 {baseDir}/scripts/checker.py policy add-rule --policy "production" \
  --rule "has-checksum" \
  --description "Must have SHA-256 checksums for all scripts" \
  --severity medium
```

### 根据政策评估技能
```bash
python3 {baseDir}/scripts/checker.py assess --skill "arc-budget-tracker" --policy "production"
```

### 评估所有已安装的技能
```bash
python3 {baseDir}/scripts/checker.py assess-all --policy "production"
```

### 查看合规状态
```bash
python3 {baseDir}/scripts/checker.py status --policy "production"
```

### 生成合规报告
```bash
python3 {baseDir}/scripts/checker.py report --policy "production" --format json
python3 {baseDir}/scripts/checker.py report --policy "production" --format text
```

## 内置规则

以下规则是开箱即用的：

| 规则 | 检查内容 | 框架映射 |
|------|---------------|-------------------|
| `no-critical-findings` | 扫描器未发现严重漏洞（CRITICAL 等级） | CIS Control 16, OWASP A06 |
| `no-high-findings` | 扫描器未发现高风险漏洞（HIGH 等级） | CIS Control 16, OWASP A06 |
| `trust-verified` | 信任级别已通过验证（VERIFIED 或 TRUSTED） | CIS Control 2 |
| `no-network-calls` | 无未经授权的网络请求 | CIS Control 9, OWASP A10 |
| `no-shell-exec` | 无 shell 执行行为 | CIS Control 2, OWASP A03 |
| `no-eval-exec` | 无评估或执行相关行为 | OWASP A03 |
| `has-checksum` | 所有文件均具有 SHA-256 校验和 | CIS Control 2 |
| `no-env-access` | 无对环境变量的访问 | CIS Control 3 |
| `no-data-exfil` | 无数据泄露行为 | CIS Control 3, CIS Control 13 |
| `version-pinned` | 所有依赖项的版本均已固定 | CIS Control 2 |

## 合规状态

每次技能政策评估的结果分为以下几种：

- **COMPLIANT**：符合所有政策规则
- **NON-COMPLIANT**：违反了一条或多条规则
- **EXEMPTED**：所有违规情况均已获得批准豁免
- **UNKNOWN**：尚未进行评估

## 例外情况

有时某个技能确实需要违反某些规则（例如，网络监控技能需要访问网络）。请记录这些例外情况并附上理由：
```bash
python3 {baseDir}/scripts/checker.py exempt --skill "arc-skill-scanner" \
  --rule "no-network-calls" \
  --reason "Scanner needs network access to check URLs against blocklists" \
  --approved-by "arc"
```

## 修复跟踪

当某个技能未通过合规性检查时，可以跟踪其修复过程：
```bash
python3 {baseDir}/scripts/checker.py remediate --skill "some-skill" \
  --rule "no-shell-exec" \
  --action "Replaced subprocess.call with safer alternative" \
  --status fixed
```

## 数据存储

合规性数据存储在 `~/.openclaw/compliance/` 目录下：
- `policies/`：政策定义（JSON 格式）
- `assessments/`：每个技能的评估结果（JSON 格式）
- `exemptions/`：已批准的豁免情况（JSON 格式）
- `remediations/`：修复跟踪记录（JSON 格式）

## 集成

合规性检查器可以从以下工具读取数据：
- **arc-skill-scanner**：漏洞扫描结果
- **arc-trust-verifier**：信任级别和验证信息

要运行完整的检查流程，请执行以下操作：
```bash
# Scan → verify trust → assess compliance
python3 {baseDir}/scripts/checker.py pipeline --skill "some-skill" --policy "production"
```