---
name: github-actions-run-gap-audit
description: 通过计算运行间隔的中位数以及当前的不活跃时间差，来检测 GitHub Actions 工作流组是否已停止按照正常的节奏运行。
version: 1.1.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---
# GitHub Actions 运行间隙审计

使用此技能来检测工作流组是否出现异常的停滞状态（例如：触发器失效、调度计划中断、自动化功能被禁用、分支版本发生变动等）。

## 该技能的功能：
- 读取 GitHub Actions 的运行日志 JSON 文件
- 按仓库、工作流、分支和事件进行分组
- 计算历史运行频率（中位数和第 90 百分位的间隔时间）
- 将当前的不活跃状态与历史运行频率进行比较
- 评估风险等级（分为“正常”、“警告”和“严重”）
- 生成文本或 JSON 格式的报告，用于持续集成（CI）检查和自动化监控

## 输入参数：
- `RUN_GLOB`（可选）：要检查的 JSON 文件路径模式（默认：`artifacts/github-actions/*.json`）
- `TOP_N`（可选）：显示的顶级结果数量（默认：20）
- `OUTPUT_FORMAT`（可选）：输出格式（“text”或“json”，默认：“text”）
- `MIN_RUNS`（可选）：至少需要检查的运行记录数量（默认：4）
- `WARN_GAP_MULTIPLIER`（可选）：警告等级的判断倍数（默认：2.0）
- `CRITICAL_gap_MULTIPLIER`（可选）：严重等级的判断倍数（默认：3.5）
- `MINWARN_GAP_HOURS`（可选）：警告等级的最低不活跃时间（默认：12 小时）
- `MIN_CRITICAL_gap_HOURS`（可选）：严重等级的最低不活跃时间（默认：24 小时）
- `WORKFLOW_MATCH`（可选）：工作流名称的正则表达式匹配规则
- `WORKFLOW_EXCLUDE`（可选）：需要排除的工作流名称的正则表达式匹配规则
- `BRANCH_MATCH`（可选）：分支名称的正则表达式匹配规则
- `BRANCH_EXCLUDE`（可选）：需要排除的分支名称的正则表达式匹配规则
- `EVENT_MATCH`（可选）：事件名称的正则表达式匹配规则
- `EVENT_EXCLUDE`（可选）：需要排除的事件名称的正则表达式匹配规则
- `REPO_MATCH`（可选）：仓库名称的正则表达式匹配规则
- `REPO_EXCLUDE`（可选）：需要排除的仓库名称的正则表达式匹配规则
- `RUN_ID_MATCH`（可选）：运行 ID 的正则表达式匹配规则
- `RUN_ID_EXCLUDE`（可选）：需要排除的运行 ID 的正则表达式匹配规则
- `RUN_URL_MATCH`（可选）：运行 URL 的正则表达式匹配规则
- `RUN_URL_EXCLUDE`（可选）：需要排除的运行 URL 的正则表达式匹配规则
- `NOW_ISO`（可选）：用于确定性 CI 测试的固定时间戳（默认：当前时间）
- `FAIL_ON_CRITICAL`（可选）：当检测到严重问题时是否终止整个流程（默认：0 或 1）

## 数据收集（代码示例）：
```bash
gh run view <run-id> --json databaseId,workflowName,event,conclusion,headBranch,headSha,createdAt,updatedAt,startedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## 运行逻辑：
- 根据输入参数执行相应的数据处理逻辑
- 生成文本报告或 JSON 输出结果

### 文本报告示例：
```bash
RUN_GLOB='artifacts/github-actions/*.json' \
MIN_RUNS=5 \
WARN_GAP_MULTIPLIER=2.25 \
bash skills/github-actions-run-gap-audit/scripts/run-gap-audit.sh
```

### 带有失败判断功能的 JSON 输出示例：
```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-run-gap-audit/scripts/run-gap-audit.sh
```

### 针对特定运行范围的筛选示例：
```bash
RUN_GLOB='artifacts/github-actions/*.json' \
RUN_ID_MATCH='^(88|89)' \
RUN_URL_EXCLUDE='rerun' \
OUTPUT_FORMAT=json \
bash skills/github-actions-run-gap-audit/scripts/run-gap-audit.sh
```

### 使用预定义测试用例的运行示例：
```bash
RUN_GLOB='skills/github-actions-run-gap-audit/fixtures/*.json' \
NOW_ISO='2026-03-07T00:00:00Z' \
bash skills/github-actions-run-gap-audit/scripts/run-gap-audit.sh
```

## 输出格式说明：
- 在文本模式下，程序以 `0` 退出（表示正常完成）
- 当 `FAIL_ON_CRITICAL` 设置为 `1` 且存在至少一个严重问题时，程序以 `1` 退出
- 文本模式会显示汇总信息及按风险等级排序的工作流组
- JSON 模式会显示汇总信息、按风险等级排序的工作流组以及严重问题的详细信息