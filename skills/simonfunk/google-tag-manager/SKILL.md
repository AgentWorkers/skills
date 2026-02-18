---
name: google-tag-manager
description: 通过 GTM API v2 管理 Google Tag Manager 的容器（containers）、标签（tags）、触发器（triggers）、变量（variables）以及版本（versions）。当用户需要列出、创建、更新、删除或检查 GTM 标签、触发器、变量、内置变量（built-in variables）、工作空间（workspaces）或版本时，可以使用该 API。此外，该 API 还可用于发布容器版本（publish container versions）、审核 GTM 设置（audit GTM setups）、创建转化标签（create conversion tags）、设置跨域跟踪（set up cross-domain tracking）或管理 dataLayer 事件（manage dataLayer events）。相关术语包括：GTM、Tag Manager、container tag（容器标签）、conversion tag（转化标签）、trigger（触发器）、GTM variable（GTM 变量）、publish GTM（发布 GTM 设置）、GTM workspace（GTM 工作空间）、dataLayer（数据层）、Google Ads tag（Google 广告标签）、GA4 tag（Google Analytics 4 标签）、cross-domain tracking（跨域跟踪）。
metadata:
  env:
    - GTM_ACCOUNT_ID: GTM account ID (numeric). Find at tagmanager.google.com.
    - GTM_CONTAINER_ID: GTM container ID (numeric).
    - GOOGLE_APPLICATION_CREDENTIALS: Path to service account JSON key file with Tag Manager API access.
---
# Google Tag Manager 技能

通过 GTM API v2 来管理容器（containers）、工作区（workspaces）、标签（tags）、触发器（triggers）、变量（variables）和版本（versions）。

## 认证

GTM API 使用 Google Cloud 服务账户进行 OAuth2 认证。

### 设置
1. 在 Google Cloud 控制台中启用 **Tag Manager API**。
2. 创建一个服务账户并获取其密钥（JSON 格式）。
3. 授予该服务账户在 GTM 中的访问权限（管理员 → 用户管理 → 添加服务账户邮箱）。
4. 设置环境变量：
   - `GOOGLE_APPLICATION_CREDENTIALS=/path/to/service-account.json`
   - `GTM_ACCOUNT_ID=123456`
   - `GTM_CONTAINER_ID=789012`

## 脚本

所有操作都使用 `scripts/gtm.sh` 脚本。不带参数运行该脚本可查看其使用方法：

```bash
scripts/gtm.sh <command> [args...]
```

### 命令

| 命令 | 描述 |
|---------|-------------|
| `accounts` | 列出所有 GTM 账户 |
| `containers [accountId]` | 列出指定账户中的容器 |
| `workspaces` | 列出容器中的工作区 |
| `tags [workspaceId]` | 列出工作区中的标签（默认：最新标签） |
| `tag <tagId> [workspaceId]` | 获取指定的标签 |
| `create-tag <jsonFile> [workspaceId]` | 从 JSON 文件创建标签 |
| `update-tag <tagId> <jsonFile> [workspaceId]` | 更新标签 |
| `delete-tag <tagId> [workspaceId]` | 删除标签 |
| `triggers [workspaceId]` | 列出触发器 |
| `trigger <triggerId> [workspaceId]` | 获取指定的触发器 |
| `create-trigger <jsonFile> [workspaceId]` | 从 JSON 文件创建触发器 |
| `update-trigger <triggerId> <jsonFile> [workspaceId]` | 更新触发器 |
| `delete-trigger <triggerId> [workspaceId]` | 删除触发器 |
| `variables [workspaceId]` | 列出变量 |
| `variable <variableId> [workspaceId]` | 获取指定的变量 |
| `create-variable <jsonFile> [workspaceId]` | 从 JSON 文件创建变量 |
| `update-variable <variableId> <jsonFile> [workspaceId]` | 更新变量 |
| `delete-variable <variableId> [workspaceId]` | 删除变量 |
| `built-in-vars [workspaceId]` | 列出已启用的内置变量 |
| `enable-built-in <type,...> [workspaceId]` | 启用指定的内置变量 |
| `versions` | 列出容器版本信息 |
| `version <versionId>` | 获取指定的版本 |
| `version-live` | 获取已发布的版本 |
| `create-version [workspaceId] [name] [notes]` | 从工作区创建版本 |
| `publish <versionId>` | 发布容器版本 |

### 工作区解析

大多数命令支持可选的 `workspaceId` 参数。如果省略该参数，脚本会自动使用 **默认工作区**（API 返回的第一个工作区，通常是 “Default Workspace”）。

## 常用操作流程

### 创建 Google Ads 转换标签

请参阅 `references/recipes.md`，其中包含以下内容的 JSON 模板：
- Google Ads 转换跟踪标签
- GA4 事件标签
- 自定义事件触发器（dataLayer）
- 跨域跟踪链接器

### 工作流程：添加标签 → 创建版本 → 发布

```bash
# 1. Create trigger
scripts/gtm.sh create-trigger trigger.json

# 2. Create tag referencing the trigger
scripts/gtm.sh create-tag tag.json

# 3. Create version from workspace
scripts/gtm.sh create-version "" "v1.2 - Added conversion tag"

# 4. Publish
scripts/gtm.sh publish <versionId>
```

## API 参考

有关完整的资源架构和触发器类型，请参阅 `references/api-reference.md`。