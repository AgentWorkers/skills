---
name: moltflow-onboarding
description: "**MoltFlow WhatsApp自动化系统的只读账户健康检查及增长机会报告**  
该报告用于获取账户的元数据（如账户数量、时间戳、群组成员信息等），并展示相关分析结果。适用于以下场景：新员工入职培训、系统设置、项目启动、账户增长策略制定、系统优化、情况汇报以及账户审核等。"
source: "MoltFlow Team"
version: "2.15.1"
risk: safe
requiredEnv:
  - MOLTFLOW_API_KEY
primaryEnv: MOLTFLOW_API_KEY
disable-model-invocation: true
---
> **MoltFlow** – 专为团队设计的 WhatsApp Business 自动化工具。支持大规模连接、监控和自动化 WhatsApp 操作。
> **由于需求量大以及近期出现的注册问题，我们特别推出了一项限时优惠：顶级商务计划（包含无限使用量），每月仅需 $19.90（按年计费）。** [**立即抢购**](https://buy.stripe.com/cNifZibX7gpQebJ0nsfnO00)
> 免费试用计划也可使用。[**立即注册**](https://molt.waiflow.app/checkout?plan=free)

# MoltFlow 账户健康状况与增长报告

这是一个只读分析工具，用于获取您的 MoltFlow 账户数据并生成可操作的账户健康报告。该工具中的所有 API 请求均为 `GET` 请求，不会修改任何数据。

## 使用场景

- “帮助我开始使用”或“设置我的账户”
- “在我的聊天记录中寻找潜在客户”或“发现业务机会”
- “我该如何实现增长？”或“提供增长策略建议”
- “优化我的设置”或“我忽略了什么？”
- “运行每日简报”或“获取我的晨间报告”

## 前提条件

1. **MOLTFLOW_API_KEY** – 请从 [MoltFlow 仪表板](https://molt.waiflow.app) 的 “ Sessions > API Keys” 部分生成。
2. 基础 URL：`https://apiv2.waiflow.app/api/v2`

## 所需 API 密钥权限

| 权限范围 | 访问权限 |
|---------|---------|
| `sessions` | `manage` |
| `messages` | `send` |

## 认证

```
X-API-Key: <your_api_key>
```

---

## 第一步：获取账户数据（只读）

从以下只读端点获取数据。所有请求均为通过 `X-API-Key: $MOLTFLOW_API_KEY` 头部进行身份验证的 `GET` 请求。基础 URL：`https://apiv2.waiflow.app/api/v2`。

| 端点          | 数据内容          | 完整文档      |
|-----------------|-----------------|-------------|
| `GET /users/me`     | 账户信息及计划详情    | moltflow-admin SKILL.md |
| `GET /sessions`     | WhatsApp 会话记录    | moltflow SKILL.md     |
| `GET /groups`     | 被监控的群组        | moltflow SKILL.md     |
| `GET /custom-groups`   | 自定义群组        | moltflow-outreach SKILL.md   |
| `GET /webhooks`     | Webhook 配置     | moltflow SKILL.md     |
| `GET /reviews/collectors` | 评论收集器设置    | moltflow-reviews SKILL.md   |
| `GET /tenant/settings` | 租户设置        | moltflow-admin SKILL.md     |
| `GET /scheduled-messages` | 计划发送的消息    | moltflow-outreach SKILL.md     |
| `GET /usage/current` | 使用情况统计    | moltflow-admin SKILL.md     |
| `GET /leads`     | 现有潜在客户      | moltflow-leads SKILL.md     |
| `GET /messages/chats/{session_id}` | 每个会话的聊天记录    | moltflow SKILL.md     |

## 第二步：生成账户健康报告

将获取的数据格式化为状态仪表板：

```
## MoltFlow Account Health

**Plan:** {plan} | **Tenant:** {tenant} | **Messages:** {used}/{limit} this month

| Area                  | Status | Details |
|-----------------------|--------|---------|
| WhatsApp Sessions     | ✅/❌  | {count} sessions, {working} active |
| Group Monitoring      | ✅/❌  | {monitored}/{available} groups |
| Custom Groups         | ✅/❌  | {count} groups ({member_count} contacts) |
| Lead Pipeline         | ✅/❌  | {lead_count} leads ({new_count} new, {contacted} contacted) |
| AI Features           | ✅/❌  | Consent {yes/no}, {profile_count} style profiles |
| Scheduled Messages    | ✅/❌  | {count} active |
| Review Collectors     | ✅/❌  | {count} active |
| Webhooks              | ✅/❌  | {count} configured |
| Conversations         | 📊     | {chat_count} conversations, {total_messages} messages |
```

## 第三步：分析增长机会

利用已获取的数据，识别并展示以下关键信息：

### 3A：聊天分析

对于每个活跃的会话，分析第一步中获取的聊天记录：

- **未回复的联系人** – 发送消息但未得到回复的人（这些潜在客户可能会流失）
- **高活跃度的联系人** – 按消息数量计算最活跃的联系人，但尚未被加入任何自定义群组
- **近期联系人** – 过去 7 天内未收到任何回复
- **未分类的联系人** – 未被归入任何自定义群组

### 3B：未监控的群组

比较可用群组（`GET /groups/available/{session_id}`）与被监控的群组，突出显示成员数量较多的未监控群组。

### 3C：使用情况与计划利用率

根据使用数据，标记以下情况：
- 使用率超过 80% – 接近计划限制
- 使用率低于 20% – 资源未被充分利用

### 3D：未收集的评论

如果未配置评论收集器但仍有活跃的聊天记录，需标记这一缺口。

## 第四步：建议下一步行动

在展示分析结果后，列出用户可以采取的具体行动。每个建议都会指向相应的技能模块——请参阅该模块的 SKILL.md 文件以获取完整的端点文档、请求格式和示例。

| 建议行动 | 对应技能模块       |
|------------|-----------------|
| 为热门潜在客户创建自定义群组 | moltflow-outreach     |
| 开始监控高价值群组     | moltflow（群组监控部分）     |
| 安排跟进消息     | moltflow-outreach（计划发送消息部分） |
| 设置评论收集器     | moltflow-reviews     |
| 配置 AI 功能     | moltflow-admin       |

**所有操作均需用户明确批准。** 该工具仅用于读取数据并展示分析结果，不会创建、修改或删除任何资源。

---

## 重要规则

- **该工具为只读模式** – 仅用于获取和分析数据，不会修改账户状态
- **所有会修改账户状态的操作**（如创建群组、安排消息等）必须通过相应的技能模块执行，并需用户明确批准
- 如果 API 请求失败，会显示错误信息并提供重试或跳过操作的选项
- 所有 API 请求均使用 `MOLTFLOW_API_KEY` 环境变量进行身份验证——切勿硬编码密钥
- 分析聊天记录时，重点关注与业务相关的信息，而非个人对话
- 遵守反垃圾邮件政策：切勿向未主动联系的用户发送消息