---
name: meegle-api
description: Meegle Open API 功能概览（索引）。请根据您的需求阅读相应的功能说明。功能分类包括：凭证管理（Credentials）、用户管理（Users）、空间管理（Space）、工作项管理（Work Items）、设置管理（Settings）、评论管理（Comments）、视图管理（Views）以及测量数据管理（Measurement）。
metadata:
  openclaw: {}
  required_credentials:
    plugin_id: "Plugin ID; see meegle-api-credentials"
    plugin_secret: "Plugin secret; see meegle-api-credentials"
    domain: "API host; see meegle-api-credentials"
  optional_context:
    project_key: "Space identifier; in Meegle Developer Platform double-click the project icon to get it"
    user_key: "User identifier; in Meegle Developer Platform double-click the avatar to get it"
    user_access_token: "Required for write operations on behalf of user; obtain via OAuth (see meegle-api-credentials)"
---
# Meegle API（索引）

Meegle OpenAPI 包含以下子功能。请先阅读 **meegle-api-credentials** 文件，以了解域名、令牌、上下文以及请求头的相关信息；之后再根据您的需求选择相应的子功能进行阅读。

| 序号 | 子功能（路径） | 阅读时机 |
|-------|------------------|--------------|
| 1 | **meegle-api-credentials/SKILL.md** | 域名、令牌、上下文（project_key、user_key）以及请求头。在进行任何 Meegle API 调用之前，请务必阅读此文件。 |
| 2 | **meegle-api-users/SKILL.md** | 与用户相关的 OpenAPI 功能（例如用户组、用户信息等）。 |
| 3 | **meegle-api-space/SKILL.md** | 与项目空间相关的操作。 |
| 4 | **meegle-api-work-items/SKILL.md** | 创建、获取和更新工作项（任务、问题等）。 |
| 5 | **meegle-api-setting/SKILL.md** | 设置、工作项类型、字段以及流程配置。 |
| 6 | **meegle-api-comments/SKILL.md** | 对工作项或其他实体进行评论的功能。 |
| 7 | **meegle-api-views-measurement/SKILL.md** | 视图显示、看板展示、甘特图、数据统计等功能。 |

所有子功能都位于 `meegle-api-skill/` 目录下（例如 `meegle-api-users/SKILL.md`）。当需要使用某个特定的 API 功能时，请通过相应的路径使用 `Read` 工具来获取详细信息。