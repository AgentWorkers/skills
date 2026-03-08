---
name: github-actions-conclusion-volatility-audit
description: 审计 GitHub Actions 工作流的稳定性，以便在问题变得严重之前发现并解决不稳定的管道（即存在故障风险的管道）。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---
# GitHub Actions：Volatility Audit（波动性审计）

使用此技能来检测那些在成功与失败之间频繁切换的工作流程。

## 功能说明：
- 读取一个或多个工作流程运行的 JSON 输出文件。
- 按仓库、工作流程和分支对运行结果进行分组。
- 通过分析运行历史中的状态变化来计算工作流程的“波动性”（即稳定性的变化程度）。
- 根据预设的不稳定性阈值（警告/严重级别）对相关组进行标记。
- 生成文本或 JSON 格式的输出，用于持续集成（CI）报告和质量控制流程。

## 输入参数（可选）：
- `RUN_GLOB`（默认值：`artifacts/github-actions/*.json`）：需要分析的 JSON 文件路径模式。
- `TOP_N`（默认值：`20`）：需要显示的运行结果数量。
- `OUTPUT_FORMAT`（`text` 或 `json`，默认值：`text`）：输出格式。
- `MIN_RUNS`（默认值：`5`）：在应用稳定性评级之前需要至少运行的次数。
- `WARN_INSTABILITY_PCT`（默认值：`35`）：达到警告级别的波动性阈值。
- `CRITICAL_INSTABILITY_PCT`（默认值：`60`）：达到严重级别的波动性阈值。
- `FAIL_ON_CRITICAL`（`0` 或 `1`，默认值：`0`）：当检测到严重级别不稳定性时是否触发失败响应。
- `WORKFLOW_MATCH`、`WORKFLOW_EXCLUDE`（正则表达式，可选）：用于筛选工作流程名称。
- `BRANCH_MATCH`、`BRANCH_EXCLUDE`（正则表达式，可选）：用于筛选分支名称。
- `REPO MATCH`、`REPO_EXCLUDE`（正则表达式，可选）：用于筛选仓库名称。

**被视为“失败”状态的结果包括：** `failure`、`cancelled`、`timed_out`、`action_required`、`startup_failure`。

## 收集运行结果数据（代码示例）：
```bash
gh run view <run-id> --json databaseId,workflowName,headBranch,conclusion,createdAt,updatedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## 生成报告（文本格式）：
```bash
RUN_GLOB='artifacts/github-actions/*.json' \
WARN_INSTABILITY_PCT=35 \
CRITICAL_INSTABILITY_PCT=60 \
bash skills/github-actions-conclusion-volatility-audit/scripts/conclusion-volatility-audit.sh
```

## 生成 JSON 格式的输出（包含失败状态信息）：
```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-conclusion-volatility-audit/scripts/conclusion-volatility-audit.sh
```

## 输出规范：
- 在报告模式下，程序的退出代码为 `0`。
- 当 `FAIL_ON_CRITICAL` 设置为 `1` 且检测到至少一个严重级别不稳定的组时，程序的退出代码为 `1`。
- 文本输出包含运行结果摘要及最不稳定的工作流程组信息。
- JSON 输出包含摘要、按稳定性排序的组列表以及所有处于严重不稳定状态的组信息。