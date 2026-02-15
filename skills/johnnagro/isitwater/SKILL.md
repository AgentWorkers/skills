---
name: isitwater
description: 使用 `IsItWater` API 来检查地理坐标是否位于水域或陆地上。
metadata: {"openclaw": {"primaryEnv": "ISITWATER_API_KEY", "emoji": "🌊", "homepage": "https://isitwater.com"}}
---

# IsItWater

使用 IsItWater API 判断给定的经纬度坐标是否位于水域上。

## 准备工作

在进行 API 调用之前，请确认用户是否已配置 API 密钥：

1. 检查环境变量 `ISITWATER_API_KEY` 是否已设置。
2. 如果未设置：
   - 通知用户：“您需要一个 IsItWater API 密钥。您可以在 [https://isitwater.com](https://isitwater.com) 获取密钥。”
   - 提供帮助用户使用浏览器工具注册的指引：导航至 [https://isitwater.com](https://isitwater.com)，创建账户并在控制面板中生成 API 密钥。
   - 用户获取密钥后，指导他们将其配置在 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "isitwater": {
        "apiKey": "YOUR_API_KEY_HERE"
      }
    }
  }
}
```

   或者，用户也可以直接导出环境变量：`export ISITWATER_API_KEY=YOUR_API_KEY_HERE`

3. 获取到密钥后，即可继续进行下面的 API 调用。

## 查找水域位置

判断坐标是位于水域还是陆地上。

**端点：** `GET https://api.isitwater.com/v1/locations/water`

**请求头：**

- `Authorization: Bearer $ISITWATER_API_KEY`

**请求参数：**

| 参数          | 类型    | 是否必填 | 描述                                      |
|---------------|--------|---------|-----------------------------------------|
| `lat`          | 数字     | 是       | 纬度，范围在 -90 到 90 之间                         |
| `lon`          | 数字     | 是       | 经度，范围在 -180 到 180 之间                         |

**示例 curl 请求：**

```bash
curl -s "https://api.isitwater.com/v1/locations/water?lat=41.7658&lon=-72.6734" \
  -H "Authorization: Bearer $ISITWATER_API_KEY"
```

**示例响应（陆地）：**

```json
{
  "request_id": "abc123",
  "water": false,
  "features": ["earth"],
  "latitude": "41.7658",
  "longitude": "-72.6734"
}
```

**示例响应（水域）：**

```json
{
  "request_id": "def456",
  "water": true,
  "features": ["earth", "ocean"],
  "latitude": "36.0",
  "longitude": "-30.0"
}
```

**响应字段：**

| 字段           | 类型     | 描述                                      |
|-----------------|---------|-----------------------------------------|
| `request_id`     | 字符串   | 请求的唯一标识符                         |
| `water`        | 布尔值   | 如果坐标位于水域，则返回 `true`，否则返回 `false`           |
| `features`      | 字符串数组 | 该点的地理特征，例如 `earth`（陆地）、`ocean`（海洋）、`lake`（湖泊）、`river`（河流）、`glacier`（冰川）、`nature_reserve`（自然保护区） |
| `latitude`     | 字符串   | 被查询的纬度                               |
| `longitude`    | 字符串   | 被查询的经度                               |

**费用：** 每次查询消耗 1 个信用点。

## 账户信息

查看用户的账户详情和剩余信用点数。

**端点：** `GET https://api.isitwater.com/v1/accounts/me`

**请求头：**

- `Authorization: Bearer $ISITWATER_API_KEY`

**示例 curl 请求：**

```bash
curl -s "https://api.isitwater.com/v1/accounts/me" \
  -H "Authorization: Bearer $ISITWATER_API_KEY"
```

**响应字段：**

| 字段            | 类型     | 描述                                      |
|-----------------|---------|-----------------------------------------|
| `id`            | 字符串     | 账户标识符                                 |
| `name`          | 字符串     | 账户名称                                   |
| `balance`        | 数字     | 剩余信用点数                               |
| `auto_recharge_enabled` | 布尔值   | 是否启用自动充值                             |

**费用：** 免费（不消耗信用点）。

## 错误处理

| 状态码       | 含义         | 描述                                      |
|--------------|-------------|-----------------------------------------|
| 200          | 成功        | 请求成功                                   |
| 400          | 请求错误     | 经纬度值无效                               |
| 401          | 未经授权     | 缺少或无效的 API 密钥                         |
| 402          | 需要支付     | 账户剩余信用点数为零                             |

错误响应会返回 JSON 格式的错误信息：

```json
{
  "error": "description of the problem"
}
```

## 提示：

- 每次查询水域位置会消耗 1 个信用点。在多次查询之前，请使用账户信息端点查看用户的剩余信用点数。
- 如果用户提供的是地点名称而非坐标（例如：“撒哈拉沙漠是水域吗？”），请先对该地点进行地理编码以获取经纬度，然后再调用水域查询端点。
- 对于同一个地点，`features` 数组中可能包含多个重叠的地理特征（例如，一个地点可能同时被标记为 `lake`（湖泊）和 `nature_reserve`（自然保护区）