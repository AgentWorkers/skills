---
name: engagelab-apppush
description: 调用 EngageLab App Push 的 REST API，向 Android、iOS 和 HarmonyOS 设备发送推送通知和应用程序内消息；管理设备标签和别名；创建定时任务和推送计划；批量推送消息；撤回已发送的消息；查询推送统计信息；以及配置回调功能。当用户需要通过 EngageLab 发送推送通知、管理设备标签/别名、安排推送任务、使用批量推送或群组推送功能、撤回消息、删除用户信息、查询推送统计数据、验证推送请求、为 OPPO 设备上传图片、使用语音播报功能，或与 EngageLab App Push 进行集成时，可以使用此技能。相关术语包括：engagelab push、app push api、push notification、registration_id、tag alias、scheduled push、push plan、batch push、message recall、push statistics、push callback 和 MTPush。
---
# EngageLab 应用推送 API 技能

此技能支持与 EngageLab 应用推送 REST API（MTPush）进行交互。该服务支持向 Android、iOS 和 HarmonyOS 设备发送推送通知和应用内消息，并支持多供应商渠道（如 FCM、华为、小米、OPPO、vivo、魅族、荣耀等）。

**主要功能包括：**

1. **创建推送**：向单个或多个设备发送通知或消息（广播、标签、别名、注册 ID、细分群体）。
2. **批量单次推送**：按注册 ID 或别名批量推送（每次请求最多 500 条）。
3. **群组推送**：向群组中的所有应用推送消息。
4. **推送计划**：创建/更新/列出推送计划，并按计划查询消息 ID。
5. **定时任务**：创建、获取、更新、删除定时推送任务（单次、定期、智能类型）。
6. **标签与别名**：查询/设置/删除设备标签和别名；查询标签数量。
7. **消息撤回**：在一天内撤回已推送的消息。
8. **删除用户**：删除用户（注册 ID）及其所有相关数据。
9. **统计信息**：消息生命周期统计信息。
10. **回调**：配置 Webhook 并验证签名。
11. **测试推送**：在不发送消息的情况下验证推送请求。
12. **图片 API**：上传 OPPO 图片（大图/小图）。
13. **语音推送**：创建/更新语音广播文件。

## 资源

### 脚本

- `push_client.py`：Python 客户端类（`EngageLabPush`），用于执行创建推送、批量推送、获取/设置/删除设备信息、查询标签数量、撤回消息、验证推送请求、创建/列出推送计划以及查询消息详细信息等操作。支持基本身份验证和错误处理。可作为辅助工具使用，或导入到用户项目中。

### 参考文档

- `error-codes.md`：推送 API 错误代码及其说明。
- `http-status-code.md`：HTTP 状态码规范。
- `callback-api.md`：回调地址、验证机制及安全要求（`X-CALLBACK-ID`、`HMAC-SHA256`）。

**源 API 文档地址**：`doc/apppush/REST API/`（包括创建推送 API、批量单次推送 API、群组推送 API、推送计划 API、定时任务 API、标签别名 API、消息撤回 API、删除用户 API、统计信息 API、回调 API、测试推送 API、图片 API、语音推送 API、REST API 概述、HTTP 状态码等）。

## 身份验证

所有 EngageLab 应用推送 API 调用均使用 **HTTP 基本身份验证**。

- **基础 URL**（根据数据中心选择）：
  - 新加坡：`https://pushapi-sgp.engagelab.com`
  - 美国弗吉尼亚州：`https://pushapi-usva.engagelab.com`
  - 法兰克福：`https://pushapi-defra.engagelab.com`
  - 香港：`https://pushapi-hk.engagelab.com`
- **请求头**：`Authorization: Basic base64(appKey:masterSecret)`
- **Content-Type**：`application/json`（或 `multipart/form-data`，用于图片/语音推送）

**AppKey** 和 **Master Secret** 可在控制台 → 应用设置 → 应用信息中获取。

