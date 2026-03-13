---
name: feishu-file
description: 将本地文件发送到 Feishu 聊天中。支持上传并发送任何类型的文件作为 Feishu 文件消息。
metadata: {
  "openclaw": {
    "requires": {
      "bins": ["curl", "jq"],
      "env": ["FEISHU_APP_ID", "FEISHU_APP_SECRET"]
    }
  }
}
---
# Feishu 文件发送器

这是一个用于将本地文件发送给 Feishu 用户或群组的技能。

## 设置

需要 Feishu 应用程序的凭据。请确保这些凭据已配置在您的环境变量中或 `openclaw.json` 文件中：

```bash
export FEISHU_APP_ID="cli_xxx"
export FEISHU_APP_SECRET="xxx"
export FEISHU_RECEIVER="ou_xxx" # Default receiver (optional)
```

## 使用方法

### 基本用法

将文件发送给默认接收者（在 `FEISHU RECEIVER` 中配置）：

```bash
bash scripts/send_file.sh "/path/to/your/file.pdf"
```

### 指定接收者

将文件发送给特定的 OpenID：

```bash
bash scripts/send_file.sh "/path/to/report.xlsx" "ou_abcdef123456"
```

### 不同类型的接收者

将文件发送给群组（`chat_id`）：

```bash
bash scripts/send_file.sh "/path/to/archive.zip" "oc_abcdef123456" "chat_id"
```

支持的接收者类型：`open_id`、`user_id`、`chat_id`、`email`。

## 脚本详情

### scripts/send_file.sh

这是处理整个发送流程的主要脚本，包括以下三个步骤：
1. **身份验证**：获取 `tenant_access_token`。
2. **上传**：使用 `POST /im/v1/files` 将文件上传到 Feishu 的内部存储。
3. **发送**：使用 `POST /im/v1/messages` 发送文件消息。

## 所需权限

Feishu 应用程序必须具有以下权限：
- `im:message`（发送和接收消息）
- `im:message:send_as_bot`（以机器人的身份发送消息）
- `im:resource`（访问和上传资源）