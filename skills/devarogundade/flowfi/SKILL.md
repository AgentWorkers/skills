---
name: flowfi
description: FlowFi的REST API使用说明——包括授权、智能账户管理、工作流操作（AI生成、编辑、部署、撤销部署、删除、暂停、恢复、停止）、执行流程（列表、启动、取消、事件处理）、WebSocket通信（用于获取工作流状态）、价格信息（以Token或USD为单位）、模板管理（列表、获取、克隆）、数据传输对象（DTO）及请求/响应格式（分页功能、工作流相关数据、模板信息、执行相关数据），以及工作流知识库的访问。这些API适用于与后端系统的集成，也可用于用户查询工作流状态、执行结果、实时价格信息、模板详情、数据传输对象（DTO）或授权相关功能时。
---
# FlowFi OpenClaw 技能

本文档提供了关于 **FlowFi** 后端 API 的使用说明。基础 URL 是后端 API 的根路径（例如：`https://api.seimoney.link`）。受保护的路由需要通过 `Authorization: Bearer <token>` 使用 **JWT** 进行身份验证。

**文档分类**（按主题划分）：

| 主题 | 文件 |
|-------|------|
| 身份验证 | [docs/authorization.md](docs/authorization.md) |
| 智能账户 | [docs/smart-accounts.md](docs/smart-accounts.md) |
| 人工智能工作流（生成、建议、基于提示的编辑） | [docs/ai-workflows.md](docs/ai-workflows.md) |
| 工作流（生命周期管理：部署/卸载/暂停/恢复/停止/删除、列表、草稿） | [docs/workflows.md](docs/workflows.md) |
| 数据传输对象（DTO）与请求/响应格式 | [docs/dto.md](docs/dto.md) |
| 执行（REST 接口） | [docs/execution.md](docs/execution.md) |
| WebSockets（实时通信） | [docs/websocket.md](docs/websocket.md) |
| 价格管理 | [docs/price.md](docs/price.md) |
| 模板 | [docs/templates.md](docs/templates.md) |
| 终端点概览表 | [docs/summary.md](docs/summary.md) |

完整的文档索引请参阅 **[docs/README.md]**。

**常用操作说明：**
- 生成工作流：`POST /ai/generate-workflow`（输入提示内容 + 智能账户 ID）
- 部署工作流：`POST /workflows/:id/deploy`
- 查看工作流列表：`GET /workflows`
- 实时通信：通过 `/workflow-status` WebSockets 接口进行通信；可订阅工作流的执行状态或模拟结果