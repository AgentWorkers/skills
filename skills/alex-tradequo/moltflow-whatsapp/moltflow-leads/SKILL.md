---
name: moltflow-leads
description: "WhatsApp潜在客户检测与CRM流程：在群组中识别购买意向信号，跟踪潜在客户的状态，支持批量操作，并支持CSV/JSON格式的数据导出。适用场景包括：潜在客户管理、潜在客户检测、流程管理、客户资格评估、转化跟踪以及批量数据导出。"
source: "MoltFlow Team"
version: "2.15.1"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
> **MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。  
> **由于需求量大以及近期注册问题，我们特别推出了一项限时优惠：顶级商业计划，每月仅需 $19.90（按年计费），并提供无限使用量。** [**立即抢购**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
> 免费试用计划也可使用。 [**立即注册**](https://molt.waiflow.app/checkout?plan=free)  

# MoltFlow — 销售线索检测与客户关系管理（CRM）系统  

该系统能够从被监控的 WhatsApp 群组中检测购买意向信号，跟踪销售线索，执行批量操作，并将数据导出至您的 CRM 系统。  

## 实际应用场景  

**房地产经纪人**：“监控我的房产群组，关注包含‘寻找房产’、‘3居室’、‘预算’等关键词的聊天记录，符合条件的人会自动进入我的销售线索系统。”  
**汽车经销商**：“当线索状态从‘已联系’变为‘符合条件’时，自动将其加入 VIP 跟进群组，发送试驾邀请。”  
**保险经纪人**：“将本季度转化的所有线索导出为 CSV 文件，以便导入 CRM 系统进行佣金追踪。”  
**婚礼策划师**：“显示所有尚未联系的新线索，按检测日期排序。”  

## 使用场景  

- **列出所有线索**  
- **更新线索状态**  
- **批量更新线索状态**  
- **将线索添加到特定群组**  
- **将线索导出为 CSV 或 JSON 格式**  
- **检查线索的互动历史**（即对方是否已回复过您）  
- **按状态筛选线索**  

## 先决条件  

1. **MOLTFLOW_API_KEY** — 请在 [MoltFlow 控制台](https://molt.waiflow.app) 的“设置” > “API 密钥”中生成。  
2. 至少需要一个启用了关键词检测功能的 WhatsApp 群组。  
3. 基本 API 地址：`https://apiv2.waiflow.app/api/v2`  

## 所需 API 密钥权限  

| 权限范围 | 访问权限 |  
|---------|---------|  
| `leads` | `读取/管理` |  
| `groups` | `读取` |  

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

## 销售线索检测机制  

1. 通过 `Groups API` 配置群组监控（详见 `moltflow` 技能文档）。  
2. 设置 `monitor_mode: "keywords"`，并指定关键词（如 “looking for”, “price”, “interested”）。  
3. 当检测到匹配关键词时，MoltFlow 会自动创建一条销售线索。  
4. 线索会以 `new` 状态显示，并突出显示触发该状态的关键词。  
5. 线索状态会依次更新为 `contacted`, `qualified`, `converted`。  

## AI 智能监控（Pro+ 计划）  

当群组启用 AI 监控（`monitor_mode: "ai_analysis"`）时，每条消息都会由您指定的 LLM（OpenAI、Anthropic、Groq 或 Mistral）进行分类。分类结果会显示在每条消息中，并通过 `lead-detected` Webhook 通知您。  

**AI 分析字段**：可通过 `GET /api/v2/groups/{group_id}/messages` 或 MCP 工具 `moltflow_get_group_messages` 获取：  

| 字段 | 类型 | 描述 |  
|-------|------|-------------|  
| `intent` | 字符串 | 购买意向（buying_intent, product_inquiry, support_request, complaint, off_topic, spam_noise, unknown） |  
| `lead_score` | 整数 | 分数（1-10，分数越高表示购买意向越强） |  
| `confidence` | 浮点数 | 分类器的置信度（0.0-1.0） |  
| `reason` | 人类可读的分类原因 |  

**AI 监控相关的 Webhook 事件**：  
- `lead-detected`：线索创建时立即触发；包含 `ai_analysis` 字段（若 AI 分析尚未完成，则该字段可能为空）。  
- `group.message.analyzed`：AI 分析完成后触发（仅限 Pro/Business 计划用户）；包含完整的 `ai_analysis` 对象。  

**设置步骤**：  
1. 进入“设置” > “AI 配置”，添加您的 LLM API 密钥。  
2. 通过 `/api/v2/groups/{id}` 或控制台设置 `monitor_mode: "ai_analysis"`。  
3. （可选）设置 `monitorprompt` 以自定义分类规则。  

---

## 销售线索 API  

| 方法 | API 端点 | 功能 |  
|--------|----------|-------------|  
| GET | `/leads` | 列出所有线索（可按状态、群组筛选） |  
| GET | `/leads/{id}` | 查看单条线索详情 |  
| PATCH | `/leads/{id}/status` | 更新线索状态 |  
| GET | `/leads/{id}/reciprocity` | 检查对方是否先发送过消息（防垃圾信息） |  
| POST | `/leads/bulk/status` | 批量更新线索状态 |  
| POST | `/leads/bulk/add-to-group` | 将线索批量添加到指定群组 |  
| GET | `/leads/export/csv` | 将线索导出为 CSV 文件（Pro+ 计划，最多 10,000 条） |  
| GET | `/leads/export/json` | 将线索导出为 JSON 文件（Pro+ 计划，最多 10,000 条） |  

### 列出线索  

**GET** `/leads`  

查询参数：  
- `status`：按状态（`new`, `contacted`, `qualified`, `converted`, `lost`）筛选线索。  
- `source_group_id`：按来源群组筛选线索。  
- `search`：按联系人姓名、电话号码或关键词搜索线索。  
- `limit`：每页显示的线索数量（默认 50 条）。  
- `offset`：分页偏移量。  

**响应格式**：`200 OK`  

---

### 查看线索详情  

**GET** `/leads/{id}`  

返回包含群组信息、检测详情、消息数量和状态在内的完整线索信息。  

### 更新线索状态  

**PATCH** `/leads/{id}/status`  

---  

**状态转换规则**：  
- `new` -> `contacted`, `qualified`, `converted`, `lost`  
- `contacted` -> `qualified`, `converted`, `lost`  
- `qualified` -> `converted`, `lost`  
- `converted`：达到最终状态后无法再次转换。  
- `lost` -> 可重新标记为 `new`（仅限重新启动监控）。  
无效的状态转换会导致 `400 Bad Request` 错误。  

### 检查线索互动历史  

**GET** `/leads/{id}/reciprocity?session_id-session-uuid`  

`session_id` 是必填参数，用于指定要检查的 WhatsApp 会话。  

---  

**使用提示**：  
在主动联系之前，请先确认线索是否已发送过消息；否则，发送冷邮件可能会触发 WhatsApp 的垃圾信息检测机制。  

### 批量更新线索状态  

**POST** `/leads/bulk/status`  

---  

**响应格式**：`200 OK`  

---  

系统会逐一验证每条线索的状态转换是否合法。状态转换不合法的线索会被标记为错误，但不会影响其他线索的处理。  

### 将线索批量添加到群组  

**POST** `/leads/bulk/add-to-group`  

---  

**导出线索**：  
- **CSV 格式**：`/leads/export/csv`  
- **JSON 格式**：`/leads/export/json`  
支持按 `status`, `source_group_id`, `search` 筛选条件。最多导出 10,000 条线索（Pro+ 计划用户）。  

---

## 示例：  
**完整工作流程**：检测线索 → 评估线索质量 → 主动联系客户  

---  

## 计划版本差异  

| 功能 | 免费版 | 起始版 | Pro 版 | 商业版 |  
|---------|---------|---------|-----|----------|  
| 销售线索检测 | 支持（2 个群组） | 支持（5 个群组） | 支持（20 个群组） | 支持（100 个群组） |  
| 线索列表与详情 | 支持 | 支持 | 支持 | 支持 |  
| 状态更新 | 支持 | 支持 | 支持 | 支持 |  
| 批量操作 | 不支持 | 不支持 | 支持 | 支持 |  
| CSV/JSON 导出 | 不支持 | 不支持 | 支持 | 支持 |  

---

## 错误响应代码  

| 状态码 | 含义 |  
|--------|---------|  
| 400 | 状态转换无效或请求错误 |  
| 401 | 未经授权（缺少或无效的认证信息） |  
| 403 | 超出计划使用限制或功能限制 |  
| 404 | 未找到线索 |  
| 429 | 请求次数过多（频率限制） |  

---

**相关工具**：  
- **moltflow**：核心 API，用于管理会话、消息、群组和 Webhook。  
- **moltflow-outreach**：用于批量发送消息、安排定时消息和创建自定义群组。  
- **moltflow-ai**：提供 AI 驱动的自动回复、语音转录等功能。  
- **moltflow-a2a**：支持代理间加密通信和内容策略管理。  
- **moltflow-reviews**：用于收集用户评价和管理客户反馈。  
- **moltflow-admin**：用于平台管理和用户配置。