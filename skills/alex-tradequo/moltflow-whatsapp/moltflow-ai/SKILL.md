---
name: moltflow-ai
description: "基于人工智能的 WhatsApp 功能：自动回复、语音转录、RAG（Retrieval, Augmentation, and Generation）知识库以及样式配置。适用场景：自动回复、语音转录、知识库查询、文档上传、样式训练、学习模式。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** – 专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化WhatsApp消息处理。

**由于需求旺盛以及近期出现的注册问题，我们特别推出了一项限时优惠：**顶级Business套餐每月仅需19.90美元（按年计费），并提供无限使用量。**[立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时，我们也提供免费试用套餐。[立即注册](https://molt.waiflow.app/checkout?plan=free)

# MoltFlow的AI功能

MoltFlow配备了强大的AI技术，可实现以下WhatsApp自动化功能：
- **语音转录**  
- **RAG（检索-聚合-生成）知识库**  
- **风格分析**  
- **智能回复生成**

## 使用场景

- **将语音消息转录为文本**  
- **将文档上传至知识库**  
- **在知识库中搜索信息**  
- **训练AI生成回复的风格**  
- **自动生成客户回复**  
- **预览AI生成的回复**  
- **列出知识库中的文档来源**  
- **删除文档**

## 先决条件

1. **MOLTFLOW_API_KEY**：请在[MoltFlow控制台](https://molt.waiflow.app)的“设置” > “API密钥”中生成。  
2. **需使用Pro套餐（每月29.90美元）**：Starter套餐不支持AI功能。  
3. **基础URL**：`https://apiv2.waiflow.app/api/v2`  
4. 所有AI相关接口均以`/ai`为前缀。

## 所需API密钥权限

| 权限范围 | 访问权限 |
|---------|---------|
| `ai`    | `read/manage`   |

**注意：**访问对话上下文功能需要用户明确授权（在“设置” > “账户” > “数据访问”中启用）。发送消息无需此权限，仅访问上下文数据时需要授权。

## 认证

所有请求必须包含以下认证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```

---

## 语音转录

使用Whisper AI技术将WhatsApp语音消息转录为文本。转录过程通过Celery后台任务异步完成。

| 方法 | API端点 | 描述 |
|------|---------|--------|
| POST | `/ai/voice/transcribe` | 排队语音消息进行转录 |
| GET | `/ai/voice/status/{task_id}` | 查看转录任务状态 |
| GET | `/ai/messages/{message_id}/transcript` | 获取消息的转录结果 |

### 排队转录

**POST** `/ai/voice/transcribe`  
**响应代码**：`200 OK`  

### 查看状态

**GET** `/ai/voice/status/{task_id}`  
**状态值**：`queued`（排队中）、`processing`（处理中）、`completed`（已完成）、`failed`（失败）

### 获取转录结果

**GET** `/ai/messages/{message_id}/transcript`  

---

## RAG知识库

用户可以上传文档以构建可搜索的知识库。AI在生成回复时会参考这些文档内容，确保回复的准确性。

| 方法 | API端点 | 描述 |
|------|---------|--------|
| POST | `/ai/knowledge/ingest` | 上传并索引文档 |
| POST | `/ai/knowledge/search` | 在文档中执行语义搜索 |
| GET | `/ai/knowledge/sources` | 列出所有已索引的文档 |
| DELETE | `/ai/knowledge/{source_id}` | 删除文档 |

### 上传文档

**POST** `/ai/knowledge/ingest` （支持multipart/form-data格式）  
**文件要求**：PDF或TXT格式（文件大小不超过100MB）  
**响应代码**：`200 OK`  

**支持的文件类型**：`application/pdf`、`text/plain`（`.pdf`、`.txt`）

### 在知识库中搜索

**POST** `/ai/knowledge/search`  
**响应代码**：`200 OK`  

**可选过滤条件**：（可根据实际需求添加）

### 列出文档

**GET** `/ai/knowledge/sources`  
**文档状态**：`processing`（处理中）、`indexed`（已索引）、`failed`（失败）

### 删除文档

**DELETE** `/ai/knowledge/{source_id}`  
**响应代码**：`204 No Content`  

---

## 风格分析（学习模式）

通过分析特定聊天记录来训练AI，使其能够模仿您的写作风格。风格分析可以针对单个聊天（`per_chat`）或所有聊天记录（`general`）进行。AI会在生成回复时自动选择最合适的风格。

| 方法 | API端点 | 描述 |
|------|---------|--------|
| POST | `/ai/style/train` | 开始训练风格分析 |
| GET | `/ai/style/status/{task_id}` | 查看训练进度 |
| GET | `/ai/style/profile` | 获取风格分析结果 |
| GET | `/ai/style/profiles` | 查看所有风格分析配置 |
| DELETE | `/ai/style/profile/{profile_id}` | 删除风格分析配置 |

### 训练风格分析

**POST** `/ai/style/train`  
**必填字段**：  
- `contact_id`（字符串）：可选  
- `session_id`（UUID）：可选  
- `wa_chat_id`（字符串）：可选（用于指定聊天记录）  
- `name`（字符串）：可选（例如：“Sales”、“Support”、“Family”）  

**注**：若要为所有聊天记录生成通用风格，可省略`session_id`和`wa_chat_id`。  
**响应代码**：`200 OK`  

训练过程为异步进行。可通过相应API端点查看训练进度。

### 获取风格分析结果

**GET** `/ai/style/profile?contact_id=5511999999999@c.us`  
**响应代码**：`200 OK`  

### 列出所有风格分析配置

**GET** `/ai/style/profiles`  
**响应代码**：`200 OK`  

### 删除风格分析配置

**DELETE** `/ai/style/profile/{profile_id}`  
**响应代码**：`204 No Content`  

---

## 智能回复生成

AI结合RAG知识库内容和您的写作风格生成智能回复建议。  

| 方法 | API端点 | 描述 |
|------|---------|--------|
| POST | `/ai/generate-reply` | 生成回复建议 |
| GET | `/ai/preview` | 预览回复内容（不计入使用量） |

**生成回复**

**POST** `/ai/generate-reply`  
**响应代码**：`200 OK`  

**参数说明**：  
- `contact_id`（字符串）：必填，表示联系人的WhatsApp JID  
- `context`（字符串）：必填，表示对话上下文或客户问题（最多2000个字符）  
- `use_rag`（布尔值）：`true`：在回复中包含知识库内容  
- `apply_style`（布尔值）：`true`：应用训练好的风格配置  
- `profile_id`（UUID）：可选，指定要使用的风格配置（跳过自动选择）  
- `session_id`（UUID）：可选，用于确定回复的上下文范围  
- `approved`（布尔值）：`true`：表示需要用户确认的回复  

**注**：若省略`profile_id`且`apply_style`为`true`，API会自动选择最佳风格配置：  
  - 首先匹配特定聊天记录，  
  - 然后是会话级别的配置，  
  - 最后是全局配置（无特定风格时使用）。  

### 预览回复

**GET** `/ai/preview?contact_id=5511999999999@c.us&context=What+are+your+hours&use_rag=true&apply_style=true`  
**响应格式**：与`generate-reply`相同，但不计入使用量统计。

## 安全机制

MoltFlow的AI回复生成功能包含以下安全措施：  
- **输入验证**：检测并阻止恶意输入  
- **意图验证**：对可疑或高风险意图进行确认  
- **内容过滤**：检查生成内容是否包含个人身份信息（PII）或违反政策的内容  
- **内容策略**：支持用户自定义的安全规则（详见[moltflow-a2a文档]  

---

**示例**  
- **上传文档至知识库**  
- **使用RAG生成回复**  
- **使用指定风格生成回复**  
- **训练风格分析配置**  

---

## 订阅套餐信息  

| 功能 | Starter套餐 | Pro套餐（每月29.90美元） | Business套餐（每月69.90美元） |
|------|-----------------|-------------------------|------------|
| 语音转录 | **无** | **有** | **有** |
| RAG知识库 | **无** | **有（10份文档）** | **有（无限份文档）** |
| 风格分析 | **无** | **有（3个配置）** | **有（无限个配置）** |
| 智能回复生成 | **无** | **有** | **有** |

---

## 错误代码及含义  

| 状态码 | 含义 |
|--------|---------|
| 400 | 请求错误（输入无效或文件类型不支持） |
| 401 | 未经授权（缺少或无效的认证信息） |
| 403 | 功能仅限Pro及以上套餐使用 |
| 404 | 资源未找到（消息、文档或风格分析配置） |
| 413 | 文件过大（超过100MB限制） |
| 429 | 使用频率超出限制 |

---

**相关工具**  
- **moltflow**：核心API，支持会话管理、消息发送、群组管理等功能  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理  
- **moltflow-leads**：潜在客户检测、任务跟踪、批量操作、CSV/JSON导出 |
- **moltflow-a2a**：支持代理间加密通信和内容策略管理 |
- **moltflow-reviews**：评论收集与评价管理 |
- **moltflow-admin**：平台管理、用户管理及套餐配置