---
name: pr-triage
description: 使用基于视觉的分析方法来对 GitHub 的 Pull Request（PR）和 Issues 进行分类和评分。当用户需要根据项目的使命和价值观来优先处理、评分、审查、去重或批量处理这些请求/问题时，该工具非常实用。该工具支持新用户的上手流程（通过面试仓库所有者来协助编写视觉分析文档）、评分流程（使用评分标准对 PR 进行评估），以及报告生成（生成可执行的 Markdown 报告）。支持通过 `gh CLI` 与任何 GitHub 仓库配合使用。
---
# PR 分类与优先级评估

根据项目愿景文档对 GitHub 的 Pull Request (PR) 进行评分和优先级排序。整个流程分为三个步骤：入门、扫描、报告。

## 快速入门

```bash
# 1. Onboard: gather repo context, interview the owner
python3 scripts/onboard.py https://github.com/owner/repo --output-dir ./triage-config

# 2. Scan: score open PRs against the vision
python3 scripts/scan.py https://github.com/owner/repo ./triage-config/vision.md --output scores.json

# 3. Report: generate markdown triage reports
python3 scripts/report.py scores.json --output-dir ./triage-reports
```

## 流程

### 第一步：入门（每个仓库执行一次）

使用 `scripts/onboard.py` 并传入 GitHub 仓库的 URL。该脚本会通过 `gh` CLI 获取仓库的 `README.md`、`CONTRIBUTING.md`、最近发布的版本以及仓库元数据，然后生成一个面试提示。

根据面试提示向仓库所有者询问以下问题：

**项目概况与使命：**
1. 用一句话描述这个项目是什么，它是为了解决什么问题而存在的？
2. 该项目解决了哪些其他方案无法解决的问题？
3. 您有哪些不可妥协的原则（3-5 条）？

**优先级：**
4. 按重要性对贡献领域进行排序：安全性、漏洞修复、功能开发、性能优化、文档编写、测试、代码重构
5. 哪些类型的 PR 会被自动拒绝？
6. 哪些类型的 PR 会得到优先处理？

**风险提示：**
7. 有哪些迹象表明 PR 的质量较低？
8. 哪些因素会让您愿意优先审查某个 PR？
9. 在哪些具体方面您需要帮助？

**项目现状：**
10. 项目目前处于增长阶段、维护阶段还是过渡阶段？
11. 有哪些即将到来的里程碑会影响优先级判断？
12. 您如何处理可能破坏现有功能的变更？

完成面试后，脚本会在输出目录中生成两个文件：
- `vision.md`：项目使命、目标、优先级以及判断依据
- `rubric.md`：根据 `references/rubric-template.md` 自定义的评分标准

### 第二步：扫描（每次分类时执行）

使用 `scripts/scan.py` 并传入仓库 URL 和项目愿景文档的路径。该脚本会：
- 通过 `gh pr list` 获取所有开放的 PR（包括标题、内容、标签、统计信息、作者和提交日期）
- 根据预设规则进行评分（基础分为 50 分，可附加正负修正分）
- 通过标题相似度检测潜在的重复 PR
- 输出包含评分、评分理由和统计信息的 JSON 文件

评分过程采用启发式方法（关键词匹配、代码差异大小、测试提及情况等）。对于评分模糊的 PR，可以进一步使用大型语言模型（LLM）进行分析（评分范围为 40-60 分）。

可选参数：
- `--count N`：获取的 PR 数量（默认：100 个）
- `--output file.json`：将结果保存到文件而非标准输出

### 第三步：报告（扫描完成后执行）

使用 `scripts/report.py` 并传入扫描得到的 JSON 数据。该脚本会生成四个 Markdown 文件：
- `prioritize.md`：评分高于 80 分的 PR（优先审查）
- `review.md`：评分在 50-79 分之间的 PR（进入标准审核流程）
- `close.md`：评分低于 50 分的 PR（建议关闭或请求修改）
- `summary.md`：包含 PR 分布情况、得分最高的 3 个 PR、常见问题以及活跃的贡献者

## 评分标准概述

基础分为 50 分。主要评分因素如下：
| 评分依据 | 分值 |
|--------|--------|
| 安全性修复 | +20 |
| 带有测试的漏洞修复 | +10 |
| 核心功能改进 | +10 |
| 性能优化 | +8 |
| 代码差异较小且目标明确 | +5 |
| 包含测试代码 | +5 |
| 无关内容或推广行为 | -30 |
| 依赖项过多 | -25 |
| 代码差异过大且无测试 | -15 |
- 未提供描述 | -5 |

完整评分标准请参考 `references/rubric-template.md`。

**示例项目愿景文档：`references/example-vision.md`

## 通过 Cron 定期执行分类任务**

设置一个 Cron 作业，每周自动执行一次分类任务：

```
description: Weekly PR triage for owner/repo
schedule: "0 9 * * MON"
model: anthropic/claude-sonnet-4-20250514
channel: telegram
```

Cron 命令示例：`"Run pr-triage scan on https://github.com/owner/repo using ./triage-config/vision.md, generate reports, and send the summary."`

## 所需条件：
- 安装并登录 `gh` CLI（`gh auth login`）
- Python 3.10 及以上版本
- 无需额外安装其他 Python 包（仅使用标准库）