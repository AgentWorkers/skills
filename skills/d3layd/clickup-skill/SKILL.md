---
name: clickup
description: "企业级 ClickUp 项目管理工具，具备高级报告功能、多工作区支持以及客户/项目跟踪能力。核心功能包括：  
1. 多工作区任务管理，支持自动切换工作区；  
2. 先进的分析与报告功能（任务数量统计、任务分配情况、状态/优先级分析、每日站会报告），支持子任务的自动包含和分页显示；  
3. 客户文件夹组织功能，包含项目跟踪功能（📋 客户概览、📁 已完成的工作、活跃项目列表）；  
4. 对工作区、文件夹、任务及自定义字段提供完整的 CRUD（创建、读取、更新、删除）操作；  
5. 时间跟踪与计时器管理功能，支持计费；  
6. 文档创建与页面管理（基于 API v3）；  
7. 任务依赖关系管理、任务链接及关系映射功能；  
8. 销售流程跟踪功能，可查看潜在客户/项目状态；  
9. 保留费及定期计费管理功能。  
专为需要在复杂工作区架构中管理多个客户的机构设计。"
---

# ClickUp Skill

**专为机构工作流程设计的企级ClickUp集成解决方案。**支持管理多个客户、项目和 workspace，具备高级报告功能、自动处理子任务以及完善的文件夹组织功能。

## 主要优势

| 功能 | 重要性说明 |
|---------|----------------|
| **🔍 自动包含子任务** | 永远不会错过70%以上的实际工作量——子任务会自动被包含在内 |
| **📊 高级报告** | 任务数量统计、工作量分布、状态明细、每日站会报告 |
| **🏢 多个工作空间** | 可在客户工作区、产品开发区、个人项目等之间无缝切换 |
| **👥 客户资料管理** | 结构化的文件夹：客户概览、已完成的工作、正在进行的项目 |
| **📈 销售流程管理** | 跟踪提案、谈判和项目生命周期 |
| **⏱️ 时间跟踪** | 内置计时器及手动输入功能，支持计费 |
| **📄 文档管理** | 通过API v3创建文档和页面 |
| **🔗 任务关联** | 任务之间的依赖关系、阻塞/等待关系以及任意任务链接 |

## 快速入门

### 设置
设置您的ClickUp API令牌：
```bash
export CLICKUP_API_TOKEN="pk_your_token_here"
```

从以下位置获取令牌：ClickUp设置 → 应用程序 → 生成API令牌

### 基本操作

**列出所有工作空间：**
```bash
python skills/clickup/scripts/clickup_client.py get_teams
```

**创建任务：**
```bash
python skills/clickup/scripts/clickup_client.py create_task list_id="123" name="New Task" status="to do"
```

**更新任务：**
```bash
python skills/clickup/scripts/clickup_client.py update_task task_id="abc" status="in progress"
```

## 工作空间层级结构

```
Team (Workspace)
├── Spaces
│   ├── Folders
│   │   └── Lists → Tasks
│   └── Lists (Folderless) → Tasks
└── Documents
```

所有操作都需要通过ID明确指定工作空间。

## 多工作空间支持

该功能支持在多个ClickUp工作空间中进行操作：

1. 使用`get_teams`列出可用的工作空间
2. 在操作中通过`team_id`引用工作空间
3. 每个工作空间都有独立的文件夹和列表
4. 自定义任务ID需要同时设置`custom_task_ids=true`和`team_id`

## 常见工作流程

### 在特定工作空间中创建任务

1. 获取工作空间ID：`get_teams`
2. 获取目标工作空间：`get_spaces team_id="xxx"`
3. 获取或创建列表：`get_folders space_id="yyy"` → `get_lists folder_id="zzz"`
4. 创建任务：`create_task list_id="aaa" name="Task" ...`

### 配置工作空间状态

