---
name: recipe-create-gmail-filter
version: 1.0.0
description: "创建一个Gmail过滤器，以便自动对收到的邮件进行标记、加星或分类。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-gmail"]
---
# 创建一个Gmail过滤器

> **先决条件：** 需要加载以下技能才能执行此操作：`gws-gmail`

创建一个Gmail过滤器，以便自动对收到的邮件进行标记、加星或分类。

## 步骤

1. 列出现有的标签：`gws gmail users labels list --params '{"userId": "me"}' --format table`
2. 创建一个新的标签：`gws gmail users labels create --params '{"userId": "me"}' --json '{"name": "Receipts"}'`
3. 创建一个过滤器：`gws gmail users settings filters create --params '{"userId": "me"}' --json '{"criteria": {"from": "receipts@example.com"}, "action": {"addLabelIds": ["LABEL_ID"], "removeLabelIds": ["INBOX"]}}'`
4. 验证过滤器：`gws gmail users settings filters list --params '{"userId": "me"}' --format table`