---
name: konteks
version: 1.0.1
author: jamesalmeida
description: 将您的 OpenClaw 代理连接到 Konteks 账户（konteks.app），以实现持久化存储、任务管理以及上下文共享功能。当您需要存储代理的运行状态、创建或读取任务/笔记、查看项目及文件夹、阅读每日计划，或在不同对话之间同步上下文时，请使用该功能。连接前需获取来自 konteks.app/dashboard/settings 的 Konteks API 密钥。
when: User asks to create/manage tasks, store memories, check projects, read daily plans, or manage notes in Konteks
examples:
  - Create a task to review the PR
  - What's on my agenda today
  - Remember that I prefer dark mode
  - Check my inbox for new items
  - What projects do I have
tags:
  - memory
  - tasks
  - notes
  - projects
  - context
  - productivity
metadata: { "openclaw": { "emoji": "🧠", "requires": { "env": ["KONTEKS_API_KEY"] }, "primaryEnv": "KONTEKS_API_KEY" } }
---

# Konteks — 代理上下文层

**来源:** https://github.com/jamesalmeida/openclaw-konteks-skill

连接到您人类的 Konteks 账户，以访问持久化存储的数据、任务、笔记和项目信息。

## 设置

您的人类需要完成以下操作：
1. 在 https://konteks.app 注册
2. 进入设置 → 生成 API 密钥
3. 将 API 密钥添加到 OpenClaw 的配置文件中：

```yaml
skills:
  konteks:
    apiKey: "sk_..."
    url: "https://konteks.app"  # optional, defaults to this
    agentId: "my-agent"         # optional, defaults to "default"
```

## API 基础

所有端点：`{url}/api/agent/...`
认证头：`Authorization: Bearer {apiKey}`

---

## 混合内存架构

当此技能被安装后，将采用**混合内存架构**：使用 Konteks 数据库存储结构化数据，使用本地文件作为快速的临时存储空间。

### Konteks 数据库（共享的信息源）
使用 Konteks 存储以下内容，这些内容需要被您的人类查看或需要在不同设备间保持同步：
- **任务与项目**——由人类或代理创建，可在 iOS 和网页应用中查看
- **项目与领域**——组织结构信息
- **决策记录**——记录选择某个选项的原因（归类为 `decision`）
- **偏好设置**——用户逐渐形成的偏好设置（归类为 `preference`）
- **学习内容**——具有长期价值的信息（归类为 `learning`）
- **项目笔记**——与特定项目相关的上下文信息（归类为 `project_note`）

### 本地 Markdown 文件（代理的临时存储空间）
继续使用本地文件（`memory/*.md`、`MEMORY.md`）来存储：
- **每日会话日志**——记录当天发生的事件
- **当前工作内容**——您在当前会话中正在思考的内容
- **草稿与临时笔记**——尚未准备好上传到 Konteks 的想法

### 两者之间的协作方式
- **会话开始时**：从 Konteks 获取最近的记忆信息（`GET /api/agent/context?limit=10`）以恢复会话上下文。同时像往常一样读取本地文件。
- **对话过程中**：使用本地 Markdown 文件快速做笔记。当有重要决策或新知识产生时，也将其记录到 Konteks 中。
- **重要时刻之后**：将决策和学习内容写入 Konteks，以确保它们在应用程序中得到保存，并且不会因本地文件更改而丢失。
- **心跳机制**：检查 Konteks 中的待办事项和到期任务，并更新本地的心跳状态。
- **如果无法访问 Konteks**：切换到本地文件。即使没有网络连接，您也应能够正常工作。

通过这种方式，您的人类可以在他们的 Konteks 应用程序中查看重要的上下文信息，而您也可以快速访问本地存储的数据。这两个系统都不是单点故障。

---

## 主动行为（心跳机制）

**当此技能被安装后，代理应在心跳机制中主动使用 Konteks。** 将以下操作添加到您的心跳处理流程中：

### 1. 收件箱分类
检查收件箱中的新项目，并将其归类到相应的项目或领域中：

```bash
# Fetch inbox items
curl -s "{url}/api/agent/items?smart_list=inbox&completed=false&archived=false&limit=20" \
  -H "Authorization: Bearer {apiKey}"
```

**分类规则：**
- 如果项目明确属于某个项目或领域 → 将其移动到相应位置（使用 `folder_id` 进行更新，同时清除 `smart_list`）
- 如果不确定项目所属的领域 → **将其留在收件箱中**。不要随意猜测。
- 如果项目可以由代理自行处理（例如，“更新 X”、“检查 Y”） → 完成处理后标记为已完成
- **切勿删除收件箱中的项目**——只需将其移动或保留即可

```bash
# Move item to a folder (clears smart_list automatically when folder_id is set)
curl -X PATCH "{url}/api/agent/items/{id}" \
  -H "Authorization: Bearer {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{"folder_id":"<folder-id>","smart_list":null}'
```

### 到期任务
检查今天到期的或已经过期的任务：

```bash
curl -s "{url}/api/agent/items?completed=false&archived=false&limit=50" \
  -H "Authorization: Bearer {apiKey}"
```

筛选出 `due_date` 或 `scheduled_date` 为今天的任务，并提醒您的人类注意紧急事项。

### 重要时刻后的记录
在对话中做出重要决策或学到新知识后，将其记录到 Konteks 中：

