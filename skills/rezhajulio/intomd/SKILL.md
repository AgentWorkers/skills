---
name: intomd
version: 1.0.0
description: 使用 `into.md` 服务来获取并转换任何文档 URL 为 Markdown 格式。
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["curl"]}}}
---

# intomd

使用 `intomd` 通过 into.md 格式从文档网站获取干净的 Markdown 内容。

## 使用方法

```bash
# Fetch markdown
curl -sL "https://into.md/$1"
```

## 示例

```bash
intomd https://zod.dev
```