---
name: "WhatsApp All-in-One CRM — ERC-8004 Agent | Campaign Analytics, Bulk Send, AI Outreach, Lead Detection, Support & MCP Server"
version: "2.11.8"
description: "这是您所需的唯一一款 WhatsApp 技能工具。该工具提供了详细的文档和 API 参考信息，但没有任何功能会自动安装或执行；所有操作都需要用户明确发起。该工具支持发送消息、收集潜在客户信息、运行营销活动、安排报告生成、跟踪营销活动分析结果以及管理客户信息等功能。业务开发人员会分析账户元数据以发现潜在的增长机会。此外，还支持通过单独的设置使用 MCP 服务器和自定义的 GPT 功能（详见 integrations.md）。该工具拥有超过 90 个 API 接口，支持批量发送消息、定时发送消息、通过 WhatsApp 发送报告、使用 AI 生成回复（并保留回复风格）、群组监控、潜在客户评分、收集用户反馈、跟踪用户参与度、符合 GDPR 法规要求，以及实现代理之间的通信协议。"
source: "MoltFlow Team"
risk: safe
homepage: "https://molt.waiflow.app"
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"📱","homepage":"https://molt.waiflow.app","requires":{"env":["MOLTFLOW_API_KEY"]},"primaryEnv":"MOLTFLOW_API_KEY"}}
---
# WhatsApp自动化——分析群组以发现购买信号

**目前，您的WhatsApp群组中隐藏着成千上万的潜在客户。**每个未在您的联系人列表中的群组成员都可能是潜在客户。MoltFlow可以根据您的需求分析群组，挖掘出未被利用的联系人，并让您代表您运行基于AI的外展活动。

**一项技能，支持90多个API端点。零手动寻客工作。**

> **业务发展代理**：将Claude指向您的群组，
> 看看它的效果。它能找到未回复的联系人，
> 检测群组对话中的购买信号，
> 发现您未监控的高价值群组，并创建
> 定向的潜在客户列表。所有分析都在您请求时按需运行——后台不会自动执行任何操作。

> **MCP服务器 + 自定义GPT动作**：支持Claude Desktop、Claude.ai（远程MCP）、Claude Code（插件）和ChatGPT（自定义GPT动作）。共有25种工具。请参阅[integrations.md](integrations.md)以获取设置指南。

> **由于需求量大以及最近出现的注册问题，我们正在限时提供顶级商业计划，每月仅需19.90美元，即可享受无限使用量。** [**立即购买**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)

