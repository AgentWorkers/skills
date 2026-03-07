---
name: telegram-business
description: Telegram bot for business automation — lead capture forms, inline keyboard menus, FAQ matching, appointment booking flows, and payment integration. Use for building customer-facing Telegram bots, community management, and lead generation.
homepage: https://www.agxntsix.ai
license: MIT
compatibility: Python 3.10+, Telegram Bot Token from @BotFather
metadata: {"openclaw": {"emoji": "\ud83e\udd16", "requires": {"env": ["TELEGRAM_BOT_TOKEN"]}, "primaryEnv": "TELEGRAM_BOT_TOKEN", "homepage": "https://www.agxntsix.ai"}}
---

# Telegram 商业机器人

在 Telegram 上构建自动化业务流程——包括潜在客户信息收集、预约预订、常见问题解答（FAQ）机器人、支付处理以及社区管理等功能。

## 快速入门

```bash
export TELEGRAM_BOT_TOKEN="123456:ABC-DEF..."

# Send a message
python3 {baseDir}/scripts/telegram_business.py send-message <chat_id> "Hello from your business bot!"

# Send inline keyboard
python3 {baseDir}/scripts/telegram_business.py send-menu <chat_id> "How can I help?" '[{"text":"📅 Book Appointment","callback_data":"book"},{"text":"❓ FAQ","callback_data":"faq"},{"text":"💬 Talk to Sales","callback_data":"sales"}]'

# Start lead capture
python3 {baseDir}/scripts/telegram_business.py send-lead-form <chat_id>
```

## 机器人设置

### 1. 通过 @BotFather 创建机器人
1. 打开 Telegram，搜索 `@BotFather`
2. 发送 `/newbot`
3. 选择机器人名称和用户名（用户名必须以 `bot` 结尾）
4. 复制生成的机器人令牌，并将其设置为 `TELEGRAM_BOT_TOKEN`

### 2. 配置机器人
```
/setdescription - Business description shown on bot profile
/setabouttext - Short about text
/setuserpic - Bot avatar
/setcommands - Set command menu:
  start - Get started
  book - Book appointment
  faq - Frequently asked questions
  contact - Contact us
  help - Get help
```

### 3. Webhook 设置
```bash
# Set webhook (use your server URL)
python3 {baseDir}/scripts/telegram_business.py set-webhook "https://your-domain.com/webhook/telegram"

# Get webhook info
python3 {baseDir}/scripts/telegram_business.py get-webhook

# Delete webhook (switch to polling)
python3 {baseDir}/scripts/telegram_business.py delete-webhook
```

## 可用命令

### 消息发送
```bash
# Send text
python3 {baseDir}/scripts/telegram_business.py send-message <chat_id> "Hello!"

# Send with HTML formatting
python3 {baseDir}/scripts/telegram_business.py send-message <chat_id> "<b>Bold</b> and <i>italic</i>" --html

# Send with Markdown
python3 {baseDir}/scripts/telegram_business.py send-message <chat_id> "**Bold** and _italic_" --markdown

# Reply to a message
python3 {baseDir}/scripts/telegram_business.py send-message <chat_id> "Got it!" --reply-to <message_id>
```

### 内联键盘
```bash
# Simple menu (buttons in rows of 2)
python3 {baseDir}/scripts/telegram_business.py send-menu <chat_id> "Choose an option:" '[
  {"text":"Option A","callback_data":"opt_a"},
  {"text":"Option B","callback_data":"opt_b"},
  {"text":"Option C","callback_data":"opt_c"}
]'

# URL buttons
python3 {baseDir}/scripts/telegram_business.py send-menu <chat_id> "Visit us:" '[
  {"text":"🌐 Website","url":"https://example.com"},
  {"text":"📸 Instagram","url":"https://instagram.com/example"}
]'

# Answer callback query (acknowledge button press)
python3 {baseDir}/scripts/telegram_business.py answer-callback <callback_query_id> "Processing..."

# Edit message (update after button press)
python3 {baseDir}/scripts/telegram_business.py edit-message <chat_id> <message_id> "Updated text!"
```

### 潜在客户信息收集
```bash
# Send lead capture form (multi-step inline flow)
python3 {baseDir}/scripts/telegram_business.py send-lead-form <chat_id>

# Process lead data (after collecting via conversation)
python3 {baseDir}/scripts/telegram_business.py process-lead '{"chat_id":123,"name":"John Doe","email":"john@example.com","phone":"+15551234567","interest":"AI automation","source":"telegram"}'
```

