---
name: confluence-v2
description: **Full Confluence Cloud REST API v2 功能**  
支持对 Confluence Cloud 的各种资源（页面、空间、文件夹、数据库、白板、评论、标签、任务、属性等）进行操作，支持基本认证（Basic Auth）和 OAuth 认证机制，具备分页功能，并支持从 `confluence-cli` 迁移数据。  

**主要功能包括：**  
- **页面管理**：创建、编辑、删除页面。  
- **空间管理**：创建、删除、重命名空间。  
- **文件夹管理**：创建、删除、移动文件夹。  
- **数据库管理**：查询、添加、删除数据库。  
- **白板管理**：创建、编辑、删除白板。  
- **评论管理**：查看、回复评论。  
- **标签管理**：创建、删除标签。  
- **任务管理**：创建、更新、删除任务。  
- **属性管理**：查看和修改任务属性。  
- **基本认证与 OAuth 认证**：支持基本用户名/密码认证以及 OAuth 2.0 认证。  
- **分页功能**：支持分页查询数据。  
- **数据迁移**：提供从 `confluence-cli` 迁移数据到 Confluence Cloud 的功能。  

**技术特性：**  
- **REST API**：使用标准的 RESTful API 接口进行数据交互。  
- **多数据源支持**：支持查询和操作多个数据库中的数据。  
- **安全性**：采用安全的 HTTPS 协议进行数据传输。  
- **可扩展性**：设计为模块化架构，便于未来功能的扩展。  

**适用场景：**  
- **企业级项目管理**：用于团队协作和知识共享。  
- **软件开发**：用于文档管理和代码托管。  
- **内容管理系统（CMS）集成**：将 Confluence Cloud 作为内容管理系统的一部分。  

**注意事项：**  
- 请确保您的 Confluence Cloud 版本支持 REST API v2。  
- 如需使用 OAuth 认证，请配置相应的 OAuth 2.0 服务器。  
- 详细的使用说明和示例代码请参考官方文档。
---

# Confluence Cloud REST API v2

使用此技能可以直接调用 **Confluence Cloud REST API v2** 的各个端点。该API 支持 **所有 v2 版本的功能**（页面、空间、文件夹、白板、数据库、嵌入内容、评论、标签、属性、任务等）。

## 快速入门

1) 配置凭据（选择以下其中一种方式）：
- **基本认证**：电子邮件 + API 令牌
- **OAuth**：访问令牌

2) 使用 `scripts/` 目录中的脚本来调用相应的端点。

## 配置

建议设置以下环境变量，或将其存储在本地配置文件中：

```
CONFLUENCE_BASE_URL=https://pangin.atlassian.net/wiki
CONFLUENCE_AUTH_METHOD=basic   # basic | oauth
CONFLUENCE_EMAIL=chrono3412@gmail.com
CONFLUENCE_API_TOKEN=YOUR_TOKEN
# or for OAuth
# CONFLUENCE_OAUTH_TOKEN=YOUR_OAUTH_ACCESS_TOKEN

# Optional admin key header (Premium/Enterprise only)
# CONFLUENCE_ADMIN_KEY=true
```

**基础 URL** 始终为 `https://<site>.atlassian.net/wiki`。

## 核心辅助工具

- `scripts/client.js` — HTTP 客户端封装层，用于处理认证请求和分页功能
- `scripts/*` — 包含各个端点的脚本（页面、空间、文件夹等）

## 示例

```bash
# list everything
node scripts/spaces.js list --all
node scripts/pages.js list --all
node scripts/labels.js list --all

# get single items
node scripts/pages.js get 89522178
node scripts/folders.js direct-children 87457793

# ad-hoc call
node scripts/call.js GET /folders/87457793/direct-children
```

## 从 confluence-cli 迁移

如果存在 `~/.confluence-cli/config.json` 文件，请进行以下映射：
- `domain` → `CONFLUENCE_BASE_URL`（`https://{domain}/wiki`)
- `email` → `CONFLUENCE_EMAIL`
- `token` → `CONFLUENCE_API_TOKEN`

## 参考资料

- OpenAPI 规范：`refs/openapi-v2.v3.json`
- 端点列表：`refs/endpoints.md`
- 授权范围：`refs/scopes.md`
- 测试用例：`refs/tests.md`
- 使用指南：`refs/usage.md`