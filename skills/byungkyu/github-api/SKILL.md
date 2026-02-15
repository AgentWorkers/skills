---
name: github
description: |
  GitHub API integration with managed OAuth. Access repositories, issues, pull requests, commits, branches, and users.
  Use this skill when users want to interact with GitHub repositories, manage issues and PRs, search code, or automate workflows.
  For other third party apps, use the api-gateway skill (https://clawhub.ai/byungkyu/api-gateway).
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    requires:
      env:
        - MATON_API_KEY
---

# GitHub

您可以使用托管的 OAuth 认证来访问 GitHub REST API，从而管理仓库、问题、拉取请求、提交、分支、用户等。

## 快速入门

```bash
# Get authenticated user
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/github/user')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本 URL

```
https://gateway.maton.ai/github/{native-api-path}
```

请将 `{native-api-path}` 替换为实际的 GitHub API 端点路径。该网关会将请求代理到 `api.github.com` 并自动插入您的 OAuth 令牌。

## 认证

所有请求都需要在 `Authorization` 头中包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

**环境变量：** 将您的 API 密钥设置为 `MATON_API_KEY`：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

### 获取 API 密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 转到 [maton.ai/settings](https://maton.ai/settings)。
3. 复制您的 API 密钥。

## 连接管理

您可以在 `https://ctrl.maton.ai` 上管理您的 GitHub OAuth 连接。

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=github&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'github'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "83e7c665-60f6-4a64-816c-5e287ea8982f",
    "status": "ACTIVE",
    "creation_time": "2026-02-06T03:00:43.860014Z",
    "last_updated_time": "2026-02-06T03:01:06.027323Z",
    "url": "https://connect.maton.ai/?session_token=...",
    "app": "github",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 `url` 以完成 OAuth 认证。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您有多个 GitHub 连接，请使用 `Maton-Connection` 头来指定要使用的连接：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/github/user')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Maton-Connection', '83e7c665-60f6-4a64-816c-5e287ea8982f')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此参数，网关将使用默认的（最旧的）活动连接。

## API 参考

### 用户

#### 获取已认证的用户

```bash
GET /github/user
```

#### 按用户名获取用户

```bash
GET /github/users/{username}
```

#### 列出用户

```bash
GET /github/users?since={user_id}&per_page=30
```

### 仓库

#### 列出用户的仓库

```bash
GET /github/user/repos?per_page=30&sort=updated
```

查询参数：`type`（全部、所有者、公共、私有、成员）、`sort`（创建时间、更新时间、推送时间、全名）、`direction`（升序、降序）、`per_page`、`page`

#### 列出组织的仓库

```bash
GET /github/orgs/{org}/repos?per_page=30
```

#### 获取仓库信息

```bash
GET /github/repos/{owner}/{repo}
```

#### 创建仓库（用户）

```bash
POST /github/user/repos
Content-Type: application/json

{
  "name": "my-new-repo",
  "description": "A new repository",
  "private": true,
  "auto_init": true
}
```

#### 创建仓库（组织）

```bash
POST /github/orgs/{org}/repos
Content-Type: application/json

{
  "name": "my-new-repo",
  "description": "A new repository",
  "private": true
}
```

#### 更新仓库

```bash
PATCH /github/repos/{owner}/{repo}
Content-Type: application/json

{
  "description": "Updated description",
  "has_issues": true,
  "has_wiki": false
}
```

#### 删除仓库

```bash
DELETE /github/repos/{owner}/{repo}
```

### 仓库内容

#### 列出仓库内容

```bash
GET /github/repos/{owner}/{repo}/contents/{path}
```

#### 获取文件内容

```bash
GET /github/repos/{owner}/{repo}/contents/{path}?ref={branch}
```

#### 创建或更新文件

```bash
PUT /github/repos/{owner}/{repo}/contents/{path}
Content-Type: application/json

{
  "message": "Create new file",
  "content": "SGVsbG8gV29ybGQh",
  "branch": "main"
}
```

注意：`content` 必须使用 Base64 编码。

#### 删除文件

```bash
DELETE /github/repos/{owner}/{repo}/contents/{path}
Content-Type: application/json

{
  "message": "Delete file",
  "sha": "{file_sha}",
  "branch": "main"
}
```

### 分支

#### 列出分支

```bash
GET /github/repos/{owner}/{repo}/branches?per_page=30
```

#### 获取分支信息

```bash
GET /github/repos/{owner}/{repo}/branches/{branch}
```

#### 重命名分支

```bash
POST /github/repos/{owner}/{repo}/branches/{branch}/rename
Content-Type: application/json

{
  "new_name": "new-branch-name"
}
```

#### 合并分支

```bash
POST /github/repos/{owner}/{repo}/merges
Content-Type: application/json

{
  "base": "main",
  "head": "feature-branch",
  "commit_message": "Merge feature branch"
}
```

### 提交

#### 列出提交记录

