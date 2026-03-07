---
name: recipe-create-doc-from-template
version: 1.0.0
description: "复制一个 Google 文档模板，填写内容，然后与协作者共享。"
metadata:
  openclaw:
    category: "recipe"
    domain: "productivity"
    requires:
      bins: ["gws"]
      skills: ["gws-drive", "gws-docs"]
---
# 从模板创建 Google 文档

> **先决条件：** 需要加载以下技能才能执行此操作：`gws-drive`、`gws-docs`

复制一个 Google 文档模板，填写内容，然后与协作者共享。

## 步骤

1. 复制模板：`gws drive files copy --params '{"fileId": "TEMPLATE_DOC_ID"}' --json '{"name": "项目简报 - 第二季度发布"}'`
2. 从响应中获取新文档的 ID：
3. 添加内容：`gws docs +write --document-id NEW_DOC_ID --text '## 项目：第二季度发布
### 目标
在第二季度末之前发布新功能。'
4. 与团队共享文档：`gws drive permissions create --params '{"fileId": "NEW_DOC_ID"}' --json '{"role": "writer", "type": "user", "emailAddress": "team@company.com"}'`