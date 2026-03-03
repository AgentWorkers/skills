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

**创建合并请求草稿：**
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

该脚本会自动完成以下操作：检出代码 → 运行测试 → 显示测试结果 → 如果测试通过则批准合并请求。

### 合并策略

**当管道（Pipeline）通过时自动合并：**
```bash
glab mr merge 123 --when-pipeline-succeeds --remove-source-branch
```

**合并前合并提交（Squash Commits）：**
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
- 检出合并请求的代码：`glab mr checkout <MR-id>`
- 在编辑器中手动解决冲突
- 提交解决后的代码：`git add . && git commit`
- 推送更改：`git push`

**无法批准合并请求：**
- 检查自己是否是该合并请求的发起者（大多数配置下不允许自我批准）
- 验证权限：`glab mr approvers <MR-id>`
- 确保合并请求不是草稿状态

**需要运行管道但未运行：**
- 检查分支中是否存在 `.gitlab-ci.yml` 文件
- 验证项目是否启用了持续集成/持续部署（CI/CD）功能
- 手动触发管道：`glab ci run`

**“合并请求已存在”错误：**
- 列出该分支下的所有合并请求：`glab mr list --source-branch <branch>`
- 如果旧合并请求已过时，关闭它：`glab mr close <MR-id>`
- 或者更新现有合并请求的标题：`glab mr update <MR-id> --title "新标题"`

## 相关技能

**处理问题（Issues）：**
- 查看 `glab-issue` 以创建/管理问题
- 使用 `glab mr for <issue-id>` 为问题创建关联的合并请求
- 脚本 `scripts/create-mr-from-issue.sh` 可自动完成分支和合并请求的创建

**持续集成/持续部署（CI/CD）集成：**
- 查看 `glab-ci` 以获取管道状态
- 使用 `glab mr merge --when-pipeline-succeeds` 实现自动合并

**自动化：**
- 脚本 `scripts/mr-review-workflow.sh` 可自动化审查和测试流程

## 在合并请求差异（Merge Request Diffs）中添加内联评论

### `glab api --field` 的问题

当 GitLab 无法解析位置数据时，`glab api --field position=<new_line>=N` 会默认生成一个**普通**（非内联）评论。这种情况可能发生在：
- 完全新创建的文件（差异中的 `new_file` 为 `true`）
- 包含复杂/编码路径的文件
- 任何在格式化过程中丢失的嵌套位置字段

这不会触发错误——GitLab 会直接生成普通评论，除非你检查返回的评论中的 `position` 字段，否则你可能不会意识到这个错误。

### 解决方法：始终使用 JSON 格式

通过 REST API 发送内联评论时，务必设置 `Content-Type: application/json`：

```python
import json, urllib.request, urllib.parse, subprocess

# Get token from glab config
token = subprocess.run(
    ["glab", "config", "get", "token", "--host", "gitlab.com"],
    capture_output=True, text=True
).stdout.strip()

project = urllib.parse.quote("mygroup/myproject", safe="")
mr_iid = 42

# Always fetch fresh SHAs — never use cached values
r = urllib.request.urlopen(urllib.request.Request(
    f"https://gitlab.com/api/v4/projects/{project}/merge_requests/{mr_iid}/versions",
    headers={"PRIVATE-TOKEN": token}
))
v = json.loads(r.read())[0]

payload = {
    "body": "Your comment here",
    "position": {
        "base_sha":  v["base_commit_sha"],
        "start_sha": v["start_commit_sha"],
        "head_sha":  v["head_commit_sha"],
        "position_type": "text",
        "new_path": "src/utils/helpers.ts",
        "new_line": 16,
        "old_path": "src/utils/helpers.ts",  # same as new_path
        "old_line": None                       # None = added line
    }
}

req = urllib.request.Request(
    f"https://gitlab.com/api/v4/projects/{project}/merge_requests/{mr_iid}/discussions",
    data=json.dumps(payload).encode(),
    headers={"PRIVATE-TOKEN": token, "Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req) as resp:
    result = json.loads(resp.read())
    note = result["notes"][0]
    is_inline = note.get("position") is not None  # True = inline, False = fell back to general
    print("inline:", is_inline, "| disc_id:", result["id"])
```

### 确定正确的行号

差异中的行号必须指向**新增的行**（行号前缀为 `+`）；否则 GitLab 会拒绝该评论：

```python
import re

def get_new_line_number(diff_text, keyword):
    """Find the new_file line number of the first added line containing keyword."""
    new_line = 0
    for line in diff_text.split("\n"):
        hunk = re.match(r"@@ -\d+(?:,\d+)? \+(\d+)(?:,\d+)? @@", line)
        if hunk:
            new_line = int(hunk.group(1)) - 1
            continue
        if line.startswith("-") or line.startswith("\\"):
            continue
        new_line += 1
        if line.startswith("+") and keyword in line:
            return new_line
    return None

# Usage
diffs = json.loads(...)  # from /merge_requests/{iid}/diffs
for d in diffs:
    if d["new_path"] == "src/utils/helpers.ts":
        line = get_new_line_number(d["diff"], "safeParse")
        print("line:", line)
```

### 可重用的脚本

对于需要脚本化或自动化的合并请求审查流程，可以使用提供的辅助工具：

```bash
# Single comment
python3 scripts/post-inline-comment.py \
  --project "mygroup/myproject" \
  --mr 42 \
  --file "src/utils/helpers.ts" \
  --line 16 \
  --body "This returns the wrapper object — use .data instead."

# Batch from JSON file
python3 scripts/post-inline-comment.py \
  --project "mygroup/myproject" \
  --mr 42 \
  --batch comments.json
```

批量处理文件时，可以使用以下格式：
```json
[
  { "file": "src/utils/helpers.ts", "line": 16, "body": "Comment 1" },
  { "file": "src/routes/+page.svelte", "line": 58, "body": "Comment 2" }
]
```

该脚本会自动从 glab 配置中读取你的访问令牌，获取最新的 SHA 值，并报告每条评论是作为内联评论添加的还是被转换为普通评论。

---

## v1.87.0 的更新：新增的 `glab mr list` 参数

在 v1.87.0 版本中，`glab mr list` 命令新增了以下参数：

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

有关所有命令的详细文档和参数信息，请参阅 [references/commands.md](references/commands.md)。

**可用命令：**
- `approve` - 批准合并请求
- `checkout` - 在本地检出合并请求的代码
- `close` - 关闭合并请求
- `create` - 创建新的合并请求
- `delete` - 删除合并请求
- `diff` - 查看合并请求中的更改
- `for` - 为某个问题创建合并请求
- `list` - 列出所有合并请求
- `merge` - 合并/接受合并请求
- `note` - 为合并请求添加评论
- `rebase` - 重新基线源代码分支
- `reopen` - 重新打开合并请求
- `revoke` - 撤销批准
- `subscribe` / `unsubscribe` - 管理通知接收
- `todo` - 添加待办事项
- `update` - 更新合并请求的元数据
- `view` - 显示合并请求的详细信息