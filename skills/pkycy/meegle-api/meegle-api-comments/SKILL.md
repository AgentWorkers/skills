---
name: meegle-api-comments
description: |
  Meegle OpenAPI for comments on work items or other entities. Prerequisites: token and domain — see skill meegle-api-users.
metadata:
  { "openclaw": {} }
---

# Meegle API — 评论功能

与评论相关的 OpenAPI（例如：在工作项上添加、列出或更新评论）。当您需要创建或查询评论时，请使用这些 API。

**先决条件：** 首先获取域名和访问令牌；有关域名、插件访问令牌（plugin_access_token）/ 用户访问令牌（user_access_token）以及请求头的信息，请参阅技能文档 **meegle-api-users**。

## 将要记录的 API

- 创建评论（Create Comment）
- 列出评论（List Comments）
- 更新/删除评论（Update/Delete Comment）

这些相关端点的详细信息将在本文档中列出。