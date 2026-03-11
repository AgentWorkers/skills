---
name: engagelab-webpush
description: 调用 EngageLab Web Push REST API 可以向浏览器（如 Chrome、Firefox、Safari、Edge 等）发送推送通知和应用程序内消息；管理标签和别名；创建定时任务；按注册 ID 或别名批量发送推送消息；进行分组推送；删除用户；查询统计数据；以及配置回调函数。当用户需要通过 EngageLab 发送推送通知、管理设备标签/别名、安排推送时间、执行批量推送、删除用户、查询推送统计数据，或与 EngageLab Web Push 集成时，可以使用此功能。相关关键词包括：engagelab web push、web push api、browser push、registration_id、tag alias web、scheduled web push、batch web push、web push callback、MTPush web。
---
# EngageLab Web Push API 技能

该技能允许与 EngageLab Web Push REST API（MTPush Web）进行交互。该服务仅支持向网页平台发送推送通知和应用程序内消息，并支持 EngageLab 自定义渠道以及 Chrome、Firefox、Safari、Edge、Opera 等系统渠道。

**功能涵盖：**

1. **创建推送通知**：向单个或多个网页设备发送通知或消息（广播、标签、别名、注册 ID）。
2. **批量单条推送**：按注册 ID 或别名批量推送（每次请求最多 500 条）。
3. **群组推送**：向群组中的所有设备推送通知。
4. **定时任务**：创建、获取、更新或删除定时推送任务（单次推送、定期推送、智能推送）。
5. **标签与别名**：查询/设置/删除设备标签和别名；查询标签数量。
6. **删除用户**：删除用户（注册 ID）及其所有相关数据。
7. **统计信息**：消息生命周期统计（目标设备、已发送消息数、已送达消息数、展示次数、点击次数等）。
8. **回调**：配置回调地址并验证签名。

## 资源

### 脚本
- `webpush_client.py`：Python 客户端类（`EngageLabWebPush`），用于执行创建推送通知、批量推送、查询设备信息、设置/删除标签、管理定时任务以及获取消息详情等操作。支持基本身份验证和错误处理。

### 参考文档
- `error-codes.md`：Web Push API 错误代码及其说明。
- `http-status-code.md`：HTTP 状态码规范。
- `callback-api.md`：回调地址、验证规则及安全相关设置（`X-CALLBACK-ID`、`HMAC-SHA256`）。

**API 文档来源**：`doc/webpush/REST API/`（包括 API 概述、创建推送通知 API、批量单条推送 API、群组推送 API、定时任务 API、标签别名 API、删除用户 API、统计信息 API、回调 API、HTTP 状态码等相关内容）。

## 身份验证

所有 EngageLab Web Push API 调用均使用 **HTTP 基本身份验证**：

- **基础 URL**（根据数据中心选择）：
  - 新加坡：`https://webpushapi-sgp.engagelab.com`
  - 香港：`https://webpushapi-hk.engagelab.com`
- **请求头**：`Authorization: Basic base64(appKey:masterSecret`
- **Content-Type**：`application/json`

**AppKey** 和 **Master Secret** 可在控制台的 **应用程序设置** → **应用程序信息** 中获取。

**群组推送** 使用不同的身份验证方式：`username` = `group-` + `GroupKey`，`password` = **群组密钥**（从群组管理界面获取）。

**示例**（使用 curl）：
```bash
curl -X POST https://webpushapi-sgp.engagelab.com/v4/push \
  -H "Content-Type: application/json" \
  -u "YOUR_APP_KEY:YOUR_MASTER_SECRET" \
  -d '{ "from": "push", "to": "all", "body": { "platform": "web", "notification": { "web": { "alert": "Hello!", "title": "Web Push", "url": "https://example.com" } } } }'
```

如果用户尚未提供凭据，请在生成 API 调用前先获取 **AppKey** 和 **Master Secret**。

## 请求速率限制

- **标准限制**：每个 AppKey 每秒 500 次请求。
- 批量单条推送的请求速率与普通推送 API 共享同一限制（每个目标设备 1 次请求/秒）。

## 快速参考 — 主要 API 端点

