---
name: "WhatsApp All-in-One CRM — ERC-8004 Agent | Campaign Analytics, Bulk Send, AI Outreach, Lead Detection, Support & MCP Server"
version: "2.13.0"
description: "这是您所需的唯一一款 WhatsApp 插件（Skill）。该插件提供了详细的文档和 API 参考资料，但没有任何功能会自动安装或执行——所有操作都需要用户明确发起。插件支持发送消息、收集潜在客户信息、运行营销活动、安排报告生成、跟踪营销活动效果以及管理客户信息等功能。业务开发人员（BizDev agents）会分析账户元数据以发现业务增长的机会。此外，还可以通过单独的设置来使用 MCP 服务器（MCP Server）和自定义的 GPT 功能（详情请参阅 integrations.md）。该插件拥有超过 90 个 API 端点，支持批量发送消息、定时发送消息、通过 WhatsApp 发送报告、AI 自动回复（可复制回复格式）、知识库管理、群组监控、潜在客户评分、反馈收集、营销活动效果跟踪等功能，并严格遵守 GDPR 法规，同时支持代理之间的通信协议（agent-to-agent protocol）。"
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

**目前，您的WhatsApp群组中隐藏着成千上万的潜在客户。**每个未在您的联系人列表中的群组成员都可能是潜在客户。MoltFlow可以根据您的需求分析群组，发现未被利用的联系人，并让您代表您运行基于AI的外展活动。

**一个技能，超过90个API端点。零手动寻找潜在客户。**

> **业务发展代理**：将Claude指向您的群组，
> 看看它的效果。它会找到未回复的联系人，
> 检测群组对话中的购买信号，
> 发现您未监控的高价值群组，并创建
> 定向的潜在客户列表。所有分析都在您请求时按需运行——后台不会自动执行任何操作。

> **MCP服务器 + 自定义GPT动作**：与Claude Desktop、Claude.ai（远程MCP）、Claude Code（插件）和ChatGPT（自定义GPT动作）兼容。支持25种工具。请参阅[integrations.md](integrations.md)以获取设置指南。

> **由于需求量大以及最近出现的注册问题，我们正在限时提供顶级商业计划，每月仅需19.90美元，即可无限使用名额。** [**立即购买**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)

