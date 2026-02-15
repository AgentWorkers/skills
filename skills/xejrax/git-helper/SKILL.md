---
name: git-helper
description: "常见的 Git 操作（状态查看、拉取代码、推送代码、创建分支、查看日志）"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔀",
        "requires": { "bins": ["git"] },
        "install": [],
      },
  }
---

# Git 辅助工具

本工具提供了一些常见的 Git 操作功能，为常用的 Git 命令（如查看状态、拉取代码、推送代码、分支管理以及查看日志等）提供了便捷的封装。

## 命令

```bash
# Show working tree status
git-helper status

# Pull latest changes
git-helper pull

# Push local commits
git-helper push

# List or manage branches
git-helper branch

# View commit log with optional limit
git-helper log [--limit 10]
```

## 安装

无需安装。系统上通常已经预装了 `git` 工具。