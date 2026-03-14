---
name: sms-gateway
description: 通过运行在 USB GSM 调制解调器上的自托管 SMS 网关来发送和接收短信。当用户需要发送文本消息、检查收到的消息或通过本地网关管理 SMS 通信时，可以使用该功能。
metadata:
  openclaw:
    requires:
      env:
        - SMS_GATEWAY_API_KEY
      bins:
        - curl
        - jq
    primaryEnv: SMS_GATEWAY_API_KEY
---
# SMS网关功能

您可以通过位于`~/.openclaw/workspace/skills/sms-gateway/scripts`目录中的shell脚本来发送和接收短信。

## 先决条件

在使用OpenClaw的SMS网关功能之前，您需要先安装相应的SMS网关服务。详情请参阅[README.md](https://github.com/mattboston/sms-gateway/blob/main/openclaw/README.md)。

## 设置

在使用此功能之前，请在`~/.openclaw/workspace/skills/sms-gateway/scripts`目录下创建一个`.env`文件，并设置以下环境变量：

```text
SMS_GATEWAY_URL=http://127.0.0.1:5174
SMS_GATEWAY_API_KEY=your-api-key-here
```

如果`.env`文件缺失或`SMS_GATEWAY_API_KEY`未设置，脚本将无法正常运行并会输出错误信息。

### 允许列表

`~/.openclaw/workspace/skills/sms-gateway/scripts/allowlist.json`文件中列出了允许发送和接收短信的用户及电话号码。发送短信的脚本会拒绝向不在该列表中的号码发送短信；接收短信的脚本默认只会显示允许列表中的号码发送的短信，过滤掉未知发件人的信息。如需添加或删除允许的联系人，请直接编辑`allowlist.json`文件。

## 功能说明

### 发送短信

向允许的电话号码发送文本短信。

```bash
~/.openclaw/workspace/skills/sms-gateway/scripts/send_sms.sh -t "+15551234567" -m "Hello from SMS Gateway"
```

选项：
- `-t` - 收件人电话号码（必须在`allowlist.json`中）
- `-m` - 短信内容

脚本会在发送前根据`allowlist.json`验证收件人号码。如果该号码不在允许列表中，脚本会显示允许的号码列表并输出错误信息。

发送成功后，脚本会输出“短信发送成功。”以及包含消息ID和状态的JSON响应；如果发送失败，脚本会输出HTTP状态码和错误信息。

### 接收短信

检查收件箱中的短信。

```bash
~/.openclaw/workspace/skills/sms-gateway/scripts/receive_sms.sh
```

选项：
- `-s <status>` - 按状态筛选：`received`（默认）、`read`或`all`
- `-a` - 显示允许列表之外的号码发送的短信（默认只显示允许列表中的号码）

示例：

```bash
~/.openclaw/workspace/skills/sms-gateway/scripts/receive_sms.sh              # Unread messages from allowlisted numbers
~/.openclaw/workspace/skills/sms-gateway/scripts/receive_sms.sh -s all       # All messages from allowlisted numbers
~/.openclaw/workspace/skills/sms-gateway/scripts/receive_sms.sh -s read      # Previously read messages from allowlisted numbers
~/.openclaw/workspace/skills/sms-gateway/scripts/receive_sms.sh -a           # Unread messages from all numbers
~/.openclaw/workspace/skills/sms-gateway/scripts/receive_sms.sh -a -s all    # All messages from all numbers
```

脚本会显示每条短信的发送时间、发件人号码、状态、内容及ID。未读短信（`status=received`）在显示后会被自动标记为已读。默认情况下，系统会过滤掉`allowlist.json`中未列出的号码发送的短信。

## 输出格式

### 发送短信的输出格式

```text
Message sent successfully.
{
  "id": "uuid",
  "status": "sent",
  "message": "message sent"
}
```

### 接收短信的输出格式

```text
Inbox messages (received): 2

[2026-03-08T12:00:00Z] From: +15551234567
  Status: received
  Body: Hey there
  ID: some-uuid

Marked message some-uuid as read.
```

## 使用指南：
- 仅向`allowlist.json`中列出的号码发送短信。
- 仅接收`allowlist.json`中列出的号码发送的短信。
- 电话号码中必须包含国家代码（例如，美国的电话号码前缀为`+1`）。
- 当用户要求“发送短信”时，使用`send_sms.sh`脚本。
- 当用户询问新短信时，运行`receive_sms.sh`（不带任何参数）。
- 当用户要求查看所有短信时，运行`receive_sms.sh -s all`。
- 如果发送短信失败，需将错误信息告知用户。
- 仅使用`send_sms.sh`和`receive_sms.sh`脚本进行发送和接收操作，切勿直接使用`SMS_GATEWAY_API_KEY`进行通信。
- 当收到来自某个联系人的短信时，需检查当前会话或最近的工作流程中是否已向该号码发送过短信；如果是，则将收到的短信视为对该对话的回复，而非无关的来电。

## 故障排除：

### “电话号码不在允许列表中”

收件人号码必须与`allowlist.json`中的条目完全匹配，包括国家代码前缀（例如`+1`）。请检查允许列表并添加相应的号码。

### “SMS_GATEWAY_API_KEY未设置”

请在`~/.openclaw/workspace/skills/sms-gateway/scripts/`目录下创建一个`.env`文件，并设置您的API密钥。具体操作请参见上述“设置”部分。

### 发送短信失败

请确认SMS网关正在运行，并且可以通过`env`文件中配置的URL访问。您可以使用以下命令验证连接是否正常：

```bash
curl -s http://127.0.0.1:5174/api/v1/health
```