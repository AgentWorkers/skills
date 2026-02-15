---
name: read-no-evil-mcp
description: 通过 `read-no-evil-mcp` 实现安全的电子邮件访问功能。该工具可有效防止电子邮件中的提示注入攻击（prompt injection attacks），支持执行电子邮件阅读、发送、删除和移动等操作。
---

# read-no-evil-mcp

这是一个安全的电子邮件网关，能够在用户查看邮件内容之前扫描邮件，以检测是否存在提示注入（prompt injection）攻击。

## 先决条件

请安装 `read-no-evil-mcp` 包（版本必须与 `skill` 的版本相匹配）：

```bash
pip install read-no-evil-mcp==0.2.0
```

## 配置

### 配置文件

创建 `~/.config/read-no-evil-mcp/config.yaml` 文件：

```yaml
accounts:
  - id: "default"
    type: "imap"
    host: "mail.example.com"
    port: 993
    username: "you@example.com"
    ssl: true
    permissions:
      read: true
      send: false
      delete: false
      move: false
    smtp_host: "mail.example.com"
    smtp_port: 587
    from_address: "you@example.com"
    from_name: "Your Name"
```

### 认证信息

创建 `~/.config/read-no-evil-mcp/.env` 文件：

```bash
RNOE_ACCOUNT_DEFAULT_PASSWORD=your-password
```

环境变量格式：`RNOE_ACCOUNT_{ACCOUNT_ID}_PASSWORD`（全部为大写）。

## 命令行接口（CLI）命令

```bash
# List recent emails (last 30 days)
rnoe-mail.py list

# List with options
rnoe-mail.py list --limit 10 --days 7 --account myaccount

# Read email (scanned for prompt injection!)
rnoe-mail.py read <uid>

# Send email (requires send permission)
rnoe-mail.py send --to "user@example.com" --subject "Hello" --body "Message"

# List folders
rnoe-mail.py folders

# Move email to folder
rnoe-mail.py move <uid> --to "Archive"
```

## 提示注入检测

所有邮件都会被自动扫描：
- **安全**：邮件内容会正常显示。
- **检测到注入攻击**：程序会以退出代码 2 结束运行，并显示攻击的详细信息及相关模式。

该工具使用 ProtectAI 的 DeBERTa 模型进行检测（本地推理，不依赖外部 API）。

## 权限设置

| 权限 | 描述 | 默认值 |
|------------|-------------|---------|
| `read` | 列出并读取邮件内容 | `true` |
| `send` | 通过 SMTP 发送邮件 | `false` |
| `delete` | 删除邮件 | `false` |
| `move` | 在文件夹间移动邮件 | `false` |

## 安全注意事项

- 邮件内容在返回给用户之前会先经过提示注入攻击的扫描。
- 机器学习模型在本地运行，不会将任何数据发送到外部 API。
- 仅在实际需要时才启用写入权限。
- 建议使用与应用程序相关的专用密码进行身份验证。