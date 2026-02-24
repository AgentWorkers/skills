---
name: line-client
description: 通过 Chrome 扩展程序网关集成 LINE 消息功能：可以发送/接收 LINE 消息、管理联系人、群组、个人资料以及表情符号。支持通过二维码进行身份验证。通过 Chrome 扩展程序网关（line-chrome-gw.line-apps.com）提供经过 HMAC 签名的 API 访问服务。
---
# LINE 客户端技能

这是一个完整的 LINE 消息客户端，通过 Chrome 扩展程序和 JSON API 进行通信。

## 仓库与文件

- **仓库:** `/data/workspace/line-client` ([github.com/2manslkh/line-api](https://github.com/2manslkh/line-api))
- **主要客户端代码:** `src/chrome_client.py` → `LineChromeClient`
- **二维码登录:** `src/auth/qr_login.py` → `QRLogin`
- **HMAC 签名器:** `src/hmac/signer.js` (Node.js，自动运行在端口 18944)
- **令牌存储:** `~/.line-client/tokens.json`
- **证书缓存:** `~/.line-client/sqr_cert`
- **WASM 文件:** `lstm.wasm` + `lstmSandbox.js` (必需，位于仓库根目录)

## 快速入门

```python
import json
from pathlib import Path
from src.chrome_client import LineChromeClient

tokens = json.loads((Path.home() / ".line-client" / "tokens.json").read_text())
client = LineChromeClient(auth_token=tokens["auth_token"])

# Send a message
client.send_message("U...", "Hello!")

# Get profile
profile = client.get_profile()
```

令牌的有效期为约 7 天。如果令牌过期（返回 `APIError(10051)`），请重新运行二维码登录。

## QR 登录（认证）

二维码登录需要用户操作：在手机上扫描二维码并输入 PIN 码。

```python
from src.hmac import HmacSigner
from src.auth.qr_login import QRLogin
import qrcode

signer = HmacSigner(mode="server")
login = QRLogin(signer)
result = login.run(
    on_qr=lambda url: send_qr_image_to_user(qrcode.make(url)),
    on_pin=lambda pin: send_pin_to_user_IMMEDIATELY(pin),  # TIME SENSITIVE!
    on_status=lambda msg: print(msg),
)
# result.auth_token, result.mid, result.refresh_token
```

**重要提示：** PIN 码必须在约 60 秒内发送给用户。`on_pin` 事件触发后立即发送 PIN 码。

### QR 登录状态机
1. `createSession` → 会话 ID
2. `createQrCode` → 回调 URL（附加 `?secret={curve25519_pubkey}&e2eeVersion=1`）
3. `checkQrCodeVerified` — 监听扫描结果（使用 `X-Line-Session-ID`，不包含 `origin` 头部）
4. **`verifyCertificate`** — 即使失败也必须调用（是必需的状态转换！）
5. `createPinCode` → 生成 6 位 PIN 码（如果步骤 4 中证书验证通过，则跳过此步骤）
6. `checkPinCodeVerified` — 监听用户输入 PIN 码
7. `qrCodeLoginV2` → 生成 JWT 令牌、证书和刷新令牌

### 服务器端登录脚本
```bash
python scripts/qr_login_server.py /tmp/qr.png
```
在标准输出（stdout）上发送 JSON 事件：`{"event": "qr", "path": "...", "url": "..."}`，`{"event": "pin", "pin": "123456"}`，`{"event": "done", "mid": "U..."}`。

## 所有 API 方法

### 联系人与好友

| 方法 | 参数 | 描述 |
|--------|------|-------------|
| `get_profile()` | — | 获取自己的个人资料（显示名称、mid、状态消息等） |
| `get_contact(mid)` | mid: str | 获取单个联系人的资料 |
| `get_contacts(mids)` | mids: list[str] | 获取多个联系人的资料 |
| `get_all_contact_ids()` | — | 获取所有好友的 MID 列表 |
| `find_contact_byuserid(userid)` | userid: str | 通过 LINE ID 搜索联系人 |
| `find_and_add_contact_by_mid(mid)` | mid: str | 通过 MID 添加好友 |
| `find_contacts_by_phone(phones)` | phones: list[str] | 通过电话号码搜索联系人 |
| `add_friend_by_mid(mid)` | mid: str | 通过 MID 添加好友（RelationService） |
| `getblocked_contact_ids()` | — | 获取被屏蔽的联系人 MID 列表 |
| `getblocked_recommendation_ids()` | — | 获取被屏蔽的推荐联系人 ID 列表 |
| `block_contact(mid)` | mid: str | 取消屏蔽某个联系人 |
| `unblock_contact(mid)` | mid: str | 解除对某个联系人的屏蔽 |
| `block_recommendation(mid)` | mid: str | 取消对某个好友的推荐 |
| `update_contact_setting(mid, flag, value)` | mid, flag: int, value: str | 更新联系人设置（例如静音） |
| `get_favorite_mids()` | — | 获取收藏的联系人 MID 列表 |
| `get_recommendation_ids()` | — | 获取推荐的好友 ID 列表 |

### 消息

| 方法 | 参数 | 描述 |
|--------|------|-------------|
| `send_message(to, text, ...)` | to: str, text: str, reply_to: str (可选) | 发送文本消息。支持通过 `reply_to/message_id` 回复 |
| `unsend_message(message_id)` | message_id: str | 取消/删除已发送的消息 |
| `get_recent_messages(chat_id, count=50)` | chat_id: str | 获取聊天中的最新消息 |
| `get_previous_messages(chat_id, end_seq, count=50)` | chat_id, end_seq: int | 分页获取聊天历史记录（较旧的消息） |
| `get_messages_by_ids(message_ids)` | message_ids: list[str] | 获取特定消息 |
| `get_message_boxes(count=50)` | — | 获取聊天列表（显示最后一条消息） |
| `get_message_boxes_by_ids(chat_ids)` | chat_ids: list[str] | 获取特定聊天的消息列表 |
| `get_message_read_range(chat_ids)` | chat_ids: list[str] | 获取消息的已读状态信息 |
| `send_chat_checked(chat_id, last_message_id)` | chat_id, last_message_id: str | 将消息标记为已读 |
| `send_chat_removed(chat_id, last_message_id)` | chat_id, last_message_id: str | 从收件箱中删除聊天记录 |
| `send_postback(to, postback_data)` | to, postback_data: str | 发送回调数据（用于机器人交互） |

### 聊天与群组

| 方法 | 参数 | 描述 |
|--------|------|-------------|
| `get_chats(chat_ids, with_members=True, with_invitees=True)` | chat_ids: list[str] | 获取聊天/群组详情 |
| `get_all_chat_mids()` | — | 获取所有聊天/群组的 MID 列表 |
| `create_chat(name, target_mids)` | name: str, target_mids: list[str] | 创建新的群组聊天 |
| `accept_chat_invitation(chat_id)` | chat_id: str | 接受群组邀请 |
| `reject_chat_invitation(chat_id)` | chat_id: str | 拒绝群组邀请 |
| `invite_into_chat(chat_id, mids)` | chat_id: str, mids: list[str] | 邀请用户加入群组 |
| `cancel_chat_invitation(chat_id, mids)` | chat_id: str, mids: list[str] | 取消待处理的邀请 |
| `delete_other_from_chat(chat_id, mids)` | chat_id: str, mids: list[str] | 将成员从群组中踢出 |
| `leave_chat(chat_id)` | chat_id: str | 离开群组聊天 |
| `update_chat(chat_id, updates)` | chat_id: str, updates: dict | 更新群组名称/设置 |
| `set_chat_hidden_status(chat_id, hidden)` | chat_id: str, hidden: bool | 将聊天归档/解档 |
| `get_rooms(room_ids)` | room_ids: list[str] | 获取旧版房间信息 |
| `invite_into_room(room_id, mids)` | room_id: str, mids: list[str] | 邀请用户加入旧版房间 |
| `leave_room(room_id)` | room_id: str | 离开旧版房间 |

### 互动反应

| 方法 | 参数 | 描述 |
|--------|------|-------------|
| `react(message_id, reaction_type)` | message_id: str, type: int | 对消息做出反应。类型：2=点赞, 3=爱, 4=笑, 5=惊讶, 6=难过, 7=生气 |
| `cancel_reaction(message_id)` | message_id: str | 取消自己的反应 |

### 个人资料与设置

| 方法 | 参数 | 描述 |
|--------|------|-------------|
| `update_profile_attributes(attr, value, meta={})` | attr: int, value: str | 更新个人资料。属性：2=DISPLAY_NAME, 16=STATUS_MESSAGE, 4=PICTURE_STATUS |
| `update_status_message(message)` | message: str | 快捷方式：更新状态消息 |
| `update_display_name(name)` | name: str | 快捷方式：更新显示名称 |
| `get_settings()` | — | 获取所有账户设置 |
| `get_settings_attributes(attr_bitset)` | attr_bitset: int | 获取特定设置 |
| `update_settings_attributes(attr_bitset, settings)` | attr_bitset: int, settings: dict | 更新设置 |

### 轮询与事件

| 方法 | 参数 | 描述 |
|--------|------|-------------|
| `get_last_oprevision()` | — | 获取最新的操作修订号 |
| `fetch_ops(count=50)` | — | 获取待处理的操作（可能需要长时间轮询） |
| `poll()` | — | 当操作到达时生成事件 |
| `on_message(handler)` | handler: Callable(msg, client) | 启动轮询线程，在新消息到达时调用处理函数。操作类型：26=SEND_MESSAGE, 27=RECEIVE_MESSAGE |
| `stop()` | — | 停止轮询线程 |

### 其他服务

| 方法 | 参数 | 描述 |
|--------|------|-------------|
| `get_server_time()` | — | 获取 LINE 服务器时间戳 |
| `get_configurations()` | — | 获取服务器配置 |
| `get_rsa_key_info()` | — | 获取用于认证的 RSA 密钥 |
| `issue_channel_token(channel_id)` | channel_id: str | 发行频道令牌（LINE 登录/LIFF） |
| `get_buddy_detail(mid)` | mid: str | 获取官方账户信息 |
| `report_abuse(mid, category=0, reason="")` | mid: str | 举报用户 |
| `add_friend_by_mid(mid)` | mid: str | 添加好友（RelationService） |
| `logout()` | — | 登出并使令牌失效 |

## MID 格式

LINE 通过 MID 来标识实体：
- `U...` 或 `u...` → 用户（toType=0）
- `C...` 或 `c...` → 群组聊天（toType=2）
- `R...` 或 `r...` → 房间（toType=1）

客户端在发送消息时会自动从 MID 前缀中检测 `toType`。

## HMAC 签名

所有 API 调用都需要 `X-Hmac` 头部。WASM 签名器会自动处理签名：
- 从版本 "3.7.1" 和访问令牌中派生密钥（通过 `lstm.wasm` 中的专有 KDF）
- 对 `path + body` 进行签名 → 转换为 base64 → 生成 `X-Hmac`
- 服务器模式：签名耗时约 13 毫秒（Node.js HTTP 服务器，运行在端口 18944）
- 子进程模式：签名耗时约 2 秒（备用方案）

## 错误处理

```python
from src.chrome_client import APIError

try:
    client.send_message(mid, "test")
except APIError as e:
    print(e.code, e.api_message)
    # 10051 = session expired / invalid
    # 10052 = HTTP error from backend
    # 10102 = invalid arguments
```

## 架构

```
User's Phone (LINE app)
    ↕ (scan QR / enter PIN)
LINE Servers (line-chrome-gw.line-apps.com)
    ↕ (JSON REST + X-Hmac signing)
LineChromeClient (this repo)
    ↕ (WASM HMAC via Node.js signer)
lstm.wasm + lstmSandbox.js
```

Chrome 扩展程序内部将 JSON 数据转换为 Thrift 数据格式，然后再进行传输。我们不直接处理 Thrift 二进制数据——所有数据都以 JSON 格式传输。