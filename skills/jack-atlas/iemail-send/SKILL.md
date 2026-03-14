---
name: iemail-send
description: 通过 Iemail OpenAPI 发送交易相关的电子邮件。配置仅需通过 OpenClaw 的技能环境（skill environment）完成。
homepage: https://app.dmartech.cn/
metadata:
  {"openclaw":{"emoji":"📧","requires":{"anyBins":["python3"],"env":["IEMAIL_ACCESS_KEY","IEMAIL_ACCESS_KEY_SECRET","IEMAIL_SENDER"]},"primaryEnv":"IEMAIL_ACCESS_KEY"}}
---
# Iemail 发送

使用 Python 通过 Dmartech/Iemail OpenAPI 发送单封交易性电子邮件。

## 配置

在 `~/.openclaw/openclaw.json` 文件中进行配置：

```json
"skills": {
  "entries": {
    "iemail-send": {
      "enabled": true,
      "env": {
        "IEMAIL_ACCESS_KEY": "your-access-key",
        "IEMAIL_ACCESS_KEY_SECRET": "your-access-key-secret",
        "IEMAIL_SENDER": "your-sender@example.com"
      }
    }
  }
}
```

| 变量 | 描述 |
|----------|-------------|
| IEMAIL_ACCESS_KEY | OpenAPI 访问密钥 |
| IEMAIL_ACCESS_KEY_SECRET | OpenAPI 访问密钥的密钥值 |
| IEMAIL_SENDER | 发件人电子邮件地址（必填） |
| IEMAIL_TO | 默认收件人（可选） |

## 代理指令

1. 凭据：读取 `~/.openclaw/openclaw.json` 文件或工作区配置文件。OpenClaw 会在运行时将这些凭据注入环境变量中。
2. 发送邮件：在工作区中运行相应的脚本：
   ```bash
   python3 {baseDir}/send_email.py --to "recipient@example.com" --subject "Subject" --content "Body"
   ```

## 使用示例

```bash
python3 {baseDir}/send_email.py --to "recipient@example.com" --subject "Hello" --content "Hello from Iemail"
python3 {baseDir}/send_email.py "recipient@example.com" "Hello" "Hello from Iemail"
```

## 故障排除

- 401 未授权：检查 IP 白名单、访问密钥/密钥值以及系统时间是否正确。
- 无法找到 `senderAddressSn`：确认 `IEMAIL_SENDER` 是否与配置中的发件人地址匹配。