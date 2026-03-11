---
name: selzy
description: >
  通过 Selzy API 创建并发送电子邮件营销活动。您可以管理联系人、联系人分组（segments）以及邮件模板；安排活动的时间表，执行 A/B 测试，并分析活动效果（如邮件打开率、点击率、退信率）。您还可以将自然语言请求转换为完整的电子邮件营销活动。
  **v2.1 — 修复了关键错误：** 现在，发送营销活动时必须提供明确的 `list_id`。如果没有提供 `list_id`，Selzy 仅会向一个联系人发送邮件。请务必先调用 `getLists` 函数获取联系人列表。
metadata:
  openclaw:
    emoji: "✉️"
    requires:
      env:
        - SELZY_API_KEY
    primaryEnv: SELZY_API_KEY
  version: "2.3"
  lastUpdated: "2026-02-26"
  changelog:
    - "2.3: HARD LIMIT changed to 1 campaign per HOUR (was 1/min) after 35-campaign ban incident"
    - "2.2: Added RATE LIMIT WARNING — max 1 campaign per minute, batch sends forbidden"
    - "2.2: Documented account ban risk: 35 campaigns in few minutes triggered block"
    - "2.1: Added CRITICAL WARNING section about list_id requirement"
    - "2.1: Added SAFETY CHECKLIST for all campaign sends"
    - "2.1: Added real-world bug fix example (1 vs 4 recipients)"
    - "2.1: Updated all workflows to verify contact count before sending"
---
# Selzy 邮件营销 API — 完整指南

Selzy 是一个提供 REST API 的邮件营销平台，用于管理联系人、创建活动以及分析活动效果。通过使用该 API，您可以通过人工智能助手来执行所有的邮件营销操作。

---

## 🚨 重要警告 — 使用前请阅读

### ⚠️ 常见陷阱：邮件发送给错误收件人

**问题：** 如果在创建活动时未明确指定 `list_id`，Selzy 会 **仅发送给 1 位联系人**（默认行为），而不是整个联系人列表。

**解决方案：** 始终遵循以下工作流程：
1. 调用 `getLists` 以获取正确的 `list_id` 并验证联系人数量
2. 将 `list_id` 传递给 `createEmailMessage`（必需参数）
3. 在调用 `createCampaign` 之前，确认收件人数量与预期一致
4. 在发送前获取用户的明确确认

**这会影响所有用户。** 解决方案在于工作流程，而非 API 本身。

---

### 🚫 速率限制警告 — 账户被封禁的风险

**真实事件（2026-02-25）：** 有用户使用 `createCampaign` 在几分钟内发送了 35 封邮件活动，导致账户被封禁，因为 Selzy 认为这是可疑的大量发送行为。

**Selzy API 的官方速率限制**（来自 https://selzy.com/en/support/api/common/selzy-api-limits/）：

| 端点/操作 | 限制 |
|-------------------|-------|
| **通用 API** | 每 API 密钥或 IP 每 60 秒 1200 次请求 |
| `checkEmail` 方法 | 每 60 秒 300 次请求 |
| `subscribe` 方法 | 限制较多（具体数值未公开） |
| `sendEmail` 方法 | 新用户每天默认 1,000 封邮件（会自动增加） |
| `sendSms` 方法 | 每次调用最多 150 个电话号码 |
| `getCampaigns` 方法 | 每次响应最多 10,000 次活动创建 |
| `getMessages` 方法 | 每次请求最多 100 条记录（默认 50 条） |
| `importContacts` 方法 | 每次调用超时 30 秒 |

**⚠️ 重要提示：** 活动创建的速率（未公开但严格执行）：

虽然通用 API 允许每分钟 1200 次请求，但 **创建活动 (`createCampaign`) 有额外的欺诈检测机制：
- **每小时最多创建 1 次活动**（封禁事件后严格执行此限制）
- **如果 5 分钟内创建 35 次活动 = 立即被封禁**（2026-02-25 的真实事件）
- Selzy 的欺诈系统会将快速创建活动视为可疑的大量发送行为

