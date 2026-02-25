---
name: kallyai-api
description: "**KallyAI 执行助理** — 一款能够代表您处理电话通话（外拨/来电）、电子邮件、预订、信息查询、跑腿服务以及电话号码管理的人工智能工具。适用于用户需要执行以下任务的情况：拨打电话/接听电话、管理来电规则、处理语音邮件、申请电话号码、发送电子邮件、预订餐厅/酒店、搜索服务、管理日历、查看收件箱/消息、处理账单、订购食物/交通服务、安排跑腿任务、查询信用额度/预算、协调工作目标、管理多种沟通渠道（如 WhatsApp、Telegram、社交媒体）、开展外联活动、处理推荐请求或执行任何其他委托任务。
**触发条件**：  
- 电话呼叫  
- 预订请求  
- 约会安排  
- 电子邮件接收  
- 信息搜索  
- 服务预订  
- 日程安排  
- 任务取消  
- 收件箱通知  
- 消息提醒  
- 信息查询  
- 助手请求  
- 协调工作  
- 目标管理  
- 信用额度查询  
- 预算核对  
- 交通服务预订  
- 跑腿服务请求  
- 账单处理  
- 争议处理  
- 日历管理  
- KallyAI 相关操作  
**主要功能**：  
- 处理电话通话（包括外拨和来电）  
- 管理电子邮件收发  
- 预订餐厅/酒店  
- 提供信息查询服务  
- 安排日程安排  
- 查看和回复消息  
- 处理账单  
- 下单食物或交通服务  
- 安排跑腿任务  
- 查询个人信用额度和预算  
- 协调工作目标  
- 管理多种沟通渠道（WhatsApp、Telegram、社交媒体）  
- 开展外联活动  
- 处理推荐请求  
- 执行其他委托任务"
---
# KallyAI 执行助理

KallyAI 是一款人工智能执行助理，能够处理外拨/内拨电话、电子邮件、预订、查询、账单处理、交通服务预约、食物订单、跑腿服务、多渠道消息传递以及电话号码管理——所有这些功能都可以在终端上完成。

## 快速入门

```bash
# The 80% command — natural language, routes automatically
python kallyai.py ask "Book a table at Nobu for 4 tonight"
python kallyai.py ask "Email Dr. Smith to reschedule my Thursday appointment"
python kallyai.py ask "Find the best plumber near me and negotiate a quote"

# Check credits (NOT minutes — credits are the sole billing unit)
python kallyai.py credits balance

# Check your inbox
python kallyai.py messages inbox

# View incoming calls handled by your AI receptionist
python kallyai.py inbound calls
```

## 完整工作流程

### 第一步：收集用户需求

确定用户的具体需求。KallyAI 支持 14 个领域：

| 领域 | 示例 |
|--------|----------|
| **协调** | “预订一个座位”、“帮我处理这件事”、“任何多步骤请求” |
| **电话** | 拨打商务电话、查询预订信息、进行协商 |
| **来电** | 查看来电信息、管理来电路由规则、语音邮件、联系人 |
| **电话号码** | 配置电话号码、设置转接、管理来电显示号码 |
| **行动** | 创建日历事件、预订服务、分析账单、安排交通服务、处理食物订单、跑腿任务 |
| **消息** | 查看收件箱、阅读消息、查看消息记录 |
| **搜索** | 查找商家、研究选项、比较价格 |
| **电子邮件** | 发送电子邮件、管理电子邮件账户、设置语音邮件模板 |
| **多渠道** | 管理 WhatsApp、Telegram、电子邮件联系人及渠道状态 |
| **外联** | 多渠道外联任务（电话 + 电子邮件 + 消息传递） |
| **预算** | 估算费用、批准预算、查看费用明细 |
| **积分** | 查看余额、查看使用记录、规划消费 |
| **订阅** | 更改订阅计划、查看订阅状态、取消待处理的变更 |
| **推荐** | 获取推荐码、查看推荐数据、追踪推荐来源 |

