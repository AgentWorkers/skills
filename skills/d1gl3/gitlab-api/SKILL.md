---
name: gitlab-api
description: GitLab API集成用于仓库操作。当您需要与GitLab仓库进行交互（如读取、写入、创建或删除文件、列出项目、管理分支等）时，可以使用该集成。
---

# GitLab API

您可以通过 REST API 与 GitLab 仓库进行交互。该 API 支持 GitLab.com 以及自托管的 GitLab 实例。

## 设置

请存储您的 GitLab 个人访问令牌：

```bash
mkdir -p ~/.config/gitlab
echo "glpat-YOUR_TOKEN_HERE" > ~/.config/gitlab/api_token
```

**所需的令牌权限：** `api` 或 `read_api` + `write_repository`

**获取令牌：**
- GitLab.com：https://gitlab.com/-/user_settings/personal_access_tokens
- 自托管 GitLab：https://YOUR_GITLAB/~/-/user_settings/personal_access_tokens

## 配置

默认实例：`https://gitlab.com`

对于自托管的 GitLab，请创建一个配置文件：

```bash
echo "https://gitlab.example.com" > ~/.config/gitlab/instance_url
```

## 常用操作

### 列出项目

```bash
GITLAB_TOKEN=$(cat ~/.config/gitlab/api_token)
GITLAB_URL=$(cat ~/.config/gitlab/instance_url 2>/dev/null || echo "https://gitlab.com")

curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects?owned=true&per_page=20"
```

### 获取项目 ID

项目可以通过 ID 或 URL 编码的路径（`namespace%2Fproject`）来识别。

```bash
# By path
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/username%2Frepo"

# Extract ID from response: jq '.id'
```

### 读取文件

```bash
PROJECT_ID="12345"
FILE_PATH="src/main.py"
BRANCH="main"

curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/files/${FILE_PATH}?ref=$BRANCH" \
  | jq -r '.content' | base64 -d
```

### 创建/更新文件

```bash
PROJECT_ID="12345"
FILE_PATH="src/new_file.py"
BRANCH="main"
CONTENT=$(echo "print('hello')" | base64)

curl -X POST -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -H "Content-Type: application/json" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/files/${FILE_PATH}" \
  -d @- <<EOF
{
  "branch": "$BRANCH",
  "content": "$CONTENT",
  "commit_message": "Add new file",
  "encoding": "base64"
}
EOF
```

进行更新时，请使用 `-X PUT` 而不是 `-X POST`。

### 删除文件

```bash
curl -X DELETE -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -H "Content-Type: application/json" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/files/${FILE_PATH}" \
  -d '{"branch": "main", "commit_message": "Delete file"}'
```

### 列出目录中的文件

```bash
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/tree?path=src&ref=main"
```

### 获取仓库内容（存档）

```bash
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/archive.tar.gz" \
  -o repo.tar.gz
```

### 列出分支

```bash
curl -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/branches"
```

### 创建分支

```bash
curl -X POST -H "PRIVATE-TOKEN: $GITLAB_TOKEN" \
  -H "Content-Type: application/json" \
  "$GITLAB_URL/api/v4/projects/$PROJECT_ID/repository/branches" \
  -d '{"branch": "feature-xyz", "ref": "main"}'
```

## 辅助脚本

使用 `scripts/gitlab_api.sh` 来执行常用操作：

```bash
# List projects
./scripts/gitlab_api.sh list-projects

# Read file
./scripts/gitlab_api.sh read-file <project-id> <file-path> [branch]

# Write file
./scripts/gitlab_api.sh write-file <project-id> <file-path> <content> <commit-msg> [branch]

# Delete file
./scripts/gitlab_api.sh delete-file <project-id> <file-path> <commit-msg> [branch]

# List directory
./scripts/gitlab_api.sh list-dir <project-id> <dir-path> [branch]
```

## 速率限制

- GitLab.com：每分钟 300 次请求（已认证用户）
- 自托管 GitLab：由管理员配置

## API 参考

完整的 API 文档：https://docs.gitlab.com/ee/api/api_resources.html

主要 API 端点：
- 项目：`/api/v4/projects`
- 仓库文件：`/api/v4/projects/:id/repository/files`
- 仓库目录结构：`/api/v4/projects/:id/repository/tree`
- 分支：`/api/v4/projects/:id/repository/branches`