**为什么会有这种差异？**
- 每分钟 1200 次请求是针对 **读取操作**（如 `getLists`, `getCampaigns`, `stats`）
- **写入操作**（如 `createCampaign`, `importContacts`）有更严格的反滥用限制
- 关于活动创建速率没有官方文档——通过启发式方法执行

**违反速率限制的症状：**
- API 返回所有活动的 `count=0`（即使活动有效）
- 活动卡在 `scheduled` 状态但从未发送
- 账户被标记为需要人工审核

**恢复方法：**
1. **立即停止所有活动创建**
2. 等待 24-48 小时以自动解封，或联系 Selzy 客服
3. 请求人工审核并解释这是自动化错误
4. 解封后：实施速率限制（**每小时最多 1 次活动**）

**预防措施：**
- **在调用 `createCampaign` 之间等待 1 小时**——这是硬性限制
- 对于批量发送：每小时最多创建 1 次活动，并分散在几天内进行
- 监控 API 响应：如果多次请求的结果都是 `count=0`，则是一个危险信号
- **在没有速率限制的情况下，** **永远不要自动化批量创建活动**
- 请记住：每分钟 1200 次请求是针对读取操作，而不是活动创建

**如果您需要向多个联系人组发送邮件：**
```
1. Create all email messages first (no rate limit on createEmailMessage)
2. Schedule campaigns across multiple days (1 per hour max)
3. OR: use single campaign with segmented list (preferred)
4. Use cron jobs with hourly spacing for automated sends
```

**现在这是强制性的：** 任何自动化操作如果每小时创建超过 1 次活动，都有被永久封禁的风险。**每小时最多 1 次活动。**

---

### 📊 Selzy API 限制汇总

| 操作 | 限制 | 备注 |
|-----------|-------|-------|
| 通用 API 调用 | 每分钟 1200 次 | 每个 API 密钥或 IP |
| checkEmail | 每分钟 300 次 | 用于验证电子邮件地址 |
| sendEmail (transactional) | 每天 1000 封 | 新用户，数量会自动增加 |
| sendSms | 每次调用 150 次 | 每次请求最多发送给 150 个电话号码 |
| getCampaigns | 每次响应最多 10,000 次活动创建 | 需要分页查询更多信息 |
| getMessages | 每次请求最多 100 条记录 | 默认 50 条 |
| importContacts | 每次调用超时 30 秒 |

**来源：** https://selzy.com/en/support/api/common/selzy-api-limits/

---

## 🔐 认证

所有请求都需要 `SELZY_API_KEY` 环境变量。请将其作为 `api_key` 参数传递。

**基础 URL：** `https://api.selzy.com/en/api`

**重要提示：** 所有方法都使用 `GET` 请求，并带有查询参数（Selzy API 的所有端点都使用 GET 方法）。在需要时，请对参数值进行 URL 编码。

## 通用请求格式

```bash
curl "https://api.selzy.com/en/api/{METHOD}?format=json&api_key=$SELZY_API_KEY&{params}"
```

**响应格式：**
- 成功：`{"result": {...}}` 或 `{"result": [...]}`
- 错误：`{"error": "message", "code": "error_code"}`

---

## 📋 1. 联系人列表

### 1.1 获取列表 — `getLists`

检索所有联系人列表。

```bash
curl "https://api.selzy.com/en/api/getLists?format=json&api_key=$SELZY_API_KEY"
```

**响应：**
```json
{
  "result": [
    {"id": 1, "title": "Newsletter subscribers", "count": 15420, "active_contacts": 14800}
  ]
}
```

### 1.2 创建列表 — `createList`

创建一个新的联系人列表。

```bash
curl "https://api.selzy.com/en/api/createList?format=json&api_key=$SELZY_API_KEY&title=VIP%20Customers"
```

**响应：`{"result": {"id": 12345}}`

### 1.3 获取列表详情 — `getList`

获取特定列表的详细信息。

```bash
curl "https://api.selzy.com/en/api/getList?format=json&api_key=$SELZY_API_KEY&list_id=12345"
```

---

## 👥 2. 联系人管理

### 2.1 导入联系人 — `importContacts`

批量导入联系人到列表中。

