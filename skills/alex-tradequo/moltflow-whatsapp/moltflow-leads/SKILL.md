---
name: moltflow-leads
description: "WhatsApp潜在客户检测与CRM流程：在群组中识别购买意向信号，跟踪潜在客户的状态，支持批量操作，并支持CSV/JSON格式的数据导出。适用于以下场景：潜在客户管理、潜在客户检测、流程自动化、客户资格评估、客户转化以及批量状态更新和数据导出。"
source: "MoltFlow Team"
version: "2.11.8"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
> **MoltFlow** — 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。
> ***由于需求旺盛以及近期出现的注册问题，我们正在限时优惠中，以每月 19.90 美元的价格提供顶级 Business 计划，该计划包含无限使用量。*** [**立即抢购**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)
> 免费试用计划也可使用。[**立即注册**](https://molt.waiflow.app/checkout?plan=free)

# MoltFlow — 销售线索检测与客户关系管理（CRM）系统

该系统能够从被监控的 WhatsApp 群组中检测购买意向信号，追踪销售线索，并将其导入您的 CRM 系统。

## 使用场景

- 查看销售线索列表
- 更新线索状态
- 批量更新线索状态
- 将线索添加到特定群组
- 将线索导出为 CSV 或 JSON 格式
- 检查线索是否已与您联系
- 按状态筛选线索

## 先决条件

1. **MOLTFLOW_API_KEY** — 请在 [MoltFlow 控制台](https://molt.waiflow.app) 的 “设置” > “API 密钥” 中生成
2. 至少有一个已启用关键词检测功能的 WhatsApp 群组
3. 基本 API 地址：`https://apiv2.waiflow.app/api/v2`

## 所需 API 密钥权限

| 权限范围 | 访问权限 |
|-------|--------|
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

## 销售线索检测机制

1. 通过 Groups API 监控 WhatsApp 群组（详见 `moltflow` 技能文档）
2. 设置 `monitor_mode: "keywords"`，并指定关键词（例如 `"looking for"`, `"price"`, `"interested"`）
3. 当群组成员发送包含这些关键词的消息时，MoltFlow 会自动创建一条销售线索
4. 新生成的线索会在 Leads API 中显示，状态为 `new`，且触发关键词会被高亮显示
5. 您可以跟踪线索的状态变化：`new` -> `contacted` -> `qualified` -> `converted`

---

## Leads API

| 方法 | API 端点 | 功能描述 |
|--------|----------|-------------|
| GET | `/leads` | 查看销售线索列表（可按状态、群组或关键词筛选） |
| GET | `/leads/{id}` | 获取单条线索的详细信息 |
| PATCH | `/leads/{id}/status` | 更新线索状态 |
| GET | `/leads/{id}/reciprocity` | 检查线索是否先与您联系（防止垃圾邮件） |
| POST | `/leads/bulk/status` | 批量更新线索状态 |
| POST | `/leads/bulk/add-to-group` | 将多条线索批量添加到指定群组 |
| GET | `/leads/export/csv` | 以 CSV 格式导出线索（Pro+ 计划用户可导出最多 10,000 条） |
| GET | `/leads/export/json` | 以 JSON 格式导出线索（Pro+ 计划用户可导出最多 10,000 条） |

### 查看销售线索列表

**GET** `/leads`

查询参数：

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
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

### 获取销售线索详细信息

**GET** `/leads/{id}`

返回包括群组信息、检测元数据、消息数量和状态在内的完整线索详情。

### 更新销售线索状态

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
- `lost` -> `new`（仅可重新开始检测）

无效的状态转换会导致 `400 Bad Request` 错误。

### 检查线索是否已与您联系

**GET** `/leads/{id}/reciprocity?session_id-session-uuid`

`session_id` 参数是必填项，用于指定要检查的 WhatsApp 会话。

```json
{
  "lead_id": "lead-uuid-...",
  "has_messaged_first": true,
  "last_inbound_at": "2026-02-12T15:00:00Z"
}
```

**注意事项**：

在主动联系销售线索之前，请先确认该线索是否已与您联系，否则发送冷邮件可能会触发 WhatsApp 的垃圾邮件检测机制。

### 批量更新线索状态

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

系统会逐一验证每条线索的状态转换是否合法。状态转换不合法的线索会被记录在错误日志中，但不会影响其他线索的处理。

### 将线索批量添加到群组

**POST** `/leads/bulk/add-to-group`

```json
{
  "lead_ids": ["uuid1", "uuid2"],
  "custom_group_id": "custom-group-uuid-..."
}
```

将线索的电话号码添加到指定群组，以便后续使用批量发送或定时发送消息功能。

### 导出线索

**GET** `/leads/export/csv` — 以 CSV 格式导出线索列表
**GET** `/leads/export/json` — 以 JSON 格式导出线索列表

支持按 `status`, `source_group_id`, `search` 参数进行筛选。每次导出最多支持 10,000 条线索。

**仅限 Pro+ 计划用户使用。**

---

## 示例流程

### 完整工作流程：检测 -> 评估线索 -> 主动联系

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

## 计划费用对比

| 功能 | 免费计划 | 起始计划 | Pro 计划 | Business 计划 |
|---------|------|---------|-----|----------|
| 销售线索检测 | 支持（2 个群组） | 支持（5 个群组） | 支持（20 个群组） | 支持（100 个群组） |
| 销售线索列表及详情 | 支持 | 支持 | 支持 | 支持 |
| 状态更新 | 支持 | 支持 | 支持 | 支持 |
| 批量操作 | 不支持 | 不支持 | 支持 | 支持 |
| CSV/JSON 导出 | 不支持 | 不支持 | 支持 | 支持 |

---

## 错误代码及含义

| 状态码 | 含义 |
|--------|---------|
| 400 | 状态转换无效或请求错误 |
| 401 | 未经授权（认证信息缺失或无效） |
| 403 | 超出计划使用限制或功能限制 |
| 404 | 未找到对应的销售线索 |
| 429 | 请求频率受限 |

---

## 相关工具

- **moltflow** — 核心 API：会话管理、消息发送、群组管理、标签设置、Webhook 配置
- **moltflow-outreach** — 批量发送消息、定时发送消息、自定义群组管理
- **moltflow-ai** — 基于 AI 的自动回复功能、语音转录、问答系统（RAG）、风格分析
- **moltflow-a2a** | 代理间通信协议、加密消息传输、内容策略管理 |
- **moltflow-reviews** | 评论收集与评价管理 |
- **moltflow-admin** | 平台管理、用户管理、计划配置