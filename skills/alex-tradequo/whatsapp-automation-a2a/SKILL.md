---
name: "WhatsApp All-in-One CRM — ERC-8004 Agent | Campaign Analytics, Bulk Send, AI Outreach, Lead Mining, Support & MCP Server"
version: "2.11.3"
description: "这是您所需要的唯一一款 WhatsApp 插件（Skill）。该插件提供了详细的文档和 API 参考资料，但没有任何功能会自动安装或执行；所有操作都需要用户明确地发起。插件提供了用于发送消息、捕获潜在客户信息、运行营销活动、安排报告生成、跟踪营销活动分析结果以及管理客户信息的接口。业务开发人员（BizDev agents）会分析账户元数据，以发现业务增长的机会。此外，还可以通过单独的设置来使用 MCP 服务器（MCP Server）和自定义的 GPT 功能（详情请参见 integrations.md）。该插件拥有超过 90 个 API 接口，支持批量发送消息、定时发送消息、通过 WhatsApp 发送报告、生成具有特定风格的 AI 回复、监控群组动态、对潜在客户进行评分、收集用户反馈、跟踪营销活动的参与情况、确保数据合规性（符合 GDPR 规定），以及实现代理之间的通信协议（agent-to-agent protocol）。"
source: "MoltFlow Team"
risk: safe
homepage: "https://molt.waiflow.app"
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"📱","homepage":"https://molt.waiflow.app","requires":{"env":["MOLTFLOW_API_KEY"]},"primaryEnv":"MOLTFLOW_API_KEY"}}
---
# WhatsApp自动化——从WhatsApp群组中挖掘潜在客户

**目前，你的WhatsApp群组中隐藏着成千上万的潜在客户。**每个未添加到你联系人列表中的群组成员都可能是潜在客户。MoltFlow可以根据你的需求分析这些群组，找出未被利用的联系人，并让你通过Claude发起基于人工智能的外展活动。

**一个技能，支持90多个API端点。完全无需人工寻找潜在客户。**

> **业务发展代理（BizDev Growth Agent）**：将Claude指向你的群组，观察其效果。它会找到未回复的消息、检测群组对话中的购买信号、发现你未监控的高价值群组，并生成针对性的潜在客户列表。所有分析都在你请求时按需执行——不会在后台自动运行。

> **MCP服务器 + 自定义GPT动作（MCP Server + Custom GPT Actions）**：支持Claude Desktop、Claude.ai（远程MCP）、Claude Code（插件）和ChatGPT（自定义GPT动作）。共有25种工具。详情请参阅[integrations.md](integrations.md)。

> **由于需求量大以及最近出现的注册问题，我们正在限时提供顶级商务计划，每月只需19.90美元，即可享受无限使用量。** [**立即购买**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)