```bash
curl "https://api.selzy.com/en/api/importContacts?format=json&api_key=$SELZY_API_KEY&field_names[]=email&field_names[]=Name&data[][]=john@example.com&data[][]=John&data[][]=jane@example.com&data[][]=Jane&list_ids=12345&overwrite=2"
```

| 参数 | 描述 |
|-----------|-------------|
| `field_names[]` | 列名称：电子邮件（必需）、姓名、电话等 |
| `data[][]` | 联系人数据行（扁平数组，逐行填充） |
| `list_ids` | 逗号分隔的列表 ID，用于添加联系人 |
| `overwrite` | 0=跳过现有联系人，1=覆盖所有联系人，2=仅覆盖空联系人 |

### 2.2 订阅 — `subscribe`

添加一个联系人，并允许其选择是否接收邮件。

```bash
curl "https://api.selzy.com/en/api/subscribe?format=json&api_key=$SELZY_API_KEY&list_ids=12345&fields[email]=user@example.com&fields[Name]=Alice&double_optin=3"
```

**double_optin 值：**
- `0` = 不发送确认邮件
- `3` = 发送确认邮件
- `4` = 已经确认（强制订阅）

### 2.3 移除联系人 — `exclude`

取消订阅/删除联系人。

```bash
curl "https://api.selzy.com/en/api/exclude?format=json&api_key=$SELZY_API_KEY&contact_type=email&contact=user@example.com"
```

### 2.4 获取联系人信息 — `getContact`

通过电子邮件地址获取联系人详情。

```bash
curl "https://api.selzy.com/en/api/getContact?format=json&api_key=$SELZY_API_KEY&email=user@example.com"
```

### 2.5 创建自定义字段 — `createField`

为联系人添加自定义字段。

```bash
curl "https://api.selzy.com/en/api/createField?format=json&api_key=$SELZY_API_KEY&field_name=Company&field_type=text"
```

**field_type 选项：** `text`, `number`, `date`, `boolean`

---

## 📧 3. 邮件模板

### 3.1 创建邮件模板 — `createEmailMessage`

⚠️ **重要：`list_id` 是必需的** ⚠️

**如果没有 `list_id`，Selzy 会 **仅发送给 1 位联系人**（默认行为）。** 这是一个常见的陷阱，会导致邮件发送给错误的收件人。

**在创建邮件模板之前，** **务必先调用 `getLists` 以获取正确的 `list_id` 并验证联系人数量。**

```bash
curl "https://api.selzy.com/en/api/createEmailMessage?format=json&api_key=$SELZY_API_KEY&sender_name=My%20Store&sender_email=news@yourdomain.com&subject=Summer%20Sale%20🔥&body=<h1>Hello!</h1><p>Check%20out%20our%20deals</p>&list_id=12345"
```

| 参数 | 必需 | 描述 |
|-----------|----------|-------------|
| `sender_name` | 是 | 发件人名称 |
| `sender_email` | 是 | 发件人电子邮件地址（必须是已验证的域名） |
| `subject` | 是 | 邮件主题行 |
| `body` | 是 | HTML 内容（需要 URL 编码） |
| `list_id` | **是 — 必须的** | **目标列表 ID。必须从 `getLists` 获取。否则，活动将仅发送给 1 位联系人！** |
| `lang` | 否 | 语言代码（如 en, ru, es 等） |
| `text_body` | 否 | 平文版本（备用） |
| `tag` | 否 | 用于过滤/分析的活动标签 |

**响应：`{"result": {"message_id": 67890}}`

### 3.2 更新邮件模板 — `updateEmailMessage`

修改现有的邮件模板。

```bash
curl "https://api.selzy.com/en/api/updateEmailMessage?format=json&api_key=$SELZY_API_KEY&id=67890&subject=Updated%20Subject"
```

### 3.3 获取邮件模板详情 — `getMessage`

获取邮件模板的详细信息。

```bash
curl "https://api.selzy.com/en/api/getMessage?format=json&api_key=$SELZY_API_KEY&id=67890"
```

### 3.4 列出所有邮件模板 — `listMessages`

列出所有邮件模板，并可按日期筛选。

