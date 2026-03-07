---
name: agent-dashboard-sync
description: 将 OpenClaw 部署环境的运行状态、心跳信号以及定时任务（cron）信息同步到 Cloudflare 的键值存储（KV）系统中，并通过 Worker API 提供可供仪表盘使用的数据。此功能适用于配置或管理 Agent 部署环境的仪表盘数据层（包括数据收集器、键值存储模式、Worker 的数据摄取/读取 API、定时任务调度机制，以及从基于 Git 的高频状态存储系统迁移到 Cloudflare KV 的过程）。
---
# 代理仪表盘数据同步

将仪表盘数据同步操作视为一个不依赖于大型语言模型（LLM）的独立流程（即：不使用LLM来处理数据同步任务）。

## 坚守的规则

1. 高频更新的状态信息不应被提交到Git仓库中。
2. 使用Cloudflare Worker与键值存储（KV）系统来实现运行时数据同步。
3. 从本地Cron任务（`*/2 * * * *`）中启动数据收集器，且不要在数据收集器的代码路径中调用任何大型语言模型相关功能。
4. 绝不要在文件、日志或截图中提交或显示生产环境的令牌/密钥信息。
5. 在技能文档中不要使用绝对路径；应使用相对路径或占位符（如`<PROJECTS_ROOT>`、`<SHARED_ROOT>`）。

## 范围界定

- 本技能负责的部分包括：数据收集器、Worker的数据摄取/读取API、键值存储（KV）的存储结构、Cron任务的部署以及仪表盘数据源的连接配置。
- 本技能不涉及的部分包括：代理间的通信协议、组织治理规则以及Discord路由规则。

## 键值存储（KV）数据契约（版本1）

- `fleet:registry`
- `fleet:heartbeat:<agent_id>`
- `fleet:cron:<agent_id>`
- `fleet:runtime:<agent_id>`
- `fleet:events:recent`
- `fleet:updated_at`

数据格式的详细信息请参见`references/schema.md`。

## 最小化部署步骤

1. 部署Cloudflare Worker及相应的键值存储（KV）命名空间。
2. 将仪表盘环境配置为“cloudflare”模式。
3. 在每个节点上安装带有唯一`AGENT_ID`的Cron任务以启动数据收集器。
4. 首先验证`/health`接口的状态，接着验证`/fleet`接口，最后验证仪表盘用户界面。

## 安全检查清单

- 将`INGEST_TOKEN`和`READ_TOKEN`作为工作节点的敏感信息进行存储。
- 仪表盘的读取令牌（`DASHBOARD_READ_TOKEN`）必须存储在服务器端，严禁在客户端展示。
- 将`NEXT_PUBLIC_*`这类变量设置为非敏感信息。
- 在共享命令或日志之前，必须对令牌内容进行脱敏处理。

## 运维手册链接

- Worker的配置与命令执行顺序：`references/worker-setup.md`
- 数据收集器的配置与Cron任务的设置：`references/collector-cron.md`
- 环境变量配置：`references/env-matrix.md`
- 数据结构参考：`references/schema.md`
- 所有代理的安全策略：`references/security-rules.md`