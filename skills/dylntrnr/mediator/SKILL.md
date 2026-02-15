---
name: mediator
description: 拦截并过滤来自“难缠联系人”的通信内容。去除其中的情感色彩，提取关键事实，并生成中立的回复。适用于为特定联系人设置通信过滤规则、配置调解器（mediator），或处理被拦截的消息。该功能会在触发“mediator”、“intercept messages”、“filter communications”、“difficult contact”等事件时启动，也可用于处理用户不想直接处理的消息请求。
---

# Mediator 技能

在复杂的人际关系中，它充当情感的“防火墙”。它会拦截来自已配置联系人的信息，去除其中的情感内容，仅呈现事实，并帮助用户起草恰当的回复。

## 快速入门

```bash
# Initialize config (creates mediator.yaml if missing)
~/clawd/skills/mediator/scripts/mediator.sh init

# Add a contact to mediate
~/clawd/skills/mediator/scripts/mediator.sh add "Ex Partner" \
  --email "ex@email.com" \
  --phone "+15551234567" \
  --channels email,imessage

# Process incoming (usually called by cron/heartbeat)
~/clawd/skills/mediator/scripts/mediator.sh check

# List configured contacts
~/clawd/skills/mediator/scripts/mediator.sh list

# Remove a contact
~/clawd/skills/mediator/scripts/mediator.sh remove "Ex Partner"
```

## 配置

配置文件位于 `~/.clawdbot/mediator.yaml`：

```yaml
mediator:
  # Global settings
  archive_originals: true      # Archive raw messages after processing
  notify_channel: telegram     # Where to send summaries (telegram|slack|imessage)
  
  contacts:
    - name: "Ex Partner"
      email: "ex@email.com"
      phone: "+15551234567"
      channels: [email, imessage]
      mode: intercept          # intercept | assist
      summarize: facts-only    # facts-only | neutral | full
      respond: draft           # draft | auto (dangerous)
      
    - name: "Difficult Client"  
      email: "client@company.com"
      channels: [email]
      mode: assist             # Don't hide originals, just help respond
      summarize: neutral
      respond: draft
```

### 模式

- **intercept**：存档/隐藏原始信息，仅显示摘要。用户永远不会看到原始的情感内容。
- **assist**：显示原始信息，并提供回复建议。

### 摘要选项

- **facts-only**：仅提取可操作的信息、请求和截止日期，不包含情感内容。
- **neutral**：用中立的语气重写信息，保留所有内容。
- **full**：显示所有内容，但会标记出情感性或具有操控性的语言。

### 回复选项

- **draft**：生成建议的回复，在发送前等待用户批准。
- **auto**：自动回复（请谨慎使用）。

## 工作原理

### 邮件处理流程

1. 收到 Gmail 的 Pub/Sub 通知（实时）
2. 检查发送者是否与已配置的联系人匹配
3. 如果匹配：
   - 获取完整的邮件内容
   - 通过大型语言模型（LLM）提取事实并去除情感内容
   - 存档原始邮件（添加 “Mediator/Raw” 标签，并标记为已读）
   - 将摘要发送到指定的通知渠道
   - 如果需要回复，则起草回复

### iMessage 处理流程

1. `imsg watch` 监控新消息
2. 检查发送者是否与已配置的联系人匹配
3. 如果匹配：
   - 处理消息内容
   - 将摘要发送到通知渠道
   - 如果需要回复，则起草回复

## 脚本

- `mediator.sh`：主要的命令行接口（CLI）包装器
- `process-email.py`：邮件处理逻辑
- `process-imessage.py`：iMessage 处理逻辑
- `summarize.py`：基于大型语言模型（LLM）的内容分析和摘要生成

## 集成

### 心跳检查

请将以下代码添加到 `HEARTBEAT.md` 文件中：
```
## Mediator Check
~/clawd/skills/mediator/scripts/mediator.sh check
```

### 定时检查（更频繁的监控）

```bash
# Check every 5 minutes during business hours
*/5 9-18 * * 1-5 ~/clawd/skills/mediator/scripts/mediator.sh check
```

## 安全注意事项

- **切勿自动回复** 法律、财务或与儿童相关的问题
- 原始邮件会被存档，但不会被删除（可恢复）
- 所有操作都会记录在 `~/.clawdbot/logs/mediator.log` 中
- 如果摘要遗漏了重要信息，请审查并调整提示语

## 示例输出

**原始邮件：**
> 我简直不敢相信你竟然会再次这样对我。我为你付出了这么多！！！你从来只考虑自己。我需要你在周六下午 3 点去接孩子，如果你连这点都做不到，那我真不知道该说什么好了。

**Mediator 摘要：**
> **发件人：** 前任伴侣
> **渠道：** 邮件
> **需要执行的操作：** 是
> 
> **请求：** 在周六下午 3 点去接孩子
> 
> **建议的回复：**
> “已确认。我会在周六下午 3 点去接孩子。”

---

有关处理过程中使用的 LLM 提示语，请参阅 `references/prompts.md` 文件。