---
name: perry-coding-agents
description: 将编码任务分配到 Perry 工作空间中的 OpenCode 或 Claude Code 平台上。适用于开发工作、代码审查（PR），或任何需要隔离环境的编码任务。
metadata: {"clawdbot":{"emoji":"🛠️"}}
---

# Perry 编码代理

将任务调度到 Perry 工作空间中的 OpenCode/Claude Code 服务。

## 规则
- **务必先创建 dex 任务** — 在任何调度操作之前，无一例外
- **不设置强制超时** — 任务在后台运行，由代理完成
- **使用 IP 地址** — 容器环境中的 MagicDNS 服务可能无法正常使用（请通过 `tailscale status` 命令查询 IP 地址）
- **每个 Pull Request（PR）对应一个任务** — 相同的会话会持续执行，直到任务完成
- **重用会话** — OpenCode 会在 `~/.opencode/` 目录中保存会话信息
- **严禁直接编写代码** — 必须通过代理来执行所有编码任务

## 命令
```bash
# OpenCode (primary)
ssh -o StrictHostKeyChecking=no workspace@<IP> "cd ~/<project> && /home/workspace/.opencode/bin/opencode run 'task'" &

# Claude Code (needs TTY)
ssh -t workspace@<IP> "cd ~/<project> && /home/workspace/.local/bin/claude 'task'"
```

## 调度模式
```bash
WAKE_IP=$(tailscale status --self --json | jq -r '.Self.TailscaleIPs[0]')

ssh -o StrictHostKeyChecking=no workspace@<IP> "cd ~/<project> && /home/workspace/.opencode/bin/opencode run 'Your task.

When done: curl -X POST http://${WAKE_IP}:18789/hooks/wake -H \"Content-Type: application/json\" -H \"Authorization: Bearer <hooks-token>\" -d \"{\\\"text\\\": \\\"Done: summary\\\", \\\"mode\\\": \\\"now\\\"}\"
'" &
```

## 任务跟踪
在调度任务之前，需要提供以下信息：工作空间 IP、分支名称、任务目标以及完成标准。任务会一直持续执行，直到持续集成（CI）系统显示“通过”状态，并附上结果总结。

## 示例：完整的 Pull Request 流程
```bash
# 1. Create task
# Track: workspace feat1 (100.109.173.45), branch feat/auth, goal: add auth

# 2. Get wake info
WAKE_IP=$(tailscale status --self --json | jq -r '.Self.TailscaleIPs[0]')

# 3. Dispatch (background, no timeout)
ssh -o StrictHostKeyChecking=no workspace@100.109.173.45 "cd ~/perry && /home/workspace/.opencode/bin/opencode run 'Add bearer token auth to all API endpoints. Create PR when done.

When finished: curl -X POST http://${WAKE_IP}:18789/hooks/wake -H \"Content-Type: application/json\" -H \"Authorization: Bearer <token>\" -d \"{\\\"text\\\": \\\"Done: Auth PR created\\\", \\\"mode\\\": \\\"now\\\"}\"
'" &

# 4. Wake received → check CI
ssh workspace@100.109.173.45 "cd ~/perry && gh pr checks 145"

# 5. CI fails → dispatch follow-up (same task, agent has context)
ssh -o StrictHostKeyChecking=no workspace@100.109.173.45 "cd ~/perry && /home/workspace/.opencode/bin/opencode run 'CI failing: test/auth.test.ts line 42. Fix and push.

When fixed: curl -X POST http://${WAKE_IP}:18789/hooks/wake ...'" &

# 6. CI green → complete task with result
```

## 故障排除
- **无法连接目标服务**：使用 `tailscale status | grep <名称>` 命令进行检查
- **命令找不到**：请使用完整路径（`/home/workspace/.opencode/bin/opencode`）
- **代理未启动**：检查 IP 地址或令牌信息，并使用 `curl` 命令进行测试