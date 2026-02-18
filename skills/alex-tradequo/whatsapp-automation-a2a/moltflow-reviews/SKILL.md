---
name: moltflow-reviews
description: "通过 MoltFlow API 收集和管理客户评价：包括情感分析、证言提取以及评价内容的日常管理。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。  
**由于需求旺盛以及近期出现的注册问题，我们特别推出了一项限时优惠：顶级 Business 计划，每月仅需 19.90 美元，即可享受无限使用额度。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时提供免费试用计划。[立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow 评论管理功能  

通过 MoltFlow API 收集、分析和管理客户评论，实现情感评分自动化、提取用户评价，并导出用于展示的社交证明数据。  

## 使用场景  
- 从 WhatsApp 对话中自动收集评论  
- 创建或配置评论收集器，并设置情感评分阈值  
- 列出、审核、隐藏或删除收集到的评论  
- 将用户评价导出为 JSON 或 HTML 格式以供外部使用  
- 触发对对话内容的手动审核以获取评论  
- 查看评论统计数据和情感分析结果  

## 前提条件  
- **MOLTFLOW_API_KEY**：必需（请从 [MoltFlow 仪表板 > API 密钥](https://molt.waiflow.app/api-keys) 生成）  
- 至少已连接一个 WhatsApp 会话（状态为 `working`）  
- 使用 MoltFlow Pro 计划或更高版本（评论收集功能为付费选项）  

## 基本 URL  
```
https://apiv2.waiflow.app/api/v2
```  

## 所需 API 密钥权限  
| 权限范围 | 访问权限 |  
|---------|---------|  
| `reviews` | `read/manage` |  

## 认证方式  
所有请求需提供以下认证信息之一：  
- `Authorization: Bearer <access_token>`（登录后生成的 JWT）  
- `X-API-Key: <api_key>`（来自仪表板的 API 密钥）  

---

## 评论收集器  
评论收集器可根据情感评分、关键词匹配和语言过滤器自动提取评论：  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/reviews/collectors` | 列出所有收集器 |  
| POST | `/reviews/collectors` | 创建新的收集器 |  
| GET | `/reviews/collectors/{id}` | 获取收集器详细信息 |  
| PATCH | `/reviews/collectors/{id}` | 更新收集器配置 |  
| DELETE | `/reviews/collectors/{id}` | 删除收集器 |  
| POST | `/reviews/collectors/{id}/run` | 触发手动审核操作 |  

### 创建收集器（请求体）  
**`source_type` 可选值：`all` | `groups` | `chats` | `selected`**  
当 `source_type` 为 `selected` 时，需提供具体的 WhatsApp 聊天 ID（`selected_chat_ids`）。  

### 创建收集器的响应内容  
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

### 更新收集器（请求体）  
所有字段均为可选字段；仅更新提供的字段。  
```json
{
  "name": "Updated Collector Name",
  "min_sentiment_score": 0.7,
  "is_active": false
}
```  

## 评论数据  
收集到的评论包含原始消息、情感评分、联系信息及审核状态：  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/reviews` | 列出评论（可设置过滤条件） |  
| GET | `/reviews/stats` | 查看评论统计信息 |  
| GET | `/reviews/{id}` | 获取单条评论 |  
| PATCH | `/reviews/{id}` | 审核、隐藏或添加备注 |  
| DELETE | `/reviews/{id}` | 删除评论 |  
| GET | `/reviews/testimonials/export` | 导出用户评价 |  

### 查看评论（查询参数）  
| 参数 | 类型 | 默认值 | 说明 |  
|---------|------|---------|-------------|  
| `collector_id` | UUID | — | 按收集器筛选评论 |  
| `is_approved` | bool | — | 仅显示已审核的评论 |  
| `is_hidden` | bool | — | 显示隐藏的评论 |  
| `min_score` | float | — | 最低情感评分阈值 |  
| `limit` | int | 50 | 每页显示数量 |  
| `offset` | int | 0 | 分页偏移量 |  

### 评论对象结构  
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

### 审核/隐藏评论（请求体）  
```json
{
  "is_approved": true,
  "is_hidden": false,
  "notes": "Great testimonial — use on website"
}
```  

### 导出用户评价（查询参数）  
| 参数 | 类型 | 默认值 | 说明 |  
|---------|------|---------|-------------|  
| `format` | string | `json` | 导出格式（json 或 html） |  
| `collector_id` | UUID | — | 按收集器筛选评论 |  
| `approved_only` | bool | `true` | 仅导出已审核的评论 |  

---

## curl 示例  
- **创建评论收集器**：  
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
- **列出已审核的评论**：  
```bash
curl "https://apiv2.waiflow.app/api/v2/reviews?is_approved=true&limit=20" \
  -H "X-API-Key: mf_your_api_key_here"
```  
- **将用户评价导出为 HTML 格式**：  
```bash
curl "https://apiv2.waiflow.app/api/v2/reviews/testimonials/export?format=html&approved_only=true" \
  -H "X-API-Key: mf_your_api_key_here" \
  -o testimonials.html
```  

## 错误代码及含义  
| 状态码 | 含义 |  
|--------|---------|  
| 400 | 请求体或参数无效 |  
| 401 | 认证信息缺失或无效 |  
| 403 | 当前计划不支持该功能 |  
| 404 | 未找到收集器或评论 |  
| 422 | 验证错误（检查字段约束） |  
| 429 | 超过请求频率限制 |  

## 使用建议：  
- **情感评分阈值**：建议从 `0.6` 开始设置，根据实际情况调整以提高准确性。  
- **关键词过滤**：使用 `include_keywords` 参数筛选特定行业的正面评价。  
- **手动审核**：在新会话连接后，使用 `POST /reviews/collectors/{id}/run` 触发手动审核。  
- **定期导出**：将已审核的用户评价导出，用于网站插件、社交媒体或营销材料。  

## 相关功能  
- **moltflow**：核心 API（用于管理会话、消息发送、群组设置等）  
- **moltflow-outreach**：批量发送消息、定时发送消息、自定义群组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON 导出  
- **moltflow-ai**：基于 AI 的自动回复、语音转录、知识库管理  
- **moltflow-a2a**：代理间通信协议、加密消息传输、内容策略管理  
- **moltflow-admin**：平台管理、用户管理、计划配置