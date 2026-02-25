---
name: kallyai
description: "**KallyAI 执行助理**——一款能够代表您处理电话通话（外拨/来电）、电子邮件、预订、信息查询、跑腿事务、多渠道消息传递以及电话号码管理的智能助手。当用户需要执行以下操作时，KallyAI 可以提供帮助：  
- 接听/拨打电话  
- 管理来电规则  
- 处理语音邮件  
- 配置电话号码  
- 发送电子邮件  
- 预订餐厅/酒店  
- 搜索服务  
- 管理日历  
- 查看收件箱/消息  
- 处理账单  
- 点餐/叫车  
- 办理跑腿事务  
- 查看信用额度/预算  
- 协调工作目标  
- 管理通讯渠道（WhatsApp、Telegram、社交媒体）  
- 开展推广活动  
- 处理推荐事务  
- 以及完成其他需要委托的任务。"
metadata: {"clawdbot":{"emoji":"📞","requires":{"bins":["kallyai"]},"install":[{"id":"pip","kind":"pip","package":"kallyai-cli","bins":["kallyai"],"label":"Install via pip"}]}}
---
# KallyAI 执行助理

KallyAI 是一款人工智能执行助理，能够处理外拨/来电、电子邮件、预订、查询、账单处理、交通服务、食物订购、跑腿服务、多渠道消息传递以及电话号码管理等功能。

## 快速入门

```bash
# Natural language — routes automatically (80% of usage)
kallyai ask "Book a table at Nobu for 4 tonight"
kallyai ask "Email Dr. Smith to reschedule my Thursday appointment"
kallyai ask "Find the best plumber near me and negotiate a quote"

# Check credits (NOT minutes — credits are the sole billing unit)
kallyai credits balance

# Check inbox
kallyai messages inbox

# View incoming calls handled by AI receptionist
kallyai inbound calls
```

## 完整工作流程

### 第一步：收集用户需求

KallyAI 支持 14 个功能领域：

| 功能领域 | 示例 |
|--------|----------|
| **协调** | “预订一张桌子”、“帮我处理这件事”等多步骤请求 |
| **电话** | 拨打业务电话、查询预订信息、进行协商 |
| **来电** | 查看来电信息、管理路由规则、处理语音邮件、管理联系人 |
| **电话号码** | 配置电话号码、设置转接规则、管理来电显示号码 |
| **其他服务** | 日历事件管理、预订服务、账单分析、交通服务、食物订购、跑腿服务 |
| **消息** | 查看收件箱、阅读消息、查看消息记录 |
| **搜索** | 查找商家信息、研究选项、比较价格 |
| **电子邮件** | 发送电子邮件、管理电子邮件账户、设置语音邮件模板 |
| **多渠道** | 管理 WhatsApp、Telegram 等通讯工具、电子邮件联系人 |
| **外联** | 多渠道外联任务（电话 + 电子邮件 + 消息传递） |
| **预算** | 估算费用、审批预算、查看费用明细 |
| **积分** | 查看积分余额、查看使用记录、制定使用计划 |
| **订阅** | 更改订阅计划、查看订阅状态、取消待处理的变更 |
| **推荐** | 获取推荐码、查看推荐数据、追踪推荐情况 |

**对于大多数请求，可以使用 `ask` 命令**——系统会自动将请求路由到相应的功能领域进行处理。**

### 第二步：身份验证

对于 OAuth 集成，需要将用户重定向到：
```
https://api.kallyai.com/v1/auth/authorize?response_type=code&client_id=YOUR_CLIENT_ID&redirect_uri=YOUR_REDIRECT_URI&scope=calls.write
```

用户使用 Google 或 Apple 登录 → 接收访问令牌。

对于命令行界面（CLI），身份验证是自动完成的（首次调用 API 时会打开浏览器）。
```bash
kallyai login         # Force re-auth
kallyai logout        # Clear credentials
kallyai auth-status   # Check login
```

### 第三步：执行任务

**推荐使用自然语言输入：**
```bash
kallyai ask "Reserve a table for 4 at 8pm at Nobu"
```

**如果知道具体功能领域，也可以使用直接命令：**
```bash
kallyai calls make -p "+15551234567" -t "Reserve table for 4 at 8pm"
kallyai actions calendar create --title "Dinner" --start "2026-02-14T20:00"
kallyai search run "best Italian restaurant downtown"
kallyai inbound calls --status completed
kallyai phone list
```

