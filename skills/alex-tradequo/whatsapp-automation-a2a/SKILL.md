---
name: "WhatsApp All-in-One CRM — ERC-8004 Agent | Campaign Analytics, Bulk Send, AI Outreach, Lead Mining, Support & MCP Server"
version: "2.11.4"
description: "这是您所需要的唯一一款 WhatsApp 技能工具。该工具提供了详细的文档和 API 参考信息，但没有任何内容会自动安装或执行；所有操作都需要用户明确发起。该工具支持发送消息、捕获潜在客户信息、运行营销活动、安排报告生成、跟踪营销活动分析结果以及管理客户信息等功能。业务开发人员会分析账户元数据以发现潜在的增长机会。此外，还支持通过单独的设置来使用 MCP 服务器和自定义的 GPT 功能（详见 integrations.md）。该工具提供了超过 90 个 API 端点，支持批量发送消息、定时发送消息、通过 WhatsApp 发送报告、AI 自动回复（具备样式复制功能）、知识库管理、群组监控、潜在客户评分、反馈收集、营销活动分析及参与度跟踪等功能，并且符合 GDPR 法规要求，同时支持代理之间的通信协议。"
source: "MoltFlow Team"
risk: safe
homepage: "https://molt.waiflow.app"
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
metadata: {"openclaw":{"emoji":"📱","homepage":"https://molt.waiflow.app","requires":{"env":["MOLTFLOW_API_KEY"]},"primaryEnv":"MOLTFLOW_API_KEY"}}
---
# WhatsApp自动化 — 从WhatsApp群组中挖掘潜在客户

**目前，你的WhatsApp群组中隐藏着成千上万的潜在客户。** 所有不在你联系人列表中的群组成员都是潜在客户。MoltFlow可以根据你的需求分析这些群组，找出未被开发的联系人，并让你通过Claude代表你发起基于人工智能的外展活动。

**一个技能，支持90多个功能端点。零手动客户开发工作。**

> **业务发展代理（BizDev Growth Agent）**：将Claude指向你的群组，观看它的效果。它会找到未回复的联系人，检测群组对话中的购买信号，发现你未监控的高价值群组，并生成有针对性的潜在客户列表。所有分析都在你请求时按需进行——不会在后台自动运行。

> **MCP服务器 + 自定义GPT动作（MCP Server + Custom GPT Actions）**：支持Claude Desktop、Claude.ai（远程MCP）、Claude Code（插件）和ChatGPT（自定义GPT动作）。共有25种工具。详情请参阅[integrations.md](integrations.md)。

> **由于需求量大以及最近出现的注册问题，我们正在限时提供顶级商业计划，每月仅需19.90美元，即可享受无限使用额度。** [**立即抢购**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)

> **免费试用层级也可使用。** [立即注册](https://molt.waiflow.app/checkout?plan=free)

---

## 只需向Claude发出指令

安装该技能，设置你的API密钥，然后开始使用：

**“分析我的WhatsApp账户以寻找增长机会”**  
查找未回复的联系人、未被监控的群组以及冷线索（未跟进的联系人）。按需运行——聊天历史分析需要用户的明确许可。

**“找到我尚未跟进的冷线索”**  
查找7天以上未收到回复的联系人，并提供重新联系的建议。

**“为我的房地产群组设置关键词监控”**  
添加关键词触发器，自动将线索添加到你的工作流程中。

**“收集来自我的支持聊天的客户反馈”**  
进行情感分析，自动批准正面反馈，并以HTML格式导出。

**“每周一上午9点向我的VIP客户列表发送促销信息”**  
支持时区设置，具有防封禁机制的发送限制，以及发送跟踪功能。

**“在我开会时自动回复我的WhatsApp消息”**  
使用你之前的消息风格生成AI回复。

---

## 代码示例

### 获取活动分析数据 — 发送率、转化漏斗、发送时间

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/campaigns/{job_id}"
```

返回发送率、失败原因、每分钟的发送消息数量以及每个联系人的详细发送状态。

### 实时跟踪发送情况（SSE）

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/bulk-send/{id}/progress"
```

服务器发送的事件流：显示已发送/失败/待处理的消息数量，每条消息发送时都会实时更新。

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

### 将新线索添加到你的工作流程中

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/leads?status=new&limit=50"
```

### 将线索在工作流程中推进

```bash
curl -X PATCH -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"status": "qualified"}' \
  https://apiv2.waiflow.app/api/v2/leads/{lead_id}/status
```

状态流转：`new` → `contacted` → `qualified` → `converted`
（或在任何阶段变为`lost`）。

### 将线索批量添加到活动群组

```bash
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "lead_ids": ["uuid-1", "uuid-2", "uuid-3"],
    "custom_group_id": "target-group-uuid"
  }' \
  https://apiv2.waiflow.app/api/v2/leads/bulk/add-to-group
```

### 将线索导出为CSV格式

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

### 用你的写作风格生成AI回复 + 知识库回复

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
| 代理ID | [#25248](https://8004agents.ai/ethereum/agent/25248) |
| 链路 | 以太坊主网（EIP155:1） |
| 注册处 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| 信任模型 | 基于声誉的 |
| 功能端点 | A2A + MCP + Web |

**相关信息：**
- 代理卡片：`https://molt.waiflow.app/.well-known/erc8004-agent.json`
- A2A发现信息：`https://apiv2.waiflow.app/.well-known/agent.json`

