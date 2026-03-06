---
name: ravi-passwords
description: **存储和检索网站凭据**——一款用于管理域名/用户名/密码信息的端到端加密密码管理器。**请勿将其用于API密钥或机密信息的存储（请使用ravi-secrets）**，也不应用于消息的读取（请使用ravi-inbox）。
---
# Ravi Passwords

用于存储和检索您注册的服务的密码。敏感信息（用户名、密码、备注）采用端到端（E2E）加密技术进行保护——命令行工具（CLI）会自动处理加密和解密操作。域名则以明文形式存储，便于查询。

## 命令

```bash
# Create entry (auto-generates password if --password not given)
ravi passwords create example.com --json
ravi passwords create example.com --username "me@example.com" --password 'S3cret!' --json

# List all entries
ravi passwords list --json

# Retrieve (decrypted)
ravi passwords get <uuid> --json

# Update
ravi passwords update <uuid> --password 'NewPass!' --json

# Delete
ravi passwords delete <uuid> --json

# Generate a password without storing it
ravi passwords generate --length 24 --json
# -> {"password": "xK9#mL2..."}
```

**创建密码时可使用的参数：** `--username`、`--password`、`--notes`、`--generate`（默认长度为16个字符）、`--no-special`、`--no-digits`、`--exclude-chars`

## JSON 格式

**`ravi passwords list --json`：**  
```json
[
  {
    "uuid": "uuid",
    "domain": "example.com",
    "username": "me@example.com",
    "created_dt": "2026-02-25T10:30:00Z"
  }
]
```

**`ravi passwords get <uuid> --json`：**  
```json
{
  "uuid": "uuid",
  "domain": "example.com",
  "username": "me@example.com",
  "password": "S3cret!",
  "notes": "",
  "created_dt": "2026-02-25T10:30:00Z"
}
```

## 重要说明：

- **端到端加密技术**：CLI会在发送密码信息前对其进行加密，在获取时再进行解密。因此您看到的始终是明文密码。
- **域名处理**：`ravi passwords create` 会自动将 URL 简化为基础域名（例如，`https://mail.google.com/inbox` 会被简化为 `google.com`）。
- **务必使用 `--json` 格式**：输出结果为人类可读格式，但不适合进一步解析。

## 相关工具：

- **ravi-secrets**：用于存储 API 密钥和环境变量（键值对形式的敏感信息，而非网站登录凭证）。
- **ravi-login**：提供端到端的注册/登录流程，可将凭证存储在该工具中。
- **ravi-identity**：用于获取与用户名对应的电子邮件地址。
- **ravi-feedback**：用于报告密码管理工具的问题或提出改进建议。