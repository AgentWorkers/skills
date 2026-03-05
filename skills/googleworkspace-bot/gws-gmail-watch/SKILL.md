---
name: gws-gmail-watch
version: 1.0.0
description: "Gmail：监控新邮件，并将它们以 NDJSON 格式流式传输。"
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws gmail +watch --help"
---
# gmail +watch

> **前提条件：** 阅读 `../gws-shared/SKILL.md` 以了解身份验证、全局参数和安全规则。如果文件缺失，请运行 `gws generate-skills` 生成该文件。

监控新邮件，并将它们以 NDJSON 格式输出。

## 使用方法

```bash
gws gmail +watch
```

## 参数说明

| 参数 | 是否必填 | 默认值 | 说明 |
|------|----------|---------|-------------|
| `--project` | — | — | 用于 Pub/Sub 资源的 GCP 项目 ID |
| `--subscription` | — | — | 现有的 Pub/Sub 订阅名称（跳过设置步骤） |
| `--topic` | — | — | 已授予 Gmail 推送权限的现有 Pub/Sub 主题 |
| `--label-ids` | — | — | 用逗号分隔的 Gmail 标签 ID（用于过滤，例如 INBOX、UNREAD） |
| `--max-messages` | — | 10 | 每次拉取的最大消息数 |
| `--poll-interval` | — | 5 | 拉取间隔（秒） |
| `--msg-format` | — | full | Gmail 消息格式：full（包含元数据）、minimal（仅包含基本信息）、raw（原始数据） |
| `--once` | — | — | 执行一次拉取后退出 |
| `--cleanup` | — | — | 退出时删除创建的 Pub/Sub 资源 |
| `--output-dir` | — | — | 将每条消息写入该目录下的单独 JSON 文件中 |

## 示例

```bash
gws gmail +watch --project my-gcp-project
gws gmail +watch --project my-project --label-ids INBOX --once
gws gmail +watch --subscription projects/p/subscriptions/my-sub
gws gmail +watch --project my-project --cleanup --output-dir ./emails
```

## 提示

- Gmail 监控功能会在 7 天后失效——请重新运行命令以续期。
- 如果未使用 `--cleanup` 选项，Pub/Sub 资源会在下次连接时继续存在。
- 按 Ctrl-C 可优雅地停止程序。

## 参考资料

- [gws-shared](../gws-shared/SKILL.md) — 全局参数和身份验证设置 |
- [gws-gmail](../gws-gmail/SKILL.md) — 所有发送、读取和管理邮件的命令