**群组推送** 使用不同的身份验证方式：`username` = `group-` + `GroupKey`，`password` = 组别密钥（从组管理中获取）。

**示例**（使用 curl）：

```bash
curl -X POST https://pushapi-sgp.engagelab.com/v4/push \
  -H "Content-Type: application/json" \
  -u "YOUR_APP_KEY:YOUR_MASTER_SECRET" \
  -d '{ "from": "push", "to": "all", "body": { "platform": "all", "notification": { "alert": "Hello!" } }'
```

如果用户尚未提供凭证，请在生成 API 调用之前获取 **AppKey** 和 **Master Secret**。

## 请求速率限制

- **标准限制**：每个 AppKey 每秒 500 次请求。
- 批量单次推送的请求速率与普通推送 API 共享同一限制（每个目标设备 1 次请求/秒）。

## 快速参考 — 主要接口

| 操作 | 方法 | 路径 |
|---------|--------|------|
| 创建推送 | `POST` | `/v4/push` |
| 按注册 ID 批量推送 | `POST` | `/v4/batch/push/regid` |
| 按别名批量推送 | `POST` | `/v4/batch/push/alias` |
| 群组推送 | `POST` | `/v4/grouppush` |
| 创建/更新推送计划 | `POST` | `/v4/push_plan` |
| 列出推送计划 | `GET` | `/v4/push_plan/list` |
| 按计划查询消息 ID | `GET` | `/v4/status/plan/msg/` |
| 创建定时任务 | `POST` | `/v4/schedules` |
| 获取定时任务 | `GET` | `/v4/schedules/{schedule_id}` |
| 更新定时任务 | `PUT` | `/v4/schedules/{schedule_id}` |
| 删除定时任务 | `DELETE` | `/v4/schedules/{schedule_id}` |
| 查询标签数量 | `GET` | `/v4/tags_count` |
| 获取设备信息（标签/别名） | `GET` | `/v4/devices/{registration_id}` |
| 设置设备标签/别名 | `POST` | `/v4/devices/{registration_id}` |
| 删除设备 | `DELETE` | `/v4/devices/{registration_id}` |
| 撤回消息 | `DELETE` | `/v4/push/withdraw/{msg_id}` |
| 查看消息统计信息 | `GET` | `/v4/status/detail` |
| 测试推送（验证） | `POST` | `/v4/push/validate` |
| 上传 OPPO 图片 | `POST` | `/v4/image/oppo` |
| 创建/更新语音文件 | `POST` | `/v4/voices` |
| 列出/删除语音文件 | `GET` / `DELETE` | `/v4/voices` |

## 创建推送（`POST /v4/push`）

向单个设备或设备列表发送通知或消息。请求体为 JSON 格式。

### 请求结构（示例）

| 字段 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| `from` | string | 否 | 发送者，例如 `"push"` |
| `to` | string 或 object | 是 | 目标：`all`（广播），或包含 `tag`、`tag_and`、`tag_not`、`alias`、`registration_id`、`live_activity_id`、`seg` 的对象 |
| `body` | object | 是 | 请参见下方说明 |
| `request_id` | string | 否 | 客户端定义的请求 ID，会在响应中返回 |
| `custom_args` | object | 否 | 回调时返回，最大长度 128 个字符 |

### 请求体（详细内容）

| 字段 | 类型 | 是否必填 | 说明 |
|-------|------|----------|-------------|
| `platform` | string 或 array | 是 | `all` 或 `["android","ios","hmos"]` |
| `notification` | object | 可选 | 通知内容（适用于 android、ios、hmos；包括 alert、title、extras 等） |
| `message` | object | 可选 | 应用内/自定义消息（包含 msg_content、title、content_type、extras 等） |
| `live_activity` | object | 可选 | iOS 实时活动信息（适用于 ios；包括 event、content-state、attributes 等） |
| `voip` | object | 可选 | iOS VoIP 信息（键值对形式）；不能与 notification 或 message 同时存在 |
| `options` | object | 否 | 包含 time_to_live、apns_production、apns_collapse_id、big_push_duration、multi_language、third_party_channel、plan_id、cid 等参数 |

