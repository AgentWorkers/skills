---
name: recipe-share-doc-and-notify
version: 1.0.0
description: "将一个具有编辑权限的 Google Docs 文档分享出去，并通过电子邮件将链接发送给协作者。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-drive", "gws-docs", "gws-gmail"]
---
# 共享 Google 文档并通知协作者

> **先决条件：** 需要安装以下工具才能执行此操作：`gws-drive`、`gws-docs`、`gws-gmail`

将 Google 文档设置为可编辑状态，并通过电子邮件将链接发送给协作者。

## 步骤

1. 查找文档：`gws drive files list --params '{"q": "name contains '\''Project Brief'\'' and mimeType = '\''application/vnd.google-apps.document'\''"}'`
2. 设置文档的编辑权限：`gws drive permissions create --params '{"fileId": "DOC_ID"}' --json '{"role": "writer", "type": "user", "emailAddress": "reviewer@company.com"}'`
3. 通过电子邮件发送链接：`gws gmail +send --to reviewer@company.com --subject '请查看：项目概述' --body '我已经将项目概述共享给了您：https://docs.google.com/document/d/DOC_ID'`