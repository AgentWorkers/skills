---
name: pr-commit-workflow
description: 此技能应在创建提交（commit）或拉取请求（pull request）时使用，以确保 PR（Pull Request）结构符合人工编写的标准，准确捕捉开发者的意图，并在自动化工作流程中提供必要的证据支持。
---

# PR（Pull Request）与提交工作流程

## 概述
实施高效率的提交工作流程，并要求所有 PR 都采用人工编写的格式。将全局流程规则作为权威依据，确保 PR 能够由人类和自动化工具进行审核。

## 工作流程决策树
- 如果任务仅涉及提交操作，请参考 `references/workflow-commit.md`。
- 如果任务涉及创建或更新 PR，请参考 `references/workflow-pr.md`。

## 全局规则
- 如果仓库中存在 `AGENTS.md` 或 `docs/agents/PROCESS.md`，请阅读其中的具体规则。
- 每个 PR 需要包含用户提供的、由人工编写的说明性文本；严禁自动生成或改写这些内容。
- 使用 `/tmp` 文件夹存放 PR 正文的草稿，使用 `gh pr edit --body-file` 命令进行更新。

## 提交工作流程（入口点）
- 按照 `references/workflow-commit.md` 中的步骤执行操作。
- 请遵循 `references/commit-format.md` 中规定的提交信息格式。

## PR 工作流程（入口点）
- 按照 `references/workflow-pr.md` 中的步骤执行操作。
- 请严格使用 `references/pr-human-template.md` 中提供的模板。
- 如果可用，请使用 `scripts/build_pr_body.sh` 脚本收集环境元数据。

## 参考资源
- `references/workflow-commit.md`：提交操作的检查清单及所需提供的证据。
- `references/workflow-pr.md`：PR 的创建/更新流程、评论审核规则及所需提供的证据。
- `references/pr-human-template.md`：人工编写的 PR 结构模板（必须原样使用）。
- `references/commit-format.md`：提交信息的格式及示例。
- `scripts/build_pr_body.sh`：用于收集 PR 提交历史相关环境元数据的脚本。