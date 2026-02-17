---
name: didit-sessions
description: 集成 Didit 会话（Session）和工作流（Workflow）API —— 这是用于管理验证会话的核心接口。当用户需要创建验证会话、设置 KYC（了解你的客户）工作流、根据工作流 ID 创建会话、检索会话结果、获取会话决策、列出会话、删除会话、更新会话状态、批准或拒绝会话、请求重新提交、生成 PDF 报告、在合作伙伴之间共享会话、导入共享的会话、将用户添加或从黑名单中移除、管理被阻止的面孔/文档/电话/电子邮件信息、处理 Webhook 事件，或使用 Didit 实现任何端到端的验证流程时，均可使用这些 API。涵盖了 11 个 API 端点：create（创建）、retrieve（检索）、list（列出）、delete（删除）、update-status（更新状态）、generate-pdf（生成 PDF 报告）、share（共享）、import-shared（导入共享会话）、blocklist-add（将用户添加到黑名单）、blocklist-remove（将用户从黑名单中移除）以及 blocklist-list（列出黑名单中的用户）。
version: 2.0.0
metadata:
  openclaw:
    requires:
      env:
        - DIDIT_API_KEY
        - DIDIT_WORKFLOW_ID
    primaryEnv: DIDIT_API_KEY
    emoji: "🔄"
    homepage: https://docs.didit.me
---
# Didit 会话与工作流 API

## 概述

会话是 Didit 验证的核心单元。每次验证都从创建一个与 **工作流**（在控制台中配置）关联的会话开始。工作流定义了要执行的检查（如身份验证、实时检测、反洗钱筛查等）以及决策逻辑。

**基础 URL：** `https://verification.didit.me/v3`

**会话生命周期：**
```
Create Session → User verifies at URL → Receive webhook/poll decision → Optionally update status
```

**速率限制：** 每个方法每分钟 300 次请求；会话创建：每分钟 600 次请求；决策轮询：每分钟 100 次请求。如果遇到 429 错误，请检查 `Retry-After` 头部字段，并使用指数退避算法进行重试。

**API 参考文档：** https://docs.didit.me/reference/create-session-verification-sessions

---

## 认证

