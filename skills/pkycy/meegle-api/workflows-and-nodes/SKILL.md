---
name: meegle-api-workflows-and-nodes
description: Meegle OpenAPI 用于工作流和节点操作。先决条件：需要 token 和域名——详情请参阅 skill meegle-api-users。
metadata:
  openclaw: {}
  required_credentials:
    domain: "From meegle-api-users"
    plugin_access_token_or_user_access_token: "From meegle-api-users (obtain token first)"
---
# Meegle API — 工作流（Workflows）与节点（Nodes）

提供用于管理工作项流程（work item workflows）及流程节点（workflow nodes）的API。

**前提条件：** 需从 **meegle-api-users** 获取域名（domain）和访问令牌（access token）。

## 功能范围

- 获取工作流定义（Get workflow definitions）
- 列出工作流节点（List workflow nodes）
- 更新工作流/节点状态（Update workflow/node state）
- 相关的工作流端点（Related workflow endpoints）

*详细的API规范将随着文档的完善而陆续添加。*