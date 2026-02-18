---
name: meegle-api-work-item-tasks
description: Meegle OpenAPI 用于工作项任务操作。前提条件：需要 token 和域名——详情请参阅 skill meegle-api-users。
metadata:
  openclaw: {}
  required_credentials:
    domain: "From meegle-api-users"
    plugin_access_token_or_user_access_token: "From meegle-api-users (obtain token first)"
---
# Meegle API — 任务管理

这些API用于在Meegle空间中管理工作项任务。

**先决条件：** 从**meegle-api-users**获取域名和访问令牌。

## 功能范围

- 任务的创建、检索和更新
- 任务的生命周期和状态
- 与任务相关的接口

*详细的API规范将在相关文档中陆续提供。有关核心工作项操作的信息，请参阅`work-item-read-and-write`和`work-item-lists`。*