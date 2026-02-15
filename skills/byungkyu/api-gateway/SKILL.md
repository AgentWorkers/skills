---
name: api-gateway
description: |
  API gateway for calling third-party APIs with managed auth. Use this skill when users want to interact with external services like Slack, HubSpot, Salesforce, Google Workspace, Stripe, and more.
compatibility: Requires network access and valid Maton API key
metadata:
  author: maton
  version: "1.0"
  clawdbot:
    emoji: 🧠
    homepage: "https://maton.ai"
    requires:
      env:
        - MATON_API_KEY
---

# API网关

该API网关充当一个代理服务器，用于通过受管理的身份验证连接直接访问第三方API，支持直接调用这些API的端点。

## 快速入门

```bash
# Native Slack API call
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'channel': 'C0123456', 'text': 'Hello from gateway!'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/slack/api/chat.postMessage', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 基本URL

```
https://gateway.maton.ai/{app}/{native-api-path}
```

请将 `{app}` 替换为服务名称，将 `{native-api-path}` 替换为实际的API端点路径。

**重要提示**：URL路径必须以对应的应用程序名称开头（例如 `/google-mail/`）。这个前缀用于告诉网关使用哪个应用程序的连接。例如，Gmail的API路径以 `gmail/v1/` 开头，因此完整的路径应为 `/google-mail/gmail/v1/users/me/messages`。

## 身份验证

所有请求都需要在 `Authorization` 头部包含 Maton API 密钥：

```
Authorization: Bearer $MATON_API_KEY
```

API网关会自动为目标服务注入适当的 OAuth 令牌。

**环境变量**：您可以将 API 密钥设置为 `MATON_API_KEY` 环境变量：

```bash
export MATON_API_KEY="YOUR_API_KEY"
```

## 获取API密钥

1. 在 [maton.ai](https://maton.ai) 上登录或创建账户。
2. 访问 [maton.ai/settings](https://maton.ai/settings)。
3. 点击 API Key 部分右侧的复制按钮来复制密钥。

## 连接管理

连接管理使用一个单独的基地址：`https://ctrl.maton.ai`

### 列出连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=slack&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**查询参数（可选）：**
- `app` - 按服务名称过滤（例如 `slack`、`hubspot`、`salesforce`）
- `status` - 按连接状态过滤（`ACTIVE`、`PENDING`、`FAILED`）

**响应：**
```json
{
  "connections": [
    {
      "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
      "status": "ACTIVE",
      "creation_time": "2025-12-08T07:20:53.488460Z",
      "last_updated_time": "2026-01-31T20:03:32.593153Z",
      "url": "https://connect.maton.ai/?session_token=5e9...",
      "app": "slack",
      "metadata": {}
    }
  ]
}
```

