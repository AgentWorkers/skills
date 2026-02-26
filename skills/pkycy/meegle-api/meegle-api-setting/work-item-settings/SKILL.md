---
name: meegle-api-setting-work-item-settings
description: Meegle OpenAPI：用于工作项类型的基本设置（获取/更新）
metadata: { openclaw: {} }
---
# Meegle API — 设置（工作项设置）

用于获取基本工作项设置以及更新工作项的基本信息设置。

## 获取基本工作项设置

工作项类型的基本配置（type_key、name、flow_mode、schedule/estimate/actual 字段键、belong_roles、resource_lib_setting）。权限：工作项实例。

### API 规范：get_basic_work_item_settings

**用法：**  
`flow_mode`：`workflow` 或 `stateflow`  
`belong_roles`：用于调度/估算的角色的键。  
`work_item_type_key` 可通过 `Get Work Item Types in Space` 获取。

---

## 更新工作项的基本信息设置

用于更新工作项的描述、禁用状态（is_disabled）、固定状态（is_pinned）、调度/估算/实际完成时间字段（schedule/estimate/actual）、所属角色（belong_role_keys）以及实际工作时间切换状态（actual_work_time_switch）。权限：工作项；需要空间管理员权限（10005）。

### API 规范：update_work_item_basic_information_settings

**用法：**  
`work_item_type_key` 可通过 `Get Work Item Types in Space` 获取。  
`belong_role_keys`：来自流程角色的键。  
字段键（field keys）可通过 `Get Field Information` 获取。