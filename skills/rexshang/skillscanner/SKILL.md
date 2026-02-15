---
name: skillscanner
version: 1.0.0
description: 来自 Gen Digital 的 ClawHub 技能安全扫描器。该扫描器通过扫描 API 来检查技能的安全性。
author: Rex Shang
license: MIT
keywords: [security, audit, scan, vet, skills, safety, skill_scanner, trust, secure]
triggers: ["skill security", "vet skill", "scan skill", "is this skill safe", "skillscanner", "skill_scanner", "audit skill", "scan skills", "secure skill", "trusted skill", "trust skill"]
---

# SkillScanner — 用于检测 ClawHub 技能安全性的扫描工具

> **“信任，但需验证。”**

SkillScanner 通过调用扫描 API 来检测 ClawHub 中技能的安全性。您需要提供技能的 URL，API 会返回该技能的安全状态和风险等级。只有当安全状态为 **SAFE** 时，才能继续使用该技能。

---

## 如何扫描技能（代理使用说明）

1. 使用实际的技能 URL 运行扫描操作（格式：`https://clawhub.ai/author/skill-name`）：

   ```bash
   curl --request POST --url "https://ai.gendigital.com/api/scan/lookup" \
     --header "Content-Type: application/json" \
     --data '{"skillUrl":"https://clawhub.ai/AUTHOR/SKILL_SLUG"}'
   ```

   请将 `AUTHOR` 替换为实际的作者 ID，将 `SKILL_SLUG` 替换为 ClawHub URL 中的技能标识符。

2. **解析响应结果**：
   - **`status: "done"`** — 查看 `severity` 字段以获取安全评估结果。
   - **`status: "analysis_pending"`** — 该技能正在等待人工审核。请勿将其视为安全技能，应告知用户该技能正在审核中。

3. **决定是否继续使用**：
   - 仅当 `severity` 为 **SAFE** 时，才能继续使用该技能。
   - 如果 `severity` 为其他值（如 `WARNING`、`DANGEROUS`、`MALICIOUS`），则应建议用户谨慎使用，并在审核完成或风险被清除之前避免使用该技能。

---

## 快速入门

```bash
# Example: scan a skill by its ClawHub URL
curl --request POST --url "https://ai.gendigital.com/api/scan/lookup" \
  --header "Content-Type: application/json" \
  --data '{"skillUrl":"https://clawhub.ai/author/skill-name"}'
```

解析 JSON 响应：根据上述说明，使用 `status` 和 `severity` 字段来判断技能的安全性。

---

## API 响应逻辑

| `status`           | 含义                        | 应采取的行动            |
|--------------------|----------------------|-------------------|
| `done`             | 扫描完成                        | 根据 `severity` 的结果决定是否可以使用该技能。 |
| `analysis_pending` | 正在等待人工审核                    | 告知用户该技能尚未通过审核，不可视为安全技能。 |

| `severity` （当 `status` = `done` 时） | 安全建议                         |
|-------------------------------------|-------------------------|
| **SAFE**                            | 可以安全使用。                         |
| 其他值                          | 建议谨慎使用；在审核完成前避免使用。         |

---

## 为什么这很重要

技能可能执行代码并访问您的系统环境。潜在风险包括：

| 风险              | 影响                         |
|------------------|-----------------------------|
| **执行任意代码**         | 会导致系统被完全控制                 |
| **访问您的文件系统**       | 可能导致数据被盗或系统被勒索软件感染       |
| **读取环境变量**       | 可能导致 API 密钥被窃取             |
| **通过 HTTP 泄露数据**       | 会造成隐私泄露                     |
| **安装恶意依赖项**       | 可能引发供应链攻击                 |

SkillScanner 通过扫描 API 帮助您在使用技能之前判断其安全性。

---

## 限制

- API 只能反映后端的当前安全评估结果；一些复杂或新型的威胁可能无法被检测到。
- 当 `status` 为 `analysis_pending` 时，表示人工审核尚未完成——应将其视为 “未知风险”，不可视为安全技能。

在不确定的情况下，请结合沙箱环境、最小权限原则以及人工审核来使用该工具。

---

**相关链接：**
- [Agent Trust Hub](https://ai.gendigital.com)