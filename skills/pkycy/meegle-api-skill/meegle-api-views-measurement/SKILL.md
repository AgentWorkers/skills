---
name: meegle-api-views-measurement
description: Meegle OpenAPI 支持视图（views）、看板（kanban）、甘特图（Gantt charts）以及测量/图表（measurement/charts）等功能。
metadata:
  openclaw: {}
---
# Meegle API — 视图与度量

这些API用于处理与视图、看板以及度量相关的操作（例如获取视图详情、列出视图、查看指标数据、生成图表等）。当您需要查询或管理视图或度量数据时，可以使用这些API。

---

## 获取视图列表及配置信息

搜索符合请求参数的视图列表及其相关配置信息。响应数据遵循FixView格式（包含view_id、name、view_type、auth、collaborators、created_at、created_by、quick_filters、system_view、view_url等字段）。权限要求：权限管理 – 视图。详情请参阅权限管理。

### 使用场景

- 按工作项类型（如故事、问题）列出或搜索视图，并可设置可选的过滤条件（view_name、view_ids、created_by、created_at）。
- 当您需要获取**view_id**、**view_url**或**quick_filters**，以便在“获取视图中的工作项列表”接口中使用，或用于视图管理界面时。
- 当需要分页显示视图结果时（**page_size**最大为10，**page_num**）；将**is_query_quick_filter**设置为true可包含快速过滤条件。

### API规范：get_list_of_views_and_settings

---


### 使用说明

- **work_item_type_key**：必填项；从“获取工作项类型”接口中获取。不支持**sub_task**。
- **view_ids**与**view_name**：如果设置了**view_ids**，则仅返回对应的视图，忽略**view_name**。**created_by**与view_name/view_ids同时使用时需满足AND条件。
- **created_at**：时间范围；省略**end**表示“截至现在”。时间戳以毫秒为单位。
- **data**字段：在“获取视图中的工作项列表”或更新/删除视图API中使用**view_id**。当**is_query_quick_filter**为true时，会填充**quick_filters**。
- **pagination**：包含total、page_num、page_size用于分页。

---

## 获取视图中的工作项列表

获取指定视图中的所有工作项实例列表。响应数据包含视图元数据（name、view_id、editable、created_at、created_by、modified_by）以及**work_item_id_list**。权限要求：权限管理 – 视图。详情请参阅权限管理。

### 使用场景

- 按**view_id**列出在固定视图中显示的工作项（可通过“获取视图列表及配置信息”接口或视图页面URL获取）。
- 当需要分页显示工作项ID时（**page_size**最大为200，**page_num**）；可使用**quick_filter_id**通过视图列表界面进行过滤。
- 不支持全景（多项目）视图；在这种情况下，请使用“获取视图中的工作项列表（全景视图）”接口。

### API规范：get_list_of_work_items_in_views

---


### 使用说明

- **view_id**：可从视图页面URL（例如`.../storyView/RHCFGTzDa` → view_id `RHCFGTzDa`）或“获取视图列表及配置信息”接口（data[]中的view_id）获取。
- **work_item_id_list**：此视图中显示的工作项ID列表；使用这些ID可以通过工作项API获取详细信息。
- **quick_filter_id**：可选；在**is_query_quick_filter**为true时，从“获取视图列表及配置信息”接口中的data[].quick_filters[].quick_filter_id获取。
- 查询结果限制：如果视图返回的工作项数量超过200,000个，将返回50006；请使用**quick_filter_id**或其他过滤条件进行筛选。
- **20012**：表示视图所属的空间与**project_key**不同；请使用正确的空间ID。

---

## 获取视图中的工作项列表（全景视图）

获取指定全景（多项目）视图中的所有工作项实例及其详细信息。响应数据遵循WorkItemInfo格式（包含id、name、work_item_type_key、project_key、simple_name、template_id、template、pattern、sub_stage、work_item_status、current_nodes、state_times、created_by、updated_by、created_at、updated_at、fields等字段）。权限要求：权限管理 – 视图。详情请参阅权限管理。

### 使用场景

- 当需要在**全景视图**中列出工作项时；请使用此API（而“获取视图中的工作项列表”接口在处理全景视图时会返回50006）。
- 当您需要获取每个工作项的完整详细信息（包括WorkItemInfo中的fields、current_nodes、state_times等字段）而不仅仅是ID时。
- 当需要分页显示工作项结果时（**page_size**最大为50，可设置**quick_filter_id**）。

### API规范：get_list_of_work_items_in_views_panorama

---


### 使用说明

- **view_id**：可从视图页面URL或“获取视图列表及配置信息”接口（data[]中的view_id）获取。必须是全景视图；对于固定视图，请使用“获取视图中的工作项列表”接口。
- **data**：每个元素都是完整的WorkItemInfo（包含id、name、work_item_type_key、project_key、simple_name、template、pattern、sub_stage、current_nodes、state_times、fields等字段）——无需为每个ID单独调用工作项详细信息API。
- **page_size**：最大为50（小于固定视图API的200）。
- **quick_filter_id**：可选；在**is_query_quick_filter**为true时，从“获取视图列表及配置信息”接口中获取。
- **20003**：当API需要按工作项类型进行过滤时，请确保提供了相应的参数（例如work_item_type_key）。