*必须至少选择 `notification`、`message`、`live_activity` 或 `voip` 中的一个；某些情况下可以同时使用 `notification` 和 `message`（详见文档）。对于 iOS，需设置 `options.apns_production`（true/false）以指定环境配置。*

### 推送目标示例

- 广播：`"to": "all"`
- 标签（或）：`"to": { "tag": ["Shenzhen","Guangzhou"] }`
- 标签（且）：`"to": { "tag_and": ["female","members"] }`
- 别名：`"to": { "alias": ["user1","user2"] }`
- 注册 ID：`"to": { "registration_id": ["id1","id2"] }`
- 细分群体：`"to": { "seg": { "id": "segid" }`
- 实时活动：`"to": { "live_activity_id": "LiveActivity-1" }`

### 响应（成功情况）

```json
{ "request_id": "12345678", "msg_id": "1828256757" }
```

有关完整参数详情（针对 android/ios/hmos 平台的通知字段、选项、多语言支持、第三方渠道等），请参阅 `doc/apppush/REST API/Create Push API.md`。错误代码请参考 `references/error-codes.md`。

## 批量单次推送

- **按注册 ID**：`POST /v4/batch/push/regid`
- **按别名**：`POST /v4/batch/push/alias`

请求体示例：`{ "requests": [ { "target": "reg_id_or_alias", "platform": "android" | "ios" | "all", "notification": {...}, "message": {...}, "options": {...}, "custom_args": {...} } ]`。每次请求最多 500 条记录；`target` 在批次中必须唯一。响应会返回每个目标设备的结果（消息 ID 或错误信息）。详情请参阅 `doc/apppush/REST API/Batch Single Push API.md`。

## 群组推送

`POST /v4/grouppush`：请求体结构与创建推送相同。身份验证方式使用 `Basic` 认证，需提供 `group-{GroupKey}` 和组别密钥。响应包含 `group_msgid` 和每个应用的消息 ID。`override_msgid` 和 Schedule API 不适用于群组推送。

## 推送计划

- **创建/更新**：`POST /v4/push_plan` — 请求体示例：`{"plan_id": "xxx", "plan_description": "..." }`
- **列出推送计划**：`GET /v4/push_plan/list?page_index=1&page_size=20&send_source=0|1&search_description=xxx`
- **按计划查询消息 ID**：`GET /v4/status/plan/msg/?plan_ids=id1,id2&start_date=yyyy-MM-dd&end_date=yyyy-MM-dd`（有效期为 30 天内）。

在创建推送时，可以使用 `plan_id` 参数将推送任务与特定计划关联。

## 定时任务

- **创建**：`POST /v4/schedules` — 请求体包含 `name`、`enabled`、`trigger`（单次/定期/智能类型）、`push`（内容与创建推送相同）。
- **获取**：`GET /v4/schedules/{schedule_id}`。
- **更新**：`PUT /v4/schedules/{schedule_id}`。
- **删除**：`DELETE /v4/schedules/{schedule_id}`。

**触发类型**：
- **单次**：指定具体时间。
- **定期**：指定开始时间、结束时间。
- **智能**：自动触发（例如 `backup_time: "now"` 或 `yyyy-MM-dd HH:mm:ss`）。

## 标签与别名

- **查询标签数量**：`GET /v4_tags_count?tags=tag1&tags=tag2&platform=android|ios|hmos`（最多支持 1000 个标签）。
- **获取设备信息**：`GET /v4/devices/{registration_id}` — 返回设备的标签和别名信息。
- **设置设备标签/别名**：`POST /v4/devices/{registration_id}` — 请求体示例：`{"tags": { "add": ["t1"], "remove": ["t2"] }, "alias": "alias1" }`。

