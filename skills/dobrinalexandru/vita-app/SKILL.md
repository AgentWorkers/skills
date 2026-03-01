---
name: vita
description: 从 VITA（他们的健康管理平台）中获取用户的个人健康数据。当用户询问自己的健康状况、当天的感受、睡眠情况、心率变异性（HRV）、所服用的补充剂、健康护理方案，或希望接收每日健康报告时，可以使用这些数据。系统会返回当天的 AI 分析结果、可穿戴设备（如 Oura/WHOOP）监测的指标，以及用户当前正在服用的补充剂信息。
---
使用此技能可以代表用户访问 VITA 的健康数据。

## 设置

在 VITA 中的 **设置 → API 密钥 → 新建密钥** 选项中生成一个 API 密钥。

然后将该密钥添加到 `~/.openclaw/openclaw.json` 文件中：

```json
{
  "skills": {
    "entries": {
      "vita": {
        "enabled": true,
        "env": {
          "VITA_API_KEY": "vita_<your key>",
          "VITA_API_URL": "https://app.vitadao.com/api/vita-api"
        }
      }
    }
  }
}
```

## 调用 API

```bash
curl "$VITA_API_URL?action=<action>" \
  -H "Authorization: Bearer $VITA_API_KEY"
```

## 可用的操作

| 操作 | 返回内容 |
|---|---|
| `get_daily_insight` | 当天的 AI 生成总结、健康状况（正面/中性/警告）、睡眠和训练情况、协议遵守情况以及相关建议 |
| `get_todays_outlook` | 当天的实时可穿戴设备数据：睡眠质量、恢复情况、心率变异性（HRV）以及 Oura 和 WHOOP 的相关指标 |
| `get_protocols` | 当前正在使用的补充剂方案，包括成分、剂量、单位、服用时间和频率 |

## 使用指南

- 每次健康检查时首先调用 `get_daily_insight`，以获取当天的整体健康状况。
- 如果需要获取可穿戴设备的原始数据（如心率变异性、睡眠质量、恢复百分比），则调用 `get_todays_outlook`。
- 当用户询问有关补充剂的信息时，调用 `get_protocols`。
- 可以同时调用这三个 API 以获取完整的每日健康报告。
- 请自行解读数据，无需让用户解释他们的健康指标。
- 如果收到 401 错误（表示密钥无效），请让用户重新在 VITA 设置中生成新的 API 密钥。