所有请求都需要 `x-api-key` 头部字段。您可以从 [Didit 商业控制台](https://business.didit.me) → API & Webhooks 获取您的 API 密钥。

---

## 会话状态

| 状态 | 描述 | 是否显示在终端 |
|---|---|---|
| `未开始` | 会话已创建，但用户尚未开始验证 | 否 |
| `进行中` | 用户正在完成验证 | 否 |
| `审核中` | 需要人工审核 | 否 |
| `已批准` | 验证成功 | 是 |
| `被拒绝` | 验证失败 | 是 |
| `放弃` | 用户未完成验证即离开 | 是 |
| `过期` | 会话已过期（默认为 7 天） | 是 |
| `重新提交` | 需要重新提交的步骤 | 否 |

---

## 工作流类型

工作流在 **商业控制台** 中创建（仅支持界面操作，不支持通过 API 创建）。每个工作流都有一个唯一的 `workflow_id`。

| 模板 | 启动方式 | 适用场景 |
|---|---|---|
| **KYC** | 身份验证（OCR） | 完整的身份信息注册 |
| **自适应年龄验证** | 自拍年龄估计 | 需要年龄验证的服务（如果年龄不确定时自动回退到身份验证） |
| **生物特征认证** | 实时检测 | 重新验证返回的用户（需要提供 `portrait_image`） |
| **地址验证** | 地址证明 | 住宅地址验证 |
| **问卷调查** | 自定义问卷 | 结构化的证明和文件 |

**两种构建模式：**
- **简单模式**：通过模板切换功能的开启/关闭 |
- **高级模式**：基于节点的可视化图形构建器，支持条件分支、并行路径和操作自动化 |

**工作流中可用的功能：** 身份验证、实时检测、面部匹配、NFC、反洗钱筛查、电话验证、电子邮件验证、地址证明、数据库验证、IP 分析、年龄估计、问卷调查。

---

## 1. 创建会话

```
POST /v3/session/
```

| 头部字段 | 值 | 是否必需 |
|---|---|---|
| `x-api-key` | 您的 API 密钥 | 是 |
| `Content-Type` | `application/json` | 是 |

### 请求体（JSON）

| 参数 | 类型 | 是否必需 | 描述 |
|---|---|---|---|
| `workflow_id` | uuid | 是 | 来自控制台的工作流 ID |
| `vendor_data` | 字符串 | 否 | 用于追踪的标识符（UUID/电子邮件） |
| `callback` | URL | 否 | 重定向 URL。Didit 会在查询参数中附加 `verificationSessionId` + `status` |
| `callback_method` | 字符串 | 否 | `"initiator"`（默认）、`"completer"` 或 `"both"` — 指定处理重定向的设备 |
| `metadata` | JSON 字符串 | 否 | 与会话关联的自定义数据。例如 `{"account_id": "ABC123"` |
| `language` | 字符串 | 否 | UI 语言的 ISO 639-1 代码（如果省略则自动检测） |
| `contact_details.email` | 字符串 | 否 | 用于电子邮件验证步骤的预填电子邮件 |
| `contact_details.phone` | 字符串 | 否 | 用于电话验证步骤的预填电话号码（E.164 格式） |
| `contact_details.send_notification_emails` | 布尔值 | 否 | 是否发送状态更新邮件（默认：`false`） |
| `expected_details.first_name` | 字符串 | 否 | 预期的名字（如果实际名字不同会触发不匹配警告） |
| `expected_details.last_name` | 字符串 | 否 | 预期的姓氏 |
| `expected_details.date_of_birth` | 字符串 | 否 | 预期的出生日期（格式为 `YYYY-MM-DD`） |
| `expected_details.gender` | 字符串 | 否 | `"M"`、`"F"` 或 `null` |
| `expected_details.nationality` | 字符串 | 否 | 国家代码（ISO 3166-1 alpha-3，例如 `USA`） |
| `portrait_image` | base64 | 否 | 生物特征认证工作流所需的参考照片（最大 1MB） |

### 示例

```python
import requests

response = requests.post(
    "https://verification.didit.me/v3/session/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "workflow_id": "d8d2fa2d-c69c-471c-b7bc-bc71512b43ef",
        "vendor_data": "user-123",
        "callback": "https://yourapp.com/callback",
        "language": "en",
    },
)
session = response.json()
# session["url"] → send user here to verify
# session["session_token"] → use for SDK initialization
```

```typescript
const response = await fetch("https://verification.didit.me/v3/session/", {
  method: "POST",
  headers: { "x-api-key": "YOUR_API_KEY", "Content-Type": "application/json" },
  body: JSON.stringify({
    workflow_id: "d8d2fa2d-c69c-471c-b7bc-bc71512b43ef",
    vendor_data: "user-123",
    callback: "https://yourapp.com/callback",
  }),
});
const session = await response.json();
// session.url → redirect user here
```

### 响应（201 创建成功）

```json
{
  "session_id": "11111111-2222-3333-4444-555555555555",
  "session_number": 1234,
  "session_token": "abcdef123456",
  "url": "https://verify.didit.me/session/abcdef123456",
  "vendor_data": "user-123",
  "status": "Not Started",
  "workflow_id": "d8d2fa2d-c69c-471c-b7bc-bc71512b43ef",
  "callback": "https://yourapp.com/callback"
}
```

| 错误代码 | 含义 | 应对措施 |
|---|---|---|
| `400` | 工作流 ID 无效或信用不足 | 确认工作流 ID 是否存在，并检查信用额度 |
| `403` | 没有权限 | 检查 API 密钥的权限 |

---

## 2. 获取会话信息（获取验证结果）

```
GET /v3/session/{sessionId}/decision/
```

返回已完成会话的所有验证结果。图像/媒体文件的 URL 在 **60 分钟** 后失效。

### 响应（200 OK）

```json
{
  "session_id": "...",
  "status": "Approved",
  "features": ["ID_VERIFICATION", "LIVENESS", "FACE_MATCH", "AML"],
  "vendor_data": "user-123",
  "id_verifications": [{"status": "Approved", "document_type": "...", "first_name": "..."}],
  "liveness_checks": [{"status": "Approved", "method": "ACTIVE_3D", "score": 89.92}],
  "face_matches": [{"status": "Approved", "score": 95.5}],
  "phone_verifications": [{"status": "Approved", "full_number": "+14155552671"}],
  "email_verifications": [{"status": "Approved", "email": "user@example.com"}],
  "aml_screenings": [{"status": "Approved", "total_hits": 0}],
  "poa_verifications": [...],
  "nfc_verifications": [...],
  "ip_analyses": [...],
  "database_validations": [...],
  "reviews": [...]
}
```

---

## 3. 列出会话

```
GET /v3/sessions/
```

| 查询参数 | 类型 | 描述 |
|---|---|---|
| `vendor_data` | 字符串 | 按标识符过滤会话 |
| `status` | 字符串 | 按状态过滤会话 |
| `page` | 整数 | 每页显示的记录数 |
| `page_size` | 整数 | 每页的结果数量 |

### 响应（200 OK）

```json
{
  "count": 42,
  "next": "https://verification.didit.me/v3/sessions/?page=2",
  "previous": null,
  "results": [
    {"session_id": "...", "session_number": 34, "status": "Approved", "vendor_data": "user-123", "created_at": "..."}
  ]
}
```

---

## 4. 删除会话

```
DELETE /v3/session/{sessionId}/delete/
```

永久删除会话及 **所有关联数据**。成功时返回 `204 No Content`，未找到会话时返回 `404`。

```python
response = requests.delete(
    f"https://verification.didit.me/v3/session/{session_id}/delete/",
    headers={"x-api-key": "YOUR_API_KEY"},
)
# response.status_code == 204 → success
```

---

## 5. 更新会话状态

```
PATCH /v3/session/{sessionId}/update-status/
```

| 参数 | 类型 | 是否必需 | 描述 |
|---|---|---|
| `new_status` | 字符串 | 是 | `"Approved"`、`"Declined"` 或 `"Resubmitted"` |
| `comment` | 字符串 | 状态变更的原因 |
| `send_email` | 布尔值 | 是否发送电子邮件通知（默认：`false` |
| `email_address` | 字符串 | 否* | 当 `send_email` 为 `true` 时必需 |
| `email_language` | 字符串 | 电子邮件的语言（默认：`en`） |
| `nodes_to_resubmit` | 数组 | 否 | 对于需要重新提交的步骤：`[{"node_id": "feature_ocr", "feature": "OCR"}]` |

> **重新提交：** 仅允许会话状态为 `Declined`、`In Review` 或 `Abandoned` 的情况。已批准的步骤将被保留。

```python
# Approve
requests.patch(f"https://verification.didit.me/v3/session/{session_id}/update-status/",
    headers=headers, json={"new_status": "Approved", "comment": "Manual review passed"})

# Resubmit specific steps with notification
requests.patch(f"https://verification.didit.me/v3/session/{session_id}/update-status/",
    headers=headers, json={
        "new_status": "Resubmitted",
        "nodes_to_resubmit": [{"node_id": "feature_ocr", "feature": "OCR"}],
        "send_email": True, "email_address": "user@example.com"
    })
```

---

## 6. 生成 PDF 报告

```
GET /v3/session/{sessionId}/generate-pdf
```

生成 PDF 验证报告。该操作每分钟限制为 **100 次请求**（受 CPU 资源限制）。

```python
response = requests.get(
    f"https://verification.didit.me/v3/session/{session_id}/generate-pdf",
    headers={"x-api-key": "YOUR_API_KEY"},
)
# Returns PDF content or URL
```

---

## 7. 共享会话

生成用于 B2B KYC 共享的 `share_token`。仅适用于 **已完成的会话**（状态为 `Approved`、`Declined` 或 `In Review`）。

```
POST /v3/session/{sessionId}/share/
```

```python
response = requests.post(
    f"https://verification.didit.me/v3/session/{session_id}/share/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
)
share_token = response.json()["share_token"]
# Transmit share_token to partner via your backend
```

---

## 8. 导入共享会话

接收方使用此 API 导入共享的验证会话。

```
POST /v3/session/import-shared/
```

| 参数 | 类型 | 是否必需 | 描述 |
|---|---|---|
| `share_token` | 字符串 | 是 | 来自共享方的令牌 |
| `trust_review` | 布尔值 | 是 | `true`：保持原始状态；`false`：将状态设置为 `In Review` |
| `workflow_id` | 字符串 | 是 | 需要关联的工作流 ID |
| `vendor_data` | 字符串 | 是 | 您自己的用户标识符 |

```python
response = requests.post(
    "https://verification.didit.me/v3/session/import-shared/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
    json={
        "share_token": "eyJhbGciOiJIUzI1NiIs...",
        "trust_review": True,
        "workflow_id": "your-workflow-uuid",
        "vendor_data": "user-789",
    },
)
```

> 每个合作伙伴的应用程序只能导入 **一次** 会话数据。导入前需签署法律数据共享协议并获得用户同意。

---

## 9. 添加到黑名单

将特定面部、文档、电话号码或电子邮件地址添加到黑名单。匹配到的项目将自动拒绝未来的验证请求。

```
POST /v3/blocklist/add/
```

| 参数 | 类型 | 是否必需 | 默认值 | 描述 |
|---|---|---|---|
| `session_id` | uuid | 是 | 需要添加到黑名单的会话 ID |
| `blocklist_face` | 布尔值 | 否 | 是否阻止生物特征面部识别 |
| `blocklist_document` | 布尔值 | 否 | 是否阻止文档验证 |
| `blocklist_phone` | 布尔值 | 否 | 是否阻止电话号码验证 |
| `blocklist_email` | 布尔值 | 否 | 是否阻止电子邮件地址验证 |

### 匹配到黑名单时的自动拒绝提示：

| 实体 | 提示标签 |
|---|---|
| 面部 | `FACE_IN_BLOCKLIST` |
| 文档 | `ID DOCUMENT_IN_BLOCKLIST` |
| 电话 | `PHONE_NUMBER_IN_BLOCKLIST` |
| 电子邮件 | `EMAIL_IN_BLOCKLIST` |

---

## 10. 从黑名单中移除

```
POST /v3/blocklist/remove/
```

| 参数 | 类型 | 是否必需 | 默认值 | 描述 |
|---|---|---|---|
| `session_id` | uuid | 是 | 需要从黑名单中移除的会话 ID |
| `unblock_face` | 布尔值 | 否 | 是否解除对面部识别的阻止 |
| `unblock_document` | 布尔值 | 否 | 是否解除对文档验证的阻止 |
| `unblock_phone` | 布尔值 | 否 | 是否解除对电话号码验证的阻止 |
| `unblock_email` | 布尔值 | 否 | 是否解除对电子邮件地址的阻止 |

```python
requests.post("https://verification.didit.me/v3/blocklist/remove/",
    headers={"x-api-key": "YOUR_API_KEY", "Content-Type": "application/json"},
    json={"session_id": "...", "unblock_face": True})
```

---

## 11. 查看黑名单

```
GET /v3/blocklist/
```

| 查询参数 | 类型 | 描述 |
|---|---|---|
| `item_type` | 字符串 | 过滤类型：`"face"`、`"document"`、`"phone"`、`"email"`。省略该参数将显示所有会话 |

---

## 错误响应（所有接口）

| 错误代码 | 含义 | 应对措施 |
|---|---|---|
| `400` | 请求体或参数无效 | 检查必填字段和格式 |
| `401` | API 密钥无效或缺失 | 确认 `x-api-key` 头部字段的存在 |
| `403 | 信用不足或缺乏权限 | 在商业控制台中检查信用额度 |
| `404` | 未找到会话 | 确认会话 ID 是否存在 |
| `429` | 超过速率限制 | 检查 `Retry-After` 头部字段，并使用指数退避算法进行重试 |

---

## 常见工作流示例

### 基本 KYC 流程

```
1. POST /v3/session/ → create session with KYC workflow_id, get URL
2. Redirect user to session URL
3. Listen for webhook OR poll GET /v3/session/{id}/decision/
4. "Approved"  → user verified
   "Declined"  → check decision, optionally resubmit
   "In Review" → manual review or auto-decide via API
```

### 程序化审核 + 添加到黑名单

```
1. Receive webhook: status "In Review"
2. GET /v3/session/{id}/decision/ → inspect all results
3. Apply business logic
4. If fraud: PATCH → Declined + POST /v3/blocklist/add/ (block all entities)
   If legit: PATCH → Approved
```

### B2B KYC 共享

```
Service X:
1. POST /v3/session/{id}/share/ → get share_token
2. Transmit token to Service Y via backend

Service Y:
3. POST /v3/session/import-shared/ → import with trust_review=true
4. Session imported instantly with original status
```

### 生物特征重新认证

```
1. Retrieve portrait_image from user's initial approved session
2. POST /v3/session/ → biometric auth workflow + portrait_image
3. User takes selfie → system matches against portrait
4. "Approved" → identity re-confirmed
```