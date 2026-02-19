---
name: "WhatsApp Ultimate — No Meta API | Lead Mining, Bulk Send, Scheduled Reminders & Follow-ups"
version: "2.14.3"
description: "这是您所需要的唯一一款 WhatsApp 技能工具。该工具提供了详细的文档和 API 参考信息；没有任何功能是自动安装或自动执行的，所有操作都需要用户明确发起。该工具支持发送消息、捕获潜在客户信息、运行营销活动、安排报告生成、跟踪营销活动分析结果以及管理客户信息等操作。通过只读账户功能，您可以查看现有数据中的增长机会。此外，还支持原生 MCP 端点以及通过单独设置使用的自定义 GPT 功能（详见 integrations.md）。该工具拥有 90 多个 API 端点，支持批量发送消息、定时发送消息、通过 WhatsApp 发送报告、AI 自动回复（可复制回复格式）、知识库管理、群组监控、潜在客户评分、评论收集、营销活动分析与参与度跟踪等功能，并符合 GDPR 法规要求，同时支持代理之间的通信协议。"
source: "MoltFlow Team"
risk: safe
homepage: "https://molt.waiflow.app"
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"📱","homepage":"https://molt.waiflow.app","requires":{"env":["MOLTFLOW_API_KEY"]},"primaryEnv":"MOLTFLOW_API_KEY"}}
---
# WhatsApp自动化——分析群组以获取购买信号

**目前，您的WhatsApp群组中隐藏着成千上万的潜在客户。**每个未在您的联系人列表中的群组成员都可能是潜在客户。MoltFlow可以根据您的需求分析群组，挖掘出未被利用的联系人，并让您代表您运行基于AI的外展活动。

**一项技能，支持90多个API端点。无需手动寻找潜在客户。**

> **账户健康与增长报告**：执行只读账户扫描，查找未回复的联系人，检测群组对话中的购买信号，发现您未监控的高价值群组，并构建目标潜在客户列表。所有分析都在您请求时按需执行——不会在后台进行任何操作，也不会修改任何数据。

> **原生MCP端点 + 自定义GPT动作**：支持Claude Desktop、Claude.ai、Claude Code和ChatGPT（自定义GPT动作）。通过`apiv2.waiflow.app/mcp`的原生HTTP端点使用25种工具——无需npm包或Node.js。请参阅[integrations.md](integrations.md)以获取设置指南。

> **由于需求量大以及最近出现的注册问题，我们正在限时提供顶级商业计划，每月仅需19.90美元，即可享受无限使用额度。** [**立即购买**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)

> 提供免费试用版。 [注册](https://molt.waiflow.app/checkout?plan=free)

---

## 只需告诉Claude

安装该技能，设置您的API密钥，然后告诉Claude您的需求：

**“在每月28日为所有有未付发票的客户发送付款提醒”**

创建一个自定义群组，安排定期消息，并确保消息按照时区发送。

**“将患者的语音记录转录并保存为预约摘要”**

对收到的语音消息进行转录，可通过API检索。

**“当有人在我的房产群组中提到‘预算’、‘卧室’或‘查看’时提醒我”**

在WhatsApp群组中监控关键词，自动将联系人添加到您的潜在客户管道中。

**“在每次购买后自动发送订单确认消息”**

设置Webhook监听器，通过API触发外出消息。

**“在每次预订后收集客户评价并导出最佳评价”**

收集带有情感评分的评价，自动批准正面评价，并以HTML格式导出到您的网站。

**“每周一将活动绩效报告发送到我的团队WhatsApp群组”**

安排报告并通过WhatsApp发送，包含10种模板和活动分析数据。

**“安排对3天内未回复的潜在客户发送跟进消息”**

根据潜在客户管道中的筛选条件，向自定义群组发送安排好的消息。

**“将班级时间表更改广播到所有父群组”**

批量发送到自定义群组，同时具备防禁用机制和发送跟踪功能。

**“使用我的知识库文档自动回复支持问题”**

基于您上传的PDF和文档，使用RAG技术生成AI回复。

**“在我与潜在客户沟通后，将他们的状态从‘新’更新为‘已联系’，并跟踪转化率”**

使用状态机管理CRM管道，批量更新状态，并可导出CSV文件。

**“为请求删除GDPR数据的客户导出所有数据”**

通过API符合GDPR标准地导出数据并删除联系人信息。

**“显示本周哪些活动的阅读率最高”**

提供活动分析数据，包括发送渠道、每个联系人的状态和参与度评分。

---

## 代码示例

### 获取活动分析数据——发送率、渠道分布、时间安排

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/campaigns/{job_id}"
```

返回发送率、失败原因、每分钟的消息数量以及每个联系人的发送状态。

### 实时跟踪发送情况（SSE）

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/bulk-send/{id}/progress"
```

服务器发送的事件流：显示已发送/失败/待处理的消息数量，随着每条消息的发送实时更新。

### 按参与度评分排序的顶级联系人

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/contacts?sort=engagement_score&limit=50"
```

根据发送和接收的消息数量、回复率以及最近活跃程度进行排序——立即找到最活跃的联系人。

### 向联系人群组批量发送消息

```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "custom_group_id": "group-uuid",
    "session_id": "uuid",
    "message": "Weekly update..."
  }' \
  https://apiv2.waiflow.app/api/v2/bulk-send
