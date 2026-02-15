---
name: beszel
description: 通过 Beszel (PocketBase) 监控家庭实验室中的服务器。
metadata: {"clawdbot":{"emoji":"📊","requires":{"bins":["node"]}}}
---

# Beszel 监控

用于检查本地服务器的状态。

## 使用方法
- `beszel status` - 查看所有系统的状态
- `beszel containers` - 按 CPU 使用率列出占用资源最多的容器

## 命令
```bash
# Get status
source ~/.zshrc && ~/clawd/skills/beszel/index.js status

# Get container stats
source ~/.zshrc && ~/clawd/skills/beszel/index.js containers
```