| 操作 | 方法 | 路径 |
|---------|--------|------|
| 创建推送通知 | `POST` | `/v4/push` |
| 按注册 ID 批量推送 | `POST` | `/v4/batch/push/regid` |
| 按别名批量推送 | `POST` | `/v4/batch/push/alias` |
| 群组推送 | `POST` | `/v4/grouppush` |
| 创建定时任务 | `POST` | `/v4/schedules` |
| 获取定时任务 | `GET` | `/v4/schedules/{schedule_id}` |
| 更新定时任务 | `PUT` | `/v4/schedules/{schedule_id}` |
| 删除定时任务 | `DELETE` | `/v4/schedules/{schedule_id}` |
| 查询标签数量 | `GET` | `/v4/tags_count` |
| 查询设备信息（标签/别名） | `GET` | `/v4/devices/{registration_id}` |
| 设置设备标签/别名 | `POST` | `/v4/devices/{registration_id}` |
| 删除设备（用户） | `DELETE` | `/v4/devices/{registration_id}` |
| 获取消息统计信息 | `GET` | `/v4/messages/details` （需要提供消息 ID） |

## 创建推送通知（`POST /v4/push`）

向网页设备发送通知或消息。**平台** 仅限于网页（`platform` 参数值为 `web`）。

### 请求结构（示例）

| 字段 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| `from` | string | 否 | 发送者，例如 `"push"` |
| `to` | string 或 object | 是 | 接收者：`all`（广播发送）或包含 `tag`、`tag_and`、`tag_not`、`alias`、`registration_id` 的对象 |
| `body` | object | 是 | 推送内容 |
| `request_id` | string | 否 | 客户端定义的请求 ID（会在响应中返回） |
| `custom_args` | object | 否 | 回调时返回的额外参数 |

### 请求体（`body`）

| 字段 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| `platform` | string | 是 | 必须为 `"web"` |
| `notification` | object | 可选 | 推送内容（包括 `alert`、`title`、`url`、`icon`、`image` 等） |
| `message` | object | 可选 | 应用程序内/自定义消息内容（`msg_content`、`title`、`content_type` 等） |
| `options` | object | 可选 | 配置选项（如 `time_to_live`、`override_msg_id`、`big_push_duration` 等） |

**注意**：`notification` 和 `message` 中必须至少选择一个字段，不能同时使用。

### `notification.web` 字段

| 字段 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| `alert` | string | 是 | 消息内容 |
| `url` | string | 是 | 点击链接 |
| `title` | string | 否 | 消息标题 |
| `icon` | string | 否 | 通知图标（建议尺寸 192×192px；格式为 JPG/PNG/GIF；兼容 Chrome 和 Firefox） |
| `image` | string | 否 | 大图（建议尺寸 360×180px；兼容 Chrome 和 Edge） |
| `extras` | object | 可选 | 附加自定义信息 |

### 配置选项

- `time_to_live`：消息的离线保留时间（以秒为单位，默认 86400 秒，最长 15 天）；0 表示仅在线显示。
- `override_msg_id`：覆盖之前的推送通知（有效期 1 天）。
- `big_push_duration`：控制推送的频率（最多 1440 分钟内最多发送 20 次）。
- `web_buttons`：最多包含 2 个按钮的数组（`id`、`text`、`icon`、`url`）；仅兼容 Chrome 4.8 及更高版本。
- `multi_language`：支持多语言内容/标题。
- `third_party_channel.w3push.distribution`：指定推送渠道的优先级（`first_ospush`、`mtpush`、`secondary_push`、`ospush`）。
- `plan_id`、`cid`：推送计划 ID 和防止重复发送的标识符（每个 AppKey 最多 64 个字符）。

### 推送目标示例

- 广播发送：`to: "all"`
- 使用标签：`to: { "tag1", "tag2" }`
- 使用别名：`to: { "alias1", "alias2" }`
- 使用注册 ID：`to: { "registration_id1", "registration_id2" }`

### 响应（成功时）

```json
{ "request_id": "12345678", "msg_id": "1828256757" }
```

**注意**：通知内容长度限制为 2048 字节；总消息长度限制为 4000 字节。详细信息请参阅 `doc/webpush/REST API/Create Push API.md`。错误代码请参考 `references/error-codes.md`。

## 批量单条推送

- **按注册 ID**：`POST /v4/batch/push/regid`
- **按别名**：`POST /v4/batch/push/alias`

请求体示例：
```json
{
  "requests": [
    {
      "target": "reg_id_or_alias",
      "platform": "web",
      "notification": {
        "web": {
          "alert": "Hello, Web Push!",
          "title": "Web Push Title",
          "url": "https://example.com",
        },
        "message": {
          "msg_content": "Hello, this is the message content.",
          "title": "Message title",
          "content_type": "text",
        },
        "options": {
          "time_to_live": 86400,
          "override_msg_id": "override_msg_id",
        },
      },
      },
    ]
  ]
}
```

