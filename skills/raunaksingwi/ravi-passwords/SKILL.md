---
name: ravi-passwords
description: 存储和检索网站凭证——一款用于管理域名/用户名/密码信息的端到端加密密码管理器。请勿将其用于API密钥或机密信息的存储（请使用ravi-vault），也不应用于消息的读取（请使用ravi-inbox）。
---
# Ravi Passwords

用于存储和检索您注册的服务的密码。所有字段均采用端到端（E2E）加密技术——命令行工具（CLI）会自动处理加密和解密操作。

## 命令

```bash
# Create entry (auto-generates password if --password not given)
ravi vault create example.com --json
ravi vault create example.com --username "me@ravi.app" --password 'S3cret!' --json

# List all entries
ravi vault list --json

# Retrieve (decrypted)
ravi vault get <uuid> --json

# Update
ravi vault edit <uuid> --password 'NewPass!' --json

# Delete
ravi vault delete <uuid> --json

# Generate a password without storing it
ravi vault generate --length 24 --json
# -> {"password": "xK9#mL2..."}
```

**创建密码存储项的参数：** `--username`（用户名），`--password`（密码），`--notes`（备注），`--generate`（生成新密码），`--length`（密码长度，默认为16个字符），`--no-special`（禁止使用特殊字符），`--no-digits`（禁止使用数字），`--exclude-chars`（排除特定字符集）

## JSON 格式

**`ravi vault list --json`：**  
用于列出所有存储的密码项。

**`ravi vault get <uuid> --json`：**  
用于根据UUID获取指定的密码项。

## 重要说明：

- **端到端加密是透明的**：CLI在发送数据前会自动加密密码字段，并在检索时解密，因此您看到的始终是明文形式。
- **域名处理**：`ravi vault create`会自动将URL简化为顶级域名（例如，`https://mail.google.com/inbox`会被简化为`google.com`）。
- **建议始终使用`--json`选项**：因为命令行输出的格式并不适合人类直接阅读或解析。

## 相关工具：

- **ravi-vault**：用于存储API密钥和环境变量（键值对形式的敏感信息，而非网站登录凭据）。
- **ravi-login**：提供端到端的注册/登录流程，用于管理用户凭据。
- **ravi-identity**：用于获取用户的电子邮件地址（用于用户名字段）。
- **ravi-feedback**：用于报告密码管理工具的问题或提出改进建议。