---
name: smb-sales-boost
description: 查询和管理来自SMB Sales Boost B2B潜在客户数据库中的潜在客户信息。您可以搜索新注册的企业，按位置/行业/关键词进行筛选，导出潜在客户数据，管理筛选预设设置，并使用基于人工智能的类别推荐功能。使用该功能需要具备有效的SMB Sales Boost订阅资格（Starter、Growth、Scale、Platinum或Enterprise级别），以及API密钥。
---
# SMB销售提升技能

此技能支持与SMB Sales Boost API进行自然语言交互——这是一个B2B潜在客户生成平台，可访问美国各地新注册的小型和中型企业。

## 设置

用户必须提供他们的API密钥。密钥以`smbk_`为前缀，可以在仪表板>API选项卡中生成。该密钥作为Bearer令牌包含在每个请求的Authorization头部中。

**基础URL:** `https://smbsalesboost.com/api/v1`

**重要提示：**API访问需要Starter、Growth、Scale、Platinum或Enterprise订阅计划。新用户可以通过API完全购买订阅服务（无需网站注册）。

## 认证

所有请求都必须包含：
```
Authorization: Bearer <API_KEY>
```

如果用户尚未提供API密钥，请在发送任何请求之前向他们索取。将其存储在一个变量中，以便在整个会话中重复使用。

## 基于信用的系统

Starter、Growth和Scale计划使用**基于信用的模型**来导出潜在客户：

- 每导出一个**新潜在客户**会扣除1个信用点
- 之前导出的潜在客户是免费的（不消耗信用点）
- Platinum和Enterprise计划没有信用点限制

**信用定价（每个信用点）：**
| 计划 | 每个信用点的价格 |
|------|----------------|
| Starter | $0.10 |
| Growth | $0.08 |
| Scale | $0.05 |
| Platinum | $0.03 |
| Enterprise | $0.02 |

用户可以通过`POST /purchase-credits`购买额外的永久信用点。

## 速率限制

- 导出：每5分钟1次
- 电子邮件调度触发：每5分钟1次
- AI类别建议：每分钟5次
- AI关键词生成：每分钟5次
- AI自动优化启用：每分钟5次
- AI自动优化禁用：每分钟60次
- AI自动优化状态：每分钟60次
- AI关键词状态：每分钟60次
- 程序化购买：每个IP每小时5次
- 获取密钥：每个IP每小时30次

速率限制头部会在每个响应中返回：`X-RateLimit-Limit`、`X-RateLimit-Remaining`、`X-RateLimit-Reset`。如果遇到速率限制，请查看`Retry-After`头部以获取等待时间。

## 两种数据库类型

SMB Sales Boost有两个独立的数据库，其中包含不同的联系信息：

1. **`home_improvement`** — 家居改善/承包商企业，包含**电话号码**、星级评分、评论数量、评论片段、个人资料URL和类别
2. **`other`** — 一般新注册的企业，包含**电话号码和电子邮件地址**、注册的URL、爬取的URL、简短/长描述和重定向状态

家居改善数据库主要提供电话号码作为联系方式。其他数据库同时提供电话号码和电子邮件地址，非常适合发送冷邮件和多渠道外展活动。

某些过滤参数仅适用于一种数据库类型。用户的账户有一个默认的数据库设置。始终检查用户想要查询哪个数据库。

---

## 核心端点

### 1. 搜索潜在客户 — `GET /leads`

主要端点。将自然语言查询转换为过滤后的潜在客户搜索。