### 常见问题解答系统
```bash
# Match question to FAQ
python3 {baseDir}/scripts/telegram_business.py faq-match "What are your business hours?"

# Send FAQ menu
python3 {baseDir}/scripts/telegram_business.py send-faq-menu <chat_id>
```

### 媒体处理
```bash
# Send photo
python3 {baseDir}/scripts/telegram_business.py send-photo <chat_id> "https://example.com/image.jpg" "Caption here"

# Send document
python3 {baseDir}/scripts/telegram_business.py send-document <chat_id> "/path/to/file.pdf"

# Send contact card
python3 {baseDir}/scripts/telegram_business.py send-contact <chat_id> "+15551234567" "John" "Doe"
```

## 潜在客户信息收集流程

机器人会引导用户完成以下多步骤表单填写：
1. **开始** → 显示带有菜单按钮的欢迎信息
2. **“获取报价”** → 请求用户输入姓名
3. 用户输入姓名后 → 请求输入电子邮件地址
4. 用户输入电子邮件地址后 → 可选：请求输入电话号码
5. 用户输入电话号码后 → 提供服务选项供选择
6. 用户选择服务后 → 确认并发送感谢信息
7. 潜在客户的信息将以 JSON 格式输出，便于集成到客户关系管理（CRM）系统中

### 与 CRM 系统集成
```bash
# Capture lead from Telegram, score it, add to GHL
LEAD='{"name":"John","email":"john@x.com","phone":"+1555...","source":"telegram"}'
SCORE=$(python3 ../lead-gen-pipeline/{baseDir}/scripts/lead_scorer.py "$LEAD")
python3 ../ghl-crm/{baseDir}/scripts/ghl_api.py contacts create "$LEAD"
```

## 常见问题解答自动化

在脚本的 `FAQ_DATABASE` 中定义常见问题解答内容：

```python
FAQ_DATABASE = [
    {"q": "What are your hours?", "a": "We're open Mon-Fri 9am-6pm EST.", "keywords": ["hours", "open", "schedule"]},
    {"q": "Where are you located?", "a": "123 Main St, New York, NY", "keywords": ["location", "address", "where"]},
    {"q": "How much does it cost?", "a": "Plans start at $99/mo. Reply 'pricing' for details.", "keywords": ["cost", "price", "pricing", "how much"]},
]
```

该系统采用关键词匹配和模糊相似度算法进行问题匹配；如需使用人工智能辅助匹配，可连接外部大型语言模型（LLM）。

## 支付集成

Telegram 支持通过支付提供商（如 Stripe）进行原生支付：

```bash
# Send invoice
python3 {baseDir}/scripts/telegram_business.py send-invoice <chat_id> '{
  "title": "Consultation Fee",
  "description": "1-hour AI automation consultation",
  "payload": "consultation_001",
  "provider_token": "STRIPE_TOKEN",
  "currency": "USD",
  "prices": [{"label": "Consultation", "amount": 9900}]
}'
```

**注意：** `amount` 以最小货币单位表示（例如，USD 的单位是分）。$99.00 表示 9900 分。

## 群组管理
```bash
# Get chat info
python3 {baseDir}/scripts/telegram_business.py get-chat <chat_id>

# Get member count
python3 {baseDir}/scripts/telegram_business.py get-member-count <chat_id>

# Pin a message
python3 {baseDir}/scripts/telegram_business.py pin-message <chat_id> <message_id>

# Set chat description
python3 {baseDir}/scripts/telegram_business.py set-description <chat_id> "Welcome to our community!"
```

## Webhook 数据处理

使用 Webhook 时，接收到的更新信息格式如下：
**消息内容：**
```json
{"update_id": 123, "message": {"chat": {"id": 456}, "from": {"id": 789, "first_name": "John"}, "text": "/start"}}
```

**回调事件（按钮被点击时）：**
```json
{"update_id": 124, "callback_query": {"id": "abc", "data": "book", "message": {"chat": {"id": 456}}}}
```

数据解析方法：
```bash
python3 {baseDir}/scripts/telegram_business.py parse-update '<json>'
```

## 致谢

本机器人由 [M. Abidi](https://www.linkedin.com/in/mohammad-ali-abidi) 和 [agxntsix.ai](https://www.agxntsix.ai) 开发。
[YouTube](https://youtube.com/@aiwithabidi) | [GitHub](https://github.com/aiwithabidi)
本机器人是 **AgxntSix Skill Suite** 的一部分，专为 OpenClaw 代理设计。

📅 **需要帮助为您的业务设置 OpenClaw 吗？** [预约免费咨询](https://cal.com/agxntsix/abidi-openclaw)