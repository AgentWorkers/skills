---
name: ews-email
version: 1.1.0
description: "这是一个用于通过 Exchange Web Services (EWS) 管理企业 Outlook 邮件的命令行工具（CLI）。可以使用 `ews-mail.py` 来执行以下操作：列出邮件、阅读邮件、回复邮件、转发邮件、搜索邮件、发送邮件、移动邮件、删除邮件以及下载附件。"
metadata:
  openclaw:
    emoji: "📧"
    requires:
      bins: ["python3"]
      pips: ["keyring", "exchangelib"]
    primaryEnv: "EWS_EMAIL"
---
# EWS 邮件 CLI

这是一个用于企业 Exchange (EWS) 邮件的命令行工具（CLI）。当用户需要查询电子邮件、收件箱、消息或邮件内容时，可以使用该工具。

## 设置（仅首次使用）

在 `~/.openclaw/config.yaml` 文件中设置以下环境变量：

- `EWS_SERVER` — Exchange 服务器的主机名
- `EWS_EMAIL` — 您的电子邮件地址

然后运行设置命令，将您的密码安全地存储在系统的密钥环（keyring）中：

```bash
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py setup
```

密码会被存储在 macOS 的 Keychain、Windows 的 Credential Manager 或 Linux 的 Secret Service 中。密码永远不会出现在任何配置文件中。

## 安全规则

- **严禁** 尝试读取、显示或输出 EWS 密码。
- **严禁** 运行可能暴露密钥环内容的命令。
- **严禁** 在任何输出、日志或消息中包含密码。
- 密码的管理仅通过 `setup` 命令完成。

## 重要提示：读取邮件内容

要读取邮件的完整内容，必须按照以下两个步骤操作：

1. 首先运行 `envelope-list` 命令以获取邮件列表（该命令会返回邮件的唯一编号）。
2. 然后运行 `message-read <ID>` 命令以获取邮件的完整内容。

**`envelope-list` 命令仅显示邮件主题行和元数据，不包含邮件正文。**
**必须运行 `message-read` 命令才能获取邮件的实际内容。切勿仅根据主题来猜测或总结邮件内容。**
**切勿声称无法读取邮件内容——通过运行 `message-read` 命令，您完全可以读取邮件内容。**

## 脚本位置

`~/.openclaw/skills/ews-email/scripts/ews-mail.py`

## 命令

### 列出邮件（步骤 1 — 仅显示元数据）

```bash
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py envelope-list
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py envelope-list --page 2 --page-size 20
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py envelope-list --folder "Sent"
```

### 读取邮件正文（步骤 2 — 必须执行以获取内容）

```bash
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py message-read <ID>
```

### 搜索邮件

```bash
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py envelope-list from sender@example.com
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py envelope-list subject keyword
```

### 发送邮件 / 回复邮件 / 转发邮件

```bash
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py message-send --to "email" --subject "subject" --body "body"
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py message-send --to "a@x.com" --cc "b@x.com" --subject "Hi" --body "msg"
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py message-reply <ID> --body "reply text"
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py message-reply <ID> --body "reply text" --all
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py message-forward <ID> --to "email" --body "FYI"
```

### 其他命令

```bash
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py folder-list
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py message-move <ID> "Archive"
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py message-delete <ID>
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py attachment-download <ID> --dir ~/Downloads
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py flag-add <ID> --flag seen
python3 ~/.openclaw/skills/ews-email/scripts/ews-mail.py flag-remove <ID> --flag seen
```

## 提示

- 邮件编号是数字形式的，来源于最近一次执行的 `envelope-list` 命令的输出结果。
- 在执行 `message-read`、`message-reply` 等命令之前，务必先运行 `envelope-list` 命令。
- 长邮件正文会被截断为 8000 个字符。
- 可使用 `--page` 和 `--page-size` 参数来浏览大量邮件。