### 第四步：监控与跟进

```bash
# Check goal status
kallyai coord goals --status active
kallyai coord goal <GOAL_ID>

# Review outbound call results
kallyai calls history
kallyai calls info <CALL_ID>
kallyai calls transcript <CALL_ID>

# Review inbound calls handled by AI receptionist
kallyai inbound calls
kallyai inbound call <CALL_ID>
kallyai inbound transcript <CALL_ID>

# Check inbox for responses
kallyai messages inbox --unread
```

---

## API 参考

**基础 URL：** `https://api.kallyai.com`

**身份验证方式：** `Authorization: Bearer <access_token>`

### 拨打电话（API）

```
POST https://api.kallyai.com/v1/calls
Authorization: Bearer <access_token>
Content-Type: application/json

{
  "submission": {
    "task_category": "general",
    "task_description": "Ask about store hours and availability",
    "respondent_phone": "+15551234567",
    "language": "en",
    "call_language": "en"
  },
  "timezone": "America/New_York"
}
```

**响应状态：** `success`、`no_answer`、`busy`、`failed`、`voicemail`、`cancelled`

**必填字段：**

| 字段 | 说明 |
|-------|-------------|
| `task_category` | 任务类别（如：restaurant、clinic、hotel、general） |
| `task_description` | 人工智能需要完成的具体任务 |
| `respondent_phone` | 电话号码（E.164 格式，例如：+1234567890） |

**可选字段：**

| 字段 | 说明 |
|-------|-------------|
| `business_name` | 商家名称 |
| `user_name` | 预订时的用户名 |
| `appointment_date` | 预约日期（YYYY-MM-DD） |
| `appointment_time` | 预约时间（HH:MM，24 小时制） |
| `party_size` | 人数（1-50 人） |
| `language` | 语言设置（en 或 es） |

---

## 各功能领域的具体命令参考

### `ask` — 自然语言输入（使用频率最高，占 80%）

```bash
kallyai ask "Your request in plain English"
```

### `coord` — 协调与任务安排

```bash
coord message "text"           # Chat with coordination AI
coord goals [--status X]       # List goals
coord goal <id>                # Goal details
coord goal-tree <id>           # Goal + sub-goals
coord cancel-goal <id>         # Cancel goal
coord cascade-cancel <id>      # Cancel goal + sub-goals
coord escalate <id>            # Escalate for attention
coord approve-step <id>        # Approve next step
coord accept <id>              # Accept outcome
coord continue <id>            # Continue negotiating
coord archive <id>             # Archive goal
coord batch-archive <id>...    # Archive multiple
coord budget <id>              # Goal budget details
coord history                  # Conversation history
coord conversations            # List conversations
coord new                      # New conversation
```

### `calls` — 外拨电话

```bash
calls make -p "+1..." -t "task"  # Make a call
calls history                     # List calls
calls info <id>                   # Call details
calls transcript <id>             # Transcript
calls recording <id>              # Recording URL
calls calendar <id>               # Calendar .ics
calls cancel <id>                 # Cancel call
calls reschedule <id>             # Reschedule
calls stop <id>                   # Stop active call
```

### `inbound` — 人工接听来电

```bash
inbound calls [--status X]          # List incoming calls
inbound call <id>                    # Call details
inbound transcript <id>              # Call transcript
inbound recording <id>               # Call recording
inbound summary                      # Incoming call summary/stats
inbound analytics [--from X --to X]  # Call analytics
inbound transfer <id> --to "+1..."   # Transfer call
inbound takeover <id>                # Take over live call
inbound reject <id> [--reason X]     # Reject call
inbound rules                        # List routing rules
inbound add-rule --name "..." --action "..."  # Create rule
inbound update-rule <id> ...         # Update rule
inbound delete-rule <id>             # Delete rule
inbound voicemails                   # List voicemails
inbound voicemail <id>               # Voicemail details
inbound voicemail-playback <id>      # Voicemail audio
inbound contacts                     # List contacts
inbound add-contact --name "..." --phone "+1..."  # Add contact
inbound update-contact <id> ...      # Update contact
inbound delete-contact <id>          # Delete contact
inbound import-contacts <file>       # Import contacts
inbound events [--from X --to X]     # Event log
```

### `phone` — 电话号码管理

