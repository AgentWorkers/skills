---
name: clawcrm
description: "使用 ClawCRM（这款原生支持人工智能的 CRM 系统）来管理潜在客户、开展外联活动、分析销售数据以及处理电子邮件跟进工作。当销售人员需要执行以下操作时，可以使用该工具：管理销售流程（创建/查看/更新潜在客户信息）、开展外联活动及发送系列电子邮件、查看销售流程的分析数据与转化指标、向潜在客户发送或草拟个性化邮件、处理客户的回复及后续跟进工作、配置问卷调查或提案页面，以及其他任何与 CRM 或销售相关的操作。使用该工具需要 ClawCRM 的部署 URL 和管理员权限令牌。"
---
# ClawCRM — 一款专为AI代理设计的CRM系统

ClawCRM是一款专为AI代理设计的CRM系统，支持代理自主执行各项任务。它通过REST API管理潜在客户、营销活动、外联工作、数据分析、问卷调查以及销售提案等流程。

## 设置

代理需要在`TOOLS.md`文件中配置以下内容：

```markdown
### ClawCRM
- Base URL: https://<deployment>.netlify.app (or self-hosted URL)
- Auth Header: x-admin-token: <token>
- Token file: secrets/clawcrm-token.txt
```

所有API调用均使用以下方式：
```bash
curl -s "$BASE_URL/api/openclaw/<endpoint>" -H "x-admin-token: $(cat secrets/clawcrm-token.txt)"
```

## 核心功能

### 潜在客户管理

```bash
# List leads (paginated)
GET /api/openclaw/leads?limit=100&offset=0

# Create lead (with optional custom fields)
POST /api/openclaw/leads
{"email":"...", "firstName":"...", "lastName":"...", "clinicName":"...", "practiceType":"...", "customFields":{"annual_revenue":"500k","referral_source":"linkedin"}}

# Update lead (with optional custom fields)
PUT /api/openclaw/leads
{"id":"...", "status":"qualified", "customFields":{"insurance_type":"commercial"}}

# Lead fields: id, email, clinicName, practiceType, tier (high/mid/low), status (new/prospect/contacted/qualified/won/lost), quizAnswers, score, crmData (includes custom fields)
```

### 营销活动流程

```bash
# List pipeline stages
GET /api/openclaw/stages

# Create stage
POST /api/openclaw/stages
{"name":"Discovery", "order":1, "color":"#3B82F6", "isDefault":false}

# Update stage
PUT /api/openclaw/stages
{"id":"...", "name":"Qualified Lead", "order":2}

# Delete stage
DELETE /api/openclaw/stages?id=<stage_id>
```

### 自定义字段

```bash
# List custom fields
GET /api/openclaw/fields

# Create custom field
POST /api/openclaw/fields
{"fieldName":"annual_revenue","fieldLabel":"Annual Revenue","fieldType":"text","order":1,"isRequired":false}

# fieldType options: text, number, date, select, multiselect, boolean
# For select/multiselect: include "options": ["Option 1", "Option 2"]

# Update custom field
PUT /api/openclaw/fields
{"id":"...", "fieldLabel":"Annual Revenue (USD)", "isRequired":true}

# Delete custom field
DELETE /api/openclaw/fields?id=<field_id>
```

### 组织设置

```bash
# Get org settings (branding, contact, locale, features)
GET /api/openclaw/org

# Update org settings (full replace)
PUT /api/openclaw/org
{"branding":{"brandName":"Acme Corp","primaryColor":"#FF6B35"},"contact":{"replyToEmail":"hello@acme.com"}}

# Partial update (merge with existing)
PATCH /api/openclaw/org
{"branding":{"logoUrl":"https://example.com/logo.png"}}

# Settings structure:
# - branding: brandName, logoUrl, primaryColor, secondaryColor
# - contact: replyToEmail, fromName, supportEmail, phone
# - locale: timezone, currency, dateFormat
# - features: quizEnabled, proposalsEnabled, analyticsEnabled, emailIntegrationEnabled
```

