---
name: moltflow-reviews
description: "通过 MoltFlow API 收集和管理客户评价：包括情感分析、评价内容的提取以及评价的管理功能。"
source: "MoltFlow Team"
version: "2.16.1"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。  
**由于需求量大以及近期注册问题，我们特推出顶级商务计划：每月仅需 19.90 美元（按年计费），并提供无限使用额度——此优惠仅限限时有效。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
**也提供免费试用计划。** [立即注册](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow 评论管理功能  

通过 MoltFlow API 收集、分析和管理客户评论。实现自动情感评分、提取用户评价，并将评论内容导出以供业务使用。  

## 实际应用场景  

**餐厅老板**：  
“每次晚餐预订后，从 WhatsApp 聊天记录中收集客户反馈；对情感评分高于 0.8 的评论自动批准。”  

**Airbnb 房东**：  
“扫描客人留言中包含的正面评价词汇（如‘棒极了’、‘环境干净’、‘推荐’等），并将优质评价内容以 HTML 格式导出到房源页面。”  

**牙医**：  
“在患者咨询聊天窗口设置评论收集功能；仅记录包含‘感谢’或‘服务很棒’等词汇的英文评论。”  

## 使用场景  
- 需要自动从 WhatsApp 聊天中收集评论  
- 配置评论收集规则（包括情感评分阈值）  
- 列出、批准、隐藏或删除收集到的评论  
- 将评论内容导出为 JSON 或 HTML 格式供外部使用  
- 手动触发评论收集  
- 查看评论统计数据和情感分析结果  

**相关术语**：  
- **收集评论**  
- **设置评论收集器**  
- **导出评价内容**  
- **情感分析**  
- **客户反馈（WhatsApp）**  

## 先决条件  
- **MOLTFLOW_API_KEY**：必需（可在 [MoltFlow 仪表板 > API 密钥](https://molt.waiflow.app/api-keys) 处生成）  
- 至少已连接一个 WhatsApp 账户（状态为“正常运行”）  
- 需使用 MoltFlow Pro 或更高版本的订阅计划（评论收集功能为付费服务）  

## 基本 URL  
```
https://apiv2.waiflow.app/api/v2
```  

## 所需 API 密钥权限  
| 权限范围 | 访问权限 |  
|---------|------------|  
| `reviews` | `读取/管理` |  

## 认证方式  
所有请求均需提供以下认证信息之一：  
- `Authorization: Bearer <access_token>`（登录后生成的 JWT 令牌）  
- `X-API-Key: <api_key>`（来自仪表板的 API 密钥）  

---

## 评论收集器  
评论收集器可根据情感评分、关键词匹配和语言筛选自动提取评论：  

| 方法 | 端点 | 说明 |  
|--------|---------|-------------|  
| GET | `/reviews/collectors` | 查看所有评论收集器 |  
| POST | `/reviews/collectors` | 创建新的评论收集器 |  
| GET | `/reviews/collectors/{id}` | 查看收集器详情 |  
| PATCH | `/reviews/collectors/{id}` | 更新收集器配置 |  
| DELETE | `/reviews/collectors/{id}` | 删除收集器 |  
| POST | `/reviews/collectors/{id}/run` | 手动触发评论收集 |

### 创建评论收集器（请求体）  
**`source_type` 可选值：`all` | `groups` | `chats` | `selected`**  
当 `source_type` 为 `selected` 时，需提供具体的 WhatsApp 聊天 ID（`selected_chat_ids`）。  

### 创建评论收集器（响应内容）  
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

### 更新评论收集器（请求体）  
所有字段均为可选；仅更新提供的字段。  
```json
{
  "name": "Updated Collector Name",
  "min_sentiment_score": 0.7,
  "is_active": false
}
```  

## 评论数据  
收集到的评论包含原始消息、情感评分、联系人信息及审批状态：  

| 方法 | 端点 | 说明 |  
|--------|---------|-------------|  
| GET | `/reviews` | 查看评论列表（可设置筛选条件） |  
| GET | `/reviews/stats` | 查看评论统计信息 |  
| GET | `/reviews/{id}` | 查看单条评论 |  
| PATCH | `/reviews/{id}` | 批准/隐藏/添加备注 |  
| DELETE | `/reviews/{id}` | 删除评论 |  
| GET | `/reviews/testimonials/export` | 导出评论内容（JSON 或 HTML 格式） |  

### 查看评论（查询参数）  
| 参数 | 类型 | 默认值 | 说明 |  
|---------|--------|-------------|  
| `collector_id` | UUID | — | 按收集器筛选评论 |  
| `is_approved` | bool | — | 仅显示已批准的评论 |  
| `is_hidden` | bool | — | 显示隐藏的评论 |  
| `min_score` | float | — | 最低情感评分阈值 |  
| `limit` | int | 50 | 每页显示条数 |  
| `offset` | int | 0 | 分页偏移量 |  

### 评论对象（详细信息）  
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

### 批准/隐藏评论（请求体）  
```json
{
  "is_approved": true,
  "is_hidden": false,
  "notes": "Great testimonial — use on website"
}
```  

### 导出评论内容（查询参数）  
| 参数 | 类型 | 默认值 | 说明 |  
|---------|--------|-------------|  
| `format` | string | `json` | 导出格式（JSON 或 HTML） |  
| `collector_id` | UUID | — | 按收集器筛选评论 |  
| `approved_only` | bool | `true` | 仅导出已批准的评论 |  

---

## 使用 curl 的示例代码  
- **创建评论收集器**  
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
- **查看已批准的评论**  
```bash
curl "https://apiv2.waiflow.app/api/v2/reviews?is_approved=true&limit=20" \
  -H "X-API-Key: mf_your_api_key_here"
```  
- **将评论内容导出为 HTML**  
```bash
curl "https://apiv2.waiflow.app/api/v2/reviews/testimonials/export?format=html&approved_only=true" \
  -H "X-API-Key: mf_your_api_key_here" \
  -o testimonials.html
```  

## 错误响应代码及含义  
| 状态码 | 说明 |  
|--------|---------|  
| 400 | 请求体或参数无效 |  
| 401 | 未提供有效的认证信息 |  
| 403 | 当前订阅计划不支持该功能 |  
| 404 | 未找到相关评论或收集器 |  
| 422 | 验证失败（检查字段格式） |  
| 429 | 超过请求频率限制 |  

## 使用建议：  
- **情感评分阈值**：建议从 0.6 开始设置，根据实际情况进行调整（避免误判）。  
- **关键词筛选**：使用 `include_keywords` 参数筛选特定行业的正面评价词汇。  
- **手动收集评论**：在新连接 WhatsApp 账户后，使用 `POST /reviews/collectors/{id}/run` 命令手动触发评论收集。  
- **定期导出评论**：将已批准的评论导出，用于网站展示、社交媒体或营销材料。  

## 相关功能  
- **moltflow**：核心 API（用于管理会话、发送消息、分组等）  
- **moltflow-outreach**：批量发送消息、定时发送通知、自定义分组管理  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON 数据导出  
- **moltflow-ai**：基于 AI 的自动回复功能、语音转录、知识库管理等  
- **moltflow-a2a**：代理间通信协议、加密消息传输、内容策略管理  
- **moltflow-admin**：平台管理、用户管理、计划配置工具