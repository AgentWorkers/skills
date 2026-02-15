---
name: moltflow-leads
description: "WhatsApp潜在客户检测与客户关系管理（CRM）流程：自动检测群组中的购买意向，跟踪潜在客户的状态，支持批量操作，以及CSV/JSON格式的数据导出。适用场景包括：潜在客户管理、潜在客户检测、流程管理、客户资格评估、转化过程、批量状态更新以及潜在客户数据导出。"
source: "MoltFlow Team"
version: "2.1.0"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---

> **MoltFlow** – 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。
> [年费订阅可节省高达 17% 的费用](https://molt.waiflow.app/checkout?plan=free) – 提供免费试用版，无需信用卡。

# MoltFlow 商机检测与客户关系管理（CRM）功能

自动检测来自被监控 WhatsApp 群组的潜在客户，通过销售流程跟踪这些客户，并将其数据导出到您的 CRM 系统中。

## 使用场景

- 查看潜在客户列表
- 更新潜在客户状态
- 批量更新潜在客户信息
- 将潜在客户添加到特定群组
- 将潜在客户数据导出为 CSV 或 JSON 格式
- 检查潜在客户是否已与您联系
- 按状态筛选潜在客户

## 前提条件

1. **MOLTFLOW_API_KEY** – 请从 [MoltFlow 仪表板](https://molt.waiflow.app) 的“设置” > “API 密钥”中生成。
2. 至少有一个启用了关键词检测功能的被监控 WhatsApp 群组。
3. 基本 API 地址：`https://apiv2.waiflow.app/api/v2`

## 所需 API 密钥权限

| 权限范围 | 访问权限 |
|---------|---------|
| `leads` | `读取/管理` |
| `groups` | `读取` |

## 认证

所有请求都必须包含以下认证信息之一：

```
Authorization: Bearer <jwt_token>
```

或

```
X-API-Key: <your_api_key>
```

---

## 潜在客户检测机制

1. 通过 `Groups API` 监控 WhatsApp 群组（详情请参阅 `moltflow` 技能文档）。
2. 设置 `monitor_mode: "keywords"`，并指定关键词（例如 `"looking for"`, `"price"`, `"interested"`）。
3. 当群组成员发送包含这些关键词的消息时，MoltFlow 会自动创建一个潜在客户记录。
4. 潜在客户记录会以 `new` 状态显示在 `leads` API 中，且触发关键词会被高亮显示。
5. 您可以跟踪这些潜在客户的状态变化：`new` -> `contacted` -> `qualified` -> `converted`。

---

## `leads` API

| 方法 | API 端点 | 功能描述 |
|--------|----------|-------------|
| GET | `/leads` | 查看潜在客户列表（可按状态、群组或关键词筛选） |
| GET | `/leads/{id}` | 获取潜在客户详情 |
| PATCH | `/leads/{id}/status` | 更新潜在客户状态 |
| GET | `/leads/{id}/reciprocity` | 检查潜在客户是否先与您联系（防垃圾信息功能） |
| POST | `/leads/bulk/status` | 批量更新潜在客户状态 |
| POST | `/leads/bulk/add-to-group` | 将潜在客户批量添加到指定群组 |
| GET | `/leads/export/csv` | 以 CSV 格式导出潜在客户数据（Pro+ 计划） |
| GET | `/leads/export/json` | 以 JSON 格式导出潜在客户数据（Pro+ 计划） |

### 查看潜在客户列表

**GET** `/leads`

查询参数：

| 参数 | 类型 | 描述 |
|---------|------|-------------|
| `status` | 字符串 | 按状态筛选（`new`, `contacted`, `qualified`, `converted`, `lost`） |
| `source_group_id` | UUID | 按来源群组筛选 |
| `search` | 字符串 | 按联系人姓名、电话号码或关键词搜索 |
| `limit` | 整数 | 每页显示数量（默认 50 条） |
| `offset` | 整数 | 分页偏移量 |

**响应** `200 OK`:

```json
{
  "leads": [
    {
      "id": "lead-uuid-...",
      "contact_phone": "+15550123456",
      "contact_name": "John D.",
      "lead_status": "new",
      "lead_score": 0,
      "lead_detected_at": "2026-02-12T14:30:00Z",
      "source_group": {
        "id": "group-uuid-...",
        "name": "Real Estate IL"
      },
      "trigger": {
        "matched_keyword": "interested in buying",
        "message_preview": "Hi, I'm interested in buying a 3-bedroom...",
        "monitor_mode": "keywords",
        "detected_at": "2026-02-12T14:30:00Z"
      }
    }
  ],
  "total": 47,
  "limit": 50,
  "offset": 0
}
```

### 获取潜在客户详情

**GET** `/leads/{id}`

返回潜在客户的完整信息，包括群组背景、检测元数据、消息数量和状态。

### 更新潜在客户状态

**PATCH** `/leads/{id}/status`

```json
{
  "status": "contacted"
}
```

**状态转换规则**：

- `new` -> `contacted`, `qualified`, `converted`, `lost`
- `contacted` -> `qualified`, `converted`, `lost`
- `qualified` -> `converted`, `lost`
- `converted` -> （达到最终状态，无法再转换）
- `lost` -> `new`（仅可重新开启检测）

无效的状态转换会导致 `400 Bad Request` 错误。

### 检查潜在客户是否已与您联系

**GET** `/leads/{id}/reciprocity?session_id-session-uuid`

`session_id` 是必填参数，用于指定要检查的 WhatsApp 会话。

```json
{
  "lead_id": "lead-uuid-...",
  "has_messaged_first": true,
  "last_inbound_at": "2026-02-12T15:00:00Z"
}
```

**注意事项**：
在主动联系潜在客户之前，请先确认他们是否已与您联系。否则，发送冷邮件可能会触发 WhatsApp 的垃圾信息检测机制。

### 批量更新潜在客户状态

**POST** `/leads/bulk/status`

```json
{
  "lead_ids": ["uuid1", "uuid2", "uuid3"],
  "status": "contacted"
}
```

**响应** `200 OK`:

```json
{
  "updated": 3,
  "failed": 0,
  "errors": []
}
```

每个潜在客户的状态转换都会经过验证。状态转换无效的记录会出现在错误信息中，但不会影响其他潜在客户的处理。

### 将潜在客户批量添加到群组

**POST** `/leads/bulk/add-to-group`

```json
{
  "lead_ids": ["uuid1", "uuid2"],
  "custom_group_id": "custom-group-uuid-..."
}
```

将潜在客户的电话号码添加到指定群组，以便后续使用批量发送或定时消息功能。

### 导出潜在客户数据

**GET** `/leads/export/csv` – 以 CSV 格式导出数据
**GET** `/leads/export/json` – 以 JSON 格式导出数据

支持以下筛选条件：`status`, `source_group_id`, `search`。每次导出最多 10,000 条记录。

**仅限 Pro+ 计划使用。**

---

## 示例流程

### 完整工作流程：检测 -> 评估 -> 主动联系

```bash
# 1. List new leads from a specific group
curl "https://apiv2.waiflow.app/api/v2/leads?status=new&source_group_id=group-uuid" \
  -H "X-API-Key: $MOLTFLOW_API_KEY"

# 2. Check reciprocity before reaching out
curl "https://apiv2.waiflow.app/api/v2/leads/{lead_id}/reciprocity?session_id=session-uuid" \
  -H "X-API-Key: $MOLTFLOW_API_KEY"

# 3. Update status to contacted
curl -X PATCH https://apiv2.waiflow.app/api/v2/leads/{lead_id}/status \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "contacted"}'

# 4. Bulk add qualified leads to a custom group for follow-up
curl -X POST https://apiv2.waiflow.app/api/v2/leads/bulk/add-to-group \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_ids": ["uuid1", "uuid2", "uuid3"],
    "custom_group_id": "follow-up-group-uuid"
  }'

# 5. Export all converted leads as CSV
curl "https://apiv2.waiflow.app/api/v2/leads/export/csv?status=converted" \
  -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -o converted-leads.csv
```

---

## 计划费用

| 功能 | 免费版 | 起始版 | Pro 计划 | Business 计划 |
|---------|------|---------|-----|----------|
| 潜在客户检测 | 支持（2 个群组） | 支持（5 个群组） | 支持（20 个群组） | 支持（100 个群组） |
| 潜在客户列表及详情 | 支持 | 支持 | 支持 | 支持 |
| 状态更新 | 支持 | 支持 | 支持 | 支持 |
| 批量操作 | 不支持 | 不支持 | 支持 | 支持 |
| CSV/JSON 导出 | 不支持 | 不支持 | 支持 | 支持 |

---

## 错误响应

| 状态码 | 含义 |
|--------|---------|
| 400 | 状态转换无效或请求错误 |
| 401 | 未经授权（认证信息缺失或无效） |
| 403 | 超出计划限制或功能限制 |
| 404 | 未找到潜在客户 |
| 429 | 请求频率限制 |

---

## 相关工具

- **moltflow** – 核心 API：会话管理、消息发送、群组管理、标签设置、Webhook 配置
- **moltflow-outreach** – 批量发送消息、定时消息、自定义群组管理
- **moltflow-ai** – 基于 AI 的自动回复功能、语音转录、问答系统、风格分析
- **moltflow-a2a** | 代理间通信协议、加密消息传输、内容策略管理
- **moltflow-reviews** | 评论收集与评价管理 |
- **moltflow-admin** | 平台管理、用户管理、计划配置