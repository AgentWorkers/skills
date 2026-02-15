---
name: "WhatsApp All-in-One CRM — Campaign Analytics, Engagement Tracking, Bulk Send, AI Outreach, Lead Mining, Reviews & MCP Server"
version: "2.9.4"
description: "这是您所需要的唯一一款 WhatsApp 技能插件。该插件提供详细的文档和 API 参考资料，但没有任何功能会自动安装或执行；所有操作都需要用户明确发起。插件支持发送消息、收集潜在客户信息、运行营销活动、安排报告发送、跟踪营销活动分析结果以及管理客户信息等功能。业务开发人员（BizDev agents）会分析账户元数据以发现业务增长机会。此外，还支持通过单独的配置流程使用 MCP 服务器（MCP Server）和自定义的 GPT 功能（详情请参阅 integrations.md）。该插件拥有超过 90 个 API 接口，支持批量发送消息、定时发送消息、通过 WhatsApp 发送报告、使用 AI 生成个性化回复、群组监控、潜在客户评分、收集用户反馈、跟踪用户参与度、遵守 GDPR 法规，以及实现代理之间的通信协议（agent-to-agent protocol）。"
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

**目前，你的WhatsApp群组中隐藏着成千上万的潜在客户。**任何不在你联系人列表中的群组成员都可能是潜在客户。MoltFlow可以根据你的需求分析这些群组，挖掘出未被利用的联系人，并让你通过Claude发起基于人工智能的外展活动。

**一项技能，支持90多个API端点，完全无需人工寻找潜在客户。**

> **业务发展代理**：将Claude指向你的群组，观察它的效果。它会找到未回复的消息、检测群组对话中的购买信号、发现你未监控的高价值群组，并生成有针对性的潜在客户列表。所有分析都在你请求时按需执行——不会在后台自动运行。

> **MCP服务器 + 自定义GPT动作**：支持Claude Desktop、Claude.ai（远程MCP）、Claude Code（插件）和ChatGPT（自定义GPT动作）。共有25种工具。详情请参阅[integrations.md](integrations.md)。

> **由于需求量大以及近期注册问题，我们正在限时提供顶级商业计划，每月仅需19.90美元，即可享受无限使用量。** [**立即购买**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)

