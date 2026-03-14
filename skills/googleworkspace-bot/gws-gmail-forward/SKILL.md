---
name: gws-gmail-forward
version: 1.0.0
description: "Gmail：将消息转发给新的收件人。"
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws gmail +forward --help"
---
# gmail +forward

> **前提条件：** 请阅读 `../gws-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。如果文件缺失，请运行 `gws generate-skills` 生成该文件。

**功能：** 将邮件转发给新的收件人。

## 使用方法

```bash
gws gmail +forward --message-id <ID> --to <EMAILS>
```

## 参数说明

| 参数 | 是否必填 | 默认值 | 说明 |
|------|----------|---------|-------------|
| `--message-id` | ✓ | — | 需要转发的 Gmail 邮件 ID |
| `--to` | ✓ | — | 收件人电子邮件地址（用逗号分隔） |
| `--from` | — | — | 发件人地址（用于“以……身份发送”或使用别名；省略则使用账户默认地址） |
| `--cc` | — | — | 抄送（CC）电子邮件地址（用逗号分隔） |
| `--bcc` | — | — | 密送（BCC）电子邮件地址（用逗号分隔） |
| `--body` | — | — | 可选：在转发邮件上方显示的备注（纯文本，或使用 `--html` 以 HTML 格式显示） |
| `--html` | — | — | 以 HTML 格式发送邮件（转发内容会采用 Gmail 的样式；此时 `--body` 参数会被视为 HTML 内容） |
| `--dry-run` | — | — | 显示发送请求的内容，但不实际执行该请求 |

## 示例

```bash
gws gmail +forward --message-id 18f1a2b3c4d --to dave@example.com
gws gmail +forward --message-id 18f1a2b3c4d --to dave@example.com --body 'FYI see below'
gws gmail +forward --message-id 18f1a2b3c4d --to dave@example.com --cc eve@example.com
gws gmail +forward --message-id 18f1a2b3c4d --to dave@example.com --bcc secret@example.com
gws gmail +forward --message-id 18f1a2b3c4d --to dave@example.com --body '<p>FYI</p>' --html
```

## 提示：
- 转发的邮件会包含原始邮件的发件人、日期、主题和收件人信息。

## 相关文档：
- [gws-shared](../gws-shared/SKILL.md) — 全局参数和身份验证设置
- [gws-gmail](../gws-gmail/SKILL.md) — 所有与发送、阅读和管理电子邮件相关的命令