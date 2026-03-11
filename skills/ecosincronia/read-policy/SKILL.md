---
name: read-policy
description: 通过本地的 Supabase Docker 堆栈，从 PostgreSQL 读取 OpenClaw 的策略信息。这些策略信息可用于查看诸如 `auto_approve`、`priority_routing` 或 `available_skills` 等关键参数。
metadata: {"clawdbot":{"notes":["Reads public.openclaw_policies through docker exec on supabase-db"]}}
---
# 读取策略信息

从实际的 OpenClaw 数据库中读取策略值。

## 命令

- 读取一个策略键  
  `{baseDir}/scripts/read-policy.sh get "auto_approve"`

- 列出所有策略键  
  `{baseDir}/scripts/read-policy.sh list`

## 注意事项

- 使用本地的 Docker 容器 `supabase-db`  
- 从 `public.openclaw_policies` 文件夹中读取数据  
- 仅用于查看策略信息