**对于大多数请求，使用 `ask` 命令**——该命令会自动通过协调 AI 进行处理。**

### 第二步：身份验证

身份验证是自动完成的。首次调用 API 时，系统会打开浏览器以进行 Google 或 Apple 的登录。

```bash
python kallyai.py login         # Force re-auth
python kallyai.py logout        # Clear credentials
python kallyai.py auth-status   # Check login
```

### 第三步：执行任务

- **推荐使用自然语言输入**：  
  KallyAI 优先支持自然语言输入。

- **直接使用命令（当你知道具体操作领域时）：**  
  你可以直接使用相应的命令来执行特定操作。

### 第四步：监控与跟进

```bash
# Check goal status
python kallyai.py coord goals --status active
python kallyai.py coord goal <GOAL_ID>

# Review outbound call results
python kallyai.py calls history
python kallyai.py calls info <CALL_ID>
python kallyai.py calls transcript <CALL_ID>

# Review inbound calls handled by AI receptionist
python kallyai.py inbound calls
python kallyai.py inbound call <CALL_ID>
python kallyai.py inbound transcript <CALL_ID>

# Check inbox for responses
python kallyai.py messages inbox --unread
```

---

## 命令参考

### `ask` — 自然语言输入（使用率 80%）

该命令会通过协调 AI 进行任务分配，包括创建目标、拨打电话、发送电子邮件等操作。

### `coord` — 协调与任务管理

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

### `inbound` — 人工智能接听员（来电处理）

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
inbound add-rule --name "..." --action "..." # Create rule
inbound update-rule <id> ...         # Update rule
inbound delete-rule <id>             # Delete rule
inbound voicemails                   # List voicemails
inbound voicemail <id>               # Voicemail details
inbound voicemail-playback <id>      # Voicemail audio
inbound contacts                     # List contacts
inbound add-contact --name "..." --phone "+1..." # Add contact
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

### `messages` — 统一收件箱管理

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

### `budget` — 费用管理

```bash
budget estimate --type call "description"
budget approve <goal_id>
budget breakdown <goal_id>
budget ack-cap <goal_id>
```

### `credits` — 余额与使用情况

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

### `referrals` — 推荐计划管理

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

## 输出格式

默认输出格式为 **JSON**（适合 Claude 代码解析）。如需格式化的表格输出，请添加 `--human` 参数。

```bash
python kallyai.py credits balance              # JSON
python kallyai.py credits balance --human      # Pretty table
```

## 向后兼容性

旧的命令格式仍然有效，它们会被映射到新的子命令中。

```bash
python kallyai.py --phone "+1..." --task "..."   → calls make
python kallyai.py --usage                         → credits balance
python kallyai.py --history                       → calls history
python kallyai.py --call-info ID                  → calls info ID
python kallyai.py --transcript ID                 → calls transcript ID
```

---

## 安全性

- 令牌存储在 `~/.kallyai_token.json` 文件中，权限设置为 0600。
- CLI 认证仅支持本地主机（localhost）的请求。
- 通过 `state` 参数提供 CSRF 防护。
- 令牌有效期为 1 小时，支持自动刷新。

## 常见错误

| 错误代码 | HTTP 状态码 | 错误原因 | 处理建议 |
|------|------|--------|-------------------|
| `quota_exceeded` | 402 | 用户积分不足，请访问 kallyai.com/pricing 查看详情。 |
| `missing_phone_number` | 422 | 请用户提供电话号码。 |
| `emergency_number` | 422 | 无法拨打紧急电话。 |
| `country_restriction` | 403 | 该国家不受支持。 |
| `budget_exceeded` | 402 | 超出预算，请批准或取消操作。 |
| `email_not_connected` | 400 | 需要先连接电子邮件账户。 |
| `phone_not_provisioned` | 400 | 需要先配置电话号码。 |

## 完整 API 参考

请参阅 [references/api-reference.md](references/api-reference.md) 以获取完整的 API 文档。