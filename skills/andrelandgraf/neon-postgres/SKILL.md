---
name: neon-postgres
description: 关于如何使用 Neon Serverless Postgres 的指南和最佳实践。内容包括：入门指南、使用 Neon 进行本地开发、选择连接方式、Neon 的核心功能、身份验证（@neondatabase/auth）、基于 PostgREST 格式的数据 API（@neondatabase/neon-js）、Neon 命令行界面（CLI），以及 Neon 的平台 API/SDK。适用于所有与 Neon 相关的问题。
---
# Neon 无服务器 Postgres

Neon 是一个基于 Postgres 的无服务器平台，它将计算资源和存储资源分离，从而实现自动扩展、分支管理、即时数据恢复以及零成本扩展等功能。该平台与 Postgres 完全兼容，并且可以与任何支持 Postgres 的编程语言、框架或对象关系映射（ORM）配合使用。

## Neon 文档

Neon 的官方文档是获取所有相关信息的权威来源。在做出任何决定之前，请务必通过官方文档核实信息的准确性。Neon 的功能和 API 会不断更新，因此建议直接查阅最新的文档，而不是依赖培训资料。

### 以 Markdown 格式获取文档

任何 Neon 文档页面都可以通过以下两种方式以 Markdown 格式获取：

1. 在 URL 后添加 `.md` 扩展名（最简单的方法）：`https://neon.com/docs/introduction/branching.md`
2. 使用 `curl` 命令并指定 `text/markdown` 请求格式：`curl -H "Accept: text/markdown" https://neon.com/docs/introduction/branching`

两种方法返回的内容相同。请根据您的工具支持的情况选择合适的方法。

### 查找所需文档

文档索引列出了所有可用的文档页面及其对应的 URL 和简短描述：

```
https://neon.com/docs/llms.txt
```

常见的文档 URL 都在下面的主题链接中列出。如果您需要未在此列出的页面，可以搜索文档索引：`https://neon.com/docs/llms.txt`（切勿随意猜测 URL）。

## 什么是 Neon

本文档用于解释 Neon 的架构及相关术语（包括组织结构、项目、分支、端点等）。在提供具体实现建议之前，请先阅读此文档。

链接：`https://neon.com/docs/ai/skills/neon-postgres/references/what-is-neon.md`

## 入门指南

本文档适用于初次使用 Neon 的用户，内容包括项目/组织选择、连接字符串配置、驱动程序安装、可选的身份验证设置以及初始数据库模式配置。

链接：`https://neon.com/docs/ai/skills/neon-postgres/references/getting-started.md`

## 连接方式与驱动程序

本文档介绍了如何根据运行时需求选择合适的连接方式及驱动程序（如 TCP、HTTP、WebSocket、无服务器架构等）。

链接：`https://neon.com/docs/ai/skills/neon-postgres/references/connection-methods.md`

### 无服务器驱动程序

本文档介绍了如何使用 `@neondatabase/serverless` 模式，包括 HTTP 查询、WebSocket 事务以及针对特定运行环境的优化措施。

链接：`https://neon.com/docs/ai/skills/neon-postgres/references/neon-serverless.md`

### Neon JS SDK

本文档介绍了如何结合 Neon 的身份验证机制与数据 API，实现基于 PostgREST 格式的查询功能及客户端代码编写。

链接：`https://neon.com/docs/ai/skills/neon-postgres/references/neon-js.md`

## 开发工具

本文档提供了本地开发所需的工具和配置方法，包括使用 `npx neonctl@latest init` 进行项目初始化、安装 VSCode 扩展程序以及配置 Neon MCP 服务器。

链接：`https://neon.com/docs/ai/skills/neon-postgres/references/devtools.md`

### Neon CLI

本文档介绍了如何通过终端命令行执行操作、编写脚本以及实现持续集成/持续部署（CI/CD）自动化流程。

链接：`https://neon.com/docs/ai/skills/neon-postgres/references/neon-cli.md`

## Neon 管理 API

Neon 管理 API 可用于程序化地管理 Neon 的各种资源。该 API 虽然主要由 Neon CLI 和 MCP 服务器后台使用，但也可以直接用于更复杂的自动化任务或将其集成到其他应用程序中。

### Neon REST API

本文档提供了通过 HTTP 请求进行直接操作的接口，支持端点级别的控制、API 密钥认证、速率限制管理以及操作状态监控等功能。

