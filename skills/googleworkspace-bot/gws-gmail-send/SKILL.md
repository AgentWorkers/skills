---
name: gws-gmail-send
version: 1.0.0
description: "Gmail：发送电子邮件。"
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws gmail +send --help"
---
# gmail +send

> **前提条件：** 请阅读 `../gws-shared/SKILL.md` 以了解认证、全局参数和安全规则。如果文件缺失，请运行 `gws generate-skills` 生成该文件。

**发送电子邮件**

## 使用方法

```bash
gws gmail +send --to <EMAILS> --subject <SUBJECT> --body <TEXT>
```

## 参数说明

| 参数          | 是否必填 | 默认值 | 说明                          |
|--------------|--------|---------|--------------------------------------------|
| `--to`        | ✓       |        | 收件人电子邮件地址（用逗号分隔）                |
| `--subject`     | ✓       |        | 电子邮件主题                        |
| `--body`       | ✓       |        | 电子邮件正文（纯文本；使用 `--html` 时为 HTML 格式）         |
| `--cc`        |        |        | 抄送（CC）电子邮件地址（用逗号分隔）                |
| `--bcc`        |        |        | 密送（BCC）电子邮件地址（用逗号分隔）                |
| `--html`       |        |        | 将 `--body` 视为 HTML 内容（默认为纯文本）             |
| `--dry-run`     |        |        | 显示发送请求的内容（不实际执行操作）                |

## 示例

```bash
gws gmail +send --to alice@example.com --subject 'Hello' --body 'Hi Alice!'
gws gmail +send --to alice@example.com --subject 'Hello' --body 'Hi!' --cc bob@example.com
gws gmail +send --to alice@example.com --subject 'Hello' --body 'Hi!' --bcc secret@example.com
gws gmail +send --to alice@example.com --subject 'Hello' --body '<b>Bold</b> text' --html
```

## 注意事项

- 该命令会自动处理 RFC 2822 格式和 Base64 编码。
- 如需添加附件，请使用相应的 API：`gws gmail users messages send --json '...'`

> [!警告！]  
> 这是一个**写入操作**命令——执行前请务必获得用户的确认。

## 相关文档

- [gws-shared](../gws-shared/SKILL.md) — 全局参数和认证设置  
- [gws-gmail](../gws-gmail/SKILL.md) — 所有与发送、读取和管理电子邮件相关的命令