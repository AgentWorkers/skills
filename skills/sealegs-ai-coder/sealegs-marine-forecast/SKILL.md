---
name: sealegs-marine-forecast
description: 获取全球任何地点的、由人工智能支持的海洋天气预报
homepage: https://developer.sealegs.ai
metadata: {"openclaw": {"requires": {"env": ["SEALEGS_API_KEY"], "bins": ["curl"]}, "primaryEnv": "SEALEGS_API_KEY"}, "emoji": "⛵", "tags": ["weather", "marine", "forecast", "boating", "sailing", "ocean", "waves", "wind"]}
---

# SeaLegs AI 海洋天气预报 API

该 API 可为全球任何地点提供基于人工智能的海洋天气预报，包括风速、波高、能见度以及降水情况，并附带“安全”（GO/CAUTION/NO-GO）分类提示。

## 主要功能

- **即时预报（SpotCast）**：为全球任意坐标位置生成海洋天气预报。
- **人工智能安全分析**：为每一天提供“安全”/“谨慎”/“不建议”（GO/CAUTION/NO-GO）的分类提示。
- **针对特定船只类型**：根据船只类型和大小提供定制化的建议。
- **多语言支持**：支持英语、西班牙语、法语、葡萄牙语、意大利语和日语。

## 设置流程

### 1. 获取 API 密钥

