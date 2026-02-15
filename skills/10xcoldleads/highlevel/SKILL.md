---
name: highlevel
version: 1.1.0
description: "将您的 AI 助手通过官方 API v2 连接到 GoHighLevel CRM。通过自然语言界面，您可以管理联系人、对话记录、日历、工作流程、发票、付款信息以及 30 多个端点组。系统提供交互式的设置向导，并内置了 40 多个安全可靠的 API 命令。仅支持 Python 3.6 及更高版本的标准库，无需任何外部依赖。"
tags: [gohighlevel, crm, api, contacts, conversations, calendars, opportunities, invoices, workflows, automation]
author: Ty Shane
homepage: https://launchmyopenclaw.com
compatibility: "Requires Python 3.6+ (stdlib only, no pip installs). Requires two environment variables: HIGHLEVEL_TOKEN and HIGHLEVEL_LOCATION_ID."
---

# GoHighLevel API 技能

> **将您的人工智能助手转变为一个 GoHighLevel 命令中心。** 使用简单的英语，您可以搜索联系人、发送消息、预约、管理销售流程、创建发票、安排社交媒体帖子——涵盖所有 39 个 GHL API v2 终端点组。

**还没有 GoHighLevel 吗？** 从免费的 5 天 AI 员工挑战开始，构建一个完全自动化的系统：
👉 [**开始 5 天 AI 员工挑战**](https://gohighlevel.com/5-day-challenge?fp_ref=369ai)

## 要求

| 要求 | 详情 |
|-------------|---------|
| **运行时** | Python 3.6+（仅使用标准库：`urllib`、`json`、`os`、`re`、`sys`、`time`） |
| **外部包** | **无** — 无需安装任何包 |
| **环境变量** | `HIGHLEVEL_TOKEN`（主要环境变量——您的私有集成令牌） |
| | `HIGHLEVEL_LOCATION_ID`（您的子账户位置 ID） |
| **网络访问** | 仅限通过 HTTPS 访问 `services.leadconnectorhq.com` |

**基础 URL**: `https://services.leadconnectorhq.com`
**必需的请求头**: `Authorization: Bearer $HIGHLEVEL_TOKEN` + `Version: 2021-07-28`
**速率限制**: 每 10 秒内允许 100 次请求，每个位置每天最多 200,000 次请求

## 安全设计

所有 API 函数都使用预定义的端点路径——不允许随意发送 HTTP 请求。每个用户提供的 ID 都会经过严格的字母数字正则表达式 (`^[a-zA-Z0-9_-]{1,128}`) 验证，然后再包含在任何 URL 路径中，以防止路径遍历和注入攻击。脚本仅使用 Python 的内置 `urllib.request` 进行所有网络调用。不使用 shell 命令，不执行外部二进制文件操作，也不会将数据写入文件系统之外。

## 设置 — `/highlevel-setup`

如果用户输入 “set up highlevel”、“connect my GHL” 或 “/highlevel-setup”，则会运行设置向导：

```bash
python3 scripts/setup-wizard.py
```

向导会自动：
- 检查环境变量
- 指导创建私有集成
- 测试连接
- 获取前 5 个联系人作为快速验证结果。

### 手动设置（如果向导无法运行）

#### 第 1 步：创建私有集成（不要使用旧的 API 密钥方法）
1. 登录到 **app.gohighlevel.com**
2. 切换到您的 **子账户**（建议用于单位置使用）
3. 点击 **设置**（左下角的齿轮图标）
4. 在左侧边栏中选择 **私有集成**
   - 如果没有显示，请先启用它：设置 → 实验室 → 打开私有集成
5. 点击 **“创建新集成”
6. 输入名称（例如：“Claude AI Assistant”）和描述
7. **仅授予所需的权限范围**（建议使用最小权限）：

   | 使用场景 | 推荐权限范围 |
   |----------|--------------------|
   | 仅限联系人管理 | `contacts.readonly`, `contacts.write` |
   | 联系人 + 消息传递 | 上述权限 + `conversations.readonly`, `conversations.write`, `conversations/message.write` |
   | 全面 CRM（联系人、日历、销售流程） | 上述权限 + `calendars.readonly`, `calendars.write`, `opportunities.readonly`, `opportunities.write` |
   | 添加工作流和发票 | 上述权限 + `workflows.readonly`, `invoices.readonly`, `invoices.write` |
   | 仅限读取报告 | `contacts.readonly`, `opportunities.readonly`, `calendars.readonly`, `invoices.readonly`, `locations.readonly` |

   您可以在之后的设置 → 私有集成 → 编辑中随时添加更多权限范围，而无需重新生成令牌。

8. 点击创建 → **立即复制令牌** — 令牌仅显示一次，之后无法再次获取

#### 机构集成与子账户集成

| 功能 | 机构集成 | 子账户集成 |
|---------|-------------------|------------------------|
| 创建位置 | 机构设置 → 私有集成 | 子账户设置 → 私有集成 |
| 访问范围 | 机构及所有子账户（通过 `locationId` 参数传递） | 仅限单个位置 |
| 可用权限范围 | 包括 `locations.write`、`oauth.*`、`saas.*`、`snapshots.*`、`companies.readonly` 的所有权限 | 仅限子账户权限 |
| 适用场景 | 多位置管理、SaaS 配置器 | 单客户集成（推荐默认设置） |

> **建议：** 先从子账户集成开始，并使用最低权限范围。如果需要多位置访问，可以 later 升级到机构级别。

### 第 2 步：获取您的位置 ID
1. 在子账户中，转到 **设置** → **业务信息**（或 **业务资料**）
2. **位置 ID** 会显示在一般信息部分
3. 或者：查看地址栏——它是在 `app.gohighlevel.com/v2/location/{LOCATION_ID}/...` 中 `/location/` 之后的 ID

### 第 3 步：设置环境变量
```bash
export HIGHLEVEL_TOKEN="your-private-integration-token"
export HIGHLEVEL_LOCATION_ID="your-location-id"
```

### 第 4 步：测试连接
运行 `python3 scripts/ghl-api.py test_connection` — 应该会返回位置名称和状态。

设置成功后，获取前 5 个联系人作为快速验证结果，以确保一切正常工作。

## 辅助脚本

`scripts/ghl-api.py` — 一个可执行的 Python 脚本（仅使用标准库），具有内置的重试逻辑、分页功能、输入验证和错误处理。

**核心命令**：
| 命令 | 描述 |
|---------|-------------|
| `test_connection` | 验证令牌和位置 ID 是否有效 |
| `search_contacts [query]` | 按名称、电子邮件或电话号码搜索联系人 |
| `get_contact [id]` | 获取联系人的完整信息 |
| `create_contact [json]` | 创建新联系人 |
| `update_contact [id] [json]` | 更新联系人信息 |
| `list_opportunities` | 列出销售流程中的机会 |
| `list_conversations` | 列出最近的对话记录 |
| `send_message [contactId] [message] | 发送短信/电子邮件 |
| `list_calendars` | 列出所有日历 |
| `get_free_slots [calendarId] [startDate] [endDate]` | 可用的预订时段 |
| `list_workflows` | 列出所有工作流 |
| `add_to_workflow [contactId] [workflowId] | 将联系人添加到工作流 |
| `list_invoices` | 列出发票 |
| `list_products` | 列出产品 |
| `list_forms` | 列出表单 |
| `list_campaigns` | 列出活动 |
| `get_location_details` | 获取位置信息 |
| `list_location_tags` | 列出位置标签 |
| `list_courses` | 列出课程/会员信息 |

所有函数都使用安全的、预定义的 API 端点，不允许随意发送请求。

## 完整的 API v2 覆盖范围（39 个终端点组）

该技能提供了针对所有主要 GHL 操作的安全、特定的功能。每个功能都映射到一个特定的、允许的 API 端点，并且参数经过验证。

| # | 组 | 基础路径 | 主要操作 | 权限前缀 |
|---|-------|-----------|----------------|-------------|
| 1 | **联系人** | `/contacts/` | 创建/读取/更新/删除联系人、搜索、添加标签、备注、任务、批量操作 | `contacts` |
| 2 | **对话记录** | `/conversations/` | 搜索、发送消息（短信/电子邮件/WhatsApp/FB/IG/聊天）、录音 | `conversations` |
| 3 | **日历** | `/calendars/` | 创建/读取/更新日历、预订时段、分组、资源 | `calendars` |
| 4 | **机会** | `/opportunities/` | 创建/读取/更新机会、搜索、管理销售流程、阶段、状态、跟踪者 | `opportunities` |
| 5 | **工作流** | `/workflows/` | 列出工作流、将联系人添加到工作流/从工作流中移除 | `workflows` |
| 6 | **活动** | `/campaigns/` | 列出活动（仅限读取） | `campaigns` |
| 7 | **发票** | `/invoices/` | 创建/读取/更新发票、发送发票、取消订单、记录付款、Text2Pay、安排付款、估算 | `invoices` |
| 8 | **支付** | `/payments/` | 订单、交易、订阅、优惠券、供应商 | `payments` |
| 9 | **产品** | `/products/` | 创建/读取产品信息、价格、收藏、评论、商店统计 | `products` |
| 10 | **位置** | `/locations/` | 获取/更新位置信息、自定义字段、自定义值、标签、模板 | `locations` |
| 11 | **用户** | `/users/` | 创建/读取用户信息、按电子邮件/角色过滤 | `users` |
| 12 | **表单** | `/forms/` | 列出表单、获取表单提交 | `forms` |
| 13 | **调查** | `/surveys/` | 列出调查问卷、获取表单提交 | `surveys` |
| 14 | **漏斗** | `/funnels/` | 列出漏斗、页面、重定向 | `funnels` |
| 15 | **社交媒体发布** | `/social-media-posting/` | 发布内容、管理账户、导入 CSV 文件、分类、统计信息 | `socialplanner` |
| 16 | **博客** | `/blogs/` | 创建/更新博客文章、分类、作者信息 | `blogs` |
| 17 | **电子邮件** | `/emails/` | 创建/更新电子邮件模板、安排电子邮件发送 | `emails` |
| 18 | **媒体** | `/medias/` | 上传/列出/删除媒体文件 | `medias` |
| 19 | **触发链接** | `/links/` | 创建/更新触发链接 | `links` |
| 20 | **企业** | `/businesses/` | 创建/读取企业信息 | `businesses` |
| 21 | **公司** | `/companies/` | 获取公司详细信息（机构专用） | `companies` |
| 22 | **自定义对象** | `/objects/` | 创建/读取自定义对象信息 | `objects` |
| 23 | **关联** | `/associations/` | 创建/读取关联关系 | `associations` |
| 24 | **提案/文档** | `/proposals/` | 创建/读取提案/合同 | `documents_contracts` |
| 25 | **快照** | `/snapshots/` | 列出快照、查看状态、分享链接（机构专用） | `snapshots` |
| 26 | **SaaS** | `/saas/` | 管理订阅、计划、批量操作（机构版需支付 497 美元） | `saas` |
| 27 | **课程** | `/courses/` | 导入课程/会员信息 | `courses` |
| 28 | **语音 AI** | `/voice-ai/` | 查看通话记录、创建/读取代理信息、执行操作、设置目标 | `voice-ai` |
| 29 | **电话系统** | `/phone-system/` | 创建/读取电话号码 | `phonenumbers` |
| 30 | **自定义菜单** | `/custom-menus/` | 创建/读取自定义菜单链接（机构专用） | `custom-menu-link` |
| 31 | **OAuth** | `/oauth/` | 交换令牌、管理已安装的位置 | `oauth` |
| 32 | **市场** | `/marketplace/` | 安装服务、管理账单 | `marketplace` |
| 33 | **对话 AI** | `/conversation-ai/` | 配置 AI 聊天机器人 | — |
| 34 | **知识库** | `/knowledge-base/` | 为 AI 功能提供知识库 | — |
| 35 | **AI 代理工作室** | `/agent-studio/` | 创建/读取自定义 AI 代理信息 | — |
| 36 | **品牌看板** | `/brand-boards/` | 管理品牌看板 | — |
| 37 | **商店** | `/store/` | 管理电子商务商店 | — |
| 38 | **LC 电子邮件** | `/lc-email/` | 电子邮件基础设施（ISV 专用） | — |
| 39 | **自定义字段** | `/locations/:id/customFields/` | 创建/读取自定义字段 | `locations/customFields` |

## 参考文档（按需加载）

有关每个组的详细端点路径、参数和示例，请参阅：
- `references/contacts.md` — 联系人创建/读取/更新、搜索、添加标签、备注、任务、批量操作
- `references/conversations.md` — 跨所有渠道的消息传递、录音、转录
- `references/calendars.md` — 日历创建/读取/更新、预订时段、分组、资源
- `references/opportunities.md` — 销售流程管理、阶段管理、状态更新
- `references/invoices-payments.md` — 发票、支付、订单、订阅、产品
- `references/locations-users.md` | 位置设置、自定义字段/值、用户、标签
- `references/social-media.md` | 社交媒体发布、账户管理、OAuth 连接
- `references/forms-surveys-funnels.md` | 表单、调查问卷、漏斗、触发链接
- `references/advanced.md` | 自定义对象、关联关系、快照、SaaS、语音 AI、博客、课程
- `references/troubleshooting.md` | 常见错误、速率限制、令牌轮换、调试

## 重要说明

- **必须使用私有集成** — 旧的设置 → API 密钥方法已过时/不再支持
- **令牌轮换**：令牌不会自动过期，但 GHL 建议每 90 天轮换一次。未使用的令牌在 90 天未使用后会自动过期
  - **“稍后轮换并过期”** — 生成新令牌，旧令牌在 7 天宽限期内仍然有效
  - **“立即轮换并过期”** — 旧令牌立即失效（用于安全原因）
  - 您可以在不重新生成令牌的情况下修改权限范围
- **OAuth 令牌**（仅限市场应用）：访问令牌在 24 小时后过期；令牌可以刷新，有效期最长为 1 年
- 机构令牌可以通过传递 `locationId` 参数访问子账户数据
- **速率限制是按资源计算的** — 每个子账户每 10 秒内允许 100 次请求，每天最多 200,000 次请求。SaaS 端点：全局每秒 100 次请求
- 所有列表端点默认显示 20 条记录，可以通过 `limit` 参数设置每页最多显示 100 条记录
- 对于大型数据集，使用 `startAfter` / `startAfterId` 进行分页
- 通过响应头监控速率限制：`X-RateLimit-Limit-Daily`、`X-RateLimit-Daily-Remaining`、`X-RateLimit-Max`、`X-RateLimit-Remaining`、`X-RateLimit-Interval-Milliseconds`
- **需要 **497 美元的机构专业版** 才能使用以下功能：SaaS 配置器、快照、全面的机构管理 API

## Webhook 事件

提供 50 多种 webhook 事件类型，用于实时通知。关键事件包括：`ContactCreate`、`ContactDelete`、`ContactTagUpdate`、`InboundMessage`、`OutboundMessage`、`OpportunityCreate`、`OpportunityStageUpdate`、`OpportunityStatusUpdate`、预约事件、支付事件、表单提交事件。即使访问令牌过期，Webhook 事件也会继续触发。配置详情请参阅：https://marketplace.gohighlevel.com/docs/webhook/WebhookIntegrationGuide

## 官方 SDK 和开发者资源

- **Node.js**: `@gohighlevel/api-client`（npm）——支持 `privateIntegrationToken` 配置、自动重试机制
- **Python**: `gohighlevel-api-client`（PyPI）——支持会话存储、自动令牌刷新、Webhook 中间件
- **PHP SDK** 也可用
- 所有 SDK 都使用 `apiVersion: '2021-07-28`
- **OpenAPI 规范**：https://github.com/GoHighLevel/highlevel-api-docs
- **API 文档**：https://marketplace.gohighlevel.com/docs/
- **开发者 Slack**：https://developers.gohighlevel.com/join-dev-community

---

### 由 Ty Shane 开发

[🌐 LaunchMyOpenClaw.com](https://launchmyopenclaw.com) • [🌐 MyFBLeads.com](https://myfbleads.com)
[▶️ YouTube @10xcoldleads](https://youtube.com/@10xcoldleads) • [📘 Facebook](https://facebook.com/ty.shane.howell.2025) • [💼 LinkedIn](https://linkedin.com/in/ty-shane/)
📧 ty@10xcoldleads.com

**还没有 GoHighLevel 账户吗？** → [开始免费的 5 天 AI 员工挑战](https://gohighlevel.com/5-day-challenge?fp_ref=369ai)