### 创建连接

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'app': 'slack'}).encode()
req = urllib.request.Request('https://ctrl.maton.ai/connections', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 获取连接信息

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

**响应：**
```json
{
  "connection": {
    "connection_id": "21fd90f9-5935-43cd-b6c8-bde9d915ca80",
    "status": "ACTIVE",
    "creation_time": "2025-12-08T07:20:53.488460Z",
    "last_updated_time": "2026-01-31T20:03:32.593153Z",
    "url": "https://connect.maton.ai/?session_token=5e9...",
    "app": "slack",
    "metadata": {}
  }
}
```

在浏览器中打开返回的 URL 以完成 OAuth 认证。

### 删除连接

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections/{connection_id}', method='DELETE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 指定连接

如果您为同一应用程序拥有多个连接，可以通过添加 `Maton-Connection` 头部并指定连接 ID 来选择使用哪个连接：

```bash
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'channel': 'C0123456', 'text': 'Hello!'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/slack/api/chat.postMessage', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Maton-Connection', '21fd90f9-5935-43cd-b6c8-bde9d915ca80')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

如果省略此头部，网关将使用该应用程序的默认（最旧的）活动连接。

## 支持的服务

| 服务 | 应用程序名称 | 代理基地址 |
|---------|----------|------------------|
| ActiveCampaign | `active-campaign` | `{account}.api-us1.com` |
| Acuity Scheduling | `acuity-scheduling` | `acuityscheduling.com` |
| Airtable | `airtable` | `api.airtable.com` |
| Apollo | `apollo` | `api.apollo.io` |
| Asana | `asana` | `app.asana.com` |
| Attio | `attio` | `api.attio.com` |
| Basecamp | `basecamp` | `3.basecampapi.com` |
| beehiiv | `beehiiv` | `api.beehiiv.com` |
| Box | `box` | `api.box.com` |
| Brevo | `brevo` | `api.brevo.com` |
| Calendly | `calendly` | `api.calendly.com` |
| Cal.com | `cal-com` | `api.cal.com` |
| CallRail | `callrail` | `api.callrail.com` |
| Chargebee | `chargebee` | `{subdomain}.chargebee.com` |
| ClickFunnels | `clickfunnels` | `{subdomain}.myclickfunnels.com` |
| ClickSend | `clicksend` | `rest.clicksend.com` |
| ClickUp | `clickup` | `api.clickup.com` |
| Coda | `coda` | `coda.io` |
| CompanyCam | `companycam` | `api.companycam.com` |
| Cognito Forms | `cognito-forms` | `www.cognitoforms.com` |
| Constant Contact | `constant-contact` | `api.cc.email` |
| Dropbox | `dropbox` | `api.dropboxapi.com` |
| ElevenLabs | `elevenlabs` | `api.elevenlabs.io` |
| Eventbrite | `eventbrite` | `www.eventbriteapi.com` |
| Fathom | `fathom` | `api.fathom.ai` |
| Fireflies | `fireflies` | `api.fireflies.ai` |
| GitHub | `github` | `api.github.com` |
| Gumroad | `gumroad` | `api.gumroad.com` |
| Google Ads | `google-ads` | `googleads.googleapis.com` |
| Google Analytics Admin | `google-analytics-admin` | `analyticsadmin.googleapis.com` |
| Google Analytics Data | `google-analytics-data` | `analyticsdata.googleapis.com` |
| Google Calendar | `google-calendar` | `www.googleapis.com` |
| Google Contacts | `google-contacts` | `people.googleapis.com` |
| Google Docs | `google-docs` | `docs.googleapis.com` |
| Google Drive | `google-drive` | `www.googleapis.com` |
| Google Forms | `google-forms` | `forms.googleapis.com` |
| Gmail | `google-mail` | `gmail.googleapis.com` |
| Google Merchant | `google-merchant` | `merchantapi.googleapis.com` |
| Google Meet | `google-meet` | `meet.googleapis.com` |
| Google Play | `google-play` | `androidpublisher.googleapis.com` |
| Google Search Console | `google-search-console` | `www.googleapis.com` |
| Google Sheets | `google-sheets` | `sheets.googleapis.com` |
| Google Slides | `google-slides` | `slides.googleapis.com` |
| Google Tasks | `google-tasks` | `tasks.googleapis.com` |
| Google Workspace Admin | `google-workspace-admin` | `admin.googleapis.com` |
| HubSpot | `hubspot` | `api.hubapi.com` |
| Instantly | `instantly` | `api.instantly.ai` |
| Jira | `jira` | `api.atlassian.com` |
| Jobber | `jobber` | `api.getjobber.com` |
| JotForm | `jotform` | `api.jotform.com` |
| Keap | `keap` | `api.infusionsoft.com` |
| Kit | `kit` | `api.kit.com` |
| Klaviyo | `klaviyo` | `a.klaviyo.com` |
| Lemlist | `lemlist` | `api.lemlist.com` |
| Linear | `linear` | `api.linear.app` |
| LinkedIn | `linkedin` | `api.linkedin.com` |
| Mailchimp | `mailchimp` | `{dc}.api.mailchimp.com` |
| MailerLite | `mailerlite` | `connect.mailerlite.com` |
| Mailgun | `mailgun` | `api.mailgun.net` |
| ManyChat | `manychat` | `api.manychat.com` |
| Microsoft Excel | `microsoft-excel` | `graph.microsoft.com` |
| Microsoft To Do | `microsoft-to-do` | `graph.microsoft.com` |
| Monday.com | `monday` | `api.monday.com` |
| Netlify | `netlify` | `api.netlify.com` |
| Notion | `notion` | `api.notion.com` |
| OneDrive | `one-drive` | `graph.microsoft.com` |
| Outlook | `outlook` | `graph.microsoft.com` |
| PDF.co | `pdf-co` | `api.pdf.co` |
| Pipedrive | `pipedrive` | `api.pipedrive.com` |
| Podio | `podio` | `api.podio.com` |
| QuickBooks | `quickbooks` | `quickbooks.api.intuit.com` |
| Quo | `quo` | `api.openphone.com` |
| Salesforce | `salesforce` | `{instance}.salesforce.com` |
| SignNow | `signnow` | `api.signnow.com` |
| Slack | `slack` | `slack.com` |
| Square | `squareup` | `connect.squareup.com` |
| Stripe | `stripe` | `api.stripe.com` |
| Systeme.io | `systeme` | `api.systeme.io` |
| Tally | `tally` | `api.tally.so` |
| Telegram | `telegram` | `api.telegram.org` |
| TickTick | `ticktick` | `api.ticktick.com` |
| Todoist | `todoist` | `api.todoist.com` |
| Trello | `trello` | `api.trello.com` |
| Twilio | `twilio` | `api.twilio.com` |
| Typeform | `typeform` | `api.typeform.com` |
| Vimeo | `vimeo` | `api.vimeo.com` |
| WhatsApp Business | `whatsapp-business` | `graph.facebook.com` |
| WooCommerce | `woocommerce` | `{store-url}/wp-json/wc/v3` |
| WordPress.com | `wordpress` | `public-api.wordpress.com` |
| Xero | `xero` | `api.xero.com` |
| YouTube | `youtube` | `www.googleapis.com` |
| Zoho Bigin | `zoho-bigin` | `www.zohoapis.com` |
| Zoho Books | `zoho-books` | `www.zohoapis.com` |
| Zoho Calendar | `zoho-calendar` | `calendar.zoho.com` |
| Zoho CRM | `zoho-crm` | `www.zohoapis.com` |
| Zoho Inventory | `zoho-inventory` | `www.zohoapis.com` |
| Zoho Mail | `zoho-mail` | `mail.zoho.com` |
| Zoho People | `zoho-people` | `people.zoho.com` |
| Zoho Recruit | `zoho-recruit` | `recruit.zoho.com` |

有关每个提供者的详细路由指南，请参阅 [references/](references/)：
- [ActiveCampaign](references/active-campaign.md) - 联系人、交易、标签、列表、自动化、活动
- [Acuity Scheduling](references/acuity-scheduling.md) - 预约、日历、客户、可用性
- [Airtable](references/airtable.md) - 记录、数据库、表格
- [Apollo](references/apollo.md) - 人员搜索、信息补充、联系人
- [Asana](references/asana.md) - 任务、项目、工作空间、Webhook
- [Attio](references/attio.md) - 人员、公司、记录、任务
- [Basecamp](references/basecamp.md) - 项目、待办事项、消息、日程安排、文档
- [beehiiv](references/beehiiv.md) - 发布物、订阅、帖子、自定义字段
- [Box](references/box.md) - 文件、文件夹、协作、共享链接
- [Brevo](references/brevo.md) - 联系人、电子邮件活动、交易邮件、模板
- [Calendly](references/calendly.md) - 活动类型、预定事件、可用性、Webhook
- [Cal.com](references/cal-com.md) - 活动类型、预订、日程安排、可用时间、Webhook
- [CallRail](references/callrail.md) - 呼叫、跟踪器、公司、标签、分析
- [Chargebee](references/chargebee.md) - 订阅、客户、发票
- [ClickFunnels](references/clickfunnels.md) - 联系人、产品、订单、课程、Webhook
- [ClickSend](references/clicksend.md) - SMS、MMS、语音消息、联系人、列表
- [ClickUp](references/clickup.md) - 任务、列表、文件夹、空间、Webhook
- [Coda](references/coda.md) - 文档、页面、表格、行、公式、控件
- [CompanyCam](references/companycam.md) - 项目、照片、用户、标签、组、文档
- [Cognito Forms](references/cognito-forms.md) - 表单、条目、文档、文件
- [Constant Contact](references/constant-contact.md) - 联系人、电子邮件活动、列表、细分
- [Dropbox](references/dropbox.md) - 文件、文件夹、搜索、元数据、修订、标签
- [ElevenLabs](references/elevenlabs.md) - 文本转语音、语音克隆、音频处理
- [Eventbrite](references/eventbrite.md) - 活动、场地、票务、订单、参与者
- [Fathom](references/fathom.md) - 会议记录、摘要、总结、Webhook
- [Fireflies](references/fireflies.md) - 会议记录、摘要、AskFred AI、频道
- [GitHub](references/github.md) - 仓库、问题、拉取请求、提交
- [Gumroad](references/gumroad.md) - 产品、销售、订阅者、许可证、Webhook
- [Google Ads](references/google-ads.md) - 活动、广告组、GAQL 查询
- [Google Analytics Admin](references/google-analytics-admin.md) - 报告、维度、指标
- [Google Analytics Data](references/google-analytics-data.md) - 报告、维度、指标
- [Google Calendar](references/google-calendar.md) - 活动、日历、忙/空
- [Google Contacts](references/google-contacts.md) - 联系人、联系人组、人员搜索
- [Google Docs](references/google-docs.md) - 文档创建、批量更新
- [Google Drive](references/google-drive.md) - 文件、文件夹、权限
- [Google Forms](references/google-forms.md) - 表单、问题、回复
- [Gmail](references/google-mail.md) - 消息、线程、标签
- [Google Meet](references/google-meet.md) - 空间、会议记录、参与者
- [Google Merchant](references/google-merchant.md) - 产品、库存、促销、报告
- [Google Play](references/google-play.md) - 应用内产品、订阅、评论
- [Google Search Console](references/google-search-console.md) - 搜索分析、站点地图
- [Google Sheets](references/google-sheets.md) - 值、范围、格式
- [Google Slides](references/google-slides.md) - 演示文稿、幻灯片、格式
- [Google Tasks](references/google-tasks.md) - 任务列表、任务、子任务
- [Google Workspace Admin](references/google-workspace-admin.md) - 用户、组、组织单位、域名、角色
- [HubSpot](references/hubspot.md) | 联系人、公司、交易
- [Instantly](references/instantly.md) | 活动、潜在客户、账户、电子邮件推广
- [Jira](references/jira.md) | 问题、项目、JQL 查询
- [Jobber](references/jobber.md) | 客户、工作、发票、报价（GraphQL）
- [JotForm](references/jotform.md) | 表单、提交、Webhook
- [Keap](references/keap.md) | 联系人、公司、标签、任务、机会、活动
- [Kit](references/kit.md) | 订阅者、标签、表单、序列、广播
- [Klaviyo](references/klaviyo.md) | 轮廓、列表、活动、事件
- [Lemlist](references/lemlist.md) | 活动、潜在客户、活动、日程安排、取消订阅
- [Linear](references/linear.md) | 问题、项目、团队、周期（GraphQL）
- [LinkedIn](references/linkedin.md) | 轮廓、帖子、分享、媒体上传
- [Mailchimp](references/mailchimp.md) | 目标群体、活动、模板、自动化
- [MailerLite](references/mailerlite.md) | 订阅者、组、活动、自动化、表单
- [Mailgun](references/mailgun.md) | 发送电子邮件、域名、路由、模板、邮件列表、抑制
- [ManyChat](references/manychat.md) | 订阅者、标签、流程、消息
- [Microsoft Excel](references/microsoft-excel.md) | 工作簿、工作表、范围、表格
- [Microsoft To Do](references/microsoft-to-do.md) | 任务列表、任务、待办事项列表、链接资源
- [Monday.com](references/monday.md) | 工作板、项目、列、组（GraphQL）
- [Netlify](references/netlify.md) | 站点、部署、构建、DNS、环境变量
- [Notion](references/notion.md) | 页面、数据库、区块
- [OneDrive](references/one-drive.md) | 文件、文件夹、驱动器、共享
- [Outlook](references/outlook.md) | 邮件、日历、联系人
- [PDF.co](references/pdf-co.md) | PDF 转换、合并、分割、编辑、文本提取、条形码
- [Pipedrive](references/pipedrive.md) | 交易、人员、组织、活动
- [Podio](references/podio.md) | 组织、工作空间、应用程序、项目、任务、评论
- [QuickBooks](references/quickbooks.md) | 客户、发票、报告
- [Quo](references/quo.md) | 呼叫、消息、联系人、对话、Webhook
- [Salesforce](references/salesforce.md) | SOQL、sObjects、CRUD
- [SignNow](references/signnow.md) | 文档、模板、邀请、电子签名
- [SendGrid](references/sendgrid.md) | 发送电子邮件、联系人、模板、抑制、统计
- [Slack](references/slack.md) | 消息、频道、用户
- [Square](references/squareup.md) | 支付、客户、订单、目录、库存、发票
- [Stripe](references/stripe.md) | 客户、订阅、支付
- [Systeme.io](references/systeme.md) | 联系人、标签、课程、社区、Webhook
- [Tally](references/tally.md) | 表单、提交、工作空间、Webhook
- [Telegram](references/telegram.md) | 消息、聊天、机器人、更新、投票
- [TickTick](references/ticktick.md) | 任务、项目、任务列表
- [Todoist](references/todoist.md) | 任务、项目、部分、标签、评论
- [Trello](references/trello.md) | 工作板、列表、卡片、检查列表
- [Twilio](references/twilio.md) | SMS、语音通话、电话号码、消息
- [Typeform](references/typeform.md) | 表单、回复、洞察
- [Vimeo](references/vimeo.md) | 视频、文件夹、相册、评论
- [WhatsApp Business](references/whatsapp-business.md) | 消息、模板、媒体
- [WooCommerce](references/woocommerce.md) | 产品、订单、客户、优惠券
- [WordPress.com](references/wordpress.md) | 文章、页面、站点、用户、设置
- [Xero](references/xero.md) | 联系人、发票、报告
- [YouTube](references/youtube.md) | 视频、播放列表、频道、订阅
- [Zoho Bigin](references/zoho-bigin.md) | 联系人、公司、管道、产品
- [Zoho Books](references/zoho-books.md) | 发票、联系人、账单
- [Zoho Calendar](references/zoho-calendar.md) | 日历、活动、参与者
- [Zoho CRM](references/zoho-crm.md) | 潜在客户、联系人、账户、交易
- [Zoho Inventory](references/zoho-inventory.md) | 项目、销售订单、发票、采购订单
- [Zoho Mail](references/zoho-mail.md) | 消息、文件夹、标签
- [Zoho People](references/zoho-people.md) | 员工、部门、职位、出勤
- [Zoho Recruit](references/zoho-recruit.md) | 应聘者、职位空缺、面试、申请

## 示例

### Slack - 发送消息（原生API）

```bash
# Native Slack API: POST https://slack.com/api/chat.postMessage
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'channel': 'C0123456', 'text': 'Hello!'}).encode()
req = urllib.request.Request('https://gateway.maton.ai/slack/api/chat.postMessage', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json; charset=utf-8')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### HubSpot - 创建联系人（原生API）

```bash
# Native HubSpot API: POST https://api.hubapi.com/crm/v3/objects/contacts
python <<'EOF'
import urllib.request, os, json
data = json.dumps({'properties': {'email': 'john@example.com', 'firstname': 'John', 'lastname': 'Doe'}}).encode()
req = urllib.request.Request('https://gateway.maton.ai/hubspot/crm/v3/objects/contacts', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Google Sheets - 获取电子表格值（原生API）

```bash
# Native Sheets API: GET https://sheets.googleapis.com/v4/spreadsheets/{id}/values/{range}
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/google-sheets/v4/spreadsheets/122BS1sFN2RKL8AOUQjkLdubzOwgqzPT64KfZ2rvYI4M/values/Sheet1!A1:B2')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Salesforce - SOQL 查询（原生API）

```bash
# Native Salesforce API: GET https://{instance}.salesforce.com/services/data/v64.0/query?q=...
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/salesforce/services/data/v64.0/query?q=SELECT+Id,Name+FROM+Contact+LIMIT+10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Airtable - 列出表格（原生API）

```bash
# Native Airtable API: GET https://api.airtable.com/v0/meta/bases/{id}/tables
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/airtable/v0/meta/bases/appgqan2NzWGP5sBK/tables')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Notion - 查询数据库（原生API）

```bash
# Native Notion API: POST https://api.notion.com/v1/data_sources/{id}/query
python <<'EOF'
import urllib.request, os, json
data = json.dumps({}).encode()
req = urllib.request.Request('https://gateway.maton.ai/notion/v1/data_sources/23702dc5-9a3b-8001-9e1c-000b5af0a980/query', data=data, method='POST')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
req.add_header('Content-Type', 'application/json')
req.add_header('Notion-Version', '2025-09-03')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### Stripe - 列出客户（原生API）

```bash
# Native Stripe API: GET https://api.stripe.com/v1/customers
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://gateway.maton.ai/stripe/v1/customers?limit=10')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

## 代码示例

### JavaScript (Node.js)

```javascript
const response = await fetch('https://gateway.maton.ai/slack/api/chat.postMessage', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': `Bearer ${process.env.MATON_API_KEY}`
  },
  body: JSON.stringify({ channel: 'C0123456', text: 'Hello!' })
});
```

### Python

```python
import os
import requests

response = requests.post(
    'https://gateway.maton.ai/slack/api/chat.postMessage',
    headers={'Authorization': f'Bearer {os.environ["MATON_API_KEY"]}'},
    json={'channel': 'C0123456', 'text': 'Hello!'}
)
```

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 请求的应用程序连接缺失 |
| 401 | Maton API 密钥无效或缺失 |
| 429 | 每个账户每秒请求次数限制（10次） |
| 500 | 内部服务器错误 |
| 4xx/5xx | 来自目标API的传递错误 |

目标API返回的错误会保留其原始的状态码和响应体。

### 故障排除：API密钥问题

1. 确保设置了 `MATON_API_KEY` 环境变量：

```bash
echo $MATON_API_KEY
```

2. 通过列出连接来验证API密钥是否有效：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：应用程序名称无效

1. 确保您的URL路径以正确的应用程序名称开头。路径必须以 `/google-mail/` 开头。例如：
- 正确：`https://gateway.maton.ai/google-mail/gmail/v1/users/me/messages`
- 错误：`https://gateway.maton.ai/gmail/v1/users/me/messages`

2. 确保您有该应用程序的活跃连接。列出您的连接以进行验证：

```bash
python <<'EOF'
import urllib.request, os, json
req = urllib.request.Request('https://ctrl.maton.ai/connections?app=google-mail&status=ACTIVE')
req.add_header('Authorization', f'Bearer {os.environ["MATON_API_KEY"]}')
print(json.dumps(json.load(urllib.request.urlopen(req)), indent=2))
EOF
```

### 故障排除：服务器错误

500 错误可能表示OAuth令牌已过期。尝试通过上面的连接管理部分创建新的连接并完成OAuth认证。如果新连接处于“ACTIVE”状态，请删除旧连接，以确保网关使用新的连接。

## 请求限制

- 每个账户每秒10次请求
- 目标API也有自己的请求限制

## 注意事项

- 当使用 `curl` 并且URL包含方括号（`fields[]`、`sort[]`、`records[]`）时，请使用 `-g` 标志以禁用全局解析。
- 当将 `curl` 输出传递给 `jq` 时，某些shell环境中环境变量可能无法正确展开，这可能导致“无效API密钥”错误。

## 提示

1. **使用原生API文档**：请参考每个服务的官方API文档以获取端点路径和参数。
2. **头部信息会被转发**：自定义头部（`Host` 和 `Authorization` 除外）会被转发到目标API。
3. **查询参数有效**：URL查询参数会被传递给目标API。
4. **支持所有HTTP方法**：支持 GET、POST、PUT、PATCH、DELETE。
5. **QuickBooks的特殊情况**：在路径中使用 `:realmId`，它将被替换为连接的领域ID。

## 可选资源

- [Github](https://github.com/maton-ai/api-gateway-skill)
- [API参考](https://www.maton.ai/docs/api-reference)
- [Maton社区](https://discord.com/invite/dBfFAcefs2)
- [Maton支持](mailto:support@maton.ai)