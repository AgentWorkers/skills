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

> **前提条件：** 请阅读 `../gws-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。如果文件缺失，请运行 `gws generate-skills` 生成该文件。

**发送电子邮件**

## 使用方法

```bash
gws gmail +send --to <EMAIL> --subject <SUBJECT> --body <TEXT>
```

## 参数

| 参数 | 是否必需 | 默认值 | 说明 |
|------|----------|---------|-------------|
| `--to` | ✓ | — | 收件人电子邮件地址 |
| `--subject` | ✓ | — | 电子邮件主题 |
| `--body` | ✓ | — | 电子邮件正文（纯文本） |

## 示例

```bash
gws gmail +send --to alice@example.com --subject 'Hello' --body 'Hi Alice!'
```

## 提示：
- 该命令会自动处理 RFC 2822 格式和 Base64 编码。
- 如果需要处理 HTML 正文、附件或抄送/密送功能，请使用原始的 API：
  - 示例：`gws gmail users messages send --json '...'`

> **注意：**  
> 这是一个**写入操作**——执行前请务必获得用户的确认。

## 参考资料：
- [gws-shared](../gws-shared/SKILL.md) — 全局参数和身份验证设置
- [gws-gmail](../gws-gmail/SKILL.md) — 所有与发送、读取和管理电子邮件相关的命令