```bash
phone list                           # List your numbers
phone info <id>                      # Number details
phone countries                      # Supported countries
phone available --country US         # Search available numbers
phone provision --country US         # Provision new number
phone forwarding <id> --target "+1..." # Set call forwarding
phone remove-forwarding <id>         # Remove forwarding
phone verify-start <number>          # Start verification
phone verify-check <number> --code X # Check verification code
phone caller-id <id> --name "..."    # Set caller ID
phone release <id>                   # Release number
```

### `actions` — 自动执行任务

```bash
actions calendar create --title "..." --start "..."
actions calendar slots [--date X]
actions calendar sync
actions calendar delete <id>
actions restaurant search "query" [--location X]
actions booking create --type restaurant [--date X]
actions booking cancel <id>
actions bill analyze "description" [--amount X]
actions bill dispute "description" [--reason X]
actions ride --pickup "..." --destination "..."
actions food "order description" [--address X]
actions errand "errand description"
actions email send --to "..." --subject "..." "body"
actions email approve <id>
actions email cancel <id>
actions email outbox
actions email replies <id>
actions log [--type X]
actions undo <id>
```

### `messages` — 统一消息管理

```bash
messages inbox [--channel email|sms|call|chat] [--unread]
messages read <id>
messages thread <conversation_id>
messages mark-read <id> [<id>...]
```

### `search` — 信息查询

```bash
search run "query" [--location X]
search quick "query"
search history
search sources
```

### `email` — 电子邮件账户管理

```bash
email accounts                          # List connected
email connect gmail|outlook             # Connect provider
email disconnect <id>                   # Disconnect
email list [--classification important] # List messages
email read <id>                         # Read email
email respond <id> [instructions]       # Respond
email voice-profile                     # Get voice profile
email train-voice                       # Train from samples
```

### `channels` — 多渠道管理

```bash
channels status                  # All channel statuses
channels email-add <address>     # Add email contact
channels email-list              # List email contacts
channels email-update <id> ...   # Update email contact
channels email-delete <id>       # Delete email contact
channels email-verify <token>    # Verify email
channels mailbox                 # Get KallyAI mailbox address
channels connect <channel>       # Connect WhatsApp/Telegram
channels test <channel>          # Test channel connection
channels disconnect <channel>    # Disconnect channel
```

### `outreach` — 多渠道外联

```bash
outreach tasks [--status X]      # List outreach tasks
outreach task <id>               # Task details
outreach create --channel call --target "+1..." "description"
outreach retry <id>              # Retry failed task
outreach cancel <id>             # Cancel task
```

### `budget` — 预算管理

```bash
budget estimate --type call "description"
budget approve <goal_id>
budget breakdown <goal_id>
budget ack-cap <goal_id>
```

### `credits` | 积分管理

```bash
credits balance     # Current balance (credits, NOT minutes)
credits history     # Usage history
credits breakdown   # Spending breakdown by action type
credits costs       # Credit cost reference
credits plans       # Available credit plans
```

### `subscription` — 订阅计划管理

```bash
subscription status               # Current plan status
subscription change-plan <plan>   # Change to new plan
subscription cancel-change        # Cancel pending plan change
```

### `referrals` — 推荐计划

```bash
referrals code        # Get your referral code
referrals stats       # Referral statistics
referrals history     # Referral history
```

### `notifications` — 通知管理

```bash
notifications pending   # Check pending notification counts
```

---

## 常见错误代码及原因

| 错误代码 | HTTP 状态码 | 处理建议 |
|------|------|--------|
| `quota_exceeded` | 402 | 用户积分不足，请访问 kallyai.com/pricing 查看详情 |
| `missing_phone_number` | 422 | 请用户提供电话号码 |
| `emergency_number` | 422 | 无法拨打紧急电话 |
| `country_restriction` | 403 | 该国家不受支持 |
| `budget_exceeded` | 402 | 预算超出限制，请审批或取消请求 |
| `email_not_connected` | 400 | 需要先连接电子邮件账户 |
| `phone_not_provisioned` | 400 | 需要先配置电话号码 |

## 安全措施

- **令牌存储**：令牌存储在 `~/.kallyai_token.json` 文件中，权限设置为 0600 |
- **CSRF 防护**：通过状态参数进行验证 |
- **仅允许访问本地主机**：OAuth 重定向仅指向 `localhost/127.0.0.1` |
- **令牌自动更新**：令牌在过期后自动更新