1. 在 [https://developer.sealegs.ai](https://developer.sealegs.ai) 注册账户，您将获得 **10 个免费信用点** 用于开始使用服务。
2. 从您的仪表板生成 API 密钥。
3. 需要更多信用点？随时可以购买（10 美元 = 200 天的预报服务）。

### 2. 配置 OpenClaw

将以下代码添加到您的 OpenClaw 配置中：

```json5
{
  skills: {
    entries: {
      "sealegs-marine-forecast": {
        enabled: true,
        apiKey: "sk_live_your_key_here"
      }
    }
  }
}
```

或者设置环境变量：

```bash
export SEALEGS_API_KEY=sk_live_your_key_here
```

### 3. 安装该服务

```bash
clawhub install sealegs-marine-forecast
```

## 使用示例

```jsonc
// Miami, FL
POST /v3/spotcast
{
  "latitude": 25.7617,
  "longitude": -80.1918,
  "start_date": "2026-02-10T00:00:00Z",
  "num_days": 2,
  "vessel_info": {"type": "sailboat", "length_ft": 35}  // optional
}
```

**示例响应：**
```json
{
  "id": "spc_FrZdSAs6T3cxbXiPtNZvxu",
  "coordinates": {
    "latitude": 25.7617,
    "longitude": -80.1918
  },
  "forecast_period": {
    "start_date": "2026-02-10T00:00:00-05:00",
    "end_date": "2026-02-11T23:59:59-05:00",
    "num_days": "2"
  },
  "trip_duration_hours": "12",
  "metadata": {
    "location_name": "Miami Marina"
  },
  "latest_forecast": {
    "status": "completed",
    "ai_analysis": {
      "summary": "Ideal conditions both days with light winds",
      "daily_classifications": [
        {
          "date": "2026-02-10",
          "classification": "GO",
          "short_summary": "Outstanding conditions all day with light winds under 7kt and calm 1.1-1.6ft seas. Best window is morning 5:00 AM-12:00 PM with nearly calm 1-4kt northwest winds and comfortable 1.4ft seas at 11-second periods.",
          "summary": "Outstanding sailing conditions throughout Monday with exceptionally light winds and calm seas. Morning hours offer the best window with nearly calm 1-4kt northwest winds and comfortable 1.4ft seas at 11-second periods from the northeast."
        },
        {
          "date": "2026-02-11",
          "classification": "GO",
          "short_summary": "Exceptional conditions with very light winds 1-6kt and minimal 1.2-1.3ft seas all day. Best window 9:00 AM-1:00 PM offers glassy conditions with 1-3kt winds and 1.2ft seas at 11-second periods.",
          "summary": "Exceptional boating conditions on Tuesday with very light winds and minimal seas throughout the day. Morning through midday provides ideal glassy conditions with 1-3kt east-southeast winds and 1.2ft seas at 10-11 second periods from the northeast."
        }
      ]
    }
  }
}
```

## API 端点

| 操作          | 端点            | 费用      |
|-----------------|-----------------|-----------|
| 创建预报        | POST /v3/spotcast       | 1 信用点/天    |
| 获取预报        | GET /v3/spotcast/{id}     | 免费       |
| 检查状态        | GET /v3/spotcast/{id}/status   | 免费       |
| 更新预报        | POST /v3/spotcast/{id}/refresh | 1 信用点/天    |
| 列出所有预报      | GET /v3/spotcast/{id}/forecasts | 免费       |
| 获取特定预报      | GET /v3/spotcast/{id}/forecast/{forecast_id} | 免费       |
| 列出所有即时预报    | GET /v3/spotcasts     | 免费       |
| 查看账户余额      | GET /v3/account/balance    | 免费       |

## 使用的天气数据

- 风速、阵风速度和方向
- 波高、周期和方向
- 能见度及雾概率
- 降水概率和强度
- 空气和海水温度

## 认证要求

所有请求都必须包含以下认证信息：
```
Authorization: Bearer $SEALEGS_API_KEY
Content-Type: application/json
```

## 速率限制

- 标准 tier：每分钟 60 次请求。
- 所有响应中都会包含以下速率限制头部信息：`X-RateLimit-Limit`、`X-RateLimit-Remaining`、`X-RateLimit-Reset`。

## 计费规则

- 每天预报服务费用为 1 信用点（3 天的预报服务需 3 个信用点）。
- 获取预报的请求是免费的。
- 更新预报的请求费用为 1 信用点/天。

---

# 即时预报（SpotCast）

即时预报功能可为特定坐标位置生成基于人工智能的海洋天气预报。

## 创建即时预报

**POST 请求**：`https://api.sealegs.ai/v3/spotcast`

此请求用于创建新的预报。处理过程是异步的（通常需要 30-60 秒）。

**必填参数：**
- `latitude`（数字）：-90 至 90
- `longitude`（数字）：-180 至 180
- `start_date`（字符串）：ISO 8601 格式（例如：“2025-12-05T00:00:00Z”）
- `num_days`（整数）：1-5

**可选参数：**
- `webhook_url`（字符串）：用于接收完成通知的 HTTPS 端点
- `metadata`（对象）：自定义的键值对
- `trip_duration_hours`（整数）：行程时长（以小时为单位）
- `preferences.language`（字符串）：语言选择（en, es, fr, pt, it, ja，默认：en）
- `preferences.distance_units`（字符串）：距离单位（nm, mi, km，默认：nm）
- `preferences.speed_units`（字符串）：速度单位（kts, mph, ms，默认：kts）
- `vessel_info.type`（字符串）：船只类型（powerBoat, sailboat, pwc, yacht, catamaran）
- `vessel_info.length_ft`（整数）：船只长度（以英尺为单位）

**示例请求：**
```bash
curl -X POST https://api.sealegs.ai/v3/spotcast \
  -H "Authorization: Bearer $SEALEGS_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "latitude": 25.7617,
    "longitude": -80.1918,
    "start_date": "2025-12-05T00:00:00Z",
    "num_days": 2,
    "vessel_info": {"type": "sailboat", "length_ft": 35}
  }'
```

**响应（202 Accepted）：**
```json
{
  "id": "spc_abc123xyz",
  "forecast_id": "fcst_xyz789",
  "status": "processing",
  "created_at": "2025-12-01T10:30:00Z",
  "estimated_completion_seconds": 45,
  "credits_charged": 2,
  "credits_remaining": 98,
  "links": {
    "self": "https://api.sealegs.ai/v3/spotcast/spc_abc123xyz",
    "forecast": "https://api.sealegs.ai/v3/spotcast/spc_abc123xyz/forecast/fcst_xyz789",
    "status": "https://api.sealegs.ai/v3/spotcast/spc_abc123xyz/status"
  }
}
```

## 检查即时预报的状态

**GET 请求**：`https://api.sealegs.ai/v3/spotcast/{id}/status`

持续查询此端点，直到状态变为“completed”或“failed”。建议的查询间隔为 10-15 秒。

**状态值：**
- `pending`：正在排队处理（无 `progress` 字段）
- `processing`：正在生成预报（包含 `progress` 字段）
- `completed`：预报已生成（`progress` 字段值为 100%）
- `failed`：处理过程中出现错误

**处理阶段**（仅当状态为 `processing` 或 `completed` 时显示）：
- fetching_weather
- processing_data
- ai_analysis
- completing
- completed（100%）

**示例请求：**
```bash
curl https://api.sealegs.ai/v3/spotcast/spc_abc123xyz/status \
  -H "Authorization: Bearer $SEALEGS_API_KEY"
```

**响应（pending）：**
```json
{
  "id": "spc_abc123xyz",
  "forecast_id": "fcst_xyz789",
  "status": "pending",
  "created_at": "2025-12-01T10:30:00Z"
}
```

**响应（processing）：**
```json
{
  "id": "spc_abc123xyz",
  "forecast_id": "fcst_xyz789",
  "status": "processing",
  "created_at": "2025-12-01T10:30:00Z",
  "progress": {
    "stage": "ai_analysis",
    "percentage": 75
  }
}
```

**响应（completed）：**
```json
{
  "id": "spc_abc123xyz",
  "forecast_id": "fcst_xyz789",
  "status": "completed",
  "created_at": "2025-12-01T10:30:00Z",
  "completed_at": "2025-12-01T10:30:45Z",
  "progress": {
    "stage": "completed",
    "percentage": 100
  }
}
```

## 获取即时预报

**GET 请求**：`https://api.sealegs.ai/v3/spotcast/{id}`

获取已生成的预报及其人工智能分析结果。

**示例请求：**
```bash
curl https://api.sealegs.ai/v3/spotcast/spc_abc123xyz \
  -H "Authorization: Bearer $SEALEGS_API_KEY"
```

**响应（200 OK）：**
```json
{
  "id": "spc_abc123xyz",
  "created_at": "2025-12-01T10:30:00Z",
  "coordinates": {
    "latitude": 25.7617,
    "longitude": -80.1918
  },
  "forecast_period": {
    "start_date": "2025-12-05T00:00:00Z",
    "end_date": "2025-12-06T00:00:00Z",
    "num_days": 2
  },
  "trip_duration_hours": 12,
  "forecast_count": 1,
  "metadata": {
    "location_name": "Miami Marina"
  },
  "latest_forecast": {
    "forecast_id": "fcst_xyz789",
    "status": "completed",
    "created_at": "2025-12-01T10:30:00Z",
    "completed_at": "2025-12-01T10:30:45Z",
    "ai_analysis": {
      "summary": "Excellent conditions expected. Light winds 8-12kt from the NE with calm 1-2ft seas.",
      "daily_classifications": [
        {
          "date": "2025-12-05",
          "classification": "GO",
          "summary": "Light winds 8-12kt from NE. Seas 1-2ft. Visibility excellent at 10+ nm. No precipitation expected."
        },
        {
          "date": "2025-12-06",
          "classification": "CAUTION",
          "summary": "Winds increasing to 15-20kt. Seas building to 3-4ft by afternoon. Morning departure recommended."
        }
      ]
    }
  }
}
```

## 更新即时预报

**POST 请求**：`https://api.sealegs.ai/v3/spotcast/{id}/refresh`

使用最新天气数据更新现有预报。费用为 1 信用点/天。

**可选请求体：**
- `webhook_url`（字符串）：用于覆盖此更新的 webhook 地址

**示例请求：**
```bash
curl -X POST https://api.sealegs.ai/v3/spotcast/spc_abc123xyz/refresh \
  -H "Authorization: Bearer $SEALEGS_API_KEY"
```

**响应（202 Accepted）：**
```json
{
  "id": "spc_abc123xyz",
  "forecast_id": "fcst_newxyz789",
  "status": "processing",
  "created_at": "2025-12-02T08:00:00Z",
  "links": {
    "self": "https://api.sealegs.ai/v3/spotcast/spc_abc123xyz",
    "status": "https://api.sealegs.ai/v3/spotcast/spc_abc123xyz/status"
  }
}
```

## 列出所有即时预报

**GET 请求**：`https://api.sealegs.ai/v3/spotcast/{id}/forecasts`

列出该即时预报的所有预报，按创建时间排序（最新条目在前）。每次创建或更新即时预报时，都会生成新的预报。

**查询参数：**
- `limit`（整数）：返回的结果数量（默认：10）

**示例请求：**
```bash
curl "https://api.sealegs.ai/v3/spotcast/spc_abc123xyz/forecasts?limit=5" \
  -H "Authorization: Bearer $SEALEGS_API_KEY"
```

**响应（200 OK）：**
```json
{
  "spotcast_id": "spc_abc123xyz",
  "data": [
    {
      "forecast_id": "fcst_newxyz789",
      "status": "completed",
      "created_at": "2025-12-02T08:00:00Z",
      "completed_at": "2025-12-02T08:00:42Z"
    },
    {
      "forecast_id": "fcst_xyz789",
      "status": "completed",
      "created_at": "2025-12-01T10:30:00Z",
      "completed_at": "2025-12-01T10:30:45Z"
    }
  ],
  "has_more": false
}
```

## 获取特定预报

**GET 请求**：`https://api.sealegs.ai/v3/spotcast/{id}/forecast/{forecast_id}`

获取包含人工智能分析结果的特定预报。此接口可用于访问即时预报历史记录中的任意一条预报，而不仅仅是最新的一条。

**示例请求：**
```bash
curl "https://api.sealegs.ai/v3/spotcast/spc_abc123xyz/forecast/fcst_xyz789" \
  -H "Authorization: Bearer $SEALEGS_API_KEY"
```

**响应（200 OK）：**
```json
{
  "forecast_id": "fcst_xyz789",
  "spotcast_id": "spc_abc123xyz",
  "status": "completed",
  "created_at": "2025-12-01T10:30:00Z",
  "completed_at": "2025-12-01T10:30:45Z",
  "forecast_period": {
    "start_date": "2025-12-05T00:00:00Z",
    "num_days": 2
  },
  "ai_analysis": {
    "summary": "Excellent conditions expected. Light winds 8-12kt from the NE with calm 1-2ft seas.",
    "daily_classifications": [
      {
        "date": "2025-12-05",
        "classification": "GO",
        "summary": "Light winds and calm seas throughout the day."
      },
      {
        "date": "2025-12-06",
        "classification": "CAUTION",
        "summary": "Improving conditions with best windows in the afternoon."
      }
    ]
  }
}
```

**响应（200 OK - 处理中）：**
```json
{
  "forecast_id": "fcst_xyz789",
  "spotcast_id": "spc_abc123xyz",
  "status": "processing",
  "created_at": "2025-12-01T10:30:00Z",
  "forecast_period": {
    "start_date": "2025-12-05T00:00:00Z",
    "num_days": 2
  },
  "progress": {
    "stage": "analyzing",
    "percentage": 65
  }
}
```

**响应（200 OK - 失败）：**
```json
{
  "forecast_id": "fcst_xyz789",
  "spotcast_id": "spc_abc123xyz",
  "status": "failed",
  "created_at": "2025-12-01T10:30:00Z",
  "forecast_period": {
    "start_date": "2025-12-05T00:00:00Z",
    "num_days": 2
  },
  "error": "Processing failed"
}
```

## 列出所有即时预报

**GET 请求**：`https://api.sealegs.ai/v3/spotcasts`

列出您账户下的所有即时预报。

**查询参数：**
- `limit`（整数）：返回的结果数量（默认：20）
- `after`（字符串）：分页参数

**示例请求：**
```bash
curl "https://api.sealegs.ai/v3/spotcasts?limit=10" \
  -H "Authorization: Bearer $SEALEGS_API_KEY"
```

**响应（200 OK）：**
```json
{
  "data": [
    {
      "id": "spc_abc123xyz",
      "created_at": "2025-12-01T10:30:00Z",
      "coordinates": {
        "latitude": 25.7617,
        "longitude": -80.1918
      },
      "start_date": "2025-12-05T00:00:00-05:00",
      "end_date": "2025-12-06T23:59:59-05:00",
      "num_days": 2,
      "latest_forecast": {
        "forecast_id": "fcst_xyz789",
        "status": "completed"
      }
    }
  ],
  "has_more": true,
  "next_cursor": "spc_def456"
}
```

---

# 账户信息

## 查看账户余额

**GET 请求**：`https://api.sealegs.ai/v3/account/balance`

查看您的当前信用点余额和使用情况。

**示例请求：**
```bash
curl https://api.sealegs.ai/v3/account/balance \
  -H "Authorization: Bearer $SEALEGS_API_KEY"
```

**响应（200 OK）：**
```json
{
  "credit_balance": 100,
  "total_credits_purchased": 200,
  "total_credits_used": 100,
  "purchase_url": "https://developers.sealegs.ai/dashboard/billing"
}
```

---

# Webhook

在创建或更新即时预报时，如果您提供了 `webhook_url`，SeaLegs 会在处理完成或失败时向该 URL 发送 POST 请求。

## Webhook 头部信息

```
Content-Type: application/json
X-SeaLegs-Event: spotcast.forecast.completed
X-SeaLegs-Signature: sha256=abc123...
X-SeaLegs-Delivery-ID: whk_abc123xyz
X-SeaLegs-Timestamp: 1733045400
User-Agent: SeaLegs-Webhooks/1.0
```

## 验证签名

每个 Webhook 请求的 `X-SeaLegs-Signature` 头部都会包含一个 HMAC-SHA256 签名。您可以在开发者仪表板中获取 Webhook 的密钥。在处理请求数据之前，请务必验证签名。

**Python 示例：**
```python
import hmac
import hashlib

def verify_webhook(payload: bytes, signature: str, secret: str) -> bool:
    expected = hmac.new(secret.encode(), payload, hashlib.sha256).hexdigest()
    return hmac.compare_digest(f"sha256={expected}", signature)
```

**JavaScript 示例：**
```javascript
const crypto = require('crypto');

function verifyWebhook(payload, signature, secret) {
  const expected = crypto.createHmac('sha256', secret).update(payload).digest('hex');
  return crypto.timingSafeEqual(
    Buffer.from(`sha256=${expected}`),
    Buffer.from(signature)
  );
}
```

## 成功处理后的响应

当人工智能分析成功完成时，响应中会包含 `summary` 字段。如果您在最初的 `POST` 请求中提供了 `metadata`，则 `metadata` 对象也会被原样返回。

## 处理失败时的响应

**失败响应**：

**重试策略**

失败请求会尝试重传最多 4 次：分别在 5 分钟、30 分钟、2 小时和 24 小时后重新尝试。

---

# 结果解读

**每日安全分类**

每天的预报都会附带一个安全分类提示：

| 分类            | 含义                          |
|-----------------|------------------------------|
| **GO**           | 船只类型可安全航行                   |
| **CAUTION**       | 需谨慎操作；环境可能具有挑战性             |
| **NO-GO**         | 不建议该船只类型航行                   |

当提供了 `vessel_info` 时，分类会根据船只类型和大小进行调整。

## 分析的天气变量

- **风**：风速（kts）、阵风速度、风向
- **波**：波高（ft）、波周期（秒）、波方向、涌浪情况
- **能见度**：能见距离（nm）、雾概率
- **降水**：降水概率（%）、降水强度
- **温度**：空气温度和海水温度

## 针对特定船只类型的调整

- **PWC/水上摩托艇**：更严格的波高限制
- **帆船**：针对风速的优化建议
- **大型游艇**：对波浪条件的容忍度更高
- **小型动力艇**：更平衡的风速/波浪阈值

---

# 错误处理

## 错误响应格式

**错误代码及其含义**

| 错误代码            | 描述                          |
|-----------------|-----------------------------------------|
| 200              | 请求成功                         |
| 201              | 资源已创建                        |
| 202              | 异步处理已开始                     |
| 400              | 请求参数错误                       |
| 401              | 未提供有效的 API 密钥                   |
| 402              | 需要购买更多信用点                     |
| 403              | 账户未验证或已被暂停                   |
| 404              | 资源未找到                       |
| 429              | 请求次数超出限制                     |
| 500              | 服务器错误                         |

## 错误代码及其详细说明

### 认证相关错误（401-403）

| 错误代码            | 描述                          |
|-----------------|-----------------------------------------|
| `missing_api_key`     | 请求中未提供 API 密钥                 |
| `invalid_api_key`     | 提供的 API 密钥无效                 |
| `key_revoked`     | API 密钥已被吊销                     |

### 授权相关错误（403）

| 错误代码            | 描述                          |
|-----------------|-----------------------------------------|
| `account_not_verified`     | 开发者账户未验证                   |
| `account_suspended`     | 开发者账户已被暂停                     |

### 计费相关错误（402）

| 错误代码            | 描述                          |
|-----------------|-----------------------------------------|
| `insufficient_balance`     | 信用点不足                     | （响应中包含 `current_balance`、`required_credits`、`purchase_url`） |
|                                 |

### 验证相关错误（400）

| 错误代码            | 描述                          |
|-----------------|-----------------------------------------|
| `invalid_coordinates`     | 坐标超出有效范围                     |
| `invalid_date_format`     | 日期格式不符合 ISO 8601 标准                 |
| `invalid_webhook_url`     | 提供的 URL 不是有效的 HTTPS 地址             |
| `invalid_preferences`     | 预设参数格式无效                     |
| `invalid_language`     | 不支持的语言                         |
| `invalid_distance_units`     | 距离单位无效                         |
| `invalid_speed_units`     | 速度单位无效                         |
| `invalid_json`     | 请求体不是有效的 JSON 格式                   |

### 资源未找到（404）

| 错误代码            | 描述                          |
|-----------------|-----------------------------------------|
| `spotcast_not_found`     | 指定的即时预报未找到                   |
| `forecast_not_found`     | 指定的预报未找到                     |

### 速率限制相关错误（429）

| 错误代码            | 描述                          |
|-----------------|-----------------------------------------|
| `rate_limit_exceeded`     | 请求次数超出限制                     | （响应中包含重试间隔时间）                 |

### 服务器错误（500）

| 错误代码            | 描述                          |
|-----------------|-----------------------------------------|
| `internal_error`     | 发生内部错误                     |
| `creation_failed`     | 创建即时预报失败                     |
| `retrieval_failed`     | 获取资源失败                     |

---

# 常见操作流程

## 获取海洋天气预报

1. 为指定坐标和日期创建即时预报。
2. 持续查询状态端点，直到预报状态变为“completed”。
3. 获取包含人工智能分析结果的完整预报。
4. 向用户展示“安全”/“谨慎”/“不建议”的分类提示。

## 出行前检查天气情况

1. 为出行坐标和日期创建即时预报。
2. 提供船只信息以获取定制化的建议。
3. 查看每天的安全分类提示。
4. 查看人工智能分析结果，了解可能存在的风险。

## 相关链接

- [开发者门户](https://developer.sealegs.ai)
- [API 文档](https://developer.sealegs.ai/docs/)
- [SeaLegs 应用程序](https://sealegs.ai)

## 许可证

本服务采用 MIT 许可协议。