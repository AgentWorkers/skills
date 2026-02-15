---
name: openclaw-shield-quickscan
description: "执行一次快速的 OpenClaw Shield 扫描，并总结可操作的发现结果。当用户要求扫描文件夹或代码库以检测凭证盗用、数据泄露行为、可疑命令执行、风险网络活动或生成快速的安全评估报告时，可以使用此功能。"
---

# OpenClaw Shield 快速扫描

使用此功能可快速扫描目标文件或文件夹，并生成简短的扫描结果摘要。

## 输入参数

- `target_path`（必填）：需要扫描的文件夹或文件路径。
- `scanner_path`（可选）：默认值为 `projects/OpenClaw-Shield/src/scanner.py`。
- `output_path`（可选）：默认值为 `/tmp/openclaw-shield-report.json`。

## 工作流程

1. 验证 `target_path` 是否存在。
2. 验证 `scanner_path` 是否存在。如果不存在，请提示用户安装 OpenClaw Shield。
3. 运行扫描工具。
4. 使用 `scripts/summarize_report.py` 对扫描结果进行汇总。
5. 返回问题的严重程度统计信息、主要发现结果以及后续处理建议。

## 命令示例

```bash
python3 "projects/OpenClaw-Shield/src/scanner.py" "<target_path>" --output "/tmp/openclaw-shield-report.json"
python3 scripts/summarize_report.py "/tmp/openclaw-shield-report.json"
```

如果扫描工具未安装：

```bash
clawhub install openclaw-shield
```

## 报告规范

- 必须包含问题的总数及严重程度分布。
- 如果存在问题，需列出严重程度最高的 5 个问题，包括文件路径和具体行号。
- 如果未发现任何问题，需明确说明扫描已完成且未检测到任何异常。
- 保持报告内容简洁明了，便于操作。