1. 获取工作空间：`get_space space_id="xxx"`
2. 更新工作空间状态：`update_space space_id="xxx" statuses=[...]`

有关状态配置格式的详细信息，请参阅[API参考](references/api_reference.md)。

### 跟踪任务时间

**选项A - 手动输入：**
```bash
python skills/clickup_client.py create_time_entry \
  team_id="xxx" \
  task_id="yyy" \
  duration=3600000 \
  description="Worked on feature"
```

**选项B - 计时器：**
```bash
# Start timer
python skills/clickup/scripts/clickup_client.py start_timer team_id="xxx" task_id="yyy"

# Stop timer (stops current running timer for user)
python skills/clickup/scripts/clickup_client.py stop_timer team_id="xxx"
```

### 创建文档结构

1. 创建文档：`create_doc workspace_id="xxx" name="Project Docs"`
2. 添加页面：使用ClickUp用户界面（页面API处于测试阶段）

注意：文档使用ClickUp API v3（使用`workspace_id`而非`team_id`）。

### 报告与分析

**获取任务数量（包含子任务）：**
```bash
python skills/clickup/scripts/clickup_client.py task_counts team_id="xxx"
# Returns: {"total": 50, "parents": 20, "subtasks": 30, "unassigned": 5}
```

**按分配者获取工作量：**
```bash
python skills/clickup/scripts/clickup_client.py assignee_breakdown team_id="xxx"
# Returns: {"John Doe": 15, "Jane Smith": 12, "Unassigned": 8}
```

**按状态获取任务：**
```bash
python skills/clickup/scripts/clickup_client.py status_breakdown team_id="xxx"
# Returns: {"to do": 20, "in progress": 10, "complete": 15}
```

**按优先级获取任务：**
```bash
python skills/clickup/scripts/clickup_client.py priority_breakdown team_id="xxx"
# Returns: {"urgent": 2, "high": 5, "normal": 15, "low": 8, "none": 20}
```

**按状态分组的每日站会报告：**
```bash
# All team members
python skills/clickup/scripts/clickup_client.py standup_report team_id="xxx"

# Specific person (use user ID)
python skills/clickup/scripts/clickup_client.py standup_report team_id="xxx" assignee_id="12345"
```

**分页获取所有任务：**
```bash
python skills/clickup/scripts/clickup_client.py get_all_tasks team_id="xxx"
# Always includes subtasks automatically (critical!)
```

**按工作空间或分配者过滤报告：**
```bash
# Specific space
python skills/clickup/scripts/clickup_client.py task_counts team_id="xxx" space_ids='["SPACE_ID_HERE"]'

# Specific assignee
python skills/clickup/scripts/clickup_client.py get_all_tasks team_id="xxx" assignees='["12345"]'

# Include closed tasks
python skills/clickup/scripts/clickup_client.py task_counts team_id="xxx" include_closed="true"
```

**报告的关键规则：**
1. **始终包含子任务** — 我们的方法会通过`subtasks=true`自动包含子任务 |
2. **分页处理** — `get_all_tasks`会循环获取所有页面 |
3. **父任务与子任务的关系**：父任务的`parent`字段为`null`，子任务的`parent`字段为`task_id` |
4. **速率限制** — 每分钟100次请求；我们的分页功能遵循此限制

### 将文档链接到任务

**选项A - 作为附件添加：**
```bash
python skills/clickup/scripts/clickup_client.py link_doc_to_task \
  task_id="xxx" \
  doc_id="yyy"
```

**选项B - 在描述中提及：**
```bash
python skills/clickup/scripts/clickup_client.py mention_doc_in_task \
  task_id="xxx" \
  doc_id="yyy"
```

这两种方法都会在任务中创建可点击的文档链接。

### 任务依赖关系