```bash
GET /github/repos/{owner}/{repo}/commits?per_page=30
```

查询参数：`sha`（分支名称或提交 SHA）、`path`（文件路径）、`author`、`committer`、`since`、`until`、`per_page`、`page`

#### 获取提交信息

```bash
GET /github/repos/{owner}/{repo}/commits/{ref}
```

#### 比较两个提交记录

```bash
GET /github/repos/{owner}/{repo}/compare/{base}...{head}
```

### 问题

#### 列出仓库中的问题

```bash
GET /github/repos/{owner}/{repo}/issues?state=open&per_page=30
```

查询参数：`state`（开放、关闭、全部）、`labels`、`assignee`、`creator`、`mentioned`、`sort`、`direction`、`since`、`per_page`、`page`

#### 获取问题信息

```bash
GET /github/repos/{owner}/{repo}/issues/{issue_number}
```

#### 创建问题

```bash
POST /github/repos/{owner}/{repo}/issues
Content-Type: application/json

{
  "title": "Found a bug",
  "body": "Bug description here",
  "labels": ["bug"],
  "assignees": ["username"]
}
```

#### 更新问题

```bash
PATCH /github/repos/{owner}/{repo}/issues/{issue_number}
Content-Type: application/json

{
  "state": "closed",
  "state_reason": "completed"
}
```

#### 锁定问题

```bash
PUT /github/repos/{owner}/{repo}/issues/{issue_number}/lock
Content-Type: application/json

{
  "lock_reason": "resolved"
}
```

#### 解锁问题

```bash
DELETE /github/repos/{owner}/{repo}/issues/{issue_number}/lock
```

### 问题评论

#### 列出问题评论

```bash
GET /github/repos/{owner}/{repo}/issues/{issue_number}/comments?per_page=30
```

#### 创建问题评论

```bash
POST /github/repos/{owner}/{repo}/issues/{issue_number}/comments
Content-Type: application/json

{
  "body": "This is a comment"
}
```

#### 更新问题评论

```bash
PATCH /github/repos/{owner}/{repo}/issues/comments/{comment_id}
Content-Type: application/json

{
  "body": "Updated comment"
}
```

#### 删除问题评论

```bash
DELETE /github/repos/{owner}/{repo}/issues/comments/{comment_id}
```

### 标签

#### 列出标签

```bash
GET /github/repos/{owner}/{repo}/labels?per_page=30
```

#### 创建标签

```bash
POST /github/repos/{owner}/{repo}/labels
Content-Type: application/json

{
  "name": "priority:high",
  "color": "ff0000",
  "description": "High priority issues"
}
```

### 里程碑

#### 列出里程碑

```bash
GET /github/repos/{owner}/{repo}/milestones?state=open&per_page=30
```

#### 创建里程碑

```bash
POST /github/repos/{owner}/{repo}/milestones
Content-Type: application/json

{
  "title": "v1.0",
  "state": "open",
  "description": "First release",
  "due_on": "2026-03-01T00:00:00Z"
}
```

### 拉取请求

#### 列出拉取请求

```bash
GET /github/repos/{owner}/{repo}/pulls?state=open&per_page=30
```

查询参数：`state`（开放、关闭、全部）、`head`、`base`、`sort`、`direction`、`per_page`、`page`

#### 获取拉取请求信息

```bash
GET /github/repos/{owner}/{repo}/pulls/{pull_number}
```

#### 创建拉取请求

```bash
POST /github/repos/{owner}/{repo}/pulls
Content-Type: application/json

{
  "title": "New feature",
  "body": "Description of changes",
  "head": "feature-branch",
  "base": "main",
  "draft": false
}
```

#### 更新拉取请求

```bash
PATCH /github/repos/{owner}/{repo}/pulls/{pull_number}
Content-Type: application/json

{
  "title": "Updated title",
  "state": "closed"
}
```

#### 列出拉取请求的提交记录

```bash
GET /github/repos/{owner}/{repo}/pulls/{pull_number}/commits?per_page=30
```

#### 列出拉取请求的文件

```bash
GET /github/repos/{owner}/{repo}/pulls/{pull_number}/files?per_page=30
```

#### 检查是否已合并

```bash
GET /github/repos/{owner}/{repo}/pulls/{pull_number}/merge
```

#### 合并拉取请求

```bash
PUT /github/repos/{owner}/{repo}/pulls/{pull_number}/merge
Content-Type: application/json

{
  "commit_title": "Merge pull request",
  "merge_method": "squash"
}
```

合并方法：`merge`、`squash`、`rebase`

### 拉取请求的审阅

#### 列出审阅记录

```bash
GET /github/repos/{owner}/{repo}/pulls/{pull_number}/reviews?per_page=30
```

#### 创建审阅

```bash
POST /github/repos/{owner}/{repo}/pulls/{pull_number}/reviews
Content-Type: application/json

{
  "body": "Looks good!",
  "event": "APPROVE"
}
```

