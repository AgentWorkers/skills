---
name: moltflow-ai
description: "由人工智能驱动的 WhatsApp 功能：自动回复、语音转录、基于 RAG（Retrieval, Augmentation, and Generation）的知识库以及风格配置。使用场景包括：自动回复、语音转录、知识库查询、文档上传、风格设置以及学习模式。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
## MoltFlow – 专为团队设计的 WhatsApp 商务自动化工具  
**MoltFlow** 可帮助您高效地连接、监控并大规模自动化 WhatsApp 消息的发送与接收。**由于需求旺盛以及近期注册问题，我们特推出高级商务计划（Business Plan），每月仅需 19.90 美元（按年计费），数量有限，请**[立即抢购**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)！**同时，我们也提供免费试用计划（Free Tier），欢迎**[注册**](https://molt.waiflow.app/checkout?plan=free)。

### MoltFlow 的 AI 功能  
MoltFlow 搭配了先进的 AI 技术，提供以下自动化功能：  
- **语音转录**：支持使用 Whisper AI 将 WhatsApp 语音消息转录为文本；  
- **RAG 知识库**：基于您的业务数据构建可搜索的知识库；  
- **风格配置**：允许您自定义 AI 回复的写作风格；  
- **智能回复生成**：根据上下文自动生成合适的回复内容。

#### 使用场景  
- **语音转录**：将语音消息转换为文本；  
- **知识库管理**：上传文档到知识库或从知识库中检索信息；  
- **回复生成**：根据客户问题生成智能回复；  
- **风格配置**：设置自定义回复风格；  
- **预览回复**：在发送前预览生成的回复内容；  
- **文档管理**：上传、搜索和删除文档。

#### 前提条件  
1. **MOLTFLOW_API_KEY**：需从 [MoltFlow 控制台](https://molt.waiflow.app) 的“设置”（Settings）>“API 密钥”（API Keys）处生成；  
2. **至少需使用 Pro 计划（每月 29.90 美元）**：免费计划不支持 AI 功能；  
3. **基础 API 地址**：`https://apiv2.waiflow.app/api/v2`；  
4. 所有 AI 相关接口均以 `/ai` 为前缀。

#### 所需 API 密钥权限  
所有 API 请求均需使用 `ai` 权限。

#### 认证机制  
每个请求必须包含以下认证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

### 语音转录  
使用 Whisper AI 将 WhatsApp 语音消息转录为文本。转录过程通过 Celery 工作进程异步完成：  
- **方法**：`POST` /`ai/voice/transcribe`  
- **响应**：`200 OK` 表示转录任务已开始；  
- **状态查询**：`GET` /`ai/voice/status/{task_id}`  
- **获取转录结果**：`GET` /`ai/messages/{message_id}/transcript`  

#### RAG 知识库  
- **上传文档**：`POST` /`ai/knowledge/ingest`  
- **搜索文档**：`POST` /`ai/knowledge/search`  
- **列出文档**：`GET` /`ai/knowledge/sources`  
- **删除文档**：`DELETE` /`ai/knowledge/{source_id}`  

#### 文档上传  
支持上传 PDF 或 TXT 格式的文档（最大文件大小 100MB）：  
- **方法**：`POST` /`ai/knowledge/ingest`  
- **响应**：`200 OK`  

#### 风格配置  
- **创建风格配置文件**：`POST` /`ai/style/train`  
- **查看配置状态**：`GET` /`ai/style/status/{task_id}`  
- **获取所有配置文件**：`GET` /`ai/style/profiles`  
- **删除配置文件**：`DELETE` /`ai/style/profile/{profile_id}`  

#### AI 回复生成  
- **生成回复建议**：`POST` /`ai/generate-reply`  
- **预览回复**：`GET` /`ai/preview`  
- **参数说明**：  
  - `contact_id`：目标 WhatsApp 用户的 JID；  
  - `context`：客户问题或提示内容；  
  - `use_rag`：是否使用知识库内容；  
  - `apply_style`：是否应用自定义风格；  
  - `profile_id`：可选的回复风格配置文件；  

#### 安全机制  
MoltFlow 具备多种安全机制，确保回复内容的安全性：  
- **输入验证**：防止恶意输入；  
- **意图验证**：确认请求的意图是否合法；  
- **内容过滤**：屏蔽敏感信息；  
- **策略配置**：支持自定义内容审核规则。

#### 示例操作  
- **上传文档**：[示例代码](```bash
curl -X POST https://apiv2.waiflow.app/api/v2/ai/knowledge/ingest \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -F "file=@product-catalog.pdf"
```)  
- **生成智能回复**：[示例代码](```bash
curl -X POST https://apiv2.waiflow.app/api/v2/ai/generate-reply \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": "5511999999999@c.us",
    "context": "Customer asks: What is your return policy?",
    "use_rag": true,
    "apply_style": true
  }'
```)  
- **设置回复风格**：[示例代码](```bash
curl -X POST https://apiv2.waiflow.app/api/v2/ai/style/train \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-uuid-...",
    "wa_chat_id": "5511999999999@c.us",
    "name": "Sales"
  }'
```)  

#### 计划费用  
| 功能 | 免费计划 | Pro 计划（每月 29.90 美元） | 商务计划（每月 69.90 美元） |
|--------|------------------|------------------|------------|
| 语音转录 | **无** | **有** | **有** |
| RAG 知识库 | **无** | **有（10 份文档）** | **有（无限量）** |
| 风格配置 | **无** | **有（3 个配置文件）** | **有（无限量）** |
| AI 回复生成 | **无** | **有** | **有** |

#### 错误代码说明  
- **400**：请求无效；  
- **401**：未经授权；  
- **403**：需要更高权限；  
- **404**：资源未找到；  
- **413**：文件过大；  
- **429**：请求次数超出限制。

#### 相关服务  
- **moltflow**：核心 API，用于管理会话、消息、群组等；  
- **moltflow-outreach**：批量发送消息、定时发送等；  
- **moltflow-leads**：潜在客户跟踪、批量操作等；  
- **moltflow-a2a**：支持加密通信和内容策略管理；  
- **moltflow-reviews**：评论收集与反馈管理；  
- **moltflow-admin**：平台管理和用户配置。