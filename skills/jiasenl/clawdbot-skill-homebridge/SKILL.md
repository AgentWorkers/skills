---
name: homebridge
description: "通过 Homebridge 的配置界面（Config UI）或 REST API 来控制智能家居设备。该功能可用于列出设备、开关设备、调节设备的亮度、颜色或温度（适用于支持 HomeKit 的设备）。支持控制的设备包括灯具、开关、恒温器、风扇等由 Homebridge 管理的智能设备。"
homepage: https://github.com/homebridge/homebridge-config-ui-x
metadata: { "clawdbot": { "emoji": "🏠" } }
---

# 通过 Homebridge Config UI X 控制智能家居设备

您可以通过 Homebridge Config UI X 的 REST API 来控制智能家居设备。

## 先决条件

1. 安装并运行了 Homebridge 以及 Config UI X。
2. 在 `~/.clawdbot/credentials/homebridge.json` 文件中配置了认证凭据：
   ```json
   {
     "url": "https://homebridge.local:8581",
     "username": "admin",
     "password": "your-password"
   }
   ```

## API 概述

Homebridge Config UI X 提供了一个 REST API。完整的文档请访问 `{HOMEBRIDGE_URL}/swagger`。

## 认证

所有 API 调用都需要一个 Bearer 令牌。请先获取令牌：

```bash
# Get auth token
TOKEN=$(curl -s -X POST "${HOMEBRIDGE_URL}/api/auth/login" \
  -H "Content-Type: application/json" \
  -d "{\"username\":\"${HOMEBRIDGE_USERNAME}\",\"password\":\"${HOMEBRIDGE_PASSWORD}\"}" \
  | jq -r '.access_token')
```

## 常见操作

### 列出所有配件

```bash
curl -s "${HOMEBRIDGE_URL}/api/accessories" \
  -H "Authorization: Bearer ${TOKEN}" | jq
```

响应中包含配件的 `uniqueId`、`serviceName`、`type` 以及当前的 `values`。

### 获取配件的布局信息（房间）

```bash
curl -s "${HOMEBRIDGE_URL}/api/accessories/layout" \
  -H "Authorization: Bearer ${TOKEN}" | jq
```

### 控制配件

使用 PUT 请求来更新配件的属性：

```bash
# Turn on a light/switch
curl -s -X PUT "${HOMEBRIDGE_URL}/api/accessories/{uniqueId}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"characteristicType": "On", "value": true}'

# Turn off
curl -s -X PUT "${HOMEBRIDGE_URL}/api/accessories/{uniqueId}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"characteristicType": "On", "value": false}'

# Set brightness (0-100)
curl -s -X PUT "${HOMEBRIDGE_URL}/api/accessories/{uniqueId}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"characteristicType": "Brightness", "value": 50}'

# Set color (Hue: 0-360, Saturation: 0-100)
curl -s -X PUT "${HOMEBRIDGE_URL}/api/accessories/{uniqueId}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"characteristicType": "Hue", "value": 240}'

# Set thermostat target temperature
curl -s -X PUT "${HOMEBRIDGE_URL}/api/accessories/{uniqueId}" \
  -H "Authorization: Bearer ${TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{"characteristicType": "TargetTemperature", "value": 22}'
```

### 常见属性类型

| 属性类型                        | 属性值         | 描述                           |
| --------------------------- | -------------- | ----------------------------------- |
| `On`                        | `true`/`false`     | 设备的开关状态                     |
| `Brightness`                | `0-100`        | 灯光的亮度（百分比）                   |
| `Hue`                       | `0-360`        | 色彩的色调（度数）                     |
| `Saturation`                | `0-100`        | 色彩的饱和度（百分比）                   |
| `ColorTemperature`          | `140-500`      | 色温（Mired 单位）                     |
| `TargetTemperature`         | `10-38`        | 温度调节器的目标温度（°C）                 |
| `TargetHeatingCoolingState` | `0-3`          | 制热/制冷模式（0=关闭，1=制热，2=制冷，3=自动）       |
| `RotationSpeed`             | `0-100`        | 风扇的转速（百分比）                     |
| `Active`                    | `0`/`1`        | 设备是否处于活动状态                     |

## 使用脚本

为方便操作，可以使用提供的脚本：

### 列出所有配件

```bash
scripts/homebridge_api.py list
scripts/homebridge_api.py list --room "Living Room"
scripts/homebridge_api.py list --type Lightbulb
```

### 控制设备

```bash
# Turn on/off
scripts/homebridge_api.py set <uniqueId> On true
scripts/homebridge_api.py set <uniqueId> On false

# Adjust brightness
scripts/homebridge_api.py set <uniqueId> Brightness 75

# Set color
scripts/homebridge_api.py set <uniqueId> Hue 120
scripts/homebridge_api.py set <uniqueId> Saturation 100
```

### 获取配件状态

```bash
scripts/homebridge_api.py get <uniqueId>
```

## 提示

- 首先列出所有配件，以找到您需要控制的配件的 `uniqueId`。
- API 文档位于 `/swagger`，其中列出了所有可用的接口。
- 属性名称区分大小写（请使用 `On` 而不是 `on`）。
- 有些配件可能包含多个服务；请查看响应中的服务类型。
- 令牌会过期，请在收到 401 错误时重新认证。