事件：`APPROVE`、`REQUEST_CHANGES`、`COMMENT`

### 搜索

#### 搜索仓库

```bash
GET /github/search/repositories?q={query}&per_page=30
```

示例查询：
- `tetris+language:python` - 包含 “tetris” 且使用 Python 语言的仓库
- `react+stars:>10000` - 包含 “react” 且星标数量超过 10,000 的仓库

#### 搜索问题

```bash
GET /github/search/issues?q={query}&per_page=30
```

示例查询：
- `bug+is:open+is:issue` - 包含 “bug” 且状态为开放的问题的仓库
- `author:username+is:pr` - 由特定作者创建的拉取请求

#### 搜索代码

```bash
GET /github/search/code?q={query}&per_page=30
```

示例查询：
- `addClass+repo:facebook/react` - 在特定仓库中搜索 “addClass” 这个函数
- `function+extension:js` - 搜索 JavaScript 函数

注意：对于范围较广的搜索，可能会超时。

#### 搜索用户

```bash
GET /github/search/users?q={query}&per_page=30
```

### 组织

#### 列出用户所属的组织

```bash
GET /github/user/orgs?per_page=30
```

注意：需要 `read:org` 权限。

#### 获取组织信息

```bash
GET /github/orgs/{org}
```

#### 列出组织成员

```bash
GET /github/orgs/{org}/members?per_page=30
```

### 速率限制

#### 获取速率限制信息

```bash
GET /github/rate_limit
```

**响应：**
```json
{
  "rate": {
    "limit": 5000,
    "remaining": 4979,
    "reset": 1707200000
  },
  "resources": {
    "core": { "limit": 5000, "remaining": 4979 },
    "search": { "limit": 30, "remaining": 28 }
  }
}
```

## 分页

GitHub 使用基于页面和链接的分页方式：

```bash
GET /github/repos/{owner}/{repo}/issues?per_page=30&page=2
```

响应头包含分页链接：
- `Link: <url>; rel="next", <url>; rel="last"`

常见的分页参数：
- `per_page`：每页显示的结果数量（最大 100 个，默认为 30 个）
- `page`：页码（默认为 1）

某些端点使用基于游标的分页方式，需要 `since` 参数（例如，列出用户时）。

## 代码示例

### JavaScript

```javascript
const response = await fetch(
  'https://gateway.maton.ai/github/repos/owner/repo/issues?state=open&per_page=10',
  {
    headers: {
      'Authorization': `Bearer ${process.env.MATON_API_KEY}`
    }
  }
);
const issues = await response.json();
```

### Python

```python
import os
import requests

response = requests.get(
    'https://gateway.maton.ai/github/repos/owner/repo/issues',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    params={'state': 'open', 'per_page': 10}
)
issues = response.json()
```

## 注意事项

- 仓库名称不区分大小写，但 API 会保留大小写。
- 问题编号和拉取请求编号在每个仓库中具有相同的顺序。
- 创建/更新文件时，内容必须使用 Base64 编码。
- 认证用户的请求速率限制为每小时 5000 次；搜索操作每分钟 30 次。
- 对于范围非常广泛的搜索，可能会超时。
- 某些端点需要特定的 OAuth 权限范围（例如，操作组织需要 `read:org`）。如果您收到权限范围错误，请通过 support@maton.ai 联系 Maton 支持团队，提供所需的操作/API 和您的使用场景。
- 重要提示：当 URL 中包含括号时，使用 `curl -g` 可以防止全局解析。
- 重要提示：当将 curl 输出传递给 `jq` 或其他命令时，在某些 shell 环境中 `$MATON_API_KEY` 环境变量可能无法正确展开。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 未建立 GitHub 连接 |
| 401 | Maton API 密钥无效或缺失 |
| 403 | 禁止访问 - 权限不足或权限范围不正确 |
| 404 | 资源未找到 |
| 408 | 请求超时（常见于复杂的搜索操作） |
| 422 | 验证失败 |
| 429 | 达到速率限制 |
| 4xx/5xx | 来自 GitHub API 的传递错误 |

### 故障排除：API 密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证 API 密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用名称无效

1. 确保您的 URL 路径以 `github` 开头。例如：
- 正确：`https://gateway.maton.ai/github/user`
- 错误：`https://gateway.maton.ai/api.github.com/user`

## 资源

- [GitHub REST API 文档](https://docs.github.com/en/rest)
- [仓库 API](https://docs.github.com/en/rest/repos/repos)
- [问题 API](https://docs.github.com/en/rest/issues/issues)
- [拉取请求 API](https://docs.github.com/en/rest/pulls/pulls)
- [搜索 API](https://docs.github.com/en/rest/search/search)
- [速率限制](https://docs.github.com/en/rest/overview/resources-in-the-rest-api#rate-limiting)
- [Maton 社区](https://discord.com/invite/dBfFAcefs2)
- [Maton 支持](mailto:support@maton.ai)