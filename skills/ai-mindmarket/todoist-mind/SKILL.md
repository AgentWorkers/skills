---
name: todoist-manager
description: "在 Todoist 中管理任务：添加任务、更新任务状态（已完成/已删除）、设置任务日期/截止日期/优先级，以及浏览项目。请使用以下命令并指定所有必要的参数：  
`add_task(content, project_id, due_date, priority)`  
`complete_task(task_id)`  
`delete_task(task_id)`  
`list_projects()`"
metadata: {
    "openclaw":
      {
        "emoji": "♊️",
        "requires": { "bins": ["uv"], "env": ["todoist_api_token"], "config": ["browser.enabled"] },
        "primaryEnv": "todoist_api_token",
        "homepage":"https:t.me/fugguri"
      },
  }
---
# Todoist 管理器

## Todoist 管理器技能

本技能提供了与 Todoist API 交互的程序指南和实用脚本。

## 先决条件

**配置要求**：Todoist API 令牌需要被放置在 `./references/API_CONFIG.json` 文件的 `todoist_api_token` 字段中。**该令牌不会从环境变量中读取。**

## 核心工作流程

### 1. 添加任务

用于创建新的待办事项。该脚本应支持提取任务详情。

**命令示例**：
`scripts/todoist_api.py add_task --content "完成项目 X 的报告" --project_id "123456" --due_date "明天" --priority 2`

| 参数 | 描述 | Todoist 对应值 |
| :--- | :--- | :--- |
| `content` | 任务的文本内容。 | 必填 |
| `project_id` | 目标项目 ID。 | 可选 |
| `due_date` | 完成任务的日期/时间（例如：明天、今天、下周五上午 10 点）。 | 可选（使用 Todoist API 识别自然语言） |
| `priority` | 优先级（1-4）。 | 可选（1=高优先级，4=无优先级） |

### 2. 管理任务状态（完成/删除）

在已知任务 ID 的情况下，用于更改任务状态。

**命令**：
- **完成**：`scripts/todoist_api.py complete_task --task_id "78901"`
- **删除**：`scripts/todoist_api.py delete_task --task_id "78901"`

### 3. 项目导航

用于列出可用的项目，以便创建新任务。

**命令**：
- **列出项目**：`scripts/todoist_api.py list_projects`

**关于项目的说明**：初步测试确认，正确的基础 URL 为 `/api/v2/`。使用有效的令牌应该能够列出项目；如果令牌无效或缺少权限范围，则会返回 401/403 错误。列出项目的端点为 `/projects`。

## 当前状态

API 集成脚本 `scripts/todoist_api.py` 已经创建为一个 **模拟 stub**。它目前通过将预期的操作和参数打印到控制台来模拟 API 调用，而不是直接访问真实的 Todoist API。

此结构现已完成，您可以在此基础上填写实际的 API 凭据和实现细节。

## 资源（可选）

仅创建本技能实际需要的资源目录。如果不需要资源，请删除此部分。

### scripts/
可执行的代码（Python/Bash 等），可以直接运行以执行特定操作。

**其他技能中的示例**：
- PDF 技能：`fill_fillable_fields.py`、`extract_form_field_info.py` - 用于 PDF 操作的实用工具
- DOCX 技能：`document.py`、`utilities.py` - 用于文档处理的 Python 模块

**适用场景**：Python 脚本、shell 脚本或任何执行自动化、数据处理或特定操作的代码。

**注意**：脚本可以在不加载到上下文中的情况下执行，但 Codex 仍可以读取它们以进行修补或环境调整。

### references/
文档和参考资料，用于为 Codex 的处理过程提供信息。

**其他技能中的示例**：
- 产品管理：`communication.md`、`context_building.md` - 详细的工作流程指南
- BigQuery：API 参考文档和查询示例
- 财务：数据库模式文档、公司政策

**适用场景**：深入的文档、API 参考、数据库模式、全面的指南或 Codex 在工作时需要引用的任何详细信息。

### assets/
文件不直接加载到上下文中，而是用于生成最终的 Codex 输出中。

**其他技能中的示例**：
- 品牌样式：PowerPoint 模板文件（.pptx）、徽标文件
- 前端构建工具：HTML/React 模板项目目录
- 字体：字体文件（.ttf、.woff2）

**适用场景**：模板、样板代码、文档模板、图片、图标、字体或任何需要在最终输出中使用的文件。

---

**并非每个技能都需要这三种类型的资源。**