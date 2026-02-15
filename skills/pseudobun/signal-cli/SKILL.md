---
name: signal-cli
description: 通过 macOS 上的本地 `signal-cli` 安装来发送 Signal 消息以及查找 Signal 收件人。当用户需要向某人发送 Signal 消息、发送 Signal 文本/附件、列出 Signal 联系人，或根据姓名/昵称/电话号码查找收件人时，可以使用该功能。
---

# signal-cli（Signal消息传递工具）

请使用本地的 `signal-cli` 命令行工具。

## 前提条件

- `signal-cli` 已经安装完成，并且已正确链接到系统路径中。
- 为确保安全，在发送消息之前，请务必与用户确认收件人信息及最终消息内容。

## 常用操作模式

### 查找可用账户

```bash
signal-cli listAccounts
```

### 列出联系人列表（JSON格式）

```bash
signal-cli -o json -u "+386..." listContacts
```

### 根据姓名/昵称/电话号码查找联系人

建议使用配套提供的脚本（支持模糊匹配及多个匹配结果）：

```bash
python3 scripts/find_contact.py --account "+386..." --query "Name"
```

### 发送消息

建议使用配套提供的脚本（该脚本会将联系人姓名转换为对应的电话号码）：

```bash
python3 scripts/send_message.py --account "+386..." --to "Name" --text "Heyo ..."
```

如果 `--to` 参数已经是以 E.164 格式表示的电话号码（例如 `+386...`），系统会直接发送消息。

## 安全注意事项（始终遵守）

- 如果根据姓名查找联系人时返回多个匹配结果，请向用户展示所有选项并询问其选择哪一位联系人。
- 如果消息中包含敏感信息，在通过 Signal 发送之前请务必获得用户的明确同意。
- 系统默认使用 `--service-environment live` 模式（即 `signal-cli` 的默认设置），并采用常规的安全信任机制。