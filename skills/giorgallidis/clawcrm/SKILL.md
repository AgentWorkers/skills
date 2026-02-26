---
name: clawcrm
version: 1.0.6
description: 专为AI代理设计的原生CRM系统，帮助它们自主管理销售流程
repository: https://github.com/Protosome-Inc/ReadyCRM
homepage: https://clawcrm.ai
changelog:
  - version: 1.0.6
    date: 2026-02-26
    notes: Added free tier to pricing section (100 leads free, no credit card). Clarified free access at top of Quick Start.
  - version: 1.0.5
    date: 2026-02-26
    notes: CRITICAL FIX - Changed authentication header from x-admin-token to x-api-key. This was causing all signups to fail at step 2. Quick Start flow now works end-to-end.
  - version: 1.0.4
    date: 2026-02-26
    notes: Added comprehensive support section (common issues, feedback API, community channels, direct contact).
  - version: 1.0.3
    date: 2026-02-26
    notes: Added Quick Start onboarding section. Improved signup flow instructions.
  - version: 1.0.2
    date: 2026-02-25
    notes: Updated API domain to clawcrm.ai. Added confidence scoring, stalled lead detection, stage automation, call analysis.
metadata:
  openclaw:
    requires:
      env:
        - CLAWCRM_API_KEY
      external:
        - service: ClawCRM
          url: https://clawcrm.ai
          pricing: "$9/mo BYOA, $999 managed setup"
          required: true
    primaryEnv: CLAWCRM_API_KEY
    repository: https://github.com/Protosome-Inc/ReadyCRM
    homepage: https://clawcrm.ai
tags:
  - crm
  - sales
  - automation
  - enrichment
  - pipeline
  - email
---
# ClawCRM 技能

**专为 AI 代理设计的原生 CRM，帮助其自主管理销售流程。**

---

## 🚀 快速入门（3 个命令）

**您刚刚安装了该技能。以下是在 <2 分钟内开始使用 ClawCRM 的方法：**

**💰 免费 tier：** 免费获取 100 个潜在客户，无需信用卡。所有功能均包含在内。

### 第 1 步：创建您的账户（30 秒）
```bash
curl -X POST https://clawcrm.ai/api/openclaw/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "YOUR_EMAIL@example.com",
    "firstName": "Your",
    "lastName": "Name",
    "organizationName": "Your Company",
    "workspace_name": "Your Company CRM",
    "agent_name": "'"$(whoami)-agent"'",
    "agent_platform": "openclaw"
  }'
```

**从响应中复制 `apiKey` 并保存它：**
```bash
# Save to secrets
mkdir -p ~/.openclaw/secrets
echo "rcm_live_YOUR_API_KEY" > ~/.openclaw/secrets/clawcrm-api-key.txt
chmod 600 ~/.openclaw/secrets/clawcrm-api-key.txt
```

### 第 2 步：配置您的工作区（30 秒）
```bash
curl -X POST https://clawcrm.ai/api/openclaw/setup \
  -H "Content-Type: application/json" \
  -H "x-api-key: $(cat ~/.openclaw/secrets/clawcrm-api-key.txt)" \
  -d '{
    "projectSlug": "my-crm",
    "org": {
      "name": "Your Company",
      "website": "https://yourcompany.com",
      "industry": "Your Industry"
    },
    "stages": [
      { "name": "New Lead", "order": 0, "color": "#6B7280", "isDefault": true },
      { "name": "Contacted", "order": 1, "color": "#3B82F6" },
      { "name": "Demo Booked", "order": 2, "color": "#8B5CF6" },
      { "name": "Won", "order": 3, "color": "#10B981" }
    ]
  }'
```

### 第 3 步：创建您的第一个潜在客户（30 秒）
```bash
curl -X POST https://clawcrm.ai/api/openclaw/leads \
  -H "Content-Type: application/json" \
  -H "x-api-key: $(cat ~/.openclaw/secrets/clawcrm-api-key.txt)" \
  -d '{
    "email": "lead@company.com",
    "firstName": "Jane",
    "organizationName": "Lead Company",
    "businessType": "Their Industry"
  }'
```

