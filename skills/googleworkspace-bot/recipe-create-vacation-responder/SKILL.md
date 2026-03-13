---
name: recipe-create-vacation-responder
version: 1.0.0
description: "启用Gmail的“外出办公”自动回复功能，并设置自定义回复内容和日期范围。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-gmail"]
---
# 设置 Gmail 休假自动回复功能

> **前提条件：** 需要安装并使用 `gws-gmail` 工具来执行此操作。

启用 Gmail 的自动回复功能，可以自定义回复内容和日期范围。

## 步骤：

1. 启用休假自动回复：  
   ```bash
   gws gmail users settings updateVacation --params '{"userId": "me"}' --json '{"enableAutoReply": true, "responseSubject": "外出办公", "responseBodyPlainText": "我将在 1 月 20 日之前不在办公室。如有紧急事务，请联系 backup@company.com.", "restrictToContacts": false, "restrictToDomain": false}'
   ```

2. 验证设置是否生效：  
   ```bash
   gws gmail users settings getVacation --params '{"userId": "me"}'
   ```

3. 停用休假自动回复：  
   ```bash
   gws gmail users settings updateVacation --params '{"userId": "me"}' --json '{"enableAutoReply": false}'
   ```