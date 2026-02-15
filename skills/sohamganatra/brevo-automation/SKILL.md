---
name: brevo-automation
description: "通过 Rube MCP (Composio) 自动化 Sendinblue 的 Brevo 任务：管理电子邮件活动、创建/编辑模板、跟踪发件人以及监控活动性能。在使用这些工具之前，请务必先查找最新的使用规范（schemas）。"
requires:
  mcp: [rube]
---

# 通过 Rube MCP 自动化 Brevo（前身为 Sendinblue）的电子邮件营销操作

您可以通过 Composio 的 Brevo 工具包和 Rube MCP 来自动化 Brevo 的电子邮件营销操作。

## 先决条件

- Rube MCP 必须已连接（RUBE_SEARCH_TOOLS 可用）
- 通过 `RUBE_MANAGE_CONNECTIONS` 使用 `brevo` 工具包建立有效的 Brevo 连接
- 在运行任何工作流之前，务必先调用 `RUBE_SEARCH_TOOLS` 以获取当前的工具架构信息

## 设置

**添加 Rube MCP**：在您的客户端配置中添加 `https://rube.app/mcp` 作为 MCP 服务器。无需 API 密钥——只需添加该端点即可。

1. 通过确认 `RUBE_SEARCH_TOOLS` 是否有响应来验证 Rube MCP 是否可用。
2. 调用 `RUBE_MANAGE_CONNECTIONS` 并指定 `brevo` 工具包。
3. 如果连接状态不是 `ACTIVE`，请按照返回的链接完成 Brevo 的身份验证。
4. 在运行任何工作流之前，确保连接状态显示为 `ACTIVE`。

## 核心工作流

### 1. 管理电子邮件活动

**使用场景**：用户需要列出、查看或更新电子邮件活动。

**工具顺序**：
1. `BREVO_LIST_EMAIL_CAMPAIGNS` - 使用过滤器列出所有活动 [必需]
2. `BREVO_UPDATE_EMAIL_CAMPAIGN` - 更新活动内容或设置 [可选]

**列出活动时的关键参数**：
- `type`：活动类型（'classic' 或 'trigger'）
- `status`：活动状态（'suspended', 'archive', 'sent', 'queued', 'draft', 'inProcess', 'inReview'）
- `startDate`/`endDate`：日期范围过滤器（格式为 YYYY-MM-DDTHH:mm:ss.SSSZ）
- `statistics`：要包含的统计类型（'globalStats', 'linksStats', 'statsByDomain'）
- `limit`：每页显示的结果数量（最大 100，默认 50）
- `offset`：分页偏移量
- `sort`：排序顺序（'asc' 或 'desc'）
- `excludeHtmlContent`：设置为 `true` 可以减少响应大小

**更新活动时的关键参数**：
- `campaign_id`：活动的唯一编号（必需）
- `name`：活动名称
- `subject`：电子邮件主题行
- `htmlContent`：HTML 电子邮件正文（与 `htmlUrl` 互斥）
- `htmlUrl`：HTML 内容的 URL
- `sender`：发送者对象，包含 `name`、`email` 或 `id`
- `recipients`：包含 `listIds` 和 `exclusionListIds` 的对象
- `scheduledAt`：计划发送时间（格式为 YYYY-MM-DDTHH:mm:ss.SSSZ）

**注意事项**：
- `startDate` 和 `endDate` 是必填项；必须同时提供或都不提供。
- 仅当 `status` 未设置或设置为 'sent' 时，日期过滤器才有效。
- `htmlContent` 和 `htmlUrl` 是互斥的。
- 活动的发送者电子邮件地址必须在 Brevo 中经过验证。
- A/B 测试字段（`subjectA`, `subjectB`, `splitRule`, `winnerCriteria`）需要设置 `abTesting: true`。
- `scheduledAt` 需要使用完整的 ISO 8601 格式，并包含时区。

### 2. 创建和管理电子邮件模板

**使用场景**：用户需要创建、编辑、列出或删除电子邮件模板。

**工具顺序**：
1. `BREVO_GET_ALL_EMAIL_TEMPLATES` - 列出所有模板 [必需]
2. `BREVO_CREATE_OR_UPDATE_EMAIL TEMPLATE` - 创建新模板或更新现有模板 [必需]
3. `BREVO_DELETE_EMAIL TEMPLATE` - 删除不活跃的模板 [可选]

**列出模板时的关键参数**：
- `templateStatus`：过滤活跃（`true`）或不活跃（`false`）的模板
- `limit`：每页显示的结果数量（最大 1000，默认 50）
- `offset`：分页偏移量
- `sort`：排序顺序（'asc' 或 'desc')

**创建/更新模板时的关键参数**：
- `templateId`：要更新的模板 ID（提供则更新模板；省略则创建新模板）
- `templateName`：模板的显示名称（创建时必需）
- `subject`：电子邮件主题行（创建时必需）
- `htmlContent`：HTML 模板正文（至少 10 个字符；可以使用此参数或 `htmlUrl`）
- `sender`：发送者对象，包含 `name` 和 `email` 或 `id`（创建时必需）
- `replyTo`：回复邮件地址
- `isActive`：激活或停用模板
- `tag`：模板的分类标签

