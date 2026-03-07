---
name: github-actions-run-gap-audit
description: 通过计算运行间隔的中位数以及当前的不活跃时间差，来检测 GitHub Actions 工作流组是否已停止按照正常的频率运行。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---
# GitHub Actions：运行间隙审计（Run Gap Audit）

使用此技能来检测工作流组是否出现异常的静默状态（例如：触发器失效、调度计划中断、自动化功能被禁用、分支状态异常等）。

## 该技能的功能：
- 读取GitHub Actions的运行日志（JSON格式）
- 按仓库、工作流、分支和事件进行数据分组
- 计算历史运行频率（中位数和90%分位数的间隔时间）
- 将当前的不活跃状态与历史运行频率进行比较
- 评估风险等级（分为“正常”、“警告”或“严重”）
- 生成文本或JSON格式的输出结果，用于持续集成（CI）检查和自动化监控

## 输入参数：
- `RUN_GLOB`（可选）：需要分析的文件路径模式（默认值：`artifacts/github-actions/*.json`）
- `TOP_N`（可选）：显示的顶级结果数量（默认值：20）
- `OUTPUT_FORMAT`（可选）：输出格式（“text”或“json”，默认值：“text”）
- `MIN_RUNS`（可选）：最低运行次数要求（默认值：4）
- `WARN_GAP_MULTIPLIER`（可选）：警告风险的放大倍数（默认值：2.0）
- `CRITICAL_GAP_MULTIPLIER`（可选）：严重风险的放大倍数（默认值：3.5）
- `MINWARN_GAP_HOURS`（可选）：警告风险的最低持续时间（默认值：12小时）
- `MIN_CRITICAL_GAP_HOURS`（可选）：严重风险的最低持续时间（默认值：24小时）
- `WORKFLOW_MATCH`（可选）：工作流匹配模式（正则表达式）
- `WORKFLOW_EXCLUDE`（可选）：需要排除的工作流匹配模式（正则表达式）
- `BRANCH_MATCH`（可选）：分支匹配模式（正则表达式）
- `BRANCH_EXCLUDE`（可选）：需要排除的分支匹配模式（正则表达式）
- `EVENT_MATCH`（可选）：事件匹配模式（正则表达式）
- `EVENT_EXCLUDE`（可选）：需要排除的事件匹配模式（正则表达式）
- `REPO_MATCH`（可选）：仓库匹配模式（正则表达式）
- `REPO_EXCLUDE`（可选）：需要排除的仓库匹配模式（正则表达式）
- `NOW_ISO`（可选）：用于确定CI测试时间的固定时间戳（默认值：当前时间）
- `FAIL_ON_CRITICAL`（可选）：当检测到严重风险时是否触发失败（默认值：0）

## 数据收集（代码示例）：
```bash
gh run view <run-id> --json databaseId,workflowName,event,conclusion,headBranch,headSha,createdAt,updatedAt,startedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## 执行审计（代码示例）：
- 生成文本报告：
```bash
RUN_GLOB='artifacts/github-actions/*.json' \
MIN_RUNS=5 \
WARN_GAP_MULTIPLIER=2.25 \
bash skills/github-actions-run-gap-audit/scripts/run-gap-audit.sh
```

- 生成包含失败检测结果的JSON输出：
```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-run-gap-audit/scripts/run-gap-audit.sh
```

- 使用预定义的测试用例执行审计：
```bash
RUN_GLOB='skills/github-actions-run-gap-audit/fixtures/*.json' \
NOW_ISO='2026-03-07T00:00:00Z' \
bash skills/github-actions-run-gap-audit/scripts/run-gap-audit.sh
```

## 输出结果：
- 在文本模式下，输出结果代码为`0`（表示审计正常完成）
- 当`FAIL_ON_CRITICAL`设置为`1`且存在至少一个严重风险组时，输出代码为`1`
- 文本模式下会显示整体统计信息及按风险等级排序的工作流组列表
- JSON模式下会显示整体统计信息、按风险等级排序的工作流组列表以及严重风险组的详细信息