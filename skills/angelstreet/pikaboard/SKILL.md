---
name: pikaboard
description: "与 PikaBoard 任务管理 API 进行交互。该 API 用于创建、更新、列出或管理任务，适用于 AI 团队使用的基于代理（Agent-first）的看板系统。触发事件包括：任务（tasks）、看板（kanban）、看板界面（board）、待办事项（todo）和待处理事项列表（backlog）等。"
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
        message: "Create .env with DATABASE_PATH and API_TOKEN"
        label: "Configure environment"
---

# PikaBoard

这是一个以代理（agent）为中心的任务/看板（kanban）管理工具。**PikaBoard 是任务信息的权威来源。**

## 快速入门

安装完成后，启动服务器：
```bash
cd pikaboard/backend && npm start
```

通过 `http://localhost:3001` 访问看板。

## 配置

创建 `backend/.env` 文件：
```env
DATABASE_PATH=./pikaboard.db
API_TOKEN=your-secret-token
PORT=3001
```

将以下配置添加到您的 `TOOLS.md` 文件中：
```markdown
## PikaBoard
- **API:** http://localhost:3001/api/
- **Token:** your-secret-token
```

## 任务操作命令

- **按 ID 查看任务**：`task 12` 或 `#12`
- **将任务状态更改为“已完成”**：`move #12 to done`
- **创建新任务**：`create task "Fix bug"`

## API 参考

请参阅 `references/api.md` 以获取完整的 API 文档。

### 常见操作

- **列出所有任务**：```bash
curl -H "Authorization: Bearer $TOKEN" $API/tasks
```
- **创建新任务**：```bash
curl -X POST -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"name":"Fix bug","status":"inbox","priority":"high"}' \
  $API/tasks
```
- **更新任务状态**：```bash
curl -X PATCH -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"status":"done"}' \
  $API/tasks/123
```

## 枚举类型（Enums）

| 字段 | 值        |
|-------|------------|
| status | `inbox`, `up_next`, `in_progress`, `in_review`, `done` |
| priority | `low`, `medium`, `high`, `urgent` |

## 多代理设置

每个代理都可以拥有自己的看板。可以使用 `board_id` 参数来指定看板：
```bash
curl "$API/tasks?board_id=6" -H "Authorization: Bearer $TOKEN"
```

看板分配示例：
- 看板 1：Pika（主看板）
- 看板 2：Tortoise（个人看板）
- 看板 3：Sala（工作看板）
- 看板 4：Evoli（VirtualPyTest）
- 看板 5：Psykokwak（EZPlanning）
- 看板 6：Bulbi（PikaBoard）
- 看板 7：Mew（创意看板）