---
name: github-actions-failure-spike-audit
description: 通过比较最近一次运行与基线运行期间的数据，按工作流组检测 GitHub Actions 失败率的突然飙升。
version: 1.0.0
metadata: {"openclaw":{"requires":{"bins":["bash","python3"]}}}
---
# GitHub Actions 失败率激增审计

使用此技能可以在工作流出现性能下降（例如新的测试失败、部署流程出错、依赖项更新失败或基础设施故障）时及时发现这些问题，从而避免这些问题演变成长期存在的问题。

## 该技能的功能：
- 读取 GitHub Actions 的运行日志（以 JSON 格式保存）
- 按仓库、工作流、分支和事件进行数据分组
- 将每个分组分为“近期运行记录”和“基准历史记录”
- 比较近期失败率与基准失败率
- 根据失败率的增幅和严重程度（正常、警告、严重）对问题进行分类
- 生成文本或 JSON 格式的输出结果，以便用于持续集成（CI）自动化流程

## 输入参数（可选）：
- `RUN_GLOB` （默认值：`artifacts/github-actions/*.json`）：需要分析的 JSON 文件路径
- `TOP_N` （默认值：`20`）：需要显示的记录数量
- `OUTPUT_FORMAT` （`text` 或 `json`，默认值：`text`）：输出格式
- `RECENT_RUNS` （默认值：`4`）：近期运行的记录数量
- `MIN_RECENT_RUNS` （默认值：`3`）：用于计算基准值的最近运行记录数量
- `MIN_BASELINE_RUNS` （默认值：`4`）：用于计算基准值的最近运行记录数量
- `WARN_SPIKE_PCT` （默认值：`15`）：警告级别的失败率阈值
- `CRITICAL_SPIKE_PCT` （默认值：`30`）：严重级别的失败率阈值
- `WARN_RECENT_FAILURE_RATE` （默认值：`25`）：警告级别的失败率阈值
- `CRITICAL_RECENT_FAILURE_RATE` （默认值：`45`）：严重级别的失败率阈值
- `WORKFLOW_MATCH` （正则表达式，可选）：需要匹配的工作流名称
- `WORKFLOW_EXCLUDE` （正则表达式，可选）：需要排除的工作流名称
- `BRANCH_MATCH` （正则表达式，可选）：需要匹配的分支名称
- `BRANCH_EXCLUDE` （正则表达式，可选）：需要排除的分支名称
- `EVENT_MATCH` （正则表达式，可选）：需要匹配的事件类型
- `EVENT_EXCLUDE` （正则表达式，可选）：需要排除的事件类型
- `REPO_MATCH` （正则表达式，可选）：需要匹配的仓库名称
- `REPO_EXCLUDE` （正则表达式，可选）：需要排除的仓库名称
- `FAIL_ON_CRITICAL` （`0` 或 `1`，默认值：`0`）：当失败率达到严重级别时是否触发警报

## 数据收集（代码示例）：
```bash
gh run view <run-id> --json databaseId,workflowName,event,conclusion,headBranch,headSha,createdAt,updatedAt,startedAt,url,repository \
  > artifacts/github-actions/run-<run-id>.json
```

## 运行审计流程（代码示例）：
- 生成文本报告：```bash
RUN_GLOB='artifacts/github-actions/*.json' \
RECENT_RUNS=8 \
WARN_SPIKE_PCT=12 \
bash skills/github-actions-failure-spike-audit/scripts/failure-spike-audit.sh
```
- 生成 JSON 格式的输出结果及失败率统计信息：```bash
RUN_GLOB='artifacts/github-actions/*.json' \
OUTPUT_FORMAT=json \
FAIL_ON_CRITICAL=1 \
bash skills/github-actions-failure-spike-audit/scripts/failure-spike-audit.sh
```
- 对包含固定测试用例的工作流进行额外审计：```bash
RUN_GLOB='skills/github-actions-failure-spike-audit/fixtures/*.json' \
bash skills/github-actions-failure-spike-audit/scripts/failure-spike-audit.sh
```

## 输出格式说明：
- 在文本模式下，程序以 `0` 退出；当 `FAIL_ON_CRITICAL` 设置为 `1` 且存在至少一个严重级别的问题时，程序以 `1` 退出
- 文本模式下会显示问题总结及按失败率排序的问题组
- JSON模式下会显示问题总结、按失败率排序的问题组以及所有严重级别的问题组