> 提供免费试用版。 [立即注册](https://molt.waiflow.app/checkout?plan=free)

---

## 只需告诉Claude

安装该技能，设置您的API密钥，然后开始使用：

**“分析我的WhatsApp账户以寻找增长机会”**

找到未回复的联系人、未监控的群组以及需要跟进的潜在客户。按需运行——对话内容需要用户的明确同意。

**“找到我尚未跟进的潜在客户”**

查找7天以上未收到回复的联系人，并提供重新联系的建议。

**“为我的房地产群组设置关键词监控”**

添加关键词触发器，将购买信号纳入您的处理流程。

**“从我的支持聊天中收集客户反馈”**

进行情感分析，自动批准正面评论，并导出为HTML格式。

**“每周一上午9点向我的VIP客户列表发送促销信息”**

支持时区设置，具有防禁言机制的发送间隔控制，以及发送跟踪功能。

**“在我开会时自动回复我的WhatsApp消息”**

AI回复会模仿您的写作风格。

---

## 代码示例

### 获取活动分析数据——发送率、渠道分布、发送时间

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/campaigns/{job_id}"
```

返回发送率、失败原因、每分钟的发送消息数量，
以及每个联系人的完整发送状态。

### 实时跟踪发送情况（SSE）

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/bulk-send/{id}/progress"
```

服务器发送的事件流：已发送/失败/待处理的消息数量
会在每条消息发送时实时更新。

### 按参与度评分排序的顶级联系人

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/contacts?sort=engagement_score&limit=50"
```

根据发送和接收的消息数量、回复率以及最近活跃度进行排序——立即找到最活跃的联系人。

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

### 将新潜在客户添加到您的处理流程中

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/leads?status=new&limit=50"
```

### 将潜在客户推进处理流程

```bash
curl -X PATCH -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "qualified"}' \
  https://apiv2.waiflow.app/api/v2/leads/{lead_id}/status
```

状态流转：`新` → `已联系` → `已评估` → `已转化`
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

### 将潜在客户导出为CSV格式

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

### 以您的写作风格生成AI回复 + 知识库

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

### 安排每周的跟进

```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monday check-in",
    "session_id": "uuid",
    "chat_id": "123@c.us",
    "message": "Hey! Anything I can help with this week?",
    "recurrence": "weekly",
    "scheduled_time": "2026-02-17T09:00:00",
    "timezone": "America/New_York"
  }' \
  https://apiv2.waiflow.app/api/v2/scheduled-messages
```

### 每周向您的WhatsApp发送报告

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

MoltFlow是一个经过验证的链上AI代理，注册在**以太坊主网**上。

| 字段 | 值 |
|-------|-------|
| 代理ID | [#25248](https://8004agents.ai/ethereum/agent/25248) |
| 链路 | 以太坊主网 (EIP155:1) |
| 注册处 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| 信任模型 | 基于声誉 |
| API端点 | A2A + MCP + Web |

**相关信息：**
- 代理卡片：`https://molt.waiflow.app/.well-known/erc8004-agent.json`
- A2A发现信息：`https://apiv2.waiflow.app/.well-known/agent.json`

---

## 使用场景

**个人创始人/小型企业**
- 在聊天中找到未回复的潜在客户
- 以您的写作风格生成AI回复
- 定时向自定义群组发送促销信息

**代理机构/多客户企业**
- 监控50多个群组
- 批量发送消息并设置防禁言机制
- 将潜在客户信息导出为CSV格式，或推送到n8n/Zapier

**营销机构/活动经理**
- 从点击链接进入WhatsApp的广告活动中捕获潜在客户
- 通过关键词检测和AI评分自动评估潜在客户
- 设置防禁言机制的批量跟进流程
- 跨客户账户管理多会话
- 通过Webhook或CSV将活动潜在客户信息导出到CRM系统

**开发者/AI代理构建者**
- 提供90多个REST API端点
- 支持E2A协议和端到端加密
- 提供适用于各种工作流程的Python脚本（[GitHub](https://github.com/moltflow/moltflow/tree/main/skills/moltflow-clawhub/scripts)

### 教程与指南

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
- [n8n潜在客户处理流程](https://molt.waiflow.app/blog/n8n-whatsapp-lead-pipeline)
- [n8n多模型AI](https://molt.waiflow.app/blog/n8n-multi-model-ai-orchestration)
- [AI自动回复设置](https://molt.waiflow.app/blog/ai-auto-replies-whatsapp-setup)
- [群组潜在客户生成](https://molt.waiflow.app/blog/whatsapp-group-lead-generation-guide)
- [客户支持](https://molt.waiflow.app/blog/openclaw-whatsapp-customer-support)
- [RAG知识库](https://molt.waiflow.app/blog/rag-knowledge-base-deep-dive)
- [风格匹配](https://molt.waiflow.app/blog/learn-mode-style-training-whatsapp)
- [潜在客户评分](https://molt.waiflow.app/blog/whatsapp-lead-scoring-automation)
- [反馈收集](https://molt.waiflow.app/blog/whatsapp-customer-feedback-collection)
- [A2A协议](https://molt.waiflow.app/blog/a2a-protocol-agent-communication)
- [提升投资回报率](https://molt.waiflow.app/blog/scaling-whatsapp-automation-roi)

[所有指南 →](https://molt.waiflow.app/guides)

---

## 平台功能

| 功能 | 详情 |
|---|---|
| 消息传递 | 文本、媒体、投票、vCard |
| 批量发送 | 具有防禁言机制，支持实时进度跟踪 |
| 定时发送 | 支持时区设置 |
| 报告 | 提供10种模板，支持定时发送和WhatsApp发送 |
| 分析 | 活动渠道分析、联系人评分、发送时间优化 |
| 群组管理 | 自定义列表、CSV导出 |
| 潜在客户管理/CRM | 检测潜在客户信号、管理处理流程 |
| 监控 | 支持监控50多个群组和关键词 |
| 标签管理 | 数据同步到WhatsApp业务系统 |
| AI回复 | 使用GPT-4/Claude技术生成回复 |
| 文风复制 | 生成与您的写作风格匹配的回复 |
| 情感分析 | 支持PDF/TXT格式，支持语义搜索 |
| 语音功能 | 支持语音转录 |
| 评论管理 | 支持情感分析，自动批准正面评论 |
| 防垃圾邮件 | 设置发送速率限制和模拟输入行为 |
| 安全防护 | 防止个人信息泄露，防止注入恶意代码 |
| Webhook | 支持HMAC签名，支持10多种事件类型 |
| A2A通信 | 支持端到端加密，使用JSON-RPC协议 |
| 遵守GDPR法规 | 自动设置消息有效期，确保合规性 |
| 发送跟踪 | 支持实时发送跟踪，显示消息状态（已阅读/已回复/被忽略） |

---

## MoltFlow与其他产品的比较

| | Molt | 替代方案1 | 替代方案2 | 替代方案3 |
|---|:---:|:---:|:---:|:---:|
| 消息传递 | 18个功能 | 14个功能 | 3个功能 | 1个功能 |
| 群组管理 | 8个功能 | 4个功能 | 0个功能 | 0个功能 |
| 外展功能 | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| CRM集成 | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| AI功能 | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| 评论管理 | 8个功能 | 0个功能 | 0个功能 | 0个功能 |
| 安全性 | 10个功能 | 0个功能 | 0个功能 | 0个功能 |
| 平台综合评分 | 90多个功能 | 约15个功能 | 约3个功能 | 约1个功能 |

---

## 该技能的功能

**该技能的功能包括：**文档生成、API调用等。**没有任何内容会自动安装或执行。此包中不包含任何脚本或可执行文件。所有操作都需要用户的确认。

| 功能类别 | 所执行操作 | 是否需要用户同意？ |
|---|---|---|
| API调用 | 仅通过HTTPS连接到`apiv2.waiflow.app` | 不需要（使用您的API密钥） |
| 联系人元数据 | 联系人姓名、时间戳、发送次数 | 不会收集 |
| 对话内容 | 仅提供摘要，需用户同意 | 需要（设置 > 数据访问权限） |
| CRM处理流程 | 潜在客户状态、参与度评分 | 不会收集 |
| AI相关功能 | 仅提供统计分析结果，不包含原始文本 | 需要用户同意（可开启/关闭） |
| 本地文件 | 生成`.moltflow.json`文件，仅记录发送次数，不包含个人信息 | 不会收集 |
| API密钥 | 作为本地环境变量存储，不会被记录或共享 | 不会收集 |

**该技能绝不会：**
- 自动安装任何软件包或运行代码
- 未经用户同意就访问对话内容
- 未经用户确认就发送消息
- 向未列入白名单的号码发送消息
- 规避任何反垃圾邮件或内容安全措施
- 与第三方共享数据
- 将凭证存储在文件中（仅作为环境变量存储）

---

## 设置说明

> **提供免费试用版**——允许1次会话，每月发送50条消息，无需信用卡。

**环境变量：**
- `MOLTFLOW_API_KEY`（必填）——请从[您的控制面板](https://molt.waiflow.app)创建一个最小权限范围的API密钥。请使用符合您工作流程的最窄权限范围的密钥，并定期更换。
- `MOLTFLOW_API_URL`（可选）——默认值为`https://apiv2.waiflow.app`

**认证方式：**
在请求头中添加`X-API-Key: $MOLTFLOW_API_KEY`或`Authorization: Bearer $TOKEN`（JWT格式）。

**基础URL：**`https://apiv2.waiflow.app/api/v2`

---

## 安全性注意事项

- **强制使用最小权限范围的API密钥**——创建密钥时必须指定权限范围。始终使用最小权限范围的密钥（例如，仅允许`messages:send`操作）。对于常见工作流程，可以使用预设的权限范围（如“Messaging”或“Read Only”）。切勿为AI代理使用全权限范围的密钥。
- **对话内容的使用需用户明确同意**——API会检查用户是否同意使用对话内容。除非您在控制面板 > 设置 > 数据访问中启用相关权限，否则AI相关功能将无法使用。
- **使用环境变量存储密钥**——将`MOLTFLOW_API_KEY`设置为环境变量，不要将其存储在共享配置文件中，并定期更换密钥。
- **电话号码白名单**——在租户设置中配置`allowed_numbers`，以限制可发送消息的号码范围。仅允许列入白名单的号码发送消息。
- **反垃圾邮件措施**——所有 outbound 消息都会经过双向验证（对方必须先发送消息）、发送速率限制、模拟输入行为和随机延迟检查。这些措施无法被绕过。
- **内容安全防护**——所有 outbound 消息都会被检查是否包含个人信息或恶意代码。发送前会自动阻止此类内容。
- **审批机制**——在租户设置中启用`require_approval`选项，以便所有AI生成的消息在发送前都需要人工审核。
- **Webhook验证**——API会阻止来自私有IP地址、使用非HTTPS协议的请求，并仅允许您控制的API端点。
- **在运行前检查第三方包**——在安装MCP或GPT集成之前，请先检查相关包的来源和维护者信息。该技能不会自动安装或执行任何第三方包。
- **在本地运行前检查脚本**——Python示例脚本托管在GitHub上，不会随软件包一起提供。请下载并检查源代码后再运行。
- **在共享环境中避免使用高权限密钥**——对于管理员操作（如密钥更换、数据导出），请使用浏览器控制面板或临时生成的权限范围有限的密钥。切勿在共享环境中暴露具有高权限的密钥。
- **先在沙箱环境中进行测试**——创建一个临时生成的、权限范围有限的密钥用于测试。测试完成后立即删除该密钥。切勿在多个租户之间共享密钥。

## AI代理集成

支持与Claude Desktop、Claude.ai、Claude Code和OpenAI Custom GPT的25种集成方案。

**用户操作说明**——每个集成都需要用户手动进行设置。该技能不会自动安装任何代码。

请参阅[integrations.md](integrations.md)以获取设置指南和安全注意事项。

---

## 模块说明

每个模块都有对应的SKILL.md文件，其中包含API端点和curl使用示例：

- **moltflow**（核心模块）：处理会话、消息传递、群组管理、Webhook设置
- **moltflow-outreach**：支持批量发送、定时发送消息、生成报告、自定义群组管理
- **moltflow-ai**：支持风格复制、情感分析、语音转录、AI回复功能
- **moltflow-leads**：负责潜在客户检测、CRM处理流程管理、批量操作
- **moltflow-a2a**：支持代理间通信、加密消息传递
- **moltflow-reviews**：负责收集用户评价、情感分析、生成评价报告
- **moltflow-admin**：负责管理用户权限、API密钥、计费功能及使用情况监控
- **moltflow-onboarding**：提供业务发展代理服务、按需分析账户信息、发现潜在客户机会

---

## 其他注意事项

- 所有消息都会经过反垃圾邮件检查（包括模拟输入行为和发送速率限制）。
- 首次连接时需要使用二维码进行配对。
- 请使用E.164电话格式发送消息，且消息前缀不得包含“+”。
- AI相关功能和A2A功能需要使用Pro级及以上的订阅计划。
- 发送速率限制：免费账户限制为10条/分钟，Starter账户限制为20条/分钟，Pro账户限制为40条/分钟，Business账户限制为60条/分钟。

## 更新日志

**v2.11.3**（2026-02-15）——完整更新日志请参阅[CHANGELOG.md](CHANGELOG.md)。

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