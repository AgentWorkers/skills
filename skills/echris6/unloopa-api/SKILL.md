---
name: unloopa-api
description: 让你的代理自动将网站出售给当地企业。该代理可以从 Google Maps 中寻找潜在客户，为每个潜在客户创建一个定制的 AI 网站，发送推广邮件，甚至还可以主动拨打电话联系他们。当你需要寻找潜在客户、生成网站、发送邮件或进行语音通话时，都可以使用这个工具。
metadata:
  author: unloopa
  version: "1.3"
  openclaw:
    primaryEnv: UNLOOPA_API_KEY
    requires:
      env:
        - UNLOOPA_API_KEY
---

# Unloopa API

您可以通过其REST API来控制Unloopa平台。所有请求均发送到`https://dashboard.unloopa.com/api/v1/`，并采用Bearer令牌进行身份验证。

## 身份验证

每个请求都需要包含以下头部信息：
```
Authorization: Bearer $UNLOOPA_API_KEY
```
API密钥设置在`UNLOOPA_API_KEY`环境变量中。密钥以`unlpa_live_`开头。

如果用户尚未配置密钥，请告知他们：
1. 访问`https://dashboard.unloopa.com/settings`并点击“API”选项卡
2. 点击“Create API Key”并复制密钥（该密钥仅显示一次）
3. 在您的OpenClaw设置中配置该密钥，或设置环境变量：`export UNLOOPA_API_KEY=unlpa_live_...`

如果收到401“未经授权”的错误，说明密钥缺失或无效——请让用户检查他们的密钥。

## 首次调用：始终从`GET /quota`开始

**在执行任何操作之前**，请先调用`GET /quota`以获取以下信息：
- 用户使用的计划类型（入门级或专业级）
- 是否启用了语音和视频功能
- 剩余的潜在客户数量和信用额度
- 如果需要升级或购买信用额度，请提供相应的链接

这个请求可以告诉您用户可以和不能做什么。根据返回的结果调整您的操作：

| quota字段 | 含义 |
|---|---|
| `voice_enabled: false` | 不提供语音通话服务——用户需要专业级计划。分享`purchase_links.upgrade`链接 |
| `video_enabled: false` | 不提供视频生成服务——用户需要专业级计划 |
| `voice_credits: 0` | 无法进行通话——分享`purchase_links.voice_credits`链接 |
| `websites_remaining: 0` | 无法生成潜在客户——信用额度在`resets_at`时间重置 |

## 错误格式

所有错误都会返回以下格式：
```json
{ "error": { "code": "error_code", "message": "Human-readable message", "details": {} } }
```

错误代码：`unauthorized`（401）、`invalid_input`（400）、`not_found`（404）、`plan_required`（403）、`insufficient_credits`（402）、`quota_exceeded`（429）、`rate_limited`（429）、`setup_required`（400）、`limit_reached`（400）、`invalid_state`（400）、`internal_error`（500）。

当收到`plan_required`（403）错误时，分享升级链接；当收到`insufficient_credits`（402）错误时，分享信用额度购买链接；当遇到速率限制时，请查看`Retry-After`头部字段（以秒为单位）。

## 计划类型

- **入门级**（每月47美元）：每月1,000个潜在客户，支持电子邮件推广和模板功能
- **专业级**（每月97美元）：每月5,000个潜在客户，支持200个视频文件、语音通话和AI代理服务

---

## 工作流程

### 1. 完整的潜在客户处理流程（任何计划）
`/command`端点会自动执行整个流程：抓取潜在客户信息 → 生成网站 → 丰富电子邮件内容 → 发送推广邮件。只需描述您想要执行的操作即可。
```
1. GET  /quota                    → check websites.remaining > 0
2. POST /command                  → submit natural language command (full pipeline runs automatically)
3. GET  /jobs/{job_id}            → poll every 5-10s until status=completed
4. GET  /leads?job_id={job_id}    → view generated leads with websites, emails, etc.
```

### 2. 电子邮件推广（任何计划）
```
1. GET  /outreach/status          → verify configured=true, remaining_today > 0
2. GET  /leads?has_email=true     → find leads with emails
3. GET  /outreach/templates       → pick a template
4. POST /outreach/send            → queue emails
```
如果`configured=false`，请告知用户在响应中的`setup_url`链接处连接他们的电子邮件账户。

