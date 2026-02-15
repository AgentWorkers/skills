---
name: basecamp-cli
description: 通过 TypeScript CLI 管理 Basecamp（使用 bc3 API 或 37signals Launchpad）中的项目、待办事项、消息以及团队讨论（campfires）。当您需要从终端列出/创建/更新 Basecamp 项目及待办事项，或者希望将 Basecamp 的自动化功能集成到 Clawdbot 工作流程中时，可以使用该工具。
---

# Basecamp CLI

这个仓库包含一个独立的命令行工具（CLI）。

## 安装

```bash
npm i -g @emredoganer/basecamp-cli
```

## 认证

在 37signals 的 Launchpad 中创建一个集成（OAuth 应用）：
- https://launchpad.37signals.com/integrations

之后，按照以下步骤操作：
```bash
basecamp auth configure --client-id <id> --redirect-uri http://localhost:9292/callback
export BASECAMP_CLIENT_SECRET="<secret>"
basecamp auth login
```

## 注意事项

- 该工具使用了 Basecamp 公布的 bc3-api 文档：https://github.com/basecamp/bc3-api
- `BASECAMP_CLIENT_SECRET` 这个密钥不会被 CLI 保存在磁盘上。