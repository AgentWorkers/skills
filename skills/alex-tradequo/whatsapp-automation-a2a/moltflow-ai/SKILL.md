---
name: moltflow-ai
description: "基于人工智能的 WhatsApp 功能：自动回复、语音转录、RAG（Retrieval, Augmentation, and Generation）知识库以及风格配置。使用场景包括：自动回复、语音转录、知识库查询、文档上传、风格训练以及学习模式。"
source: "MoltFlow Team"
version: "2.1.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

## MoltFlow – 为团队打造的 WhatsApp 商务自动化工具  
**MoltFlow** 可帮助您高效地连接、监控并自动化 WhatsApp 沟通。**由于需求旺盛以及近期注册问题，我们特别推出了一项限时优惠：**顶级商务计划（Business Plan）每月仅需 $19.90（按年计费），并提供无限使用量。**[立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)！**同时，我们还提供免费试用计划。**[立即注册](https://molt.waiflow.app/checkout?plan=free)。

### MoltFlow 的 AI 功能  
MoltFlow 搭配了先进的 AI 技术，实现了以下 WhatsApp 自动化功能：  
- **语音转录**：可将 WhatsApp 语音消息转换为文本；  
- **RAG 知识库**：支持上传文档并构建可搜索的知识库，AI 会利用这些数据生成准确的回复；  
- **风格配置**：允许您训练 AI 以匹配您的写作风格；  
- **智能回复**：根据对话历史和知识库内容生成智能回复。

#### 使用场景  
- **语音转录**：将语音消息转换为文本；  
- **文档上传**：将文件上传至知识库；  
- **知识库搜索**：在知识库中查找信息；  
- **风格训练**：自定义回复生成风格；  
- **智能回复**：自动回复客户；  
- **回复预览**：查看生成的回复内容；  
- **文档管理**：列出所有索引的文档或删除特定文档。

#### 前提条件  
1. **MOLTFLOW_API_KEY**：需从 [MoltFlow 控制台](https://molt.waiflow.app) 的“设置”>“API 密钥”中生成；  
2. **至少使用 Pro 计划（每月 $29.90）**：免费计划不支持 AI 功能；  
3. **基础 API 地址**：`https://apiv2.waiflow.app/api/v2`；  
4. **所有 AI 相关接口前缀为 `/ai`。

#### 所需 API 密钥权限  
- **`ai`：`read/manage`：用于读取和管理相关数据。

#### 访问聊天记录  
读取聊天记录需要用户明确授权（在“设置”>“账户”>“数据访问”中启用）。  
**注意：**发送消息无需授权，仅读取聊天记录需要授权。

#### 认证  
所有请求必须包含以下认证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

---

### 语音转录  
使用 Whisper AI 将 WhatsApp 语音消息转录为文本。转录过程通过 Celery 工作进程异步完成：  
- **方法**：`POST` /`ai/voice/transcribe`  
- **接口**：`/ai/voice/transcribe`  
- **描述**：提交语音消息进行转录。  

#### 查看转录状态  
- **方法**：`GET` /`ai/voice/status/{task_id}`  
- **接口**：`/ai/voice/status/{task_id}`  
- **描述**：查询转录任务的状态。  

#### 查看文档转录结果  
- **方法**：`GET` /`ai/messages/{message_id}/transcript`  
- **接口**：`/ai/messages/{message_id}/transcript`  
- **描述**：获取指定消息的转录文本。

---

### RAG 知识库  
- **上传文档**：上传文档以构建可搜索的知识库。AI 会利用这些文档生成更准确的回复。  
- **方法**：`POST` /`ai/knowledge/ingest`  
- **接口**：`/ai/knowledge/ingest`  
- **描述**：上传并索引文档。  
- **方法**：`POST` /`ai/knowledge/search`  
- **接口**：`/ai/knowledge/search`  
- **描述**：在知识库中搜索文档。  
- **方法**：`DELETE` /`ai/knowledge/{source_id}`  
- **接口**：`/ai/knowledge/{source_id}`  
- **描述**：删除文档。  

#### 支持的文件类型：`application/pdf`、`text/plain`（`.pdf`、`.txt`）。

---

### 风格配置  
- **训练 AI**：通过分析特定聊天记录来训练 AI 以匹配您的写作风格。  
- **方法**：`POST` /`ai/style/train`  
- **接口**：`/ai/style/train`  
- **描述**：开始训练风格配置。  
- **方法**：`GET` /`ai/style/status/{task_id}`  
- **接口**：`/ai/style/status/{task_id}`  
- **描述**：查询训练进度。  
- **方法**：`GET` /`ai/style/profile`  
- **接口**：`/ai/style/profile`  
- **描述**：获取或删除风格配置。  
- **方法**：`DELETE` /`ai/style/profile/{profile_id}`  
- **描述**：删除风格配置。  

#### 生成智能回复  
- **方法**：`POST` /`ai/generate-reply`  
- **接口**：`/ai/generate-reply`  
- **描述**：生成智能回复建议。  
- **方法**：`GET` /`ai/preview`  
- **接口**：`/ai/preview`  
- **描述**：预览生成的回复内容（不计入使用量）。  

#### 安全机制  
MoltFlow 具备多项安全机制，确保回复内容的安全性：  
- **输入验证**：检测并阻止恶意输入；  
- **意图验证**：对可疑或高风险意图进行确认；  
- **内容过滤**：屏蔽包含个人身份信息（PII）的内容；  
- **内容策略**：支持用户自定义的规则（详见 [moltflow-a2a] 文档）。

---

### 示例操作  
- **上传文档**：[示例代码](___CODE_BLOCK_17_)  
- **生成智能回复**：[示例代码](___CODE_BLOCK_18_)  
- **训练风格配置**：[示例代码](___CODE_BLOCK_20_)  

---

### 计划费用  
| 功能 | 免费计划 | Pro 计划（每月 $29.90） | 商务计划（每月 $69.90） |
|--------|-----------------|-----------------|-------------|
| 语音转录 | **无** | **有** | **有** |
| RAG 知识库 | **无** | **有（10 份文档）** | **有（无限量）** |
| 风格配置 | **无** | **有（3 个配置）** | **有（无限量）** |
| 智能回复 | **无** | **有** | **有** |

---

### 错误代码及含义  
- **400**：请求无效（输入错误或文件格式不支持）；  
- **401**：未经授权（缺少或无效的认证信息）；  
- **403**：需要 Pro 计划才能使用该功能；  
- **404**：资源未找到（消息、文档或配置文件缺失）；  
- **413**：文件过大（超过 100MB）；  
- **429**：请求频率超出限制。

---

### 相关工具  
- **moltflow**：核心 API，用于管理会话、消息、群组等；  
- **moltflow-outreach**：批量发送消息、安排发送时间、管理自定义群组；  
- **moltflow-leads**：检测潜在客户、跟踪处理流程、导出数据（CSV/JSON）；  
- **moltflow-a2a**：支持代理间安全通信；  
- **moltflow-reviews**：管理用户评价和反馈；  
- **moltflow-admin**：平台管理、用户管理及计划配置。