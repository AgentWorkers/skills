# Jira PAT 技能

使用个人访问令牌（Personal Access Tokens, PAT）来管理自托管或企业版 Jira 实例中的问题。此技能适用于因单点登录（SSO）/SAML 身份验证而无法使用基本认证（Basic Auth）的环境。

## 何时使用此技能

在以下情况下使用此技能：
- 自托管的 Jira 实例（例如 Red Hat 部署）
- 使用 SSO/SAML 身份验证的 Jira 实例
- `jira-cli` 或基本认证失败的环境

**注意：**对于使用电子邮件 + API 令牌进行身份验证的 Atlassian Cloud，请使用 `clawdbot-jira-skill` 技能。

## 先决条件

1. **个人访问令牌（PAT）**：在 Jira 中创建一个令牌：
   - 访问您的 Jira 个人资料 → 个人访问令牌
   - 创建具有适当权限的新令牌
   - 将其存储在环境变量 `JIRA_PAT` 中

2. **Jira 基本 URL**：您的 Jira 实例 URL，存储在 `JIRA_URL` 变量中

## 环境变量

```bash
export JIRA_PAT="your-personal-access-token"
export JIRA_URL="https://issues.example.com"
```

## 工具

此技能使用 `curl` 和 `jq` 来执行所有操作。

## 指令

### 获取问题详情

获取 Jira 问题的完整详情：

```bash
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_URL/rest/api/2/issue/PROJECT-123" | jq
```

仅获取特定字段：

```bash
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_URL/rest/api/2/issue/PROJECT-123?fields=summary,status,description" | jq
```

### 搜索问题（JQL）

```bash
# Find child issues of an epic
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_URL/rest/api/2/search?jql=parent=EPIC-123" | jq

# Complex queries (URL-encoded)
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_URL/rest/api/2/search?jql=project%3DPROJ%20AND%20status%3DOpen" | jq
```

常见的 JQL 模式：
- `parent=EPIC-123` - 某个史诗任务的子问题
- `project=PROJ AND status=Open` - 项目中的未解决问题
- `assignee=currentUser()` - 被分配给您的任务
- `labels=security` - 带有特定标签的问题
- `updated >= -7d` - 最近更新的问题

### 获取可用的问题状态转换

在更改问题状态之前，查询可用的状态转换：

```bash
curl -s -H "Authorization: Bearer $JIRA_PAT" \
  "$JIRA_URL/rest/api/2/issue/PROJECT-123/transitions" | jq '.transitions[] | {id, name}'
```

### 更改问题状态

通过添加评论来关闭问题：

```bash
curl -s -X POST \
  -H "Authorization: Bearer $JIRA_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "transition": {"id": "61"},
    "update": {
      "comment": [{"add": {"body": "Closed via API"}}]
    }
  }' \
  "$JIRA_URL/rest/api/2/issue/PROJECT-123/transitions"
```

### 添加评论

```bash
curl -s -X POST \
  -H "Authorization: Bearer $JIRA_PAT" \
  -H "Content-Type: application/json" \
  -d '{"body": "Comment added via API."}' \
  "$JIRA_URL/rest/api/2/issue/PROJECT-123/comment"
```

### 更新问题字段

```bash
curl -s -X PUT \
  -H "Authorization: Bearer $JIRA_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "summary": "Updated summary",
      "labels": ["api", "automated"]
    }
  }' \
  "$JIRA_URL/rest/api/2/issue/PROJECT-123"
```

### 创建问题

```bash
curl -s -X POST \
  -H "Authorization: Bearer $JIRA_PAT" \
  -H "Content-Type: application/json" \
  -d '{
    "fields": {
      "project": {"key": "PROJ"},
      "summary": "New issue via API",
      "description": "Issue description",
      "issuetype": {"name": "Task"},
      "parent": {"key": "EPIC-123"}
    }
  }' \
  "$JIRA_URL/rest/api/2/issue"
```

## 有用的 `jq` 过滤器

```bash
# Summary and status
jq '{key: .key, summary: .fields.summary, status: .fields.status.name}'

# List search results
jq '.issues[] | {key: .key, summary: .fields.summary, status: .fields.status.name}'

# Issue links
jq '.fields.issuelinks[] | {type: .type.name, key: (.inwardIssue // .outwardIssue).key}'
```

## 故障排除

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| 401 未经授权 | 令牌无效/过期 | 重新生成令牌，并检查 `Bearer` 格式 |
| 404 未找到 | 问题不存在或没有访问权限 | 验证问题键和权限 |
| 400 转换请求错误 | 转换 ID 无效 | 先查询可用的转换选项 |

## 与基本认证技能的比较

此技能使用 **Bearer 令牌认证**（`Authorization: Bearer <PAT>`），适用于使用 SSO/SAML 的自托管 Jira 实例。对于使用电子邮件 + API 令牌的 Atlassian Cloud，应使用实现基本认证的技能。