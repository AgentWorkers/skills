---
name: github-actions-retry-recovery-audit
description: Audit GitHub Actions 采用“失败后重试”的恢复机制，以量化因代码不稳定导致的重复执行所造成的资源浪费。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---
# GitHub Actions 重试恢复审计（Retry Recovery Audit）

使用此技能可以找出那些反复失败但最终成功的工作流/任务片段，从而帮助团队针对那些浪费时间最多的失败尝试进行优化。

## 功能概述：
- 读取一个或多个 GitHub Actions 工作流运行的 JSON 输出文件
- 按仓库、工作流、分支和提交（`headSha`）对尝试进行分组
- 检测出“恢复序列”：即一次或多次失败尝试之后紧接着成功的尝试
- 计算每个序列中在首次成功之前所浪费的时间（以分钟为单位）
- 生成文本或 JSON 格式的输出，用于故障排查仪表板和持续集成（CI）的失败检测机制

## 输入参数：
- `RUN_GLOB`（默认值：`artifacts/github-actions/*.json`）：需要分析的 JSON 文件路径模式
- `TOP_N`（默认值：`20`）：显示的序列数量上限
- `OUTPUT_FORMAT`（`text` 或 `json`，默认值：`text`）：输出格式
- `WARN_WASTE_MINUTES`（默认值：`20`）：警告级别的时间浪费阈值（分钟）
- `CRITICAL_WASTE_MINUTES`（默认值：`60`）：严重级别的时间浪费阈值（分钟）
- `FAIL_ON_CRITICAL`（`0` 或 `1`，默认值：`0`）：是否在出现严重级别失败时停止执行
- `WORKFLOW_MATCH`、`WORKFLOW_EXCLUDE`（正则表达式，可选）：需要匹配或排除的工作流名称
- `BRANCH_MATCH`、`BRANCH_EXCLUDE`（正则表达式，可选）：需要匹配或排除的分支名称
- `REPO_MATCH`、`REPO_EXCLUDE`（正则表达式，可选）：需要匹配或排除的仓库名称

## 收集工作流运行数据（代码示例）：
```bash
gh run view <run-id> --json databaseId,workflowName,headBranch,headSha,conclusion,createdAt,updatedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## 执行审计（代码示例）：
- **文本报告：**
```bash
RUN_GLOB='artifacts/github-actions/*.json' \
WARN_WASTE_MINUTES=20 \
CRITICAL_WASTE_MINUTES=60 \
bash skills/github-actions-retry-recovery-audit/scripts/retry-recovery-audit.sh
```

- **JSON 输出（包含失败检测机制）：**
```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-retry-recovery-audit/scripts/retry-recovery-audit.sh
```

## 输出格式说明：
- 在文本模式下，程序返回 `0` 表示审计完成。
- 当 `FAIL_ON_CRITICAL` 设置为 `1` 且存在严重级别的恢复序列时，程序返回 `1`。
- 文本输出包含总结信息以及按浪费时间排序的恢复序列。
- JSON 输出包含总结信息、按时间排序的恢复序列列表以及严重级别的恢复序列列表。