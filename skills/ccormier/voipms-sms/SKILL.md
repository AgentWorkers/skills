---
name: voipms-sms
description: OpenClaw技能：通过VoIP.ms API发送和接收短信
---
# VoIP.ms SMS 技能

使用此技能通过 VoIP.ms API 发送和检索 SMS 消息。

## 可用的脚本

### `scripts/send_sms.py`

从您的 VoIP.ms DID 中向目标号码发送 SMS 消息。

必需参数：
- `--did`：源 VoIP.ms 号码
- `--dst`：目标电话号码
- `--message`：SMS 消息内容

示例：

```bash
python3 scripts/send_sms.py \
  --did "15551234567" \
  --dst "15557654321" \
  --message "Hello from OpenClaw"
```

### `scripts/get_sms.py`

从 VoIP.ms API 检索指定日期范围内的 SMS 消息。

参数：
- `--did`（可选）：按特定源号码过滤
- `--days`（可选，默认值为 `1`）：要检索的天数

示例（所有号码，过去一天）：

```bash
python3 scripts/get_sms.py --days 1
```

示例（特定 DID，过去 7 天）：

```bash
python3 scripts/get_sms.py --did "15551234567" --days 7
```

## 必需的凭据

在运行任一脚本之前，请设置以下环境变量。由于密码不应被硬编码或在聊天命令中直接传递，请使用 Bitwarden 保管库动态获取这些凭据。

确保保管库中包含两个条目：`api-voipms-username` 和 `api-voipms-password`。

示例：

```bash
export VOIPMS_API_USERNAME=$(rbw get api-voipms-username)
export VOIPMS_API_PASSWORD=$(rbw get api-voipms-password)
```