---

## 创建固定视图

在指定空间和工作项类型下创建一个固定视图。请求参数包括**work_item_id_list**（最多200个ID）、**name**以及可选的合作设置。响应数据包含新创建的视图信息（FixView格式：view_id、name、work_item_id_list、editable、created_by、created_at、modified_by）以及分页信息。权限要求：权限管理 – 视图与度量。详情请参阅权限管理。

### 使用场景

- 当需要为某种工作项类型（例如故事）创建一个新的固定视图，并指定工作项ID列表时。
- 当需要设置**cooperation_mode**（1：指定用户/团队；2：所有空间管理员；3：所有空间成员）以及可选的**cooperation_user_keys**/**cooperation_team_ids**时。
- 当您需要返回的**view_id**用于“获取视图中的工作项列表”或更新/删除视图时。

### API规范：create_fixed_view

---


### 使用说明

- **work_item_id_list**：必须是该空间内的有效工作项ID；最多200个ID。所有ID必须与**work_item_type_key**匹配（否则返回30005）。
- **cooperation_mode**：可选参数**1**：提供**cooperation_user_keys**和/或**cooperation_team_ids**；用户ID可从空间内的用户头像双击或租户内的用户列表中获取；团队ID可从“获取团队成员”接口中获取。
- **data.view_id**：用于“获取视图中的工作项列表”、“更新固定视图”或“删除视图”接口。

---


## 更新固定视图

在指定的固定视图中添加或删除工作项实例。请求参数包括**add_work_item_ids**或**remove_work_item_ids**（两者不可同时提供，且两者都不能为空）；每个列表最多包含200个ID。成功时，响应数据为空。权限要求：权限管理 – 视图与度量。详情请参阅权限管理。

### 使用场景

- 当需要向现有固定视图添加工作项（**add_work_item_ids**）或删除工作项（**remove_work_item_ids**）时。
- 当**view_id**来自“获取视图列表及配置信息”或“创建固定视图”接口时。
- 每个请求只能执行添加或删除操作之一；两个列表中至少有一个不能为空。

### API规范：update_fixed_view

---


### 使用说明

- **view_id**：可从视图页面URL或“获取视图列表及配置信息”/“创建固定视图”接口（data.view_id）获取。
- **add_work_item_ids**与**remove_work_item_ids**：每次请求只能传递其中一个参数，并且必须非空。如果两者都传递或都为空，将返回20005。
- 每个列表中的ID数量最多为200个（超过200个ID时返回1000053645）。
- **10001**：调用者无权限修改此视图。

---

## 创建条件视图

在指定空间和工作项类型下创建一个新的条件视图。请求参数包括**search_group**（过滤条件：使用conjunction、search_params以及param_key、value、operator）。响应数据包含**view_id**。权限要求：权限管理 – 视图。详情请参阅权限管理。

### 使用场景

- 当需要为某种工作项类型创建基于条件的视图（使用**search_group**（AND/OR以及search_params）时。
- 当需要设置**cooperation_mode**（1：指定用户/团队；2：所有空间管理员；3：所有空间成员）以及可选的**cooperation_user_keys**/**cooperation_team_ids**时。
- 当您需要返回的**view_id**用于“获取视图中的工作项列表”或更新/删除视图时。

### API规范：create_conditional_view

---


### 使用说明

- **project_key**：必须是正确的空间**project_key**（通过双击空间名称获取）；此API不支持**simple_name**（空间域名）。
- **search_group**：使用conjunction（例如“AND”）和search_params（每个参数包括param_key、value、operator，例如“=”）。**param_key**必须是支持的字段（无效时返回20029）。对于日期/时间字段，请使用UTC格式（例如`2024-09-01T00:00:00+07:00`）；过滤仅在日级别有效（不支持小时/分钟/秒级别）。
- **data.view_id**：用于“获取视图中的工作项列表”、“更新条件视图”或“删除视图”接口。
- **cooperation_mode**：可选参数**1**：提供**cooperation_user_keys**和/或**cooperation_team_ids**，与创建固定视图时的要求相同。

---

## 更新条件视图

更新指定条件视图的过滤条件和协作信息。请求参数包括**view_id**、**search_group**（必填）以及可选的**name**、**cooperation_mode**、**cooperation_user_keys**、**cooperation_team_ids**。成功时，响应数据为空（err_code为0）。权限要求：权限管理 – 视图。详情请参阅权限管理。

### 使用场景

