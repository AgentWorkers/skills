---
name: smart-linkedin-inbox
description: 由 Linxa 提供支持的 LinkedIn 收件箱管理器和对话助手。每当用户提到 LinkedIn 消息、LinkedIn 收件箱、LinkedIn 对话、LinkedIn 私信，或者想要阅读、搜索、过滤或管理他们的 LinkedIn 消息时，都可以使用此技能。在用户询问“谁在 LinkedIn 上给我发了消息？”、“显示我的 LinkedIn 收件箱？”、“查找与招聘相关的对话”、“列出潜在客户信息”、“我在 LinkedIn 上的下一步行动是什么？”、“将对话标记为已读”，或者询问 LinkedIn 消息的情感分析、标签、意图或潜在客户管理相关内容时，此技能会自动触发。该技能支持以下功能：使用丰富的过滤条件（标签、情感分析、意图方向、产品兴趣）来列出和搜索对话；获取完整的消息记录；为潜在客户生成下一步行动的摘要；向联系人添加类似 CRM 的评论；以及将对话标记为已读。此外，当用户提到 Linxa 时，此技能也会自动触发。在任何与 LinkedIn 消息或潜在客户管理相关的任务中，都请使用此技能。
---
# LinkedIn收件箱管理器 — 来自Linxa的智能LinkedIn收件箱工具

这款工具利用人工智能技术，帮助您管理LinkedIn收件箱：搜索对话、按情感和意图筛选信息、追踪潜在客户，并采取相应行动——所有这些功能都不需要您分享LinkedIn密码。完全免费，无需任何付费计划。

## 功能介绍

- **搜索与筛选对话**：可通过关键词、标签、情感（正面/负面/中性）、意图方向（发给你/来自你）或产品兴趣进行筛选。
- **阅读完整消息记录**：按时间顺序查看所有对话内容。
- **获取下一步行动建议**：AI会根据每个潜在客户的情况生成下一步操作的建议。
- **为潜在客户添加备注**：可以为LinkedIn联系人添加类似CRM系统的备注，以影响后续的操作建议。
- **标记对话为已读**：保持收件箱的整洁有序。
- **智能标签分类**：包括“紧急”、“需要跟进”、“投资者”、“客户”、“招聘”、“合作伙伴关系”等。
- **安全访问**：采用基于令牌的认证方式，无需提供LinkedIn密码或浏览器cookie。
- **完全免费**：所有功能均包含在内，无任何付费层级。

## 使用示例

您可以尝试使用以下命令与AI工具进行交互：

```
Who messaged me on LinkedIn this week?
Show my hot conversations with positive sentiment
Find all messages about hiring
List investors who reached out to me
What are my next actions on LinkedIn?
Show the full thread with [person name]
Add a note to John: "Follow up after demo on Friday"
Mark my conversation with Sarah as read
List conversations labeled "Need Follow Up" with intent direction to_me
Search LinkedIn messages for "partnership proposal"
```

## 快速入门（3分钟）

