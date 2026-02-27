---
name: gh-modify-pr
description: 根据 GitHub PR 评论中的建议修改代码，并使用 `gh + git` 命令创建一个本地提交。当用户要求“关注 PR 评论”、“修复评论中的问题”、”更新该 PR”或提供 PR 的 URL 并请求进行编辑/提交时，可以使用此方法。
metadata:
  openclaw:
    requires:
      bins: ["gh", "git"]
---
# gh-modify-pr

使用此工作流程来处理由 PR 评论驱动的代码修改。

## 输入参数

- PR 的 URL（推荐使用），例如：`https://github.com/owner/repo/pull/123`
- 用户可选的修改范围（例如：仅修改一条评论，或修改所有未解决的评论）

## 工作流程

1. 从 URL 中解析出仓库所有者（owner）、仓库名称（repo）和 PR 编号（number）。
2. 查看 PR 的摘要：
   - `gh pr view <url> --json number,title,headRefName,baseRefName,files,reviews,reviewDecision`
3. 获取 PR 中的评论内容：
   - `gh api repos/<owner>/<repo>/pulls/<number>/comments`
4. 从评论内容中提取需要修改的代码部分。
5. 确保本地仓库已存在于工作区中：
   - 如果不存在：`git clone git@github.com:<owner>/<repo>.git`
6. 在本地仓库中切换到对应的 PR 分支：
   - `gh pr checkout <number>`
7. 打开相关文件并精确地实现评论中要求的修改。
8. 快速验证修改后的文件（仅在需要或用户要求时进行代码检查/测试）。
9. 提交更改：
   - `git add <files>`
   - `git commit -m "<修改说明>"
10. 向用户报告以下信息：
   - 修改了哪些内容
   - 提交的哈希值（commit hash）
   - 使用的分支名称（branch name）
11. 仅在用户请求或批准后才能推送更改：
   - `git push`

## 规则

- 尽量使用最简洁的差异（diff）来直接反映审阅者的意图。
- 不要随意修改与评论无关的代码。
- 如果某条评论表述不明确，应向作者提出一个具体的澄清问题。
- 如果本地仓库不存在，请先克隆仓库再继续操作，而不是直接失败。
- 当用户要求追踪修改过程时，将所有尝试但未成功的操作记录在日志中。

## 实用命令

```bash
# PR meta
gh pr view <url> --json number,title,headRefName,baseRefName,files,reviews,reviewDecision

# Inline review comments
gh api repos/<owner>/<repo>/pulls/<number>/comments

# Checkout PR branch (inside repo)
gh pr checkout <number>

# Status and commit
git status --short
git add <files>
git commit -m "chore: address PR review comments"
```

## 输出模板

- PR：`<url>`
- 已处理的评论数量：`<n>`
- 被修改的文件：
  - `<文件路径>`：`<修改内容>`
- 提交信息：`<commit hash>`
- 使用的分支：`<branch>`
- 是否已推送：`是/否`