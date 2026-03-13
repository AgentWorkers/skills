---
name: recipe-forward-labeled-emails
version: 1.0.0
description: "查找带有特定标签的Gmail邮件，并将它们转发到另一个地址。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-gmail"]
---
# 转发带有标签的 Gmail 消息

> **先决条件：** 需要安装并加载以下工具才能执行此操作：`gws-gmail`

查找带有特定标签的 Gmail 消息，并将其转发到另一个地址。

## 步骤

1. 查找带有标签的消息：`gws gmail users messages list --params '{"userId": "me", "q": "label:needs-review"}' --format table`
2. 获取消息内容：`gws gmail users messages get --params '{"userId": "me", "id": "MSG_ID"}'`
3. 通过新邮件转发：`gws gmail +send --to manager@company.com --subject '转发：[原始主题]' --body '转发给您审核：

[原始消息内容]'`