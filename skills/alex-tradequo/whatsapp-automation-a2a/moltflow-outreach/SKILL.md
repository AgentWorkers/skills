---
name: moltflow-outreach
description: "批量消息发送、定时消息发送、定时报告生成以及用于 WhatsApp 客户群管理的自定义群组功能。适用场景包括：批量发送消息、广播消息、定时发送消息/报告、使用 Cron 任务进行自动化操作、创建自定义群组、以及实现安全可靠的消息传递（避免被屏蔽）。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
## MoltFlow – 面向团队的WhatsApp商务自动化工具  
**MoltFlow**能够帮助您高效地连接、监控并自动化大规模的WhatsApp消息发送。**由于需求旺盛以及近期出现的注册问题，我们特推出顶级商务计划：每月仅需19.90美元（按年计费），即可享受无限发送量——此优惠仅限短时间内有效。**[立即抢购](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)！**同时，我们还提供免费试用计划。**[立即注册](https://molt.waiflow.app/checkout?plan=free)。

### 主要功能  
- **批量发送**：支持安全发送机制，可向自定义联系人列表广播消息。  
- **定时消息**：支持时间区设置，可定时向联系人发送消息。  
- **报告生成**：自动生成包含发送结果的报告。  
- **自定义联系人组**：便于您管理目标联系人群组。

### 实际应用场景  
- **健身房老板**：可向所有会员发送新年祝福信息，并附赠折扣码，同时避免被WhatsApp封禁。  
- **自由职业顾问**：每周五下午向活跃客户发送周末可用性通知。  
- **营销机构**：可整合多个WhatsApp群组的数据，生成统一的联系人列表并发送产品发布公告。  

### 使用场景  
- 批量发送消息  
- 安排WhatsApp消息  
- 生成报告  
- 创建联系人列表  
- 暂停批量发送  
- 将联系人导出为CSV文件  
- 设置定时任务  

### 先决条件  
1. **MOLTFLOW_API_KEY**：需从[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成。  
2. 至少已连接一个可使用的WhatsApp会话（状态为“working”）。  
3. 基础URL：`https://apiv2.waiflow.app/api/v2`  

### 所需API密钥权限  
| 权限范围 | 访问权限 |  
|---------|---------|  
| `custom-groups` | `读取/管理` |  
| `bulk-send` | `读取/管理` |  
| `scheduled` | `读取/管理` |  
| `reports` | `读取/管理` |  

### 认证要求  
每个请求都必须包含以下认证信息之一：  
```
Authorization: Bearer <jwt_token>
```  
或  
```
X-API-Key: <your_api_key>
```  

---

### 自定义联系人组  
**自定义联系人组**用于批量发送和定时消息。这些组是MoltFlow内部的联系人列表，而非实际的WhatsApp群组。  

- **操作方法**：  
  - **GET** `/custom-groups`：列出所有自定义组。  
  - **POST** `/custom-groups`：创建新组（可选包含初始成员）。  
  - **GET** `/custom-groups/contacts`：列出所有跨会话的唯一联系人。  
  - **GET** `/custom-groups/wa-groups`：列出可用于导入的WhatsApp群组。  
  - **POST** `/custom-groups/from-wa-groups`：通过导入WhatsApp群组成员创建新组。  
  - **GET** `/custom-groups/{id}`：查看组详情及成员信息。  
  - **PATCH** `/custom-groups/{id}`：更新组名。  
  - **DELETE** `/custom-groups/{id}`：删除组及所有成员。  
  - **POST** `/custom-groups/{id}/members/add`：添加成员（避免重复）。  
  - **POST** `/custom-groups/{id}/members/remove`：按电话号码删除成员。  
  - **GET** `/custom-groups/{id}/export/csv`：将成员导出为CSV文件。  
  - **GET** `/custom-groups/{id}/export/json`：将成员导出为JSON文件。  

#### 创建自定义组  
**POST** `/custom-groups`  
（具体请求格式请参考**```json
{
  "name": "VIP Clients",
  "members": [
    {"phone": "+15550123456"},
    {"phone": "+15550987654", "name": "Jane Doe"}
  ]
}
```**。）  

#### 从WhatsApp群组创建自定义组  
**POST** `/custom-groups/from-wa-groups`  
（具体请求格式请参考**```json
{
  "name": "Imported Leads",
  "wa_groups": [
    {"wa_group_id": "120363012345@g.us", "session_id": "session-uuid-..."},
    {"wa_group_id": "120363067890@g.us", "session_id": "session-uuid-..."}
  ]
}
```**。）  

#### 列出WhatsApp群组  
**GET** `/custom-groups/wa-groups`  
（返回所有已连接会话中的WhatsApp群组及其成员数量。）  

#### 添加成员  
**POST** `/custom-groups/{id}/members/add`  
（每个联系人对象包含`phone`（必填）和`name`（可选）字段。每次请求最多添加1,000个成员，重复成员会被自动忽略。）  

#### 导出成员  
**GET** `/custom-groups/{id}/export/csv`：将成员信息导出为CSV文件。  
**GET** `/custom-groups/{id}/export/json`：将成员信息导出为JSON数组。  

#### 批量发送  
**POST** `/bulk-send`  
（用于批量发送消息，支持安全发送机制。发送间隔随机设置为30秒至2分钟，模拟人类行为。）  
- **字段**：  
  - `session_id`：发送消息的WhatsApp会话ID。  
  - `custom_group_id`：目标自定义组ID。  
  - `message_type`：消息类型（`text`或`media`）。  
  - `message_content`：消息内容（最多4096个字符）。  
  - `media_url`：媒体文件的HTTP(S)链接（如提供媒体文件时使用）。  

#### 监控发送进度  
**GET** `/bulk-send/{id}/progress`  
（实时显示发送进度。）  

#### 定时消息  
**POST** `/scheduled-messages`  
（用于安排一次性或定期发送消息。支持时间区设置和完整的任务管理功能。）  
- **字段**：  
  - `name`：任务名称。  
  - `session_id`：发送消息的WhatsApp会话ID。  
  - `custom_group_id`：目标自定义组ID。  
  - `schedule_type`：发送类型（`one_time`、`daily`、`weekly`、`monthly`或`cron`）。  
  - `cron_expression`：定时表达式（用于重复发送）。  

#### 报告生成  
**POST** `/reports`  
（可生成关于MoltFlow活动的报告。支持多种报告模板，可查看或直接发送到用户的WhatsApp会话中。）  
- **字段**：  
  - `name`：报告名称。  
  - `schedule_type`：发送类型。  
  - `delivery_method`：报告发送方式（`dashboard`或`whatsapp`）。  

---

### 示例流程  
- **完整流程**：创建自定义组 → 批量发送 → 安排定时消息。  

### 操作示例  
- **暂停和恢复批量发送**。  
- **导出联系人组成员**。  

### 计划限制  
| 功能 | 免费版 | 起始版 | 专业版 | 商务版 |  
|---------|---------|---------|---------|----------|  
| 自定义联系人组 | 2个 | 5个 | 20个 | 100个 |  
| 批量发送 | 否 | 是 | 是 | 是 |  
| 定时消息 | 否 | 是 | 是 | 是 |  
| 定时报告 | 2个 | 5个 | 10个 | 无限 |  
| 每月消息发送量 | 50条 | 500条 | 1,500条 | 3,000条 |  

### 错误响应  
| 状态码 | 含义 |  
|---------|---------|  
| 400 | 请求无效。  
| 401 | 未经授权。  
| 403 | 超过计划限制或功能受限。  
| 404 | 资源未找到。  
| 422 | 需要填写的字段缺失。  
| 429 | 发送频率受限。  

### 相关服务  
- **moltflow**：核心API（会话管理、消息发送、联系人组等）。  
- **moltflow-leads**：潜在客户检测、流程跟踪、批量操作等。  
- **moltflow-ai**：智能自动回复、语音转录等功能。  
- **moltflow-a2a**：代理间通信协议、加密消息传输等。  
- **moltflow-reviews**：评论收集与评价管理。  
- **moltflow-admin**：平台管理、用户管理及计划配置等。