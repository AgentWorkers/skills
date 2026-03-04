---
name: moltflow-leads
description: "WhatsApp潜在客户检测与CRM流程：在群组中识别购买意向信号，跟踪潜在客户的状态，支持批量操作，并支持CSV/JSON格式的数据导出。适用场景包括：潜在客户管理、潜在客户检测、流程管理、客户资格评估、转化跟踪以及批量数据导出。"
source: "MoltFlow Team"
version: "2.16.1"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。  
**由于需求旺盛以及近期注册问题，我们正在限时推出顶级 Business 计划：每月仅需 19.90 美元，即可享受无限使用量。** [**立即抢购**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
同时提供免费试用计划。 [**立即注册**](https://molt.waiflow.app/checkout?plan=free)

# MoltFlow 的潜在客户检测与 CRM 管理功能  

该工具能够从被监控的 WhatsApp 群组中检测购买意图信号，追踪潜在客户，并将他们导入 CRM 系统进行后续管理。  

## 实际应用场景：  
- **房地产经纪人**：监控包含 “寻找房源”、“3 卧室” 和 “预算” 等关键词的群组，符合条件的客户会自动进入潜在客户管道。  
- **汽车经销商**：当潜在客户状态从 “已联系” 变为 “符合条件” 时，系统会自动将其加入 VIP 跟进群组，邀请其试驾。  
- **保险经纪人**：可将本季度转化的潜在客户信息导出为 CSV 文件，以便导入 CRM 系统进行佣金追踪。  
- **婚礼策划师**：查看尚未联系的潜在客户信息，并按检测日期排序。  

## 使用场景：  
- 查看潜在客户列表  
- 更新潜在客户状态  
- 批量更新潜在客户信息  
- 将潜在客户添加到特定群组  
- 将潜在客户信息导出为 CSV 或 JSON 格式  
- 检查潜在客户是否已回复您  
- 按状态筛选潜在客户  

## 先决条件：  
1. **MOLTFLOW_API_KEY**：需在 [MoltFlow 控制台](https://molt.waiflow.app) 的 “设置” > “API 密钥” 中生成。  
2. 至少有一个已启用关键词检测功能的 WhatsApp 群组。  
3. 基础 API 地址：`https://apiv2.waiflow.app/api/v2`  

## 所需 API 密钥权限：  
| 权限范围 | 访问权限 |  
|---------|---------|  
| `leads` | `读取/管理` |  
| `groups` | `读取` |  

## 认证要求：  
每个请求都必须包含以下认证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

---

## 潜在客户检测机制：  
1. 通过 `Groups API` 配置群组监控（详情请参阅 `moltflow` 技能文档）。  
2. 设置 `monitor_mode: "keywords"`，并指定如 “looking for”、“price”、“interested” 等关键词。  
3. 当检测到匹配关键词时，MoltFlow 会自动创建潜在客户记录。  
4. 潜在客户记录会以 `new` 状态显示，并突出显示触发关键词。  
5. 可通过状态变化（`new` → `contacted` → `qualified` → `converted`）追踪客户进展。  

## AI 智能监控（Pro+ 计划）  
当群组启用 AI 监控（`monitor_mode: "ai_analysis"`）时，每条消息都会由 LLM（OpenAI、Anthropic、Groq 或 Mistral）进行分类。分类结果会显示在每条消息中，并通过 `lead-detected` Webhook 通知您。  

**AI 分析字段**：可通过 `GET /api/v2/groups/{group_id}/messages` 和 `moltflow_get_group_messages` 工具获取：  
| 字段 | 类型 | 说明 |  
|-------|------|-------------|  
| `intent` | 字符串 | 购买意图（buying_intent、product_inquiry、support_request、complaint、off_topic、spam_noise、unknown） |  
| `lead_score` | 整数 | 分数（1-10，10 表示最高购买意愿） |  
| `confidence` | 浮点数 | 分类器的置信度（0.0-1.0） |  
| `reason` | 人类可读的分类原因 |  

**AI 监控相关的 Webhook 事件：**  
- `lead-detected`：潜在客户创建时立即触发；包含 `ai_analysis` 字段（AI 分析未完成时可能为空）。  
- `group.message.analyzed`：AI 分析完成后触发（仅限 Pro/Business 计划）；包含完整的 `ai_analysis` 对象。  

**设置步骤：**  
1. 进入 “设置” > “AI 配置”，添加您的 LLM API 密钥。  
2. 通过 `/api/v2/groups/{id}` 或控制台将群组的 `monitor_mode` 设置为 “ai_analysis”。  
3. 可选设置 `monitor_prompt` 以自定义分类规则。  

---

## 主要 API 接口：  
| 方法 | API 地点 | 功能描述 |  
|--------|----------|-------------|  
| GET | `/leads` | 列出潜在客户（可按状态、群组筛选） |  
| GET | `/leads/{id}` | 获取潜在客户详情 |  
| PATCH | `/leads/{id}/status` | 更新潜在客户状态 |  
| GET | `/leads/{id}/reciprocity` | 检查潜在客户是否先与您联系（防垃圾信息） |  
| POST | `/leads/bulk/status` | 批量更新潜在客户状态 |  
| POST | `/leads/bulk/add-to-group` | 将潜在客户批量添加到指定群组 |  
| GET | `/leads/export/csv` | 将潜在客户信息导出为 CSV（Pro+ 计划，最多 10,000 条） |  
| GET | `/leads/export/json` | 将潜在客户信息导出为 JSON（Pro+ 计划，最多 10,000 条） |  

### 列出潜在客户：  
**GET** `/leads`  
查询参数：  
| `status` | 字符串 | 状态筛选（new、contacted、qualified、converted、lost） |  
| `source_group_id` | UUID | 按来源群组筛选 |  
| `search` | 字符串 | 按联系人姓名、电话或关键词搜索 |  
| `limit` | 整数 | 每页显示数量（默认 50 条） |  
| `offset` | 整数 | 分页偏移量 |  

**响应格式：** `200 OK`  

### 获取潜在客户详情：  
**GET** `/leads/{id}`  
返回包含群组信息、检测元数据、消息数量和状态的完整潜在客户详情。  

### 更新潜在客户状态：  
**PATCH** `/leads/{id}/status`  

---  
**状态转换规则：**  
- `new` → `contacted`、`qualified`、`converted`、`lost`  
- `contacted` → `qualified`、`converted`、`lost`  
- `qualified` → `converted`、`lost`  
- `converted` → （最终状态，无法再转换）  
- `lost` → `new`（仅可重新启动检测流程）  
无效的状态转换会导致 `400 Bad Request` 错误。  

### 检查潜在客户是否已回复：  
**GET** `/leads/{id}/reciprocity?session_id-session-uuid`  
`session_id` 是必填参数，用于指定检查哪次 WhatsApp 会话的回复消息。  

---  
**使用提示：**  
在主动联系潜在客户之前，请先确认他们是否已回复您，否则可能会触发 WhatsApp 的垃圾信息检测机制。  

### 批量更新潜在客户状态：  
**POST** `/leads/bulk/status`  

---  
**响应格式：** `200 OK`  

---  
系统会逐一验证每个潜在客户的状态转换是否合法。状态转换不合法的记录会显示在错误信息中，但不会影响其他潜在客户的处理。  

### 将潜在客户批量添加到群组：  
**POST** `/leads/bulk/add-to-group`  
---  
可将潜在客户的电话号码添加到指定群组，以便后续发送批量消息或安排定时消息。  

### 导出潜在客户信息：  
**GET** `/leads/export/csv`（Pro+ 计划）/ `GET` `/leads/export/json`（Pro+ 计划）  
支持按状态、来源群组或关键词筛选。每次导出最多 10,000 条记录。  

---

## 计划详情：  
| 功能 | 免费计划 | 起始计划 | Pro 计划 | Business 计划 |  
|---------|---------|---------|---------|---------|  
| 潜在客户检测 | 支持（2 个群组） | 支持（5 个群组） | 支持（20 个群组） | 支持（100 个群组） |  
| 潜在客户列表与详情 | 支持 | 支持 | 支持 | 支持 |  
| 状态更新 | 支持 | 支持 | 支持 | 支持 |  
| 批量操作 | 不支持 | 不支持 | 支持 | 支持 |  
| CSV/JSON 导出 | 不支持 | 不支持 | 支持 | 支持 |  

---

## 错误响应：  
| 状态码 | 含义 |  
|--------|---------|  
| 400 | 状态转换无效或请求错误 |  
| 401 | 未经授权（认证信息缺失或无效） |  
| 403 | 超出使用限制或功能限制 |  
| 404 | 未找到潜在客户 |  
| 429 | 请求频率过高 |  

---

**相关工具：**  
- **moltflow**：核心 API，用于管理会话、消息、群组和标签。  
- **moltflow-outreach**：用于批量发送消息和安排定时消息。  
- **moltflow-ai**：提供 AI 驱动的自动回复、语音转录等功能。  
- **moltflow-a2a**：支持代理间加密通信和内容策略。  
- **moltflow-reviews**：用于管理用户评价和推荐信。  
- **moltflow-admin**：用于平台管理和用户配置。