**关键参数：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `page` | 整数 | 页码（默认：1） |
| `limit` | 整数 | 每页的结果数量（最多1000个，默认100个） |
| `database` | 字符串 | `home_improvement`或`other` |
| `positiveKeywords` | JSON数组字符串 | 要包含的关键词（OR逻辑）。支持`*`通配符进行模式匹配（例如，`["*dental*", "*ortho*"]`）。如果没有通配符，则默认执行子字符串匹配。 |
| `negativeKeywords` | JSON数组字符串 | 要排除的关键词（AND逻辑）。也支持`*`通配符（例如，`["*franchise*"]`）。 |
| `orColumns` | JSON数组字符串 | 根据这些列名称搜索关键词 |
| `search` | 字符串 | 在所有字段中进行全文搜索 |
| `stateInclude` | 字符串 | 用逗号分隔的状态代码：`CA,NY,TX` |
| `stateExclude` | 字符串 | 用逗号分隔要排除的状态代码 |
| `cityInclude` | JSON数组字符串 | 要包含的城市 |
| `cityExclude` | JSON数组字符串 | 要排除的城市 |
| `zipInclude` | JSON数组字符串 | 要包含的邮政编码 |
| `zipExclude` | JSON数组字符串 | 要排除的邮政编码 |
| `nameIncludeTerms` | JSON数组字符串 | 包含在业务名称中的术语 |
| `nameExcludeTerms` | JSON数组字符串 | 从业务名称中排除的术语 |
| `lastUpdatedFrom` | 字符串 | 按最后更新日期过滤（在此日期之后）。支持ISO 8601或相对格式（例如，`rel:7d`，`rel:6m`）。 |
| `lastUpdatedTo` | 字符串 | 按最后更新日期过滤（在此日期之前） |
| `updateReasonFilter` | 字符串 | 用逗号分隔的更新原因（例如，“Newly Added”，“Phone Primary”） |

**理解“Last Updated” — 这对于找到最新的潜在客户至关重要：**
- **家居改善潜在客户：**最后更新意味着检测到新的电话号码
- **其他潜在客户：**最后更新意味着任何5个联系/地址字段发生了变化：主要电话、次要电话、主要电子邮件、次要电子邮件或完整地址
- 两个数据库都包括此日期内新添加的记录
- 许多企业在添加联系信息之前会先建立网站，因此最后更新日期可以用来识别最可行的潜在客户

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `countryInclude` | JSON数组字符串 | 要包含的国家 |
| `countryExclude` | JSON数组字符串 | 要排除的国家 |
| `sortBy` | 字符串 | 排序字段 |
| `sortOrder` | 字符串 | `asc`或`desc`（默认：`desc`）

**通配符关键词提示：**
- 使用`*`来匹配任何字符：`"*dental*`匹配“dental clinic”、“pediatric dentistry”等
- 结合通配符来匹配复合术语：`"*auto*repair*`匹配“auto body repair”、“automotive repair shop”等
- 使用多个关键词变体以获得更广泛的覆盖范围：`["*dental*", "*dentist*", "*orthodont*"]`
- 没有通配符的关键词仍然默认执行子字符串匹配

**仅限家居改善数据库：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `minStars` / `maxStars` | 数字 | 星级评分范围 |
| `minReviewCount` / `maxReviewCount` | 整数 | 评论数量范围 |
| `categoriesIncludeTerms` / `categoriesExcludeTerms` | JSON数组字符串 | 类别过滤器 |
| `reviewSnippetIncludeTerms` / `reviewSnippetExcludeTerms` | JSON数组字符串 | 评论文本过滤器 |
| `profileUrlIncludeTerms` / `profileUrlExcludeTerms` | JSON数组字符串 | 个人资料URL过滤器 |

**仅限其他数据库：**

