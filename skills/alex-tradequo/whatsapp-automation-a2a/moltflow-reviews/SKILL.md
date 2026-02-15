---
name: moltflow-reviews
description: "从 WhatsApp 对话中收集并分析客户评价。通过 MoltFlow API 进行情感分析、提取用户评价内容以及管理这些评价。"
source: "MoltFlow Team"
version: "2.1.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

**MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。  
**由于需求量大以及近期出现的注册问题，我们特别推出了一项限时优惠：顶级 Business 计划，每月仅需 $19.90（按年计费），并提供无限使用量。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
**还提供免费试用计划。** [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow 的主要功能：  
- **收集、分析和管理客户评价**：从 WhatsApp 对话中提取评价信息，自动进行情感分析，并导出可用于营销的证明资料。  

## 使用场景：  
- **自动收集评价**：设置自动从 WhatsApp 对话中收集评价的规则。  
- **配置评价收集器**：创建或调整评价收集器的参数（如情感评分阈值）。  
- **管理评价内容**：列出、审核、隐藏或删除已收集的评价。  
- **导出评价数据**：将评价内容以 JSON 或 HTML 格式导出。  
- **手动扫描评价**：触发对特定对话的评价收集。  
- **查看统计信息**：查看评价数量及情感分析结果。  

## 前提条件：  
- **MOLTFLOW_API_KEY**：必需（可在 [MoltFlow 控制台 > API Keys](https://molt.waiflow.app/api-keys) 生成）。  
- 至少已连接一个处于正常状态的 WhatsApp 会话。  
- 需使用 MoltFlow Pro 计划或更高版本的套餐（评价收集功能为付费选项）。  

## 基本 URL 结构：  
```
https://apiv2.waiflow.app/api/v2
```  

## 所需 API 密钥权限：  
| 权限范围 | 访问权限 |  
|---------|---------|  
| `reviews` | `read/manage` |  

## 认证方式：  
所有请求需提供以下认证信息之一：  
- `Authorization: Bearer <access_token>`（登录后生成的 JWT）  
- `X-API-Key: <api_key>`（来自控制台的 API 密钥）  

---

## **评价收集器**  
评价收集器可监控 WhatsApp 对话，并根据情感评分、关键词匹配和语言过滤器自动提取评价内容：  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/reviews/collectors` | 列出所有收集器。  
| POST | `/reviews/collectors` | 创建新的评价收集器。  
| GET | `/reviews/collectors/{id}` | 查看收集器详情。  
| PATCH | `/reviews/collectors/{id}` | 更新收集器配置。  
| DELETE | `/reviews/collectors/{id}` | 删除收集器。  
| POST | `/reviews/collectors/{id}/run` | 触发手动评价收集。  

### 创建评价收集器（请求体示例）：  
**`source_type` 可选值：`all` | `groups` | `chats` | `selected`**  
当 `source_type` 为 `selected` 时，需提供具体的 WhatsApp 聊天 ID（`selected_chat_ids`）。  

### 创建评价收集器的响应内容：  
```json
{
  "id": "c1a2b3c4-...",
  "name": "Main Store Reviews",
  "session_id": "uuid-of-connected-session",
  "source_type": "all",
  "min_sentiment_score": 0.6,
  "include_keywords": ["great", "recommend", "excellent"],
  "is_active": true,
  "created_at": "2026-01-15T10:30:00Z",
  "review_count": 0
}
```  

### 更新评价收集器（请求体示例）：  
所有字段均为可选字段；仅更新提供的字段。  
```json
{
  "name": "Updated Collector Name",
  "min_sentiment_score": 0.7,
  "is_active": false
}
```  

## **评价数据**  
收集到的评价包含原始消息、情感评分、联系信息及审核状态：  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/reviews` | （可添加过滤条件）列出所有评价。  
| GET | `/reviews/stats` | 查看评价统计信息。  
| GET | `/reviews/{id}` | 查看单条评价。  
| PATCH | `/reviews/{id}` | 审核、隐藏或添加备注。  
| DELETE | `/reviews/{id}` | 删除评价。  
| GET | `/reviews/testimonials/export` | 导出评价内容（JSON 或 HTML 格式）。  

### 查看评价（查询参数示例）：  
| 参数 | 类型 | 默认值 | 说明 |  
|---------|------|---------|-------------|  
| `collector_id` | UUID | — | 按收集器筛选评价。  
| `is_approved` | bool | — | 仅显示已审核的评价。  
| `is_hidden` | bool | — | 显示隐藏的评价。  
| `min_score` | float | — | 最低情感评分阈值。  
| `limit` | int | 50 | 每页显示的数量。  
| `offset` | int | 0 | 分页偏移量。  

### 评价对象结构：  
```json
{
  "id": "r1a2b3c4-...",
  "collector_id": "c1a2b3c4-...",
  "contact_name": "John D.",
  "contact_phone": "1234567890@c.us",
  "message_text": "Your service was excellent! Highly recommend to anyone looking for quality support.",
  "sentiment_score": 0.92,
  "sentiment_label": "positive",
  "detected_language": "en",
  "is_approved": false,
  "is_hidden": false,
  "notes": null,
  "collected_at": "2026-01-16T14:22:00Z"
}
```  

### 审核/隐藏评价（请求体示例）：  
```json
{
  "is_approved": true,
  "is_hidden": false,
  "notes": "Great testimonial — use on website"
}
```  

### 导出评价内容（查询参数示例）：  
| 参数 | 类型 | 默认值 | 说明 |  
|---------|------|---------|-------------|  
| `format` | string | `json` | 导出格式（JSON 或 HTML）。  
| `collector_id` | UUID | — | 按收集器筛选评价。  
| `approved_only` | bool | `true` | 仅导出已审核的评价。  

## **curl 示例**：  
- **创建评价收集器**：  
```bash
curl -X POST https://apiv2.waiflow.app/api/v2/reviews/collectors \
  -H "X-API-Key: mf_your_api_key_here" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Feedback",
    "session_id": "a1b2c3d4-e5f6-7890-abcd-ef1234567890",
    "source_type": "all",
    "min_sentiment_score": 0.7,
    "include_keywords": ["thank", "recommend", "love"],
    "languages": ["en"]
  }'
```  
- **列出已审核的评价**：  
```bash
curl "https://apiv2.waiflow.app/api/v2/reviews?is_approved=true&limit=20" \
  -H "X-API-Key: mf_your_api_key_here"
```  
- **将评价内容导出为 HTML**：  
```bash
curl "https://apiv2.waiflow.app/api/v2/reviews/testimonials/export?format=html&approved_only=true" \
  -H "X-API-Key: mf_your_api_key_here" \
  -o testimonials.html
```  

## **错误响应代码及含义**：  
| 状态码 | 含义 |  
|--------|---------|  
| 400 | 请求体或参数无效。  
| 401 | 未提供有效的认证信息。  
| 403 | 当前套餐不支持该功能。  
| 404 | 未找到相应的收集器或评价。  
| 422 | 验证失败（检查字段格式）。  
| 429 | 超过请求频率限制。  

## **使用建议**：  
- **情感评分阈值**：建议从 `0.6` 开始设置，根据实际情况调整。  
- **关键词过滤**：使用 `include_keywords` 参数筛选特定行业的正面评价。  
- **手动扫描**：在新连接 WhatsApp 会话后，使用 `POST /reviews/collectors/{id}/run` 命令手动收集评价。  
- **定期导出**：将已审核的评价导出，用于网站插件、社交媒体或营销材料。  

## **相关功能**：  
- **moltflow**：核心 API，支持会话管理、消息发送、群组管理等功能。  
- **moltflow-outreach**：批量发送消息、定时发送消息、自定义群组管理。  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON 导出。  
- **moltflow-ai**：基于 AI 的自动回复、语音转录、知识库管理等。  
- **moltflow-a2a**：代理间通信协议、加密消息传输、内容策略管理。  
- **moltflow-admin**：平台管理、用户管理、套餐配置等。