**设置阻塞关系：**
```bash
# Task B is blocked by/waiting on Task A
python skills/clickup/scripts/clickup_client.py add_dependency \
  task_id="TASK_B_ID" \
  depends_on="TASK_A_ID"

# Check dependencies
python skills/clickup/scripts/clickup_client.py get_dependencies \
  task_id="TASK_B_ID"

# Remove dependency
python skills/clickup/scripts/clickup_client.py remove_dependency \
  task_id="TASK_B_ID" \
  depends_on="TASK_A_ID"
```

**设置反向依赖关系（任务被另一个任务阻塞）：**
```bash
# Task A is blocking Task B
python skills/clickup/scripts/clickup_client.py add_dependency \
  task_id="TASK_A_ID" \
  waiting_on="TASK_B_ID"
```

### 链接相关任务（非依赖关系）

对于不相互阻塞的相关任务：

```bash
# Link Task A to Task B (arbitrary relationship)
python skills/clickup/scripts/clickup_client.py link_tasks \
  task_id="TASK_A_ID" \
  links_to="TASK_B_ID"

# Remove link
python skills/clickup/scripts/clickup_client.py unlink_tasks \
  task_id="TASK_A_ID" \
  links_to="TASK_B_ID"
```

注意：`link_tasks`会创建“关联任务”关系（显示在任务的“关联任务”部分），而`add_dependency`会创建阻塞/等待关系。

### 批量任务操作

对于批量操作，可以循环处理任务：
```bash
# Get tasks
TASKS=$(python skills/clickup/scripts/clickup_client.py get_tasks list_id="xxx")

# Process each (parse JSON and loop)
```

## 脚本参考

### scripts/clickup_client.py

这是用于ClickUp操作的主要命令行接口。

**使用方法：**
```bash
python scripts/clickup_client.py <command> [key=value ...]
```

**命令：**

#### 工作空间操作
- `get_teams` - 列出所有可访问的工作空间

#### 工作空间操作
- `get_spaces team_id="xxx"` - 列出工作空间
- `create_space team_id="xxx" name="Name" [options...]` - 创建工作空间
- `update_space space_id="xxx" [options...]` - 更新工作空间

#### 文件夹操作
- `get_folders space_id="xxx"` - 列出文件夹
- `create_folder space_id="xxx" name="Name"` - 创建文件夹

#### 列表操作
- `get_lists folder_id="xxx"` - 列出文件夹内的列表
- `get_space_lists space_id="xxx"` - 无文件夹的列表
- `create_list folder_id="xxx" name="Name" [options...]` - 在文件夹中创建列表
- `create_space_list space_id="xxx" name="Name" [options...]` - 创建无文件夹的列表

#### 任务操作
- `get_task task_id="xxx"` - 获取任务详情（包括依赖关系和关联任务）
- `get_tasks list_id="xxx" [filters...]` - 列出任务
- `create_task list_id="xxx" name="Name" [options...]` - 创建任务
- `update_task task_id="xxx" [options...]` - 更新任务

#### 时间跟踪
- `get_time_entries team_id="xxx" [filters...]` - 列出时间记录
- `create_time_entry team_id="xxx" task_id="yyy" duration=3600000 [...]` - 创建时间记录
- `start_timer team_id="xxx" task_id="yyy"` - 启动计时器
- `stop_timer team_id="xxx"` - 停止计时器

#### 文档（API v3）
- `get_docs workspace_id="xxx"` - 列出文档
- `create_doc workspace_id="xxx" name="Name" [options...]` - 创建文档
- `get_doc doc_id="xxx"` - 获取文档详情

**关于页面：** 文档页面API处于测试阶段。可能需要通过ClickUp用户界面创建页面。

#### 文档与任务的关联
- `link_doc_to_task task_id="xxx" doc_id="yyy"` - 将文档URL附加到任务
- `mention_doc_in_task task_id="xxx" doc_id="yyy"` - 在任务描述中添加文档链接

#### 任务依赖关系（阻塞/等待）