| 参数 | 类型 | 描述 |
|-----------|------|-------------|
| `urlIncludeTerms` / `urlExcludeTerms` | JSON数组字符串 | 注册URL过滤器 |
| `crawledUrlIncludeTerms` / `crawledUrlExcludeTerms` | JSON数组字符串 | 爬取的URL过滤器 |
| `descriptionIncludeTerms` / `descriptionLongIncludeTerms` / `descriptionLongExcludeTerms` | 简短描述过滤器 |
| `emailPrimaryInclude` / `emailPrimaryExclude` | JSON数组字符串 | 主要电子邮件过滤器 |
| `emailSecondaryInclude` / `emailSecondaryExclude` | JSON数组字符串 | 次要电子邮件过滤器 |
| `phonePrimaryInclude` / `phonePrimaryExclude` | JSON数组字符串 | 主要电话过滤器 |
| `phoneSecondaryInclude` / `phoneSecondaryExclude` | JSON数组字符串 | 次要电话过滤器 |
| `redirectFilter` | 字符串 | `yes`或`no` — 根据重定向状态过滤 |
| `registrationDateFrom` / `registrationDateTo` | 字符串 | 根据域名注册日期过滤（ISO 8601或相对格式，例如，`rel:6m`） |
| `timeScrapedFrom` / `timeScrapedTo` | 字符串 | 根据抓取时间过滤（ISO 8601或相对格式，例如，`rel:30d`） |
| `websiteSchemaFilter` | 字符串 | 用逗号分隔的网站模式类型（例如，`LocalBusiness,Organization`）。使用`GET /leads/other/schema-types`获取可用值。 |

**重要提示：**至少需要一个正面过滤条件（positiveKeywords或任何特定列的包含条件）。

**响应包括：`leads`数组、`totalCount`、`page`、`limit`、`databaseType`

**潜在客户字段：`id`、`companyName`、`state`、`city`、`zip`、`phone`、`email`、`categories`、`lastUpdated`（免费用户的电话/电子邮件被屏蔽）。`lastUpdated`字段表示联系信息最后一次被检测或更新的时间——这是判断潜在客户新鲜度和可行性的最佳指标）。

### 2. 网站模式类型 — `GET /leads/other/schema-types`

返回其他潜在客户数据库中找到的所有不同网站模式类型的排序列表。使用这些值与`GET /leads`中的`websiteSchemaFilter`参数一起使用。

### 3. 导出潜在客户 — `POST /leads/export`

将过滤后的潜在客户导出为CSV、JSON或XLSX文件。

**请求体：**
```json
{
  "database": "home_improvement" | "other",
  "filters": { /* same filter params as GET /leads */ },
  "selectedIds": [1, 2, 3],  // alternative to filters
  "formatId": 123,  // optional export format template ID
  "maxLeads": 500,  // optional: cap leads per export, overflow stored in reservoir
  "maxResults": 1000,  // optional: total leads (new + previously-exported)
  "maxCredits": 100  // optional: credit spending cap (0 = only previously-exported leads)
}
```

**信用系统（Starter/Growth/Scale计划）：**
- 每导出一个新潜在客户会扣除1个信用点
- 之前导出的潜在客户免费包含
- 使用`maxCredits`来控制支出，`maxLeads`来限制数量
- 设置`maxCredits: 0`以免费接收之前导出的潜在客户

**响应：`files`数组（包含base64编码的数据）、`leadCount`、`exportId`、`databaseType`、`creditsUsed`、`creditsRemaining`、`overflowCount`

**错误402：需要支付：**当信用计划用户信用不足时返回。

速率限制：每5分钟1次导出，每次导出最多10,000个潜在客户。

### 4. 过滤预设 — `/filter-presets`

- `GET /filter-presets` — 列出所有保存的预设
- `POST /filter-presets` — 创建预设（需要`name`和`filters`对象）
- `DELETE /filter-presets/{id}` — 删除预设

### 5. 关键词列表 — `/keyword-lists`

关键词列表现在支持键入的列表（正面或负面），并具有配对的列表管理和来源类别。

- `GET /keyword-lists` — 列出所有关键词列表
- `POST /keyword-lists` — 创建（需要`name`、可选的`keywords`数组、`sourceCategories`数组最多3个）
- `PUT /keyword-lists/{id}` — 更新
- `DELETE /keyword-lists/{id}` — 删除

**关键词列表属性：`name`、`keywords`（通配符模式，例如，`*dentist*`）、`type`（正面/负面）、`pairedListId`（链接的正面/负面对）、`sourceCategories`（最多3个）、`autoRefineEnabled`、`refinementStatus`（运行/完成/暂停）

### 6. 电子邮件调度 — `/email-schedules`

电子邮件调度现在支持分发模式和潜在客户储备。