```bash
curl "https://api.selzy.com/en/api/listMessages?format=json&api_key=$SELZY_API_KEY&date_from=2026-01-01&date_to=2026-02-01"
```

### 3.5 创建邮件模板 — `createEmailTemplate`

创建可重用的模板（与邮件内容分开）。

```bash
curl "https://api.selzy.com/en/api/createEmailTemplate?format=json&api_key=$SELZY_API_KEY&name=Welcome%20Series&subject=Welcome!&body=<h1>Welcome {{Name}}!</h1>"
```

### 3.6 获取模板详情 — `getTemplate`

获取模板的详细信息。

```bash
curl "https://api.selzy.com/en/api/getTemplate?format=json&api_key=$SELZY_API_KEY&template_id=12345"
```

---

## 🚀 4. 活动

### 4.1 创建活动 — `createCampaign`

创建并安排活动。

```bash
curl "https://api.selzy.com/en/api/createCampaign?format=json&api_key=$SELZY_API_KEY&message_id=67890&start_time=2026-02-10%2010:00:00&timezone=Europe/Moscow&track_read=1&track_links=1"
```

| 参数 | 必需 | 描述 |
|-----------|----------|-------------|
| `message_id` | 是 | 来自 `createEmailMessage` 的邮件模板 ID |
| `start_time` | 否 | 安排时间（格式为 YYYY-MM-DD HH:MM:SS）。如需立即发送可省略 |
| `timezone` | 否 | 安排发送时的时区（例如，Europe/Belgrade） |
| `track_read` | 否 | 是否跟踪打开情况（1=是，0=否） |
| `track_links` | 否 | 是否跟踪点击情况（1=是，0=否） |

**响应：`{"result": {"campaign_id": 11111}}`

### 4.2 取消活动 — `cancelCampaign`

取消已安排的活动。

```bash
curl "https://api.selzy.com/en/api/cancelCampaign?format=json&api_key=$SELZY_API_KEY&campaign_id=11111"
```

### 4.3 获取活动状态 — `getCampaignStatus`

检查活动的状态和进度。

```bash
curl "https://api.selzy.com/en/api/getCampaignStatus?format=json&api_key=$SELZY_API_KEY&campaign_id=11111"
```

**状态值：** `draft`, `scheduled`, `sending`, `analysed`, `canceled`

### 4.4 获取活动列表 — `getCampaigns`

列出最近的活动，可添加日期筛选条件。

```bash
curl "https://api.selzy.com/en/api/getCampaigns?format=json&api_key=$SELZY_API_KEY&from=2026-01-01&to=2026-02-24"
```

**日期格式：** `YYYY-MM-DD HH:MM:SS` 或 `YYYY-MM-DD`

---

## 📊 5. 活动统计

### 5.1 获取活动统计信息 — `getCampaignCommonStats`

获取活动的综合统计信息。

```bash
curl "https://api.selzy.com/en/api/getCampaignCommonStats?format=json&api_key=$SELZY_API_KEY&campaign_id=11111"
```

**响应：**
```json
{
  "result": {
    "total": 15000,
    "sent": 14800,
    "delivered": 14500,
    "read_unique": 4200,
    "read_all": 5100,
    "clicked_unique": 890,
    "clicked_all": 1200,
    "unsubscribed": 12,
    "spam": 3
  }
}
```

**统计指标：**
- **打开率** = `(read_unique / delivered) × 100`
- **点击率** = `(clicked_unique / delivered) × 100`
- **退信率** = `((sent - delivered) / sent) × 100`
- **取消订阅率** = `(unsubscribed / delivered) × 100`
- **垃圾邮件率** = `(spam / delivered) × 100`

---

## 📮 6. 发件人

### 6.1 获取发件人电子邮件地址 — `getSenderEmails`

列出所有已验证的发件人电子邮件地址。

```bash
curl "https://api.selzy.com/en/api/getSenderEmails?format=json&api_key=$SELZY_API_KEY"
```

**响应：**
```json
{
  "result": [
    {
      "id": 8526648,
      "email": "news@yourdomain.com",
      "name": "Your Store",
      "isVerified": true,
      "dkimStatus": "verified",
      "isFreeDomain": false
    }
  ]
}
```

