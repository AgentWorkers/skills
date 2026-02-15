---
name: "WhatsApp Automation & A2A"
description: "MoltFlow——一个全面的WhatsApp自动化平台：支持会话管理、消息发送与接收、群组功能、标签设置、基于人工智能的自动回复系统、反垃圾邮件规则、内容保护机制、自动反馈收集、用户意图检测、潜在客户管理，以及代理之间的通信协议（JSON-RPC，支持加密）。同时，该平台还提供可配置的政策设置功能。"
metadata: {"openclaw":{"emoji":"📱","homepage":"https://waiflow.app","requires":{"env":["MOLTFLOW_API_KEY"]},"primaryEnv":"MOLTFLOW_API_KEY"}}
---

# WhatsApp自动化与AI交互（A2A）

MoltFlow提供了一个全面的WhatsApp自动化API，支持会话管理、消息发送与接收、群组监控、标签设置、反垃圾邮件规则、内容保护、基于AI的回复生成、用户反馈收集以及代理间的通信等功能。

## 使用场景

当您需要以下功能时，可以使用该服务：
- 连接并管理WhatsApp会话（通过二维码配对）
- 发送文本消息、查看聊天记录
- 监控群组以发现潜在客户或关键词
- 管理联系人标签（与WhatsApp Business同步）
- 配置反垃圾邮件规则（如发送频率限制、重复消息拦截、模式过滤）
- 设置内容保护机制（阻止敏感信息如API密钥和个人身份信息）
- 生成AI回复
- 通过情感分析收集用户反馈（支持14种以上语言）
- 导出用户评价（JSON/HTML格式）
- 发送跨代理的消息（使用A2A协议，基于JSON-RPC 2.0）

## 功能详情

**个人自动化：**
- 在您忙碌时自动回复WhatsApp消息（AI会学习您的回复风格）
- 将群组中的重要信息转发到私信
- 在会议后自动向联系人发送跟进消息
- 从群组对话中收集并整理客户评价

**业务与潜在客户管理：**
- 监控行业群组以捕捉购买意向相关的关键词
- 根据消息内容自动将新客户标记为VIP/热销/冷门客户
- 通过标签将检测到的潜在客户路由到销售团队
- 在所有聊天中收集用户反馈，并自动批准正面评价

**代理间通信（A2A）：**
- 构建支持系统，将复杂问题升级给人工代理
- 确保通信的安全性（使用X25519-AES256GCM加密）
- 实现多代理协作流程：潜在客户检测 → 评估 → 接触 → 跟进

**安全与合规性：**
- 自动阻止包含API密钥、信用卡号码或社会安全号码（SSN）的出站消息
- 设置发送频率限制以防止垃圾邮件
- 创建自定义正则表达式规则以过滤敏感内容
- 在发送前检查消息是否符合公司政策

## 设置与费用

> **免费 tier 提供**：1个会话，每月50条消息，无需信用卡。
> 注册地址：https://molt.waiflow.app/register

**环境变量：**
- `MOLTFLOW_API_KEY`（必填）：来自waiflow.app控制台的API密钥
- `MOLTFLOW_API_URL`（可选）：默认为`https://apiv2.waiflow.app`

**认证方式：**
- 使用`X-API-Key: $MOLTFLOW_API_KEY`头部或`Authorization: Bearer $TOKEN`（登录生成的JWT令牌）

**基础URL：**
`https://apiv2.waiflow.app/api/v2`

---

## API详细信息

### 1. 会话管理
```bash
# List all sessions
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/sessions

# Create new session
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "Main Line"}' \
  https://apiv2.waiflow.app/api/v2/sessions

# Get session details
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/sessions/{session_id}

# Delete session
curl -X DELETE -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/sessions/{session_id}
```

| 端点 | 方法 | 描述 |
| ---------- | -------- | ------------- |
| `/sessions` | GET | 查看所有会话 |
| `/sessions` | POST | 创建新会话 |
| `/sessions/{id}` | GET | 获取会话详情 |
| `/sessions/{id}` | DELETE | 删除会话 |

### 2. 消息发送
```bash
# Send text message
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "uuid", "chat_id": "1234567890@c.us", "message": "Hello!"}' \
  https://apiv2.waiflow.app/api/v2/messages/send

# List chats for a session
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/messages/chats/{session_id}

# Get chat messages
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/messages/chat/{session_id}/{chat_id}
```

| 端点 | 方法 | 描述 |
| ---------- | -------- | ------------- |
| `/messages/send` | POST | 发送文本消息 |
| `/messages/send/poll` | POST | 发送投票问卷 |
| `/messages/send/sticker` | POST | 发送贴纸（WebP URL或base64编码） |
| `/messages/send/gif` | POST | 发送GIF（MP4 URL或base64编码） |
| `/messages/chats/{session_id}` | GET | 查看聊天记录 |
| `/messages/chat/{session_id}/{chat_id}` | GET | 获取特定聊天中的消息 |
| `/messages/{message_id}` | GET | 获取单条消息 |

