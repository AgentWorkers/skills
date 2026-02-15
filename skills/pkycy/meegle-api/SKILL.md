---
name: meegle-api
description: |
  Meegle Open API skills (index). Read the specific skill for your need. Order: Users, Space, Work Items, Setting, Comments, Views & Measurement.
metadata:
  { "openclaw": {} }
---

# Meegle API（索引）

Meegle OpenAPI 包含以下子功能。请先阅读 **meegle-api-users**，以了解域名和访问令牌的相关信息；之后再根据您的需求阅读相应的子功能文档。

| 序号 | 子功能（位于 `meegle-api/` 目录下的路径） | 阅读建议 |
|-------|-------------------------------------|--------------|
| 1 | **meegle-api-users/SKILL.md** | 域名、访问令牌、上下文（project_key、user_key）、请求头、全局限制。在调用任何 Meegle API 之前，请务必阅读此文档。 |
| 2 | **meegle-api-space/SKILL.md** | 与项目（space）相关的操作。 |
| 3 | **meegle-api-work-items/SKILL.md** | 创建、获取、更新工作项（任务、问题、漏洞）。 |
| 4 | **meegle-api-setting/SKILL.md** | 设置、工作项类型、字段、流程配置。 |
| 5 | **meegle-api-comments/SKILL.md** | 对工作项或其他实体进行评论。 |
| 6 | **meegle-api-views-measurement/SKILL.md** | 视图显示、看板、甘特图、数据统计功能。 |

所有子功能文档都存储在 `skills/meegle-api/` 目录下（例如：`skills/meegle-api/meegle-api-users/SKILL.md`）。当需要使用某个特定的 API 功能时，请访问相应的路径并使用相应的阅读工具（如 “Read”）。