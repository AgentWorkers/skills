---
name: voipms-sms
description: **OpenClaw 技能：通过 VoIP.ms API 发送和接收短信（不依赖 Bitwarden）**
---
# VoIP.ms SMS Skill

使用此技能通过 VoIP.ms API 发送和检索 SMS 消息。

## 可用的脚本

### `scripts/send_sms.py`

从您的 VoIP.ms DID 发送 SMS 消息到目标号码。

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
- `--days`（可选，默认为 `1`）：要检索的天数

示例（所有号码，最近一天）：

```bash
python3 scripts/get_sms.py --days 1
```

示例（特定 DID，过去 7 天）：

```bash
python3 scripts/get_sms.py --did "15551234567" --days 7
```

## 必需的凭据

在运行任一脚本之前，请设置这些环境变量。Python 脚本将直接读取这些凭据。
请创建一个子账户或专用的 VoIP.ms API 账户，仅具有发送 SMS 的权限，而不要使用您的主管理员凭据。

示例：

```bash
export VOIPMS_API_USERNAME="my_api_username"
export VOIPMS_API_PASSWORD="my_api_password"
```