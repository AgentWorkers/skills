---
name: bird
description: X/Twitter CLI：通过cookies或Sweetistics工具实现数据的读取、搜索和发布功能。
homepage: https://bird.fast
metadata: {"clawdbot":{"emoji":"🐦","requires":{"bins":["bird"]},"install":[{"id":"brew","kind":"brew","formula":"steipete/tap/bird","bins":["bird"],"label":"Install bird (brew)"}]}}
---

# bird

使用 `bird` 命令可以读取/搜索信息以及发布推文/回复。

**快速入门：**
- `bird whoami`  查看当前用户信息
- `bird read <url-or-id>`  读取指定 URL 或 ID 的内容
- `bird thread <url-or-id>`  查看指定 URL 或 ID 的讨论线程
- `bird search "query" -n 5`  搜索指定关键词（返回前 5 条结果）

**发布内容（请先获得用户授权）：**
- `bird tweet "text"`  发布新推文
- `bird reply <id-or-url> "text"`  回复指定 ID 或 URL 的推文

**授权方式：**
- 浏览器 cookies（默认：Firefox/Chrome）
- Sweetistics API：设置 `SWEETISTICS_API_KEY` 或使用 `--engine sweetistics`
- 检查授权来源：`bird check`