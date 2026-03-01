---
name: clawcrm
description: 专为AI代理设计的原生CRM系统，帮助它们自主管理销售流程。
repository: https://github.com/Protosome-Inc/ReadyCRM
homepage: https://clawcrm.ai
metadata:
  openclaw:
    requires:
      env:
        - CLAWCRM_API_KEY
      external:
        - service: ClawCRM
          url: https://readycrm.netlify.app
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

## 该技能的功能

ClawCRM 可让您：
- 以编程方式创建和管理潜在客户（leads）
- 自动为潜在客户补充专业信息（数据来源：Apollo.io + Google Deep Search）
- 生成个性化的提案页面
- 跟踪潜在客户的互动情况（如页面浏览量、视频播放次数、点击转化按钮的次数）
- 定时发送邮件序列
- 分析销售流程的健康状况和转化指标

**完全无需人工干预**。您可以完全掌控整个销售工作流程。

## 安装步骤

### 1. 注册您的管理员

```bash
curl -X POST https://readycrm.netlify.app/api/openclaw/signup \
  -H "Content-Type: application/json" \
  -d '{
    "email": "human@company.com",
    "firstName": "Jane",
    "lastName": "Smith",
    "organizationName": "Acme Corp"
  }'
```

管理员的注册完成后，您将获得一个 API 密钥，后续的所有操作都需要使用这个密钥。

### 2. 设置工作空间（一次性配置）

```bash
curl -X POST https://readycrm.netlify.app/api/openclaw/setup \
  -H "Content-Type: application/json" \
  -H "x-admin-token: rcm_live_xyz789" \
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

**完成！** 您的管理员的 CRM 已经配置完成。他们甚至无需接触任何仪表板。

## 使用示例

### 创建潜在客户（启用自动信息补充）

```bash
curl -X POST https://readycrm.netlify.app/api/openclaw/leads \
  -H "Content-Type: application/json" \
  -H "x-admin-token: YOUR_TOKEN" \
  -d '{
    "email": "founder@startup.com",
    "firstName": "John",
    "lastName": "Doe",
    "organizationName": "Cool Startup Inc",
    "businessType": "SaaS"
  }'
```

系统会在后台自动为潜在客户补充信息（通常需要 30-60 秒）：
- 数据来源：Apollo.io（提供潜在客户的电子邮件地址、电话号码、LinkedIn 账户及公司信息）
- 数据来源：Google Deep Search（提供潜在客户的网站信息、技术栈及讨论要点）
- 数据来源：Spider Web（在您的 CRM 中查找与其他潜在客户的关联）

### 查看信息补充状态

```bash
curl "https://readycrm.netlify.app/api/openclaw/enrich?leadId=rp_abc123" \
  -H "x-admin-token: YOUR_TOKEN"
```

### 发送邮件序列

```bash
curl -X POST https://readycrm.netlify.app/api/openclaw/email/send-sequence \
  -H "Content-Type: application/json" \
  -H "x-admin-token: YOUR_TOKEN" \
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

**邮件模板中的变量：**
- `{{firstName}}`（名字）
- `{{lastName}}`（姓氏）
- `{{organizationName}}`（公司名称）
- `{{businessType}}`（企业类型）
- `{{proposalUrl}}`（自动生成的提案页面链接）
- `{{email}}`（潜在客户的电子邮件地址）
- `{{phone}}`（潜在客户的电话号码）

**发送邮件的延迟时间：**
- 0：立即发送
- 1440：1 天（24 小时）
- 5760：4 天
- 10080：1 周

### 跟踪提案的互动情况

```bash
curl "https://readycrm.netlify.app/api/tracking/proposal?leadId=rp_abc123" \
  -H "x-admin-token: YOUR_TOKEN"
```

### 列出潜在客户（筛选与排序）

```bash
curl "https://readycrm.netlify.app/api/openclaw/leads?status=new&tier=high&limit=50" \
  -H "x-admin-token: YOUR_TOKEN"
```

### 更新潜在客户的状态

```bash
curl -X PATCH https://readycrm.netlify.app/api/openclaw/leads \
  -H "Content-Type: application/json" \
  -H "x-admin-token: YOUR_TOKEN" \
  -d '{
    "id": "rp_abc123",
    "status": "qualified"
  }'
```

## 高级功能

### 批量信息补充

```bash
curl -X POST https://readycrm.netlify.app/api/openclaw/enrich/bulk \
  -H "Content-Type: application/json" \
  -H "x-admin-token: YOUR_TOKEN" \
  -d '{
    "leadIds": ["rp_123", "rp_456", "rp_789"]
  }'
```

### 使用 Spider Web 分析潜在客户之间的关联

```bash
curl -X POST https://readycrm.netlify.app/api/openclaw/enrich/spider-web \
  -H "Content-Type: application/json" \
  -H "x-admin-token: YOUR_TOKEN" \
  -d '{
    "leadId": "rp_abc123"
  }'
```

### 销售流程分析

```bash
curl "https://readycrm.netlify.app/api/openclaw/analytics?days=30" \
  -H "x-admin-token: YOUR_TOKEN"
```

### 定价方案

**自行提供账户（BYOA）：**
- 每个工作空间每月 9 美元
- 需要自行提供的资源：Apollo.io API 密钥、Gmail 账户、Calendly 链接
- 永无限制的潜在客户数量和信息补充次数

**托管服务（即将推出）：**
- 一次性设置费用：999 美元
- 我们提供的服务：Apollo.io 信用额度、会议记录转录服务（Recall.ai）、优先支持
- 设置完成后每月费用：99 美元

## 完整的 API 参考文档

请参阅 [OPENCLAW_API.md](../../docs/OPENCLAW_API.md) 以获取完整的 API 端点文档。

## 支持方式

- **代理反馈：** 发送 POST 请求到 /api/openclaw/feedback
- **Discord 社区：** [OpenClaw Community](https://discord.com/invite/clawd)
- **GitHub 问题反馈：** [Protosome-Inc/ReadyCRM](https://github.com/Protosome-Inc/ReadyCRM/issues)

## 为什么选择 ClawCRM 用于 OpenClaw 代理？

传统的 CRM 是为人类设计的，需要用户手动点击各种按钮。而 ClawCRM 是专为 **AI 代理设计的，它们可以通过 API 来执行各种操作。

**主要优势：**
- ✅ **以代理为中心的设计**：所有功能都可通过 API 访问
- ✅ **无需人工干预**：自动信息补充、模板自动填充、邮件发送时间精确控制
- ✅ **内置智能工具**：结合 Apollo.io、Google Deep Search 和潜在客户关联分析功能
- ✅ **易于理解的使用方式**：GET 请求端点会清晰地说明数据结构
- ✅ **一次性的配置流程**：通过 POST 请求到 /api/openclaw/setup 即可配置整个工作空间

**不适合您的场景：**
- ❌ 如果您需要一个带有大量按钮的用户界面
- ❌ 如果您需要企业级的单点登录（SSO）或复杂的企业组织结构
- ❌ 如果您需要一个功能繁杂的 CRM 工具

**适合您的场景：**
- ✅ 如果您是负责管理销售任务的 AI 代理
- ✅ 如果您希望实现自主的销售流程管理
- ✅ 如果您希望以编程方式访问所有系统功能
- ✅ 如果您更看重简洁性和高效性，而非复杂的系统架构

---

**由 ClawCRM EIR 开发 | 基于 OpenClaw 技术支持**