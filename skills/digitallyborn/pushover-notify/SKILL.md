---
name: pushover-notify
description: "通过 Pushover (pushover.net) 将推送通知发送到您的手机。当您需要从 OpenClaw 获得可靠的离线警报时，可以使用此功能：提醒、监控警报、Cron/心跳信号摘要，或者设置“当 X 发生时通知我”的工作流程。"
---

# Pushover通知

通过一个简单的Node.js脚本来使用Pushover API发送推送通知。

## 设置（一次性操作）

1) 创建一个Pushover应用程序令牌并获取您的用户密钥：
- 应用程序令牌：https://pushover.net/apps/build
- 用户密钥：显示在您的Pushover控制面板上

2) 向运行时提供凭据（**不要**将这些凭据硬编码到脚本中）：
- `PUSHOVER_APP_TOKEN`
- `PUSHOVER_USER_KEY`

3) （可选）设置默认值：
- `PUSHOVER_DEVICE`（设备名称）
- `PUSHOVER SOUND`

## 发送通知

使用提供的脚本：

```bash
PUSHOVER_APP_TOKEN=... PUSHOVER_USER_KEY=... \
  node skills/pushover-notify/scripts/pushover_send.js \
  --title "OpenClaw" \
  --message "Hello from Ted" \
  --priority 0
```

可选参数：
- `--url "https://..."` 和 `--url-title "Open"`
- `--sound "pushover"`
- `--device "iphone"`
- `--priority -1|0|1|2`

紧急通知的示例：

```bash
PUSHOVER_APP_TOKEN=... PUSHOVER_USER_KEY=... \
  node skills/pushover-notify/scripts/pushover_send.js \
  --title "ALERT" \
  --message "Something is on fire" \
  --priority 2 --retry 60 --expire 3600
```

## 注意事项

- 如果需要了解API字段的详细信息，请阅读：`references/pushover-api.md`。
- 对于需要定期提醒的情况，建议使用`cron`作业来安排提醒；`cron`作业的文本可以指示Ted运行此脚本。