---
name: deepresearch-conversation
description: Deep ReSearch Conversation 是由百度提供的一项服务，支持与“深度研究”代理进行多轮流式对话。这种“深度研究”任务是一个涉及多步骤推理和执行的长过程，与普通的“问答”方式有所不同。它需要用户不断验证和修正自己的回答，直到得到令人满意的答案为止。
metadata: { "openclaw": { "emoji": "📌", "requires": { "bins": ["python3", "curl"], "env": ["BAIDU_API_KEY"] }, "primaryEnv": "BAIDU_API_KEY" } }
---

# 深度研究对话

该功能允许 OpenClaw 代理与用户就特定主题进行深入的研究讨论。API 密钥会自动从 OpenClaw 配置文件中加载，无需手动设置。

## API 表格
|    名称    |               路径              |            描述                |
|------------|---------------------------------|---------------------------------------|
|DeepresearchConversation|/v2/agent/deepresearch/run|多轮流式深度研究对话（通过 Python 脚本实现）|
|ConversationCreate|/v2/agent/deepresearch/create|创建新的对话会话，返回会话 ID|
|FileUpload|/v2/agent/file/upload|为对话上传文件|
|FileParseSubmit|/v2/agent/file/parse/submit|提交上传的文件以进行解析|
|FileParseQuery|/v2/agent/file/parse/query|查询文件解析任务的进度|

## 工作流程

### 方式 A：无文件的主题讨论
1. 直接使用用户的查询内容调用 **DeepresearchConversation**。系统会自动创建一个新的对话会话。

### 方式 B：包含文件的主题讨论
1. 调用 **ConversationCreate** 以获取 `conversation_id`。
2. 使用 `conversation_id` 调用 **FileUpload** 上传文件。
3. 使用返回的 `file_id` 调用 **FileParseSubmit**。
4. 每隔几秒调用一次 **FileParseQuery**，直到文件解析完成。
5. 使用 `query`、`conversation_id` 和 `file_ids` 调用 **DeepresearchConversation**。

### 多轮对话规则
- **DeepresearchConversation** API 是一个 **SSE 流式** 接口，会逐步返回数据。
- 在第一次调用之后，后续的所有调用都必须传递 `conversation_id`。
- 如果响应中包含 `interrupt_id`（表示需要“进一步澄清”或“确认大纲内容”），下一次调用必须包含该 `interrupt_id`。
- 如果响应中包含 `structured_outline`，请将其展示给用户以供确认或修改，然后在下一次调用中传递最终的大纲内容。
- 重复调用 **DeepresearchConversation**，直到用户对结果满意为止。

## API

### ConversationCreate API

#### 参数
无参数

#### 执行 shell 命令
```bash
curl -X POST "https://qianfan.baidubce.com/v2/agent/deepresearch/create" \
  -H "X-Appbuilder-From: openclaw" \
  -H "Authorization: Bearer $BAIDU_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{}'
```

### FileUpload API

#### 参数
- `agent_code`: 固定值 `"deepresearch"`（必填）
- `conversation_id`: 来自 `ConversationCreate` 的响应（必填）
- `file`: 本地文件二进制文件（与 `file_url` 互斥）。最多支持上传 10 个文件。支持的文件格式：
  - 文本文件：.doc, .docx, .txt, .pdf, .ppt, .pptx（txt 文件大小不超过 10MB，pdf 文件不超过 100MB/3000 页，doc/docx 文件不超过 100MB/2500 页，ppt/pptx 文件不超过 400 页）
  - 电子表格文件：.xlsx, .xls（文件大小不超过 100MB，仅支持单个工作表）
  - 图像文件：.png, .jpg, .jpeg, .bmp（每个文件大小不超过 10MB）
  - 音频文件：.wav, .pcm（文件大小不超过 10MB）
- `file_url`: 文件的公共 URL（与 `file` 互斥）

#### 本地文件上传
```bash
curl -X POST "https://qianfan.baidubce.com/v2/agent/file/upload" \
  -H "Authorization: Bearer $BAIDU_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -H "X-Appbuilder-From: openclaw" \
  -F "agent_code=deepresearch" \
  -F "conversation_id=$conversation_id" \
  -F "file=@local_file_path"
```

#### 文件 URL 上传
```bash
curl -X POST "https://qianfan.baidubce.com/v2/agent/file/upload" \
  -H "Authorization: Bearer $BAIDU_API_KEY" \
  -H "Content-Type: multipart/form-data" \
  -H "X-Appbuilder-From: openclaw" \
  -F "agent_code=deepresearch" \
  -F "conversation_id=$conversation_id" \
  -F "file_url=$file_url"
```

### FileParseSubmit API

#### 参数
- `file_id`: 来自 `FileUpload` 的响应（必填）

#### 执行 shell 命令
```bash
curl -X POST "https://qianfan.baidubce.com/v2/agent/file/parse/submit" \
  -H "Authorization: Bearer $BAIDU_API_KEY" \
  -H "Content-Type: application/json" \
  -H "X-Appbuilder-From: openclaw" \
  -d '{"file_id": "$file_id"}'
```

### FileParseQuery API

#### 参数
- `task_id`: 来自 `FileParseSubmit` 的响应（必填）

#### 执行 shell 命令
```bash
curl -X GET "https://qianfan.baidubce.com/v2/agent/file/parse/query?task_id=$task_id" \
  -H "Authorization: Bearer $BAIDU_API_KEY" \
  -H "X-Appbuilder-From: openclaw"
```

### DeepresearchConversation API

#### 参数
- `query`: 用户的问题或研究主题（必填）
- `conversation_id`：首次调用时可选（系统自动生成），后续调用时必填。
- `file_ids`: 已解析文件的 ID 列表（可选，仅在讨论文件时使用）
- `interrupt_id`: 在响应“需要进一步澄清”或“确认大纲内容”时必填。该 ID 可在之前 SSE 响应的 `content.text.data` 中找到。
- `structured_outline`: 研究报告的大纲内容。如果上一轮生成了大纲，则在后续调用中必填。大纲结构如下：
```json
{
    "title": "string",
    "locale": "string",
    "description": "string",
    "sub_chapters": [
        {
            "title": "string",
            "locale": "string",
            "description": "string",
            "sub_chapters": []
        }
    ]
}
```
- `version`: `"Lite"`（速度更快，耗时约 10 分钟）或 `"Standard"`（解析更详细，耗时较长）。默认值为 `"Standard"`。

#### 执行 shell 命令
```bash
python3 scripts/deepresearch_conversation.py '{"query": "your question here", "version": "Standard"}'
```

#### 包含所有参数的示例
```bash
python3 scripts/deepresearch_conversation.py '{"query": "the question", "file_ids": ["file_id_1"], "interrupt_id": "interrupt_id", "conversation_id": "conversation_id", "structured_outline": {"title": "Report Title", "locale": "zh", "description": "desc", "sub_chapters": [{"title": "Chapter 1", "locale": "zh", "description": "chapter desc", "sub_chapters": []}]}, "version": "Standard"}'
```