```bash
curl -X POST "{url}/api/agent/context" \
  -H "Authorization: Bearer {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{"category":"decision","key":"descriptive_key","value":"What was decided and why","agent_id":"{agentId}"}'
```

### 会话开始时恢复上下文
在重要的会话开始时（例如与人类进行主要交流时），从 Konteks 中获取最近的记忆信息：

```bash
curl -s "{url}/api/agent/context?limit=10" \
  -H "Authorization: Bearer {apiKey}"
```

### 心跳机制的集成
将以下代码添加到您的 `HEARTBEAT.md`（或等效文件）中：

```markdown
## Konteks Checks
- [ ] Check inbox for new items — triage if obvious, leave if not
- [ ] Check for due/overdue tasks — alert if urgent
- [ ] Write any recent decisions/learnings to agent_contexts
```

**频率：** 在每次心跳机制中检查收件箱和到期任务 2-3 次。不要每次心跳都进行检查，可以与其他任务轮换进行。

---

## 代理内存（agent_contexts）

用于存储和检索持久化的记忆信息、决策记录、偏好设置和学习内容。

**写入/更新内存：**
```bash
curl -X POST "{url}/api/agent/context" \
  -H "Authorization: Bearer {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{"category":"memory","key":"user_preference","value":"Prefers dark mode","agent_id":"{agentId}"}'
```

分类：`memory`、`decision`、`preference`、`learning`、`project_note`

更新操作会自动触发——相同的 `agent_id`、`category` 和 `key` 会更新现有条目。

**读取内存：**
```bash
curl "{url}/api/agent/context?category=memory&limit=20" \
  -H "Authorization: Bearer {apiKey}"
```

查询参数：`category`、`key`、`limit`

**删除：**
```bash
curl -X DELETE "{url}/api/agent/context?id={contextId}" \
  -H "Authorization: Bearer {apiKey}"
```

## 任务与笔记（项目）

**列出项目：**
```bash
curl "{url}/api/agent/items?archived=false&completed=false&limit=50" \
  -H "Authorization: Bearer {apiKey}"
```

查询参数：`smart_list`（收件箱|任意时间|未来某天）、`folder_id`、`completed`（true|false）、`archived`（true|false）、`item_type`（任务|笔记|混合类型）、`limit`

**创建项目：**
```bash
curl -X POST "{url}/api/agent/items" \
  -H "Authorization: Bearer {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{"title":"Review PR","item_type":"task","smart_list":"inbox","priority":"high","tags":["dev"]}'
```

必填字段：`title`、`item_type`（任务|笔记|混合类型）
可选字段：`body`、`folder_id`、`smart_list`（收件箱|任意时间|未来某天——如果没有指定文件夹，则默认为收件箱）、`priority`（高|正常|低）、`due_date`、`scheduled_date`、`tags`（字符串数组）

由代理创建的项目会标记 `source: "ai"`。

**更新项目：**
```bash
curl -X PATCH "{url}/api/agent/items/{id}" \
  -H "Authorization: Bearer {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{"completed_at":"2026-01-29T12:00:00Z"}'
```

可更新字段：`title`、`body`、`priority`、`due_date`、`scheduled_date`、`tags`、`completed_at`、`archived_at`、`canceled_at`、`folder_id`、`smart_list`

**删除项目：**
```bash
curl -X DELETE "{url}/api/agent/items/{id}" \
  -H "Authorization: Bearer {apiKey}"
```

## 项目与领域（文件夹）

**列出文件夹：**
```bash
curl "{url}/api/agent/folders?type=project" \
  -H "Authorization: Bearer {apiKey}"
```

查询参数：`type`（项目|领域）

**创建文件夹：**
```bash
curl -X POST "{url}/api/agent/folders" \
  -H "Authorization: Bearer {apiKey}" \
  -H "Content-Type: application/json" \
  -d '{"name":"Q1 Launch","folder_type":"project","icon":"🚀","goal":"Ship MVP by March"}'
```

必填字段：`name`、`folder_type`（项目|领域）
可选字段：`icon`、`color`、`goal`

## 每日计划

**获取今天的计划：**
```bash
curl "{url}/api/agent/plans?date=2026-01-29" \
  -H "Authorization: Bearer {apiKey}"
```

返回内容：`task_ids`、`summary`、`rationale`、`available_minutes`、`calendar_events`

---

## 使用模式

**会话开始时：** 读取最近的记忆信息以恢复会话上下文。
```
GET /api/agent/context?category=memory&limit=10
```

**做出重要决策后：** 创建记忆记录。
```
POST /api/agent/context {"category":"decision","key":"chose_react","value":"Chose React over Vue for the dashboard because..."}
```

**当人类请求创建任务时：** 在 Konteks 中创建任务，使其在他们的应用程序中显示。
```
POST /api/agent/items {"title":"...","item_type":"task","smart_list":"inbox"}
```

**在心跳机制期间：** 检查收件箱、对项目进行分类、检查到期任务。
```
GET /api/agent/items?smart_list=inbox&completed=false&archived=false&limit=20
GET /api/agent/items?completed=false&archived=false&limit=50
```

**学到新知识时：** 将其存储起来以备后续会话使用。
```
POST /api/agent/context {"category":"learning","key":"ssh_config","value":"Home server is at 192.168.1.100, user admin"}
```

**整理收件箱中的项目：** 将项目归类到正确的项目或领域中。
```
PATCH /api/agent/items/{id} {"folder_id":"<id>","smart_list":null}
```