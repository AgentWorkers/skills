---
name: memos-cloud-server
description: 这是您的外部“大脑”和“记忆”系统。每当您不确定用户的意图、过去的上下文，或者不知道答案时，请务必使用这个工具来查询记忆中的信息。不要猜测，先在 MemOS 云存储系统中进行搜索。当有重要信息需要记住时，也必须使用这个工具来完成记忆任务。
user-invocable: true
metadata: {"openclaw":{"emoji":"☁️","os":["darwin","linux","win32"],"requires":{"bins":["python3"],"env":["MEMOS_API_KEY", "MEMOS_USER_ID"]}}}
---
# MemOS Cloud Server Skill

该技能允许代理与 MemOS Cloud API 进行交互，以实现内存的搜索、添加、删除以及反馈功能。

## ⚠️ 设置与安全规则（务必阅读）

在执行任何 API 操作之前，您（代理）必须确保以下环境变量已配置：

1. **获取凭证**：
   - `MEMOS_API_KEY`（MemOS Cloud 服务 API 密钥）和 `MEMOS_USER_ID`（当前用户的唯一标识符）必须已配置。
2. **自动配置**：
   - 如果这些变量不存在，请提示用户将它们保存到他们的全局环境配置文件中（例如：`~/.zshrc` 或 `~/.bashrc`）。

## 🛠 核心命令

您可以直接通过 `memos_cloud.py` 脚本来执行操作。该脚本会自动读取 `MEMOS_API_KEY` 环境变量。所有操作请求和响应都以 JSON 格式输出。

### 1. 搜索内存（`/v1/search/memory`）

搜索与用户查询相关的长期记忆内容。

**用法：**
```bash
python3 skills/memos-cloud-server/memos_cloud.py search <user_id> "<query>" [--conversation-id <id>]
```
**示例：**
```bash
python3 skills/memos-cloud-server/memos_cloud.py search "$MEMOS_USER_ID" "Python related project experience"
```

### 2. 添加消息（`/v1/add/message`）

用于将多轮对话中的重要内容存储到云端。
- `conversation_id`：必需。当前对话的 ID。
- `messages`：必需。必须是一个有效的 JSON 字符串，其中包含 `role` 和 `content` 字段。

**用法：**
```bash
python3 skills/memos-cloud-server/memos_cloud.py add_message <user_id> <conversation_id> '<messages_json_string>'
```
**示例：**
```bash
python3 skills/memos-cloud-server/memos_cloud.py add_message "$MEMOS_USER_ID" "topic-123" '[{"role":"user","content":"I like apples"},{"role":"assistant","content":"Okay, I noted that"}]'
```

### 3. 删除内存（`/v1/delete/memory`）

删除云端存储的记忆内容。根据 API 规范，`memory_ids` 是必需的。

**用法：**
```bash
# Delete by Memory IDs (comma-separated)
python3 skills/memos-cloud-server/memos_cloud.py delete "id1,id2,id3"
```

### 4. 添加反馈（`/v1/add/feedback`）

向云端添加关于对话的反馈，以修正或强化记忆内容。

**用法：**
```bash
python3 skills/memos-cloud-server/memos_cloud.py add_feedback <user_id> <conversation_id> "<feedback_content>" [--allow-knowledgebase-ids "kb1,kb2"]
```
**示例：**
```bash
python3 skills/memos-cloud-server/memos_cloud.py add_feedback "$MEMOS_USER_ID" "topic-123" "The previous answer was not detailed enough"
```