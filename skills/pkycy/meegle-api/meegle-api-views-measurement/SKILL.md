---
name: meegle-api-views-measurement
description: |
  Meegle OpenAPI for views, kanban, Gantt, and measurement/charts. Prerequisites: token and domain — see skill meegle-api-users.
metadata:
  { "openclaw": {} }
---

# Meegle API — 视图与测量数据

这些API用于查询或管理视图（views）及测量数据（measurement data），包括获取视图详情、列出所有视图、获取指标（metrics）、生成图表等功能。

**先决条件：** 首先需要获取域名（domain）和访问令牌（access token）；有关域名、插件访问令牌（plugin_access_token）/用户访问令牌（user_access_token）以及请求头（request headers）的信息，请参阅相关技能文档 **meegle-api-users**。

## 将要文档化的API：

- 获取视图详情（Get View Detail）
- 列出所有视图（List Views）
- 获取视图相关的工作项（Get View Work Items）
- 测量数据/图表相关API（Measurement/Chart APIs）

这些API的详细使用说明将在此处进行文档化。