- 当需要更改条件视图的过滤条件或协作设置时。
- 当**view_id**来自条件视图（例如通过“创建条件视图”接口或浏览器URL后缀（如.../multiProjectView/view_text → view_id "view_text"）获取时。
- 当需要重命名视图（**name**）或更新协作权限（**cooperation_mode**、**cooperation_user_keys**、**cooperation_team_ids**）时。

### API规范：update_conditional_view

---


### 使用说明

- 对于此API，**view_id**目前只能通过浏览器URL后缀获取（例如URL `.../multiProjectView/view_text` → view_id `"view_text"`）。使用正确的view_id，否则将返回30004。
- **project_key**：必须是正确的空间**project_key**；不支持**simple_name**。
- **search_group**：与创建条件视图时的结构相同（使用conjunction、search_params）；日期字段仅支持UTC格式。
- 成功时，响应数据为空；**err_code** 0表示操作成功。

---

## 删除视图

从指定空间中删除视图。支持删除**条件视图**、**固定视图**和**全景视图**。请求方法为DELETE，路径中包含**project_key**和**view_id**。成功时，响应数据为空（err_code为0）。权限要求：权限管理 – 视图。详情请参阅权限管理。

### 使用场景

- 当需要从空间中删除视图（固定视图、条件视图或全景视图）时。
- 当**view_id**来自“获取视图列表及配置信息”或“创建固定视图”接口时。

### API规范：delete_views

---


### 使用说明

- **view_id**：可从视图页面URL（例如`.../storyView/RHCFGTzDa` → view_id `RHCFGTzDa`）或“获取视图列表及配置信息”接口（data[]中的view_id）、“创建固定视图”接口（data.view_id）或“创建条件视图”接口（data.view_id）获取。
- **project_key**：可以是空间**project_key**或**simple_name**（与创建/更新条件视图时不同）。
- 适用于所有类型的视图：固定视图、条件视图和全景视图。

---


## 从图表中获取详细数据

检索指定指标图表的详细数据。请求方法为GET，路径中包含**project_key**和**chart_id**。响应数据包含图表信息（name、chart_id、chart_data_list，其中包含dim/value/is_zero_spec、dim_titles、quota_titles）。权限要求：权限管理 – 度量与视图。详情请参阅权限管理。

### 使用说明

- **chart_id**：从图表页面的浏览器URL中获取。
- **Timeout**：某些指标图表计算复杂，可能需要较长时间；请将**HTTP timeout**设置为超过60秒。
- **并发限制**：对指标数据的访问存在速率限制。请将**并发控制**设置为1**，即在单台机器上使用单线程串行调用；否则可能会受到速率限制。

### 使用场景

- 当需要根据**chart_id**获取特定指标图表的详细数据时（通过浏览器URL或“按视图ID查询所有图表”接口）。
- 当需要构建显示图表维度和配额值的仪表板或报告时。

### API规范：get_detailed_data_from_charts

---


### 使用说明

- **chart_id**：从查看图表时的浏览器URL或“按视图ID查询所有图表”接口中获取。
- **data.chart_data_list**：包含数据点数组；每个数据点包含**dim**（维度键值对）、**value**（配额键值对）以及**is_zero_spec**。**dim_titles**和**quota_titles**用于描述轴标签。
- **50006 / 1000051872**：表示图表配置有异常；请检查产品中标记为红色的配置并进行相应调整。
- **500006 / 1000050535**：表示**chart_id**无效或图表已被删除；请确认chart_id并确认图表是否存在。

---

## 按视图ID查询所有图表

按视图ID查询该空间下的所有指标图表。请求方法为POST，请求体中包含**project_key**和**view_id**；可选参数**page_num**（默认为1）和**page_size**（最大为200，默认为50）。响应数据包含**chart_list**（包含每个图表的chart_id和chart_name）以及**chart_page**（总页数、当前页码、每页数量）。权限要求：权限管理 – 视图与分析。详情请参阅权限管理。

### 使用场景

- 当需要按**view_id**列出视图下的所有指标图表时（通过“获取视图列表及配置信息”接口或视图页面URL获取）。
- 当您需要每个图表的**chart_id**和**chart_name**时（例如为了调用“从图表中获取详细数据”接口）。
- 当需要分页显示图表结果时（**page_size**最大为200）。

### API规范：query_all_charts_by_view_id

---


### 使用说明

- **view_id**：可从视图页面URL（例如`.../storyView/RHCFGTzDa`）或“获取视图列表及配置信息”接口（data[]中的view_id）获取。
- **data.chart_list**：每个条目包含**chart_id**和**chart_name**；可以使用**chart_id**通过“从图表中获取详细数据”接口获取图表详细信息。
- **data.chart_page**：包含**total**（总页数或每个产品的总数）、**page_num**、**page_size**用于分页。
- **1000051401**：输入参数无效或不合理；请验证project_key和view_id。

---

---

这些API提供了Meegle平台中与视图、度量以及图表相关的各种操作。请根据实际需求选择合适的API进行调用，并确保遵守相应的权限管理规则。