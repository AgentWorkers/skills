---
name: meegle-api-work-items
description: Meegle OpenAPI 支持对工作项（work items）进行创建（create）、获取（get）、更新（update）、列出（list）、搜索（search）以及相关操作。
metadata:
  openclaw: {}
---
# Meegle API — 工作项（Work Items）

用于在 Meegle 空间中创建和管理工作项（任务、故事、漏洞等）。

---

## 相关 API 功能位置

| 功能          | 目录          | 描述                                      |
|---------------|--------------|-----------------------------------------|
| 创建/读取/更新工作项    | `work-item-read-and-write/` | 创建工作项、获取工作项详情、更新工作项                 |
| 列出及搜索工作项    | `work-item-lists/`     | 过滤、搜索、全文搜索、关联工作项、通用搜索                |
| 工作流与节点      | `workflows-and-nodes/`   | 与工作流和节点相关的 API                        |
| 任务（Tasks）     | `tasks/`        | 与任务相关的 API                            |
| 附件（Attachments） | `attachment/`      | 与工作项附件相关的 API                        |
| 空间关联（Space Association） | `space-association/` | 与空间关联相关的 API                        |
| 组（Groups）      | `group/`        | 与工作项组相关的 API                        |