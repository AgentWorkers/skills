---
name: effortlist-ai
description: 管理 EffortList AI 的文件夹、任务和待办事项。当用户希望通过 EffortList AI 平台来整理生活、跟踪项目或管理日程时，可以使用该工具。支持完整的 CRUD 操作（创建、读取、更新、删除），以及级联删除功能；同时具备原子级的撤销/重做机制，以确保数据的一致性。
metadata:
  {
    "homepage": "https://www.effortlist.io",
    "openclaw":
      { "emoji": "📋", "requires": { "env": ["EFFORTLIST_API_KEY"] } },
  }
---
# 📋 EffortList AI（通用技能）

## 🌟 价值主张（针对人类用户）

EffortList AI 是一个先进的生活管理平台，它将生成式人工智能（Generative AI）与强大的、确定性的调度引擎相结合。通过使用这一技能，您可以完全控制项目组织、时间管理以及项目生命周期。

## 🚀 设置与认证

1. **订阅服务：** 需要开发者订阅（每月5美元），订阅地址为 [effortlist.io](https://www.effortlist.io)。
2. **API密钥：** 人类用户必须在开发者设置中生成一个 **永久性的API密钥**。
3. **存储方式：** 通过 `EFFORTLIST_API_KEY` 环境变量或在 OpenClaw 内部配置中设置 API 密钥（例如：`openclaw config set skills.entries.effortlist-ai.env.EFFORTLIST_API_KEY "your_key"`）。

## 📐 数据结构（数据层次）

EffortList AI 的数据结构采用严格的嵌套形式：
**文件夹（Container）** ──> **任务（Task）** ──> **待办事项（Todo）**

- **文件夹：** 可选的高级容器，用于分组相关项目。
- **任务（Task）：** 可执行的项目，可以是顶级元素，也可以嵌套在文件夹中。
- **待办事项（Todo）：** 具体的可执行步骤。**每个待办事项都必须有一个父任务**。

## 🤖 智能处理与数据映射（针对智能代理）

| 用户意图            | 智能代理的工作流程                                      | 终端点目标                                      |
| :----------------:|------------------------------------------------------:|
| “规划项目”           | 创建文件夹 → 添加任务 → 添加待办事项                         | `POST /folders`, `POST /tasks`, `POST /todos`                 |
| “修正错误”           | 获取历史记录 → 查找目标ID → 撤销操作                         | `GET /api/v1/undo`, `POST /api/v1/undo?id=...`                |
| “查看今日安排”        | 根据时间范围获取待办事项                               | `GET /api/v1/todos?from=...&to=...`                     |
| “精确编辑”           | 修补特定记录                                   | `PATCH /api/v1/{type}?id=...`                          |

## 🛠️ 执行逻辑（“Omni”处理方式）

1. **精确查询与修改：** 始终建议通过 ID（`?id=...`）来获取特定记录，而非批量查询。更新时使用 `PATCH` 方法并指定记录 ID。
2. **分阶段处理：** 遵循五阶段处理流程（时间解析、分解、并行推理、合成和验证）。对于需要保护的记录，设置 `isProtectedTime: true` 以触发服务器端的保护机制。
3. **级联安全性：** 删除文件夹或任务会执行 **原子级删除** 操作。不过，系统会防止正在更新的项目被意外删除。
4. **人为因素：** 在制定计划时，遵循“优先安排间隔时间”和“考虑人为因素”的原则（例如，为过渡留出时间）。

## 🔒 安全性与隐私（零信任原则）

- **数据隔离：** 严格的数据隔离机制；用户只能查看自己的数据。
- **AI隐私政策：** 您的个人数据 **绝不会** 被用于模型训练。

## 📖 详细参考资料

- **完整 API 文档：** [API 文档](https://www.effortlist.io/docs)
- **系统架构：** 详见 [architecture.md]
- **安全审计文档：** [安全策略](https://www.effortlist.io/security)

**项目版本：** 1.7.5