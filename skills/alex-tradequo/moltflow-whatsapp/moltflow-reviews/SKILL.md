---
name: moltflow-reviews
description: "通过 MoltFlow API 收集和管理客户评价：包括情感分析、证词提取以及评价内容的管理功能。"
source: "MoltFlow Team"
version: "2.15.1"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
> **MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 沟通。  
> **由于需求旺盛以及近期出现的注册问题，我们特别推出了一项限时优惠：顶级 Business 计划，每月仅需 $19.90（按年计费），并提供无限使用额度。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
> 免费试用计划也可使用。 [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow 评论管理功能  

通过 MoltFlow API 收集、分析和管理客户评论。可自动进行情感分析、提取用户评价，并将评论内容导出以供业务使用。  

## 实际应用场景  

**餐厅老板**：**每次晚餐预订后，从 WhatsApp 聊天记录中收集客户反馈，自动批准评分高于 0.8 的评论。**  
**Airbnb 房东**：**扫描客人留言中包含“令人惊叹”、“干净”或“推荐”等正面词汇的评论，并将其以 HTML 格式导出到房源页面。**  
**牙医**：**在患者服务聊天界面设置评论收集功能，仅捕获包含“感谢”或“服务很棒”等词语的英文评论。**  

## 使用场景  

- 需要自动从 WhatsApp 聊天中收集评论时  
- 需要创建或配置带有情感评分阈值的评论收集器时  
- 需要列出、批准、隐藏或删除收集到的评论时  
- 需要将评论内容导出为 JSON 或 HTML 格式供外部使用时  
- 需要手动触发评论收集时  
- 需要查看评论统计数据和情感分析结果时  

**相关术语**：  
- **评论收集** (Review Collection)  
- **情感分析** (Sentiment Analysis)  
- **客户反馈** (Customer Feedback)  
- **API Key** (API Key)  

## 先决条件  

- **MOLTFLOW_API_KEY**：必需。可从 [MoltFlow 控制台 > API Keys](https://molt.waiflow.app/api-keys) 生成。  
- 至少已连接一个处于“工作状态”（working）的 WhatsApp 账户。  
- 需要使用 MoltFlow Pro 计划或更高版本（评论收集功能为付费服务）。  

## 基本 URL  

```
https://apiv2.waiflow.app/api/v2
```  

## 所需 API Key 权限范围  

| 权限范围 | 访问权限 |  
|---------|---------|  
| `reviews` | `read/manage` |  

## 认证方式  

所有请求均需提供以下认证信息之一：  
- `Authorization: Bearer <access_token>`（登录后生成的 JWT 令牌）  
- `X-API-Key: <api_key>`（来自控制台的 API 密钥）  

---

## 评论收集器（Review Collectors）  

评论收集器可根据情感评分、关键词匹配和语言筛选自动提取评论。  

| 方法 | 端点 | 描述 |  
|-------|---------|-------------|  
| GET | `/reviews/collectors` | 查看所有评论收集器 |  
| POST | `/reviews/collectors` | 创建新的评论收集器 |  
| GET | `/reviews/collectors/{id}` | 获取评论收集器详情 |  
| PATCH | `/reviews/collectors/{id}` | 更新评论收集器配置 |  
| DELETE | `/reviews/collectors/{id}` | 删除评论收集器 |  
| POST | `/reviews/collectors/{id}/run` | 手动触发评论收集 |  

### 创建评论收集器（Create Collector）——请求体  

**`source_type` 可选值：**  
- `all` | 所有聊天记录  
- `groups` | 指定群组内的聊天记录  
- `chats` | 单个聊天记录  
- `selected` | 用户指定的聊天记录 ID  

当 `source_type` 为 `selected` 时，需提供 `selected_chat_ids`（具体的 WhatsApp 聊天记录 ID）。  

### 创建评论收集器（Create Collector）——响应内容  

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

### 更新评论收集器（Update Collector）——请求体  

所有字段均为可选。仅更新提供的字段。  

```json
{
  "name": "Updated Collector Name",
  "min_sentiment_score": 0.7,
  "is_active": false
}
```  

## 评论信息（Reviews）  

收集到的评论包含原始消息、情感评分、联系信息和审核状态。  

| 方法 | 端点 | 描述 |  
|-------|---------|-------------|  
| GET | `/reviews` | 查看评论列表（可设置过滤条件） |  
| GET | `/reviews/stats` | 查看评论统计信息 |  
| GET | `/reviews/{id}` | 查看单条评论 |  
| PATCH | `/reviews/{id}` | 批准、隐藏或添加备注 |  
| DELETE | `/reviews/{id}` | 删除评论 |  
| GET | `/reviews/testimonials/export` | 导出评论内容（JSON 或 HTML 格式） |  

### 查看评论列表（List Reviews）——查询参数  

| 参数 | 类型 | 默认值 | 描述 |  
|---------|--------|----------------|  
| `collector_id` | UUID | — | 按评论收集器筛选 |  
| `is_approved` | bool | — | 仅显示已批准的评论 |  
| `is_hidden` | bool | — | 显示隐藏的评论 |  
| `min_score` | float | — | 最低情感评分阈值 |  
| `limit` | int | 50 | 每页显示的评论数量 |  
| `offset` | int | 0 | 分页偏移量 |  

### 评论对象（Review Object）  

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

### 批准/隐藏评论（Approve/Hide Review）——请求体  

```json
{
  "is_approved": true,
  "is_hidden": false,
  "notes": "Great testimonial — use on website"
}
```  

### 导出评论内容（Export Testimonials）——查询参数  

| 参数 | 类型 | 默认值 | 描述 |  
|---------|--------|----------------|  
| `format` | string | `json` | 导出格式（JSON 或 HTML） |  
| `collector_id` | UUID | — | 按评论收集器筛选 |  
| `approved_only` | bool | `true` | 仅导出已批准的评论 |  

---

## curl 示例  

### 1. 创建评论收集器  

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

### 2. 查看已批准的评论  

```bash
curl "https://apiv2.waiflow.app/api/v2/reviews?is_approved=true&limit=20" \
  -H "X-API-Key: mf_your_api_key_here"
```  

### 3. 将评论内容导出为 HTML  

```bash
curl "https://apiv2.waiflow.app/api/v2/reviews/testimonials/export?format=html&approved_only=true" \
  -H "X-API-Key: mf_your_api_key_here" \
  -o testimonials.html
```  

## 错误响应（Error Responses）  

| 状态码 | 错误原因 |  
|---------|----------------|  
| 400 | 请求体或参数无效 |  
| 401 | 未提供有效的认证信息 |  
| 403 | 当前套餐不支持该功能 |  
| 404 | 未找到评论收集器或评论 |  
| 422 | 验证失败（字段格式错误） |  
| 429 | 超过请求频率限制 |  

## 使用提示：  
- **情感评分阈值**：建议从 0.6 开始设置，根据实际情况调整。  
- **关键词过滤**：使用 `include_keywords` 参数匹配行业特定的正面评价词汇。  
- **手动收集评论**：在新连接 WhatsApp 账户后，使用 `POST /reviews/collectors/{id}/run` 命令手动触发评论收集。  
- **定期导出评论**：将已批准的评论导出，用于网站插件、社交媒体或营销材料。  

## 相关功能：  
- **moltflow**：核心 API，支持会话管理、消息发送、群组管理、标签设置和 Webhook 配置。  
- **moltflow-outreach**：批量发送消息、定时发送消息和自定义群组管理。  
- **moltflow-leads**：潜在客户检测、流程跟踪和批量操作功能。  
- **moltflow-ai**：基于 AI 的自动回复、语音转录、知识库管理等功能。  
- **moltflow-a2a**：支持代理间加密通信和内容策略管理。  
- **moltflow-admin**：平台管理、用户管理和计划配置工具。