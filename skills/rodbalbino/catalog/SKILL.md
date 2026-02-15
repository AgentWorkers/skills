---
name: catalog
description: 简易工作室目录（Hello World示例）
user-invocable: true
---

当用户询问服务或价格时，执行一个本地命令以返回 JSON 数据，然后以简洁明了的方式回复用户。

请使用命令执行工具（Exec Tool）来运行以下命令：

```
node {baseDir}/catalog.js
```

该命令会返回一个包含 `name`（服务名称）、`price`（价格）和 `duration`（服务时长）的 JSON 列表。

请不要自行编造数据值：只需使用返回的 JSON 数据即可。