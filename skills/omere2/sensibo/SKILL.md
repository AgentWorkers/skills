---
name: sensibo
description: 通过 REST API 控制 Sensibo 智能空调设备。适用于用户需要开启/关闭空调、调节温度、设置模式、查看室内温度/湿度或管理气候控制计划的情况。可响应以下指令：“开启空调”、“将卧室温度设置为 22 度”、“现在有多热？”、“关闭空调”、“制冷模式”等语音指令。
---

# Sensibo空调控制

通过Sensibo的REST API来控制智能空调设备。

## 首次设置

1. 从 https://home.sensibo.com/me/api 获取API密钥。
2. 列出设备以获取设备ID：
   ```bash
   curl --compressed "https://home.sensibo.com/api/v2/users/me/pods?fields=id,room&apiKey={API_KEY}"
   ```
3. 将设备ID保存到TOOLS.md文件中：
   ```markdown
   ## Sensibo
   API Key: `{your_key}`
   
   | Room | Device ID |
   |------|-----------|
   | Living Room | abc123 |
   | Bedroom | xyz789 |
   ```

## API参考

**基础URL:** `https://home.sensibo.com/api/v2`
**认证:** 使用查询参数 `?apiKey={key}` 进行认证
**建议使用:** 使用 `--compressed` 标志以获得更好的速率限制

### 开/关空调

```bash
curl --compressed -X POST "https://home.sensibo.com/api/v2/pods/{device_id}/acStates?apiKey={key}" \
  -H "Content-Type: application/json" -d '{"acState":{"on":true}}'
```

### 设置温度

```bash
curl --compressed -X PATCH "https://home.sensibo.com/api/v2/pods/{device_id}/acStates/targetTemperature?apiKey={key}" \
  -H "Content-Type: application/json" -d '{"newValue":23}'
```

### 设置运行模式

可选模式：`cool`（制冷）、`heat`（制热）、`fan`（风扇模式）、`auto`（自动模式）、`dry`（除湿模式）

```bash
curl --compressed -X PATCH "https://home.sensibo.com/api/v2/pods/{device_id}/acStates/mode?apiKey={key}" \
  -H "Content-Type: application/json" -d '{"newValue":"cool"}'
```

### 设置风扇转速

可选档位：`low`（低速）、`medium`（中速）、`high`（高速）、`auto`（自动调节）

```bash
curl --compressed -X PATCH "https://home.sensibo.com/api/v2/pods/{device_id}/acStates/fanLevel?apiKey={key}" \
  -H "Content-Type: application/json" -d '{"newValue":"auto"}'
```

### 全面状态更改

```bash
curl --compressed -X POST "https://home.sensibo.com/api/v2/pods/{device_id}/acStates?apiKey={key}" \
  -H "Content-Type: application/json" \
  -d '{"acState":{"on":true,"mode":"cool","targetTemperature":22,"fanLevel":"auto","temperatureUnit":"C"}}'
```

## 空调状态属性

| 属性          | 类型         | 值         |
|---------------|-------------|------------|
| on            | boolean       | true        | false        |
| mode           | string       | cool        | heat        | fan        | auto        | dry        |
| targetTemperature | integer      | （根据空调型号不同而变化） |
| temperatureUnit    | string       | C          | F          |
| fanLevel       | string       | low        | medium      | high        | auto        |
| swing          | string       | stopped     | rangeful     |

## 读取传感器数据

### 当前测量数据

在响应中包含 `measurements` 字段：
```bash
curl --compressed "https://home.sensibo.com/api/v2/pods/{device_id}?fields=measurements&apiKey={key}"
```

响应内容示例：
```json
{"measurements": {"temperature": 24.5, "humidity": 55, "time": "2024-01-15T12:00:00Z"}}
```

### 历史数据

```bash
curl --compressed "https://home.sensibo.com/api/v2/pods/{device_id}/historicalMeasurements?days=1&apiKey={key}"
```

## 气候反应（智能自动化）

### 启用/禁用

```bash
curl --compressed -X PUT "https://home.sensibo.com/api/v2/pods/{device_id}/smartmode?apiKey={key}" \
  -H "Content-Type: application/json" -d '{"enabled":true}'
```

### 配置阈值

```bash
curl --compressed -X POST "https://home.sensibo.com/api/v2/pods/{device_id}/smartmode?apiKey={key}" \
  -H "Content-Type: application/json" \
  -d '{
    "enabled": true,
    "lowTemperatureThreshold": 20,
    "lowTemperatureState": {"on": true, "mode": "heat"},
    "highTemperatureThreshold": 26,
    "highTemperatureState": {"on": true, "mode": "cool"}
  }'
```

## 安排任务

**注意：** 安排任务的API使用基础URL：`https://home.sensibo.com/api/v1`

### 列出所有安排任务

```bash
curl --compressed "https://home.sensibo.com/api/v1/pods/{device_id}/schedules/?apiKey={key}"
```

### 创建新的安排任务

```bash
curl --compressed -X POST "https://home.sensibo.com/api/v1/pods/{device_id}/schedules/?apiKey={key}" \
  -H "Content-Type: application/json" \
  -d '{
    "targetTimeLocal": "22:00",
    "timezone": "Europe/London",
    "acState": {"on": false},
    "recurOnDaysOfWeek": ["sunday","monday","tuesday","wednesday","thursday","friday","saturday"]
  }'
```

### 删除安排任务

```bash
curl --compressed -X DELETE "https://home.sensibo.com/api/v1/pods/{device_id}/schedules/{schedule_id}/?apiKey={key}"
```

## 定时器

设置一次性延迟操作：

```bash
curl --compressed -X PUT "https://home.sensibo.com/api/v1/pods/{device_id}/timer/?apiKey={key}" \
  -H "Content-Type: application/json" \
  -d '{"minutesFromNow": 30, "acState": {"on": false}}'
```

## 使用技巧

1. **匹配房间名称：** 当用户输入“living room”（客厅）或“bedroom”（卧室）时，在TOOLS.md中查找对应的设备ID。
2. **检查响应状态：** 确保API响应中包含 `“status”: “success”。
3. **温度范围：** 取决于具体的空调型号。
4. **速率限制：** 使用 `--compressed` 标志来提高请求的发送频率。
5. **批量操作：** 遍历设备ID以批量执行操作（例如“关闭所有空调”）。