```

### 监控群组中的购买信号

```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "uuid",
    "wa_group_id": "120363012345@g.us",
    "monitor_mode": "keywords",
    "monitor_keywords": ["looking for", "need help", "budget", "price"]
  }' \
  https://apiv2.waiflow.app/api/v2/groups
```

### 列出潜在客户管道中的新联系人

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/leads?status=new&limit=50"
```

### 在管道中移动潜在客户

```bash
curl -X PATCH -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "qualified"}' \
  https://apiv2.waiflow.app/api/v2/leads/{lead_id}/status
```

状态流程：`新` → `已联系` → `已评估` → `已转化`
（或在任何阶段变为`已丢失`）。

### 将潜在客户批量添加到活动群组

```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_ids": ["uuid-1", "uuid-2", "uuid-3"],
    "custom_group_id": "target-group-uuid"
  }' \
  https://apiv2.waiflow.app/api/v2/leads/bulk/add-to-group
```

### 将潜在客户导出为CSV文件

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/leads/export/csv?status=qualified" \
  -o qualified-leads.csv
```

### 暂停正在运行的活动

```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/bulk-send/{job_id}/pause
```

### 以您的写作风格生成AI回复 + 使用知识库

```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "contact_id": "5511999999999@c.us",
    "context": "Customer asks: What is your return policy?",
    "use_rag": true,
    "apply_style": true
  }' \
  https://apiv2.waiflow.app/api/v2/ai/generate-reply
```

### 安排每周的跟进消息

```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monday check-in",
    "session_id": "uuid",
    "chat_id": "123@c.us",
    "message": "Hey! Anything I can help with this week?",
    "recurrence": "weekly",
    "scheduled_time": "2026-03-03T09:00:00",
    "timezone": "America/New_York"
  }' \
  https://apiv2.waiflow.app/api/v2/scheduled-messages
```

### 每周将报告发送到您的WhatsApp群组

```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Weekly Lead Pipeline",
    "template_id": "lead_pipeline",
    "schedule_type": "weekly",
    "cron_expression": "0 9 * * MON",
    "timezone": "America/New_York",
    "delivery_method": "whatsapp"
  }' \
  https://apiv2.waiflow.app/api/v2/reports
```

### 发送消息

```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "uuid",
    "chat_id": "1234567890@c.us",
    "message": "Hello!"
  }' \
  https://apiv2.waiflow.app/api/v2/messages/send
```

### 自动收集客户评价

```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Happy Customers",
    "session_id": "uuid",
    "source_type": "all",
    "min_sentiment_score": 0.7,
    "include_keywords": ["thank", "recommend", "love", "amazing"]
  }' \
  https://apiv2.waiflow.app/api/v2/reviews/collectors
