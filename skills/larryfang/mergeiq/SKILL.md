---
name: mergeiq
description: 使用一个四维框架来评估任何 GitLab 提交（MR）或 GitHub 合并请求（PR）的复杂性：规模（20%）、认知负荷（30%）、审查工作量（30%）以及风险/影响（20%）。该工具适用于 GitLab 或 GitHub，且无需任何外部依赖。在需要根据复杂性来审查、分类、评分或优先处理拉取请求（pull requests）和合并请求（merge requests）时可以使用。
license: MIT
metadata:
  author: larry.l.fang@gmail.com
  version: "1.0.0"
  tags: gitlab, github, pull-request, merge-request, code-review, engineering, dora, complexity
---
# MR/PR 复杂度评分器

这是一个与具体提供者无关的复杂度评分工具，适用于 GitLab 和 GitHub 的合并请求（Merge Requests）和拉取请求（Pull Requests）。该评分器基于一个四维框架，能够真正反映代码审查中的“复杂性”——而不仅仅是代码行数的变化。

## 复杂度维度

| 维度              | 权重    | 测量内容                                                         |
|-----------------|--------|---------------------------------------------------------------|
| 代码规模            | 20%    | 变更的代码量（对数计算——大型合并请求的评分会迅速升高）                         |
| 认知负担          | 30%    | 目录的层级结构、跨模块的变更、文件的多样性                            |
| 审查工作量          | 30%    | 审查的深度、审核者的数量、审批的迭代次数                            |
| 风险/影响            | 20%    | 可能导致系统故障的变更、数据迁移、安全相关问题、依赖关系                    |

**评分等级**：简单 / 中等 / 复杂 / 高度复杂

## 使用场景

- 在审查会议前，按复杂度对待审的拉取请求进行分类
- 标记高复杂度的合并请求，要求进行二次审核
- 为团队生成每周的复杂度趋势报告
- 了解某个合并请求为何耗时较长（通过各维度的数据进行分析）
- 用于构建工程总监的仪表盘（详见 score_mr.py 文件）

## 快速入门

```bash
# Score a GitHub PR (basic — just the PR object)
curl -s "https://api.github.com/repos/OWNER/REPO/pulls/NUMBER" \
     -H "Authorization: Bearer $GITHUB_TOKEN" \
     | python score_mr.py --provider github

# Score a GitLab MR (with diff stats)
curl -s "https://gitlab.com/api/v4/projects/PROJECT_ID/merge_requests/IID?include_diff_stats=true" \
     -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
     | python score_mr.py --provider gitlab

# Richer scoring — fetch files + reviews too
curl -s ".../pulls/NUMBER" > pr.json
curl -s ".../pulls/NUMBER/files" > files.json
curl -s ".../pulls/NUMBER/reviews" > reviews.json
python score_mr.py --provider github --pr pr.json --files files.json --reviews reviews.json
```

## 示例输出

```json
{
  "provider": "github",
  "id": 412,
  "title": "Migrate auth service to OAuth2",
  "score": {
    "total": 74.2,
    "tier": "complex",
    "size": 68.0,
    "cognitive": 81.5,
    "review_effort": 72.0,
    "risk_impact": 60.0
  },
  "summary": "High mental load: 14 files across 6 directories, 3 reviewers involved",
  "tier_insight": "Needs careful review — high cognitive load and cross-module impact.",
  "stats": {
    "additions": 412,
    "deletions": 87,
    "files_changed": 14,
    "reviewers": 3,
    "discussions": 9,
    "net_lines": 325
  }
}
```

## 文件相关操作

```
mr-complexity-scorer/
  SKILL.md                      # This file
  mr_complexity_service.py      # Core 4-dimension scoring engine (pure Python)
  score_mr.py                   # CLI: pipe in API JSON, get complexity JSON out
  requirements.txt              # No external deps — stdlib only, Python 3.9+
  adapters/
    gitlab_adapter.py           # GitLab MR API dict → MRData
    github_adapter.py           # GitHub PR API dict → MRData
```

## 在你的代码中如何使用该评分器

```python
from mr_complexity_service import MRComplexityCalculator, MRData
from adapters.github_adapter import github_pr_to_mrdata

# Build MRData from a GitHub PR dict (from API or webhook payload)
mr_data = github_pr_to_mrdata(
    pr=pr_dict,
    files=files_list,       # optional: /pulls/:number/files
    commits=commits_list,   # optional: /pulls/:number/commits
    reviews=reviews_list,   # optional: /pulls/:number/reviews
)

calculator = MRComplexityCalculator()
result = calculator.calculate(mr_data)

print(result.complexity_tier)   # "complex"
print(result.total_score)       # 74.2
print(result.human_summary)     # "High mental load: ..."
```

## 数据扩展——值得获取的额外信息

| 需要调用的额外 API          | 可提供的功能                         | 是否值得获取？         |
|------------------|----------------------------------|----------------------|
| `/pulls/:n/files`        | 文件路径的认知分析                          | 始终值得获取            |
| `/pulls/:n/reviews`       | 准确的审核者数量及审批次数                        | 对于分析审查工作量很有帮助     |
| `/pulls/:n/commits`       | 检测是否存在可能导致系统故障的变更                    | 可供参考                 |
| `/pulls/:n/comments`      | 实时显示评论数量                          | 可选                 |

即使不使用这些扩展数据，评分器也能正常工作（它使用合并请求对象中的 `changed_files`、`review_comments` 和 `requested_reviewers` 字段）。不过，扩展后的数据能够提高评分的准确性。

## 扩展到其他平台

只需实现一个简单的适配器，将你的平台对应的合并请求/拉取请求数据结构映射到 `MRData` 格式即可：

```python
from mr_complexity_service import MRData

def linear_issue_to_mrdata(issue: dict) -> MRData:
    return MRData(
        iid=issue["number"],
        title=issue["title"],
        # ... map your fields
    )
```

支持的平台：GitLab、GitHub、Gitea、Bitbucket、Azure DevOps——任何具有合并请求/拉取请求元数据的功能平台。

## 权重调整

```python
from mr_complexity_service import MRComplexityCalculator, ComplexityConfig

config = ComplexityConfig(
    weight_size=0.15,
    weight_cognitive=0.35,
    weight_review=0.30,
    weight_risk=0.20,
)
calculator = MRComplexityCalculator(config=config)
```