**注意：** 活动中的 `sender_email` 必须来自这些已验证的列表。**

---

## 🎯 代理操作指南

### 重要规则

#### 🚨 安全检查清单（在发送任何活动之前）

**必须完成以下步骤：**
- [ ] 调用 `getLists` → 确保有明确的 `list_id`
- [ ] 验证联系人数量 → 确认与预期收件人一致
- [ ] 如果数量为 0 或与预期不符 → **停止并提醒用户**
- [ ] `createEmailMessage` 包含 `list_id` 参数
- [ ] 用户确认：列表名称、数量、主题、发送时间
- [ ] 明确收到用户的“发送”或“确认”指令
- [ ] **速率限制检查：** 最后创建的活动是否超过 1 小时（严格执行此限制）
- [ ] **批量发送警告：** 如果每小时创建超过 1 次活动 = 有账户被封禁的风险**

**如果任何检查失败 → **不要发送，先询问用户。**

**重要提示：** 如果在几分钟内创建 35 次活动 = 账户将被封禁。每小时最多创建 1 次活动。**

---

1. **在没有用户明确确认的情况下，** **永远不要发送活动。** 始终显示：
   - 收件人列表的名称和数量（**确认这与预期一致**）
   - 主题行
   - 正文摘要（前 100 个字符）
   - 发送时间（立即发送或安排发送）
   **使用的 `list_id`

2. **对于新活动，遵循以下工作流程（必须执行）：**
   ```
   1. getLists → GET list_id AND count of contacts
   2. VERIFY: count >= expected recipients (if count=0, STOP and ask)
   3. createEmailMessage → MUST include list_id parameter + confirm subject + content
   4. RATE LIMIT CHECK: If created campaign in last 60s, WAIT before proceeding
   5. createCampaign → confirm timing + recipient count
   6. WAIT for explicit "send" or "confirm" from user
   ```

   **⚠️ 批量发送：** 如果要创建多个活动（例如，针对不同的联系人组）：
   - 先创建所有 `createEmailMessage` 调用（不受速率限制）
   - 在每次调用 `createCampaign` 之间间隔 **1 小时**（严格执行此限制）
   **永远** 不要每小时创建超过 1 次活动 — 否则会有立即被封禁的风险
   - 真实事件：几分钟内创建 35 次活动会导致账户被封禁
   - 如有必要，可以使用定时任务将活动分散在几天内发送

3. **重要提示：** `list_id` 是必需的**
   - **在没有明确 `list_id` 的情况下，** **永远不要创建邮件模板**
   **在发送之前，务必验证联系人数量与预期一致**
   - 如果 `list_id` 缺失或数量错误 → 停止并提醒用户

4. **对于统计请求：**
   - 始终以百分比计算各项指标
   - 如果需要，与行业基准进行比较（平均打开率：20%，点击率：2.5%）
   - 强调与之前活动的趋势对比

4. **优雅地处理错误：**
   - 用简单的语言解释问题所在
   - 建议具体的解决方法
   - 由于速率限制，可以尝试重新发送一次（延迟 1 秒）

5. **安全提醒：**
   - **永远不要记录或显示完整的 API 密钥**
   | 提醒用户 `sender_email` 必须经过验证**
   | 提醒用户关于联系人导入的 GDPR/合规性要求

### 常见工作流程

#### “为我的 VIP 客户创建活动”
```
1. getLists → find VIP list, confirm count (MUST match expected recipients)
2. If count is wrong → STOP and alert user (DO NOT proceed)
3. Ask: subject, content type (promo/newsletter/event)
4. createEmailMessage → MUST include list_id parameter, show preview
5. createCampaign (omit start_time for immediate)
6. ⚠️ WAIT for "send it" or "confirm" before considering it done
7. Report: campaign_id, status, recipient count (verify matches step 1)
```

#### “我的上一次活动效果如何？”
```
1. getCampaigns (last 7 days) → get latest campaign_id
2. getCampaignCommonStats → get metrics
3. Calculate: open rate, click rate, bounce rate, unsubscribe rate
4. Present as: "X% opened, Y% clicked, Z% bounced"
5. Optional: compare to industry avg or previous campaign
```

