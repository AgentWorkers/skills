---
name: openclaw-policy-check
description: "在执行操作之前，扫描代码库以检测可能存在的安全风险。适用于用户需要快速进行安全预检查、政策执行扫描、可疑代码排查、检测不安全命令、秘密泄露以及危险shell行为的情况。"
---

# OpenClaw 政策检查

执行一次轻量级的政策扫描，以检测代码和脚本中常见的高风险模式。

## 输入参数

- `target_path`（必填）：需要扫描的文件或目录。
- `fail_on`（可选）：非零退出状态的严重性阈值。可选值：`critical`（严重）、`high`（高）、`medium`（中）、`low`（低）。
- `json_output`（可选）：以原始 JSON 格式输出结果。

## 工作流程

1. 在目标路径上运行 `scripts/policy_check.py` 脚本。
2. 查看严重性统计结果和主要发现内容。
3. 如果存在问题，优先处理 `critical`（严重）和 `high`（高）级别的问题。
4. 为每个被标记的问题提供具体的修复建议。

## 命令示例

```bash
python3 scripts/policy_check.py "<target_path>"
python3 scripts/policy_check.py "<target_path>" --json
python3 scripts/policy_check.py "<target_path>" --fail-on high
```

## 响应规范

- 必须包含总的问题数量及严重性分布。
- 显示主要问题的详细信息，包括文件路径、问题所在的行号、规则ID以及问题原因。
- 如果未发现任何问题，需明确说明未检测到任何政策违规行为。
- 修复建议应具体且简洁。