> 提供免费 tier。 [注册](https://molt.waiflow.app/checkout?plan=free)

---

## 只需告诉Claude

安装该技能，设置您的API密钥，然后告诉Claude您的需求：

**“在每月28日向所有有未付发票的客户发送付款提醒”**

创建一个自定义群组，安排一个定期消息，并确保消息按时送达（考虑时区差异）。

**“将患者的语音记录转录并保存为预约摘要”**

对收到的语音消息进行转录，可通过API检索。

**“当有人在我的房产群组中提到‘预算’、‘卧室’或‘查看’时提醒我”**

在WhatsApp群组中监控关键词，自动将联系人添加到您的潜在客户列表中。

**“在每次购买后自动发送订单确认消息”**

设置Webhook监听器，通过API触发 outbound 消息。

**“在每次预订后收集客户评价并导出最佳评价”**

收集带有情感评分的评价，自动批准正面评价，并以HTML格式导出到您的网站。

**“每周一将活动绩效报告发送到我的团队WhatsApp群组”**

安排报告并通过WhatsApp发送，包含10种模板和活动分析数据。

**“安排对3天内未回复的潜在客户发送跟进消息”**

根据潜在客户列表中的筛选条件，安排消息发送到自定义群组。

**“将班级时间表变更广播到所有父群组”**

批量发送到自定义群组，具有防屏蔽限制和发送跟踪功能。

**“使用我的知识库文档自动回复支持问题”**

基于您上传的PDF和文档，使用RAG（Reactive Adaptive Generation）技术生成AI回复。

**“在我与潜在客户沟通后，将他们的状态从‘新’更改为‘已联系’，并跟踪转化率”**

使用状态机管理CRM流程，批量更新状态，并可导出CSV文件。

**“为请求GDPR数据删除的客户导出所有数据”**

通过API进行符合GDPR标准的数据导出和联系人删除。

**“显示本周哪些活动的阅读率最高”**

提供活动分析数据，包括发送渠道、每个联系人的状态和参与度评分。

---

## 代码示例

### 获取活动分析数据——送达率、渠道、时间安排

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/campaigns/{job_id}"
```

返回送达率、失败原因、每分钟发送的消息数量，
以及每个联系人的完整送达状态。

### 实时跟踪送达情况（SSE）

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/bulk-send/{id}/progress"
```

服务器发送的事件流：显示已发送/失败/待处理的消息数量，
并在每条消息送达时实时更新。

### 按参与度评分排序的顶级联系人

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/contacts?sort=engagement_score&limit=50"
```

根据发送和接收的消息数量、回复率以及最近活跃程度进行排序——
立即找到最活跃的联系人。

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

### 列出潜在客户列表

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/leads?status=new&limit=50"
```

### 在流程中移动潜在客户

```bash
curl -X PATCH -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "qualified"}' \
  https://apiv2.waiflow.app/api/v2/leads/{lead_id}/status
```

状态流转：`新` → `已联系` → `符合条件` → `转化`
（或在任何阶段变为`丢失`）。

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

### 用您的写作风格生成AI回复 + 使用知识库

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
| 链路 | 以太坊主网（eip155:1） |
| 注册处 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| 信任模型 | 基于声誉的 |
| API端点 | A2A + MCP + Web |

**发现信息：**
- 代理卡片：`https://molt.waiflow.app/.well-known/erc8004-agent.json`
- A2A发现信息：`https://apiv2.waiflow.app/.well-known/agent.json`

---

## 使用场景

**个人创始人/小型企业**
- 在聊天中找到未回复的潜在客户
- 用您的写作风格生成AI回复
- 定期向自定义群组发送推广信息

**代理机构/多客户**
- 监控50多个群组
- 批量发送消息，具有防屏蔽限制
- 将潜在客户信息导出为CSV文件，推送到n8n/Zapier

**营销机构/活动经理**
- 从点击式WhatsApp广告活动中捕获潜在客户
- 通过关键词检测和AI评分自动筛选潜在客户
- 批量发送跟进消息，具有防屏蔽限制
- 在多个客户账户之间管理多个会话
- 通过Webhook或CSV将潜在客户信息导出到CRM系统

**开发者/AI代理构建者**
- 超过90个REST API端点，提供API密钥
- 支持A2A协议和端到端加密
- Python SDK：`pip install moltflow` ([GitHub](https://github.com/moltflow/moltflow-python))

### 指南和教程

**AI集成指南：**
- [将ChatGPT连接到MoltFlow](https://molt.waiflow.app/guides/connect-chatgpt-to-moltflow) — 自定义GPT动作，10分钟设置
- [将Claude连接到MoltFlow](https://molt.waiflow.app/guides/connect-claude-to-moltflow) — MCP服务器设置，5分钟
- [将OpenClaw连接到MoltFlow](https://molt.waiflow.app/guides/connect-openclaw-to-moltflow) — 原生AI配置，5分钟设置

**操作指南：**
- [入门指南](https://molt.waiflow.app/blog/whatsapp-automation-getting-started)
- [API完整指南](https://molt.waiflow.app/blog/moltflow-api-complete-guide)
- [n8n集成](https://molt.waiflow.app/blog/moltflow-n8n-whatsapp-automation)
- [n8n + Google Sheets](https://molt.waiflow.app/blog/n8n-whatsapp-google-sheets)
- [n8n群组自动回复](https://molt.waiflow.app/blog/n8n-whatsapp-group-auto-reply)
- [n8n潜在客户流程](https://molt.waiflow.app/blog/n8n-whatsapp-lead-pipeline)
- [n8n多模型AI](https://molt.waiflow.app/blog/n8n-multi-model-ai-orchestration)
- [AI自动回复设置](https://molt.waiflow.app/blog/ai-auto-replies-whatsapp-setup)
- [群组潜在客户生成](https://molt.waiflow.app/blog/whatsapp-group-lead-generation-guide)
- [客户支持](https://molt.waiflow.app/blog/openclaw-whatsapp-customer-support)
- [RAG知识库](https://molt.waiflow.app/blog/rag-knowledge-base-deep-dive)
- [风格匹配](https://molt.waiflow.app/blog/ai-auto-replies-whatsapp-setup#style-profiles)
- [潜在客户评分](https://molt.waiflow.app/blog/whatsapp-lead-scoring-automation)
- [反馈收集](https://molt.waiflow.app/blog/whatsapp-customer-feedback-collection)
- [A2A协议](https://molt.waiflow.app/blog/a2a-protocol-agent-communication)
- [扩大ROI](https://molt.waiflow.app/blog/scaling-whatsapp-automation-roi)

[所有指南 →](https://molt.waiflow.app/guides)

---

## 平台特性

| 特性 | 详情 |
|---|---|
| 消息传递 | 文本、媒体、投票、vCards |
| 批量发送 | 具有防屏蔽限制，支持SSE（Server-Sent Events） |
| 定时发送 | 支持Cron调度，考虑时区差异 |
| 报告 | 提供10种模板，支持Cron调度和WhatsApp发送 |
| 分析 | 活动渠道分析、联系人评分、发送时间优化 |
| 群组管理 | 支持自定义列表和CSV导出 |
| 潜在客户管理 | 检测潜在客户信号，管理流程 |
| 监控 | 支持监控50多个群组和关键词 |
| 标签管理 | 数据同步到WhatsApp业务系统 |
| AI回复 | 支持GPT-4/Claude和RAG技术 |
| 文风克隆 | 自动匹配您的写作风格 |
| RAG技术 | 支持PDF/TXT格式，支持语义搜索 |
| 语音功能 | 支持语音转录 |
| 评价管理 | 支持情感分析，自动批准评价 |
| 防垃圾邮件 | 设置发送速率限制和模拟输入行为 |
| 安全措施 | 防止个人信息泄露，防止注入恶意内容 |
| Webhook | 支持HMAC签名，支持10多种事件类型 |
| A2A功能 | 支持端到端加密和JSON-RPC协议 |
| GDPR合规 | 自动过期处理，确保数据合规 |
| 送达跟踪 | 支持实时SSE跟踪，显示消息状态（已阅读/已回复/被忽略） |

---

## MoltFlow与其他产品的比较

| | Molt | 替代方案1 | 替代方案2 | 替代方案3 |
|---|:---:|:---:|:---:|:---:|
| 消息传递 | 18个功能 | 14个功能 | 3个功能 | 1个功能 |
| 群组管理 | 8个功能 | 4个功能 | 0个功能 | 0个功能 |
| 外展功能 | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| CRM集成 | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| AI功能 | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| 评价管理 | 8个功能 | 0个功能 | 0个功能 | 0个功能 |
| 安全性 | 10个功能 | 0个功能 | 0个功能 | 0个功能 |
| 平台综合评分 | **90多个功能** | **约15个功能** | **约3个功能** | **约1个功能 |

---

## 该技能的功能

**该技能仅用于读取、写入数据，不会自动执行任何操作。** 该软件包不包含任何自动安装或自动执行的脚本或可执行文件。所有操作都需要用户确认。

| 功能类别 | 所执行操作 | 是否需要用户授权？ |
|---|---|---|
| API调用 | 仅通过HTTPS连接到`apiv2.waiflow.app` | 不需要（使用您的API密钥） |
| 联系人元数据 | 联系人姓名、时间戳、发送次数 | 不需要 |
| CRM流程管理 | 联系人状态、参与度评分 | 不需要 |
| AI相关功能 | 通过API提供统计分析 | 需要用户同意 |
| 本地文件 | `.moltflow.json`文件（仅用于计数，不包含个人信息） | 不需要 |
| API密钥 | 作为环境变量存储，不会被记录或共享 | 不需要 |

**该技能绝不会：**
- 自动安装任何软件包或代码
- 未经用户明确授权就发送消息
- 向未列入白名单的号码发送消息（除非另有配置）
- 规避任何反垃圾邮件或内容安全措施
- 与第三方共享数据
- 将凭证存储在文件中（仅通过环境变量存储）

---

## 设置说明

> **提供免费tier** — 允许1次使用，
> 每月发送50条消息，无需信用卡。

**环境变量：**
- `MOLTFLOW_API_KEY`（必填）——从[您的控制面板](https://molt.waiflow.app)创建一个
  最小范围的API密钥。根据您的工作流程选择合适的范围。定期更换密钥。
- `MOLTFLOW_API_URL`（可选）——默认值为`https://apiv2.waiflow.app`

**认证方式：**
在请求头中添加`X-API-Key: $MOLTFLOW_API_KEY`或`Authorization: Bearer $TOKEN`（JWT）。

**基础URL：`https://apiv2.waiflow.app/api/v2`

---

## 安全性注意事项

- **强制使用最小范围的API密钥** — 创建密钥时必须指定`scopes`。始终创建最窄范围的密钥（例如，仅允许`messages:send`操作）。对于常见工作流程，可以使用预设范围如“Messaging”或“Read Only”。切勿使用全范围密钥与AI代理配合使用。
- **使用环境变量存储密钥** — 将`MOLTFLOW_API_KEY`设置为环境变量，不要将其存储在共享配置文件中。定期更换密钥。
- **电话号码白名单** — 在租户设置中配置`allowed_numbers`，以限制允许发送消息的号码。仅允许列入白名单的号码发送消息。
- **反垃圾邮件措施** — 所有 outbound 消息都会经过互惠检查（对方必须先发送消息）、发送速率限制、模拟输入行为和随机延迟等安全措施。这些措施无法被绕过。
- **内容安全** — 对所有 outbound 消息进行检测，防止个人信息泄露和恶意内容注入。
- **审批机制** — 在租户设置中启用`require_approval`选项，以确保所有AI生成的消息在发送前都需要人工审核。
- **Webhook验证** — API会阻止私密IP地址、云服务元数据和非HTTPS协议的请求。仅配置您控制的API端点。务必为HMAC签名设置`secret`参数。
- **安装第三方插件前的审核** — 如果您要安装MCP或GPT集成，请先检查插件的来源和维护者信息。该技能不会自动安装或执行任何插件。
- **运行前的本地审核** — Python示例脚本托管在GitHub上，不会随软件包一起提供。请下载并检查源代码后再运行。
- **在共享环境中使用低权限密钥** — 对于管理员操作（如密钥轮换、数据导出），请使用浏览器控制面板或临时生成的密钥。切勿在共享环境中暴露高级权限密钥。
- **先在沙箱环境中进行测试** — 创建临时生成的、有限范围的密钥进行测试。测试完成后立即撤销密钥。切勿在多个租户之间共享密钥。

## AI代理集成

支持Claude Desktop、Claude.ai、Claude Code和OpenAI Custom GPT的25种MCP工具。

**用户操作要求** — 每个集成都需要用户手动进行设置。该技能不会自动安装任何代码。

请参阅[integrations.md](integrations.md)以获取设置指南和安全注意事项。

---

## 模块说明

每个模块都有自己的SKILL.md文件，其中包含API端点和curl示例：

- **moltflow**（核心模块）：处理会话、消息传递、群组管理、Webhook功能
- **moltflow-outreach**：支持批量发送消息、定时发送消息、安排报告、管理自定义群组
- **moltflow-ai**：提供风格克隆、RAG技术、语音转录和AI回复功能
- **moltflow-leads**：负责潜在客户检测、CRM流程管理、批量操作和数据导出
- **moltflow-a2a**：实现代理之间的安全通信和加密消息传递
- **moltflow-reviews**：收集评价、进行情感分析并导出评价结果
- **moltflow-admin**：处理授权、API密钥管理、计费和使用情况跟踪
- **moltflow-onboarding**：提供业务发展代理功能、按需账户分析和服务机会发现

---

## 其他注意事项

- 所有消息都遵循反垃圾邮件规则（包括发送速率限制和随机延迟）
- 首次连接时需要使用二维码进行配对
- 使用E.164电话格式发送消息（无需添加`+`前缀）
- AI相关功能和A2A功能需要使用Pro计划或更高级别的订阅
- 发送速率限制：免费账户限10条/分钟，Starter账户限20条/分钟，Pro账户限40条/分钟，Business账户限60条/分钟

---

## 更新日志

**v2.11.3**（2026-02-15）——详细更新日志请参见[CHANGELOG.md](CHANGELOG.md)。

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