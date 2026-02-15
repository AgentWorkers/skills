---
name: azure-devops
description: 列出 Azure DevOps 项目、仓库和分支；创建拉取请求（pull requests）；管理工作项（work items）；检查构建状态（build status）。适用于处理 Azure DevOps 资源、查看拉取请求的状态、查询项目结构或自动化 DevOps 工作流程的场景。
metadata: {"openclaw": {"emoji": "☁️", "requires": {"bins": ["curl", "jq"], "env": ["AZURE_DEVOPS_PAT"]}, "primaryEnv": "AZURE_DEVOPS_PAT"}}
---

# Azure DevOps 技能

列出项目、仓库和分支；创建拉取请求；管理工作项；检查构建状态。

## 在运行前请检查配置是否有效，如果缺少值，请询问用户！

**所需参数：**
- `AZURE_DEVOPS_PAT`：个人访问令牌（Personal Access Token）
- `AZURE_DEVOPS_ORG`：组织名称（Organization name）

**如果 `~/.openclaw/openclaw.json` 文件中缺少这些值，代理应：**
1. **询问** 用户缺失的访问令牌和/或组织名称
2. 将这些信息保存到 `~/.openclaw/openclaw.json` 文件的 `skills.entries["azure-devops"]` 部分中

### 示例配置

```json5
{
  skills: {
    entries: {
      "azure-devops": {
        apiKey: "YOUR_PERSONAL_ACCESS_TOKEN",  // AZURE_DEVOPS_PAT
        env: {
          AZURE_DEVOPS_ORG: "YourOrganizationName"
        }
      }
    }
  }
}
```

## 命令

### 列出项目

```bash
curl -s -u ":${AZURE_DEVOPS_PAT}" \
  "https://dev.azure.com/${AZURE_DEVOPS_ORG}/_apis/projects?api-version=7.1" \
  | jq -r '.value[] | "\(.name) - \(.description // "No description")"'
```

### 列出项目中的仓库

```bash
PROJECT="YourProject"
curl -s -u ":${AZURE_DEVOPS_PAT}" \
  "https://dev.azure.com/${AZURE_DEVOPS_ORG}/${PROJECT}/_apis/git/repositories?api-version=7.1" \
  | jq -r '.value[] | "\(.name) - \(.webUrl)"'
```

### 列出仓库中的分支

```bash
PROJECT="YourProject"
REPO="YourRepo"
curl -s -u ":${AZURE_DEVOPS_PAT}" \
  "https://dev.azure.com/${AZURE_DEVOPS_ORG}/${PROJECT}/_apis/git/repositories/${REPO}/refs?filter=heads/&api-version=7.1" \
  | jq -r '.value[] | .name | sub("refs/heads/"; "")'
```

### 创建拉取请求

```bash
PROJECT="YourProject"
REPO_ID="repo-id-here"
SOURCE_BRANCH="feature/my-branch"
TARGET_BRANCH="main"
TITLE="PR Title"
DESCRIPTION="PR Description"

curl -s -u ":${AZURE_DEVOPS_PAT}" \
  -H "Content-Type: application/json" \
  -X POST \
  -d '{
    "sourceRefName": "refs/heads/'"${SOURCE_BRANCH}"'",
    "targetRefName": "refs/heads/'"${TARGET_BRANCH}"'",
    "title": "'"${TITLE}"'",
    "description": "'"${DESCRIPTION}"'"
  }' \
  "https://dev.azure.com/${AZURE_DEVOPS_ORG}/${PROJECT}/_apis/git/repositories/${REPO_ID}/pullrequests?api-version=7.1"
```

### 获取仓库 ID

```bash
PROJECT="YourProject"
REPO_NAME="YourRepo"
curl -s -u ":${AZURE_DEVOPS_PAT}" \
  "https://dev.azure.com/${AZURE_DEVOPS_ORG}/${PROJECT}/_apis/git/repositories/${REPO_NAME}?api-version=7.1" \
  | jq -r '.id'
```

### 列出拉取请求

```bash
PROJECT="YourProject"
REPO_ID="repo-id"
curl -s -u ":${AZURE_DEVOPS_PAT}" \
  "https://dev.azure.com/${AZURE_DEVOPS_ORG}/${PROJECT}/_apis/git/repositories/${REPO_ID}/pullrequests?api-version=7.1" \
  | jq -r '.value[] | "#\(.pullRequestId): \(.title) [\(.sourceRefName | sub("refs/heads/"; ""))] -> [\(.targetRefName | sub("refs/heads/"; ""))] - \(.createdBy.displayName)"'
```

## 注意事项：
- 基本 URL：`https://dev.azure.com/${AZURE_DEVOPS_ORG>`
- API 版本：`7.1`
- 认证方式：使用空用户名和访问令牌（PAT）进行基本认证（Basic Auth）
- 绝不要在响应中记录或泄露访问令牌（PAT）
- 文档参考：https://learn.microsoft.com/en-us/rest/api/azure/devops/