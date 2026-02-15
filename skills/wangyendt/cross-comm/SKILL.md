---
name: pywayne-cross-comm
description: 基于WebSocket的跨语言通信服务，支持多种消息类型（文本、JSON、字典、字节数据、图片、文件、文件夹），并具备客户端管理功能。适用于构建Python与其他语言之间的实时通信应用程序，特别是在需要多设备间消息传递或通过阿里云OSS进行文件传输的场景中。该服务支持服务器端和客户端角色，具备心跳机制、客户端列表管理功能，以及按消息类型或发送者进行消息过滤的能力。
---
# Pywayne Cross Comm

`pywayne.cross_comm.CrossCommService` 提供了基于 WebSocket 的实时通信功能，支持 Python 与其他语言之间的通信，并内置了通过阿里云 OSS（Alibaba Cloud Object Storage）进行文件传输的功能。

## 先决条件

**OSS 配置**（文件/图片/文件夹传输所需）：

文件传输使用阿里云 OSS。请设置以下环境变量：

```bash
# .env file
OSS_ENDPOINT=your-oss-endpoint
OSS_BUCKET_NAME=your-bucket-name
OSS_ACCESS_KEY_ID=your-access-key
OSS_ACCESS_KEY_SECRET=your-access-secret
```

有关 OSS 的更多详细信息，请参阅 `pywayne-aliyun-oss` 技能文档。

## 快速入门

```python
import asyncio
from pywayne.cross_comm import CrossCommService, CommMsgType

# Server
server = CrossCommService(role='server', ip='0.0.0.0', port=9898)
await server.start_server()

# Client
client = CrossCommService(role='client', ip='localhost', port=9898, client_id='my_client')
await client.login()
```

## 服务器端

### 初始化服务器

```python
server = CrossCommService(
    role='server',
    ip='0.0.0.0',        # Listen on all interfaces
    port=9898,
    heartbeat_interval=30,     # Seconds between heartbeats
    heartbeat_timeout=60       # Seconds before marking offline
)
```

### 注册消息监听器

```python
@server.message_listener(msg_type=CommMsgType.TEXT)
async def handle_text(message):
    print(f"From {message.from_client_id}: {message.content}")

@server.message_listener(msg_type=CommMsgType.FILE, download_directory="./downloads")
async def handle_file(message):
    print(f"File downloaded: {message.content}")
```

### 启动服务器

```python
await server.start_server()  # Blocks until server stops
```

### 获取在线客户端列表

```python
online_clients = server.get_online_clients()  # Returns list of client IDs
```

## 客户端

### 初始化客户端

```python
client = CrossCommService(
    role='client',
    ip='localhost',           # Server address
    port=9898,
    client_id='my_client',    # Optional: auto-generated if omitted
    heartbeat_interval=30,
    heartbeat_timeout=60
)
```

### 登录和登出

```python
success = await client.login()
if success:
    print("Connected!")
    # ... communicate ...
    await client.logout()
```

### 发送消息

```python
# Broadcast to all
await client.send_message("Hello!", CommMsgType.TEXT)

# Send to specific client
await client.send_message("Private", CommMsgType.TEXT, to_client_id='target_id')

# JSON message
await client.send_message('{"key": "value"}', CommMsgType.JSON)

# Dict message
await client.send_message({"type": "data", "value": 123}, CommMsgType.DICT)

# Bytes (auto base64 encoded)
await client.send_message(b"binary", CommMsgType.BYTES)

# File (auto uploads to OSS)
await client.send_message("/path/to/file.txt", CommMsgType.FILE)

# Image (auto uploads to OSS)
await client.send_message("/path/to/image.jpg", CommMsgType.IMAGE)

# Folder (auto uploads to OSS)
await client.send_message("/path/to/folder", CommMsgType.FOLDER)
```

### 获取客户端列表

```python
# All clients (online + offline)
all_clients = await client.list_clients(only_show_online=False)
# Returns: {'clients': [...], 'total_count': N, 'only_show_online': False}

# Online only
online = await client.list_clients(only_show_online=True)
```

## 消息类型

`CommMsgType` 枚举（使用这些类型，而非字符串）：

| 类型 | 描述 |
|------|-------------|
| `CommMsgType TEXT` | 纯文本 |
| `CommMsgType.JSON` | JSON 字符串 |
| `CommMsgType.DICT` | Python 字典 |
| `CommMsgType.BYTES` | 二进制数据 |
| `CommMsgTypeIMAGE` | 图片文件 |
| `CommMsgType.FILE` | 普通文件 |
| `CommMsgType.FOLDER` | 文件夹 |

**内部类型**（自动处理）：HEARTBEAT、LOGIN、LOGOUT、LIST_CLIENTS、LIST_CLIENTS_RESPONSE、LOGIN_RESPONSE

## 消息监听器装饰器

```python
# Listen to specific type
@service.message_listener(msg_type=CommMsgType.TEXT)
async def handler(message):
    pass

# Listen from specific sender
@service.message_listener(msg_type=CommMsgType.FILE, from_client_id='specific_client')
async def handler(message):
    pass

# Listen to all types
@service.message_listener()
async def handler(message):
    pass
```

**注意**：监听器会自动过滤掉来自同一客户端自身的消息。

## 文件下载控制

文件下载功能通过监听器的 `download_directory` 参数进行控制：

```python
# Auto-download files to ./downloads
@client.message_listener(msg_type=CommMsgType.FILE, download_directory="./downloads")
async def handle_file(message):
    # message.content contains downloaded file path
    print(f"Downloaded: {message.content}")

# No auto-download - saves bandwidth
@client.message_listener(msg_type=CommMsgType.FILE, from_client_id='low_priority')
async def handle_file(message):
    # message.content contains OSS key, not downloaded
    print(f"File available: {message.oss_key}")
    # Optionally: client.download_file_manually(message.oss_key, "./manual_downloads/")
```

### 手动下载

```python
success = client.download_file_manually(
    oss_key="cross_comm/sender_id/123456_file.txt",
    save_directory="./downloads"
)
```

## 消息对象

```python
@dataclass
class Message:
    msg_id: str                    # Unique message ID
    from_client_id: str            # Sender ID
    to_client_id: str              # 'all' or specific client ID
    msg_type: CommMsgType           # Message type enum
    content: Any                   # Message content
    timestamp: float                # Unix timestamp
    oss_key: Optional[str]         # OSS key for file transfers

    def to_dict(self) -> Dict:      # Convert to dict
    @classmethod
    def from_dict(cls, data) -> 'Message':  # Create from dict
```

## 客户端 ID 生成

如果未指定 `client_id`，系统会使用 MAC 地址和 UUID 自动生成：
- 格式：`{mac_address}_{uuid_suffix}`
- 例如：`a1b2c3d4e5f6_abc12345`

## 命令行接口

```bash
# Run server
python -m pywayne.cross_comm server

# Run client
python -m pywayne.cross_comm client
```

## 重要说明

- **文件传输**：需要设置 OSS 相关的环境变量；文件会在发送时自动上传到阿里云 OSS。
- **异步操作**：所有操作均为异步的；请在异步环境中使用 `asyncio.run()` 或 `await`。
- **心跳信号**：系统会自动发送心跳信号；根据网络状况调整发送间隔。
- **消息过滤**：通过 `download_directory` 参数控制文件的自动下载，以节省带宽。
- **状态持久化**：服务器会将客户端状态保存到 `cross_comm_clients.yaml` 文件中。
- **角色特定方法**：服务器提供 `start_server()` 和 `get_online_clients()` 方法；客户端提供 `login()`、`logout()`、`send_message()` 和 `list_clients()` 方法。