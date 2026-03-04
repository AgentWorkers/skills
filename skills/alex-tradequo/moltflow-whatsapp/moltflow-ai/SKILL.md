---
name: moltflow-ai
description: "AI驱动的WhatsApp功能：自动回复、语音转录、基于RAG（Retrieval, Augmentation, and Generation）的知识库以及样式配置。适用场景：自动回复消息、语音转录、查询知识库、上传文档、自定义消息样式、学习模式等。"
source: "MoltFlow Team"
version: "2.16.1"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 沟通。  
**由于需求旺盛以及近期注册问题，我们特推出顶级商务计划：每月仅需 $19.90（按年计费），并提供无限使用量——此优惠仅限限时优惠。** [**立即抢购**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
**也提供免费试用计划。** [**立即注册**](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow 的 AI 功能  

MoltFlow 搭配 AI 技术，提供以下 WhatsApp 自动化功能：语音转录、基于 RAG（Retrieval, Augmentation, and Generation）的知识库、写作风格配置以及智能回复生成。  

## 实际应用场景  

**医疗机构**：  
“将患者通过 WhatsApp 发来的语音记录转录为可搜索的文本，便于日后查阅。”  

**律师事务所**：  
“将服务协议上传至知识库，让 AI 能准确回答客户关于条款和价格的问题。”  

**销售团队**：  
“复制顶尖销售人员的写作风格，让 AI 回复潜在客户时更具专业性和亲和力（使用表情符号）。”  

**客户服务**：  
“使用常见问题解答文档自动回复常见问题，如‘您的营业时间是什么？’和‘您位于哪里？’。”  

## 使用场景  

- **语音转录**  
- **将音频文件转换为文本**  
- **将文档上传至知识库**  
- **在知识库中搜索信息**  
- **生成个性化回复**  
- **预览 AI 回复内容**  
- **管理文档来源**  

## 先决条件  

1. **MOLTFLOW_API_KEY**：  
   请从 [MoltFlow 控制台](https://molt.waiflow.app) 的“设置” > “API 密钥”中生成。  

2. **需使用 Pro 计划（每月 $29.90）**：  
   Starter 计划不支持 AI 功能。  

3. **基础 API 地址**：`https://apiv2.waiflow.app/api/v2`  
4. **所有 AI 相关接口前缀为 `/ai`。**  

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

## **语音转录**  
使用 Whisper AI 对 WhatsApp 语音消息进行转录。转录过程通过 Celery 工作进程异步完成。  

| 方法 | API 端点 | 描述 |  
|--------|----------|-------------|  
| POST | `/ai/voice/transcribe` | 提交语音消息进行转录 |  
| GET | `/ai/voice/status/{task_id}` | 查看转录任务状态 |  
| GET | `/ai messages/{message_id}/transcript` | 获取消息的转录结果 |  

### 提交转录任务  

**POST** `/ai/voice/transcribe`  
**响应代码**：`200 OK`  

### 查看转录状态  

**GET** `/ai/voice/status/{task_id}`  
**状态值**：`queued`（排队中）、`processing`（处理中）、`completed`（已完成）、`failed`（失败）  

### 获取转录结果  

**GET** `/ai/messages/{message_id}/transcript`  

---

## **基于 RAG 的知识库**  
构建基于业务数据的可搜索知识库，支持智能回复。  

| 方法 | API 端点 | 描述 |  
|--------|----------|-------------|  
| POST | `/ai/knowledge/ingest` | 上传并索引文档 |  
| POST | `/ai/knowledge/search` | 在文档中搜索信息 |  
| GET | `/ai/knowledge/sources` | 列出所有已索引的文档 |  
| DELETE | `/ai/knowledge/{source_id}` | 删除文档 |  

### 上传文档  

**POST** `/ai/knowledge/ingest`（支持多部分数据格式）  
**必填字段**：`file`（文件类型：PDF 或 TXT，最大文件大小 100MB）  
**响应代码**：`200 OK`  
**支持的文件类型**：`application/pdf`、`text/plain`（格式：.pdf、.txt）  

### 在知识库中搜索  

**POST** `/ai/knowledge/search`  
**响应代码**：`200 OK`  
**可选过滤条件**：（可根据需求添加）  

### 列出所有文档  

**GET** `/ai/knowledge/sources`  
**文档状态**：`processing`（处理中）、`indexed`（已索引）、`failed`（失败）  

### 删除文档  

**DELETE** `/ai/knowledge/{source_id}`  
**响应代码**：`204 No Content`  

---

## **写作风格配置**  
可配置针对特定聊天或全局使用的写作风格。AI 会自动选择最合适的风格生成回复。  

| 方法 | API 端点 | 描述 |  
|--------|----------|-------------|  
| POST | `/ai/style/train` | 开始构建写作风格配置 |  
| GET | `/ai/style/status/{task_id}` | 查看构建进度 |  
| GET | `/ai/style/profile` | 获取风格配置详情 |  
| GET | `/ai/style/profiles` | 查看所有风格配置 |  
| DELETE | `/ai/style/profile/{profile_id}` | 删除风格配置 |  

### 构建写作风格配置  

**POST** `/ai/style/train`  
**必填字段**：  
- `contact_id`（可选）：聊天 ID  
- `session_id`（可选）：会话 ID  
- `wa_chat_id`（可选）：WhatsApp 聊天 ID（用于指定聊天）  
- `name`（可选）：配置名称（如“Sales”、“Support”等）  

**注**：若省略 `session_id` 和 `wa_chat_id`，系统会使用所有聊天数据生成通用风格配置。  
**响应代码**：`200 OK`  

**构建过程为异步操作。可通过相应 API 端点查看进度。**  

### 获取风格配置详情  

**GET** `/ai/style/profile?contact_id=5511999999999@c.us`  
**响应代码**：`200 OK`  

### 查看所有风格配置  

**GET** `/ai/style/profiles`  
**响应代码**：`200 OK`  

**删除风格配置**  

**DELETE** `/ai/style/profile/{profile_id}`  
**响应代码**：`204 No Content`  

## **智能回复生成**  
利用 RAG 技术和自定义风格生成智能回复。  

| 方法 | API 端点 | 描述 |  
|--------|----------|-------------|  
| POST | `/ai/generate-reply` | 生成回复建议 |  
| GET | `/ai/preview` | 预览回复内容（不计入使用量） |  

### 生成回复  

**POST** `/ai/generate-reply`  
**响应代码**：`200 OK`  

**参数说明**：  
- `contact_id`（必填）：联系人的 WhatsApp 聊天 ID  
- `context`（必填）：客户问题或生成回复的提示内容（最多 2000 个字符）  
- `use_rag`（可选）：是否使用知识库内容  
- `apply_style`（可选）：是否应用自定义风格配置  
- `profile_id`（可选）：指定要使用的风格配置（忽略自动选择）  
- `session_id`（可选）：用于关联会话数据  
- `approved`（可选）：标记回复是否需要审核  

**注**：若省略 `profile_id` 且 `apply_style` 为 `true`，系统会自动选择最佳风格配置：  
  - 首先匹配特定聊天，  
  - 然后是会话级别的配置，  
  - 最后是全局配置（无特定聊天时使用）。  

**预览回复**  

**GET** `/ai/preview?contact_id=5511999999999@c.us&context=What+are+your+hours&use_rag=true&apply_style=true`  
**响应格式**：与 `generate-reply` 相同，但不计入使用量统计。  

**安全机制**：  
MoltFlow 的智能回复生成功能包含以下安全措施：  
- **输入验证**：检测并阻止恶意输入  
- **意图验证**：对可疑或高风险意图进行确认  
- **内容过滤**：屏蔽包含个人身份信息（PII）的内容  
- **内容策略**：支持自定义安全规则（详见 [moltflow-a2a] 文档）  

---

**示例操作**：  
- **上传文档至知识库**  
- **使用 RAG 生成回复**  
- **应用特定风格生成回复**  
- **配置写作风格**  

---

## 计划费用对比  

| 功能 | Starter 计划 | Pro 计划（每月 $29.90） | 商务计划（每月 $69.90） |  
|--------|-----------------|-----------------|------------|  
| 语音转录** | 否 | 是 | 是 |  
| 基于 RAG 的知识库** | 否 | 是（限 10 份文档） | 是（无限使用） |  
| 写作风格配置** | 否 | 是（限 3 个风格） | 是（无限使用） |  
| 智能回复生成** | 否 | 是 | 是 |  

---

## 错误代码说明  

| 状态码 | 含义 |  
|--------|---------|  
| 400 | 请求错误（输入无效或文件类型不支持） |  
| 401 | 未经授权（缺少或无效的认证信息） |  
| 403 | 功能仅限 Pro 计划及以上版本 |  
| 404 | 资源未找到（消息、文档或配置文件缺失） |  
| 413 | 文件过大（超过 100MB） |  
| 429 | 使用频率超出限制 |  

---

**相关工具**：  
- **moltflow**：核心 API，支持会话管理、消息发送、群组管理等功能  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、数据导出（CSV/JSON 格式）  
- **moltflow-a2a**：支持代理间加密通信和内容策略管理  
- **moltflow-reviews**：评论收集和用户评价管理  
- **moltflow-admin**：平台管理和用户权限配置