> **免费试用层也可使用。** [立即注册](https://molt.waiflow.app/checkout?plan=free)

---

## 如何使用Claude

安装该技能，设置你的API密钥，然后开始使用：

**“分析我的WhatsApp账户以寻找增长机会”**  
查找未回复的消息、未监控的群组以及冷联系人。按需执行——聊天历史分析需要用户明确同意。

**“找到我尚未跟进的冷联系人”**  
查找7天以上未收到回复的联系人，并提供重新联系的建议。

**“为我的房地产群组设置关键词监控”**  
添加关键词触发器，自动将联系人添加到你的潜在客户管道中。

**“收集我的客服聊天中的客户反馈”**  
进行情感分析，自动批准积极的反馈，并以HTML格式导出。

**“每周一上午9点向我的VIP客户列表发送促销信息”**  
支持时区设置，具有防屏蔽机制，并可追踪发送情况。

**“在我开会时自动回复我的WhatsApp消息”**  
使用你之前的消息风格生成AI回复。

---

## 代码示例

### 获取活动分析数据——发送率、渠道、时间安排  
```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/campaigns/{job_id}"
```

返回发送率、失败原因、每分钟的发送消息数量以及每个联系人的发送状态。

### 实时跟踪发送情况（SSE）  
```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/bulk-send/{id}/progress"
```

服务器发送的事件流：显示已发送/失败/待处理的消息数量，每条消息发送时实时更新。

### 按互动得分排序的顶级联系人  
```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/contacts?sort=engagement_score&limit=50"
```

根据发送和接收的消息数量、回复率以及消息的新鲜度进行排序——立即找到最活跃的联系人。

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

### 将新联系人添加到你的潜在客户管道中  
```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/leads?status=new&limit=50"
```

### 将联系人推进潜在客户管道  
```bash
curl -X PATCH -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "qualified"}' \
  https://apiv2.waiflow.app/api/v2/leads/{lead_id}/status
```

状态流程：`新联系人` → `已联系` → `符合条件` → `转化`
（或在任何阶段`丢失`）。

### 将联系人批量添加到活动群组  
```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_ids": ["uuid-1", "uuid-2", "uuid-3"],
    "custom_group_id": "target-group-uuid"
  }' \
  https://apiv2.waiflow.app/api/v2/leads/bulk/add-to-group
```

### 将联系人列表导出为CSV  
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

### 用你的写作风格生成AI回复  
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

### 安排每周的跟进邮件  
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

### 每周将报告发送到你的WhatsApp  
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

完整API参考：请参阅每个模块的SKILL.md文件。

---

## ERC-8004代理注册

MoltFlow是一个经过验证的链上AI代理，注册在**以太坊主网**上。

| 字段 | 值 |
|-------|-------|
| 代理ID | [#25248](https://8004agents.ai/agent/25248) |
| 链路 | 以太坊主网（EIP155:1） |
| 注册处 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| 信任模型 | 基于声誉的 |
| API端点 | A2A + MCP + Web |

**相关信息：**
- 代理卡片：`https://molt.waiflow.app/.well-known/erc8004-agent.json`
- A2A代理信息：`https://apiv2.waiflow.app/.well-known/agent.json`

---

## 使用场景

**个人创始人/小型企业**  
- 在聊天中查找未回复的潜在客户  
- 用你的写作风格生成AI回复  
- 定时向自定义群组发送促销信息

**代理机构/多客户企业**  
- 监控50多个群组  
- 批量发送消息，具有防屏蔽机制  
- 将联系人列表导出为CSV格式，或推送到n8n/Zapier

**营销机构/活动经理**  
- 从点击链接进入WhatsApp的广告活动中捕获潜在客户  
- 通过关键词检测和AI评分自动筛选潜在客户  
- 批量发送跟进消息，具有防屏蔽机制  
- 在多个客户账户间管理多个会话  
- 通过Webhook或CSV将活动联系人导出到CRM系统

**开发者/AI代理构建者**  
- 提供90多个REST API端点  
- 支持A2A协议和端到端加密  
- 提供Python脚本（[GitHub](https://github.com/moltflow/moltflow/tree/main/skills/moltflow-clawhub/scripts)  

### 指南与教程

**AI集成指南：**  
- [将ChatGPT连接到MoltFlow](https://molt.waiflow.app/guides/connect-chatgpt-to-moltflow) — 自定义GPT动作，设置只需10分钟  
- [将Claude连接到MoltFlow](https://molt.waiflow.app/guides/connect-claude-to-moltflow) — MCP服务器设置，只需5分钟  
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
- [风格训练](https://molt.waiflow.app/blog/learn-mode-style-training-whatsapp)  
- [潜在客户评分](https://molt.waiflow.app/blog/whatsapp-lead-scoring-automation)  
- [反馈收集](https://molt.waiflow.app/blog/whatsapp-customer-feedback-collection)  
- [A2A协议](https://molt.waiflow.app/blog/a2a-protocol-agent-communication)  
- [提升ROI](https://molt.waiflow.app/blog/scaling-whatsapp-automation-roi)  

[所有指南 →](https://molt.waiflow.app/guides)

---

## 平台特性

| 特性 | 详情 |
|---|---|
| 消息传递 | 文本、媒体、投票、vCard |
| 批量发送 | 具有防屏蔽机制，支持实时进度跟踪（SSE） |
| 定时发送 | 支持Cron任务，考虑时区设置 |
| 报告 | 提供10种模板，支持Cron任务和WhatsApp发送 |
| 分析 | 活动渠道分析、联系人评分、发送时间优化 |
| 群组管理 | 支持自定义列表和CSV导出 |
| 潜在客户管理 | 自动检测联系人，支持导入到CRM系统 |
| 监控 | 支持监控50多个群组和关键词 |
| 标签管理 | 数据同步到WhatsApp业务系统 |
| AI回复 | 使用GPT-4/Claude技术生成回复 |
| 风格复制 | 根据你的消息风格生成回复 |
| 情感分析 | 支持PDF/TXT格式，提供语义搜索 |
| 语音功能 | 支持语音转录 |
| 评论管理 | 支持情感分析，自动批准积极评论 |
| 防垃圾邮件 | 设有发送速率限制和模拟输入功能 |
| 安全保护 | 防止个人信息泄露，阻止恶意数据注入 |
| Webhook | 支持HMAC签名，支持10多种事件类型 |
| A2A通信 | 支持端到端加密和JSON-RPC协议 |
| 遵守GDPR法规 | 自动设置过期时间，确保合规 |
| 发送跟踪 | 支持实时跟踪，显示消息状态（已发送/已阅读/已忽略） |

---

## MoltFlow与其他产品的对比

| | Molt | 替代方案1 | 替代方案2 | 替代方案3 |
|---|---:|:---:|:---:|:---:|
| 消息传递 | 18个功能 | 14个功能 | 3个功能 | 1个功能 |
| 群组管理 | 8个功能 | 4个功能 | 0个功能 | 0个功能 |
| 外展活动 | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| 客户关系管理（CRM） | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| AI功能 | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| 评论管理 | 8个功能 | 0个功能 | 0个功能 | 0个功能 |
| 安全性 | 10个功能 | 0个功能 | 0个功能 | 0个功能 |
| 平台综合能力 | 90多个功能 | 约15个功能 | 约3个功能 | 约1个功能 |

---

## 该技能的功能

**该技能仅用于：**  
文档阅读、API调用以及提供相关参考信息。不会自动安装或执行任何内容。此软件包不包含脚本或可执行文件。所有操作均需用户确认。

| 功能类别 | 执行内容 | 是否需要用户同意？ |
|---|---|---|
| API调用 | 仅通过HTTPS连接到`apiv2.waiflow.app` | 不需要（使用你的API密钥） |
| 聊天元数据 | 显示联系人名称和时间戳 | 不显示 |
| 消息内容 | 仅显示前500个字符的预览 | 显示（需用户同意） |
| 业务发展分析 | 统计发送次数，不包含个人信息 | 不包含 |
| 风格分析 | 显示统计模式，不显示原始文本 | 需用户同意 |
| 本地文件 | 生成`.moltflow.json`文件（仅记录发送次数，不包含个人信息） | 不包含 |
| API密钥 | 作为本地环境变量存储，不会被记录或共享 | 不包含 |

**该技能绝不会：**  
- 自动安装任何软件包或运行代码  
- 未经用户同意就阅读完整消息内容  
- 未经用户确认就发送消息  
- 向未列入白名单的号码发送消息  
- 规避任何反垃圾邮件或内容安全措施  
- 与第三方共享数据  
- 将凭证存储在文件中（仅作为环境变量）  

---

## 设置说明

> **免费试用层可用** — 允许1次会话，每月发送50条消息，无需信用卡。

**环境变量：**  
- `MOLTFLOW_API_KEY`（必需）—— 请从[你的仪表板](https://molt.waiflow.app)获取  
- `MOLTFLOW_API_URL`（可选）—— 默认值为`https://apiv2.waiflow.app`  

**认证方式：**  
在请求头中添加`X-API-Key: $MOLTFLOW_API_KEY`  
或使用`Authorization: Bearer $TOKEN`（JWT认证）。  

**基础URL：** `https://apiv2.waiflow.app/api/v2`

---

## 安全性注意事项  

- **使用受限的API密钥** — 创建密钥时必须指定权限范围（例如`messages:send`、`leads:read`）。根据常见工作流程选择合适的权限范围。  
- **聊天历史记录需要用户明确同意** — API会验证用户的同意意愿。例如“扫描我的聊天记录”或“风格训练”等功能只有在用户通过仪表板 > 设置 > 数据访问启用权限后才能使用。为遵守GDPR法规，这些功能默认是禁用的。  
- **使用环境变量存储密钥** — 将`MOLTFLOW_API_KEY`设置为环境变量，不要将其存储在共享配置文件中。定期更换密钥。  
- **电话号码白名单** — 在租户设置中配置`allowed_numbers`，以限制可发送消息的号码。仅允许列入白名单的号码发送消息。  
- **反垃圾邮件措施** — 所有外出消息都会经过双向检查（对方必须先发送消息）、发送速率限制、模拟输入延迟等机制。这些措施无法被绕过。  
- **内容安全** — 对所有外出消息进行隐私信息（PII）检测，防止恶意数据注入。  
- **审核机制** — 在租户设置中启用`require_approval`选项，确保所有AI生成的回复都需经过人工审核后再发送。  
- **Webhook验证** — API会阻止私有IP地址、云服务元数据和非HTTPS协议的请求。仅配置你控制的API端点。  
- **运行前检查第三方软件包** — 如果你使用外部工具（如MCP或GPT集成），请先查看软件包的来源和维护者信息。该技能不会自动安装或执行任何第三方软件包。  
- **在测试环境中进行测试** — 先在测试环境中使用临时密钥。测试完成后立即撤销密钥。切勿在多个租户之间共享密钥。  

## AI代理集成  

MoltFlow支持与Claude Desktop、Claude.ai、Claude Code和OpenAI Custom GPT的集成。  

**用户操作说明：**  
每个集成都需要用户手动进行设置。该技能不会自动安装任何代码。  

详细设置指南和安全注意事项请参阅[integrations.md](integrations.md)。

---

## 模块说明  

每个模块都有自己的SKILL.md文件，其中包含API端点和curl示例：  
- **moltflow**（核心模块）：处理会话、消息传递、群组管理、Webhook  
- **moltflow-outreach**：批量发送消息、定时发送消息、生成报告、管理自定义群组  
- **moltflow-ai**：生成个性化回复、进行情感分析、提供语音转录服务  
- **moltflow-leads**：检测潜在客户、管理潜在客户管道、执行批量操作  
- **moltflow-a2a**：支持代理间的安全通信  
- **moltflow-reviews**：收集用户评价、进行情感分析、导出评价内容  
- **moltflow-admin**：处理用户认证、管理API密钥、记录使用情况  

---

## 其他注意事项  

- 所有消息都经过反垃圾邮件处理（包括模拟输入和延迟机制）  
- 首次连接时需要使用二维码配对  
- 支持E.164电话号码格式（不包含`+`符号）  
- AI功能和A2A功能需要使用Pro级及以上计划  
- 发送速率限制：免费账户限制为10条/分钟，Starter账户限制为20条/分钟，Pro账户限制为40条/分钟，Business账户限制为60条/分钟  

## 更新日志  

**v2.11.3**（2026-02-15）——完整更新记录请参阅[CHANGELOG.md](CHANGELOG.md)。

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