---
name: zulip
description: 通过 REST API 和 Python 客户端与 Zulip 聊天平台进行交互。当您需要从流或主题中读取消息、向频道或用户发送消息、管理私信对话、列出用户，或与 Zulip 组织集成以实现团队沟通工作流程时，可以使用此功能。
---
# Zulip 集成

与 Zulip 聊天平台进行交互，以实现团队沟通。

## 设置

### 1. 安装 Python 客户端

```bash
pip install zulip
```

### 2. 创建配置文件

创建 `~/.config/zulip/zuliprc` 文件：

```ini
[api]
email=bot@example.zulipchat.com
key=YOUR_API_KEY_HERE
site=https://example.zulipchat.com
```

从 Zulip 管理面板（设置 → 机器人）获取凭据。

### 3. 验证连接

```bash
python scripts/zulip_client.py streams
```

## 快速入门

### 使用辅助脚本

`scripts/zulip_client.py` 提供了以下常用操作：

- **列出聊天流：**
```bash
python scripts/zulip_client.py streams
python scripts/zulip_client.py streams --json
```

- **读取消息：**
```bash
# Recent stream messages (by name)
python scripts/zulip_client.py messages --stream "General" --num 10

# By stream ID (more reliable, use 'streams' to find IDs)
python scripts/zulip_client.py messages --stream-id 42 --num 10

# Specific topic
python scripts/zulip_client.py messages --stream "General" --topic "Updates"

# Private messages
python scripts/zulip_client.py messages --type private --num 5

# Mentions
python scripts/zulip_client.py messages --type mentioned
```

**注意：** 聊天流的名称可能包含描述性信息。使用 `--stream-id` 可以准确识别聊天流。

- **发送消息：**
```bash
# To stream
python scripts/zulip_client.py send --type stream --to "General" --topic "Updates" --content "Hello!"

# Private message (user_id)
python scripts/zulip_client.py send --type private --to 123 --content "Hi there"
```

- **列出用户：**
```bash
python scripts/zulip_client.py users
python scripts/zulip_client.py users --json
```

### 直接使用 Python 客户端

```python
import zulip

client = zulip.Client(config_file="~/.config/zulip/zuliprc")

# Read messages
result = client.get_messages({
    "anchor": "newest",
    "num_before": 10,
    "num_after": 0,
    "narrow": [{"operator": "stream", "operand": "General"}]
})

# Send to stream
client.send_message({
    "type": "stream",
    "to": "General",
    "topic": "Updates",
    "content": "Message text"
})

# Send DM
client.send_message({
    "type": "private",
    "to": [user_id],
    "content": "Private message"
})
```

### 使用 curl

```bash
# List streams
curl -u "bot@example.com:KEY" https://example.zulipchat.com/api/v1/streams

# Get messages
curl -u "bot@example.com:KEY" -G \
  "https://example.zulipchat.com/api/v1/messages" \
  --data-urlencode 'anchor=newest' \
  --data-urlencode 'num_before=20' \
  --data-urlencode 'num_after=0' \
  --data-urlencode 'narrow=[{"operator":"stream","operand":"General"}]'

# Send message
curl -X POST "https://example.zulipchat.com/api/v1/messages" \
  -u "bot@example.com:KEY" \
  --data-urlencode 'type=stream' \
  --data-urlencode 'to=General' \
  --data-urlencode 'topic=Updates' \
  --data-urlencode 'content=Hello!'
```

## 常见工作流程

- **监控聊天流中的新消息：**
```python
def get_latest_messages(client, stream_name, last_seen_id=None):
    narrow = [{"operator": "stream", "operand": stream_name}]
    
    if last_seen_id:
        # Get only messages after last seen
        request = {
            "anchor": last_seen_id,
            "num_before": 0,
            "num_after": 100,
            "narrow": narrow
        }
    else:
        # Get recent messages
        request = {
            "anchor": "newest",
            "num_before": 20,
            "num_after": 0,
            "narrow": narrow
        }
    
    result = client.get_messages(request)
    return result["messages"]
```

- **回复特定主题：**
```python
def reply_to_message(client, original_message, reply_text):
    """Reply in the same stream/topic as original message."""
    client.send_message({
        "type": "stream",
        "to": original_message["display_recipient"],
        "topic": original_message["subject"],
        "content": reply_text
    })
```

- **搜索消息：**
```python
def search_messages(client, keyword, stream=None):
    narrow = [{"operator": "search", "operand": keyword}]
    
    if stream:
        narrow.append({"operator": "stream", "operand": stream})
    
    result = client.get_messages({
        "anchor": "newest",
        "num_before": 50,
        "num_after": 0,
        "narrow": narrow
    })
    
    return result["messages"]
```

- **通过电子邮件获取用户 ID：**
```python
def get_user_id(client, email):
    """Find user_id by email address."""
    result = client.get_members()
    
    for user in result["members"]:
        if user["email"] == email:
            return user["user_id"]
    
    return None
```

## 消息格式

Zulip 支持 Markdown 格式：

- **加粗：** `**文本**`
- **斜体：** `*文本*`
- **代码：** `` `代码` ``
- **代码块：` ```语言\ncode\n``` `
- **引用：`> 引用文本`
- **提及用户：`@**全名**`
- **链接聊天流：`#**聊天流名称**`
- **链接：`[文本](网址)`

## 高级功能

- **上传和共享文件：**
```python
with open("file.pdf", "rb") as f:
    result = client.upload_file(f)
    file_url = result["uri"]

# Share in message
client.send_message({
    "type": "stream",
    "to": "General",
    "topic": "Files",
    "content": f"Check out [this file]({file_url})"
})
```

- **对消息作出反应：**
```python
# Add reaction
client.add_reaction({
    "message_id": 123,
    "emoji_name": "thumbs_up"
})

# Remove reaction
client.remove_reaction({
    "message_id": 123,
    "emoji_name": "thumbs_up"
})
```

## 参考

请参阅 `references/api-quick-reference.md` 以获取完整的 API 文档、端点和示例。

## 故障排除

- **配置文件未找到：**
  - 确保 `~/.config/zulip/zuliprc` 文件存在且格式正确。
  - 检查文件权限（应具有读取权限）。

- **身份验证失败：**
  - 确认 API 密钥正确。
  - 检查机器人是否在 Zulip 管理面板中处于激活状态。
  - 确保站点 URL 与组织 URL 一致。

- **消息数组为空：**
  - 机器人可能未订阅该聊天流。
  - 使用 `client.get_subscriptions()` 方法检查订阅情况。
  - 管理员可能需要将机器人添加到私有聊天流中。

- **速率限制错误：**
  - 标准限制：每分钟 200 次请求。
  - 每分钟消息发送量限制约为 20-30 条。
  - 在批量操作之间添加延迟。
  - 检查 429 响应中的 `Retry-After` 头部信息。