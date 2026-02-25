---
name: meegle-api
description: >
  Meegle Open API 功能索引。请根据您的需求查阅相应的功能说明。功能分类包括：凭证（Credentials）、用户（Users）、空间（Space）、工作项（Work Items）、设置（Setting）、评论（Comments）、视图（Views）以及测量（Measurement）。  
  当系统检测到所需的凭证（如 user_key、project_key）缺失时，应提醒用户需要哪些凭证以及从何处获取这些凭证（请参阅 meegle-api-credentials 文档），而不仅仅是简单地报告错误。
metadata:
  openclaw: {}
---
# Meegle API（索引）

Meegle OpenAPI 包含以下子功能。请先阅读 **meegle-api-credentials** 文件，以了解域名、令牌、上下文以及请求头的相关信息；之后再根据您的需求阅读相应的子功能文档。

| 序号 | 子功能（路径） | 阅读时机 |
|-------|------------------|--------------|
| 1 | **meegle-api-credentials/SKILL.md** | 域名、令牌、上下文（project_key、user_key）以及请求头。在调用任何 Meegle API 之前，请务必阅读此文件。 |
| 2 | **meegle-api-users/SKILL.md** | 与用户相关的 OpenAPI 功能（例如用户组、成员信息等）。 |
| 3 | **meegle-api-space/SKILL.md** | 与项目（space）相关的操作功能。 |
| 4 | **meegle-api-work-items/SKILL.md** | 创建、获取和更新工作项（任务、问题等）。 |
| 5 | **meegle-api-setting/SKILL.md** | 设置相关功能，包括工作项类型、字段以及流程配置。 |
| 6 | **meegle-api-comments/SKILL.md** | 对工作项或其他实体进行评论的功能。 |
| 7 | **meegle-api-views-measurement/SKILL.md** | 查看功能，包括看板视图、甘特图、图表以及数据统计等。 |

所有子功能文档都位于 `meegle-api-skill/` 目录下（例如 `meegle-api-users/SKILL.md`）。当需要使用某个特定的 API 功能时，请使用相应的路径并通过“Read”工具来获取相关文档。