- `GET /email-schedules` — 列出调度
- `POST /email-schedules` — 创建（需要`name`、`filterPresetId`、`intervalValue`、`intervalUnit`、`recipients`至少1个）
- `PATCH /email-schedules/{id}` — 更新（支持`isActive`切换）
- `DELETE /email-schedules/{id}` — 删除
- `POST /email-schedules/{id}/trigger` — 立即触发活动调度（速率限制：每5分钟1次）

**分发模式：**
- `full_copy`（默认）：将所有潜在客户发送给每个接收者
- `split_evenly`：将潜在客户平均分配给接收者。可选的`fullCopyRecipients`数组用于应接收完整列表的人（例如，经理）

**潜在客户储备：**设置`maxLeadsPerEmail`来限制每次发送的潜在客户数量。超出部分将存储并在下一次安排的电子邮件中包含。

### 7. 导出格式 — `/export-formats`

- `GET /export-formats` — 列出自定义导出格式
- `POST /export-formats` — 创建（需要`name`，支持`fileType`、`fieldMappings`、split设置）
- `GET /export-formats/{id}` — 获取特定格式
- `PATCH /export-formats/{id}` — 更新
- `DELETE /export-formats/{id}` — 删除
- `POST /export-formats/{id}/set-default` — 设置为默认

### 8. 导出历史 — `/export-history`

- `GET /export-history` — 列出过去的导出（可选`limit`参数，默认50）
- `GET /export-history/{id}/download` — 重新下载（7天后过期）

### 9. AI功能

**`POST /ai/suggest-categories`** — 根据公司资料获取AI类别建议。

必需参数：`companyName`、`companyDescription`、`productService`
可选参数：`companyWebsite`、`smbType`、`excludeCategories`

**`POST /ai/generate-keywords`** — 根据您的公司资料和目标类别触发异步关键词生成（每个列表最多3个）。关键词生成为通配符模式，并默认启用自动优化保存在关键词列表中。使用 `/ai/keyword-status` 来检查进度。

**`GET /ai/keyword-status`** — 检查关键词生成作业的状态。在触发关键词生成后使用此命令来查询完成情况。

**AI自动优化** — 单次通过的四阶段优化，使用AI自动优化关键词列表：

- 第1阶段：验证正面关键词（50%阈值，最多2次尝试）
- 第1B阶段：在单次AI调用中发现最多15个新的正面关键词
- 第2阶段：验证负面关键词（40%阈值）
- 第2B阶段：从大约80个样本潜在客户中发现最多5个新的负面关键词
- 最终质量得分（1-10分，中值为3）决定是否需要重试
- 完成后自动优化关闭
- 使用`sourceCategories`（每个列表最多3个）进行准确的AI评分

端点：

- `POST /ai/auto-refine/enable` — 为关键词列表启用自动优化（需要`listId`）
- `POST /ai/auto-refine/disable` — 为关键词列表禁用自动优化（需要`listId`）
- `GET /ai/auto-refine/status` — 检查自动优化状态（可选`listId`查询参数以过滤特定列表）

### 10. 导出黑名单 — `/export-blacklist`

- `GET /export-blacklist` — 列出黑名单条目
- `POST /export-blacklist` — 添加条目（通过`entries`数组单独或批量）
- `DELETE /export-blacklist/{id}` — 删除条目

### 11. 账户

- `GET /me` — 获取用户资料（订阅计划、设置、入职状态、信用余额）
- `PATCH /me` — 更新资料（firstName、lastName、companyName、companyWebsite）
- `GET /settings/database` — 检查当前数据库类型并切换可用性
- `POST /settings/switch-database` — 在数据库之间切换（有冷却时间）

### 12. 程序化购买 — 通过API购买订阅

无需网站注册。新用户可以通过API完全购买并获取API密钥：