> **免费试用版也可使用。** [立即注册](https://molt.waiflow.app/checkout?plan=free)

---

## 只需向Claude发出指令

安装该技能，设置你的API密钥，然后开始使用：

**“分析我的WhatsApp账户以寻找增长机会”**  
- 查找未回复的消息、未被监控的群组以及冷门潜在客户。按需执行——聊天记录分析需要用户明确同意。

**“查找我尚未跟进的冷门潜在客户”**  
- 找出7天以上未收到回复的联系人，并提供重新联系的建议。

**“为我的房地产群组设置关键词监控”**  
- 添加关键词触发器，自动将潜在客户添加到你的管道中。

**“从我的客服聊天中收集客户反馈”**  
- 进行情感分析，自动批准正面反馈，并导出为HTML格式。

**“每周一上午9点向我的VIP客户列表发送促销信息”**  
- 支持时区设置，具有防封禁机制，可追踪发送情况。

**“在我开会时自动回复我的WhatsApp消息”**  
- 使用与你消息风格匹配的AI回复。

---

## 代码示例

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

### 安排定时消息  
```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Monday update",
    "session_id": "uuid",
    "chat_id": "123@c.us",
    "message": "...",
    "recurrence": "weekly",
    "scheduled_time": "2026-02-17T09:00:00",
    "timezone": "America/New_York"
  }' \
  https://apiv2.waiflow.app/api/v2/scheduled-messages
```

### 创建定期报告  
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

### 获取活动分析数据  
```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/campaigns/{job_id}"
```

### 获取联系人参与度排行榜  
```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/contacts?sort=engagement_score&limit=50"
```

### 监控群组中的关键词  
```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "session_id": "uuid",
    "wa_group_id": "120363012345@g.us",
    "monitor_mode": "keywords",
    "monitor_keywords": ["looking for", "need help", "budget"]
  }' \
  https://apiv2.waiflow.app/api/v2/groups
```

### 列出新潜在客户  
```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/leads?status=new&limit=50"
```

### 生成带有风格的AI回复  
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

### 创建反馈收集工具  
```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Customer Feedback",
    "session_id": "uuid",
    "source_type": "all",
    "min_sentiment_score": 0.7,
    "include_keywords": ["thank", "recommend", "love"],
    "languages": ["en"]
  }' \
  https://apiv2.waiflow.app/api/v2/reviews/collectors
```

### 发现A2A代理  
```bash
curl https://apiv2.waiflow.app/.well-known/agent.json
```

### 创建受限范围的API密钥  
```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "outreach-bot",
    "scopes": [
      "messages:send",
      "custom-groups:manage",
      "bulk-send:manage"
    ],
    "expires_in_days": 90
  }' \
  https://apiv2.waiflow.app/api/v2/api-keys
```

### 订阅Webhook事件  
Webhook地址会在服务器端进行验证（会阻止私有IP和非HTTPS地址）。务必设置`secret`字段用于HMAC签名验证。  
```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "url": "https://your-server.com/webhook",
    "events": [
      "message.received",
      "lead.detected",
      "session.connected"
    ],
    "secret": "whsec_your_secret_here"
  }' \
  https://apiv2.waiflow.app/api/v2/webhooks
```

完整API参考：请参阅每个模块的SKILL.md文件。

---

## 使用场景

**个人创始人/小型企业**  
- 在聊天中查找未回复的潜在客户  
- 使用你的写作风格生成AI回复  
- 定时向自定义群组发送促销信息

**代理机构/多客户企业**  
- 监控50多个群组  
- 批量发送消息，同时具备防封禁机制  
- 将潜在客户数据导出为CSV格式，或推送到n8n/Zapier

**营销机构/活动经理**  
- 从点击式WhatsApp广告活动中捕获潜在客户  
- 通过关键词检测和AI评分自动筛选潜在客户  
- 批量跟进潜在客户，同时具备防封禁机制  
- 在多个客户账户间管理多个会话  
- 通过Webhook或CSV格式将潜在客户数据导出到CRM系统

**开发者/AI代理构建者**  
- 支持90多个REST API端点  
- 使用A2A协议进行端到端加密  
- 提供适用于各种工作流程的Python脚本（[GitHub](https://github.com/moltflow/moltflow/tree/main/skills/moltflow-clawhub/scripts)  

### 指南与教程  

**AI集成指南：**  
- [将ChatGPT连接到MoltFlow](https://molt.waiflow.app/guides/connect-chatgpt-to-moltflow) — 自定义GPT动作，设置只需10分钟  
- [将Claude连接到MoltFlow](https://molt.waiflow.app/guides/connect-claude-to-moltflow) — MCP服务器（使用`npx @moltflow/mcp-server`），设置只需5分钟  
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
| 消息传递 | 文本、媒体、投票、vCards |
| 批量发送 | 具有防封禁机制，支持SSE进度显示 |
| 定时发送 | 支持Cron任务，考虑时区设置 |
| 报告 | 提供10种模板，支持Cron任务和WhatsApp发送 |
| 分析 | 支持活动跟踪、联系人评分、发送时间优化 |
| 群组管理 | 支持自定义列表和CSV导出 |
| 潜在客户管理 | 自动检测潜在客户，支持导入到CRM系统 |
| 监控 | 支持监控50多个群组和关键词 |
| 标签管理 | 数据可同步到WhatsApp业务系统 |
| AI回复 | 使用GPT-4/Claude技术生成回复 |
| 风格复制 | 根据你的消息内容生成回复 |
| 情感分析 | 支持PDF/TXT格式，支持语义搜索 |
| 语音功能 | 支持语音转录 |
| 评论管理 | 支持情感分析，自动批准积极评论 |
| 防垃圾邮件 | 设有发送速率限制和模拟输入机制 |
| 安全措施 | 防止个人信息泄露，阻止恶意数据注入 |
| Webhook | 支持HMAC签名，支持10多种事件类型 |
| A2A功能 | 支持端到端加密和JSON-RPC协议 |
| 遵守GDPR法规 | 支持数据删除和自动过期设置 |

---

## MoltFlow与其他产品的对比  

| | Molt | 替代方案1 | 替代方案2 | 替代方案3 |
|---|:---:|:---:|:---:|:---:|
| 消息传递 | 18项功能 | 14项功能 | 3项功能 | 1项功能 |
| 群组管理 | 8项功能 | 4项功能 | 0项功能 | 0项功能 |
| 外展活动 | 7项功能 | 0项功能 | 0项功能 | 0项功能 |
| CRM集成 | 7项功能 | 0项功能 | 0项功能 | 0项功能 |
| AI支持 | 7项功能 | 0项功能 | 0项功能 | 0项功能 |
| 评论管理 | 8项功能 | 0项功能 | 0项功能 | 0项功能 |
| 安全性 | 10项高级安全措施 | 0项功能 | 0项功能 | 0项功能 |
| 平台整体 | 共80多项功能 | 约15项功能 | 约3项功能 | 约1项功能 |

---

## 该技能的功能  

**该技能的功能包括：**  
- 文档和API参考：不会自动安装或执行任何内容。此软件包中不包含任何脚本或可执行文件。所有操作都需要用户确认。  
- **数据读取与写入**：仅读取文档和API相关数据；不会自动执行任何操作。  
- **权限设置**：明确要求用户同意才能读取聊天记录、发送消息等。  

| 功能类别 | 具体操作 | 是否需要用户同意？ |
|---|---|---|
| API调用 | 仅通过HTTPS连接到`apiv2.waiflow.app` | 不需要（使用用户的API密钥） |
| 聊天元数据 | 读取联系人姓名、时间戳和消息数量 | 不需要 |
| 消息内容 | 仅提供500个字符的预览内容 | 需要用户同意（用于聊天记录访问） |
| 业务发展分析 | 统计消息数量，不包含个人信息 | 不需要 |
| 风格分析 | 生成统计模式，不包含原始文本 | 需要用户同意 |
| 本地文件 | 读取`.moltflow.json`文件（仅统计数据，不包含个人信息） | 不需要 |
| API密钥 | 作为本地环境变量存储，不会被记录或共享 | 不需要 |

**该技能绝不会：**  
- 自动安装软件包或运行代码  
- 未经用户同意就读取完整消息内容  
- 未经用户确认就发送消息  
- 向未列入白名单的号码发送消息  
- 规避任何反垃圾邮件或内容安全措施  
- 与第三方共享数据  
- 将凭证存储在文件中（仅作为环境变量）  

---

## 设置说明  

> **免费试用版可用**：  
- 允许1次会话，每月发送50条消息，无需信用卡。  

**环境变量设置：**  
- `MOLTFLOW_API_KEY`（必填）：从[你的仪表板](https://molt.waiflow.app)获取  
- `MOLTFLOW_API_URL`（可选）：默认为`https://apiv2.waiflow.app`  

**认证方式：**  
在请求头中添加`X-API-Key: $MOLTFLOW_API_KEY`  
或使用`Authorization: Bearer $TOKEN`（JWT认证）。  

**基础URL：** `https://apiv2.waiflow.app/api/v2`  

---

## 安全性说明  

- **使用受限范围的API密钥**：创建密钥时必须指定权限范围（例如`messages:send`、`leads:read`）。根据常用工作流程选择合适的权限范围。  
- **聊天记录访问需要用户同意**：API会强制要求用户同意才能访问聊天记录。  
- **遵循GDPR法规**：默认情况下，访问聊天记录的功能会被禁用。  
- **使用环境变量存储密钥**：将`MOLTFLOW_API_KEY`设置为环境变量，避免在共享配置文件中存储。定期更换密钥。  
- **电话号码白名单**：在租户设置中配置`allowed_numbers`，以限制发送消息的号码范围。只有列入白名单的号码才能发送消息。  
- **反垃圾邮件措施**：所有出站消息都会经过双向验证（接收方必须先发送消息）、发送速率限制、模拟输入机制和随机延迟处理。  
- **内容安全**：出站消息会经过严格检查，防止个人信息泄露和恶意数据注入。  
- **审核机制**：在租户设置中启用`require_approval`选项，确保所有AI生成的回复都需要人工审核后再发送。  
- **Webhook验证**：仅允许安全的Webhook地址（排除私有IP和非HTTPS协议）。  
- **运行前验证包文件**：在运行npx命令前，确认包的名称和版本。  
- **本地预览脚本**：Python脚本托管在GitHub上，运行前请先下载并检查代码。  
- **安全使用高权限密钥**：在共享环境中使用临时密钥进行管理操作（如密钥轮换和数据导出）。  

---

## AI代理集成  

支持Claude Desktop、Claude.ai、Claude Code和OpenAI Custom GPT的25种MCP工具。  
**用户操作说明**：每种集成都需要用户手动配置。该技能不会自动安装任何代码。  
详情请参阅[integrations.md](integrations.md)中的设置说明和配置示例。  

---

## 模块说明  

每个模块都有自己的SKILL.md文件，其中包含API端点和curl使用示例：  
- **moltflow**（核心模块）：会话管理、消息传递、群组管理、Webhook设置  
- **moltflow-outreach**：批量发送消息、定时发送、定期报告、自定义群组管理  
- **moltflow-ai**：风格复制、情感分析、语音转录、AI回复  
- **moltflow-leads**：潜在客户检测、CRM集成、批量操作、数据导出  
- **moltflow-a2a**：支持代理间的安全通信  
- **moltflow-reviews**：评论收集、情感分析、评价收集  
- **moltflow-admin**：权限管理、API密钥管理、计费设置、GDPR合规性检查  
- **moltflow-onboarding**：协助业务发展、按需分析、潜在客户发现  

## 示例脚本  

11个独立的Python脚本可在GitHub上下载：  
[github.com/moltflow/moltflow/tree/main/skills/moltflow-clawhub/scripts](https://github.com/moltflow/moltflow/tree/main/skills/moltflow-clawhub/scripts)  
- `quickstart.py`：创建会话、发送第一条消息  
- `send_message.py`：向联系人发送文本消息  
- `outreach.py`：批量发送消息、定时发送  
- `analytics.py`：分析活动数据、生成潜在客户排行榜、导出CSV文件  
- `leads.py`：管理潜在客户、批量操作、数据导出  
- `ai_config.py`：训练回复风格、生成AI回复  
- `reviews.py`：创建评论收集工具、导出用户评价  
- `group_monitor.py`：监控群组和潜在客户  
- `a2a_client.py`：发现其他代理、发送A2A消息  
- `admin.py`：登录、创建API密钥、管理计费  
- `gdpr.py`：删除客户数据、导出数据  

这些脚本不包含在该软件包中。请从GitHub下载脚本，查看源代码后手动运行：  
`MOLTFLOW_API_KEY=key python quickstart.py`

---

## 其他注意事项：  
- 所有消息都遵循反垃圾邮件规则（包括发送速率限制和随机延迟机制）。  
- 首次连接时需要通过二维码配对。  
- 使用E.164电话格式发送消息（无需添加`+`符号）。  
- AI功能和A2A功能需要高级订阅计划才能使用。  
- 发送速率限制：免费账户限制为10条/分钟，初级账户20条/分钟，高级账户40条/分钟，企业账户60条/分钟。  

## 更新日志  

**v2.9.0**（2026-02-14）——详细更新日志请查看[CHANGELOG.md](CHANGELOG.md)。  

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