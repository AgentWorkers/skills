---
name: moltflow-ai
description: "由人工智能驱动的 WhatsApp 功能：自动回复、语音转录、基于 RAG（Retrieval, Augmentation, and Generation）的知识库以及风格配置。适用场景：自动回复、语音转录、知识库查询、文档上传、风格设置、学习模式。"
source: "MoltFlow Team"
version: "2.15.1"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** — 专为团队打造的 WhatsApp 商务自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。  
**由于需求旺盛以及近期出现的注册问题，我们特推出高级商务计划，提供无限使用量，每月仅需 19.90 美元（按年计费），限时优惠。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
**也有免费试用计划可供选择。** [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow 的 AI 功能  

MoltFlow 搭配 AI 技术，提供以下 WhatsApp 自动化功能：语音转录、基于 RAG（Retrieval, Augmentation, Generation）的知识库、写作风格学习以及智能回复生成。  

## 实际应用场景  

**医疗机构**：  
“将患者通过 WhatsApp 发送的语音记录转录为可搜索的文本，方便日后查阅。”  

**律师事务所**：  
“将服务协议上传至知识库，让 AI 能够准确回答客户关于条款和价格的问题。”  

**销售团队**：  
“复制顶尖销售人员的写作风格，让 AI 回复潜在客户时更具专业性和亲和力（使用表情符号）。”  

**客户服务**：  
“使用常见问题解答文档，自动回复客户常见的问题，如‘您的工作时间是什么？’和‘您位于哪里？’。”  

## 使用场景  

- **语音转录**：将语音消息转换为文本  
- **知识库管理**：将文档上传至知识库  
- **内容搜索**：在知识库中查找信息  
- **写作风格配置**：创建或调整 AI 的写作风格  
- **智能回复**：自动生成合适的回复  
- **回复预览**：查看 AI 生成的回复内容  
- **文档管理**：列出所有可用的知识资源  

## 先决条件  

1. **MOLTFLOW_API_KEY**：需在 [MoltFlow 控制台](https://molt.waiflow.app) 的 “设置” > “API 密钥” 中生成。  
2. **至少需使用 Pro 计划（每月 29.90 美元）**；Starter 计划不支持 AI 功能。  
3. 基础 API 地址：`https://apiv2.waiflow.app/api/v2`  
4. 所有 AI 相关接口前缀均为 `/ai`  

## 所需 API 密钥权限  

| 权限范围 | 访问内容 |  
|---------|---------|  
| `ai` | `读取/管理` |  

## 认证要求  

每个请求都必须包含以下认证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

---

## 语音转录  

使用 Whisper AI 对 WhatsApp 语音消息进行转录。转录过程通过 Celery 工作进程异步完成。  

| 方法 | API 端点 | 描述 |  
|--------|----------|-------------|  
| POST | `/ai/voice/transcribe` | 排队语音消息进行转录 |  
| GET | `/ai/voice/status/{task_id}` | 查看转录任务状态 |  
| GET | `/ai/messages/{message_id}/transcript` | 获取消息的转录结果 |  

### 排队转录任务  

**POST** `/ai/voice/transcribe`  
**响应代码**：`200 OK`  

### 查看转录状态  

**GET** `/ai/voice/status/{task_id}`  
**状态值**：`queued`（排队中）、`processing`（处理中）、`completed`（已完成）、`failed`（失败）  

### 获取转录结果  

**GET** `/ai/messages/{message_id}/transcript`  

---

## 基于 RAG 的知识库  

构建一个可搜索的知识库，帮助 AI 生成更准确的回复。  

| 方法 | API 端点 | 描述 |  
|--------|----------|-------------|  
| POST | `/ai/knowledge/ingest` | 上传并索引文档 |  
| POST | `/ai/knowledge/search` | 在文档中进行语义搜索 |  
| GET | `/ai/knowledge/sources` | 列出所有已索引的文档 |  
| DELETE | `/ai/knowledge/{source_id}` | 删除文档 |  

### 上传文档  

**POST** `/ai/knowledge/ingest`（支持 `multipart/form-data`）  
**文件类型**：`application/pdf` 或 `text/plain`（文件大小不超过 100MB）  
**响应代码**：`200 OK`  

**支持的文件类型**：`.pdf`、`.txt`  

### 搜索知识库  

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

## 写作风格配置  

可以针对特定聊天或全局配置 AI 的写作风格。AI 会自动选择最合适的风格生成回复。  

| 方法 | API 端点 | 描述 |  
|--------|----------|-------------|  
| POST | `/ai/style/train` | 开始构建写作风格 |  
| GET | `/ai/style/status/{task_id}` | 查看构建进度 |  
| GET | `/ai/style/profile` | 获取写作风格配置 |  
| GET | `/ai/style/profiles` | 查看所有风格配置 |  
| DELETE | `/ai/style/profile/{profile_id}` | 删除风格配置 |  

**构建写作风格**  

**POST** `/ai/style/train`  
**必填字段**：  
- `contact_id`（可选）：聊天 ID  
- `session_id`（可选）：会话 ID  
- `wa_chat_id`（可选）：WhatsApp 聊天 ID（用于指定聊天）  
- `name`（可选）：风格配置名称（如“销售”、“客服”等）  

**注意**：若省略 `session_id` 和 `wa_chat_id`，系统会使用所有聊天数据生成通用风格配置。  
**响应代码**：`200 OK`  

构建过程为异步操作，可通过相应 API 端点查看进度。  

### 获取写作风格配置  

**GET** `/ai/style/profile?contact_id=5511999999999@c.us`  
**响应代码**：`200 OK`  

**查看所有风格配置**  

**GET** `/ai/style/profiles`  
**响应代码**：`200 OK`  

**删除风格配置**  

**DELETE** `/ai/style/profile/{profile_id}`  
**响应代码**：`204 No Content`  

## 智能回复生成  

利用 RAG 技术和配置的风格生成智能回复。  

| 方法 | API 端点 | 描述 |  
|--------|----------|-------------|  
| POST | `/ai/generate-reply` | 生成回复建议 |  
| GET | `/ai/preview` | 预览生成的回复（不计入使用量） |  

**生成回复**  

**POST** `/ai/generate-reply`  
**响应代码**：`200 OK`  

**参数说明**：  
- `contact_id`：联系人的 WhatsApp 聊天 ID  
- `context`：客户问题或用于生成回复的提示（最多 2000 个字符）  
- `use_rag`：是否使用知识库中的信息  
- `apply_style`：是否应用写作风格配置  
- `profile_id`：可选的特定风格配置 ID  
- `session_id`：会话 ID（用于确定使用哪种风格）  
- `approved`：是否需要用户确认回复内容  

**注意**：若省略 `profile_id` 且 `apply_style` 为 `true`，API 会自动选择最佳风格：  
- 首先匹配特定聊天，其次使用会话级别配置，最后使用全局配置（无风格配置时使用默认风格）。  

**预览回复**  

**GET** `/ai/preview?contact_id=5511999999999@c.us&context=What+are+your+hours&use_rag=true&apply_style=true`  
**响应格式**：与 `generate-reply` 相同，但不计入使用量统计。  

## 安全机制  

MoltFlow 的智能回复生成功能包含以下安全措施：  
- **输入验证**：检测并阻止恶意输入  
- **意图验证**：对可疑或高风险意图进行确认  
- **内容过滤**：检查生成的回复是否包含个人身份信息（PII）或违反政策的内容  
- **内容策略**：支持自定义安全规则（详见 `moltflow-a2a` 技能）  

---

**示例**  
- **上传文档至知识库**  
- **使用 RAG 生成回复**  
- **根据特定风格生成回复**  
- **配置写作风格**  

---

## 计划费用对比  

| 功能 | Starter 计划 | Pro 计划（每月 29.90 美元） | 商务计划（每月 69.90 美元） |  
|--------|-----------------|-----------------|------------|  
| 语音转录 | **无** | **有** | **有** |  
| 基于 RAG 的知识库 | **无** | **有（10 份文档）** | **有（无限量）** |  
| 写作风格配置 | **无** | **有（3 个风格配置）** | **有（无限量）** |  
| 智能回复生成 | **无** | **有** | **有** |  

---

## 错误代码及含义  

| 状态码 | 含义 |  
|--------|---------|----------------|----------------|