---

## 使用场景

**个人创业者/小型企业**  
- 在聊天中找到未回复的线索  
- 用你的写作风格生成AI回复  
- 定时向自定义群组发送促销信息

**代理机构/多客户企业**  
- 监控50多个群组  
- 批量发送消息，同时具备防封禁机制  
- 将线索导出为CSV格式，或推送到n8n/Zapier

**营销机构/活动经理**  
- 从点击式WhatsApp广告活动中捕获线索  
- 通过关键词检测和AI评分自动筛选潜在客户  
- 批量发送消息，同时具备防封禁机制  
- 在多个客户账户间管理多个会话  
- 通过Webhook或CSV将活动线索导入CRM系统

**开发者/AI代理构建者**  
- 支持90多个REST端点，提供范围化的API密钥  
- 使用A2A协议进行端到端加密  
- 提供Python脚本（[GitHub](https://github.com/moltflow/moltflow/tree/main/skills/moltflow-clawhub/scripts)  

### 教程与指南

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
- [n8n线索工作流程](https://molt.waiflow.app/blog/n8n-whatsapp-lead-pipeline)  
- [n8n多模型AI](https://molt.waiflow.app/blog/n8n-multi-model-ai-orchestration)  
- [AI自动回复设置](https://molt.waiflow.app/blog/ai-auto-replies-whatsapp-setup)  
- [群组线索生成](https://molt.waiflow.app/blog/whatsapp-group-lead-generation-guide)  
- [客户支持](https://molt.waiflow.app/blog/openclaw-whatsapp-customer-support)  
- [RAG知识库](https://molt.waiflow.app/blog/rag-knowledge-base-deep-dive)  
- [风格训练](https://molt.waiflow.app/blog/learn-mode-style-training-whatsapp)  
- [线索评分](https://molt.waiflow.app/blog/whatsapp-lead-scoring-automation)  
- [反馈收集](https://molt.waiflow.app/blog/whatsapp-customer-feedback-collection)  
- [A2A协议](https://molt.waiflow.app/blog/a2a-protocol-agent-communication)  
- [提升ROI](https://molt.waiflow.app/blog/scaling-whatsapp-automation-roi)  

[所有指南 →](https://molt.waiflow.app/guides)

---

## 平台功能

| 功能 | 详情 |
|---|---|
| 消息传递 | 文本、媒体文件、投票、vCard |
| 批量发送 | 具备防封禁机制，支持实时更新（SSE） |
| 定时发送 | 支持时区设置 |
| 报告 | 提供10种模板，支持定时发送至WhatsApp |
| 分析 | 活动转化漏斗、联系人评分、发送时间优化 |
| 群组管理 | 自定义列表，支持CSV导出 |
| 线索管理/CRM | 自动检测线索，支持导入到CRM系统 |
| 监控 | 支持监控50多个群组，支持关键词搜索 |
| 标签管理 | 可与WhatsApp业务数据同步 |
| AI回复 | 使用GPT-4/Claude生成回复 |
| 文本风格克隆 | 根据你的消息风格生成回复 |
| 情感分析 | 支持PDF/TXT格式，支持语义搜索 |
| 语音功能 | 支持语音转录 |
| 评论管理 | 支持情感分析，自动批准积极评论 |
| 防垃圾邮件 | 设置发送速率限制，模拟用户输入 |
| 安全措施 | 防止个人信息泄露，防止数据注入 |
| Webhook | 支持HMAC签名，支持10多种事件类型 |
| A2A功能 | 支持端到端加密，使用JSON-RPC协议 |
| 遵守GDPR法规 | 自动设置消息有效期，确保合规性 |
| 发送跟踪 | 支持实时跟踪发送情况，包括阅读、回复或忽略的状态 |

---

## MoltFlow与其他产品的对比

| | Molt | 替代方案1 | 替代方案2 | 替代方案3 |
|---|:---:|:---:|:---:|:---:|
| 消息传递 | 18个功能 | 14个功能 | 3个功能 | 1个功能 |
| 群组管理 | 8个功能 | 4个功能 | 0个功能 | 0个功能 |
| 外展活动 | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| CRM集成 | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| AI功能 | 7个功能 | 0个功能 | 0个功能 | 0个功能 |
| 评论管理 | 8个功能 | 0个功能 | 0个功能 | 0个功能 |
| 安全性 | 10个功能 | 0个功能 | 0个功能 | 0个功能 |
| 平台整体 | 90多个功能 | 约15个功能 | 约3个功能 | 约1个功能 |

---

## 该技能的功能范围

**该技能仅用于：**  
文档阅读、API调用以及相关参考信息的提供。没有任何内容会自动安装或执行。此软件包不包含任何脚本或可执行文件。所有操作都需要用户的确认。

| 功能类别 | 所执行操作 | 是否需要用户许可？ |
|---|---|---|
| API调用 | 仅通过HTTPS连接到`apiv2.waiflow.app` | 不需要（使用你的API密钥） |
| 聊天元数据 | 联系人姓名、时间戳、发送次数 | 不会获取 |
| 消息内容 | 仅提供500个字符的预览 | 会获取（但需要用户同意） |
| 业务发展分析 | 统计发送次数，不涉及个人信息 | 不会获取 |
| 文本风格分析 | 分析统计模式，不获取原始文本 | 需要用户同意 |
| 本地文件 | `.moltflow.json`文件（仅用于统计，不涉及个人信息） | 不会获取 |
| API密钥 | 作为本地环境变量存储，不会被记录或共享 | 不会获取 |

**该技能绝不会：**  
- 自动安装任何软件包或运行代码  
- 未经用户许可自动读取完整消息内容  
- 未经用户确认自动发送消息  
- 向未列入白名单的号码发送消息  
- 规避任何反垃圾邮件或内容安全措施  
- 与第三方共享数据  
- 将凭证存储在文件中（仅作为环境变量）  

---

## 设置说明

> **免费试用层级可用** — 每月1次会话，50条消息，无需信用卡。  

**环境变量：**  
- `MOLTFLOW_API_KEY`（必填）—— 从[你的控制面板](https://molt.waiflow.app)获取  
- `MOLTFLOW_API_URL`（可选）—— 默认为`https://apiv2.waiflow.app`  

**认证方式：**  
在请求头中添加`X-API-Key: $MOLTFLOW_API_KEY`  
或使用`Authorization: Bearer $TOKEN`（JWT认证）。  

**基础URL：** `https://apiv2.waiflow.app/api/v2`  

---

## 安全性注意事项：**

- **使用范围化的API密钥** — 创建密钥时必须指定权限范围（例如`messages:send`、`leads:read`）。根据常见工作流程选择合适的权限范围。  
- **聊天历史记录需要用户许可** — API要求用户明确同意才能访问聊天记录。例如“扫描我的聊天记录”或“风格训练”等功能只有在用户通过控制面板 > 设置 > 数据访问启用权限后才能使用。为遵守GDPR法规，这些功能默认是禁用的。  
- **使用环境变量存储密钥** — 将`MOLTFLOW_API_KEY`设置为环境变量，避免在共享配置文件中存储。定期更换密钥。  
- **电话号码白名单** — 在租户设置中配置`allowed_numbers`，以限制可发送消息的号码。仅允许列入白名单的号码发送消息。  
- **反垃圾邮件措施** — 所有发送的消息都会经过双向验证（对方必须先给你发送消息）、发送速率限制、模拟用户输入以及随机延迟等安全检查。  
- **内容安全** — 发送的消息会经过个人信息检查、秘密内容检测以及防止注入的尝试。  
- **审批机制** — 在租户设置中启用`require_approval`选项，以便所有AI生成的消息在发送前都需要人工审核。  
- **Webhook验证** — API会阻止私有的IP地址、云服务元数据以及非HTTPS协议的请求。仅配置你控制的端点。  
- **运行前验证第三方插件** — 如果你使用外部插件（如MCP或GPT集成），请先检查插件的来源和维护者。该技能不会自动安装或执行任何插件。  
- **在测试环境中进行测试** — 先在测试环境中使用临时密钥。测试完成后立即撤销密钥。切勿在多个租户之间共享密钥。  

## AI代理集成

支持Claude Desktop、Claude.ai、Claude Code和OpenAI Custom GPT的25种MCP工具。  
**用户操作说明：** 每个集成都需要用户手动进行设置。该技能不会自动安装任何代码。  
详情请参阅[integrations.md](integrations.md)中的设置指南和安全注意事项。  

## 模块说明  

每个模块都有自己的SKILL.md文件，其中包含详细的端点和curl使用示例：  
- **moltflow**（核心模块）：会话管理、消息传递、群组管理、标签设置、Webhook配置  
- **moltflow-outreach**：批量发送消息、定时发送、定期报告、自定义群组管理  
- **moltflow-ai**：文本风格克隆、情感分析、AI回复  
- **moltflow-leads**：线索检测、CRM工作流程管理、批量操作  
- **moltflow-a2a**：支持代理间的安全通信  
- **moltflow-reviews**：评论收集、情感分析、评价内容导出  
- **moltflow-admin**：代理管理、API密钥管理、费用统计、使用情况跟踪  
- **moltflow-onboarding**：提供业务发展支持、按需账户分析、潜在客户发现功能  

## 其他注意事项：**

- 所有消息都遵循反垃圾邮件规则（包括发送速率限制和随机延迟）  
- 首次连接时需要使用二维码进行配对  
- 使用E.164电话格式（不包含`+`符号）  
- AI功能和A2A功能需要使用Pro级及以上的订阅计划  
- 发送速率限制：免费账户限制为10条/分钟，Starter账户限制为20条/分钟，Pro账户限制为40条/分钟，Business账户限制为60条/分钟  

## 更新日志  

**v2.11.3**（2026-02-15）—— 详细更新日志请参见[CHANGELOG.md](CHANGELOG.md)  

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