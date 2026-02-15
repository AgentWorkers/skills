---
name: thingsboard
description: 通过 ThingsBoard 的 REST API 来管理 ThingsBoard 设备、仪表板、遥测数据以及用户。
homepage: https://thingsboard.io
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["jq","curl"],"env":["TB_URL","TB_USERNAME","TB_PASSWORD"]}}}
---

# ThingsBoard 技能

用于管理 ThingsBoard IoT 平台的资源，包括设备、仪表板、遥测数据以及用户。

## 设置

1. 在 `credentials.json` 中配置您的 ThingsBoard 服务器：
   ```json
   [
     {
       "name": "Server Thingsboard",
       "url": "http://localhost:8080",
       "account": [
         {
           "sysadmin": {
             "email": "sysadmin@thingsboard.org",
             "password": "sysadmin"
           }
         },
         {
           "tenant": {
             "email": "tenant@thingsboard.org",
             "password": "tenant"
           }
         }
       ]
     }
   ]
   ```

2. 设置环境变量：
   ```bash
   export TB_URL="http://localhost:8080"
   export TB_USERNAME="tenant@thingsboard.org"
   export TB_PASSWORD="tenant"
   ```

3. 获取认证令牌：
   ```bash
   export TB_TOKEN=$(curl -s -X POST "$TB_URL/api/auth/login" \
     -H "Content-Type: application/json" \
     -d "{\"username\":\"$TB_USERNAME\",\"password\":\"$TB_PASSWORD\"}" | jq -r '.token')
   ```

## 使用方法

所有命令均通过 `curl` 与 ThingsBoard REST API 进行交互。

### 认证

**登录并获取令牌：**
```bash
curl -s -X POST "$TB_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$TB_USERNAME\",\"password\":\"$TB_PASSWORD\"}" | jq -r '.token'
```

**刷新令牌（令牌过期时）：**
```bash
curl -s -X POST "$TB_URL/api/auth/token" \
  -H "Content-Type: application/json" \
  -d "{\"refreshToken\":\"$TB_REFRESH_TOKEN\"}" | jq -r '.token'
```

**获取当前用户信息：**
```bash
curl -s "$TB_URL/api/auth/user" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq
```

### 设备管理

**列出所有租户设备：**
```bash
curl -s "$TB_URL/api/tenant/devices?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq '.data[] | {name, id: .id.id, type}'
```

**按 ID 获取设备：**
```bash
curl -s "$TB_URL/api/device/{deviceId}" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq
```

**获取设备凭据：**
```bash
curl -s "$TB_URL/api/device/{deviceId}/credentials" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq
```

### 遥测与属性

**获取遥测键：**
```bash
curl -s "$TB_URL/api/plugins/telemetry/DEVICE/{deviceId}/keys/timeseries" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq
```

**获取最新的遥测数据：**
```bash
curl -s "$TB_URL/api/plugins/telemetry/DEVICE/{deviceId}/values/timeseries?keys=temperature,humidity" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq
```

**按时间范围获取时间序列数据：**
```bash
START_TS=$(($(date +%s)*1000 - 3600000))  # 1 hour ago
END_TS=$(($(date +%s)*1000))              # now
curl -s "$TB_URL/api/plugins/telemetry/DEVICE/{deviceId}/values/timeseries?keys=temperature&startTs=$START_TS&endTs=$END_TS&limit=100" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq
```

**获取属性键：**
```bash
# Client scope
curl -s "$TB_URL/api/plugins/telemetry/DEVICE/{deviceId}/keys/attributes/CLIENT_SCOPE" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq

# Shared scope
curl -s "$TB_URL/api/plugins/telemetry/DEVICE/{deviceId}/keys/attributes/SHARED_SCOPE" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq

# Server scope
curl -s "$TB_URL/api/plugins/telemetry/DEVICE/{deviceId}/keys/attributes/SERVER_SCOPE" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq
```

**按范围获取属性：**
```bash
curl -s "$TB_URL/api/plugins/telemetry/DEVICE/{deviceId}/values/attributes/CLIENT_SCOPE?keys=attribute1,attribute2" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq
```

**保存设备属性：**
```bash
curl -s -X POST "$TB_URL/api/plugins/telemetry/DEVICE/{deviceId}/attributes/SERVER_SCOPE" \
  -H "X-Authorization: Bearer $TB_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"attribute1":"value1","attribute2":"value2"}' | jq
```

