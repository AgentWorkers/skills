---
name: onebot-adapter
description: 将 OpenClaw 连接到 OneBot 协议，以实现与 QQ 机器人的集成。当通过 NapCat 或其他 OneBot 服务器接收或发送 QQ 消息时，请使用此功能。
version: 1.0.0
---
# OneBot 适配器

将 OpenClaw 连接到基于 OneBot 协议的服务器（如 NapCat），以实现 QQ 聊天机器人的功能。

## 快速入门

### 1. 配置连接

在环境变量或配置文件中设置 OneBot 服务器的 URL：
```bash
export ONEBOT_WS_URL="ws://127.0.0.1:3001"
export ONEBOT_HTTP_URL="http://127.0.0.1:3000"
export ONEBOT_TOKEN="your-token"
```

### 2. 接收消息

使用 WebSocket 监听器脚本接收 QQ 消息：
```bash
python scripts/onebot_ws_listener.py
```

### 3. 发送消息

使用 HTTP API 发送消息：
```python
from scripts.onebot_client import OneBotClient

client = OneBotClient()
client.send_private_msg(user_id=123456, message="Hello!")
client.send_group_msg(group_id=789012, message="Group message")
```

## 连接方式

### WebSocket（推荐）
- 实时双向通信
- 可立即接收事件
- 支持发送和接收消息

### HTTP
- 请求-响应模式
- 适用于简单的消息发送
- 需要轮询才能接收消息

## 常见任务

### 获取登录信息
```python
client.get_login_info()
```

### 获取好友/群列表
```python
client.get_friend_list()
client.get_group_list()
```

### 处理消息
有关消息解析和响应模式的详细信息，请参阅 [references/message-handling.md](references/message-handling.md)。

## NapCat 特性

NapCat 是基于 NTQQ 实现的 OneBot11 客户端。

默认端口：
- WebSocket：3001
- HTTP：3000
- WebUI：6099

令牌认证是可选的，但在公共部署中推荐使用。

## 故障排除

**连接被拒绝**：检查 OneBot 服务器是否正在运行以及端口设置是否正确。

**认证失败**：验证令牌是否与 OneBot 服务器的配置一致。

**消息未送达**：检查用户 ID/群组 ID 是否存在，以及机器人是否具有相应的权限。