---
name: vibes
description: **AI编程代理的社交互动层**  
可以查看当前正在编程的用户，并分享即时的互动信息（如代码状态、反馈等）。
homepage: https://binora.github.io/vibes/
user-invocable: true
allowed-tools:
  - mcp__vibes__vibes
metadata: {"openclaw":{"mcp":{"command":"npx","args":["vibes-mcp@latest"],"env":{"VIBES_API_URL":"https://vibes-api.fly.dev"}}}}
---

# 开发者的动态

查看或发布正在编程的开发者的动态信息。

## 使用方法

使用 `vibes` MCP 工具来查看其他人分享的内容：

- `/vibes` — 查看最近的动态信息以及哪些开发者在线
- `/vibes "你的消息"` — 发布一条动态（最多 140 个字符）

如果用户在 `/vibes` 后提供了消息，请将该消息作为参数传递，以便发布一条新的动态。

## 你将看到的内容

```
💭 12 others vibing · 47 drops this week

"it works and I don't know why"      3m
"mass-deleted 400 lines"             8m
"shipping at 2am again"             12m
```

## 特点

- **匿名性**：无需注册账户，无需创建个人资料
- **临时性**：动态信息会在 24 小时后自动删除
- **按代理划分**：每个开发者只能看到属于自己的社区动态
- **资源消耗低**：每次调用大约消耗 180 个令牌

## 使用限制

- 每小时最多可发布 5 条动态
- 每条动态最多 140 个字符

$ARGUMENTS