### 3. 语音通话（仅限专业级计划）
如果`/quota`中的`voice_enabled`设置为`false`，则完全跳过此流程。告知用户他们需要升级到专业级计划，并分享升级链接。

前提条件：`voice_enabled=true` + `voice_credits > 0` + 至少1个电话号码 + 至少1个语音代理。
```
1. GET  /quota                    → voice_enabled? voice_credits > 0?
   If voice_credits=0 → share purchase_links.voice_credits
2. GET  /phone-numbers            → count > 0? (max 3)
   If empty → POST /phone-numbers/search + POST /phone-numbers/buy
3. GET  /voice/agents             → count > 0? (max 3)
   If empty → POST /voice/agents (create one)
4. POST /voice/call               → single call, OR:
5. POST /voice/campaigns          → bulk campaign (starts as draft)
6. PATCH /voice/campaigns/{id}    → action=activate, then action=trigger
```

### 4. 完整的营销流程
`/command`端点现在会自动执行步骤1-3。语音通话是唯一需要手动操作的步骤。
```
1. GET  /quota                    → know the plan, adapt accordingly
2. POST /command → poll /jobs/{id} → GET /leads  (scrape + websites + emails + outreach all automatic)
3. Voice (Pro only): /phone-numbers → /voice/agents → /voice/campaigns
```

---

## 端点参考

### POST /command
提交一个自然语言相关的潜在客户生成命令。API会自动执行整个流程：抓取潜在客户信息 → 生成网站 → 丰富电子邮件内容 → 发送推广邮件。无需在命令中详细说明每个步骤。

**请求体：**
```json
{
  "command": "Find 50 plumbers in Miami",
  "max_results": 50,
  "with_video": false,
  "with_vsl": false
}
```
- `command`（必填，字符串，最多1000个字符）——只需描述目标市场和位置。命令中提到的任何数字都会被忽略——使用`max_results`来控制潜在客户数量。
- `max_results`（可选，1-100，默认值为100；当`with_video`/`with_vsl`为true时，默认值为10）
- `with_video`（可选，布尔值，仅限专业级计划）
- `with_vsl`（可选，布尔值，仅限专业级计划）

**默认行为：**API会覆盖命令中的设置。它会抓取最多`max_results`个潜在客户（默认为100个），为每个潜在客户生成一个网站，查找他们的电子邮件地址，丰富他们的社交媒体资料，并自动发送推广邮件。命令中的数字（如“Find 15 plumbers”）会被忽略；请使用`max_results`来指定数量。

