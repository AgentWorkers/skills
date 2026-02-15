---
name: sandboxer
version: 1.0.0
description: 通过 **Sandboxer** 将编码任务分配到 **tmux** 会话中。当您需要在工作区仓库中创建 **Claude Code**、**Gemini**、**OpenCode**、**bash** 或 **lazygit** 会话，监控它们的进度，或向它们发送命令时，可以使用此方法。
---

# Sandboxer — 将任务分配到 Tmux 会话中

> **高级用户技能。** Sandboxer 允许代理程序完全访问服务器上的 tmux 会话、工作区文件以及终端输出。适用于运行在具有 root 权限的专用 AI 机器；不适用于共享或不受信任的环境。

Sandboxer 运行在 `localhost:8081` 上，无需对本地主机进行身份验证。

## 快速操作：分配任务

```bash
# 1. Spawn a Claude session in a repo
curl "localhost:8081/api/create?type=claude&dir=/root/workspaces/AGENT/data/repos/PROJECT"

# 2. Send it a task
curl "localhost:8081/api/send?session=SESSION_NAME&text=Fix+the+failing+tests"

# 3. Check progress
curl "localhost:8081/api/session-monitor?session=SESSION_NAME"

# 4. Kill when done
curl "localhost:8081/api/kill?session=SESSION_NAME"
```

会话类型：`claude`、`bash`、`lazygit`、`gemini`、`opencode`

## 工作区结构

Sandboxer 管理 `/root/workspaces/`——这是一个包含所有代理工作区的单一 Git 仓库。

```
/root/workspaces/                          ← git repo (Sandboxer commits this)
├── .gitignore                             ← tracks only .md, .gitignore, cronjobs/
├── <agent-name>/                          ← one folder per OpenClaw agent
│   ├── AGENTS.md                          ← agent behavior rules
│   ├── SOUL.md, USER.md, TOOLS.md         ← agent identity & config
│   ├── MEMORY.md                          ← curated long-term memory
│   ├── TODO.md                            ← workspace task list (P1/P2/P3)
│   ├── CLAUDE.md                          ← coding rules for this workspace
│   ├── memory/YYYY-MM-DD.md               ← daily memory logs
│   ├── cronjobs/                          ← cron configs (tracked by git)
│   └── data/
│       └── repos/                         ← software projects (git clones)
│           ├── <project-a>/               ← separate git repo
│           │   ├── CLAUDE.md              ← project-specific coding rules
│           │   └── ...source code...
│           └── <project-b>/
```

### 主要规则：
- **`data/repos/` 包含独立的 Git 仓库**——每个项目都有自己的 `.git` 文件、分支和远程仓库
- **工作区的 `.gitignore` 文件会排除 `data/` 目录**——仓库内容保留在各自的 Git 仓库中，不会被纳入工作区的提交中
- **工作区的 Git 仓库仅跟踪以下文件类型**：`.md` 文件、`.gitignore` 文件以及 `cronjobs/` 文件
- **在将任务分配到会话之前，务必在工作区和仓库中读取 `CLAUDE.md` 和 `AGENTS.md` 文件**

## API 参考

| API 端点 | 功能 |
|----------|------|
| `GET /api/sessions` | 列出所有会话（状态：运行中/空闲/已完成/出错） |
| `GET /api/create?type=T&dir=D` | 创建新的会话 |
| `GET /api/session-monitor?session=S` | 查看会话的最后 20 行内容、状态及持续时间 |
| `GET /api/capture?session=S` | 获取完整的终端输出 |
| `GET /api/send?session=S&text=T` | 向会话发送按键输入 |
| `GET /api/forward?session=S&task=T` | 先执行 `Ctrl+C` 然后发送任务 |
| `GET /api/kill?session=S` | 终止会话 |
| `GET /api/workspaces` | 列出所有工作区（及其对应的 Git 仓库） |
| `GET /api/workspace-repos?workspace=W` | 列出工作区中的 Git 仓库 |
| `GET /api/repo-tree?path=P` | 查看仓库的文件结构及 Git 状态 |
| `GET/POST /api/workspace/W/file/PATH` | 读写工作区文件 |
| `POST /api/auto-commit?workspace=W` | 提交工作区的更改 |

`POST /api/create` 接受包含 `notify_url` 的 JSON 数据——当会话完成时会触发该接口。