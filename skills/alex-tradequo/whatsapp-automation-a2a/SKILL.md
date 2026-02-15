---
name: "WhatsApp All-in-One CRM — Campaign Analytics, Engagement Tracking, Bulk Send, AI Outreach, Lead Mining, Reviews & MCP Server"
version: "2.10.2"
description: "这是您唯一需要的 WhatsApp 技能（skill）。提供了详细的文档和 API 参考资料，但没有任何功能会自动安装或自动执行；所有操作都需要用户明确发起。该技能支持发送消息、收集潜在客户信息、运行营销活动、安排报告发送、跟踪营销活动分析结果以及管理客户信息等功能。BizDev 代理会分析账户元数据以发现潜在的增长机会。此外，还支持通过单独的设置来使用 MCP 服务器和自定义的 GPT 功能（详见 integrations.md）。该技能拥有超过 90 个 API 端点，支持批量发送消息、定时发送消息、通过 WhatsApp 发送报告、智能回复（具备风格克隆功能）、知识库管理、群组监控、潜在客户评分、反馈收集、营销活动分析及参与度跟踪等功能，并符合 GDPR 法规要求，同时支持代理之间的通信协议。"
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

**目前，你的WhatsApp群组中隐藏着成千上万的潜在客户。**任何不在你联系人列表中的群组成员都可能是潜在客户。MoltFlow可以根据你的需求分析这些群组，找出未被利用的联系人，并让你通过Claude发起基于人工智能的外展活动。

**一个技能，支持90多个API接口，零手动客户开发工作。**

> **业务开发成长助手**：将Claude指向你的群组，
> 看看它的效果。它会找到未回复的联系人，
> 检测群组对话中的购买信号，
> 发现你未监控的高价值群组，并生成针对性的潜在客户列表。所有分析都在你请求时按需进行——不会在后台自动运行。

> **MCP服务器 + 自定义GPT操作**：支持Claude Desktop、Claude.ai（远程MCP）、Claude Code（插件）和ChatGPT（自定义GPT操作）。共有25种工具。详情请参阅[integrations.md](integrations.md)。

> **由于需求量大以及近期注册问题，我们正在限时提供顶级商业计划，每月仅需19.90美元，即可无限使用该计划。** [**立即购买**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)

> 提供免费试用版本。 [立即注册](https://molt.waiflow.app/checkout?plan=free)

---

## 只需向Claude发出指令

安装该技能，设置你的API密钥，然后开始使用：

**“分析我的WhatsApp账户以寻找增长机会”**

找到未回复的联系人、未被监控的群组以及冷联系人。按需运行——聊天历史分析需要用户明确同意。

**“查找我尚未跟进的冷联系人”**

找到7天以上未收到回复的联系人，并提供重新联系的建议。

**“为我的房地产群组设置关键词监控”**

添加关键词触发器，自动将联系人添加到你的潜在客户管道中。

**“从我的支持聊天中收集客户反馈”**

进行情感分析，自动批准正面反馈，并导出为HTML格式。

**“每周一上午9点向我的VIP客户列表发送促销信息”**

支持时区设置，具有防封禁机制，并可追踪发送情况。

**“在我开会时自动回复我的WhatsApp消息”**

使用你之前的消息风格生成AI回复。

---

## 代码示例

### 获取活动分析数据——发送率、转化漏斗、发送时间

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/campaigns/{job_id}"
```

返回发送率、失败原因、每分钟发送的消息数量以及每个联系人的详细发送状态。

### 实时跟踪发送情况（SSE）

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/bulk-send/{id}/progress"
```

服务器发送的事件流：显示已发送/失败/待发送的消息数量，
并在每条消息发送时实时更新。

### 按互动得分排序的顶级联系人

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/contacts?sort=engagement_score&limit=50"
```

根据发送和接收的消息数量、回复率以及消息的最新时间进行排序——立即找到最活跃的联系人。

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

### 在管道中推进联系人的状态

```bash
curl -X PATCH -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "qualified"}' \
  https://apiv2.waiflow.app/api/v2/leads/{lead_id}/status
