---
name: recipe-save-email-to-doc
version: 1.0.0
description: "将 Gmail 消息正文保存到 Google 文档中，以便存档或参考。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-gmail", "gws-docs"]
---
# 将Gmail邮件保存到Google Docs中

> **前提条件：** 需要安装并使用以下工具来执行此操作：`gws-gmail`、`gws-docs`

将Gmail邮件的正文保存到Google Docs中，以便归档或参考。

## 步骤

1. 查找邮件：`gws gmail users messages list --params '{"userId": "me", "q": "subject:important from:boss@company.com"}' --format table`
2. 获取邮件内容：`gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID"}`
3. 使用邮件内容创建一个新的文档：`gws docs documents create --json '{"title": "保存的邮件 - 重要更新"}'`
4. 将邮件正文写入文档：`gws docs +write --document-id DOC_ID --text '发件人: boss@company.com
主题: 重要更新

[邮件正文]'`