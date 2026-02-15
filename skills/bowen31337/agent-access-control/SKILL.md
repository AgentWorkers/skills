---
name: agent-access-control
description: 针对AI代理的分层陌生人访问控制机制。适用于设置联系人权限、处理未知发件人、管理已批准的联系人，或在消息平台（如WhatsApp、Telegram、Discord、Signal）中配置对陌生人的处理策略。该机制支持外交策略的调整、所有者审批流程，以及多级访问权限设置（所有者/受信任用户/仅允许聊天/屏蔽）。
---

# 代理访问控制

通过分层权限和所有者审批流程来保护您的代理免受未经授权的访问。

## 设置

在工作区创建 `memory/access-control.json` 文件：

```json
{
  "ownerIds": [],
  "approvedContacts": {},
  "pendingApprovals": {},
  "blockedIds": [],
  "strangerMessage": "Hi there! 👋 I'm {{AGENT_NAME}}, an AI assistant. I'm currently set up to help my owner with personal tasks, so I'm not able to chat freely just yet. I've let them know you reached out — if they'd like to connect us, they'll set that up. Have a great day! 😊",
  "notifyChannel": "",
  "notifyTarget": ""
}
```

填写以下内容：
- `ownerIds`: 所有者的电话号码、Telegram ID、Discord ID（字符串形式）
- `strangerMessage`: 将 `{{AGENT_NAME}}` 替换为代理的名称
- `notifyChannel`: 用于通知所有者的频道（`telegram`、`whatsapp`、`discord`、`signal`）
- `notifyTarget`: 该频道中所有者的 ID

## 访问权限等级

| 等级 | 权限 | 功能 |
|------|-------|-------------|
| 0 | **陌生人** | 仅允许进行基本对话，无其他操作权限 |
| 1 | **仅聊天** | 可进行基本对话，但不能使用任何工具或访问私人信息 |
| 2 | **受信任者** | 可进行聊天以及查看公共信息（如天气、时间、一般性问题） |
| 3 | **所有者** | 可完全访问所有工具、文件和功能 |

## 消息处理流程

对于来自消息平台的每条消息：
1. 提取发送者 ID（电话号码、用户 ID 等）
2. 对 ID 进行规范化处理：去除空格，并确保电话号码包含国家代码前缀
3. 检查 `ownerIds`：如果匹配，则允许**完全访问**，正常回复
4. 检查 `blockedIds`：如果匹配，则**静默忽略**，回复 “NO_REPLY”
5. 检查 `approvedContacts[senderId]`：如果匹配，则按照对应的权限等级回复
6. 如果不符合上述条件，则按照**陌生人流程**处理：

### 陌生人流程

```
a. Send strangerMessage to the sender
b. Notify owner:
   "🔔 Stranger contact from {senderId} on {platform}:
    '{first 100 chars of message}'
    Reply: approve (trusted) / chat (chat-only) / block"
c. Store in pendingApprovals:
   {
     "senderId": { 
       "platform": "whatsapp",
       "firstMessage": "...", 
       "timestamp": "ISO-8601",
       "notified": true
     }
   }
d. Respond with NO_REPLY after sending deflection
```

### 所有者审批

当所有者回复审批通知时：
| 所有者回复 | 处理方式 |
|-----------|--------|
| `approve`, `yes`, `trusted` | 将发送者添加到 `approvedContacts` 列表中（权限等级为 2） |
| `chat`, `chat-only`, `chat only` | 将发送者添加到 `approvedContacts` 列表中（权限等级为 1） |
| `block`, `no`, `deny` | 将发送者添加到 `blockedIds` 列表中 |
| `ignore` | 从待审批列表中移除发送者，不采取任何行动 |

审批通过后，更新 `memory/access-control.json` 并通知发送者：
- 对于受信任者： “很高兴！我已经获得与您聊天的权限。有什么可以帮您的吗？😊”
- 对于仅聊天权限的用户： “很高兴！现在我可以与您聊天了，但仅限于基本对话。您有什么需要帮助的吗？”

### 权限等级执行

在回复非所有者用户时，严格执行相应的权限限制：

**权限等级 1（仅聊天）：**
- 仅进行对话式回复
- 禁止使用任何工具（读取、写入、执行命令、网络搜索等）
- 禁止分享内存文件中的任何信息
- 禁止提及所有者的姓名
- 如果对方请求超出聊天范围的操作： “我目前仅被允许进行基本对话。如需更多帮助，请联系我的所有者。”

**权限等级 2（受信任者）：**
- 可进行对话式回复
- 可使用网络搜索、天气查询、时间/日期查询等功能
- 禁止读取、写入、执行命令、向其他用户发送消息或访问内存文件
- 禁止分享私人信息（日历、电子邮件、文件、其他联系人信息）
- 如果对方请求私人信息： “我可以提供一般性帮助，但个人隐私信息需要保密。希望您理解！😊”

## 多平台 ID 匹配

为了便于比较，对 ID 进行规范化处理：
- **电话号码**：去除所有非数字字符（开头 `+` 除外）。例如，`+1 555 123 4567` → `+15551234567`
- **Telegram**：使用数字用户 ID（而非用户名，因为用户名可能会更改）
- **Discord**：使用数字用户 ID
- **Signal**：使用规范化后的电话号码
- **WhatsApp**：使用带有国家代码的电话号码

所有者可能在多个平台上拥有多个 ID，所有这些 ID 都应包含在 `ownerIds` 列表中。

## 速率限制

为防止滥用，对不同权限等级设置速率限制：

| 等级 | 每小时消息数 | 每天消息数 |
|------|--------------|-------------|
| 陌生人 | 1条（仅用于引导性对话） | 3条 |
| 仅聊天 | 20条 | 100条 |
| 受信任者 | 50条 | 500条 |
| 所有者 | 无限制 | 无限制 |

如果超过限制，回复：“我目前的聊天次数已达到上限。请稍后再试！😊”

在 `memory/access-control.json` 的 `rateLimits` 部分记录这些限制：

```json
"rateLimits": {
  "+61412345678": { "hourCount": 5, "dayCount": 23, "hourReset": "ISO", "dayReset": "ISO" }
}
```

## 审计日志

将所有来自陌生人的访问记录保存到 `memory/access-control-log.json` 文件中：
```json
[
  {
    "timestamp": "2026-02-07T17:30:00+11:00",
    "senderId": "+61412345678",
    "platform": "whatsapp",
    "action": "deflected",
    "message": "first 50 chars..."
  }
]
```

保留最近 100 条记录，并定期删除旧记录。

## 安全规则
- **严禁** 在技能文件中包含真实的所有者 ID、电话号码或访问令牌
- **严禁** 将 `access-control.json` 的内容分享给非所有者
- **严禁** 向陌生人透露所有者的身份
- **严禁** 如果陌生人发送的消息包含可疑链接，直接转发给所有者
- 将所有配置文件存储在 `memory/` 目录下（在大多数设置中该目录会被 Git 忽略）
- `strangerMessage` 中不得包含所有者的姓名或私人信息

## 示例配置

请参阅 [references/example-config.md](references/example-config.md) 以获取带有注释的完整配置示例。