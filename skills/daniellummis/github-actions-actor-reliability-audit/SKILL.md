---
name: github-actions-actor-reliability-audit
description: 通过“Actor”机制来审计 GitHub Actions 的运行可靠性，从而识别出高风险贡献者和存在问题的自动化脚本所有者。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---
# GitHub Actions 演员（Actor）可靠性审计

使用此技能来评估哪些演员（人类或机器人）产生的 GitHub Actions 结果最不可靠。

## 该技能的功能：
- 读取 GitHub Actions 的运行结果 JSON 数据
- 按演员对运行结果进行分组（可选：按演员 + 工作流分组）
- 统计每个演员的失败率、失败次数以及连续失败的次数
- 为故障情况分配严重等级（`ok`、`warn`、`critical`），以便进行故障排查和持续集成（CI）策略判断
- 以文本或 JSON 格式输出结果，以便自动化处理

## 输入参数（可选）：
- `RUN_GLOB` （默认值：`artifacts/github.actions/*.json`）：需要分析的 JSON 文件路径
- `TOP_N` （默认值：`20`）：显示的排名前 N 个演员
- `OUTPUT_FORMAT` （`text` 或 `json`，默认值：`text`）：输出格式
- `GROUP_BY` （`actor` 或 `actor-workflow`，默认值：`actor`）：分组方式
- `FAILURE_CONCLUSIONS` （逗号分隔的字符串，默认值：`failure,cancelled,timed_out,startup_failure`）：故障原因（如失败、取消、超时、启动失败）
- `MIN_RUNS` （最小运行次数，默认值：`5`）：必须满足的最低运行次数
- `WARN_FAILURE_RATE` （0..1，默认值：`0.25`）：警告级别的失败率阈值
- `CRITICAL_FAILURE_RATE` （0..1，默认值：`0.5`）：严重级别的失败率阈值
- `WARN_FAILED_RUNS` （默认值：`4`）：达到警告级别的失败次数
- `CRITICAL_FAILED_RUNS` （默认值：`8`）：达到严重级别的失败次数
- `WARN_FAILURE_STREAK` （默认值：`2`）：连续警告失败的次数
- `CRITICAL_FAILURE_STREAK` （默认值：`4`）：连续严重失败的次数
- `ACTOR_MATCH` / `ACTOR_EXCLUDE` （正则表达式，可选）：匹配/排除的演员名称
- `WORKFLOW_MATCH` / `WORKFLOW_EXCLUDE` （正则表达式，可选）：匹配/排除的工作流名称
- `BRANCH_MATCH` / `BRANCH_EXCLUDE` （正则表达式，可选）：匹配/排除的仓库分支
- `EVENT_MATCH` / `EVENT_EXCLUDE` （正则表达式，可选）：匹配/排除的事件类型
- `REPO_MATCH` / `REPO_EXCLUDE` （正则表达式，可选）：匹配/排除的仓库名称
- `FAIL_ON_CRITICAL` （`0` 或 `1`，默认值：`0`）：是否在发生严重故障时停止所有相关操作

## 收集运行结果 JSON 数据（代码示例）：
```bash
gh run view <run-id> --json databaseId,workflowName,event,headBranch,conclusion,createdAt,updatedAt,url,repository,actor,triggeringActor \
  > artifacts/github-actions/run-<run-id>.json
```

## 运行审计流程：
- 生成文本报告：```bash
RUN_GLOB='artifacts/github-actions/*.json' \
bash skills/github-actions-actor-reliability-audit/scripts/actor-reliability-audit.sh
```
- 生成 JSON 格式输出结果及故障判断信息：```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-actor-reliability-audit/scripts/actor-reliability-audit.sh
```
- 使用预定义的测试用例对运行结果进行进一步分析：```bash
RUN_GLOB='skills/github-actions-actor-reliability-audit/fixtures/*.json' \
bash skills/github-actions-actor-reliability-audit/scripts/actor-reliability-audit.sh
```

## 输出格式说明：
- 在文本模式下，程序返回退出代码 `0`；当 `FAIL_ON_CRITICAL` 设置为 `1` 且存在至少一个严重故障的演员组时，返回退出代码 `1`
- 文本模式下会显示故障总结及排名后的演员组
- JSON模式下会显示故障总结、排名后的演员组以及所有出现严重故障的演员组