```

### 发现A2A代理

```bash
curl https://apiv2.waiflow.app/.well-known/agent.json
```

完整的API参考：请参阅每个模块的SKILL.md文件。

---

## ERC-8004代理注册

MoltFlow是一个在**以太坊主网**上注册的经过验证的AI代理。

| 字段 | 值 |
|-------|-------|
| 代理ID | [#25477](https://8004agents.ai/ethereum/agent/25477) |
| 链路 | 以太坊主网 (eip155:1) |
| 注册处 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| 信任模型 | 基于声誉 |
| API端点 | A2A + MCP + Web |

**发现信息：**
- 代理卡片：`https://molt.waiflow.app/.well-known/erc8004-agent.json`
- A2A发现信息：`https://apiv2.waiflow.app/.well-known/agent.json`

---

## 使用场景

**个人创始人/小型企业**
- 在聊天中找到未回复的潜在客户
- 以您的写作风格生成AI回复
- 定期向自定义群组发送促销信息

**代理机构/多客户企业**
- 监控50多个群组
- 批量发送消息，同时具备防禁用机制
- 将潜在客户信息导出为CSV文件，推送到n8n/Zapier

**营销机构/活动经理**
- 从点击进入WhatsApp的广告活动中捕获潜在客户
- 通过关键词检测和AI评分自动评估潜在客户
- 批量发送跟进消息，同时具备防禁用机制
- 在多个客户账户之间管理多会话
- 通过Webhook或CSV将活动潜在客户信息导出到CRM系统