### 营销活动模板

```bash
# List campaign templates (org-specific + public)
GET /api/openclaw/templates?category=<category>&include_public=true

# Create campaign template
POST /api/openclaw/templates
{"name":"Welcome Sequence","category":"onboarding","trigger":"quiz_completed","steps":[{"channel":"email","delay":0,"subject":"...","body":"..."}]}

# Instantiate template as campaign
PATCH /api/openclaw/templates
{"templateId":"...", "name":"Q1 Welcome Campaign"}

# Categories: onboarding, nurture, reactivation, winback, custom
# Steps: [{"channel":"email|sms","delay":<hours>,"subject":"...","body":"..."}]
```

### 数据分析

```bash
# Pipeline overview (default 30d)
GET /api/openclaw/analytics

# Returns: totalLeads, leadsInPeriod, quizCompletions, proposalsViewed, conversionRate, leadsWon, pipeline byStatus
```

### 营销活动与执行顺序

```bash
# List campaigns
GET /api/openclaw/campaigns

# Create campaign sequence
POST /api/openclaw/campaigns
{"name":"...", "trigger":"quiz_completed|high_score_lead|manual|...", "steps":[...]}

# Triggers: quiz_completed, proposal_viewed, proposal_not_viewed_24h, high_score_lead, stage_changed, manual
# Channels: email, sms, linkedin, twitter
```

### 后续跟进

```bash
# Get actionable follow-ups with email templates
GET /api/openclaw/followups

# Send follow-up
POST /api/openclaw/followups
{"leadId":"...", "channel":"email", "subject":"...", "body":"..."}
```

### 接触点记录

```bash
# Lead activity history
GET /api/openclaw/touchpoints?leadId=<id>

# Log touchpoint
POST /api/openclaw/touchpoints
{"leadId":"...", "type":"email|call|meeting|note", "content":"..."}
```

### 其他API端点

```bash
GET /api/openclaw/health          # Health check
GET /api/openclaw/quiz            # Quiz funnel config
GET /api/openclaw/playbooks       # SDR workflow playbooks
GET /api/config/proposal          # Proposal page config
```

## 邮件集成

ClawCRM支持与外部邮件服务提供商集成，以便发送外联邮件：
- **MailerSend** — 基于API的交易型邮件服务（需配置API密钥和经过验证的域名）
- **Himalaya/IMAP** — 用于读取回复、搜索邮件线程及管理收件箱
- **Gmail/Outlook OAuth** — 用户无需额外设置，可通过OAuth登录并使用自己的真实邮箱发送邮件

具体集成方式请参阅`references/email-integration.md`文件。

## 外联工作流程

1. 获取潜在客户信息：`GET /api/openclaw/leads`（可根据层级或状态进行筛选）
2. 根据潜在客户信息（如问卷调查答案、练习类型、需求痛点）起草个性化邮件
3. 将邮件草稿保存以供人工审核后再发送
4. 通过MailerSend或后续跟进API端点发送邮件
5. 记录所有接触点：`POST /api/openclaw/touchpoints`
6. 通过IMAP监控回复并更新潜在客户状态
7. 查看数据分析结果：`GET /api/openclaw/analytics`

有关创意外联策略的详细信息，请参阅`references/outreach-playbook.md`文件。

## 关键原则

- **注重实际效果而非数量** — 即使有100个潜在客户，如果没有人被联系，这些数据也毫无价值。应以回复数量、预约会议次数和成交数量来衡量工作效果。
- **始终个性化沟通** — 根据潜在客户的具体情况（如问卷答案、练习类型、地理位置和需求）定制邮件内容，切勿使用通用模板。
- **人工审核后再发送邮件** — 邮件草稿需先保存供人工审核，只有在获得批准后才能发送；除非明确指示自动发送。
- **详细记录所有操作** — 每封发送的邮件、收到的回复以及预约的会议都应被记录为接触点。