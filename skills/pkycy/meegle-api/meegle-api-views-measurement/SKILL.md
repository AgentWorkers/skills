---
name: meegle-api-views-measurement
description: Meegle OpenAPI 提供了视图、看板（Kanban）、甘特图（Gantt Chart）以及测量/图表（Measurement/Chart）等功能。
metadata: { openclaw: {} }
---
# Meegle API — 视图与度量

## 视图、看板及度量相关的OpenAPI：

- **列出视图**：列出所有视图、视图中的工作项、创建/更新/删除视图、图表数据等。
- **获取视图列表及配置**：根据请求参数在指定空间内搜索符合条件的视图列表，响应格式为FixView（包含view_id、name、view_type、auth、collaborators、created_at、created_by、quick_filters、system_view、view_url等）。权限要求：权限管理 – 视图。
- **按工作项类型列出视图**：根据工作项类型（如story、issue）列出视图，并可设置过滤条件（view_name、view_ids、created_by、created_at）。
- **获取视图ID、视图URL或快速过滤条件**：用于获取视图中的工作项列表或进行视图管理。
- **分页显示视图结果**：支持分页（每页最多10条记录，页码page_num），设置is_query_quick_filter为true可包含快速过滤条件。
- **获取视图中的工作项列表**：获取指定视图中的所有工作项信息，包括视图元数据（name、view_id、editable、created_at、created_by、modified_by）等。
- **获取全景视图（多项目）中的工作项列表**：获取全景视图中的所有工作项信息。
- **获取全景视图（多项目）中的工作项详细信息**：获取全景视图中的所有工作项的详细信息。
- **创建固定视图**：在指定空间和工作项类型下创建新的固定视图。
- **更新固定视图**：修改指定固定视图中的工作项或删除视图。
- **创建条件视图**：根据过滤条件创建新的条件视图。
- **删除视图**：从指定空间删除视图。

---

## 重要说明：

- 请确保翻译内容保持技术准确性，同时保持代码示例、命令和URL的原样。
- 技术术语（如OpenClaw、ClawHub、API、CLI等）保持英文不变。
- 仅翻译代码块中的注释，如果注释具有解释性。
- 保持原始文档的结构和组织方式不变。
- 不要添加或删除任何部分。