- `add_dependency task_id="xxx" depends_on="yyy"` - 任务被另一个任务阻塞/等待
- `add_dependency task_id="xxx" waiting_on="yyy"` - 另一个任务被这个任务阻塞/等待
- `remove_dependency task_id="xxx" depends_on="yyy"` - 删除依赖关系
- `get_dependencies task_id="xxx"` - 获取任务的所有依赖关系

#### 任务链接（任意关系）

- `link_tasks task_id="xxx" links_to="yyy"` - 在任务之间创建任意链接
- `unlink_tasks task_id="xxx" links_to="yyy"` - 删除任务链接

#### 报告与分析
- `get_all_tasks team_id="xxx" [include_closed="true"] [space_ids='["id1"]'] [assignees='["uid1"]']` - 所有任务（包含子任务）
- `task_counts team_id="xxx" [filters...]` - 统计结果：总数、父任务、子任务、未分配任务
- `assignee_breakdown team_id="xxx" [filters...] - 按分配者分配工作量
- `status_breakdown team_id="xxx" [filters...] - 按状态分组任务
- `priority_breakdown team_id="xxx" [filters...] - 按优先级分组任务
- `standup_report team_id="xxx" [assignee_id="yyy"] - 按状态分组的每日站会报告`

#### 文档
- `get_docs team_id="xxx"` - 列出文档
- `create_doc team_id="xxx" name="Name" [options...] - 创建文档

## 高级配置

### 自定义字段

要使用自定义字段：

1. 获取字段定义：`GET /list/{list_id}/field`（详见API参考）
2. 在创建/更新任务时设置字段值：
   ```bash
   python skills/clickup/scripts/clickup_client.py update_task \
     task_id="xxx" \
     'custom_fields=[{"id":"field_id","value":"value"}]'
   ```

### 状态配置

在创建/更新工作空间或列表时：

```bash
python skills/clickup/scripts/clickup_client.py update_space \
  space_id="xxx" \
  'statuses=[{"status":"To Do","type":"open"},{"status":"Done","type":"closed"}]'
```

### 优先级等级

- `1` - 紧急
- `2` - 高
- `3` - 一般
- `4` - 低

## 错误处理

常见错误及解决方法：

| 错误 | 原因 | 解决方案 |
|-------|-------|----------|
| `401 Unauthorized` | API令牌无效 | 请检查CLICKUP_API_TOKEN |
| `404 Not Found` | ID无效 | 请验证工作空间/空间/文件夹/列表/任务ID |
| `429 Too Many Requests` | 超过请求速率限制 | 等待片刻后重试（每分钟100次请求限制） |
| `400 Bad Request` | 参数无效 | 请检查参数的JSON格式 |

## Python客户端使用

对于复杂操作，可以直接导入客户端库：

```python
from skills.clickup.scripts.clickup_client import ClickUpClient

client = ClickUpClient()

# Get all workspaces
teams = client.get_teams()

# Create task with full control
task = client.create_task(
    list_id="123",
    name="Complex Task",
    description="Detailed description",
    assignees=[123, 456],
    tags=["urgent", "client"],
    priority=2,
    due_date=1704067200000,
    time_estimate=14400000
)
```

## 参考资料

- **API详情**：请参阅[references/api_reference.md](references/api_reference.md)，了解完整的端点文档、请求/响应格式和字段类型。
- **ClickUp API文档**：https://clickup.com/api

## 最佳实践

1. **存储ID**：工作空间/空间/文件夹/列表的ID很少变化。将它们存储在`TOOLS.md`中以便快速参考。
2. **自定义任务ID**：如果使用自定义ID，请在任务操作中始终设置`custom_task_ids=true`和`team_id`。
3. **速率限制**：分散批量操作以避免429错误。
4. **时间跟踪**：所有持续时间/时间戳值请使用毫秒为单位。
5. **多工作空间**：在不同工作空间之间操作时，请务必检查`team_id`，以避免修改错误的工作空间。