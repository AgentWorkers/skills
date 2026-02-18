---
name: "WhatsApp All-in-One CRM — ERC-8004 Agent | Campaign Analytics, Bulk Send, AI Outreach, Lead Detection, Support & MCP Server"
version: "2.12.2"
description: "这是您所需的唯一一款 WhatsApp 技能插件。该插件提供了详细的文档和 API 参考资料，但没有任何功能会自动安装或自动执行；所有操作都需要用户明确发起。插件支持发送消息、收集潜在客户信息、运行营销活动、安排报告生成、跟踪营销活动效果以及管理客户信息等功能。业务开发人员可通过分析账户元数据来发现业务增长的机会。此外，还支持通过单独的设置来使用 MCP 服务器和自定义 GPT 功能（详情请参见 integrations.md）。该插件提供了超过 90 个 API 端点，支持批量发送消息、定时发送消息、通过 WhatsApp 发送报告、生成具有自定义风格的 AI 回复、群组监控、潜在客户评分、收集用户反馈、跟踪营销活动效果与用户参与度、遵守 GDPR 法规，以及实现代理之间的通信协议。"
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
> 看看它的效果。它会找到未回复的联系人，
> 检测群组对话中的购买信号，
> 发现您未监控的高价值群组，并生成
> 定向的潜在客户列表。所有分析都在您请求时按需运行——不会在后台自动执行任何操作。

> **MCP服务器 + 自定义GPT动作**：可与Claude Desktop、Claude.ai（远程MCP）、Claude Code（插件）和ChatGPT（自定义GPT动作）配合使用。共有25种工具。请参阅[integrations.md](integrations.md)以获取设置指南。

> ***由于需求量大以及最近的注册问题，我们正在限时提供顶级商业计划，每月只需19.90美元即可享受无限配额。** [**立即购买**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)

