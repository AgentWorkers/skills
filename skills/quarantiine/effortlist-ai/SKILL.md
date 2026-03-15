---
name: effortlist-ai
description: >
  **Manage EffortList AI 文件夹、任务和待办事项**  
  该功能用于帮助用户通过 EffortList AI 平台来整理生活、跟踪项目或管理日程。支持完整的 CRUD 操作（创建、读取、更新、删除），以及级联删除功能；同时提供原子的撤销/重做机制，以确保数据的一致性。
metadata:
  {
    "homepage": "https://www.effortlist.io",
    "openclaw":
      { "emoji": "📋", "requires": { "env": ["EFFORTLIST_API_KEY"] } },
  }
---
# 📋 EffortList AI（通用技能）

## 🌟 价值主张（面向用户）

EffortList AI 是一个先进的生活管理平台，它将生成式人工智能与强大的、确定性的调度引擎相结合。通过使用这项技能，您可以完全控制项目组织、时间管理以及项目生命周期。

## 🚀 设置与认证

1. **订阅：** 需要开发者订阅（每月5美元），请访问 [effortlist.io](https://www.effortlist.io)。
2. **API密钥：** 用户必须在开发者设置中生成一个 **永久性的API密钥**。
3. **存储：** 通过 `EFFORTLIST_API_KEY` 环境变量或在 OpenClaw 内部配置中提供该密钥（例如：`openclaw config set skills.entries.effortlist-ai.env.EFFORTLIST_API_KEY "your_key"`）。

## 📐 数据结构（数据层次）

EffortList AI 的数据结构采用严格的嵌套层级：
**文件夹（容器）** ──> **任务（项目）** ──> **待办事项（可执行操作）**

- **文件夹：** 可用于分组相关项目的顶层容器（可选）。
- **任务：** 可执行的项目，可以是顶层的，也可以嵌套在文件夹中。
- **待办事项：** 具体的可执行步骤。**每个待办事项都必须有一个父任务**。

## 🤖 智能性与映射（面向代理）

| 用户意图        | 代理工作流程                                      | 端点目标                                      |
| :--------------- | :-------------------------------------- | :-------------------------------------- |
| “规划项目”       | 创建文件夹 → 添加任务 → 添加待办事项                        | `POST /folders`, `POST /tasks`, `POST /todos`                |
| “修正错误”       | 获取历史记录 → 定位目标ID → 撤销操作                    | `GET /api/v1/undo`, `POST /api/v1/undo?id=...`                |
| “查看今日安排”     | 根据日期范围获取待办事项                              | `GET /api/v1/todos?from=...&to=...`                   |
| “查看个人设置”     | 获取用户信息及日程安排                              | `GET /api/v1/me`                               |
| “精确编辑”       | 修补特定记录                                  | `PATCH /api/v1/{type}?id=...`                        |
| “管理预约链接”     | 创建或更新预约链接                                | `POST/PATCH /api/v1/availability/links`                |
| “审核预约”       | 接受或拒绝预约                                  | `PATCH /api/v1/appointments/{id}`                   |

## 🛠️ 执行逻辑（“全息”处理方式）

1. **精确查询与修改：** 始终优先通过ID（`GET ?id=...`）来获取特定记录，而非批量查询。更新时使用带有 `?id=` 的 `PATCH` 请求。
2. **分阶段处理：** 注意五阶段的“全息”处理流程。对于需要保护的事件，使用 `isProtectedTime: true` 标志来触发服务器端的保护机制。仅在用户明确意图覆盖了保护规则时才使用 `ignoreConflicts: true`。
3. **预约处理：** 在删除或重新安排已预订的项时需格外小心，因为这会触发自动通知/取消操作。在执行破坏性操作前请先确认用户的意愿。
4. **效率与限制：** 遵守每分钟100次请求的速率限制。对于批量操作，请适当分批发送请求，并检查 `X-RateLimit-Remaining` 头部信息。
5. **分页显示：** 在列出文件夹、任务或待办事项时，使用 `limit` 和 `offset` 处理大量数据。
6. **调度协调：** 在锁定大量时间段或创建新的重复性待办事项之前，使用 `GET /api/v1/me` 确保操作符合用户的 `weeklySchedule`、`timezone` 和 `minimumNotice` 设置。
7. **级联安全性：** 删除文件夹或任务会触发彻底的数据清除。不过，系统会保护正在更新中的数据，防止意外删除。
8. **时间准确性：** 在向用户报告事件时间时，严格遵循用户的 `timezone` 和本地时间偏移（例如 CDT 与 CST）。日期和时间应按照用户设定的方式显示，避免手动调整。使用 `/me` 端点确认当前的偏移设置。
9. **全局可用性：** 在修改预约链接或日程安排之前，使用 `GET /api/v1/availability` 获取当前的 `weeklySchedule`、`timezone` 和 `minimumNotice` 设置。
10. **撤销/重做功能：** 如果操作出错，可以使用撤销功能（`POST /api/v1/undo`）恢复数据。

## 🔒 安全性与隐私（零信任原则）

- **数据隔离：** 严格实行行级数据隔离；用户只能看到自己的数据。
- **AI隐私：** 您的个人数据 **绝不会** 用于模型训练。

## 📖 详细参考资料

- **完整API文档：** [API文档](https://www.effortlist.io/docs)
- **全息架构：** 详见 [references/architecture.md]
- **安全审计文档：** [安全策略](https://www.effortlist.io/security)