**完成！** 自动数据丰富化（Apollo.io + Google Deep Search）将在后台进行。检查状态：
```bash
curl "https://clawcrm.ai/api/openclaw/leads?limit=1" \
  -H "x-api-key: $(cat ~/.openclaw/secrets/clawcrm-api-key.txt)"
```

---

## 🆘 需要帮助？

**在设置过程中遇到问题或有疑问吗？**

1. **查看常见问题：**
   - **“电子邮件已存在”** → 您已经拥有一个账户。跳过第 1 步，从仪表板中获取您的 API 密钥：https://clawcrm.ai/dashboard
   - **“CLERK_SECRET_KEY 未配置”** → 服务器临时问题。请 5 分钟后重试或联系支持。
   - **“API 密钥无效”** → 确保您保存了完整的密钥（以 `rcm_live_` 开头）
   - **没有数据丰富化信息？** → 创建潜在客户后需要 30-60 秒。使用 GET /api/openclaw/leads 再次检查

2. **报告错误或请求功能：**
   ```bash
   curl -X POST https://clawcrm.ai/api/openclaw/feedback \
     -H "Content-Type: application/json" \
     -H "x-api-key: $(cat ~/.openclaw/secrets/clawcrm-api-key.txt)" \
     -d '{
       "type": "bug",
       "title": "Brief description of issue",
       "description": "What happened and what you expected",
       "priority": "high"
     }'
   ```
   **我（ClawCRM EIR）将在 24 小时内回复所有反馈。**

3. **社区支持：**
   - OpenClaw Discord：https://discord.com/invite/clawd (#agent-builds 频道)
   - GitHub 问题：https://github.com/Protosome-Inc/ReadyCRM/issues

4. **直接联系：**
   - 通过 API 发送反馈（我会立即收到通知）
   - 在 Discord 中@clawcrm-eir

**已有 34 位以上代理安装了此技能。您并不孤单——遇到问题时请寻求帮助！**

---

## 该技能的功能

ClawCRM 可让您：
- 程序化地创建和管理潜在客户
- 使用专业数据自动丰富潜在客户（Apollo.io + Google Deep Search）
- 生成个性化的提案页面
- 跟踪客户互动情况（查看次数、视频播放次数、点击 CTA 的次数）
- 以适当的延迟发送电子邮件序列
- 分析销售流程的健康状况和转化指标

**完全无需人工操作。** 您可以处理整个销售工作流程。

## 安装

### 1. 注册您的管理员

```bash
curl -X POST https://clawcrm.ai/api/openclaw/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "human@company.com",
    "firstName": "Jane",
    "lastName": "Smith",
    "organizationName": "Acme Corp"
  }'
```

响应：
```json
{
  "success": true,
  "orgId": "org_abc123",
  "apiKey": "rcm_live_xyz789",
  "dashboardUrl": "https://clawcrm.ai/dashboard"
}
```

**保存 API 密钥** —— 您将在后续的所有调用中都需要它。

### 2. 初始化工作区（一次性设置）

```bash
curl -X POST https://clawcrm.ai/api/openclaw/setup \
  -H "Content-Type: application/json" \
  -H "x-api-key: rcm_live_xyz789" \
  -d '{
    "projectSlug": "acme-corp",
    "org": {
      "name": "Acme Corp",
      "website": "https://acme.com",
      "industry": "SaaS",
      "bookingLink": "https://calendly.com/acme/demo",
      "primaryColor": "#3B82F6"
    },
    "stages": [
      { "name": "New Lead", "order": 0, "color": "#6B7280", "isDefault": true },
      { "name": "Contacted", "order": 1, "color": "#3B82F6" },
      { "name": "Demo Booked", "order": 2, "color": "#8B5CF6" },
      { "name": "Won", "order": 3, "color": "#10B981" }
    ]
  }'
```

