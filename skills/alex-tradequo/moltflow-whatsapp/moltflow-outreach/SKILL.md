---
name: moltflow-outreach
description: "批量消息发送、定时消息发送、定时报告生成以及用于 WhatsApp 客户群管理的自定义群组功能。适用场景包括：批量发送消息、广播消息、定时发送消息/报告、使用 Cron 任务进行自动化操作、创建自定义群组、以及实现安全可靠的消息发送（避免被屏蔽）。"
source: "MoltFlow Team"
version: "2.15.1"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
**MoltFlow** — 专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化WhatsApp消息发送。

**由于需求量大以及近期出现的注册问题，我们特别推出顶级商务计划：每月仅需19.90美元（按年计费），且配额无限——此优惠仅限限时优惠。** [立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)  
**还提供免费试用计划。** [立即注册](https://molt.waiflow.app/checkout?plan=free)

# MoltFlow 功能概述  
- **批量发送消息**：支持安全发送机制，可向自定义联系人列表广播消息。  
- **定时发送消息**：支持时间区设置，可定时发送重复消息。  
- **生成报告**：自动生成包含发送结果的报告。  
- **自定义联系人组**：便于管理目标联系人群体。  

## 实际应用场景：  
- **健身房老板**：向所有会员发送“新年快乐”促销信息，并附上折扣码，同时避免被WhatsApp封禁。  
- **自由职业顾问**：每周五下午5点向活跃客户发送“周末可用性”通知。  
- **营销机构**：整合多个WhatsApp群组，生成唯一联系人列表，并发送产品发布公告。  
- **连锁餐厅**：每周生成预订确认情况报告，并通过WhatsApp发送给相关人员。  

## 使用场景：  
- 批量发送消息  
- 定时发送消息  
- 生成报告  
- 创建联系人列表  
- 暂停批量发送  
- 将联系人导出为CSV  
- 设置定时任务  

## 先决条件：  
1. **MOLTFLOW_API_KEY**：需在[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。  
2. 至少连接一个可使用的WhatsApp会话（状态为“working”）。  
3. 基础URL：`https://apiv2.waiflow.app/api/v2`  

## 所需API权限：  
| 权限范围 | 访问权限 |  
|--------|--------|  
| `custom-groups` | `读取/管理` |  
| `bulk-send` | `读取/管理` |  
| `scheduled` | `读取/管理` |  
| `reports` | `读取/管理` |  

## 认证方式：  
每个请求必须包含以下认证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

---

## 自定义联系人组  
用于批量发送和定时发送消息。自定义联系人组属于MoltFlow的内部管理工具，而非WhatsApp群组。  

**操作方式：**  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/custom-groups` | 查看所有自定义联系人组 |  
| POST | `/custom-groups` | 创建新的自定义联系人组（可选包含初始成员） |  
| GET | `/custom-groups/contacts` | 查看所有跨会话的唯一联系人信息 |  
| GET | `/custom-groups/wa-groups` | 查看可用于导入的WhatsApp群组列表 |  
| POST | `/custom-groups/from-wa-groups` | 通过导入WhatsApp群组成员创建新组 |  
| GET | `/custom-groups/{id}` | 查看特定组的详细信息及成员列表 |  
| PATCH | `/custom-groups/{id}` | 更新组名 |  
| DELETE | `/custom-groups/{id}` | 删除组及所有成员 |  
| POST | `/custom-groups/{id}/members/add` | 添加成员（避免重复） |  
| POST | `/custom-groups/{id}/members/remove` | 通过电话号码删除成员 |  
| GET | `/custom-groups/{id}/export/csv` | 将成员信息导出为CSV |  
| GET | `/custom-groups/{id}/export/json` | 将成员信息导出为JSON |  

### 创建自定义联系人组  
**POST** `/custom-groups`  
（具体请求格式请参考**```json
{
  "name": "VIP Clients",
  "members": [
    {"phone": "+15550123456"},
    {"phone": "+15550987654", "name": "Jane Doe"}
  ]
}
```**）  

### 从WhatsApp群组创建自定义联系人组  
**POST** `/custom-groups/from-wa-groups`  
（具体请求格式请参考**```json
{
  "name": "Imported Leads",
  "wa_groups": [
    {"wa_group_id": "120363012345@g.us", "session_id": "session-uuid-..."},
    {"wa_group_id": "120363067890@g.us", "session_id": "session-uuid-..."}
  ]
}
```**）  

### 查看WhatsApp群组  
**GET** `/custom-groups/wa-groups`  
（具体请求格式请参考**```json
{
  "id": "group-uuid-...",
  "name": "VIP Clients",
  "member_count": 2,
  "created_at": "2026-02-12T10:00:00Z"
}
```**）  

### 添加成员  
**POST** `/custom-groups/{id}/members/add`  
（具体请求格式请参考**```json
{
  "contacts": [
    {"phone": "+15551112222"},
    {"phone": "+15553334444", "name": "Bob Smith"}
  ]
}
```**）  

### 导出成员信息  
**GET** `/custom-groups/{id}/export/csv` | 以CSV格式导出成员信息  
**GET** `/custom-groups/{id}/export/json` | 以JSON格式导出成员信息  

---

## 批量发送消息  
支持安全发送机制，可向自定义联系人组广播消息。消息发送之间会随机间隔30秒至2分钟，模拟人类发送消息的行为。  

**操作方式：**  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| POST | `/bulk-send` | 创建批量发送任务 |  
| GET | `/bulk-send` | 查看所有批量发送任务列表 |  
| GET | `/bulk-send/{id}` | 查看特定任务的详细信息及接收者列表 |  
| POST | `/bulk-send/{id}/pause` | 暂停正在运行的任务 |  
| POST | `/bulk-send/{id}/resume` | 恢复暂停的任务 |  
| POST | `/bulk-send/{id}/cancel` | 取消任务（释放未使用的配额） |  
| GET | `/bulk-send/{id}/progress` | 通过SSE实时获取任务进度 |  

**创建批量发送任务**  
**POST** `/bulk-send`  
（具体请求格式请参考**```json
{
  "session_id": "session-uuid-...",
  "custom_group_id": "custom-group-uuid-...",
  "message_content": "Special offer for our VIP clients!"
}
```**）  

### 实时进度更新  
**GET** `/bulk-send/{id}/progress`  
（具体请求格式请参考**```
data: {"sent": 45, "total": 127, "failed": 0, "status": "running"}
data: {"sent": 46, "total": 127, "failed": 0, "status": "running"}
```**）  

## 定时消息  
支持一次性或重复发送消息，支持时间区设置，并可完全控制消息的发送流程。  

**操作方式：**  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/scheduled-messages` | 查看所有定时任务列表 |  
| POST | `/scheduled-messages` | 创建新的定时任务（一次性或重复发送） |  
| GET | `/scheduled-messages/{id}` | 查看任务详情及执行历史记录 |  
| PATCH | `/scheduled-messages/{id}` | 更新任务设置或重新计算发送时间 |  
| POST | `/scheduled-messages/{id}/cancel` | 取消定时任务 |  
| POST | `/scheduled-messages/{id}/pause` | 暂停正在运行的任务 |  
| POST | `/scheduled-messages/{id}/resume` | 恢复暂停的任务 |  
| DELETE | `/scheduled-messages/{id}` | 删除已取消或已完成的任务 |  
| GET | `/scheduled-messages/{id}/history` | 查看任务执行历史记录（分页显示） |  

### 创建一次性定时任务  
**POST** `/scheduled-messages`  
（具体请求格式请参考**```json
{
  "name": "Follow-up",
  "session_id": "session-uuid-...",
  "custom_group_id": "custom-group-uuid-...",
  "schedule_type": "one_time",
  "message_content": "Just checking in on your order!",
  "scheduled_time": "2026-02-15T09:00:00",
  "timezone": "Asia/Jerusalem"
}
```**）  

### 创建重复发送任务（基于Cron表达式）  
**POST** `/scheduled-messages`  
（具体请求格式请参考**```json
{
  "name": "Weekly Update",
  "session_id": "session-uuid-...",
  "custom_group_id": "custom-group-uuid-...",
  "schedule_type": "cron",
  "message_content": "Weekly team report is ready!",
  "cron_expression": "0 9 * * MON",
  "timezone": "America/New_York"
}
```**）  

**注意：** 所有重复发送任务（`daily`、`weekly`、`monthly`、`cron`）都需要提供`cron_expression`。最小发送间隔为5分钟。  

## 定时报告  
可自动生成MoltFlow活动的报告，支持多种预建模板。报告可查看于控制台，也可直接发送至用户的WhatsApp会话。  

**设置方式：**  
将`delivery_method`设置为`"whatsapp"`，报告将以纯文本形式发送至用户的WhatsApp会话。  

**操作方式：**  
| 方法 | 端点 | 说明 |  
|--------|----------|-------------|  
| GET | `/reports/templates` | 查看所有可用报告模板 |  
| POST | `/reports` | 创建新的定时报告 |  
| GET | `/reports` | 查看所有报告列表 |  
| GET | `/reports/{id}` | 查看特定报告的详细信息及执行历史记录 |  
| PATCH | `/reports/{id}` | 更新报告设置 |  
| POST | `/reports/{id}/pause` | 暂停定时报告 |  
| POST | `/reports/{id}/resume` | 恢复暂停的报告 |  
| DELETE | `/reports/{id}` | 删除报告 |  

**报告模板**  
（具体请求格式请参考**```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/reports/templates
```**）  

**创建定时报告**  
**POST** `/reports`  
（具体请求格式请参考**```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Weekly Lead Pipeline",
    "template_id": "lead_pipeline",
    "schedule_type": "weekly",
    "cron_expression": "0 9 * * MON",
    "timezone": "America/New_York",
    "delivery_method": "whatsapp"
  }' \
  https://apiv2.waiflow.app/api/v2/reports
```**）  

**报告字段说明：**  
（具体字段说明请参考**```json
{
  "id": "report-uuid-...",
  "name": "Weekly Lead Pipeline",
  "template_id": "lead_pipeline",
  "schedule_type": "weekly",
  "cron_expression": "0 9 * * MON",
  "timezone": "America/New_York",
  "delivery_method": "whatsapp",
  "status": "active",
  "next_run_at": "2026-02-17T09:00:00-05:00",
  "created_at": "2026-02-13T10:00:00Z"
}
```**）  

## 计划限制：  
| 功能 | 免费版 | 起始版 | 专业版 | 商务版 |  
|--------|---------|---------|---------|----------|  
| 自定义联系人组 | 2个 | 5个 | 20个 | 100个 |  
| 批量发送 | 不支持 | 支持 | 支持 | 支持 |  
| 定时消息 | 不支持 | 支持 | 支持 | 支持 |  
| 定时报告 | 2个 | 5个 | 10个 | 无限 |  
| 每月消息发送量 | 50条 | 500条 | 1,500条 | 3,000条 |  

## 错误响应代码及含义：  
| 状态 | 含义 |  
|--------|---------|--------|---------|  
| 400 | 请求无效 |  
| 401 | 未经授权 |  
| 403 | 超过计划限制或功能限制 |  
| 404 | 资源未找到 |  
| 422 | 缺少必要字段 |  
| 429 | 发送频率受限 |  

## 相关服务：  
- **moltflow**：核心API（会话管理、消息发送、联系人组管理、Webhook等）  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作、CSV/JSON导出功能  
- **moltflow-ai**：基于AI的自动回复、语音转录等功能  
- **moltflow-a2a**：代理间通信协议、加密消息传输  
- **moltflow-reviews**：评论收集与评价管理  
- **moltflow-admin**：平台管理、用户管理、计划配置等