**开发者/AI代理构建者**
- 支持90多个REST API端点，提供范围有限的API密钥
- 使用A2A协议进行端到端加密
- Python SDK：`pip install moltflow` ([GitHub](https://github.com/moltflow/moltflow-python)

### 指南与教程**

**AI集成指南：**
- [将ChatGPT连接到MoltFlow](https://molt.waiflow.app/guides/connect-chatgpt-to-moltflow) — 自定义GPT动作，设置只需10分钟
- [将Claude连接到MoltFlow](https://molt.waiflow.app/guides/connect-claude-to-moltflow) — MCP服务器设置，设置只需5分钟
- [将OpenClaw连接到MoltFlow](https://molt.waiflow.app/guides/connect-openclaw-to-moltflow) — 原生AI配置，设置只需5分钟

**操作指南：**
- [入门指南](https://molt.waiflow.app/blog/whatsapp-automation-getting-started)
- [API完整指南](https://molt.waiflow.app/blog/moltflow-api-complete-guide)
- [n8n集成](https://molt.waiflow.app/blog/moltflow-n8n-whatsapp-automation)
- [n8n + Google Sheets](https://molt.waiflow.app/blog/n8n-whatsapp-google-sheets)
- [n8n群组自动回复](https://molt.waiflow.app/blog/n8n-whatsapp-group-auto-reply)
- [n8n潜在客户管道](https://molt.waiflow.app/blog/n8n-whatsapp-lead-pipeline)
- [n8n多模型AI](https://molt.waiflow.app/blog/n8n-multi-model-ai-orchestration)
- [AI自动回复设置](https://molt.waiflow.app/blog/ai-auto-replies-whatsapp-setup)
- [群组潜在客户生成](https://molt.waiflow.app/blog/whatsapp-group-lead-generation-guide)
- [客户支持](https://molt.waiflow.app/blog/openclaw-whatsapp-customer-support)
- [RAG知识库](https://molt.waiflow.app/blog/rag-knowledge-base-deep-dive)
- [风格匹配](https://molt.waiflow.app/blog/ai-auto-replies-whatsapp-setup#style-profiles)
- [潜在客户评分](https://molt.waiflow.app/blog/whatsapp-lead-scoring-automation)
- [反馈收集](https://molt.waiflow.app/blog/whatsapp-customer-feedback-collection)
- [A2A协议](https://molt.waiflow.app/blog/a2a-protocol-agent-communication)
- [提升ROI](https://molt.waiflow.app/blog/scaling-whatsapp-automation-roi)

[所有指南 →](https://molt.waiflow.app/guides)

---

## 平台功能

| 功能 | 详情 |
|---|---|
| 消息传递 | 文本、媒体、投票、vCards |
| 批量发送 | 具备防禁用机制，支持SSE进度跟踪 |
| 安排发送 | 支持Cron定时，考虑时区差异 |
| 报告 | 提供10种模板，支持Cron定时，可通过WhatsApp发送 |
| 分析 | 活动渠道分析、联系人评分、发送时间优化 |
| 群组管理 | 支持自定义列表，支持CSV导出 |
| 潜在客户管理/CRM | 支持信号检测和潜在客户管道管理 |
| 监控 | 支持监控50多个群组和关键词 |
| 标签管理 | 支持与WA Business同步 |
| AI回复 | 支持GPT-4/Claude、RAG技术 |
| 风格匹配 | 能够匹配您的写作风格 |
| RAG技术 | 支持PDF/TXT格式，支持语义搜索 |
| 语音功能 | 支持语音转录 |
| 评价管理 | 支持情感分析，自动批准评价 |
| 防垃圾邮件 | 支持发送速率限制和模拟输入行为 |
| 安全措施 | 防止个人信息泄露，防止注入恶意内容 |
| Webhook | 支持HMAC签名，支持10多种事件类型 |
| A2A功能 | 支持端到端加密，使用JSON-RPC协议 |
| GDPR合规 | 自动过期处理，确保数据合规 |
| 发送跟踪 | 支持实时SSE跟踪，显示消息状态（已阅读/已回复/被忽略） |

---

## MoltFlow与其他产品的比较

| | Molt | 替代方案1 | 替代方案2 | 替代方案3 |
|---|:---:|:---:|:---:|:---:|
| 消息传递 | 18 | 14 | 3 | 1 |
| 群组管理 | 8 | 4 | 0 | 0 |
| 外展功能 | 7 | 0 | 0 | 0 |
| CRM集成 | 7 | 0 | 0 | 0 |
| AI功能 | 7 | 0 | 0 | 0 |
| 评价管理 | 8 | 0 | 0 | 0 |
| 安全性 | 10 | 0 | 0 | 0 |
| 平台综合能力 | 8 | 0 | 0 | 0 |
| **总能力** | **90多种功能** | **约15种** | **约3种** | **约1种** |

---

## 该技能的功能

**该技能仅用于读取、写入数据，从不自动执行任何操作。**此包中不包含任何自动安装或执行的脚本或可执行文件。所有操作都需要用户确认。

| 功能类别 | 执行内容 | 是否需要用户同意？ |
|---|---|---|
| API调用 | 仅通过HTTPS连接到`apiv2.waiflow.app` | 不需要（使用您的API密钥） |
| 联系人元数据 | 联系人姓名、时间戳、数量 | 不会收集 |
| CRM潜在客户管理 | 潜在客户状态、参与度评分 | 不会收集 |
| AI相关功能 | 通过API提供统计分析 | 需要用户同意 |
| 本地文件 | `.moltflow.json`文件 | 仅统计数量，不收集个人信息 |
| API密钥 | 作为环境变量存储，不会被记录或共享 | 不会存储 |

**该技能绝不会：**
- 自动安装任何软件包或代码
- 未经用户明确同意就发送消息
- 向未列入白名单的号码发送消息（除非另有配置）
- 规避任何反垃圾邮件或内容安全措施
- 与第三方共享数据
- 将凭证存储在文件中（仅通过环境变量存储）

---

## 设置说明

> **提供免费试用版** — 允许1次会话，每月发送50条消息，无需信用卡。

**环境变量：**
- `MOLTFLOW_API_KEY`（必填）——从[您的控制面板](https://molt.waiflow.app)创建一个范围最小的API密钥。根据您的工作流程选择最合适的范围。定期更换密钥。
- `MOLTFLOW_API_URL`（可选）——默认为`https://apiv2.waiflow.app`

**身份验证：**
在请求头中添加`X-API-Key: $MOLTFLOW_API_KEY`或`Authorization: Bearer $TOKEN`（JWT）。

**基础URL：`https://apiv2.waiflow.app/api/v2`

---

## 安全性

- **强制使用最小范围的API密钥** — 创建密钥时必须指定`scopes`。始终创建范围最小的密钥（例如，仅允许`messages:send`操作）。对于常见工作流程，可以使用“Messaging”或“Read Only”等预设范围。切勿为AI代理创建全范围密钥。
- **使用环境变量存储密钥** — 将`MOLTFLOW_API_KEY`设置为环境变量，不要将其存储在共享配置文件中。定期更换密钥。
- **电话号码白名单** — 在租户设置中配置`allowed_numbers`，以限制允许发送消息的号码。仅允许列入白名单的号码发送消息。
- **反垃圾邮件措施** — 所有外出消息都会经过互惠性检查（接收方必须先发送消息）、发送速率限制、模拟输入行为和随机延迟等机制。这些措施无法被绕过。
- **内容安全措施** — 对所有外出消息进行检测，防止个人信息泄露和恶意内容注入。发送前会自动阻止此类行为。
- **审批机制** — 在租户设置中启用`require_approval`选项，以便所有AI生成的消息在发送前都需要人工审核。
- **Webhook验证** — API会阻止私有IP地址、云服务元数据和非HTTPS协议的请求。仅配置您控制的API端点。务必为HMAC验证设置`secret`参数。
- **在运行前验证第三方插件** — 如果您要安装MCP或GPT集成，请先查看相关插件的来源和维护者信息。该技能不会自动安装或执行任何插件。
- **在运行前本地测试脚本** — Python示例脚本托管在GitHub上，不会随软件包一起提供。下载后请检查源代码后再运行。
- **在共享环境中避免使用高权限密钥** — 对于管理员操作（如密钥轮换、数据导出等），请使用浏览器控制面板或临时生成的密钥。切勿在共享环境中暴露具有高权限的密钥。
- **先在沙箱环境中进行测试** — 创建临时生成的、范围有限的密钥用于测试。测试完成后立即撤销。切勿在多个租户之间共享密钥。

## AI代理集成

支持Claude Desktop、Claude.ai、Claude Code和OpenAI Custom GPT的25种MCP工具。

**用户操作要求** — 每项集成都需要用户手动进行设置。该技能不会自动安装任何代码。

请参阅[integrations.md](integrations.md)以获取设置指南和安全注意事项。

---

## 模块说明

每个模块都有自己的SKILL.md文件，其中包含API端点和curl示例：

- **moltflow**（核心模块）：处理会话、消息传递、群组管理、标签设置、Webhook配置
- **moltflow-outreach**：支持批量发送消息、安排发送、生成报告、管理自定义群组
- **moltflow-ai**：支持风格匹配、RAG技术、语音转录、AI回复
- **moltflow-leads**：处理潜在客户检测、CRM管道管理、批量操作、数据导出
- **moltflow-a2a**：支持代理之间的安全通信协议和加密消息传递
- **moltflow-reviews**：收集评价、进行情感分析、导出用户评价
- **moltflow-admin**：处理身份验证、API密钥管理、计费功能和使用情况跟踪
- **moltflow-onboarding**：提供只读账户访问权限、账户健康检查以及增长机会报告

---

## 其他注意事项

- 所有消息都遵循反垃圾邮件规则（包括发送速率限制和随机延迟）
- 首次连接时需要使用二维码进行配对
- 使用E.164电话格式发送消息（无需添加`+`符号）
- AI相关功能和A2A功能需要Pro计划或更高级别的订阅
- 发送速率限制：免费账户限10条/分钟，Starter账户限20条/分钟，Pro账户限40条/分钟，Business账户限60条/分钟

## 更新日志

**v2.11.3**（2026-02-15）——完整更新日志请参见[CHANGELOG.md](CHANGELOG.md)。

<!-- FILEMAP:BEGIN -->
```text
[moltflow file map]|root: .
|.:{SKILL.md,CHANGELOG.md,integrations.md,package.json}
|moltflow:{SKILL.md}
|moltflow-ai:{SKILL.md}
|moltflow-a2a:{SKILL.md}
|moltflow-reviews:{SKILL.md}
|moltflow-outreach:{SKILL.md}
|moltflow-leads:{SKILL.md}
|moltflow-admin:{SKILL.md}
|moltflow-onboarding:{SKILL.md}
```
<!-- FILEMAP:END -->