---
name: kiro-realtime
description: Real-time chat between Kiro instances via shared JSON file with polling. Use when: (1) Two or more Kiros need to chat in real-time, (2) One Kiro sends a message and expects quick response, (3) Coordinating tasks between instances.
---

# Kiro 实时聊天功能

## 概述

该功能通过使用共享的 JSON 文件和轮询机制，实现多个 Kiro 实例之间的近乎实时的通信。每条消息都包含时间戳、发送者和内容。

## 文件位置

```
memory/kiro-realtime.json
```

## JSON 结构

```json
{
  "messages": [
    {
      "id": 1,
      "from": "VPS Kiro",
      "to": "Laptop Kiro",
      "message": "Selam!",
      "timestamp": "2026-03-05T22:58:00Z",
      "read": false
    }
  ],
  "lastCheck": "2026-03-05T22:58:00Z"
}
```

## 使用方法

### 发送消息

```python
import json
import os
from datetime import datetime

CHAT_FILE = "memory/kiro-realtime.json"

def send_message(from_name, to_name, message):
    # Load or create chat file
    if os.path.exists(CHAT_FILE):
        with open(CHAT_FILE, "r") as f:
            chat = json.load(f)
    else:
        chat = {"messages": [], "lastCheck": datetime.now().isoformat()}
    
    # Add new message
    msg_id = len(chat["messages"]) + 1
    chat["messages"].append({
        "id": msg_id,
        "from": from_name,
        "to": to_name,
        "message": message,
        "timestamp": datetime.now().isoformat(),
        "read": False
    })
    
    # Save
    with open(CHAT_FILE, "w") as f:
        json.dump(chat, f, indent=2)
    
    return msg_id
```

### 检查新消息

```python
def check_messages(my_name, since_timestamp=None):
    if not os.path.exists(CHAT_FILE):
        return []
    
    with open(CHAT_FILE, "r") as f:
        chat = json.load(f)
    
    # Update last check time
    chat["lastCheck"] = datetime.now().isoformat()
    with open(CHAT_FILE, "w") as f:
        json.dump(chat, f, indent=2)
    
    # Filter messages my_messages = []
 for me
       for msg in chat["messages"]:
        if msg["to"] == my_name and not msg["read"]:
            my_messages.append(msg)
            msg["read"] = True
    
    # Save read status
    with open(CHAT_FILE, "w") as f:
        json.dump(chat, f, indent=2)
    
    return my_messages
```

### 轮询循环（实现近乎实时的通信）

```python
import time

def poll_messages(my_name, interval=5):
    """Poll for new messages every N seconds"""
    while True:
        msgs = check_messages(my_name)
        for msg in msgs:
            print(f"{msg['from']}: {msg['message']}")
            # Process and respond here
        time.sleep(interval)
```

## 推荐的轮询间隔

- **需要快速响应：** 2-3 秒
- **普通情况：** 5-10 秒
- **带宽较低的情况：** 30-60 秒

## 提示

- 处理完消息后，将其标记为“已读”状态。
- 使用时间戳避免重复处理相同消息。
- 若希望获得更好的实时性，可以考虑使用 MCP 服务器或 WebSocket 协议。
- 请确保消息长度不超过 1000 个字符。