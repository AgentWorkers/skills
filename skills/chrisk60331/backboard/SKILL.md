---
name: backboard
description: 通过位于 http://localhost:5100 的本地后端，将 Backboard.io 集成到助手、线程、内存管理以及文档 RAG（Random Access Group）系统中。
---

## 工具

该技能与一个本地 Flask 后端相连，该后端用于封装 Backboard SDK。后端必须运行在 `http://localhost:5100` 上。

### backboard_create_assistant

创建一个新的 Backboard 助手，包括名称和系统提示语。

**参数：**
- `name`（字符串，必填）：助手的名称
- `system_prompt`（字符串，必填）：助手的系统提示语

**示例：**
```json
{
  "name": "Support Bot",
  "system_prompt": "You are a helpful customer support assistant."
}
```

### backboard_list_assistants

列出所有可用的 Backboard 助手。

**参数：** 无

### backboard_get_assistant

获取特定助手的详细信息。

**参数：**
- `assistant_id`（字符串，必填）：助手的 ID

### backboard_delete_assistant

删除一个助手。

**参数：**
- `assistant_id`（字符串，必填）：要删除的助手的 ID

### backboard_create_thread

为某个助手创建一个新的对话线程。

**参数：**
- `assistant_id`（字符串，必填）：要创建线程的助手的 ID

### backboard_list_threads

列出所有对话线程，可选地按助手进行过滤。

**参数：**
- `assistant_id`（字符串，可选）：按助手 ID 过滤线程

### backboard_get_thread

获取某个线程及其消息历史记录。

**参数：**
- `thread_id`（字符串，必填）：线程的 ID

### backboard_send_message

向某个线程发送消息并获取回复。

**参数：**
- `thread_id`（字符串，必填）：线程的 ID
- `content`（字符串，必填）：消息内容
- `memory`（字符串，可选）：内存模式 - "Auto"、"Readonly" 或 "off"（默认值："Auto")

### backboard_add_memory

为某个助手存储一条可在对话中持续使用的内存记录。

**参数：**
- `assistant_id`（字符串，必填）：助手的 ID
- `content`（字符串，必填）：要存储的内容
- `metadata`（对象，可选）：内存记录的附加元数据

**示例：**
```json
{
  "assistant_id": "asst_123",
  "content": "User prefers Python programming and dark mode interfaces",
  "metadata": {"category": "preferences"}
}
```

### backboard_list_memories

列出某个助手的所有内存记录。

**参数：**
- `assistant_id`（字符串，必填）：助手的 ID

### backboard_get_memory

获取特定的内存记录。

**参数：**
- `assistant_id`（字符串，必填）：助手的 ID
- `memory_id`（字符串，必填）：内存记录的 ID

### backboard_update_memory

更新现有的内存记录。

**参数：**
- `assistant_id`（字符串，必填）：助手的 ID
- `memory_id`（字符串，必填）：内存记录的 ID
- `content`（字符串，必填）：内存记录的新内容

### backboard_delete_memory

删除一条内存记录。

**参数：**
- `assistant_id`（字符串，必填）：助手的 ID
- `memory_id`（字符串，必填）：要删除的内存记录的 ID

### backboard_memory_stats

获取某个助手的内存使用统计信息。

**参数：**
- `assistant_id`（字符串，必填）：助手的 ID

### backboard_upload_document

将文档上传到助手或线程中，以便进行 RAG（Retrieval-Augmented Generation，检索增强生成）处理。

**参数：**
- `assistant_id`（字符串，可选）：助手的 ID（使用此参数或 `thread_id`）
- `thread_id`（字符串，可选）：线程的 ID（使用此参数或 `assistant_id`）
- `file_path`（字符串，必填）：文档文件的路径

**支持的文件类型：** PDF、DOCX、XLSX、PPTX、TXT、CSV、MD、PY、JS、HTML、CSS、XML、JSON

### backboard_list_documents

列出某个助手或线程的所有文档。

**参数：**
- `assistant_id`（字符串，可选）：助手的 ID
- `thread_id`（字符串，可选）：线程的 ID

### backboard_document_status

检查上传文档的处理状态。

**参数：**
- `document_id`（字符串，必填）：文档的 ID

### backboard_delete_document

删除文档。

**参数：**
- `document_id`（字符串，必填）：要删除的文档的 ID

## 指令

当用户提出以下请求时，请使用相应的技能：