### 3. 群组管理
```bash
# List monitored groups
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/groups

# List available WhatsApp groups
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/groups/available/{session_id}

# Add group to monitor
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"session_id": "uuid", "wa_group_id": "123456@g.us", "monitor_mode": "first_message"}' \
  https://apiv2.waiflow.app/api/v2/groups

# Update monitoring settings
curl -X PATCH -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"monitor_mode": "keyword", "monitor_keywords": ["looking for", "need help"]}' \
  https://apiv2.waiflow.app/api/v2/groups/{group_id}
```

| 端点 | 方法 | 描述 |
| ---------- | -------- | ------------- |
| `/groups` | GET | 查看所有被监控的群组 |
| `/groups/available/{session_id}` | GET | 查看可使用的WhatsApp群组 |
| `/groups` | POST | 添加群组到监控列表 |
| `/groups/create` | POST | 创建新的WhatsApp群组 |
| `/groups/{id}` | GET | 获取群组详情 |
| `/groups/{id}` | PATCH | 更新群组监控设置 |
| `/groups/{id}` | DELETE | 从监控列表中移除群组 |
| `/groups/{wa_group_id}/participants/add` | POST | 向群组添加成员 |
| `/groups/{wa_group_id}/participants/remove` | POST | 从群组中移除成员 |
| `/groups/{wa_group_id}/admin/promote` | POST | 提升群组管理员权限 |
| `/groups/{wa_group_id}/admin/demote` | 降低群组管理员权限 |

### 4. 标签管理
```bash
# Create label (color must be hex #RRGGBB)
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name": "VIP", "color": "#00FF00"}' \
  https://apiv2.waiflow.app/api/v2/labels

# Sync label to WhatsApp Business
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/labels/{label_id}/sync?session_id={session_id}"

# Import labels from WhatsApp Business
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/labels/sync-from-whatsapp?session_id={session_id}"
```

| 端点 | 方法 | 描述 |
| ---------- | -------- | ------------- |
| `/labels` | GET | 查看所有标签 |
| `/labels` | POST | 创建新标签 |
| `/labels/business-check` | GET | 检查群组的WhatsApp Business状态 |
| `/labels/{id}` | GET / PATCH / DELETE | 获取/更新/删除标签 |
| `/labels/{id}/sync` | POST | 将标签同步到WhatsApp Business |
| `/labels/sync-from-whatsapp` | POST | 从WhatsApp导入标签 |

### 5. 反垃圾邮件规则
```bash
# Get anti-spam settings
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/antispam/settings

# Update anti-spam settings
curl -X PUT -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"enabled": true, "rate_limit": 60, "rate_limit_window": 60, "block_duplicates": true, "auto_block_spammers": true, "max_violations": 5}' \
  https://apiv2.waiflow.app/api/v2/antispam/settings

# Create spam filter rule (actions: block, flag, delay)
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"pattern": "buy now|limited offer", "action": "block", "enabled": true}' \
  https://apiv2.waiflow.app/api/v2/antispam/rules

# Update rule
curl -X PUT -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"pattern": "buy now|limited offer|act fast", "action": "flag", "enabled": true}' \
  https://apiv2.waiflow.app/api/v2/antispam/rules/{rule_id}

# Delete rule
curl -X DELETE -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/antispam/rules/{rule_id}

# Get spam statistics
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/antispam/stats
```

| 端点 | 方法 | 描述 |
| ---------- | -------- | ------------- |
| `/antispam/settings` | GET | 查看反垃圾邮件设置 |
| `/antispam/settings` | PUT | 更新设置（如发送频率限制、重复消息拦截） |
| `/antispam/rules` | POST | 创建新的垃圾邮件过滤规则 |
| `/antispam/rules/{id}` | PUT | 更新规则 |
| `/antispam/rules/{id}` | DELETE | 删除规则 |
| `/antispam/stats` | GET | 垃圾邮件统计信息（被阻止的消息、被标记的消息等）

**规则操作：** `block`（阻止消息）、`flag`（标记待审核）、`delay`（设置延迟）

### 6. 内容保护
```bash
# Get content policy settings
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/a2a-policy/settings

# Update content policy
curl -X PUT -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"block_api_keys": true, "block_credit_cards": true, "block_ssn": true, "block_emails": false, "max_message_length": 4096}' \
  https://apiv2.waiflow.app/api/v2/a2a-policy/settings

# View built-in safeguard patterns (prompt injection, secrets, PII)
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/a2a-policy/safeguards

# Create custom blocking rule
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"pattern": "sk-[a-zA-Z0-9]{48}", "description": "Block OpenAI API keys"}' \
  https://apiv2.waiflow.app/api/v2/a2a-policy/rules

# Toggle rule on/off
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/a2a-policy/rules/{rule_id}/toggle

# Delete custom rule
curl -X DELETE -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/a2a-policy/rules/{rule_id}

# Test content against all policies
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"content": "My API key is sk-abc123"}' \
  https://apiv2.waiflow.app/api/v2/a2a-policy/test

# Get blocking statistics
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/a2a-policy/stats

# Reset policy to defaults
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/a2a-policy/reset
```

