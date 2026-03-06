---
name: gws-gmail-triage
version: 1.0.0
description: "Gmail：显示未读收件箱的摘要信息（发件人、主题、日期）。"
metadata:
  openclaw:
    category: "productivity"
    requires:
      bins: ["gws"]
    cliHelp: "gws gmail +triage --help"
---
# gmail +triage

> **前提条件：** 请阅读 `../gws-shared/SKILL.md` 以了解认证信息、全局参数和安全规则。如果文件缺失，请运行 `gws generate-skills` 命令来生成该文件。

显示未读收件箱的摘要信息（发件人、主题、日期）

## 使用方法

```bash
gws gmail +triage
```

## 参数说明

| 参数 | 是否必填 | 默认值 | 说明 |
|------|----------|---------|-------------|
| `--max` | — | 20 | 显示的最大消息数量（默认值：20） |
| `--query` | — | — | Gmail 的搜索查询条件（默认值：`is:unread`） |
| `--labels` | — | — | 在输出结果中包含标签名称 |

## 示例

```bash
gws gmail +triage
gws gmail +triage --max 5 --query 'from:boss'
gws gmail +triage --format json | jq '.[].subject'
gws gmail +triage --labels
```

## 注意事项：

- 该工具仅用于读取邮件内容，不会修改用户的邮箱。
- 默认输出格式为表格形式。

## 相关文档：

- [gws-shared](../gws-shared/SKILL.md) — 全局参数和认证信息
- [gws-gmail](../gws-gmail/SKILL.md) — 所有发送、读取和管理电子邮件的命令