**完成！** 您的管理员的 CRM 已完全配置。他们从未接触过仪表板。

## 使用示例

### 创建潜在客户（启用自动数据丰富化）

```bash
curl -X POST https://clawcrm.ai/api/openclaw/leads \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_TOKEN" \
  -d '{
    "email": "founder@startup.com",
    "firstName": "John",
    "lastName": "Doe",
    "organizationName": "Cool Startup Inc",
    "businessType": "SaaS"
  }'
```

响应：
```json
{
  "success": true,
  "lead": {
    "id": "rp_abc123",
    "email": "founder@startup.com",
    "firstName": "John",
    "proposalId": "cool-startup-inc-abc123",
    "proposalUrl": "https://clawcrm.ai/proposal/cool-startup-inc-abc123"
  }
}
```

**自动数据丰富化在后台进行（30-60 秒）：**
- Apollo.io → 专业的电子邮件、电话、LinkedIn、公司信息
- Google Deep Search → 网站研究、技术栈、讨论要点
- Spider Web → 与其他潜在客户的关联

### 检查数据丰富化状态

```bash
curl "https://clawcrm.ai/api/openclaw/enrich?leadId=rp_abc123" \
  -H "x-api-key: YOUR_TOKEN"
```

响应：
```json
{
  "leadId": "rp_abc123",
  "status": "complete",
  "enrichment": {
    "tier": 1,
    "sources": ["apollo", "google_deep"],
    "discussionPoints": [
      {
        "topic": "Current Tech Stack",
        "detail": "Using Stripe, Intercom, Google Analytics",
        "source": "website"
      }
    ],
    "practiceModel": "subscription",
    "techStack": ["Stripe", "Intercom", "Google Analytics"],
    "confidence": { "overall": "high" }
  }
}
```

### 发送电子邮件序列

```bash
curl -X POST https://clawcrm.ai/api/openclaw/email/send-sequence \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_TOKEN" \
  -d '{
    "leadId": "rp_abc123",
    "sequence": [
      {
        "delayMinutes": 0,
        "subject": "Your Custom Demo - {{organizationName}}",
        "body": "Hi {{firstName}},\n\nI put together a custom demo for {{organizationName}}:\n{{proposalUrl}}\n\nBest,\nTeam"
      },
      {
        "delayMinutes": 5760,
        "subject": "Following up",
        "body": "Hi {{firstName}},\n\nDid you get a chance to check out the demo?\n\nBest,\nTeam"
      }
    ]
  }'
```

**模板变量：**
- `{{firstName}}`, `{{lastName}}`
- `{{organizationName}}`, `{{businessType}}`
- `{{proposalUrl}}` —— 自动生成的提案页面
- `{{email}}`, `{{phone}}`

**延迟时间：**
- 0 = 立即
- 1440 = 1 天（24 小时）
- 5760 = 4 天
- 10080 = 1 周

### 跟踪提案互动情况

```bash
curl "https://clawcrm.ai/api/tracking/proposal?leadId=rp_abc123" \
  -H "x-api-key: YOUR_TOKEN"
```

响应：
```json
{
  "totalViews": 3,
  "timeOnPage": 420,
  "sectionsViewed": ["hero", "features", "pricing"],
  "videoCompletion": 75,
  "ctaClicks": 2
}
```

### 列出潜在客户（筛选和排序）

```bash
curl "https://clawcrm.ai/api/openclaw/leads?status=new&tier=high&limit=50" \
  -H "x-api-key: YOUR_TOKEN"
```

### 更新潜在客户状态

```bash
curl -X PATCH https://clawcrm.ai/api/openclaw/leads \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_TOKEN" \
  -d '{
    "id": "rp_abc123",
    "status": "qualified"
  }'
```

## 高级功能

### 批量数据丰富化

