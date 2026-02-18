---
name: meegle-api-work-items
description: >
  Meegle OpenAPI 支持对工作项（work items）进行创建（create）、获取（get）、更新（update）、列出（list）、搜索（search）及相关操作。  
  使用前提：需要具备有效的 token 和域名（domain）——详情请参阅技能文档 `meegle-api-users`。
metadata:
  openclaw: {}
  required_credentials:
    domain: "From meegle-api-users"
    plugin_access_token_or_user_access_token: "From meegle-api-users (obtain token first)"
---
# Meegle API — 工作项（Work Items）

用于在 Meegle 空间中创建和管理工作项（任务、问题、漏洞等）。

**前提条件：** 首先获取域名和访问令牌；请参阅技能 **meegle-api-users**。

---

## 在哪里找到相关技能

| 技能 | 目录          | 描述                          |
|-------|--------------|---------------------------------------------|
| 创建/读取/更新工作项 | `work-item-read-and-write/` | 创建工作项、获取工作项详情、更新工作项            |
| 列出和搜索工作项 | `work-item-lists/` | 过滤、搜索、全文搜索、关联项目、通用搜索                |
| 工作流和节点   | `workflows-and-nodes/` | 与工作流和节点相关的 API                    |
| 任务        | `tasks/`         | 与任务相关的 API                        |
| 附件        | `attachment/`       | 与工作项附件相关的 API                    |
| 空间关联     | `space-association/`   | 与空间关联相关的 API                    |
| 组          | `group/`         | 与工作项组相关的 API                        |