**响应：`
```json
{
  "job_id": "...", 
  "status": "processing",
  "defaults": {
    "max_results": ..., 
    "generate_websites": ..., 
    "enrich_emails": ..., 
    "send_outreach": ..., 
    "with_video": ..., 
    "with_vsl": ...
  },
  "quota": {
    "used": ..., 
    "limit": ..., 
    "remaining": ...
  }
}
```

---

### GET /jobs
列出已提交的命令。

**查询参数：`?limit=20&offset=0`（限制结果数量为100）

**响应：**
```json
{
  "jobs": [
    { "job_id": "...", 
      "command": "...", 
      "intent": "...", 
      "status": "...", 
      "error": "...", 
      "created_at": "...", 
      "updated_at": "..." 
    ],
    "total": ..., 
    "limit": ..., 
    "offset": ...
  ],
  "total": ...
}
```

### GET /jobs/{id}
查询任务的进度和结果。

**响应：**
```json
{
  "job_id": "uuid",
  "status": "processing|completed|failed",
  "progress": 75,
  "current_step": "Generating websites...",
  "steps": [{ "name": "scraping", "status": "completed", "message": "Found 50 leads", "count": 50 }],
  "result": {
    "websites": [{ "id": "uuid", "url": "https://...", "business_name": "...", "city": "...", "industry": "..." }],
    "leads_scraped": 50,
    "emails_sent": 0
  },
  "error": null
}
```
每5-10秒查询一次任务进度。根据潜在客户数量和视频生成情况，任务处理时间可能为30秒到5分钟不等。

---

### GET /leads
列出并过滤潜在客户信息。

**查询参数（全部为可选）：**
- `limit`（1-100，默认值50），`offset`（默认值0）
- `city`（部分匹配，例如“miami”）
- `industry`（部分匹配，例如“plumber”）
- `has_phone=true`（仅显示有电话号码的潜在客户）
- `has_email=true`（仅显示有电子邮件地址的潜在客户）
- `min_rating`（最低Google评分，例如4.0）
- `min_reviews`（最低评论数量）
- `job_id`（从特定命令生成的潜在客户）
- `search`（在名称、城市和行业中进行自由文本搜索）
- `created_after`（ISO格式日期，例如“2025-01-15”）
- `created_before`（ISO格式日期）
- `has_website=true`（仅显示有生成网站的潜在客户）
- `has_video=true`（仅显示有视频文件的潜在客户）
- `video_status`（待处理|生成中|已完成|失败）

**响应：**
```json
{
  "leads": [{
    "id": "uuid",
    "business_name": "Acme Plumbing",
    "city": "Miami",
    "industry": "Plumber",
    "phone": "+13055551234",
    "email": "info@acme.com",
    "rating": 4.8,
    "reviews": 127,
    "url": "https://unlora.com/acme-plumbing-miami",
    "language": "en",
    "video_url": "https://...",
    "video_status": "completed",
    "vsl_url": "https://...",
    "vsl_status": "completed",
    "socials": { "instagram": "...", "facebook": "...", "linkedin": "...", "twitter": "..." },
    "created_at": "2025-01-15T..."
  }],
  "total": 50, "limit": 50, "offset": 0
}
```

### GET /leads/{id}
显示潜在客户的详细信息，包括现有网站的信息。

**响应：**
与列表字段相同，另外还包括：
- `slug`（URL路径）
- `existing_website`：`{ url, pagespeed_score, load_time, mobile_optimized }` 或 `null`

---

### GET /websites
列出生成的网站列表。

**查询参数：`?limit=20&offset=0`

**响应：**
```json
{
  "websites": [
    { "id": "...", 
      "url": "...", 
      "slug": "...", 
      "business_name": "...", 
      "city": "...", 
      "industry": "...", 
      "phone": "...", 
      "email": "...", 
      "language": "...", 
      "video_url": "...", 
      "vsl_url": "...", 
      "created_at": "..." 
    ],
    "total": ..., 
    "limit": ..., 
    "offset": ...
  ]
}
```

### GET /quota
检查计划类型、使用情况、信用额度和购买链接。

**响应：**
```json
{
  "plan": "pro",
  "plan_status": "active",
  "websites": { "used": 150, "limit": 5000, "remaining": 4850 },
  "videos": { "used": 0, "limit": 200, "remaining": 200 },
  "voice_credits": 45,
  "voice_enabled": true,
  "video_enabled": true,
  "resets_at": "2025-02-01T00:00:00.000Z",
  "purchase_links": {
    "voice_credits": {
      "50_credits_$10": "https://whop.com/checkout/plan_xBEWrVWZ8MRvM/",
      "200_credits_$35": "https://whop.com/checkout/plan_ucYBrssGb4E2G/",
      "500_credits_$75": "https://whop.com/checkout/plan_zTX2bQyWLCqlx/"
    },
    "upgrade": "https://whop.com/unloopa/"
  }
}
```

### GET /outreach/status
检查电子邮件配置、每日发送量以及DNS服务器的运行状态。

**响应：**
```json
{
  "configured": true,
  "accounts": [{
    "id": "uuid",
    "email": "outreach@company.com",
    "display_name": "Company",
    "daily_limit": 25,
    "sent_today": 10,
    "remaining_today": 15,
    "warmup_enabled": true,
    "warmup_day": 14,
    "health": { "score": 85, "status": "good", "checked_at": "2025-01-15T..." },
    "created_at": "2025-01-01T..."
  }],
  "summary": {
    "total_accounts": 1,
    "total_daily_capacity": 25,
    "total_sent_today": 10,
    "total_remaining_today": 15,
    "pending_in_queue": 5,
    "accounts_with_health_issues": 0
  },
  "setup_url": "https://dashboard.unloopa.com/settings?tab=email"
}
```
新SMTP账户的启用数量按时间逐步增加：每天5个 → 10个 → 15个 → 25个。

---

### GET /outreach/templates
列出预构建和自定义的电子邮件模板。

**响应：**
```json
{
  "templates": [
    { "id": "...", 
      "name": "...", 
      "subject": "...", 
      "body": "...", 
      "is_custom": "...", 
      "is_default": "...", 
      "language": "..." 
    ],
    "custom_templates": [
      { "id": "...", 
      "name": "...", 
      "subject": "...", 
      "body": "...", 
      "is_custom": "...", 
      "is_default": "...", 
      "language": "..." 
    ]
  ]
}
```

模板支持以下占位符：`{{business_name}}`、`{{city}}`、`{{industry}}`、`{{website_url}}`、`{{video_url}}`（仅限专业级计划）。

---

### POST /outreach/templates
创建自定义电子邮件模板。

**请求体：**
```json
{
  "name": "Miami Pitch",
  "subject": "{{business_name}} - New Website Ready",
  "body": "Hi! I built a website for {{business_name}} in {{city}}...",
  "language": "en",
  "is_default": true
}
```
必填字段：名称和主题。

---

### PATCH /outreach/templates/{id}
更新自定义模板。

**请求体：**
```json
{
  "name?:...", 
  "subject?:...", 
  "body?:...", 
  "language?:..."
}
```

---

### DELETE /outreach/templates/{id}
删除自定义模板。

---

### POST /outreach/send
向潜在客户发送电子邮件。

**请求体：**
```json
{
  "lead_ids": ["uuid1", "uuid2"],
  "template_id": "uuid",
  "custom_subject": "Optional override",
  "custom_body": "Optional override"
}
```
- `lead_ids`（必填，1-100个UUID）
- `template_id`（如果提供了`custom_subject`和`custom_body`，则为可选字段）

**响应：**
```json
{
  "emails_queued":..., 
  "emails_waiting_for_video":..., 
  "skipped_duplicates":..., 
  "failed":..., 
  "manual_outreach": []
}
```
发送邮件之前，请确保SMTP已配置（请先查看`/outreach/status`）。系统会检测重复邮件，避免向同一潜在客户重复发送。

---

### GET /phone-numbers
列出可用的电话号码。需要专业级计划。

**响应：**
```json
{
  "numbers": [
    { "id": "...", 
      "phone_number": "...", 
      "area_code": "...", 
      "locality": "...", 
      "region": "...", 
      "country": "...", 
      "monthly_cost_cents": "..." 
    ], 
    "count": 2 
  ]
}
```
最多可购买3个电话号码。购买前请检查`count`参数是否在允许的范围内。

---

### POST /phone-numbers/search
按区号搜索可用电话号码。需要专业级计划。

**请求体：**
```json
{
  "area_code": "...", 
  "country": "..."
}
```
**响应：**
```json
{
  "numbers": [
    { "phone_number": "+13055551234", 
      "friendly_name": "...", 
      "locality": "...", 
      "region": "..." 
    ]
}
```
**注意：`area_code`必须为3位数字**

**响应：**
```json
{
  "numbers": [
    { "phone_number": "+13055551234", 
      "friendly_name": "...", 
      "locality": "...", 
      "region": "..." 
    ]
}
```
**注意：`phone_number`必须为E.164格式**

**响应：**
```json
{
  "number": { "id": "...", 
      "phone_number": "...", 
      "area_code": "...", 
      "monthly_cost_cents": "..." 
    }
}
```
**注意：`number`字段必须为E.164格式**

---

### POST /phone-numbers/buy
购买电话号码。需要专业级计划。费用为每月1美元/号码。

**请求体：**
```json
{
  "phone_number": "+13055551234"
}
```
**注意：`number`字段必须为E.164格式**

**响应：**
```json
{
  "number": { "id": "...", 
      "phone_number": "...", 
      "area_code": "...", 
      "monthly_cost_cents": "..." 
}
```
**注意：`number`字段必须为E.164格式**

**注意：**购买后，该号码将被释放。

---

### GET /voice/agents
列出可用的语音代理。需要专业级计划。

**响应：**
```json
{
  "agents": [
    { "id": "...", 
      "name": "...", 
      "voice_id": "...", 
      "voice_name": "...", 
      "elevenlabs_agent_id": "...", 
      "has_script": "...", 
      "has_first_message": "...", 
      "created_at": "..." 
    ], 
    "count": 1 
  ]
}
```
最多可购买3个语音代理。

---

### POST /voice/agents
创建一个新的语音代理。需要专业级计划。

**请求体：**
```json
{
  "name": "Sales Agent",
  "voice_id": "cjVigY5qzO86Huf0OWal",
  "voice_name": "Eric",
  "script": "You are a friendly sales rep calling {{business_name}} in {{city}}...",
  "first_message": "Hi there, do you have just a moment?",
  "agent_config": { "stability": 0.3, "similarityBoost": 0.85 }
}
```
**必填字段：**名称和语音ID

**请求体：**
```json
{
  "name?:...", 
  "voice_id?:...", 
  "voice_name?:...", 
  "script?:..."
}
```
**注意：**`script`字段可以使用动态变量：`{{business_name}}`、`{{city}}`、`{{industry}}`、`{{website_url}}`（这些变量会从潜在客户数据中自动填充）

---

### PATCH /voice/agents/{id}
更新语音代理的信息。更改会自动同步到ElevenLabs系统。

**请求体：**
```json
{
  "name?:...", 
  "voice_id?:...", 
  "voice_name?:...", 
  "script?:...", 
  "first_message?:...", 
  "agent_config?:..."
}
```

---

### DELETE /voice/agents/{id}
删除语音代理。

---

### POST /voice/call
发起一次外出通话。每次通话消耗1个信用额度。需要专业级计划。

**请求体：**
```json
{
  "agent_id": "uuid",
  "phone_number": "+13055551234",
  "dynamic_variables": { "business_name": "Acme", "city": "Miami", "industry": "Plumbing", "website_url": "https://..." }
}
```
**必填字段：**代理ID

**响应：**
```json
{
  "call_id": "...", 
  "conversation_id": "...", 
  "status": "initiated"
}
```
**注意：**每次通话都会消耗1个信用额度

**响应：**
```json
{
  "call_id": "...", 
  "conversation_id": "...", 
  "status": "initiated", 
  "phone_number": "..."
}
```

---

### GET /voice/calls
列出语音通话记录。需要专业级计划。

**查询参数：**
```json
```
?limit=50&offset=0&campaign_id=uuid&status=completed&outcome=interested
```
**响应：**
```json
{
  "calls": [
    { "id": "...", 
      "campaign_id": "...", 
      "business_name": "...", 
      "phone_number": "...", 
      "status": "...", 
      "outcome": "...", 
      "outcome_notes": "...", 
      "duration_secs": "...", 
      "transcript": "...", 
      "analysis": "...", 
      "started_at": "...", 
      "completed_at": "..." 
    ], 
    "total": ..., 
    "limit": ..., 
    "offset": ...
  ]
}
```
**响应包含通话的详细信息和转录内容**

---

### GET /voice/campaigns
列出语音通话活动的相关信息。需要专业级计划。

**响应：**
```json
{
  "campaigns": [{
    "id": "uuid",
    "name": "Miami Plumbers",
    "status": "active",
    "stats": { "total": 50, "connected": 30, "interested": 8, "not_interested": 15, "no_answer": 7, "failed": 0, "avg_duration_secs": 45 },
    "created_at": "...", "updated_at": "..."
  }]
}
```

---

### POST /voice/campaigns
创建一个语音通话活动。需要专业级计划和信用额度。

**请求体：**
```json
{
  "name": "Miami Plumbers Campaign",
  "phone_number_id": "uuid",
  "agent_id": "uuid",
  "lead_filter": { "city": "Miami", "industry": "plumber" },
  "timezone": "America/New_York",
  "calling_window_start": "09:00",
  "calling_window_end": "17:00",
  "calling_days": ["mon", "tue", "wed", "thu", "fri"],
  "calls_per_hour": 10,
  "max_calls": 50
}
```
**必填字段：**名称和电话号码ID，或者`agent_id`和`voice_id`/`script`。

**请求体：**
```json
{
  "name": "...", 
  "phone_number_id": "...", 
  "agent_id": "...", 
  "voice_id": "...", 
  "script": "..."
}
```
**注意：**可以选择提供`lead_ids`（潜在客户ID数组）或`lead_filter`（动态筛选条件）。只有拥有电话号码的潜在客户才会被纳入活动范围。

**响应：**
```json
{
  "campaign": {
    "id": "...", 
    "name": "...", 
    "status": "draft",
    "leads_count": "...",
    "callable_leads": [...]
  }
}
```
**注意：**创建活动后，系统会立即发起最多10次通话，每次通话消耗1个信用额度**

---

### GET /voice/campaigns/{id}
查看语音通话活动的详细信息。

**响应：**
```json
{
  "id": "...", 
  "name": "...", 
  "status": "...",
  "script": "...",
  "script_version": "...",
  "first_message": "...",
  "voice_id": "...",
  "voice_name": "...",
  "timezone": "...",
  "calling_window": "...",
  "calling_days": "...",
  "calls_per_hour": "...",
  "stats": {...}
}
```
**响应包含活动的详细信息和统计数据**

---

### POST /voice/campaigns
创建或修改语音通话活动。

**请求体：**
```json
{
  "name": "Miami Plumbers Campaign",
  "phone_number_id": "uuid",
  "agent_id": "uuid",
  "lead_filter": { "city": "Miami", "industry": "plumber" },
  "timezone": "America/New_York",
  "calling_window_start": "09:00",
  "calling_window_end": "17:00",
  "calling_days": ["mon", "tue", "wed", "thu", "fri"],
  "calls_per_hour": 10,
  "max_calls": 50
}
```
**必填字段：**名称和电话号码ID，或者`agent_id`和`voice_id`/`script`。

**请求体：**
```json
{
  "name": "...",
  "phone_number_id": "...",
  "voice_id": "...",
  "script": "...",
  "lead_ids": [...], 
  "lead_filter": "[...]" 
}
```
**注意：**只有拥有电话号码的潜在客户才会被纳入活动范围**

**响应：**
```json
{
  "campaign": {
    "id": "...",
    "name": "...",
    "status": "draft",
    "leads_count": "...",
    "callable_leads": [...]
  }
}
```
**注意：**创建活动后，系统会立即发起最多10次通话，每次通话消耗1个信用额度**

---

### GET /voice/campaigns/{id}
查看语音通话活动的详细信息和配置。

**响应：**
```json
{
  "id": "...",
  "name": "...",
  "status": "...",
  "script": "...",
  "script_version": "...",
  "first_message": "...",
  "voice_id": "...",
  "voice_name": "...",
  "timezone": "...",
  "calling_window": "...",
  "calling_days": "...",
  "calls_per_hour": "...",
  "stats": {...}
}
```
**响应包含活动的详细信息和统计数据**

---

### PATCH /voice/campaigns/{id}
控制语音通话活动的生命周期或修改相关设置。

**请求体：**
```json
{
  "action": "..."
}
```
**可选操作：**`activate`（将草稿状态的活动激活为活跃状态）/`pause`（将活跃状态的活动暂停）/`cancel`（取消任何活动）
**注意：**每个操作都会影响活动的状态和通话次数**

**更新字段（仅适用于草稿/暂停状态）：**
```json
{
  "updates": {
    "script": "...",
    "voice_id": "...",
    "voice_name": "...",
    "first_message": "...",
    "calling_window_start": "...",
    "calling_window_end": "...",
    "calling_days": "...",
    "calls_per_hour": "..."
  }
}
```
**注意：**每个操作都会更新活动的状态和通话设置**

**响应：**
```json
{
  "trigger": 5,
  "calls": [
    { "id": "...", 
      "business_name": "...", 
      "conversation_id": "..."
    ]
}
```
**注意：**每次触发操作会立即发起最多10次通话**

---

## 重要说明

- 完整的潜在客户处理流程大约需要8-10分钟。抓取潜在客户信息的速度很快（约20秒），但生成网站的时间较长（约8分钟）。请不要假设任务卡住了——请每隔15-20秒查询一次进度，并在网站生成过程中保持耐心。
- 新SMTP账户的启用数量会逐步增加：每天5个，4周内增加到每天25个。
- 语音通话活动必须按照“创建（草稿）→激活→触发”的顺序进行。
- `trigger`操作每次最多可以发起10次通话，每次通话消耗1个信用额度。
- 动态变量（如`{{business_name}}`等）会从潜在客户数据中自动填充。
- 系统会检测重复的电子邮件，避免向同一潜在客户重复发送邮件。
- 视频功能（`with_video`、`with_vsl`）仅限专业级计划使用。
- 电话号码和语音代理的数量都有上限限制（各3个）。
- 在执行任何操作之前，请务必检查前提条件（信用额度、可用资源、SMTP配置和计划类型）。