> 提供免费试用版。[立即注册](https://molt.waiflow.app/checkout?plan=free)

---

## 只需告诉Claude

安装该技能，设置您的API密钥，然后开始使用：

**“分析我的WhatsApp账户以寻找增长机会”**

查找未回复的联系人、未监控的群组以及需要跟进的潜在客户。可通过API按需运行。

**“找到我尚未跟进的潜在客户”**

查找7天以上未收到回复的联系人，并提供重新联系的建议。

**“为我的房地产群组设置关键词监控”**

添加关键词触发器，将购买信号纳入您的处理流程。

**“从我的支持聊天中收集客户反馈”**

进行情感分析，自动批准正面评论，并导出为HTML格式。

**“每周一上午9点向我的VIP客户列表发送促销信息”**

支持时区设置，具有防封禁机制的发送延迟功能，并可追踪发送情况。

**“在我开会时自动回复我的WhatsApp消息”**

AI回复会匹配您的写作风格。

---

## 代码示例

### 获取活动分析数据——发送率、渠道、时间安排

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/campaigns/{job_id}"
```

返回发送率、失败原因、每分钟的消息数量，
以及每个联系人的完整发送状态。

### 实时跟踪发送情况（SSE）

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/bulk-send/{id}/progress"
```

服务器发送的事件流：已发送/失败/待处理的消息数量
会在每条消息发送时实时更新。

### 按互动得分排序的顶级联系人

```bash
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/analytics/contacts?sort=engagement_score&limit=50"
```

根据发送的消息数量、收到的消息数量、回复率以及最近活跃程度进行排序——立即找到最活跃的联系人。

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
（或在任何阶段被标记为`已丢失`）。

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

### 以您的写作风格生成AI回复 + 知识库回复

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

MoltFlow是一个经过验证的链上AI代理，注册在**Ethereum主网**上。

| 字段 | 值 |
|-------|-------|
| 代理ID | [#25477](https://8004agents.ai/ethereum/agent/25477) |
| 链路 | Ethereum主网 (eip155:1) |
| 注册处 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| 信任模型 | 基于声誉的 |
| API端点 | A2A + MCP + Web |

**相关信息：**
- 代理卡片：`https://molt.waiflow.app/.well-known/erc8004-agent.json`
- A2A代理信息：`https://apiv2.waiflow.app/.well-known/agent.json`

---

## 使用场景

**个人创始人/小型企业**
- 在聊天中找到未回复的潜在客户
- 以您的写作风格生成AI回复
- 定时向自定义群组发送促销信息

**代理机构/多客户企业**
- 监控50多个群组
- 批量发送消息并设置防封禁机制
- 将潜在客户信息导出为CSV格式，或推送到n8n/Zapier

**营销机构/活动经理**
- 从点击链接进入WhatsApp的广告活动中捕获潜在客户
- 通过关键词检测和AI评分自动评估潜在客户
- 设置防封禁机制的批量跟进流程
- 在多个客户账户间管理多个会话
- 通过Webhook或CSV将活动潜在客户信息导出到CRM系统

**开发者/AI代理构建者**
- 提供90多个REST API端点及相应的API密钥
- 支持A2A协议和端到端加密
- Python SDK：`pip install moltflow` ([GitHub](https://github.com/moltflow/moltflow-python))

### 教程与指南

**AI集成指南：**
- [将ChatGPT连接到MoltFlow](https://molt.waiflow.app/guides/connect-chatgpt-to-moltflow) — 自定义GPT动作，10分钟设置完成
- [将Claude连接到MoltFlow](https://molt.waiflow.app/guides/connect-claude-to-moltflow) — MCP服务器设置，5分钟完成
- [将OpenClaw连接到MoltFlow](https://molt.waiflow.app/guides/connect-openclaw-to-moltflow) — 原生AI配置，5分钟完成

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
| 消息传递 | 文本、媒体文件、投票、vCard |
| 批量发送 | 具有防封禁机制，支持SSE实时跟踪 |
| 定时发送 | 支持Cron任务，考虑时区设置 |
| 报告 | 提供10种模板，支持Cron任务和WhatsApp发送 |
| 分析 | 活动渠道分析、联系人评分、发送时间优化 |
| 群组管理 | 支持自定义列表和CSV导出 |
| 潜在客户管理 | 检测潜在客户信号，管理处理流程 |
| 监控 | 支持监控50多个群组和关键词 |
| 标签管理 | 数据同步到WhatsApp业务系统 |
| AI回复 | 使用GPT-4/Claude技术生成回复 |
| 文风匹配 | 自动匹配您的写作风格 |
| 情感分析 | 支持PDF/TXT格式，支持语义搜索 |
| 语音转录 | 支持语音转文本功能 |
| 评论管理 | 支持情感分析，自动批准正面评论 |
| 防垃圾邮件 | 设置发送速率限制，模拟真实输入 |
| 安全防护 | 防止个人信息泄露，防止注入恶意代码 |
| Webhook | 支持HMAC签名，支持10多种事件类型 |
| A2A通信 | 支持端到端加密，使用JSON-RPC协议 |
| 遵守GDPR法规 | 自动设置消息有效期，确保合规性 |
| 发送跟踪 | 支持实时SSE跟踪，显示消息状态（已读/已回复/已忽略） |

---

## MoltFlow与其他产品的对比

| | Molt | 替代方案1 | 替代方案2 | 替代方案3 |
|---|:---:|:---:|:---:|:---:|
| 消息传递 | 支持18种消息类型 | 支持14种 | 支持3种 | 支持1种 |
| 群组管理 | 支持8个群组功能 | 支持4个 | 不支持 | 不支持 |
| 外展功能 | 支持7种外展功能 | 不支持 | 不支持 | 不支持 |
| CRM集成 | 支持7种CRM集成 | 不支持 | 不支持 | 不支持 |
| AI功能 | 支持AI相关功能 | 不支持 | 不支持 | 不支持 |
| 评论管理 | 支持评论收集 | 支持8种评论类型 | 不支持 | 不支持 |
| 安全性 | 提供10项高级安全防护措施 | 完全支持 | 部分支持 | 部分支持 |
| 平台综合能力 | 总计支持90多种功能 | 约15种 | 约3种 | 约1种 |

---

## 该技能的功能

**该技能的功能包括：**文档生成、API调用等。**没有任何内容会自动安装或执行。此软件包不包含任何脚本或可执行文件。所有操作都需要用户明确授权。

| 功能类别 | 具体功能 | 是否需要用户授权？ |
|---|---|---|
| API调用 | 仅通过HTTPS连接到`apiv2.waiflow.app` | 不需要（使用您的API密钥） |
| 联系人信息 | 收集联系人姓名、时间戳、发送次数 | 不收集 |
| CRM集成 | 收集潜在客户状态、互动评分 | 不收集 |
| AI相关功能 | 通过API提供统计分析 | 需要用户同意 |
| 本地文件 | 生成`.moltflow.json`文件（仅记录发送次数，不存储个人信息） | 不存储 |
| API密钥 | 作为环境变量存储，不会被记录或共享 | 不存储 |

**该技能绝不会：**
- 自动安装任何软件包或运行代码
- 未经用户明确授权就发送消息
- 向未列入白名单的号码发送消息（除非用户特别设置）
- 规避任何反垃圾邮件或内容安全措施
- 与第三方共享数据
- 将敏感信息存储在文件中（仅通过环境变量存储）

---

## 设置说明

> **提供免费试用版** — 允许1次使用，
> 每月发送50条消息，无需信用卡。

**环境变量设置：**
- `MOLTFLOW_API_KEY`（必填）—— 请从[您的控制面板](https://molt.waiflow.app)创建一个最小权限范围的API密钥。根据您的实际工作流程选择合适的权限范围，并定期更换密钥。
- `MOLTFLOW_API_URL`（可选）—— 默认值为`https://apiv2.waiflow.app`

**身份验证方式：**
在请求头中添加`X-API-Key: $MOLTFLOW_API_KEY`或`Authorization: Bearer $TOKEN`（JWT格式）。

**基础URL：** `https://apiv2.waiflow.app/api/v2`

---

## 安全性注意事项

- **强制使用最小权限范围的API密钥** — 创建密钥时必须指定权限范围。始终使用最小权限范围的密钥（例如，仅允许`messages:send`操作）。对于涉及AI功能的操作，建议使用“ Messaging”或“Read Only”等预设权限范围。
- **使用环境变量存储API密钥** — 将`MOLTFLOW_API_KEY`设置为环境变量，避免在共享配置文件中存储。
- **设置电话号码白名单** — 在租户设置中配置`allowed_numbers`，以限制允许发送消息的号码范围。只有列入白名单的号码才能发送消息。
- **严格的安全防护措施** — 所有 outbound 消息都会经过双向验证（接收方必须先发送消息），并设置发送速率限制、模拟真实输入延迟等机制。这些措施无法被绕过。
- **内容审核** — 发送的每条消息都会经过隐私信息检测、恶意代码检测等安全检查。
- **审核机制** — 在租户设置中启用`require_approval`选项，确保所有AI生成的回复都需要人工审核后再发送。
- **Webhook验证** — API会阻止来自私密IP地址、使用非HTTPS协议的请求。
- **第三方包的安装检查** — 在安装MCP或GPT集成之前，请务必先审查相关包的来源和维护者信息。该技能不会自动安装或执行任何第三方包。
- **运行前的本地检查** — Python示例代码托管在GitHub上，切勿直接使用。请下载代码并检查源代码后再运行。
- **共享环境中的安全注意事项** — 在共享环境中使用权限有限的密钥进行测试。对于管理员操作（如密钥轮换、数据导出等），请使用浏览器控制面板或临时生成的密钥。
- **在沙箱环境中进行测试** — 在测试前请创建临时权限范围的密钥。测试完成后立即删除该密钥，切勿在多个租户之间共享。

## AI代理集成

支持与Claude Desktop、Claude.ai、Claude Code和OpenAI Custom GPT的集成。

**用户操作要求** — 每项集成都需要用户手动进行配置。该技能不会自动安装任何相关代码。

请参阅[integrations.md](integrations.md)以获取详细的设置指南和安全注意事项。

---

## 模块说明

每个模块都有自己的SKILL.md文件，其中包含API端点和curl使用示例：

- **moltflow**（核心模块）：处理会话、消息传递、群组管理、Webhook配置
- **moltflow-outreach**：支持批量发送消息、定时发送、生成报告、管理自定义群组
- **moltflow-ai**：支持风格匹配、情感分析、语音转录、AI回复
- **moltflow-leads**：负责潜在客户检测、管理处理流程、批量操作
- **moltflow-a2a**：支持代理间的安全通信、加密消息传输
- **moltflow-reviews**：收集用户评价、进行情感分析、导出评价结果
- **moltflow-admin**：处理用户授权、管理API密钥、记录使用情况

---

## 其他注意事项

- 所有发送的消息都经过反垃圾邮件检测（包括模拟输入延迟等安全措施）
- 首次连接时需要使用二维码进行配对
- 通信格式必须使用E.164电话号码格式（不包含`+`符号）
- 使用AI功能或A2A功能需要升级到Pro计划及以上版本
- 发送速率限制：免费账户限制为10条/分钟，Starter账户限制为20条/分钟，Pro账户限制为40条/分钟，Business账户限制为60条/分钟

## 更新日志

**v2.11.3**（2026-02-15）——详情请参阅[CHANGELOG.md](CHANGELOG.md)。

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