**限制**：
- 每个应用最多 100,000 个标签。
- 每个标签最多 40 字节。
- 每个设备最多 100 个标签。
- 每个设备最多使用 100,000 个标签。
- 每个设备最多使用 1 个别名（每个别名最多 40 字节）。详情请参阅 `doc/apppush/REST API/Tag Alias API.md`。

## 撤回消息

`DELETE /v4/push/withdraw/{msg_id}` — 在一天内撤回已推送的消息；不支持重复撤回。

## 删除用户

`DELETE /v4/devices/{registration_id}` — 异步删除用户及其所有相关数据（标签、别名、设备信息、时区设置）。无法恢复已删除的用户数据。不支持批量删除。

## 统计信息

- **消息详细信息**：`GET /v4/status/detail?message_ids=id1,id2`（最多查询 100 个消息 ID）。返回目标设备、发送次数、送达次数、展示次数、点击次数等统计信息。数据保留期限为一个月。

其他报告接口的详细信息请参阅 `doc/apppush/REST API/Statistics API.md`。

## 回调

请通过 EngageLab 客服配置回调 URL。验证机制：服务器会发送包含 `echostr` 的 POST 请求；响应时需返回相同的 `echostr` 值。安全要求：使用 `X-CALLBACK-ID` 请求头，并使用 `signature = HMAC-SHA256(secret, timestamp+nonce+username)` 进行签名验证。成功响应时状态码为 200/204。详情请参阅 `references/callback-api.md` 和 `doc/apppush/REST API/Callback API.md`。

## 测试推送

`POST /v4/push/validate` — 请求体与创建推送相同，用于在不发送实际消息的情况下验证请求逻辑。

## 图片 API（OPPO）

`POST /v4/image/oppo` — 请求体示例：`{"big_picture_url": "url", "small_picture_url": "url"}`。返回 `big_picture_id` 和 `small_picture_id`，可用于推送配置（例如第三方渠道）。OPPO 图片格式要求：大图尺寸 984×369 像素，文件大小不超过 1MB；小图尺寸 144×144 像素，文件格式为 PNG/JPG/JPEG。

## 语音推送

- **创建/更新语音文件**：`POST /v4/voices` — 请求体格式为 `multipart/form-data`；参数包括 `language`（en, zh-Hans, zh-Hant）和 `file`（mp3 文件的 zip 文件）。返回 `file_url`。
- **列出语音文件**：`GET /v4/voices`。
- **删除语音文件**：`DELETE /v4/voices?language=en`。

在推送请求体中设置 `optionsVOICE_VALUE` 以指定使用的语音文件。详情请参阅 `doc/apppush/REST API/Push-to-Speech API.md`。

## 代码生成

当用户需要发送推送消息或使用其他推送 API 时，系统会生成可执行的代码。默认使用 `curl`；用户也可选择其他编程语言（如 Python、Node.js、Java、Go）。

**示例代码（Python）**：

```python
import requests

APP_KEY = "YOUR_APP_KEY"
MASTER_SECRET = "YOUR_MASTER_SECRET"
BASE_URL = "https://pushapi-sgp.engagelab.com"

resp = requests.post(
    f"{BASE_URL}/v4/push",
    auth=(APP_KEY, MASTER_SECRET),
    headers={"Content-Type": "application/json"},
    json={
        "from": "push",
        "to": "all",
        "body": {
            "platform": "all",
            "notification": {
                "alert": "Hello, Push!",
                "android": {"alert": "Hi, Android!", "title": "Title"},
                "ios": {"alert": "Hi, iOS!", "sound": "default", "badge": "+1"},
            },
            "options": {"time_to_live": 86400, "apns_production": False},
        },
        "request_id": "req_001",
    },
)
result = resp.json()
if resp.status_code == 200:
    print("消息 ID:", result.get("msg_id"))
else:
    print("错误:", result.get("error"))
```