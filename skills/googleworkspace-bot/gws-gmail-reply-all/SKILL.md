---
name: gws-gmail-reply-all
version: 1.0.0
description: "Gmail：对消息使用“回复全部”功能（会自动处理消息的线程结构）。"
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws gmail +reply-all --help"
---
# gmail +reply-all

> **前提条件：** 请阅读 `../gws-shared/SKILL.md` 以了解认证、全局参数和安全规则。如果文件缺失，请运行 `gws generate-skills` 命令来生成它。

**功能说明：**  
该命令用于回复一条邮件，并自动处理邮件的多线程（即同时发送给多个收件人）。  

## 使用方法  

```bash
gws gmail +reply-all --message-id <ID> --body <TEXT>
```  

## 常用参数  

| 参数          | 是否必填 | 默认值 | 说明                          |
|---------------|---------|---------|--------------------------------------------|
| `--message-id`    | ✓       | —       | 需要回复的 Gmail 邮件 ID                |
| `--body`       | ✓       | —       | 回复内容（纯文本或使用 `--html` 选项的 HTML 格式）       |
| `--from`       | —       | —       | 发件人地址（用于“以……身份发送”或设置别名；省略则使用默认账户地址） |
| `--to`        | —       | —       | 需要添加的收件人邮箱地址（用逗号分隔）             |
| `--cc`        | —       | —       | 需要添加的抄送收件人邮箱地址（用逗号分隔）             |
| `--bcc`        | —       | —       | 需要添加的密送收件人邮箱地址（用逗号分隔）             |
| `--remove`      | —       | —       | 从回复邮件中排除某些收件人（用逗号分隔的邮箱地址）         |
| `--html`       | —       | —       | 以 HTML 格式发送回复（保留原始邮件的样式；`--body` 参数将被视为 HTML 内容） |
| `--dry-run`     | —       | —       | 显示即将发送的请求内容（不实际执行操作）             |

## 使用示例  

```bash
gws gmail +reply-all --message-id 18f1a2b3c4d --body 'Sounds good to me!'
gws gmail +reply-all --message-id 18f1a2b3c4d --body 'Updated' --remove bob@example.com
gws gmail +reply-all --message-id 18f1a2b3c4d --body 'Adding Eve' --cc eve@example.com
gws gmail +reply-all --message-id 18f1a2b3c4d --body 'Adding Dave' --to dave@example.com
gws gmail +reply-all --message-id 18f1a2b3c4d --body 'Reply' --bcc secret@example.com
gws gmail +reply-all --message-id 18f1a2b3c4d --body '<i>Noted</i>' --html
```  

## 注意事项：  
- 回复内容会同时发送给发件人和所有原始的“收件人”及“抄送”收件人。  
- 使用 `--to` 参数可以添加额外的收件人。  
- 使用 `--cc` 参数可以添加新的抄送收件人。  
- 使用 `--bcc` 参数可以添加需要保密的密送收件人。  
- 如果在排除某些收件人后，`--to` 参数指定的收件人仍然存在，或者添加了新的收件人，命令将失败。  

## 相关文档：  
- [gws-shared](../gws-shared/SKILL.md) — 全局参数和认证相关设置  
- [gws-gmail](../gws-gmail/SKILL.md) — 所有与发送、读取和管理邮件相关的命令