---
name: strapi
description: 通过官方的 @strapi/client SDK 管理 Strapi 内容管理系统（CMS）中的内容。可以对集合类型（collections）、单一类型（single types）以及媒体文件（media files）执行创建（Create）、读取（Read）、更新（Update）和删除（Delete, CRUD）操作。支持将文件上传到媒体库（media library）。能够查询内容类型的架构（schemas）、它们之间的关系（relations）以及相关组件（components）。同时具备管理国际化（i18n）设置和本地化内容（localized content）的功能，包括翻译（translations）。提供草稿编辑到发布的完整工作流程（draft/publish workflow）。允许用户自定义编辑表单的布局（field order, sizes, labels）。系统还支持用户管理（end users）、角色分配（roles）以及身份验证（authentication）功能。当用户询问关于 Strapi 的相关信息，或者需要了解无头 CMS（headless CMS）、内容管理、文章（articles）、博客帖子（blog posts）、页面（pages）、条目（entries）、媒体文件（media files）的创建/上传/下载、翻译、本地化、发布等操作时，本 SDK 都能提供相应的帮助。
metadata: {"openclaw": {"emoji": "🔵", "requires": {"bins": ["node"], "env": ["STRAPI_API_TOKEN", "STRAPI_BASE_URL"]}, "primaryEnv": "STRAPI_API_TOKEN", "install": [{"id": "node", "kind": "node", "package": ".", "bins": ["node"], "label": "Install Strapi skill dependencies"}]}}
---
# Strapi CMS 技能

通过官方的 `@strapi/client` SDK，在无头（headless）的 Strapi CMS 实例中管理内容。

## 设置

在安装过程中，请在 API Key 字段中输入您的 **Strapi API Token**。
然后，在 `env` 部分添加 `STRAPI_BASE_URL`：

```json5
{
  skills: {
    entries: {
      strapi: {
        enabled: true,
        apiKey: "your-strapi-api-token",     // → STRAPI_API_TOKEN
        env: {
          STRAPI_BASE_URL: "http://localhost:1337/api"
        }
      }
    }
  }
}
```

## 功能

- **集合类型（Collection Types）**：查找、查询单个记录、创建、更新、删除记录
- **单个类型（Single Types）**：查找、更新、删除文档
- **内容洞察（Content Insights）**：发现内容类型、数据结构、组件、关联关系，并检查实际数据
- **数据结构管理（Schema Management）**：创建/更新/删除内容类型、组件和字段（具有破坏性操作）
- **表单布局（Form Layout）**：配置编辑表单中字段的顺序、大小、标签和描述（仅限本地/开发模式）
- **草稿与发布（Draft & Publish）**：列出草稿、发布、取消发布、将内容创建为草稿或已发布状态
- **文件（Files）**：列出文件、获取文件、上传文件（支持本地路径或 URL）、更新文件元数据、删除媒体文件
- **用户与权限（Users & Permissions）**：列出用户、创建用户、更新用户、删除用户；查看用户角色；登录、注册、重置密码
- **本地化（Locales）**：列出本地化设置、创建本地化资源、删除本地化资源
- **本地化内容（Localized Content）**：针对每个本地化设置进行 CRUD 操作；查看翻译状态；一次性获取所有本地化资源
- **原始数据获取（Raw Data Fetch）**：直接通过 HTTP 请求访问任何 Strapi 端点

## 使用方法

请参阅 [instructions.md](instructions.md) 以获取完整的代理使用说明。
请参阅 [examples/usage.md](examples/usage.md) 以了解使用示例。