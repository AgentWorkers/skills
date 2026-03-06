---
name: gws-gmail
version: 1.0.0
description: "Gmail：发送、阅读和管理电子邮件。"
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws gmail --help"
---
# gmail (v1)

> **前提条件：** 阅读 `../gws-shared/SKILL.md` 以了解认证、全局参数和安全规则。如果文件缺失，请运行 `gws generate-skills` 来生成它。

```bash
gws gmail <resource> <method> [flags]
```

## 帮助命令

| 命令 | 描述 |
|---------|-------------|
| [`+send`](../gws-gmail-send/SKILL.md) | 发送电子邮件 |
| [`+triage`](../gws-gmail-triage/SKILL.md) | 显示未读收件箱的摘要（发件人、主题、日期） |
| [`+watch`](../gws-gmail-watch/SKILL.md) | 监控新邮件并将其以 NDJSON 格式流式传输 |

## API 资源

### users

  - `getProfile` — 获取当前用户的 Gmail 信息。
  - `stop` — 停止接收指定用户邮箱的推送通知。
  - `watch` — 为指定用户邮箱设置或更新推送通知。
  - `drafts` — 对 “drafts” 资源进行操作。
  - `history` — 对 “history” 资源进行操作。
  - `labels` — 对 “labels” 资源进行操作。
  - `messages` — 对 “messages” 资源进行操作。
  - `settings` — 对 “settings” 资源进行操作。
  - `threads` — 对 “threads” 资源进行操作。

## 查找命令

在调用任何 API 方法之前，请先查看其文档：

```bash
# Browse resources and methods
gws gmail --help

# Inspect a method's required params, types, and defaults
gws schema gmail.<resource>.<method>
```

使用 `gws schema` 的输出来构建你的 `--params` 和 `--json` 参数。