1. `POST /purchase` — 创建Stripe结算会话。提供`email`和`plan`（starter、growth、scale、platinum或enterprise）。返回`checkoutUrl`和`claimToken`。
2. 将用户引导至结算URL完成支付。
3. `POST /claim-key` — 支付后，提供`email`和`claimToken`以检索API密钥。如果支付仍待处理，返回状态`pending` — 每5-10秒轮询一次。

### 13. 信用和订阅管理

- `POST /purchase-credits` — 购买额外的永久信用点。提供`creditCount`（至少100）或`dollarAmount`（至少$1）。使用保存的支付方式（Stripe离线收费）。
- `POST /subscription/change-plan` — 在starter、growth和scale之间升级或降级。升级时，未使用的月度信用点将转换为永久信用点。降级在续订时生效。
- `POST /subscription/cancel` — 在当前计费周期结束时取消订阅。访问权限持续到周期结束。

---

## 自然语言翻译指南

当用户提出自然语言请求时，将它们转换为API调用。使用多个通配符关键词变体来扩大搜索范围——关键词通过OR逻辑匹配，因此更多的变体意味着更好的覆盖范围：

| 用户输入 | API调用 |
|-----------|---------|
| “在德克萨斯州找到新的牙科诊所” | `GET /leads?positiveKeywords=["*dental*","*dentist*","*orthodont*"]&stateInclude=TX` |
| “在佛罗里达州搜索医疗水疗中心和美容企业” | `GET /leads?positiveKeywords=["*med*spa*","*medical*spa*","*aesthet*","*botox*","*medspa*"]&stateInclude=FL` |
| “显示本周更新的芝加哥汽车修理店” | `GET /leads?positiveKeywords=["*auto*repair*","*body*shop*","*mechanic*","*oil*change*","*brake*"]&cityInclude=["Chicago"]&lastUpdatedFrom=rel:7d` |
| “在加利福尼亚州找到宠物美容企业，排除寄养服务” | `GET /leads?positiveKeywords=["*pet*groom*","*dog*groom*","*pet*salon*"]&negativeKeywords=["*boarding*","*kennel*"]&stateInclude=CA` |
| “获取纽约的面包店和餐饮公司” | `GET /leads?positiveKeywords=["*bakery*","*bake*shop*","*cater*","*pastry*","*cake*"]&stateInclude=NY` |
| “在乔治亚州和北卡罗来纳州找到健身工作室” | `GET /leads?positiveKeywords=["*fitness*","*gym*","*yoga*","*pilates*","*crossfit*"]&stateInclude=GA,NC` |
| “获取50个评分高的潜在客户” | `GET /leads?limit=50&minStars=4`（仅限home_improvement） |
| “找到具有LocalBusiness模式类型的企业” | `GET /leads?websiteSchemaFilter=LocalBusiness`（仅限other） |
| “显示过去6个月内注册的潜在客户” | `GET /leads?registrationDateFrom=rel:6m`（仅限other） |
| “导出我所有的过滤结果” | `POST /leads/export` 并使用当前的过滤条件 |
| “导出但最多花费50个信用点” | `POST /leads/export` 并设置`maxCredits: 50` |
| “仅导出之前导出的潜在客户（免费）” | `POST /leads/export` 并设置`maxCredits: 0` |
| “我应该针对哪些类别？” | `POST /ai/suggest-categories` |
| “将此搜索保存为‘FL Med Spas’” | `POST /filter-presets` |
| “显示我最近的导出结果” | `GET /export-history` |
| “我当前使用的是哪个计划？” | `GET /me` |
| “我还剩下多少信用点？” | `GET /me` |
| “购买500个额外的信用点” | `POST /purchase-credits` 并设置`creditCount: 500` |
| “升级到Growth计划” | `POST /subscription/change-plan` 并设置`targetPlan: "growth"` |
| “取消我的订阅” | `POST /subscription/cancel` |
| “从导出中排除这些域名” | `POST /export-blacklist` |
| “在我的关键词列表上启用自动优化” | `POST /ai/auto-refine/enable` 并提供`listId` |
| “检查我的关键词生成情况” | `GET /ai/keyword-status` |
| “立即发送我的预定邮件” | `POST /email-schedules/{id}/trigger` |
| “将潜在客户平均分配给我的销售团队” | `POST /email-schedules` 并设置`distributionMode: "split-evenly"` |
| “我想注册Starter计划” | `POST /purchase` 并设置`plan: "starter"` |

