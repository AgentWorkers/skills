---
name: moltflow-ai
description: "由人工智能驱动的 WhatsApp 功能：自动回复、语音转录、RAG（检索-聚合-生成）知识库以及样式配置。适用场景：自动回复、语音转录、知识库查询、文档上传、样式设置、学习模式。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** — 专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化WhatsApp消息处理。  
**由于需求量庞大以及近期出现的注册问题，我们特推出顶级商务计划：每月19.90美元，提供无限使用量，仅限限时优惠。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
**也提供免费试用计划。** [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow的AI功能  

MoltFlow具备强大的AI自动化能力：支持语音转录、基于检索式问答（RAG）的知识库、写作风格学习以及智能回复生成。  

## 实际应用场景  

**医疗诊所**：  
“将患者通过WhatsApp发送的语音记录转录为可搜索的文本，方便日后查询。”  

**律师事务所**：  
“将服务协议上传至知识库，让AI能够准确回答客户关于条款和价格的问题。”  

**销售团队**：  
“复制顶尖销售人员的写作风格，让AI回复客户时更具专业性和亲和力（使用表情符号）。”  

**客户服务**：  
“使用常见问题解答文档自动回复客户常见问题，如‘营业时间是什么？’和‘您位于哪里？’。”  

## 使用场景  

- **语音转录**  
- **将音频文件转换为文本**  
- **将文档上传至知识库**  
- **在知识库中搜索信息**  
- **创建或调整写作风格**  
- **生成智能回复**  
- **预览AI生成的回复**  
- **管理知识库内容**  

## 前提条件  

1. **MOLTFLOW_API_KEY**：  
   请从[MoltFlow控制台](https://molt.waiflow.app)的“设置” > “API密钥”中生成。  

2. **需使用Pro计划（每月29.90美元）**：  
   免费计划不支持AI功能。  

3. **基础URL**：`https://apiv2.waiflow.app/api/v2`  
4. **所有AI相关接口均以 `/ai` 为前缀。  

## 所需API密钥权限  

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

使用Whisper AI技术对WhatsApp语音消息进行转录。转录过程通过Celery后台任务异步处理。  

| 方法 | 接口 | 说明 |  
|--------|----------|-------------|  
| POST | `/ai/voice/transcribe` | 提交语音消息进行转录 |  
| GET | `/ai/voice/status/{task_id}` | 查看转录任务状态 |  
| GET | `/ai/messages/{message_id}/transcript` | 获取消息的转录结果 |  

### 提交转录任务  

**POST** `/ai/voice/transcribe`  

**响应代码**：`200 OK`  

### 查看转录状态  

**GET** `/ai/voice/status/{task_id}`  

**状态代码**：`queued`（排队中）、`processing`（处理中）、`completed`（已完成）、`failed`（失败）  

### 获取转录结果  

**GET** `/ai/messages/{message_id}/transcript`  

---

## 基于检索式问答（RAG）的知识库  

构建基于业务数据的可搜索知识库，支持AI生成智能回复。  

| 方法 | 接口 | 说明 |  
|--------|----------|-------------|  
| POST | `/ai/knowledge/ingest` | 上传并索引文档 |  
| POST | `/ai/knowledge/search` | 在文档中搜索信息 |  
| GET | `/ai/knowledge/sources` | 查看所有已索引的文档 |  
| DELETE | `/ai/knowledge/{source_id}` | 删除文档 |  

### 上传文档  

**POST** `/ai/knowledge/ingest`（支持multipart/form-data）  

| 参数 | 类型 | 说明 |  
|-------|------|-------------|  
| `file` | 文件 | PDF或TXT格式文件（最大100MB） |  

**响应代码**：`200 OK`  

**支持的文件类型**：`application/pdf`、`text/plain`（`.pdf`、`.txt`）  

### 在知识库中搜索  

**POST** `/ai/knowledge/search`  

**响应代码**：`200 OK`  

**可选过滤条件**：  

---  

### 查看文档列表  

**GET** `/ai/knowledge/sources`  

**文档状态**：`processing`（处理中）、`indexed`（已索引）、`failed`（失败）  

### 删除文档  

**DELETE** `/ai/knowledge/{source_id}`  
**响应代码**：`204 No Content`  

---

## 写作风格配置  

允许为特定聊天或全局配置写作风格。AI会根据聊天内容自动选择最合适的回复风格。  

| 方法 | 接口 | 说明 |  
|--------|----------|-------------|  
| POST | `/ai/style/train` | 开始构建写作风格 |  
| GET | `/ai/style/status/{task_id}` | 查看构建进度 |  
| GET | `/ai/style/profile` | 获取写作风格信息 |  
| GET | `/ai/style/profiles` | 查看所有风格配置 |  
| DELETE | `/ai/style/profile/{profile_id}` | 删除风格配置 |  

### 构建写作风格  

**POST** `/ai/style/train`  

**必填参数**：  
- `contact_id`（字符串）：可选  
- `session_id`（UUID）：可选  
- `wa_chat_id`（字符串）：可选（用于指定聊天会话）  
- `name`（字符串）：可选（例如：“Sales”、“Support”等）  

**注**：若省略`session_id`和`wa_chat_id`，系统将使用所有聊天记录生成通用风格。  

**响应代码**：`200 OK`  

构建过程为异步进行，可通过相应接口查看进度。  

### 获取写作风格信息  

**GET** `/ai/style/profile?contact_id=5511999999999@c.us`  

**所有风格配置的列表**：  
**GET** `/ai/style/profiles`  

**删除风格配置**：  
**DELETE** `/ai/style/profile/{profile_id}`  
**响应代码**：`204 No Content`  

---

## 智能回复生成  

利用RAG技术和写作风格生成智能回复。  

| 方法 | 接口 | 说明 |  
|--------|----------|-------------|  
| POST | `/ai/generate-reply` | 生成回复建议 |  
| GET | `/ai/preview` | 预览回复内容（不计入使用量） |  

**生成回复**：  
**POST** `/ai/generate-reply`  

**响应代码**：`200 OK`  

**参数说明**：  
- `contact_id`（字符串）：必填，表示联系人的WhatsApp JID  
- `context`（字符串）：必填，用于生成回复的上下文（最多2000个字符）  
- `use_rag`（布尔值）：是否使用知识库内容  
- `apply_style`（布尔值）：是否应用写作风格  
- `profile_id`（UUID）：可选，指定使用的风格配置  
- `session_id`（UUID）：可选，用于确定回复风格  
- `approved`（布尔值）：设置为`true`表示需要审核的回复  

**注意**：若省略`profile_id`且`apply_style`为`true`，API会自动选择最佳回复风格：  
- 首先匹配特定聊天记录，  
- 若未匹配，则根据会话信息选择，  
- 若仍未匹配，则使用全局配置。  

**预览回复**：  
**GET** `/ai/preview?contact_id=5511999999999@c.us&context=What+are+your+hours&use_rag=true&apply_style=true`  

预览格式与`generate-reply`相同，但不计入使用量统计。  

## 安全机制  

MoltFlow的智能回复生成功能包含以下安全措施：  
- **输入验证**：检测并阻止恶意输入  
- **意图验证**：对可疑或高风险意图进行确认  
- **内容过滤**：检查回复内容是否包含个人身份信息（PII）或违反政策的内容  
- **内容策略**：支持自定义安全规则（详见[moltflow-a2a技能文档]  

---

## 示例操作  

- **上传文档到知识库**  
- **使用RAG生成回复**  
- **根据特定风格生成回复**  
- **配置写作风格**  

---

## 计划费用对比  

| 功能 | 免费计划 | Pro计划（每月29.90美元） | 商务计划（每月69.90美元） |  
|--------|-----------------|-----------------|------------|  
| 语音转录 | **无** | **有** | **有** |  
| RAG知识库 | **无** | **有（10份文档）** | **有（无限份文档）** |  
| 写作风格配置 | **无** | **有（3个风格配置）** | **有（无限个风格配置）** |  
| 智能回复生成 | **无** | **有** | **有** |  

---

## 错误代码及含义  

| 状态码 | 含义 |  
|--------|---------|-----------------|-----------------|  
| 400 | 请求无效（输入错误或文件格式不支持） |  
| 401 | 未经授权（缺少或无效的认证信息） |  
| 403 | 功能需Pro计划才能使用 |  
| 404 | 资源未找到（消息、文档或风格配置） |  
| 413 | 文件过大（超过100MB限制） |  
| 429 | 使用频率超出限制 |  

---

## 相关服务  

- **moltflow**：核心API，支持会话管理、消息发送、群组管理等功能  
- **moltflow-outreach**：批量发送消息、定时发送、自定义群组管理  
- **moltflow-leads**：潜在客户检测、任务跟踪、批量操作、CSV/JSON导出  
- **moltflow-a2a**：支持代理间安全通信和内容策略管理  
- **moltflow-reviews**：评论收集与评价管理  
- **moltflow-admin**：平台管理、用户管理、计划配置