**注意**：每次请求最多包含 500 条推送记录；`target` 参数必须唯一。详细信息请参阅 `doc/webpush/REST API/Batch Single Push API.md`。

## 群组推送

请求路径：`POST /v4/grouppush`。请求体结构与创建推送通知相同。身份验证方式同样使用基本身份验证（`Authorization: Basic group-GroupKey GroupMasterSecret`）。群组推送不支持 `override_msg_id` 和 `Schedule` 相关功能。

## 定时任务

- **创建**：`POST /v4/schedules`
- **获取**：`GET /v4/schedules/{schedule_id}`
- **更新**：`PUT /v4/schedules/{schedule_id}`
- **删除**：`DELETE /v4/schedules/{schedule_id}`

**触发类型**：
- **单次推送**：指定具体时间。
- **定期推送**：指定开始时间、结束时间。
- **智能推送**：自动选择最佳推送时间（例如 `now` 或 `yyyy-MM-dd HH:mm:ss`）。

**注意**：最多可创建 1000 个有效的定时任务。详细信息请参阅 `doc/webpush/REST API/Scheduled Tasks API.md`。

## 标签与别名

- **查询标签数量**：`GET /v4tags_count?tags=tag1&tags=tag2&platform=web`
- **查询设备信息**：`GET /v4/devices/{registration_id}`（返回设备的标签和别名信息）。
- **设置设备标签**：`POST /v4/devices/{registration_id}`（示例请求体）：
  ```json
  {
    "tags": {
      "add": ["tag1"],
      "remove": ["tag2"]
    },
    "alias": "alias1"
  }
  ```
**注意**：
- 每个应用最多支持 100,000 个标签；每个标签最多 40 字节；每个设备最多关联 100 个标签；每个设备最多使用 100 个别名；每个应用最多支持 100,000 个别名。详细信息请参阅 `doc/webpush/REST API/Tag Alias API.md`。

## 删除用户

`DELETE /v4/devices/{registration_id}`：异步删除用户及其所有相关数据。删除操作不可恢复，不支持批量删除。

## 统计信息

- **获取消息详情**：`GET /v4/messages/details?message_ids=id1,id2`（最多提供 100 个消息 ID）。返回目标设备、已发送消息数、已送达消息数、展示次数、点击次数等统计信息（按 Chrome、Safari、Firefox、Edge、Opera 等渠道划分）。数据保留时间最长为一个月。详细信息请参阅 `doc/webpush/REST API/Statistics API.md`。

## 回调

请通过 EngageLab 客服配置回调地址。服务器会通过 POST 请求发送包含 `echostr` 的数据；响应时需要返回相同的 `echostr` 值。**安全提示**：使用 `X-CALLBACK-ID` 请求头，并通过 `HMAC-SHA256` 算法验证签名。成功响应时状态码应为 200 或 204。详细信息请参阅 `references/callback-api.md` 和 `doc/webpush/REST API/Callback API.md`。

## 代码生成

当用户需要发送推送通知或使用其他 Web Push API 时，可以生成相应的代码。默认使用 `curl`；用户也可选择使用其他编程语言（如 Python、Node.js、Java、Go 等）。请确保在代码中添加正确的身份验证信息（`YOUR_APP_KEY` 和 `YOUR_MASTER_SECRET`）。

**Python 示例（创建推送通知）**：
```python
import requests

APP_KEY = "YOUR_APP_KEY"
MASTER_SECRET = "YOUR_MASTER_SECRET"
BASE_URL = "https://webpushapi-sgp.engagelab.com"

resp = requests.post(
    f"{BASE_URL}/v4/push",
    auth=(APP_KEY, MASTER_SECRET),
    headers={"Content-Type": "application/json",
    json={
        "from": "push",
        "to": "all",
        "body": {
            "platform": "web",
            "notification": {
                "web": {
                    "alert": "Hello, Web Push!",
                    "title": "Web Push Title",
                    "url": "https://example.com",
                    "extras": {"key": "value"},
                },
            },
            "options": {"time_to_live": 86400},
        },
        "request_id": "req_001",
    },
)
result = resp.json()
if resp.status_code == 200:
    print("msg_id:", result.get("msg_id"))
else:
    print("Error:", result.get("error"))
```