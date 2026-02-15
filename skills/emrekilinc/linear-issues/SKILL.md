---
name: linear
description: 与 Linear 进行交互以进行问题跟踪。适用于创建、更新、查看问题列表或搜索问题。支持查看已分配的问题、更改问题状态、添加评论以及管理任务。
---

# Linear

通过 `scripts/linear.sh` 命令来管理 Linear 相关的问题。

## 设置

将 API 密钥保存在 `~/.clawdbot/credentials/linear.json` 文件中：
```json
{"apiKey": "lin_api_..."}
```

## 命令

```bash
# List my assigned issues
scripts/linear.sh issues --mine

# List team issues
scripts/linear.sh issues --team TEAM_ID

# Get issue details
scripts/linear.sh get CLP-123

# Search issues
scripts/linear.sh search "auth bug"

# Create issue
scripts/linear.sh create --team TEAM_ID --title "Bug: login fails" --description "Details"

# Update issue (status, title, assignee, priority)
scripts/linear.sh update CLP-123 --state STATE_ID

# Add comment
scripts/linear.sh comment CLP-123 "Fixed in PR #42"

# List teams (to get TEAM_ID)
scripts/linear.sh teams

# List states (to get STATE_ID)
scripts/linear.sh states

# List users (to get assignee ID)
scripts/linear.sh users
```

使用 `--json` 标志可获取原始的 API 输出：`scripts/linear.sh --json issues --mine`

## 工作流程示例

**创建并分配一个问题：**
```bash
# Find team ID
scripts/linear.sh teams
# Create with priority 2 (high)
scripts/linear.sh create --team abc123 --title "Critical: API down" --priority 2
```

**将问题状态更改为“进行中”：**
```bash
# Find state ID
scripts/linear.sh states
# Update
scripts/linear.sh update CLP-45 --state xyz789
```

有关 GraphQL 的详细信息，请参阅 [references/api-examples.md](references/api-examples.md)。