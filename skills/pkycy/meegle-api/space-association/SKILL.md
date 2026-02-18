---
name: meegle-api-space-association
description: Meegle OpenAPI 用于空间关联操作。前提条件：需要 token 和域名——详情请参阅 skill meegle-api-users。
metadata:
  openclaw: {}
  required_credentials:
    domain: "From meegle-api-users"
    plugin_access_token_or_user_access_token: "From meegle-api-users (obtain token first)"
---
# Meegle API — 空间关联（Space Association）

提供用于将工作项（work items）与空间（spaces）关联以及管理这些关联的 API。

**前提条件：** 请从 **meegle-api-users** 获取域名（domain）和访问令牌（access token）。

## 功能范围

- 将工作项与空间关联
- 列出或管理空间关联关系
- 相关的关联操作端点（association endpoints）

*详细的 API 规范将在相关文档完成编写后陆续添加。*