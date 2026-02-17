---
name: pikaboard
description: "与 PikaBoard 任务管理 API 进行交互。适用于创建、更新、列出或管理任务。专为 AI 团队设计的基于代理（Agent-first）的看板系统。触发事件包括：任务（tasks）、看板（kanban）、看板页面（board）、待办事项（todo）、待办列表（backlog）和冲刺（sprint）。"
metadata:
  openclaw:
    emoji: "📋"
    requires:
      bins: ["node", "npm"]
    install:
      - id: clone
        kind: git
        repo: https://github.com/angelstreet/pikaboard
        branch: main
        label: "Clone PikaBoard repository"
      - id: backend
        kind: script
        cwd: "pikaboard/backend"
        run: "npm install && npm run build"
        label: "Install backend dependencies"
      - id: frontend
        kind: script
        cwd: "pikaboard/frontend"
        run: "npm install && npm run build"
        label: "Build frontend"
      - id: env
        kind: prompt
        message: "Create .env with DATABASE_PATH and PIKABOARD_TOKEN"
        label: "Configure environment"
---
# PikaBoard

这是一个以代理（Agent）为中心的任务/看板（Kanban）管理工具。**PikaBoard 是任务管理的核心数据源。**

## 快速入门

安装完成后，启动服务器：
```bash
cd pikaboard/backend && npm start
```

通过 `http://localhost:3001` 访问仪表板。

## 配置

创建 `backend/.env` 文件：
```env
DATABASE_PATH=./pikaboard.db
PIKABOARD_TOKEN=your-secret-token
PORT=3001
```

将以下配置添加到您的 `TOOLS.md` 文件中：
```markdown
## PikaBoard
- **API:** http://localhost:3001/api/
- **Token:** your-secret-token
```

代理运行时变量：
```bash
export PIKABOARD_API="http://localhost:3001/api"
export PIKABOARD_TOKEN="your-secret-token"
export AGENT_NAME="bulbi"
```

## 任务命令

- **按 ID 查看任务**：
  - `task 12` 或 `#12` → 查看任务详情
- `move #12 to done` → 更改任务状态
- `create task "Fix bug"` → 创建新任务

## API 参考

请参阅 `backend/API.md` 以获取完整的 API 文档（统一规范文档）。

### 常用操作

- **列出任务**：
  ```bash
curl -H "Authorization: Bearer $PIKABOARD_TOKEN" "$PIKABOARD_API/tasks"
```

- **创建任务**：
  ```bash
curl -X POST -H "Authorization: Bearer $PIKABOARD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Fix bug","status":"inbox","priority":"high","tags":["bug","backend"]}' \
  "$PIKABOARD_API/tasks"
```

- **更新任务状态**：
  ```bash
curl -X PATCH -H "Authorization: Bearer $PIKABOARD_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}' \
  "$PIKABOARD_API/tasks/123"
```

## 枚举（Enumerations）

| 字段 | 值         |
|-------|------------|
| status | `inbox`, `up_next`, `in_progress`, `testing`, `in_review`, `done`, `rejected` |
| priority | `low`, `medium`, `high`, `urgent` |

## 代理入职流程（简化步骤）

使用辅助工具自动将每个代理分配到相应的看板上：

```bash
cd pikaboard
MY_BOARD_ID="$(
  ./skills/pikaboard/scripts/setup-agent-board.sh | sed -n 's/^MY_BOARD_ID=//p' | tail -n1
)"
export MY_BOARD_ID
```

该工具的功能包括：
- 读取 `PIKABOARD_API`, `PIKABOARD_TOKEN`, `AGENT_NAME`
- 根据 `BOARD_NAME`（默认为 `AGENT_NAME`）查找对应的看板
- 如果看板不存在，则创建该看板
- 输出 `MY_BOARD_ID=<id>`
- 验证 `GET /api/tasks?board_id=<id>&status=up_next` 的响应

（可选步骤）：
```bash
export BOARD_NAME="Bulbi"
export BOARD_ENV_FILE="$HOME/.openclaw/agents/bulbi/.pikaboard.env"
./skills/pikaboard/scripts/setup-agent-board.sh
```

## 多代理设置

每个代理都可以拥有自己的看板。可以使用 `board_id` 参数进行区分：
```bash
curl "$PIKABOARD_API/tasks?board_id=6" -H "Authorization: Bearer $PIKABOARD_TOKEN"
```

看板分配示例：
- 看板 1：Pika（用于主要任务）
- 看板 2：Tortoise（个人任务）
- 看板 3：Sala（工作相关任务）
- 看板 4：Evoli（用于虚拟测试）
- 看板 5：Psykokwak（用于计划管理）
- 看板 6：Bulbi（用于 PikaBoard 任务）
- 看板 7：Mew（用于创意任务）

## 验证步骤

在设置完成后，请运行以下命令进行验证：
```bash
# 1) API reachable
curl -s http://localhost:3001/health

# 2) Auth works
curl -s -H "Authorization: Bearer $PIKABOARD_TOKEN" "$PIKABOARD_API/boards"

# 3) Board mapping works
echo "$MY_BOARD_ID"

# 4) Agent can read own queue
curl -s -H "Authorization: Bearer $PIKABOARD_TOKEN" \
  "$PIKABOARD_API/tasks?board_id=$MY_BOARD_ID&status=up_next"
```