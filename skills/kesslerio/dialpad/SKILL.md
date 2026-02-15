---
name: dialpad
description: 通过 Dialpad API 发送短信和进行语音通话。支持单条/批量发送短信、带有 TTS（文本转语音）功能的语音通话，以及选择来电显示号码。
homepage: https://developers.dialpad.com/
---

# Dialpad技能

通过Dialpad API发送短信和进行语音通话。

## 可用的电话号码

| 数字 | 用途 | 格式 |
|--------|---------|--------|
| (415) 520-1316 | 销售团队 | 销售场景的默认号码 |
| (415) 360-2954 | 工作/个人 | 工作场景的默认号码 |
| (415) 991-7155 | 仅支持短信 | 仅支持短信（不支持语音通话） |

使用`--from <数字>`来指定显示在来电显示中的号码。

## 设置

**必需的环境变量：**
```
DIALPAD_API_KEY=your_api_key_here
```

**可选（用于ElevenLabs TTS语音合成）：**
```
ELEVENLABS_API_KEY=your_elevenlabs_api_key
```

从[Dialpad API设置](https://dialpad.com/api/settings)获取您的Dialpad API密钥。

## 使用方法

### 发送短信

```bash
# Basic SMS
python3 send_sms.py --to "+14155551234" --message "Hello from Clawdbot!"

# From specific number (e.g., work phone)
python3 send_sms.py --to "+14155551234" --message "Hello!" --from "+14153602954"

# Batch SMS (up to 10 recipients)
python3 send_sms.py --to "+14155551234" "+14155555678" --message "Group update"
```

### 进行语音通话

```bash
# Basic call (ring recipient - they'll answer to speak with you)
python3 make_call.py --to "+14155551234"

# Call with Text-to-Speech greeting (Dialpad's robotic TTS)
python3 make_call.py --to "+14155551234" --text "Hello! This is a call from ShapeScale."

# Call from specific number with TTS
python3 make_call.py --to "+14155551234" --from "+14153602954" --text "Meeting reminder"

# With custom voice (requires ELEVENLABS_API_KEY)
python3 make_call.py --to "+14155551234" --voice "Adam" --text "Premium voice test"
```

### 代理使用说明

**短信：**
```bash
python3 send_sms.py --to "+14155551234" --message "Your message here"
```

**语音通话：**
```bash
python3 make_call.py --to "+14155551234" --text "Optional TTS message"
```

## 语音选项

### 经济实惠的语音（推荐用于预算有限的情况）
| 语音 | 风格 | 说明 |
|-------|-------|-------|
| **Eric** ⭐ | 男性，声音平稳，值得信赖 | 经济实惠，可用！ |
| Daniel | 男性，英式发音，语气稳重 | 经济实惠 |
| Sarah | 女性，成熟稳重 | 经济实惠 |
| River | 男性，语气中性 | 经济实惠 |
| Alice | 女性，发音清晰 | 经济实惠 |
| Brian | 男性，声音低沉 | 经济实惠 |
| Bill | 男性，声音沉稳 | 经济实惠 |

### 高端语音（音质更高）
| 语音 | 风格 | 说明 |
|-------|-------|-------|
| **Adam** | 男性，声音低沉，发音清晰 | 最适合专业场合 |
| Antoni | 男性，语气温暖 | 语气友好 |
| Bella | 女性，声音柔和 | 语气温暖，易于交流 |

要使用特定的语音，请添加`--voice "语音名称"`。

## API功能

### SMS
- **端点：`POST https://dialpad.com/api/v2/sms`
- **每条消息的最大接收人数：** 每次请求最多10人
- **每条消息的最大长度：** 1600个字符
- **速率限制：** 每分钟100-800次请求（根据套餐不同而异）

### 语音通话
- **端点：`POST https://dialpad.com/api/v2/call`
- **所需参数：** `phone_number` + `user_id`
- **功能：** 出站通话、文本转语音
- **来电显示：** 必须为您的Dialpad账户分配一个来电显示号码

### 已知用户（自动检测）
| 名称 | 电话号码 | 用户ID |
|------|-------|---------|
| Martin | (415) 360-2954 | `5765607478525952` |
| Lilla | (415) 870-1945 | `5625110025338880` |
| Scott | (415) 223-0323 | `5964143916400640` |

## 响应

### SMS响应
```json
{
  "id": "4612924117884928",
  "status": "pending",
  "message_delivery_result": "pending",
  "to_numbers": ["+14158235304"],
  "from_number": "+14155201316",
  "direction": "outbound"
}
```

### 通话响应
```json
{
  "call_id": "6342343299702784",
  "status": "ringing"
}
```

## 错误处理

| 错误 | 含义 | 处理方式 |
|-------|---------|--------|
| `invalid_destination` | 无效的电话号码 | 验证E.164格式 |
| `invalid_source` | 来电显示号码未设置 | 检查`--from`参数的设置 |
| `no_route` | 无法送达 | 检查运营商/接收方信息 |
| `user_id required` | 缺少用户ID | 使用`--from`参数并指定用户ID |

## SMS存储（使用SQLite和FTS5）

短信存储在单个SQLite数据库中，并支持全文搜索。

### 存储方式

```
~/.dialpad/sms.db  # Single file with messages + FTS5 index
```

### 命令

```bash
# List all SMS conversations
python3 sms_sqlite.py list

# View specific conversation thread
python3 sms_sqlite.py thread "+14155551234"

# Full-text search across all messages
python3 sms_sqlite.py search "demo"

# Show unread message summary
python3 sms_sqlite.py unread

# Statistics
python3 sms_sqlite.py stats

# Mark messages as read
python3 sms_sqlite.py read "+14155551234"

# Migrate from legacy storage
python3 sms_sqlite.py migrate
```

### 功能特性

- **全文搜索**（使用FTS5技术，例如：`search "关键词"`）
- **快速查询**：通过联系人信息、时间戳和通话方向进行查询
- **ACID事务**：支持并发写入，数据不会损坏
- **未读消息跟踪**：可查看每个联系人的未读消息数量
- **非规范化联系人信息**：便于快速查看联系人列表

### Webhook集成

```python
from webhook_sqlite import handle_sms_webhook, format_notification, get_inbox_summary

# Store incoming message
result = handle_sms_webhook(dialpad_payload)
notification = format_notification(result)

# Get inbox summary
summary = get_inbox_summary()
```

### 旧版JSON存储（已弃用）

虽然仍支持基于JSON的存储方式，但不推荐使用：

```bash
python3 sms_storage.py [list|thread|search|unread]
```

## 系统要求

- Python 3.7及以上版本
- 无需外部依赖（仅使用标准库）
- 必须设置有效的`DIALPAD_API_KEY`环境变量
- 如果使用ElevenLabs TTS语音合成服务，还需设置`ELEVENLABS_API_KEY`并配置Webhook

## 阅读短信消息

Dialpad没有提供直接的`GET /sms`端点。您可以使用以下方法来获取短信信息：

### 1. 实时获取：短信Webhook

当短信发送或接收时，通过Webhook实时接收通知。

```bash
# Create a webhook subscription
python3 create_sms_webhook.py create --url "https://your-server.com/webhook/dialpad" --direction "all"

# List existing subscriptions
python3 create_sms_webhook.py list
```

**Webhook事件：**
- `sms_sent` — 发出的短信
- `sms_received` — 收到的短信

**注意：** 需要添加`message_content_export`权限才能在事件中获取短信内容。

### 2. 历史记录：统计信息导出

可以将过去的短信信息导出为CSV文件。

```bash
# Export all SMS
python3 export_sms.py --output all_sms.csv

# Export by date range
python3 export_sms.py --start-date 2026-01-01 --end-date 2026-01-31 --output jan_sms.csv

# Export for specific office
python3 export_sms.py --office-id 6194013244489728 --output office_sms.csv
```

**输出文件格式：**
- `date` — 时间戳
- `from_number` — 发件人
- `to_number` — 收件人
- `text` — 短信内容
- `status` — 短信送达状态

## 架构

```
Dialpad SMS Skill
├── send_sms.py           # Send SMS (working)
├── make_call.py          # Make voice calls (working)
├── create_sms_webhook.py # Create webhook subscriptions (new)
├── export_sms.py         # Export historical SMS (new)
├── sms_sqlite.py         # SQLite storage with FTS5 (RECOMMENDED)
├── webhook_sqlite.py     # Webhook handler for SQLite
├── sms_storage.py        # Legacy JSON storage (deprecated)
└── webhook_receiver.py   # Legacy webhook handler
```