#### “将新订阅者添加到我的新闻通讯中”
```
1. getLists → find newsletter list
2. Confirm: list name, number of contacts to add
3. importContacts (bulk) OR subscribe (single)
4. Report: success count, skipped count, errors
```

#### “查看我的联系人列表”
```
1. getLists → retrieve all
2. Present table: Name | Total | Active | Created
3. Offer: "Want to create a new list or add contacts?"
```

#### “安排网络研讨会邀请”
```
1. getLists → confirm audience (GET list_id + count)
2. VERIFY count matches expected recipients
3. Ask: webinar details (title, date, time, link)
4. createEmailMessage with storytelling approach + list_id parameter
5. createCampaign with start_time="2026-02-25 10:00:00" timezone="Europe/Belgrade"
6. Confirm: "Scheduled for Feb 25 at 10:00 AM Belgrade time to {count} recipients"
```

---

## 📖 实际问题修复示例

### ❌ 错误 — 邮件发送给 1 人而不是 4 人

```bash
# Missing list_id — Selzy sends to 1 contact by default!
curl "https://api.selzy.com/en/api/createEmailMessage?format=json&api_key=$KEY&sender_name=My+Store&sender_email=me@example.com&subject=Sale&body=<h1>Sale!</h1>"
```

**结果：** 活动 #327590492 被发送给了列表中的 1 位收件人，而不是 4 位收件人。

### ✅ 正确做法 — 始终包含 `list_id`

```bash
# Step 1: Get lists and verify count
curl "https://api.selzy.com/en/api/getLists?format=json&api_key=$KEY"
# Response: [{"id": 12345, "title": "My first list", "count": 4}]

# Step 2: Create message WITH list_id
curl "https://api.selzy.com/en/api/createEmailMessage?format=json&api_key=$KEY&sender_name=My+Store&sender_email=me@example.com&subject=Sale&body=<h1>Sale!</h1>&list_id=12345"
# Response: {"result": {"message_id": 67890}}

# Step 3: Create campaign
curl "https://api.selzy.com/en/api/createCampaign?format=json&api_key=$KEY&message_id=67890"
# Response: {"result": {"campaign_id": 11111}}

# Result: Campaign sent to ALL 4 contacts ✅
```

---

## ⚠️ API 错误处理

| 错误响应 | 含义 | 解决方法 |
|----------------|---------|-----|
| `"error": "Incorrect API key"` | API 密钥错误/缺失 | 检查配置中的 SELZY_API_KEY |
| `"error": "Access denied"` | 权限不足 | 确认 API 密钥的权限范围是否正确 |
| `"error": "Not found"` | 资源不存在 | 检查 ID（campaign_id, message_id, list_id） |
| `"error": "Bad date-time literal"` | 日期格式错误 | 使用 `YYYY-MM-DD HH:MM:SS` 格式 |
| HTTP 429 | 速率限制 | 等待 1-2 秒，然后重试一次 |
| `"error": "Sender not verified"` | 发件人电子邮件地址不在已验证的列表中 | 使用 `getSenderEmails` 选择已验证的地址 |

---

## 📚 资源

- **API 参考：** https://selzy.com/en/support/api/
- **入门指南：** https://selzy.com/en/support/
- **注册：** https://selzy.com/en/registration/
- **博客：** https://selzy.com/en/blog/

---

## 🧪 快速测试命令

验证 API 访问：
```bash
# Check connection
curl "https://api.selzy.com/en/api/getLists?format=json&api_key=YOUR_KEY"

# Check verified senders
curl "https://api.selzy.com/en/api/getSenderEmails?format=json&api_key=YOUR_KEY"

# Test campaign stats (replace ID)
curl "https://api.selzy.com/en/api/getCampaignCommonStats?format=json&api_key=YOUR_KEY&campaign_id=123456"
```

---

**技能版本：** 2.0（完整版）  
**最后更新：** 2026-02-24  
**已测试的方法：** getLists, getSenderEmails, getCampaigns, getCampaignCommonStats, createEmailMessage, createCampaign, getTemplates