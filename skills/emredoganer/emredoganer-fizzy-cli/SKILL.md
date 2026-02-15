---
name: fizzy-cli
description: 通过 TypeScript CLI 和个人访问令牌（Personal Access Token）来管理 Fizzy Kanban 任务板、卡片、评论、标签以及各个步骤。当您需要从终端创建或管理 Fizzy 卡片，或者将 Fizzy 的自动化功能集成到 Clawdbot 工作流程中时，可以使用此工具。
---

# Fizzy CLI

该仓库包含一个独立的命令行工具（CLI）。

## 安装

```bash
npm i -g @emredoganer/fizzy-cli
```

## 认证

在 Fizzy 中生成一个个人访问令牌：

```bash
fizzy auth login
```

（系统会提示您输入令牌。）