1. 安装[Linxa Chrome扩展程序](https://chromewebstore.google.com/detail/ai-smart-inbox-for-linked/ggkdnjblijkchfmgapnbhbhnphacmabm)。
2. 使用LinkedIn在[app.uselinxa.com](https://app.uselinxa.com/)登录。
3. 从[MCP设置](https://app.uselinxa.com/setup-mcp)中复制您的令牌，并进行设置：

```bash
export LINXA_TOKEN=YOUR_TOKEN
```

## 安装技能

```bash
clawhub install smart-linkedin-inbox
```

## 认证要求

所有请求都需要`LINXA_TOKEN`环境变量。这是一个安全的令牌，Linxa绝不会要求您提供LinkedIn密码或会话cookie。

```
Authorization: Bearer $LINXA_TOKEN
```

如果令牌丢失或过期，请引导用户在[app.uselinxa.com/setup-mcp](https://app.uselinxa.com/setup-mcp)重新生成令牌。

**安全机制：**
- 绝不共享LinkedIn密码。
- 防止浏览器cookie被窃取或会话被劫持。
- 访问需用户明确同意。
- 所有数据仅存储在Linxa服务器和您的工具之间。
- 可随时通过Linxa控制面板撤销访问权限。

## API基础URL

```
https://app.uselinxa.com
```

## 可用接口

### 1. 验证当前用户

```
GET /api/mcp/current-li-user
```

用于验证用户身份并返回当前LinkedIn个人资料。在会话开始时首先调用此接口。

### 2. 列出并搜索对话

```
GET /api/mcp/conversations
```

**查询参数（均为可选）：**

| 参数 | 类型 | 默认值 | 说明 |
|---------|------|---------|-------------|
| `limit` | 整数 | 50 | 返回的最大对话数量 |
| `search` | 字符串 | — | 按关键词在消息和参与者中搜索 |
| `label` | 字符串 | — | 按类别标签筛选 |
| `sentiment` | 字符串 | — | `POSITIVE`（正面）、`NEGATIVE`（负面）或`NEUTRAL`（中性） |
| `primary_intent` | 字符串 | — | 按意图筛选（例如：“销售”、“招聘”） |
| `intent_direction` | 字符串 | — | `to_me`（发给你）或`from_me`（来自你） |
| `product` | 字符串 | — | 按检测到的产品兴趣筛选 |

**可用标签：**紧急、需要跟进、个人联系人、投资者、客户、招聘、垃圾信息、合作伙伴关系、已归档、已安排、未联系

### 3. 获取特定对话的详细信息

```
GET /api/mcp/messages/{chatId}
```

返回特定对话中的所有消息。`chatId`来自对话列表的响应结果；如果`chatId`包含特殊字符，请对其进行URL编码。

### 4. 生成收件箱摘要及下一步行动建议

```
POST /api/mcp/next-actions
```

根据用户的LinkedIn对话内容，生成AI生成的下一步行动建议。当用户询问“我接下来应该做什么？”或“我在LinkedIn上的优先事项是什么？”时，可以使用此接口。

### 5. 为潜在客户添加备注

```
POST /api/mcp/comments
```

为LinkedIn潜在客户的个人资料添加类似CRM系统的备注。这些备注会影响后续的操作建议。请求体格式如下：

```json
{
  "profileId": "PROFILE_ID",
  "text": "Follow up after demo on Friday"
}
```

### 6. 将对话标记为已读

```
POST /api/mcp/conversations/{chatId}/read
```

将特定对话标记为已读。当用户要求“将此对话标记为已读”或希望清理收件箱时使用此功能。

## 请求方式

可以使用辅助脚本进行认证后的请求：

```bash
bash scripts/linxa_api.sh GET /api/mcp/current-li-user
bash scripts/linxa_api.sh GET "/api/mcp/conversations?label=Hot&limit=5"
bash scripts/linxa_api.sh GET "/api/mcp/messages/CHAT_ID_HERE"
bash scripts/linxa_api.sh POST /api/mcp/next-actions
bash scripts/linxa_api.sh POST /api/mcp/comments '{"profileId":"PROFILE_ID","text":"Note here"}'
bash scripts/linxa_api.sh POST "/api/mcp/conversations/CHAT_ID/read"
```

或者直接使用curl进行请求：

```bash
curl -sL \
  -H "Authorization: Bearer $LINXA_TOKEN" \
  "https://app.uselinxa.com/api/mcp/conversations?limit=10&sentiment=POSITIVE"
```

## 工作流程

1. **验证身份**：调用 `/api/mcp/current-li-user` 确认令牌有效。
2. **列出或搜索对话**：使用筛选条件缩小搜索范围。
3. **获取特定对话的详细信息**：从步骤2中获取`chatId`并获取完整消息。
4. **采取行动**：添加备注、标记为已读或查看下一步行动建议。
5. **清晰展示结果**：汇总对话内容，突出关键信息，并按时间顺序展示消息。

## 结果展示格式

向用户展示对话时：
- 显示参与者姓名、最后一条消息的预览以及任何标签或情感标签。
- 对于消息记录，按时间顺序显示消息内容，包括发送者姓名和时间戳。
- 除非用户要求查看完整内容，否则仅显示简短摘要。
- 突出显示未读或高优先级的条目。
- 将下一步行动建议以优先级列表的形式呈现。

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| 401未经授权 | 令牌丢失或过期 — 请在[Linxa控制面板](https://app.uselinxa.com/setup-mcp)重新生成令牌。 |
| 结果为空 | Chrome扩展程序可能未同步 — 请检查扩展程序是否处于活动状态以及LinkedIn标签页是否已打开。 |
| `chatId`编码错误 | 在发送请求前请对`chatId`进行URL编码。 |
| 未找到对话 | 确保您有LinkedIn对话记录，并且扩展程序最近已同步数据。

## 完整API参考

有关完整的OpenAPI规范，请参阅`references/openapi.yaml`。