**注意事项**：
- 提供 `templateId` 时，工具会更新模板；省略则创建新模板。
- 创建模板时，`templateName`、`subject` 和 `sender` 是必填项。
- `htmlContent` 必须至少包含 10 个字符。
- 模板个性化使用 `{{contact.ATTRIBUTE}}` 语法。
- 只能删除不活跃的模板。
- `htmlContent` 和 `htmlUrl` 是互斥的。

### 3. 管理发送者

**使用场景**：用户需要查看已授权的发送者信息。

**工具顺序**：
1. `BREVO_GET_ALL_SENDERS` - 列出所有已验证的发送者 [必需]

**关键参数**：（无）

**注意事项**：
- 发送者在用于活动或模板之前必须经过验证。
- 发送者验证通过 Brevo 的网页界面完成，无法通过 API 进行。
- 发送者 ID 可以用于活动或模板中的 `sender.id` 字段。

### 4. 配置 A/B 测试活动

**使用场景**：用户需要设置或修改活动的 A/B 测试设置。

**工具顺序**：
1. `BREVO_LIST_EMAIL_CAMPAIGNS` - 查找目标活动 [先决条件]
2. `BREVO_UPDATE_EMAIL_CAMPAIGN` - 配置 A/B 测试设置 [必需]

**关键参数**：
- `campaign_id`：要配置的活动
- `abTesting`：设置为 `true` 以启用 A/B 测试
- `subjectA`：变体 A 的主题行
- `subjectB`：变体 B 的主题行
- `splitRule`：测试中接收变体 A 的联系人百分比（1-99）
- `winnerCriteria`：确定获胜者的条件（'open' 或 'click'）
- `winnerDelay`：选择获胜者之前等待的小时数（1-168）

**注意事项**：
- 必须先启用 A/B 测试（`abTesting: true`）才能设置变体字段。
- `splitRule` 指定接收变体 A 的联系人百分比。
- `winnerDelay` 定义在向剩余联系人发送获胜者之前的等待时间。
- 仅适用于 'classic' 类型的活动。

## 常见模式

### 活动生命周期

```
1. Create campaign (status: draft)
2. Set recipients (listIds)
3. Configure content (htmlContent or htmlUrl)
4. Optionally schedule (scheduledAt)
5. Send or schedule via Brevo UI (API update can set scheduledAt)
```

### 分页

- 使用 `limit`（每页显示的数量）和 `offset`（起始索引）。
- 默认限制为 50；具体数量因端点而异（活动为 100，模板为 1000）。
- 每页递增 `offset` 的值等于 `limit`。
- 通过检查响应中的 `count` 来确定总数量。

### 模板个性化

```
- First name: {{contact.FIRSTNAME}}
- Last name: {{contact.LASTNAME}}
- Custom attribute: {{contact.CUSTOM_ATTRIBUTE}}
- Mirror link: {{mirror}}
- Unsubscribe link: {{unsubscribe}}
```

## 常见问题

**日期格式**：
- 所有日期都使用带有毫秒的 ISO 8601 格式：YYYY-MM-DDTHH:mm:ss.SSSZ。
- 为了获得准确的结果，请在日期时间格式中指定时区。
- `startDate` 和 `endDate` 必须一起使用。

**发送者验证**：
- 所有发送者的电子邮件地址必须在 Brevo 中经过验证才能使用。
- 未验证的发送者会导致活动创建/更新失败。
- 使用 `GET_ALL_SENDERS` 来查看可用的已验证发送者。

**速率限制**：
- Brevo API 对每个账户计划有速率限制。
- 在收到 429 错误响应时，请实施重试机制。
- 模板操作的速率限制低于读取操作。

**响应解析**：
- 响应数据可能嵌套在 `data` 或 `data.data` 下。
- 使用防御性解析方法来处理响应数据。
- 活动和模板的 ID 是数值整数。

## 快速参考

| 任务 | 工具名称 | 关键参数 |
|------|-----------|------------|
| 列出活动 | BREVO_LIST_EMAIL_CAMPAIGNS | type, status, limit, offset |
| 更新活动 | BREVO_UPDATE_EMAIL_CAMPAIGN | campaign_id, subject, htmlContent |
| 列出模板 | BREVO_GET_ALL_EMAIL_TEMPLATES | templateStatus, limit, offset |
| 创建模板 | BREVO_CREATE_OR_UPDATE_EMAIL TEMPLATE | templateName, subject, htmlContent, sender |
| 更新模板 | BREVO_CREATE_OR_UPDATE_EMAIL TEMPLATE | templateId, htmlContent |
| 删除模板 | BREVO_DELETE_EMAIL TEMPLATE | templateId |
| 列出发送者 | BREVO_GET_ALL_SENDERS | （无） |