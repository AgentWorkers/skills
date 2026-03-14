---
name: gws-gmail-reply
version: 1.0.0
description: "Gmail：回复消息（会自动处理消息的关联关系，即“线程”）。"
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws gmail +reply --help"
---
# gmail +reply

> **前提条件：** 阅读 `../gws-shared/SKILL.md` 以了解认证、全局参数和安全规则。如果文件缺失，请运行 `gws generate-skills` 生成该文件。

**功能：** 回复邮件（自动处理邮件线程）

## 使用方法

```bash
gws gmail +reply --message-id <ID> --body <TEXT>
```

## 参数说明

| 参数 | 是否必填 | 默认值 | 说明 |
|------|----------|---------|-------------|
| `--message-id` | ✓ | — | 需要回复的 Gmail 邮件 ID |
| `--body` | ✓ | — | 回复内容（纯文本，或使用 `--html` 选项指定 HTML 格式） |
| `--from` | — | — | 发件人地址（用于“以...身份发送”或使用别名；省略则使用账户默认地址） |
| `--to` | — | — | 需要抄送的电子邮件地址（用逗号分隔） |
| `--cc` | — | — | 需要密送的电子邮件地址（用逗号分隔） |
| `--bcc` | — | — | 需要密送的电子邮件地址（用逗号分隔） |
| `--html` | — | — | 以 HTML 格式发送回复（会保留原始邮件的格式；此时 `--body` 参数会被视为 HTML 内容） |
| `--dry-run` | — | — | 显示发送请求的内容，但不实际执行发送操作 |

## 使用示例

```bash
gws gmail +reply --message-id 18f1a2b3c4d --body 'Thanks, got it!'
gws gmail +reply --message-id 18f1a2b3c4d --body 'Looping in Carol' --cc carol@example.com
gws gmail +reply --message-id 18f1a2b3c4d --body 'Adding Dave' --to dave@example.com
gws gmail +reply --message-id 18f1a2b3c4d --body 'Reply' --bcc secret@example.com
gws gmail +reply --message-id 18f1a2b3c4d --body '<b>Bold reply</b>' --html
```

## 提示：
- 该命令会自动设置 `In-Reply-To`、`References` 和 `threadId` 标头。
- 回复内容中会保留原始邮件的格式。
- 使用 `--to` 可以添加额外的收件人。
- 如果需要回复所有收件人，请使用 `+reply-all`。

## 相关文档：
- [gws-shared](../gws-shared/SKILL.md) — 全局参数和认证设置
- [gws-gmail](../gws-gmail/SKILL.md) — 所有与发送、阅读和管理邮件相关的命令