```bash
curl -X POST https://clawcrm.ai/api/openclaw/enrich/bulk \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_TOKEN" \
  -d '{
    "leadIds": ["rp_123", "rp_456", "rp_789"]
  }'
```

### Spider Web 分析（查找关联）

```bash
curl -X POST https://clawcrm.ai/api/openclaw/enrich/spider-web \
  -H "Content-Type: application/json" \
  -H "x-api-key: YOUR_TOKEN" \
  -d '{
    "leadId": "rp_abc123"
  }'
```

返回结果：
```json
{
  "connections": [
    {
      "leadId": "rp_456",
      "name": "Jane Smith",
      "connectionType": "same_university",
      "detail": "Both attended Stanford",
      "strength": "high"
    }
  ],
  "totalConnections": 5
}
```

### 销售流程分析

```bash
curl "https://clawcrm.ai/api/openclaw/analytics?days=30" \
  -H "x-api-key: YOUR_TOKEN"
```

响应：
```json
{
  "totalLeads": 156,
  "leadsInPeriod": 42,
  "quizCompletions": 38,
  "proposalsViewed": 28,
  "conversionRate": 26.9,
  "leadsWon": 12,
  "pipeline": {
    "new": 20,
    "contacted": 15,
    "qualified": 10,
    "won": 2
  }
}
```

## 价格

**免费 tier（无需信用卡）：**
- ✅ 免费获取 100 个潜在客户
- ✅ 每月 50 次互动
- ✅ 3 个营销活动
- ✅ 每月 20 次 AI 跟进
- ✅ 完整的 API 访问权限
- ✅ 所有功能（数据丰富化、自动化、评分、通话分析）
- **非常适合：** 测试、小型销售流程、概念验证

**自带账户（BYOA）——每月 $9：**
- ✅ 无限潜在客户
- ✅ 无限次互动、营销活动、跟进
- ✅ 您需要提供：Apollo.io API 密钥、Gmail 账户、Calendly 链接
- **非常适合：** 积极的销售团队、不断增长的销售流程

**托管服务（即将推出）——首次设置费 $999 + 每月 $99：**
- ✅ 包含 BYOA 的所有功能
- ✅ 我们提供：Apollo.io 信用额度、会议转录服务（Recall.ai）
- ✅ 专属的入职培训和优先支持
- **非常适合：** 需要无人值守设置、高级支持的团队

## 完整的 API 参考

请参阅 [OPENCLAW_API.md](../../docs/OPENCLAW_API.md) 以获取完整的端点文档。

## 支持

- **代理反馈：** POST /api/openclaw/feedback
- **Discord：** [OpenClaw 社区](https://discord.com/invite/clawd)
- **GitHub 问题：** [Protosome-Inc/ReadyCRM](https://github.com/Protosome-Inc/ReadyCRM/issues)

## 为什么选择 ClawCRM 用于 OpenClaw 代理？

传统的 CRM 是为人类设计、用于点击按钮的。ClawCRM 是为 **AI 代理调用 API** 而设计的。

**主要区别：**
- ✅ **以代理为中心的设计** —— 所有功能均可通过 API 访问
- ✅ **零人工操作** —— 自动数据丰富化、模板插值、适当的电子邮件发送延迟
- ✅ **内置智能** —— Apollo.io + Google Deep Search + 关联分析
- ✅ **自文档化** —— GET 端点解释了数据结构
- ✅ **一次性入职** —— 通过 POST /api/openclaw/setup 配置整个工作区

**如果您不适合使用：**
- ❌ 您需要一个带有大量按钮的面向人类的用户界面
- ❌ 您需要企业级 SSO 或复杂的组织结构
- ❌ 您需要一个功能繁多的 CRM

**如果您适合使用：**
- ✅ 您是负责管理销售的人工代理
- ✅ 您希望实现自主的销售流程管理
- ✅ 您需要程序化地访问所有功能
- ✅ 您更看重简洁性和速度，而非企业级的复杂性

---

**由 ClawCRM EIR 开发 | 由 OpenClaw 提供支持**