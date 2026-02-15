---
name: meegle-api-work-items
description: |
  Meegle OpenAPI for work items: create, get, update, and related operations. Prerequisites: token and domain — see skill meegle-api-users.
metadata:
  { "openclaw": {} }
---

# Meegle API — 工作项

在 Meegle 空间中创建和管理工作项（任务、故事、漏洞等）。

**先决条件：** 首先获取域名和访问令牌；有关域名、插件访问令牌（plugin_access_token）/ 用户访问令牌（user_access_token）以及请求头的详细信息，请参阅技能文档 **meegle-api-users**。

---

## 创建工作项

在 Meegle 空间中创建一个新的工作项。支持多种工作项类型、模板和自定义字段。需要具备 “Work Items” 权限。

### 使用场景

- 当需要创建新的任务、故事、漏洞或其他工作项时
- 当需要将结构化的工作内容保存到 Meegle 中时
- 当需要通过编程方式初始化工作流程或规划相关事项时

### API 规范：create_work_item

```yaml
name: meegle.create_work_item
description: >
  Create a new work item in a specified Meegle space.
  Supports different work item types, templates, and custom fields.
  Requires permission: Work Items.

when_to_use:
  - When creating a new task, story, bug, or other work item
  - When an AI needs to persist structured work into Meegle
  - When initializing workflows or planning items programmatically

http:
  method: POST
  path: /open_api/{project_key}/work_item/create
  auth: plugin_access_token

path_parameters:
  project_key:
    type: string
    required: true
    description: Space ID (project_key) or space domain name (simple_name)

body_parameters:
  work_item_type_key:
    type: string
    required: false
    description: Work item type key (e.g. story, task, bug)

  template_id:
    type: integer
    required: false
    description: >
      Work item process template ID.
      If omitted, the default template of the work item type is used.

  name:
    type: string
    required: false
    description: Work item name

  required_mode:
    type: integer
    required: false
    default: 0
    enum:
      - 0  # do not validate required fields
      - 1  # validate required fields and fail if missing

  field_value_pairs:
    type: list[object]
    required: false
    description: >
      Field configuration list.
      Field definitions must match metadata from
      "Get Work Item Creation Metadata".
    item_schema:
      field_key:
        type: string
        required: true
      field_value:
        type: any
        required: true
      notes:
        - For option/select fields, value must be option ID
        - Cascading fields must follow configured option hierarchy
        - role_owners must follow role + owners structure

response:
  data:
    type: integer
    description: Created work item ID
  err_code:
    type: integer
  err_msg:
    type: string

error_handling:
  - code: 30014
    meaning: Work item type not found or invalid
  - code: 50006
    meaning: Role owners parsing failed or template invalid
  - code: 20083
    meaning: Duplicate fields in request
  - code: 20038
    meaning: Required fields not set

constraints:
  - name must not also appear in field_value_pairs
  - template_id must not appear in field_value_pairs
  - option-type fields must use option ID, not label
  - role_owners default behavior depends on process role configuration

examples:
  minimal:
    project_key: doc
    body:
      work_item_type_key: story
      name: "New Story"

  full:
    project_key: doc
    body:
      work_item_type_key: story
      template_id: 123123
      name: "Example Work Item"
      field_value_pairs:
        - field_key: description
          field_value: "Example description"
        - field_key: priority
          field_value:
            value: "xxxxxx"
        - field_key: role_owners
          field_value:
            - role: rd
              owners:
                - testuser
```

### 使用说明

- **project_key**：路径参数，必填。可以使用空间 ID（project_key）或空间域名（simple_name）。
- **name**：工作项名称；请勿同时在 `field_value_pairs` 中重复发送该名称。
- **field_value_pairs**：在此处发送其他字段（描述、优先级、分配者等）；对于选项类型的字段，请使用选项 ID，而不是显示标签。
- 在创建工作项之前，请先调用 “Get Work Item Creation Metadata” 来获取该类型和模板的字段元数据，然后据此构建 `field_value_pairs`。

---

## 其他工作项 API（待文档化）

获取工作项信息、更新工作项、列出工作项等相关接口的详细信息将在后续文档中提供。