```

状态流转：`new` → `contacted` → `qualified` → `converted`
（或在任何阶段变为`lost`）。

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

### 将联系人列表导出为CSV格式

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

### 每周向你的WhatsApp发送报告

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

### 发现双向互动（A2A）代理

```bash
curl https://apiv2.waiflow.app/.well-known/agent.json
```

完整的API参考：请参阅每个模块的SKILL.md文件。

---

## 使用场景

**个人创始人/小型企业**
- 在聊天中找到未回复的潜在客户
- 用你的写作风格生成AI回复
- 定时向自定义群组发送促销信息

**代理机构/多客户企业**
- 监控50多个群组
- 批量发送消息，同时避免被封禁
- 将联系人列表导出为CSV格式，然后推送到n8n/Zapier

**营销机构/活动经理**
- 从点击链接进入WhatsApp的广告活动中捕获潜在客户
- 通过关键词检测和AI评分自动筛选潜在客户
- 批量发送跟进信息，同时避免被封禁
- 在多个客户账户之间管理多个会话
- 通过Webhook或CSV将活动联系人导出到CRM系统

**开发者/AI代理构建者**
- 支持90多个REST接口和API密钥
- 支持双向互动（A2A）协议和端到端加密
- 为每种工作流程提供Python脚本（[GitHub](https://github.com/moltflow/moltflow/tree/main/skills/moltflow-clawhub/scripts)

### 教程与指南

**AI集成指南：**
- [将ChatGPT连接到MoltFlow](https://molt.waiflow.app/guides/connect-chatgpt-to-moltflow) — 自定义GPT操作，设置只需10分钟
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
- [提升投资回报率（ROI）](https://molt.waiflow.app/blog/scaling-whatsapp-automation-roi)

[所有指南 →](https://molt.waiflow.app/guides)

---

## 平台特性

| 特性 | 详情 |
|---|---|
| 消息传递 | 文本、媒体文件、投票、vCards |
| 批量发送 | 具有防封禁机制，支持实时进度跟踪（SSE） |
| 定时发送 | 支持Cron任务，考虑时区设置 |
| 报告 | 提供10种模板，支持Cron任务和WhatsApp发送 |
| 分析 | 活动转化漏斗、联系人评分、发送时间优化 |
| 群组管理 | 支持自定义列表和CSV导出 |
| 潜在客户管理 | 自动检测联系人，支持导入到CRM系统 |
| 监控 | 支持监控50多个群组和关键词 |
| 标签管理 | 可同步到WhatsApp业务系统 |
| AI回复 | 支持GPT-4/Claude和RAG技术 |
| 文风克隆 | 可根据你的消息风格生成回复 |
| 情感分析 | 支持PDF/TXT格式，支持语义搜索 |
| 语音功能 | 支持语音转文字 |
| 评价收集 | 支持情感分析，自动批准正面评价 |
| 防垃圾邮件 | 设置发送速率限制，模拟用户输入 |
| 安全保护 | 防止个人身份信息（PII）泄露 |
| Webhook | 支持HMAC签名，支持10多种事件类型 |
| 双向互动（A2A） | 支持端到端加密和JSON-RPC协议 |
| 遵守GDPR法规 | 自动设置消息有效期，确保合规 |
| 发送跟踪 | 支持实时跟踪，显示消息状态（已阅读/已回复/被忽略） |

---

## MoltFlow与其他产品的比较

| | Molt | 替代方案1 | 替代方案2 | 替代方案3 |
|---|:---:|:---:|:---:|:---:|
| 消息传递 | 18个功能 | 14个功能 | 3个功能 | 1个功能 |
| 群组管理 | 8个功能 | 4个功能 | 0个功能 | 0个功能 |
| 外展活动 | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| 客户关系管理（CRM） | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| AI功能 | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| 评价收集 | 8个功能 | 0个功能 | 0个功能 | 0个功能 |
| 安全性 | 10个功能 | 0个功能 | 0个功能 | 0个功能 |
| 平台综合能力 | 90多个功能 | 约15个功能 | 约3个功能 | 约1个功能 |

---

## 该技能的功能

**该技能的功能包括：**  
- 文档生成和API参考。**没有任何内容会自动安装或执行。此软件包不包含任何脚本或可执行文件。所有操作都需要用户确认。  
- **读取和写入内容：**  
  - 仅读取文档和API参考信息；  
  - 不会自动安装任何软件或执行任何代码；  
  - 不会在未经用户明确同意的情况下发送消息。  
- **发送范围：**  
  - 仅通过HTTPS连接到`apiv2.waiflow.app`；  
  - 不会读取联系人的完整消息内容（除非用户明确同意）；  
  - 不会向未列入白名单的号码发送消息（除非用户设置允许）；  
  - 会遵守反垃圾邮件规则和内容安全措施；  
- **数据安全：**  
  - 防止个人身份信息（PII）泄露；  
  - 在发送消息前会进行必要的安全检查；  
- **设置：**  
  - 提供免费试用版本（1次会话，每月50条消息，无需信用卡）；  
  - 需要设置环境变量`MOLTFLOW_API_KEY`和`MOLTFLOW_API_URL`；  
- **安全性：**  
  - 使用API密钥时需设置权限范围（例如`messages:send`、`leads:read`）；  
  - 消息历史记录的访问需要用户明确同意；  
  - 遵守GDPR法规，定期更换API密钥；  
- **其他功能：**  
  - 支持批量发送、定时发送、报告生成、群组管理、标签设置等；  
  - 提供AI回复和双向互动（A2A）功能；  
  - 支持多种平台集成（如Claude Desktop、Claude.ai等）。  

---

## 如何设置

> **免费试用版本**：  
  - 1次会话，每月50条消息，无需信用卡。  

**环境变量：**  
- `MOLTFLOW_API_KEY`（必填）：从[你的控制面板](https://molt.waiflow.app)获取；  
- `MOLTFLOW_API_URL`（可选）：默认为`https://apiv2.waiflow.app`。  

**认证方式：**  
- 使用`X-API-Key: $MOLTFLOW_API_KEY`头部；  
- 或者使用`Authorization: Bearer $TOKEN`（JWT认证）。  

**基础URL：** `https://apiv2.waiflow.app/api/v2`  

---

## 注意事项

- **请注意：**  
  - 该技能不会自动安装任何软件或代码；  
  - 所有操作都需要用户确认；  
  - 请确保遵循平台的安全规定和隐私政策。