**删除时间序列键：**
```bash
curl -s -X DELETE "$TB_URL/api/plugins/telemetry/DEVICE/{deviceId}/timeseries/delete?keys=oldKey1,oldKey2&deleteAllDataForKeys=true" \
  -H "X-Authorization: Bearer $TB_TOKEN"
```

### 仪表板管理

**列出所有仪表板：**
```bash
curl -s "$TB_URL/api/tenant/dashboards?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq '.data[] | {name, id: .id.id}'
```

**获取仪表板信息：**
```bash
curl -s "$TB_URL/api/dashboard/{dashboardId}" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq
```

**将仪表板设置为公开：**
```bash
curl -s -X POST "$TB_URL/api/customer/public/dashboard/{dashboardId}" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq
```

**获取公开仪表板信息（无需认证）：**
```bash
curl -s "$TB_URL/api/dashboard/info/{publicDashboardId}" | jq
```

**移除公开访问权限：**
```bash
curl -s -X DELETE "$TB_URL/api/customer/public/dashboard/{dashboardId}" \
  -H "X-Authorization: Bearer $TB_TOKEN"
```

### 用户管理

**列出租户用户：**
```bash
curl -s "$TB_URL/api/tenant/users?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq '.data[] | {email, firstName, lastName, id: .id.id}'
```

**列出客户：**
```bash
curl -s "$TB_URL/api/customers?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq '.data[] | {title, id: .id.id}'
```

**获取客户用户：**
```bash
curl -s "$TB_URL/api/customer/{customerId}/users?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq '.data[]'
```

### 资产

**列出所有资产：**
```bash
curl -s "$TB_URL/api/tenant/assets?pageSize=100&page=0" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq '.data[] | {name, type, id: .id.id}'
```

**按 ID 获取资产：**
```bash
curl -s "$TB_URL/api/asset/{assetId}" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq
```

## 注意事项

- **认证**：JWT 令牌在配置的时间段后失效（默认为 2 小时）。收到 401 错误时请重新认证。
- **设备/仪表板 ID**：实体 ID 的格式为 `{entityType: "DEVICE", id: "uuid"}`。在 API 调用中使用 `id` 字段。
- **分页**：大多数列表端点支持 `pageSize` 和 `page` 参数（默认每页 100 项，最大 1000 项）。
- **属性范围**：
  - `CLIENT_SCOPE`：客户端属性（由设备设置）
  - `SHARED_SCOPE`：在服务器和设备之间共享
  - `SERVER_SCOPE`：仅限服务器端使用（设备不可见）
- **时间戳**：使用自纪元以来的毫秒数作为 `startTs` 和 `endTs` 参数。
- **速率限制**：请查看 ThingsBoard 服务器的配置以了解 API 的速率限制。
- **HTTPS**：在生产环境中，请使用 HTTPS URL（例如：`https://demo.thingsboard.io`）。

## 示例

```bash
# Complete workflow: Login, list devices, get telemetry
export TB_URL="http://localhost:8080"
export TB_USERNAME="tenant@thingsboard.org"
export TB_PASSWORD="tenant"

# Get token
export TB_TOKEN=$(curl -s -X POST "$TB_URL/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"$TB_USERNAME\",\"password\":\"$TB_PASSWORD\"}" | jq -r '.token')

# List all devices
curl -s "$TB_URL/api/tenant/devices?pageSize=10&page=0" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq '.data[] | {name, type, id: .id.id}'

# Get first device ID
DEVICE_ID=$(curl -s "$TB_URL/api/tenant/devices?pageSize=1&page=0" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq -r '.data[0].id.id')

# Get telemetry keys for device
curl -s "$TB_URL/api/plugins/telemetry/DEVICE/$DEVICE_ID/keys/timeseries" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq

# Get latest telemetry values
curl -s "$TB_URL/api/plugins/telemetry/DEVICE/$DEVICE_ID/values/timeseries?keys=temperature,humidity" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq

# Get historical data (last hour)
START_TS=$(($(date +%s)*1000 - 3600000))
END_TS=$(($(date +%s)*1000))
curl -s "$TB_URL/api/plugins/telemetry/DEVICE/$DEVICE_ID/values/timeseries?keys=temperature&startTs=$START_TS&endTs=$END_TS&limit=100" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq

# List dashboards and make first one public
DASHBOARD_ID=$(curl -s "$TB_URL/api/tenant/dashboards?pageSize=1&page=0" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq -r '.data[0].id.id')

curl -s -X POST "$TB_URL/api/customer/public/dashboard/$DASHBOARD_ID" \
  -H "X-Authorization: Bearer $TB_TOKEN" | jq
```