---
name: moltflow-ai
description: "AI驱动的WhatsApp功能：自动回复、语音转录、RAG知识库以及样式配置。使用场景包括：自动回复、语音转录、知识库查询、文档上传、样式训练以及学习模式。"
source: "MoltFlow Team"
version: "2.1.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

**MoltFlow**——专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化WhatsApp消息处理。  
**年费订阅可节省高达17%的费用**（[点击此处查看详情](https://molt.waiflow.app/checkout?plan=free）；提供免费试用计划，无需信用卡。  

# MoltFlow的AI功能  

MoltFlow具备基于AI的自动化功能，包括语音转录、RAG（Retrieval, Augmentation, and Generation）知识库、风格分析以及智能回复生成等。  

## 使用场景  

- **语音转录**：将WhatsApp语音消息转换为文本。  
- **知识库管理**：上传文档到知识库或从中搜索信息。  
- **回复生成**：利用AI生成合适的回复。  
- **风格训练**：根据聊天历史数据训练AI以匹配您的写作风格。  

## 前提条件  

1. **MOLTFLOW_API_KEY**：需在[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。  
2. **至少需使用Pro计划（每月29.90美元）**；Starter计划不支持AI功能。  
3. 基础URL：`https://apiv2.waiflow.app/api/v2`  
4. 所有AI相关接口前缀均为`/ai`。  

## 所需API权限  

| 权限范围 | 访问内容 |
|---------|---------|-------------------|
| `ai` | `读取/管理`数据 |

**注意：**  
- **聊天记录访问**：需用户明确授权。请在“设置”>“账户”>“数据访问”中启用该功能。  
- **发送消息**无需授权，仅读取聊天记录需授权。  

## 认证方式  

所有请求必须包含以下认证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

---

## **语音转录**  
使用Whisper AI技术将WhatsApp语音消息转录为文本。转录过程通过Celery后台进程异步执行。  

| 方法 | 接口地址 | 功能描述 |
|------|---------|-------------------|
| POST | `/ai/voice/transcribe` | 提交语音消息进行转录 |
| GET | `/ai/voice/status/{task_id}` | 查看转录任务状态 |
| GET | `/ai/messages/{message_id}/transcript` | 获取消息的转录结果 |

### 提交转录任务  
**POST** `/ai/voice/transcribe`  

**响应状态**：`200 OK`  

### 查看转录结果  
**GET** `/ai/messages/{message_id}/transcript`  

---

## **RAG知识库**  
上传文档以构建可搜索的知识库。AI在生成回复时会参考这些文档内容。  

| 方法 | 接口地址 | 功能描述 |
|------|---------|-------------------|
| POST | `/ai/knowledge/ingest` | 上传并索引文档 |
| POST | `/ai/knowledge/search` | 在文档中执行语义搜索 |
| GET | `/ai/knowledge/sources` | 列出所有已索引的文档 |
| DELETE | `/ai/knowledge/{source_id}` | 删除文档 |

### 上传文档  
**POST** `/ai/knowledge/ingest`（使用multipart/form-data格式）  
**文件要求**：PDF或TXT格式（文件大小不超过100MB）  

**响应状态**：`200 OK`  

**支持的文件类型**：`application/pdf`、`text/plain`  

### 搜索知识库  
**POST** `/ai/knowledge/search`  

**响应状态**：`200 OK`  

### 列出文档  
**GET** `/ai/knowledge/sources`  

**文档状态**：`processing`（处理中）、`indexed`（已索引）、`failed`（上传失败）  

### 删除文档  
**DELETE** `/ai/knowledge/{source_id}`  
**响应状态**：`204 No Content`  

---

## **风格分析（学习模式）**  
通过分析特定聊天的历史记录来训练AI以匹配您的写作风格。风格配置可针对单个聊天或所有消息进行设置。AI会在生成回复时自动选择最合适的风格。  

| 方法 | 接口地址 | 功能描述 |
|------|---------|-------------------|
| POST | `/ai/style/train` | 开始训练风格配置 |
| GET | `/ai/style/status/{task_id}` | 查看训练进度 |
| GET | `/ai/style/profile` | 获取当前风格配置 |
| GET | `/ai/style/profiles` | 查看所有风格配置 |
| DELETE | `/ai/style/profile/{profile_id}` | 删除风格配置 |

### 训练风格配置  
**POST** `/ai/style/train`  

**必填参数**：  
- `contact_id`（可选）：聊天ID（用于指定训练范围；如使用默认值`wa_chat_id`）  
- `session_id`（可选）：会话ID（用于限定训练范围）  
- `wa_chat_id`（可选）：WhatsApp聊天ID（用于指定训练范围；如需通用风格配置可省略）  
- `name`（可选）：配置名称（如“Sales”、“Support”等）  

**注意**：省略`session_id`和`wa_chat_id`可训练通用风格配置。  

**训练状态**：`200 OK`  

**查看风格配置**：  
**GET** `/ai/style/profile?contact_id=5511999999999@c.us`  

**列出所有风格配置**：  
**GET** `/ai/style/profiles`  

**删除风格配置**：  
**DELETE** `/ai/style/profile/{profile_id}`  
**响应状态**：`204 No Content`  

---

## **AI回复生成**  
利用RAG知识和风格配置生成智能回复。AI会综合考虑聊天历史、知识库内容及您的沟通风格。  

| 方法 | 接口地址 | 功能描述 |
|------|---------|-------------------|
| POST | `/ai/generate-reply` | 生成回复建议 |
| GET | `/ai/preview` | 预览生成的回复（不计入使用量） |

**生成回复**：  
**POST** `/ai/generate-reply`  

**响应状态**：`200 OK`  

**参数说明**：  
- `contact_id`：联系人的WhatsApp ID。  
- `context`：聊天上下文或客户问题（最多2000个字符）。  
- `use_rag`：是否包含知识库内容。  
- `apply_style`：是否应用训练好的风格配置。  
- `profile_id`：可选的特定风格配置ID（可跳过自动选择）。  
- `session_id`：会话ID（用于确定风格配置）。  
- `approved`：是否需要用户确认回复。  

**预览回复**：  
**GET** `/ai/preview?contact_id=5511999999999@c.us&context=What+are+your+hours&use_rag=true&apply_style=true`  
（与`generate-reply`接口返回相同格式，但不计入使用量。）  

## 安全机制  
MoltFlow的AI回复生成功能包含以下安全措施：  
- **输入验证**：检测并阻止恶意输入。  
- **意图验证**：对可疑或高风险意图进行确认。  
- **内容过滤**：检查生成内容是否包含个人身份信息（PII）或违反政策的内容。  
- **内容策略**：支持用户自定义的安全规则（详情见[moltflow-a2a技能文档]。  

---

## 示例操作  

- **上传文档到知识库**  
- **使用RAG生成回复**  
- **根据特定风格生成回复**  
- **训练风格配置**  

---

## 计划费用对比  
| 功能 | Starter计划 | Pro计划（每月29.90美元） | Business计划（每月69.90美元） |
|------|------------------|--------------------------------------|
| 语音转录 | - | 支持 | 支持 |
| RAG知识库 | - | 支持（最多10份文档） | 支持（无限制） |
| 风格分析 | - | 支持（最多3个配置） | 支持（无限制） |
| AI回复生成 | - | 支持 | 支持 |

---

## 错误代码及含义  
| 状态码 | 含义 |  
|------|---------|-------------------|
| 400 | 请求无效（输入错误或文件格式不支持） |
| 401 | 未经授权（缺少或无效的认证信息） |
| 403 | 该功能仅限Pro计划及以上版本使用 |  
| 404 | 资源未找到（消息、文档或配置文件缺失） |
| 413 | 文件过大（超过100MB限制） |
| 429 | 日使用量达到上限 |  

---

## 相关服务  
- **moltflow**：核心API，支持会话管理、消息发送、群组管理等功能。  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理。  
- **moltflow-leads**：潜在客户识别、流程跟踪、数据导出（CSV/JSON格式）。  
- **moltflow-a2a**：支持代理间加密通信和内容策略管理。  
- **moltflow-reviews**：评论收集与评价管理工具。  
- **moltflow-admin**：平台管理、用户管理及计划配置工具。