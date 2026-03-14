---
name: recipe-save-email-attachments
version: 1.0.0
description: "查找包含附件的Gmail邮件，并将它们保存到Google Drive文件夹中。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-gmail", "gws-drive"]
---
# 将Gmail附件保存到Google Drive

> **先决条件：** 需要安装以下工具或库才能执行此操作：`gws-gmail`、`gws-drive`

本教程将指导您如何查找包含附件的Gmail邮件，并将其保存到Google Drive文件夹中。

## 步骤

1. 查找包含附件的邮件：  
   `gws gmail users messages list --params '{"userId": "me", "q": "has:attachment from:client@example.com"}' --format table`

2. 获取邮件详细信息：  
   `gws gmail users messages get --params '{"userId": "me", "id": "MESSAGE_ID"}`

3. 下载附件：  
   `gws gmail users messages attachments get --params '{"userId": "me", "messageId": "MESSAGE_ID", "id": "ATTACHMENT_ID"}`

4. 将附件上传到Google Drive文件夹：  
   `gws drive +upload --file ./attachment.pdf --parent FOLDER_ID`