---
name: ABM Outbound
description: 多渠道自动化营销（ABM）系统：可将 LinkedIn 上的链接转化为协调一致的 outbound（外发）营销活动。该系统能够抓取用户资料，并通过 Apollo 工具补充用户的电子邮件和电话信息；通过 Skip Trace 获取用户的邮寄地址；随后通过 Scribeless 工具安排发送邮件的顺序、在 LinkedIn 上发起互动，以及发送手写信件。这是在信息泛滥的收件箱中脱颖而出的“秘密武器”。
---

# ABM 外部营销（Outbound Marketing）

将 LinkedIn 的潜在客户列表转化为多渠道营销策略：包括电子邮件序列、LinkedIn 联系以及手写信件。

## 先决条件

| 服务 | 用途 | 注册链接 |
|---------|---------|---------|
| **Apify** | LinkedIn 数据抓取、Skip Trace | [apify.com](https://apify.com) |
| **Apollo** | 电子邮件和电话信息补充 | [apollo.io](https://apollo.io) |
| **Scribeless** | 手写信件服务 | [platform.scribeless.co](https://platform.scribeless.co) |
| **Instantly** （可选） | 专业的冷邮件发送服务 | [instantly.ai](https://instantly.ai) |

```bash
export APIFY_API_KEY="your_key"
export APOLLO_API_KEY="your_key"
export SCRIBELESS_API_KEY="your_key"
```

## 营销流程

```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│  1. INPUT   │───▶│  2. SCRAPE  │───▶│  3. ENRICH  │───▶│  4. ADDRESS │───▶│ 5. OUTREACH │
│  LinkedIn   │    │  Profiles   │    │ Email/Phone │    │ Skip Trace  │    │             │
│    URLs     │    │             │    │             │    │             │    │             │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
   Your list          Apify             Apollo            Apify PFI        Email +
                                                                          LinkedIn +
                                                                          Scribeless
```

## 第一步：收集 LinkedIn 用户信息

从以下途径获取 LinkedIn 用户的 URL：
- LinkedIn Sales Navigator 的导出数据
- LinkedIn 搜索结果
- 客户关系管理（CRM）系统的数据
- 手动收集的潜在客户信息

```csv
linkedin_url
https://linkedin.com/in/johndoe
https://linkedin.com/in/janesmith
```

## 第二步：抓取 LinkedIn 用户信息

```bash
curl -X POST "https://api.apify.com/v2/acts/harvestapi~linkedin-profile-scraper/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "profileUrls": [
      "https://linkedin.com/in/johndoe",
      "https://linkedin.com/in/janesmith"
    ]
  }'
```

**返回信息：** 名字、姓氏、公司名称、职位、所在地区。

## 第三步：使用 Apollo 服务补充信息（电子邮件和电话）

```bash
curl -X POST "https://api.apollo.io/api/v1/people/bulk_match" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "reveal_personal_emails": true,
    "reveal_phone_number": true,
    "details": [{
      "first_name": "John",
      "last_name": "Doe",
      "organization_name": "Acme Corp",
      "linkedin_url": "https://linkedin.com/in/johndoe"
    }]
  }'
```

**返回信息：** 工作邮箱地址和电话号码。

## 第四步：获取邮寄地址（使用 Skip Trace 服务）

```bash
curl -X POST "https://api.apify.com/v2/acts/one-api~skip-trace/run-sync-get-dataset-items" \
  -H "Authorization: Bearer $APIFY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": ["John Doe"]}'
```

**返回信息：** 街道地址、城市、州、邮政编码。

**重要提示：** 确保 Skip Trace 提供的地址与 LinkedIn 上显示的地址一致。

## 第五步：多渠道营销策略

### 5a：电子邮件营销序列

**选项 1：Apollo 电子邮件序列（推荐）**
```bash
curl -X POST "https://api.apollo.io/api/v1/emailer_campaigns/add_contact_ids" \
  -H "X-Api-Key: $APOLLO_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "emailer_campaign_id": "YOUR_SEQUENCE_ID",
    "contact_ids": ["CONTACT_ID_1", "CONTACT_ID_2"],
    "send_email_from_email_account_id": "YOUR_EMAIL_ACCOUNT_ID"
  }'
```

**选项 2：Instantly.ai**
```bash
curl -X POST "https://api.instantly.ai/api/v1/lead/add" \
  -H "Authorization: Bearer $INSTANTLY_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "campaign_id": "YOUR_CAMPAIGN_ID",
    "email": "john@acme.com",
    "first_name": "John",
    "last_name": "Doe",
    "company_name": "Acme Corp",
    "personalization": "Saw Acme just expanded to UK"
  }'
```

**选项 3：通过 CSV 文件上传数据**
```csv
email,first_name,last_name,company,title,phone,personalization
john@acme.com,John,Doe,Acme Corp,VP Marketing,555-1234,Saw Acme just expanded to UK
```

### 5b：LinkedIn 联系策略
- 第 1 天：查看用户资料
- 第 2 天：发送带有个性化信息的联系请求
- 第 4 天：如果对方已接受请求，则发送跟进邮件
- 第 7 天：根据用户分享的内容进行互动

### 5c：手写信件（使用 Scribeless 服务）

在 [platform.scribeless.co](https://platform.scribeless.co) 创建营销活动，然后添加收件人信息：

**更多 API 详情请参考 [references/scribeless-api.md](references/scribeless-api.md)。**

## 营销时间安排协调

| 时间 | 电子邮件 | LinkedIn | 手写信件 |
|-----|-------|----------|--------|
| 1 天 | — | 查看用户资料 | 发送手写信件 |
| 3 天 | — | 发送联系请求 | — |
| 5 天 | “收到我的消息了吗？” | — | 手写信件送达 |
| 7 天 | 发送价值信息邮件 | 如果对方已接受请求，则发送邮件 | — |
| 10 天 | 发送案例研究相关邮件 | — | — |
| 14 天 | 结束联系 | 根据用户分享的内容进行互动 | — |

**营销流程说明：** 首先发送手写信件，随后通过电子邮件提醒对方；最后通过 LinkedIn 进一步加强与对方的联系。

## 完整的工作流程

```python
# 1. Start with LinkedIn URLs
linkedin_urls = load_csv("prospects.csv")

# 2. Scrape profiles
profiles = apify_linkedin_scrape(linkedin_urls)

# 3. Enrich with Apollo
for profile in profiles:
    enriched = apollo_bulk_match(profile)
    profile['email'] = enriched['email']
    profile['phone'] = enriched['phone']

# 4. Get mailing addresses
for profile in profiles:
    address = skip_trace(profile['name'])
    if address['state'] == profile['linkedin_state']:
        profile['address'] = address
        profile['mailable'] = True

# 5. Push to channels
push_to_email_tool(profiles)
push_to_scribeless(profiles, campaign_id)
export_for_linkedin(profiles)
```

## 输出格式

```csv
first_name,last_name,email,phone,company,title,address1,city,state,postal,country,linkedin,mailable
John,Doe,john@acme.com,555-1234,Acme Corp,VP Marketing,123 Main St,San Francisco,CA,94102,US,linkedin.com/in/johndoe,TRUE
```

## 最佳实践：
1. **核实地址**：确保 Skip Trace 提供的地址与 LinkedIn 上显示的地址一致。
2. **个性化沟通**：根据用户的最新信息（如公司动态、工作变动、共同联系人等）进行个性化沟通。
3. **协调发送时间**：确保手写信件在发送“收到我的消息了吗？”邮件之前送达。
4. **从小规模开始**：在扩大规模之前，先对 20-50 名潜在客户进行测试。
5. **按渠道跟踪反馈**：记录哪种营销渠道最能有效引发用户的回复。