| 端点 | 方法 | 描述 |
| ---------- | -------- | ------------- |
| `/a2a-policy/settings` | GET / PUT | 获取/更新内容保护策略 |
| `/a2a-policy/safeguards` | GET | 查看内置的安全策略 |
| `/a2a-policy/rules` | POST | 创建自定义过滤规则 |
| `/a2a-policy/rules/{id}` | DELETE | 删除自定义规则 |
| `/a2a-policy/rules/{id}/toggle` | POST | 开/关规则 |
| `/a2a-policy/test` | POST | 测试消息是否符合策略 |
| `/a2a-policy/stats` | GET | 过滤统计信息 |
| `/a2a-policy/reset` | POST | 重置策略设置 |

### 7. AI风格配置
```bash
# Train style profile from message history
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -d '{"contact_id": "optional-contact-jid"}' \
  https://apiv2.waiflow.app/api/v2/ai/style/train

# Check training status
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/ai/style/status/{task_id}

# Get / list / delete style profiles
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  https://apiv2.waiflow.app/api/v2/ai/style/profiles
```

### 8. AI回复生成
```bash
# Generate AI reply (uses style profile)
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -d '{"contact_id": "jid", "context": "customer question", "apply_style": true}' \
  https://apiv2.waiflow.app/api/v2/ai/ai/generate-reply

# Preview AI reply (no usage tracking)
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/ai/ai/preview?contact_id=jid&context=question&apply_style=true"
```

### AI API参考
```bash
# Generate AI reply (uses style profile)
curl -X POST -H "X-API-Key: $MOLTFLOW_API_KEY" \
  -d '{"contact_id": "jid", "context": "customer question", "apply_style": true}' \
  https://apiv2.waiflow.app/api/v2/ai/ai/generate-reply

# Preview AI reply (no usage tracking)
curl -H "X-API-Key: $MOLTFLOW_API_KEY" \
  "https://apiv2.waiflow.app/api/v2/ai/ai/preview?contact_id=jid&context=question&apply_style=true"
```

### 9. 代理间通信（A2A）
**需使用商业计划。** 支持基于JSON-RPC 2.0的通信协议，采用X25519-AES256GCM加密。

### 其他功能

- **代理启动与加密**：支持代理间的安全通信
- **发现其他代理**：自动识别并连接其他AI代理
- **发送A2A消息**：支持跨代理的消息交换

---

## 与其他服务的比较

MoltFlow不仅仅是一个简单的消息发送工具，而是一个全面的WhatsApp业务自动化平台。以下是与其他类似服务的对比：

| 功能 | MoltFlow | whatsapp-ultimate | wacli | whatsapp-automation |
| -------- | -------- | -------- | -------- |
| 发送文本消息 | 支持 | 支持 | 支持 | 不支持 |
| 发送媒体文件（图片、音频） | 支持 | 支持 | 支持 | 不支持 |
| 发送投票问卷 | 支持 | 支持 | 不支持 | 不支持 |
| 发送贴纸（URL或base64编码） | 支持 | 支持 | 不支持 | 不支持 |
| 发送GIF（MP4或base64编码） | 支持 | 支持 | 不支持 | 不支持 |
| 语音留言 | 支持 | 支持 | 不支持 | 不支持 |
| 生成AI回复 | 支持 | 支持 | 不支持 | 不支持 |
| 编辑消息 | 支持 | 支持 | 不支持 | 不支持 |
| 取消发送消息 | 支持 | 支持 | 不支持 | 不支持 |
| 发送位置信息 | 支持 | 不支持 | 不支持 | 不支持 |
| 发送联系卡片 | 支持 | 不支持 | 不支持 | 不支持 |
| 给消息加星/取消星标 | 支持 | 不支持 | 不支持 | 不支持 |
| 控制消息接收显示 | 支持 | 不支持 | 不支持 | 不支持 |
| 模拟输入（防止被封禁） | 支持 | 不支持 | 不支持 | 不支持 |
| 状态管理 | 支持 | 不支持 | 不支持 | 不支持 |
| 接收消息 | 支持 | 支持 | 支持 | 支持 |
| 双向聊天 | 支持 | 支持 | 支持 | 不支持 |

---

## 注意事项

- 所有消息均遵循WhatsApp的反垃圾邮件规则（包括发送频率限制和内容过滤）
- 发送频率限制：免费账户为每分钟10条消息，高级账户为20条，专业账户为40条，企业账户为60条
- 首次连接时需要使用二维码配对
- AI功能需要高级账户或更高级别的订阅
- A2A功能需要企业账户
- 反垃圾邮件规则支持多种处理方式（阻止、标记或延迟）
- 内容保护机制可阻止敏感信息（API密钥、个人身份信息等）
- AI回复生成过程中会进行输入清洗和意图验证

---

## 文件结构说明
```markdown
# 文件结构说明
--- 
# WhatsApp自动化与AI交互（A2A）
--- 
# 功能概述与技术细节
--- 
# 其他服务对比
--- 
# 注意事项
--- 
# 文件映射（用于指示代码块的开始和结束）
--- 
```