## 构建API请求

使用包含的`smb_api.py`脚本进行所有API调用。它处理认证、URL编码、响应解析和安全的文件导出，所有这些都在一个可重用的文件中完成。**不要使用shell命令如`curl`** — 从用户提供的输入构建shell命令存在shell注入漏洞的风险。

### 使用方法

```bash
python smb_api.py <API_KEY> <METHOD> <ENDPOINT> [--params '{"key":"value"}'] [--body '{"key":"value"}'] [--output-dir /path/to/dir]
```

### 示例

```bash
# Search for med spas in Florida using wildcard keywords (OR logic)
python smb_api.py smbk_xxx GET /leads --params '{"positiveKeywords":"[\"*med*spa*\",\"*medical*spa*\",\"*aesthet*\",\"*botox*\",\"*medspa*\"]","stateInclude":"FL","limit":"25"}'

# Find auto shops in multiple states, exclude franchises
python smb_api.py smbk_xxx GET /leads --params '{"positiveKeywords":"[\"*auto*repair*\",\"*body*shop*\",\"*mechanic*\",\"*tire*\",\"*oil*change*\"]","negativeKeywords":"[\"*franchise*\",\"*jiffy*\"]","stateInclude":"GA,FL,NC,SC,TN","limit":"50"}'

# Search for recently updated dental leads in Texas
python smb_api.py smbk_xxx GET /leads --params '{"positiveKeywords":"[\"*dental*\",\"*dentist*\",\"*orthodont*\",\"*oral*surg*\"]","stateInclude":"TX","lastUpdatedFrom":"rel:7d"}'

# Full-text search across all fields
python smb_api.py smbk_xxx GET /leads --params '{"search":"organic coffee","limit":"25"}'

# Filter by website schema type (other database only)
python smb_api.py smbk_xxx GET /leads --params '{"websiteSchemaFilter":"LocalBusiness","stateInclude":"CA","limit":"25"}'

# Get available website schema types
python smb_api.py smbk_xxx GET /leads/other/schema-types

# Get account info (includes credit balance)
python smb_api.py smbk_xxx GET /me

# Export with credit controls
python smb_api.py smbk_xxx POST /leads/export --body '{"database":"other","filters":{"positiveKeywords":["*pet*groom*","*veterinar*","*dog*train*"],"stateInclude":"CA,OR,WA"},"maxCredits":100}'

# Export only previously-exported leads (free, no credits used)
python smb_api.py smbk_xxx POST /leads/export --body '{"database":"other","filters":{"positiveKeywords":["*dental*"],"stateInclude":"TX"},"maxCredits":0}'

# Purchase additional credits
python smb_api.py smbk_xxx POST /purchase-credits --body '{"creditCount":500}'

# Purchase credits by dollar amount
python smb_api.py smbk_xxx POST /purchase-credits --body '{"dollarAmount":50}'

# Change subscription plan
python smb_api.py smbk_xxx POST /subscription/change-plan --body '{"targetPlan":"growth"}'

# Cancel subscription
python smb_api.py smbk_xxx POST /subscription/cancel

# Start a programmatic purchase (no auth needed, but script still requires a placeholder key)
python smb_api.py none POST /purchase --body '{"email":"user@example.com","plan":"starter"}'

# Claim API key after payment
python smb_api.py none POST /claim-key --body '{"email":"user@example.com","claimToken":"tok_abc123"}'

# AI category suggestions
python smb_api.py smbk_xxx POST /ai/suggest-categories --body '{"companyName":"FitPro Supply","companyDescription":"Commercial fitness equipment distributor","productService":"Gym equipment, treadmills, weight systems"}'

# Create a filter preset
python smb_api.py smbk_xxx POST /filter-presets --body '{"name":"NY Bakeries","filters":{"positiveKeywords":["*bakery*","*bake*shop*","*cater*","*pastry*"],"stateInclude":"NY"}}'

# Create email schedule with split distribution
python smb_api.py smbk_xxx POST /email-schedules --body '{"name":"Daily TX Leads","filterPresetId":5,"intervalValue":1,"intervalUnit":"days","recipients":["rep1@co.com","rep2@co.com"],"distributionMode":"split_evenly","fullCopyRecipients":["manager@co.com"],"maxLeadsPerEmail":50}'

# Enable AI auto-refine on a keyword list
python smb_api.py smbk_xxx POST /ai/auto-refine/enable --body '{"listId":42}'

# Check auto-refine status for a specific list
python smb_api.py smbk_xxx GET /ai/auto-refine/status --params '{"listId":"42"}'

# Check keyword generation job status
python smb_api.py smbk_xxx GET /ai/keyword-status

# Manually trigger an email schedule
python smb_api.py smbk_xxx POST /email-schedules/15/trigger

# Delete a filter preset
python smb_api.py smbk_xxx DELETE /filter-presets/42
```