链接：`https://neon.com/docs/ai/skills/neon-postgres/references/neon-rest-api.md`

### Neon TypeScript SDK

本文档介绍了如何使用 TypeScript 通过 `@neondatabase/api-client` 实现对 Neon 资源的程序化控制。

链接：`https://neon.com/docs/ai/skills/neon-postgres/references/neon-typescript-sdk.md`

### Neon Python SDK

本文档介绍了如何使用 Python 和 `neon-api` 包实现对 Neon 资源的程序化管理。

链接：`https://neon.com/docs/ai/skills/neon-postgres/references/neon-python-sdk.md`

## Neon 身份验证（Neon Auth）

本文档介绍了用户身份验证的设置方法、相关 UI 组件，以及在使用 Next.js 或 React 应用程序时可能遇到的身份验证问题。

链接：`https://neon.com/docs/ai/skills/neon-postgres/references/neon-auth.md`

需要注意的是，Neon JS SDK 也内置了身份验证功能，因此根据实际需求可以选择使用 Neon JS SDK 代替单独的 Neon Auth。更多详情请参阅：`https://neon.com/docs/ai/skills/neon-postgres/references/connection-methods.md`。

## 分支管理（Branching）

本文档介绍了如何创建和管理独立的环境、进行数据库模式迁移测试、预览部署以及自动化分支生命周期管理。

- 分支是即时创建的、基于写时复制机制的克隆（不会复制全部数据）。
- 每个分支都有自己的计算端点。
- 可使用 `neonctl CLI` 或 MCP 服务器来创建、查看和比较分支。

链接：`https://neon.com/docs/ai/skills/neon-postgres/references/branching.md`

## 自动扩展（Autoscaling）

本文档介绍了如何根据工作负载自动扩展计算资源，并提供了关于计算单元（CU）大小选择和运行时行为的指导。

链接：`https://neon.com/docs/introduction/autoscaling.md`

## 零成本扩展（Scale to Zero）

本文档介绍了如何优化空闲资源的消耗，以及暂停/恢复功能的配置方法（包括冷启动带来的性能影响）。

- 空闲的计算资源会自动暂停（默认为 5 分钟，可配置），除非用户明确禁用该功能。
- 恢复操作通常会有冷启动延迟（约几百毫秒）。
- 计算资源暂停时，存储资源仍保持活跃状态。

链接：`https://neon.com/docs/introduction/scale-to-zero.md`

## 即时数据恢复（Instant Restore）

本文档介绍了如何实现精确的数据恢复功能，无需依赖传统的备份流程。

- 数据恢复的时间窗口受配置限制。
- 用户可以从历史数据点创建新的分支。
- 可使用“时间旅行”查询功能进行历史数据查询。

链接：`https://neon.com/docs/introduction/branch-restore.md`

## 读复制（Read Replicas）

本文档适用于读操作密集型的应用场景，用户需要专用只读计算资源而无需复制存储数据。

- 复制端点仅提供读取权限，共享相同的存储资源。
- 复制端的创建速度快，且扩展能力独立于主计算节点。
- 常见应用场景包括数据分析、报表生成和读操作较多的 API。

链接：`https://neon.com/docs/introduction/read-replicas.md`

## 连接池（Connection Pooling）

本文档介绍了在无服务器或高并发环境下如何安全、高效地管理 Postgres 连接。

- Neon 使用 `PgBouncer` 工具实现连接池管理。
- 可在端点地址后添加 `-pooler` 选项来启用连接池功能。
- 在并发波动较大的无服务器环境中，连接池尤为重要。

链接：`https://neon.com/docs/connect/connect-pooling.md`

## IP 访问控制（IP Allow Lists）

本文档介绍了如何通过受信任的网络、IP 地址或 CIDR 范围来限制数据库访问权限。

链接：`https://neon.com/docs/introduction/ip-allow.md`

## 逻辑复制（Logical Replication）

本文档介绍了如何集成 CDC 数据复制机制、与外部 Postgres 系统进行数据同步，或实现基于复制的数据迁移。

- Neon 支持原生的逻辑复制功能。
- 适用于将数据复制到外部 Postgres 系统或从外部系统复制数据。

链接：`https://neon.com/docs/guides/logical-replication-guide.md`