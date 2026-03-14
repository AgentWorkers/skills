---
name: nerve-kanban
description: 与 Nerve Kanban 平台的后端 API 进行交互。支持创建（Create）、读取（Read）、更新（Update）和删除（Delete）任务（CRUD 操作），管理工作流程（执行、批准、拒绝、中止任务），处理提案（Proposals），以及配置 Kanban 画布（Board Settings）。所有相关接口都位于 Nerve 服务器的 `/api/kanban` 路径下。
---
# Nerve Kanban API 技能

使用此技能通过其 REST API 管理 Nerve Kanban 平板上的任务。

## 基本 URL

所有端点都相对于 Nerve 服务器的地址（例如 `http://localhost:3000`）。在每个路径前加上 `/api/kanban` 前缀。

## 核心概念

- **任务** 的流程为：`待办列表 (backlog)` → `进行中 (in-progress)` → `审核中 (review)` → `已完成 (done)`（或 `取消 (cancelled)`）。
- **CAS 版本控制**：更新和重新排序任务时需要提供当前的 `version` 号。如果提供的版本号与服务器上的最新任务版本不一致，将会收到 `409 Version Conflict` 错误。请重新读取请求并重试。
- **工作流操作** 会确保任务状态之间的转换是有效的。您无法执行已经处于审核中的任务。
- **提案 (Proposals)** 允许代理（agents）建议创建或更新任务。操作员（operator）或自动策略（auto-policy）会批准或拒绝这些提案。
- **执行者 (Actors)** 可以是 `"operator"` 或 `"agent:<name>"`。

## 快速参考

| 操作 | 方法 | 路径 |
|---|---|---|
| 列出任务 | GET | `/api/kanban/tasks` |
| 创建任务 | POST | `/api/kanban/tasks` |
| 更新任务 | PATCH | `/api/kanban/tasks/:id` |
| 删除任务 | DELETE | `/api/kanban/tasks/:id` |
| 重新排序/移动任务 | POST | `/api/kanban/tasks/:id/reorder` |
| 执行任务（启动代理） | POST | `/api/kanban/tasks/:id/execute` |
| 批准任务（从审核中转到已完成） | POST | `/api/kanban/tasks/:id/approve` |
| 拒绝任务（从审核中转到待办列表） | POST | `/api/kanban/tasks/:id/reject` |
| 中止任务（从进行中转到待办列表） | POST | `/api/kanban/tasks/:id/abort` |
| 完成任务（通过 webhook） | POST | `/api/kanban/tasks/:id/complete` |
| 列出提案 | GET | `/api/kanban/proposals` |
| 创建提案 | POST | `/api/kanban/proposals` |
| 批准提案 | POST | `/api/kanban/proposals/:id/approve` |
| 拒绝提案 | POST | `/api/kanban/proposals/:id/reject` |
| 获取配置 | GET | `/api/kanban/config` |
| 更新配置 | PUT | `/api/kanban/config` |

## 常见用法

### 创建和执行任务
1. 使用 `POST /api/kanban/tasks` 并传递 `{ "title": "...", "description": "..." }`，系统会返回任务的 `id` 和 `version`。
2. 使用 `POST /api/kanban/tasks/:id/execute`，任务状态会变为 `进行中`，同时会启动一个代理会话。
3. 代理会话完成后，任务会自动变为 `审核中` 状态。
4. 使用 `POST /api/kanban/tasks/:id/approve`，任务状态会变为 `已完成`。

### 处理版本冲突
在发送更新或重新排序请求时，务必包含 `version` 号。如果收到 `409 Version Conflict` 错误，请从响应中获取最新的 `version` 号，然后使用正确的版本号重新尝试。

### 提出变更（作为代理）
无法直接修改任务的代理应使用提案功能：
1. 使用 `POST /api/kanban/proposals` 并传递 `{ "type": "create", "payload": { "title": "...", "proposedBy": "agent:myname" }`。
2. 操作员会通过 `/api/kanban/proposals/:id/approve` 或 `/api/kanban/proposals/:id/reject` 来批准或拒绝提案。

## 完整 API 参考

有关完整的端点文档、类型定义、错误代码和示例请求，请参阅 [references/api.md](references/api.md)。