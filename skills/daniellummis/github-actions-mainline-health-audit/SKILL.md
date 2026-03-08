---
name: github-actions-mainline-health-audit
description: 通过评估关键工作流程的失败率、连续失败次数以及“虚假成功”（即看似成功但实际上存在问题的情况）的风险，来审计 GitHub Actions 的主线分支（mainline branch）的可靠性。
version: 1.4.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---
# GitHub Actions 主线健康审计（Mainline Health Audit）

使用此技能来检测受保护分支（main/master/release）上的不稳定工作流，以防止它们在不知不觉中降低交付的可靠性。

## 该技能的功能：
- 读取 GitHub Actions 的运行结果 JSON 文件
- 根据配置的正则表达式筛选出主线/受保护分支
- 按仓库、工作流、分支和事件进行分组
- 通过以下指标评估风险：
  - 失败率
  - 连续失败的天数
  - 自上次成功运行以来的时间
- 根据可配置的阈值标记警告/严重风险组
- 生成文本或 JSON 格式的输出，用于持续集成（CI）检查和运维仪表板

## 输入参数（可选）：
- `RUN_GLOB`（默认值：`artifacts/github-actions/*.json`）
- `TOP_N`（默认值：`20`）
- `OUTPUT_FORMAT`（`text` 或 `json`，默认值：`text`）
- `MIN_RUNS`（默认值：`2`）
- `MAINLINE_BRANCH_MATCH`（默认值：`^(main|master|release.*)$`）
- `WORKFLOW_MATCH`（正则表达式，可选）
- `WORKFLOW_EXCLUDE`（正则表达式，可选）
- `EVENT_MATCH`（正则表达式，可选）
- `EVENT_EXCLUDE`（正则表达式，可选）
- `REPO_MATCH`（正则表达式，可选）
- `REPO_EXCLUDE`（正则表达式，可选）
- `HEAD_SHA_MATCH`（正则表达式，可选）
- `HEAD_SHA_EXCLUDE`（正则表达式，可选）
- `CONCLUSION_MATCH`（正则表达式，可选）
- `CONCLUSION_EXCLUDE`（正则表达式，可选）
- `RUN_ID_MATCH`（正则表达式，可选）
- `RUN_ID_EXCLUDE`（正则表达式，可选）
- `RUN_URL_MATCH`（正则表达式，可选）
- `RUN_URL_EXCLUDE`（正则表达式，可选）
- `FAILWARN_PERCENT`（默认值：`20`）
- `FAIL_CRITICAL_PERCENT`（默认值：`40`）
- `STALE_SUCCESS_days`（默认值：`7`）
- `WARN SCORE`（默认值：`30`）
- `CRITICAL SCORE`（默认值：`55`）
- `FAIL_ON_CRITICAL`（`0` 或 `1`，默认值：`0`）

## 收集运行结果 JSON 数据（代码块示例）：
```bash
gh run view <run-id> --json databaseId,workflowName,event,conclusion,headBranch,headSha,createdAt,updatedAt,startedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## 运行流程（代码块示例）：
- 生成文本报告：
```bash
RUN_GLOB='artifacts/github-actions/*.json' \
MAINLINE_BRANCH_MATCH='^(main|release/.*)$' \
HEAD_SHA_MATCH='^[a-f0-9]{7,40}$' \
CONCLUSION_EXCLUDE='^(success)$' \
RUN_ID_MATCH='^50(0[1-5])$' \
MIN_RUNS=3 \
bash skills/github-actions-mainline-health-audit/scripts/mainline-health-audit.sh
```

- 生成包含失败信息的 JSON 输出：
```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-mainline-health-audit/scripts/mainline-health-audit.sh
```

- 使用预定义的测试用例运行工作流：
```bash
RUN_GLOB='skills/github-actions-mainline-health-audit/fixtures/*.json' \
bash skills/github-actions-mainline-health-audit/scripts/mainline-health-audit.sh
```

## 输出格式说明：
- 在文本模式下，程序以 `0` 结束执行（默认情况）
- 当 `FAIL_ON_critical` 设置为 `1` 且存在一个或多个严重风险组时，程序以 `1` 结束执行
- 文本模式会显示风险组的排名和总结信息
- JSON 模式会显示风险组的排名、评分以及详细信息