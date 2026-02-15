---
name: frigate
description: 通过基于会话的身份验证来访问护卫舰（Frigate）的NVR（网络视频录像）摄像头。可以获取实时快照、检索运动事件信息，并获取视频流的URL。该系统为门铃、车道、前部、东侧、邮箱和车库摄像头提供了相应的CLI（命令行接口）辅助脚本。
---

# Frigate NVR集成

使用环境变量 `FRIGATE_USER` 和 `FRIGATE_PASS` 中的凭据，通过 `FRIGATE_URL` 访问 Frigate NVR 服务器。

## 认证

Frigate 使用基于会话的认证方式（而非 HTTP Basic Auth）：

```python
import requests

session = requests.Session()
response = session.post(
    f"{FRIGATE_URL}/api/login",
    json={"user": FRIGATE_USER, "password": FRIGATE_PASS},
    verify=False  # For self-signed certificates
)
# session.cookies contains frigate_token for subsequent requests
```

## 常用操作

### 获取摄像头列表
```python
response = session.get(f"{FRIGATE_URL}/api/config", verify=False)
config = response.json()
cameras = list(config.get('cameras', {}).keys())
# Returns: ['driveway', 'front', 'east', 'mailbox', 'garage', 'doorbell']
```

### 从摄像头获取快照
```python
snapshot = session.get(
    f"{FRIGATE_URL}/api/{camera_name}/latest.jpg",
    verify=False
)
# Save: with open(f"/tmp/{camera_name}.jpg", "wb") as f: f.write(snapshot.content)
```

### 获取运动事件
```python
events = session.get(
    f"{FRIGATE_URL}/api/events?cameras={camera_name}&has_clip=1",
    verify=False
).json()
# Returns list of motion detection events with timestamps
```

### 获取摄像头流媒体地址
```python
config = session.get(f"{FRIGATE_URL}/api/config", verify=False).json()
stream_config = config.get('go2rtc', {}).get('streams', {}).get(camera_name)
# Returns RTSP/WebRTC stream URLs
```

## 环境变量

**必填变量：**
- `FRIGATE_URL` - Frigate 服务器的 URL（例如：`https://server.local:8971/`）
- `FRIGATE_USER` - 用于认证的用户名
- `FRIGATE_PASS` - 用于认证的密码

**可选变量：**
- 除上述变量外，无需其他可选变量

## 示例：将门铃快照发送到 Telegram
```python
import requests

session = requests.Session()
session.post(f"{FRIGATE_URL}/api/login",
    json={"user": FRIGATE_USER, "password": FRIGATE_PASS}, verify=False)

# Get doorbell snapshot
snapshot = session.get(f"{FRIGATE_URL}/api/doorbell/latest.jpg", verify=False)

# Send to Telegram
from clawdbot import message
message(action="send", channel="telegram", target="3215551212",
        message="Doorbell snapshot", path="/tmp/doorbell_snapshot.jpg")
```

## 注意事项：

- 在家庭网络中，对于自签名证书，请始终使用 `verify=False`。
- 会话令牌在 24 小时后失效（可通过 `session_length` 配置更改）。
- `/api/cameras` 端点不存在；请使用 `/api/config` 获取摄像头信息。
- Frigate 0.16 及更高版本使用此认证模型。

## 随附资源

- **脚本**：请参阅 [scripts/frigate.py](scripts/frigate.py)，其中包含以下 CLI 工具：`list`、`snapshot`、`events`、`stream`。
- **API 参考**：请参阅 [references/api.md](references/api.md)，以获取完整的 API 文档。