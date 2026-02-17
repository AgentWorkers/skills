---
name: moltflow-reviews
description: "从 WhatsApp 对话中收集并分析客户评价。通过 MoltFlow API 进行情感分析、提取用户证言以及管理客户评价。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。  
**由于需求旺盛以及近期出现的注册问题，我们特别推出了一项限时优惠：顶级商务计划（Business Plan），每月仅需 19.90 美元，即可享受无限使用量。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时提供免费试用计划。 [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow 的主要功能：  
- **收集、分析和管理客户评价**：从 WhatsApp 对话中收集评价信息，自动进行情感分析，提取用户反馈。  
- **自动化处理评价流程**：支持批量处理评价，包括审核、隐藏或删除操作。  
- **导出评价内容**：可将评价结果以 JSON 或 HTML 格式导出，便于后续使用（如网站插件、社交媒体或营销材料）。  

## 使用场景：  
- **自动收集评价**：设置自动评价收集机制。  
- **配置评价规则**：自定义情感评分阈值或关键词筛选条件。  
- **管理评价数据**：查看评价列表，审批、隐藏或删除评价内容。  
- **数据导出**：灵活导出评价数据以供外部使用。  
- **统计分析**：获取评价数量及情感分析结果。  

## 前提条件：  
- **MOLTFLOW_API_KEY**：必需的 API 密钥（可在 [MoltFlow 仪表板 > API Keys](https://molt.waiflow.app/api-keys) 生成）。  
- 至少已连接一个处于“工作状态”（working）的 WhatsApp 会话。  
- 需使用 MoltFlow Pro 或更高版本的订阅计划（评价功能为付费选项）。  

## 基本 URL 结构：  
```
https://apiv2.waiflow.app/api/v2
```  

## 所需 API 密钥权限：  
| 权限范围 | 访问权限 |  
|--------|--------|  
| `reviews` | `read/manage` |  

## 认证方式：  
所有请求均需提供以下认证信息之一：  
- `Authorization: Bearer <access_token>`（登录后生成的 JWT 令牌）  
- `X-API-Key: <api_key>`（来自仪表板的 API 密钥）  

---

## 评价收集器（Review Collectors）：  
这些工具可监控 WhatsApp 对话，并根据情感评分、关键词匹配或语言筛选条件自动提取评价内容：  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/reviews/collectors` | 查看所有评价收集器。  
| POST | `/reviews/collectors` | 创建新的评价收集器。  
| GET | `/reviews/collectors/{id}` | 获取特定收集器的详细信息。  
| PATCH | `/reviews/collectors/{id}` | 更新收集器配置。  
| DELETE | `/reviews/collectors/{id}` | 删除收集器。  
| POST | `/reviews/collectors/{id}/run` | 手动触发评价收集。  

### 创建评价收集器（Create Collector）：  
**请求体示例（Request Body）：**  
```json
{
  "source_type": "selected",  // 设置数据来源类型（all、groups、chats 或 selected）
  "selected_chat_ids": [chat IDs]  // 提供需要收集评价的 WhatsApp 聊天 ID 列表
}
```  
**响应示例（Response Example）：**  
```json
{
  "collectors": [
  {
    "id": "collector1",
    "name": "Team Feedback",
    "status": "active",
    // 其他配置信息
  },
  // 其他收集器信息
}
```  

### 更新评价收集器（Update Collector）：  
**请求体示例（Request Body）：**  
```json
{
  "collector_id": "collector1",
  "config": {
    // 更新的配置项
  }
}
```  
（仅提供需要更新的字段。）  

## 评价数据（Reviews）：  
收集到的评价信息包含原始对话内容、情感评分、联系人信息及审核状态：  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/reviews` | 查看评价列表（可添加过滤条件）。  
| GET | `/reviews/stats` | 获取评价统计信息。  
| GET | `/reviews/{id}` | 获取单条评价详情。  
| PATCH | `/reviews/{id}` | 审核、隐藏或添加备注。  
| DELETE | `/reviews/{id}` | 删除评价。  
| GET | `/reviews/testimonials/export` | 导出评价内容（JSON 或 HTML 格式）。  

### 查看评价列表（List Reviews）：  
**查询参数（Query Parameters）：**  
| 参数 | 类型 | 默认值 | 说明 |  
|---------|------|---------|-------------|  
| collector_id | UUID | | 按收集器筛选评价。  
| is_approved | bool | | 仅显示已审核的评价。  
| is_hidden | bool | | 显示隐藏的评价。  
| min_score | float | | 最低情感评分阈值。  
| limit | int | | 每页显示条数。  
| offset | int | | 分页偏移量。  
```  

### 评价对象（Review Object）：  
包含评价的详细信息：  
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

### 审核/隐藏评价（Approve/Hide Reviews）：  
**请求体示例（Request Body）：**  
```json
{
  "id": "evaluation_id",
  "action": "approve"  // 或 "hide"
}
```  

### 导出评价内容（Export Testimonials）：  
**查询参数（Query Parameters）：**  
| 参数 | 类型 | 默认值 | 说明 |  
|---------|------|---------|-------------|  
| format | string | "json" | 导出格式（json 或 html）。  
| collector_id | UUID | | 按收集器筛选评价。  
| approved_only | bool | | 仅导出已审核的评价。  
```  

## 使用 curl 的示例：  
- **创建评价收集器**：  
```bash
curl -X POST https://molt.waiflow.app/reviews/collectors -d '{"source_type": "selected", "selected_chat_ids": ["chat1_id", "chat2_id"]}'
```  
- **查看已审核的评价**：  
```bash
curl -X GET https://molt.waiflow.app/reviews
```  
- **导出评价内容（HTML 格式）**：  
```bash
curl -X GET https://molt.waiflow.app/reviews/testimonials/export -f json -c collector_id="collector_id"
```  

## 错误响应（Error Responses）：  
| 状态码 | 含义 |  
|--------|---------|  
| 400 | 请求体或参数无效。  
| 401 | 未提供有效的认证信息。  
| 403 | 当前订阅计划不支持该功能。  
| 404 | 未找到相应的收集器或评价内容。  
| 422 | 验证失败（检查字段格式）。  
| 429 | 超过请求频率限制。  

## 使用建议：  
- **情感评分阈值**：初始值设为 0.6，可根据实际需求调整。  
- **关键词过滤**：使用 `include_keywords` 参数筛选特定行业的正面评价关键词。  
- **手动收集**：在新会话连接后，使用 `POST /reviews/collectors/{id}/run` 手动触发评价收集。  
- **定期导出**：定期导出已审核的评价数据，用于网站或营销用途。  

## 相关服务：  
- **moltflow**：核心 API，支持会话管理、消息发送、群组管理等功能。  
- **moltflow-outreach**：批量发送消息、定时发送功能。  
- **moltflow-leads**：潜在客户检测、流程跟踪及数据导出。  
- **moltflow-ai**：基于 AI 的自动回复、语音转录等服务。  
- **moltflow-a2a**：代理间加密通信协议。  
- **moltflow-admin**：平台管理工具，用于用户管理和计划配置。