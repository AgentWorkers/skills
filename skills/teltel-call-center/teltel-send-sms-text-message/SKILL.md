---
name: teltel-send-sms-text-message
description: 通过 TelTel (teltel.io) 的 REST API (api.teltel.io) 发送 SMS 文本消息。支持批量发送、发送结果查询以及批量短信管理功能。
metadata: {"openclaw":{"emoji":"💬","homepage":"https://www.teltel.io/","primaryEnv":"TELTEL_API_KEY"}}
---

使用随附的 Node.js 脚本，通过 TelTel API 发送 SMS 消息。

## 在使用该功能之前（TelTel 的前置要求）

1) 在 **https://www.teltel.io/** 注册账号。
2) 为你的 TelTel 账户充值。
3) 在 TelTel 的 **SMS** 部分，先发送一条 **测试短信** 以确认你的发件人名称/电话号码已被接受/验证。
4) 在 TelTel 的 **设置** 中找到你的 **API 密钥**。
5) 现在你可以使用该功能了！

## 通过 OpenClaw Skills 面板进行配置

### API 密钥字段（在 Skills UI 中显示）

该功能将 `TELTEL_API_KEY` 定义为 **主要环境变量**，因此 OpenClaw Skills UI 会提供一个用于输入 API 密钥的字段。

在内部，这个环境变量对应于：
- `skills.entries.teltel-send-sms-text-message.apiKey` → `TELTEL_API_KEY`

### 默认发件人

设置一个默认的发件人名称/电话号码（当未传递 `--from` 参数时使用）：
- `skills.entries.teltel-send-sms-text-message.env.TELTEL_SMS_FROM`

## 通过环境变量进行配置（另一种方式）

- `TELTEL_API_KEY`（必需）
- `TELTEL_SMS_FROM`（可选）—— 默认发件人名称/电话号码
- `TELTEL_BASE_URL`（可选）—— 默认值为 `https://api.teltel.io/v2`

## 发送单条 SMS 消息

```bash
node {baseDir}/scripts/send_sms.js \
  --to "+3712xxxxxxx" \
  --message "Hello from TelTel" \
  --from "37167881855"
```

如果你省略 `--from` 参数，脚本将使用 `TELTEL_SMS_FROM` 中设置的发件人信息。

**干运行示例**（仅打印 URL 和消息内容，不实际发送短信）：

```bash
node {baseDir}/scripts/send_sms.js \
  --dry-run \
  --to "+37111111111" \
  --message "test" \
  --from "37167881855"
```

## 发送批量 SMS 消息

```bash
node {baseDir}/scripts/send_sms_bulk.js \
  --from "37167881855" \
  --to "+3712...,+1..." \
  --message "Hello everyone"
```

`--to` 参数可以使用逗号、换行符或分号进行分隔。

## API 详细信息（供参考）

- 基础 URL：`https://api.teltel.io/v2`
- 单条 SMS 消息：`POST /sms/text`
  - JSON 格式：`{"data": {"from": "...", "to": "+...", "message": "...", "callback": "https://..."? }`
- 批量 SMS 消息：`POST /sms/bulk/text`
  - JSON 格式：`{"data": {"from": "...", "to": ["+...", "+..."], "message": "...", "callback": "https://..."? }`

**注意**：
- `to` 参数必须使用国际格式的电话号码。