### 内存操作
- “记住……” 或 “存储这个……” → 使用 `backboard_add_memory`
- “你记得关于……什么？” → 使用 `backboard_list_memories` 或 `backboard_get_memory`
- “忘记……” 或 “删除内存记录……” → 使用 `backboard_delete_memory`
- “更新我的偏好设置……” → 使用 `backboard_update_memory`

### 文档操作
- “上传这个文档” 或 “索引这个文件” → 使用 `backboard_upload_document`
- “我有哪些文档？” → 使用 `backboard_list_documents`
- “我的文档准备好了吗？” → 使用 `backboard_document_status`

### 助手管理
- “创建一个新的助手” → 使用 `backboard_create_assistant`
- “列出我的助手” → 使用 `backboard_list_assistants`
- “删除助手” → 使用 `backboard_delete_assistant`

### 对话线程
- “开始一个新的对话” → 使用 `backboard_create_thread`
- “显示对话历史记录” → 使用 `backboard_get_thread`
- “向线程发送消息” → 使用 `backboard_send_message`

### 通用指南
1. 始终向用户确认操作是否成功。
2. 在创建助手时，建议使用有意义的名称和系统提示语。
3. 在上传文档之前，验证文件类型是否被支持。
4. 在使用内存记录时，向用户说明存储了哪些信息。
5. 应该为用户的上下文存储/跟踪线程 ID 和助手 ID。

## 示例

### 示例 1：存储用户偏好设置
- 用户： “记住我更喜欢深色界面和 Python 代码示例。”
- 操作： 调用 `backboard_add_memory`，传入内容 “用户更喜欢深色界面和 Python 代码示例” 以及元数据 `{"category": "preferences"}`
- 回复： “我已经存储了您的偏好设置。您更喜欢深色界面和 Python 代码示例。”

### 示例 2：创建一个助手
- 用户： “创建一个代码审核助手。”
- 操作： 调用 `backboard_create_assistant`，设置名称为 “Code Reviewer” 和系统提示语 “您是一个专业的代码审核员。请分析代码中的错误、性能问题及最佳实践，并提供建设性反馈。”
- 回复： “已创建您的 Code Reviewer 助手（ID：asst_xxx）。它已准备好审核代码并提供反馈。”

### 示例 3：上传并查询文档
- 用户： “上传我的项目文档，然后告诉我它包含哪些内容。”
- 操作 1： 调用 `backboard_upload_document` 上传文档。
- 操作 2： 等待处理结果，然后使用 `backboard_document_status` 检查处理状态。
- 操作 3： 使用 `backboard_send_message` 并设置内存模式为 “Auto” 来查询文档内容。
- 回复： “我已经上传并索引了您的文档。根据内容，该文档涵盖了……”

### 示例 4：启动一个对话线程
- 用户： “与我的支持助手开始一个新的对话。”
- 操作： 调用 `backboard_create_thread`，传入助手的 ID。
- 回复： “已启动一个新的对话线程（ID：thread_xxx）。您现在可以向您的支持助手发送消息。”

## 后端设置

该技能需要一个运行中的后端服务器。要启动后端，请执行以下操作：
1. 设置 `BACKBOARD_API_KEY` 环境变量。
2. 进入后端目录。
3. 运行 `./start.sh`。

后端将在 `http://localhost:5100` 上提供服务。

## API 端点参考

| 端点 | 方法 | 描述 |
|----------|--------|-------------|
| `/health` | GET | 健康检查 |
| `/assistants` | GET, POST | 列出/创建助手 |
| `/assistants/{id}` | GET, PATCH, DELETE | 获取/更新/删除助手 |
| `/assistants/{id}/threads` | GET, POST | 为助手创建/列出线程 |
| `/assistants/{id}/memory` | GET, POST | 列出/添加内存记录 |
| `/assistants/{id}/memory/{mid}` | GET, PATCH, DELETE | 获取/更新/删除内存记录 |
| `/assistants/{id}/memory/stats` | GET | 内存使用统计信息 |
| `/assistants/{id}/documents` | GET, POST | 列出/上传文档 |
| `/threads` | GET | 列出所有线程 |
| `/threads/{id}` | GET, DELETE | 获取/删除线程 |
| `/threads/{id}/messages` | POST | 向线程发送消息 |
| `/threads/{id}/documents` | GET, POST | 列出/上传线程文档 |
| `/documents/{id}/status` | GET | 文档处理状态 |
| `/documents/{id}` | DELETE | 删除文档 |