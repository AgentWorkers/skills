---
name: moltflow-outreach
description: "**WhatsApp群发功能：批量消息发送、定时消息、自定义群组**  
**适用场景：**  
- 批量发送消息  
- 广播通知  
- 定时发送消息  
- 使用Cron任务进行自动化操作  
- 自定义消息发送对象（群组）  
- 安全地与联系人列表中的成员进行消息交流  

**主要功能：**  
1. **批量消息发送**：一次性向大量联系人发送相同或不同的消息。  
2. **定时消息**：设置消息发送的时间和频率，确保消息在指定时间点到达收件人手中。  
3. **自定义群组**：根据需要创建或管理特定的消息接收群组。  
4. **联系人列表支持**：支持从现有的联系人列表中选择目标接收者。  
5. **安全机制**：确保消息发送过程的安全性，避免未经授权的访问或滥用。  

**实用建议：**  
- 根据业务需求灵活使用这些功能，提高消息传递的效率和质量。  
- 定期更新WhatsApp的官方文档以了解最新的功能更新和最佳实践。"
source: "MoltFlow Team"
version: "2.1.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

> **MoltFlow**——专为团队设计的WhatsApp Business自动化工具。支持大规模连接、监控和自动化WhatsApp消息发送。
> [年费订阅可节省高达17%的费用](https://molt.waiflow.app/checkout?plan=free)——提供免费试用版，无需信用卡。

# MoltFlow功能概述——批量发送、定时消息与自定义联系人组

- 支持向自定义联系人列表批量发送消息，并具备防封禁的发送策略；
- 可设置定时消息，支持时区调整；
- 支持管理用于WhatsApp推广的目标联系人组。

## 使用场景

- 批量发送消息或向特定群组广播；
- 安排WhatsApp消息的发送时间；
- 创建新的联系人列表或自定义联系人组；
- 暂停或取消批量发送操作；
- 将联系人组成员导出为CSV文件或导入新的联系人数据；
- 发送每周更新信息或设置定时任务。

## 前提条件

1. **MOLTFLOW_API_KEY**——需从[MoltFlow控制台](https://molt.waiflow.app)的“设置”>“API密钥”中生成；
- 至少有一个已连接的WhatsApp会话（状态为“working”）；
- 基础URL：`https://apiv2.waiflow.app/api/v2`。

## 所需API密钥权限

| 权限范围 | 访问权限 |
|---------|-----------|
| `custom-groups` | `读取/管理` |
| `bulk-send` | `读取/管理` |
| `scheduled` | `读取/管理` |

## 认证方式

所有请求必须包含以下认证信息之一：

```
Authorization: Bearer <jwt_token>
```

或

```
X-API-Key: <your_api_key>
```

---

## 自定义联系人组

- 用于批量发送和定时消息的目标联系人列表。自定义联系人组是MoltFlow的内部管理工具，而非WhatsApp的群组。

| 方法 | 端点 | 功能描述 |
|--------|---------|-------------------|
| GET | `/custom-groups` | 列出所有自定义联系人组 |
| POST | `/custom-groups` | 创建新的联系人组（可选包含初始成员） |
| GET | `/custom-groups/contacts` | 列出所有跨会话的唯一联系人信息 |
| GET | `/custom-groups/wa-groups` | 列出可供导入的WhatsApp群组 |
| POST | `/custom-groups/from-wa-groups` | 通过导入WhatsApp群组成员来创建新的自定义联系人组 |
| GET | `/custom-groups/{id}` | 查看指定联系人组的详细信息及成员列表 |
| PATCH | `/custom-groups/{id}` | 更新联系人组名称 |
| DELETE | `/custom-groups/{id}` | 删除联系人组及其所有成员 |
| POST | `/custom-groups/{id}/members/add` | 向联系人组添加成员（避免重复） |
| POST | `/custom-groups/{id}/members/remove` | 根据电话号码删除联系人组成员 |
| GET | `/custom-groups/{id}/export/csv` | 将联系人组成员导出为CSV文件 |
| GET | `/custom-groups/{id}/export/json` | 将联系人组成员导出为JSON格式 |

### 创建自定义联系人组

**POST** `/custom-groups`

```json
{
  "name": "VIP Clients",
  "members": [
    {"phone": "+15550123456"},
    {"phone": "+15550987654", "name": "Jane Doe"}
  ]
}
```

`members`参数是一个对象数组，其中`phone`字段为必填项，`name`字段为可选项。省略`members`参数可创建一个空联系人组。

### 从WhatsApp群组创建自定义联系人组

**POST** `/custom-groups/from-wa-groups`

```json
{
  "name": "Imported Leads",
  "wa_groups": [
    {"wa_group_id": "120363012345@g.us", "session_id": "session-uuid-..."},
    {"wa_group_id": "120363067890@g.us", "session_id": "session-uuid-..."}
  ]
}
```

- 从每个WhatsApp群组中提取成员信息，通过电话号码去重后生成新的自定义联系人组。

### 列出所有WhatsApp群组

**GET** `/custom-groups/wa-groups`

- 显示所有已连接的WhatsApp群组及其成员数量，便于选择合适的群组进行导入。

**响应状态码** `201 Created` 表示操作成功。

```json
{
  "id": "group-uuid-...",
  "name": "VIP Clients",
  "member_count": 2,
  "created_at": "2026-02-12T10:00:00Z"
}
```

### 添加联系人组成员

**POST** `/custom-groups/{id}/members/add`

```json
{
  "contacts": [
    {"phone": "+15551112222"},
    {"phone": "+15553334444", "name": "Bob Smith"}
  ]
}
```

每个联系人对象包含`phone`（必填）和`name`（可选）字段。每次请求最多可添加1,000个成员，重复成员会被自动忽略。

### 导出联系人组成员

**GET** `/custom-groups/{id}/export/csv` | 以CSV格式导出成员信息 |
**GET** `/custom-groups/{id}/export/json` | 以JSON格式导出成员信息 |

---

## 批量发送消息

- 支持向自定义联系人组批量发送消息，并具备防封禁的发送策略；
- 消息发送之间会随机间隔30秒至2分钟，以模拟真实用户行为。

| 方法 | 端点 | 功能描述 |
|--------|---------|-------------------|
| POST | `/bulk-send` | 创建批量发送任务（会消耗相应的发送配额） |
| GET | `/bulk-send` | 查看所有已创建的批量发送任务 |
| GET | `/bulk-send/{id}` | 查看特定任务的详细信息及接收者列表 |
| POST | `/bulk-send/{id}/pause` | 暂停正在执行的批量发送任务 |
| POST | `/bulk-send/{id}/resume` | 恢复暂停的任务 |
| POST | `/bulk-send/{id}/cancel` | 取消批量发送任务（释放未使用的配额） |
| GET | `/bulk-send/{id}/progress` | 通过SSE协议实时获取任务进度 |

### 创建批量发送任务

**POST** `/bulk-send`

```json
{
  "session_id": "session-uuid-...",
  "custom_group_id": "custom-group-uuid-...",
  "message_content": "Special offer for our VIP clients!"
}
```

| 参数 | 类型 | 是否必填 | 功能描述 |
|-------|--------|---------------------------|
| `session_id` | UUID | 是 | 指定用于发送消息的WhatsApp会话 |
| `custom_group_id` | UUID | 是 | 目标自定义联系人组ID |
| `message_type` | 字符串 | 否 | 消息类型（默认为“text”或“media”） |
| `message_content` | 字符串 | 可选 | 消息内容（最多4096个字符）。如未提供`media_url`则必填 |
| `media_url` | 字符串 | 可选 | 媒体文件的HTTP(S)链接。如未提供`message_content`则必填 |

**响应状态码** `201 Created` 表示任务创建成功。

### 实时跟踪任务进度

**GET** `/bulk-send/{id}/progress`

- 通过SSE协议实时获取任务发送进度更新。

---

## 定时消息

- 支持向自定义联系人组发送一次性或定期消息，并支持时区设置及完整的任务管理功能。

| 方法 | 端点 | 功能描述 |
|--------|---------|-------------------|
| GET | `/scheduled-messages` | 列出所有已安排的定时消息 |
| POST | `/scheduled-messages` | 创建新的定时任务（一次性或定期） |
| GET | `/scheduled-messages/{id}` | 查看特定任务的详细信息及执行历史记录 |
| PATCH | `/scheduled-messages/{id}` | 更新定时任务设置并重新计算下次执行时间 |
| POST | `/scheduled-messages/{id}/cancel` | 取消定时任务 |
| POST | `/scheduled-messages/{id}/pause` | 暂停正在执行的定时任务 |
| POST | `/scheduled-messages/{id}/resume` | 恢复暂停的定时任务 |
| DELETE | `/scheduled-messages/{id}` | 删除已取消或已完成的定时任务 |
| GET | `/scheduled-messages/{id}/history` | 分页查看任务执行历史记录 |

### 创建一次性定时任务

**POST** `/scheduled-messages`

```json
{
  "name": "Follow-up",
  "session_id": "session-uuid-...",
  "custom_group_id": "custom-group-uuid-...",
  "schedule_type": "one_time",
  "message_content": "Just checking in on your order!",
  "scheduled_time": "2026-02-15T09:00:00",
  "timezone": "Asia/Jerusalem"
}
```

### 创建定期任务（使用cron表达式）

**POST** `/scheduled-messages`

```json
{
  "name": "Weekly Update",
  "session_id": "session-uuid-...",
  "custom_group_id": "custom-group-uuid-...",
  "schedule_type": "cron",
  "message_content": "Weekly team report is ready!",
  "cron_expression": "0 9 * * MON",
  "timezone": "America/New_York"
}
```

**响应状态码** `201 Created` 表示任务创建成功。

### 定时任务类型

- `one_time` | 在指定时间点发送一次 |
- `daily` | 每天发送 |
- `weekly` | 每周发送 |
- `monthly` | 每月发送 |
- `cron` | 使用自定义cron表达式（例如：`0 9 * * MON-FRI`）

**注意：** 所有定期任务类型（`daily`、`weekly`、`monthly`、`cron`）都需要提供`cron_expression`。最小发送间隔为5分钟。

### 必需字段

| 参数 | 类型 | 是否必填 | 功能描述 |
|-------|--------|-------------------------|
| `name` | 字符串 | 是 | 任务名称（1-255个字符） |
| `session_id` | UUID | 是 | 用于发送消息的WhatsApp会话ID |
| `custom_group_id` | UUID | 是 | 目标自定义联系人组ID |
| `schedule_type` | 字符串 | 是 | 任务类型（`one_time`、`daily`、`weekly`、`monthly`、`cron`之一） |
| `message_type` | 字符串 | 可选 | 消息类型（`text`或`media`） |
| `message_content` | 字符串 | 可选 | 消息内容（最多4096个字符）。如未提供`media_url`则必填 |
| `media_url` | 字符串 | 可选 | 媒体文件的HTTP(S)链接。如未提供`message_content`则必填 |
| `scheduled_time` | datetime | 可选 | 发送时间（ISO 8601格式）。仅适用于`one_time`类型 |
| `cron_expression` | 字符串 | 可选 | 定时任务的cron表达式。仅适用于定期任务类型 |

### 定时任务状态

- `active` | 正在运行 |
- `paused` | 暂停 |
- `cancelled` | 已取消 |
- `completed` | 已完成 |

---

## 示例用法

- **完整工作流程**：创建自定义联系人组 → 批量发送消息 → 设置定时任务。

```bash
# 1. Create a custom group
curl -X POST https://apiv2.waiflow.app/api/v2/custom-groups \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "VIP Clients"}'

# 2. Add members to the group
curl -X POST https://apiv2.waiflow.app/api/v2/custom-groups/{group_id}/members/add \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"contacts": [{"phone": "+15550123456"}, {"phone": "+15550987654"}, {"phone": "+15551112222"}]}'

# 3. Bulk send to the group
curl -X POST https://apiv2.waiflow.app/api/v2/bulk-send \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "session-uuid-...",
    "custom_group_id": "group-uuid-...",
    "message_content": "Exclusive offer for our VIP clients!"
  }'

# 4. Schedule a weekly follow-up to the group
curl -X POST https://apiv2.waiflow.app/api/v2/scheduled-messages \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Weekly VIP Update",
    "session_id": "session-uuid-...",
    "custom_group_id": "group-uuid-...",
    "schedule_type": "cron",
    "message_content": "Weekly report is ready!",
    "cron_expression": "0 9 * * MON",
    "timezone": "Asia/Jerusalem"
  }'
```

### 暂停和恢复批量发送操作

```bash
# Pause
curl -X POST https://apiv2.waiflow.app/api/v2/bulk-send/{job_id}/pause \
  -H "X-API-Key: $MOLTFLOW_API_KEY"

# Resume
curl -X POST https://apiv2.waiflow.app/api/v2/bulk-send/{job_id}/resume \
  -H "X-API-Key: $MOLTFLOW_API_KEY"
```

### 导出联系人组成员

```bash
curl https://apiv2.waiflow.app/api/v2/custom-groups/{group_id}/export/csv \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -o vip-clients.csv
```

---

## 计划使用限制

| 功能 | 免费版 | 起始版 | 专业版 | 商业版 |
|---------|--------|------------------|-------------------------|
| 自定义联系人组 | 2个 | 5个 | 20个 | 100个 |
| 批量发送 | 不支持 | 支持 | 支持 |
| 定时消息 | 不支持 | 支持 | 支持 |
| 每月消息发送量 | 50条 | 500条 | 1,500条 | 3,000条 |

---

## 错误响应代码及含义

| 状态码 | 错误原因 |
|--------|-------------------|
| 400 | 请求无效 |
| 401 | 未经授权（缺少或无效的认证信息） |
| 403 | 超过使用限制或功能受限 |
| 404 | 资源未找到 |
| 422 | 需要填写的字段缺失 |
| 429 | 发送频率超出限制 |

---

## 相关服务

- **moltflow**：核心API接口，包括会话管理、消息发送、联系人组管理、标签设置、Webhook集成等 |
- **moltflow-leads**：用于潜在客户检测、任务跟踪、批量操作、CSV/JSON数据导出等功能 |
- **moltflow-ai**：提供智能自动回复、语音转录、问答系统（RAG）等功能 |
- **moltflow-a2a**：支持代理间安全通信、加密消息传输及内容策略管理 |
- **moltflow-reviews**：用于收集用户评价和管理用户反馈 |
- **moltflow-admin**：平台管理工具，包括用户管理和计划配置等。