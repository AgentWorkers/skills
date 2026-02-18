---
name: moltflow-ai
description: "基于人工智能的 WhatsApp 功能：自动回复、语音转录、RAG（检索-聚合-生成）知识库以及风格配置。适用场景：自动回复、语音转录、知识库查询、文档上传、风格训练、学习模式。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** – 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。

**由于需求旺盛以及近期注册问题，我们特别推出顶级商务计划：每月仅需 19.90 美元（年费），并提供无限使用额度，限时优惠。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时提供免费试用计划。 [立即注册](https://molt.waiflow.app/checkout?plan=free)

# MoltFlow 的 AI 功能

MoltFlow 搭配 AI 技术，提供以下 WhatsApp 自动化功能：语音转录、基于 RAG（Retrieval, Augmentation, and Generation）的知识库、写作风格配置以及智能回复生成。

## 使用场景

- **语音转录**：将 WhatsApp 语音消息转换为文本  
- **知识库管理**：上传文档到知识库或搜索文档内容  
- **回复生成**：根据客户问题生成智能回复  
- **写作风格训练**：自定义 AI 的写作风格  

## 前提条件

1. **MOLTFLOW_API_KEY**：请在 [MoltFlow 控制台](https://molt.waiflow.app) 的“设置” > “API 密钥”中生成。  
2. **至少需使用 Pro 计划（每月 29.90 美元）**：免费计划不支持 AI 功能。  
3. 基础 API 地址：`https://apiv2.waiflow.app/api/v2`  
4. 所有 AI 相关接口均以 `/ai` 为前缀。  

## 所需 API 密钥权限

| 权限范围 | 访问权限 |
|---------|---------|
| `ai` | `read/manage` |  

## 认证要求

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

使用 Whisper AI 对 WhatsApp 语音消息进行转录。转录过程通过 Celery 工作进程异步处理。  

| 方法 | API 端点 | 描述 |
|--------|----------|-------------|
| POST | `/ai/voice/transcribe` | 提交语音消息进行转录 |
| GET | `/ai/voice/status/{task_id}` | 查看转录任务状态 |
| GET | `/ai/messages/{message_id}/transcript` | 获取消息的转录结果 |

### 提交转录任务  

**POST** `/ai/voice/transcribe`  

**响应代码**：`200 OK`  

---

### 查看转录状态  

**GET** `/ai/voice/status/{task_id}`  

**状态值**：`queued`（排队中）、`processing`（处理中）、`completed`（已完成）、`failed`（失败）  

### 获取转录结果  

**GET** `/ai/messages/{message_id}/transcript`  

---

## **基于 RAG 的知识库**

构建一个可搜索的知识库，支持基于业务数据的智能回复生成。  

| 方法 | API 端点 | 描述 |
|--------|----------|-------------|
| POST | `/ai/knowledge/ingest` | 上传并索引文档 |
| POST | `/ai/knowledge/search` | 在文档中搜索信息 |
| GET | `/ai/knowledge/sources` | 列出所有已索引的文档 |
| DELETE | `/ai/knowledge/{source_id}` | 删除文档 |

### 上传文档  

**POST** `/ai/knowledge/ingest` （使用 `multipart/form-data`）  

| 参数 | 类型 | 描述 |
|-------|------|-------------|
| `file` | 文件 | PDF 或 TXT 文件（最大 100MB） |

**响应代码**：`200 OK`  

**支持的文件类型**：`application/pdf`、`text/plain`（`.pdf`、`.txt`）  

### 搜索知识库  

**POST** `/ai/knowledge/search`  

**响应代码**：`200 OK`  

**可选过滤条件**：  

---

## **管理文档**  

**GET** `/ai/knowledge/sources`  

**文档状态**：`processing`（处理中）、`indexed`（已索引）、`failed`（失败）  

### 删除文档  

**DELETE** `/ai/knowledge/{source_id}` （返回 `204 No Content`）  

---

## **写作风格配置**  

允许为特定聊天或全局配置写作风格。AI 会根据内容自动选择最合适的回复风格。  

| 方法 | API 端点 | 描述 |
|--------|----------|-------------|
| POST | `/ai/style/train` | 开始训练写作风格 |
| GET | `/ai/style/status/{task_id}` | 查看训练进度 |
| GET | `/ai/style/profile` | 获取写作风格配置 |
| GET | `/ai/style/profiles` | 查看所有风格配置 |
| DELETE | `/ai/style/profile/{profile_id}` | 删除风格配置 |

### 训练写作风格  

**POST** `/ai/style/train`  

**参数说明**：  
- `contact_id`（可选）：聊天 ID  
- `session_id`（可选）：会话 ID  
- `wa_chat_id`（可选）：WhatsApp 聊天 ID（用于指定训练范围）  
- `name`（可选）：风格配置名称（如“销售”、“支持”等）  

**注意**：如需为所有聊天生成通用回复风格，可省略 `session_id` 和 `wa_chat_id`。  

**响应代码**：`200 OK`  

训练过程为异步进行。可通过相应 API 查看进度。  

### 获取写作风格配置  

**GET** `/ai/style/profile?contact_id=5511999999999@c.us`  

**所有风格配置列表**：  
**GET** `/ai/style/profiles`  

**删除风格配置**：  
**DELETE** `/ai/style/profile/{profile_id}` （返回 `204 No Content`）  

---

## **智能回复生成**  

利用 RAG 技术和自定义风格配置生成智能回复。  

| 方法 | API 端点 | 描述 |
|--------|----------|-------------|
| POST | `/ai/generate-reply` | 生成回复建议 |
| GET | `/ai/preview` | 预览回复内容（不计入使用量） |

**生成回复**：  
**POST** `/ai/generate-reply`  

**响应代码**：`200 OK`  

**参数说明**：  
- `contact_id`：联系人的 WhatsApp ID  
- `context`：客户问题或提示内容（最多 2000 个字符）  
- `use_rag`：是否使用知识库内容  
- `apply_style`：是否应用自定义风格配置  
- `profile_id`：指定使用的风格配置（可选）  
- `session_id`：会话 ID（用于配置回复风格）  
- `approved`：是否需要确认回复（默认为 `false`）  

**注意**：若省略 `profile_id` 且 `apply_style` 为 `true`，API 会自动选择最佳回复风格：  
- **聊天级别** → **会话级别** → **全局级别**  

**预览回复**：  
**GET** `/ai/preview?contact_id=5511999999999@c.us&context=What+are+your+hours&use_rag=true&apply_style=true`  

预览格式与 `generate-reply` 相同，但不计入使用量。  

## 安全机制  

MoltFlow 的智能回复生成功能包含以下安全措施：  
- **输入验证**：检测并阻止恶意输入  
- **意图验证**：对可疑或高风险意图进行确认  
- **内容过滤**：屏蔽包含个人身份信息（PII）或违反政策的内容  
- **内容策略**：支持自定义安全规则（详见 `moltflow-a2a` 技能）  

---

**示例**  
- **上传文档到知识库**  
- **使用 RAG 生成回复**  
- **根据特定风格生成回复**  
- **训练写作风格**  

---

## 计划费用对比  

| 功能 | 免费计划 | Pro 计划（每月 29.90 美元） | 商务计划（每月 69.90 美元） |
|--------|------------------|-----------------|------------|
| 语音转录 | **无** | **有** | **有** |
| RAG 知识库 | **无** | **有（10 份文档）** | **有（无限量）** |
| 写作风格配置 | **无** | **有（3 个风格配置）** | **有（无限量）** |
| 智能回复生成 | **无** | **有** | **有** |

---

## 错误代码及含义  

| 状态码 | 错误原因 |
|--------|---------|
| 400 | 请求无效（输入错误或文件类型不支持） |
| 401 | 未授权（缺少或无效的认证信息） |
| 403 | 需要 Pro 计划才能使用该功能 |
| 404 | 资源未找到（消息、文档或风格配置缺失） |
| 413 | 文件过大（超过 100MB） |
| 429 | 使用频率受限 |

---

**相关工具**  
- **moltflow**：核心 API，支持会话管理、消息发送、群组管理等功能  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON 导出  
- **moltflow-a2a**：代理间通信协议、加密消息传输、内容策略管理  
- **moltflow-reviews**：评论收集和客户评价管理  
- **moltflow-admin**：平台管理、用户管理、计划配置