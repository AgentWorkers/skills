---
name: github-actions-branch-drift-audit
description: 通过将分支级别的 GitHub Actions 的失败次数与运行时间变化与主线（mainline）的基线进行比较，来检测其可靠性的变化趋势。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---
# GitHub Actions 分支漂移审计

使用此技能可以在特定分支的持续集成（CI）可靠性问题扩散到主线发布流程之前及时发现并处理这些问题。

## 功能介绍
- 读取 GitHub Actions 的运行结果 JSON 文件
- 按仓库、工作流和分支对运行结果进行分组
- 为每个仓库/工作流选择一个基准分支（默认为 `main` 或 `master`）
- 将每个非基准分支与基准分支进行比较，检查以下指标：
  - 失败率漂移（百分比）
  - 平均运行时间漂移（比率）
- 标记警告/严重级别的漂移情况，并支持设置 CI 失败门（fail gate）
- 生成文本或 JSON 格式的输出，用于管道检查（pipeline checks）和问题排查（triage dashboards）

## 输入参数
可选参数：
- `RUN_GLOB` （默认值：`artifacts/github-actions/*.json`）
- `TOP_N` （默认值：`20`）
- `OUTPUT_FORMAT` （`text` 或 `json`，默认值：`text`）
- `MIN_RUNS_PER_BRANCH` （默认值：`2`）
- `MIN_BRANCHES` （默认值：`2`）
- `BASELINE_BRANCH_MATCH` （默认值：`^(main|master)$`）
- `WORKFLOW_MATCH` （正则表达式，可选）
- `WORKFLOW_EXCLUDE` （正则表达式，可选）
- `REPO_MATCH` （正则表达式，可选）
- `REPO_EXCLUDE` （正则表达式，可选）
- `FAILURE_DRIFT_WARN_PP` （默认值：`10`）
- `FAILURE_DRIFT_CRITICAL_PP` （默认值：`25`）
- `RUNTIME_DRIFT_WARN_RATIO` （默认值：`1.25`）
- `RUNTIME_DRIFT_CRITICAL_RATIO` （默认值：`1.6`）
- `FAIL_ON_CRITICAL` （`0` 或 `1`，默认值：`0`）

## 收集运行结果 JSON 数据

```bash
gh run view <run-id> --json databaseId,workflowName,event,conclusion,headBranch,headSha,createdAt,updatedAt,startedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## 运行审计流程

**文本报告：**

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
BASELINE_BRANCH_MATCH='^(main|release/.*)$' \
MIN_RUNS_PER_BRANCH=3 \
bash skills/github-actions-branch-drift-audit/scripts/branch-drift-audit.sh
```

**包含失败门（fail gate）的 JSON 输出：**

```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-branch-drift-audit/scripts/branch-drift-audit.sh
```

**使用预定义的测试用例（bundled fixtures）运行审计流程：**

```bash
RUN_GLOB='skills/github-actions-branch-drift-audit/fixtures/*.json' \
bash skills/github-actions-branch-drift-audit/scripts/branch-drift-audit.sh
```

## 输出规范
- 在文本模式下，程序退出代码为 `0` 表示审计成功
- 当 `FAIL_ON_CRITICAL` 设置为 `1` 且存在一个或多个严重级别的漂移情况时，程序退出代码为 `1`
- 文本模式会显示汇总信息以及按严重程度排序的分支漂移数据
- JSON 模式会显示汇总信息、漂移数据以及仅包含严重级别问题的数据