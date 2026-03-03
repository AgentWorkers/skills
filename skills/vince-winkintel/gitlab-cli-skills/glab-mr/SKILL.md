---
name: glab-mr
description: Create, view, manage, approve, and merge GitLab merge requests. Use when working with MRs: creating from branches/issues, reviewing, approving, adding comments, checking out locally, viewing diffs, rebasing, merging, or managing state. Triggers on merge request, MR, pull request, PR, review, approve, merge.
---

# glab mr

用于创建、查看和管理 GitLab 合并请求。

## 快速入门

```bash
# Create MR from current branch
glab mr create --fill

# List my MRs
glab mr list --assignee=@me

# Review an MR
glab mr checkout 123
glab mr diff
glab mr approve

# Merge an MR
glab mr merge 123 --when-pipeline-succeeds --remove-source-branch
```

## 常见工作流程

### 创建合并请求（Merge Requests, MRs）

**从当前分支创建：**
```bash
glab mr create --fill --label bugfix --assignee @reviewer
```

**从问题（Issue）创建：**
```bash
glab mr for 456  # Creates MR linked to issue #456
```

**创建草稿合并请求：**
```bash
glab mr create --draft --title "WIP: Feature X"
```

### 审查工作流程

1. **查看待审的合并请求：**
   ```bash
   glab mr list --reviewer=@me --state=opened
   ```

2. **检出代码并测试：**
   ```bash
   glab mr checkout 123
   npm test
   ```

3. **留下反馈：**
   ```bash
   glab mr note 123 -m "Looks good, one question about the cache logic"
   ```

4. **批准：**
   ```bash
   glab mr approve 123
   ```

**自动化审查工作流程：**

对于重复性的审查任务，可以使用自动化脚本：
```bash
scripts/mr-review-workflow.sh 123
scripts/mr-review-workflow.sh 123 "pnpm test"
```

该脚本会自动执行以下操作：检出代码 → 运行测试 → 显示测试结果 → 如果测试通过则批准合并请求。

### 合并策略

**当管道（Pipeline）通过时自动合并：**
```bash
glab mr merge 123 --when-pipeline-succeeds --remove-source-branch
```

**合并前压缩提交（Squash Commits）：**
```bash
glab mr merge 123 --squash
```

**合并前重新基线（Rebase before Merge）：**
```bash
glab mr rebase 123
glab mr merge 123
```

## 故障排除

**合并冲突：**
- 检出合并请求：`glab mr checkout <MR-id>`
- 在编辑器中手动解决冲突
- 提交解决后的代码：`git add . && git commit`
- 推送更改：`git push`

**无法批准合并请求：**
- 确认自己是否为该合并请求的发起者（大多数配置下不允许自我批准）
- 检查权限：`glab mr approvers <MR-id>`
- 确保合并请求不是草稿状态

**需要运行管道但未运行：**
- 检查分支中是否存在 `.gitlab-ci.yml` 文件
- 确认项目已启用 CI/CD 功能
- 手动触发管道：`glab ci run`

**出现“合并请求已存在”的错误：**
- 列出该分支下的所有合并请求：`glab mr list --source-branch <branch>`
- 如果旧合并请求已过时，可以关闭它：`glab mr close <MR-id>`
- 或者更新现有合并请求的标题：`glab mr update <MR-id> --title "新标题"`

## 相关技能

**处理问题（Issues）：**
- 查看 `glab-issue` 命令以创建/管理问题
- 使用 `glab mr for <issue-id>` 为某个问题创建合并请求
- 脚本 `scripts/create-mr-from-issue.sh` 可自动完成分支和合并请求的创建

**CI/CD 集成：**
- 查看 `glab-ci` 命令以获取管道状态
- 使用 `glab mr merge --when-pipeline-succeeds` 实现自动合并

**自动化：**
- 脚本 `scripts/mr-review-workflow.sh` 可实现自动化审查和测试流程

## v1.87.0 的更新：新增 `glab mr list` 的标志参数

在 v1.87.0 版本中，`glab mr list` 命令新增了以下标志参数：

```bash
# Filter by author
glab mr list --author <username>

# Filter by source or target branch
glab mr list --source-branch feature/my-branch
glab mr list --target-branch main

# Filter by draft status
glab mr list --draft
glab mr list --not-draft

# Filter by label or exclude label
glab mr list --label bugfix
glab mr list --not-label wip

# Order and sort
glab mr list --order updated_at --sort desc
glab mr list --order merged_at --sort asc

# Date range filtering
glab mr list --created-after 2026-01-01
glab mr list --created-before 2026-03-01

# Search in title/description
glab mr list --search "login fix"

# Full flag reference (all available flags)
glab mr list \
  --assignee @me \
  --author vince \
  --reviewer @me \
  --label bugfix \
  --not-label wip \
  --source-branch feature/x \
  --target-branch main \
  --milestone "v2.0" \
  --draft \
  --state opened \
  --order updated_at \
  --sort desc \
  --search "auth" \
  --created-after 2026-01-01
```

## 命令参考

有关命令的完整文档和所有标志参数，请参阅 [references/commands.md](references/commands.md)。

**可用命令：**
- `approve` - 批准合并请求
- `checkout` - 在本地检出合并请求
- `close` - 关闭合并请求
- `create` - 创建新的合并请求
- `delete` - 删除合并请求
- `diff` - 查看合并请求中的更改
- `for` - 为某个问题创建合并请求
- `list` - 列出所有合并请求
- `merge` - 合并/接受合并请求
- `note` - 为合并请求添加注释
- `rebase` - 重新基线源分支
- `reopen` - 重新打开合并请求
- `revoke` - 撤销批准
- `subscribe` / `unsubscribe` - 管理通知
- `todo` - 添加待办事项
- `update` - 更新合并请求的元数据
- `view` - 查看合并请求的详细信息