该脚本将JSON输出到stdout，将速率限制头部输出到stderr。对于导出请求，文件会自动保存并使用清理后的文件名。

**记住：**
- 使用多个通配符关键词变体来扩大搜索范围（例如，`["*dental*", "*dentist*", "*orthodont*"]`而不仅仅是`["dental"]`）——关键词通过OR逻辑匹配
- 使用`*`进行灵活的模式匹配：`"*auto*repair*`匹配“auto body repair”、“automotive repair shop”等
- JSON数组参数应作为字符串序列化在`--params` JSON中
- 搜索潜在客户时至少需要一个正面过滤条件
- 在应用特定于数据库的过滤条件之前，请检查用户需要哪个数据库
- 家居改善数据库提供电话号码；其他数据库提供电话号码和电子邮件地址
- 免费用户的电话和电子邮件被屏蔽
- 以清晰、易读的表格格式呈现结果
- 对于信用计划用户，导出后请提及使用的/剩余的信用点
- `POST /purchase`和`POST /claim-key`端点不需要认证（不需要API密钥）

## 安全性

此技能解决了两个特定的代理执行风险：**shell注入**（通过使用用户输入构建CLI命令）和**任意文件写入**（来自未经清理的API提供的文件名）。

**防止shell注入：**`smb_api.py`脚本使用Python的`requests`库进行所有HTTP调用。用户提供的搜索词、位置和其他输入作为结构化函数参数传递——从未插入到shell命令字符串中。这消除了代理从用户输入构建`curl`命令时存在的shell注入风险。

**防止导出中的路径遍历：**`/leads/export`端点返回带有API提供的`fileName`字段的base64编码文件。恶意或损坏的文件名（例如，`../../etc/passwd`）可能会将文件写入任意位置。脚本实施了三个安全措施：
1. **基名提取：`os.path.basename()`删除所有目录组件——`../../etc/passwd`变为`passwd`
2. **扩展名验证：**只允许`.csv`、`.json`和`.xlsx`扩展名；其他扩展名默认为`.csv`
3. **输出目录限制：**文件仅写入指定的输出目录（默认为`/mnt/user-data/outputs/`），永远不会写入用户指定的或API指定的路径

**API密钥处理：**密钥作为CLI参数传递，并仅发送在Authorization头部。它从未被记录、写入文件或包含在错误输出中。

## 错误处理

| 状态 | 含义 |
|--------|---------|
| 400 | 请求错误 — 检查参数 |
| 401 | API密钥无效或缺失 |
| 402 | 信用不足（信用计划用户） — 使用`GET /me`检查信用余额 |
| 403 | 需要活跃订阅 |
| 404 | 资源未找到 |
| 429 | 速率限制 — 检查`Retry-After`头部 |
| 500 | 服务器错误 |

所有错误都会返回：`{ "error": "error_code", "message": "Human-readable message" }`