---
name: claw-skill-hookaido
description: 操作 Hookaido v2 的入站/出站/内部 Webhook 流程、队列分拣、MCP 工作流程、发布验证以及 HTTP/GRPC 拉取任务。适用于需要执行以下操作的场景：编写 Hookaido 文件、选择队列后端（`sqlite`、`memory`、`postgres`）、使用 `hookaido` CLI 命令（`run`、`config fmt`、`config validate`、`mcp serve`、`verify-release`）、通过 HTTP 或 gRPC 进行拉取操作（`dequeue`/`ack`/`nack`/`extend`）、处理 Admin API 的积压任务/延迟队列（DLQ），以及为数据传输和分发过程进行安全性加固（production hardening）。
metadata: {"openclaw":{"homepage":"https://github.com/7schmiede/claw-skill-hookaido","requires":{"bins":["hookaido"]},"install":[{"id":"download-darwin-amd64","kind":"download","os":["darwin"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v2.0.0/hookaido_v2.0.0_darwin_amd64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v2.0.0 (macOS amd64)"},{"id":"download-darwin-arm64","kind":"download","os":["darwin"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v2.0.0/hookaido_v2.0.0_darwin_arm64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v2.0.0 (macOS arm64)"},{"id":"download-linux-amd64","kind":"download","os":["linux"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v2.0.0/hookaido_v2.0.0_linux_amd64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v2.0.0 (Linux amd64)"},{"id":"download-linux-arm64","kind":"download","os":["linux"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v2.0.0/hookaido_v2.0.0_linux_arm64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v2.0.0 (Linux arm64)"},{"id":"download-windows-amd64","kind":"download","os":["win32"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v2.0.0/hookaido_v2.0.0_windows_amd64.zip","archive":"zip","extract":true,"targetDir":"~/.openclaw/tools/hookaido","bins":["hookaido"],"label":"Download hookaido v2.0.0 (Windows amd64)"},{"id":"download-windows-arm64","kind":"download","os":["win32"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v2.0.0/hookaido_v2.0.0_windows_arm64.zip","archive":"zip","extract":true,"targetDir":"~/.openclaw/tools/hookaido","bins":["hookaido"],"label":"Download hookaido v2.0.0 (Windows arm64)"}]}}
---
# Hookaido

## 概述

使用“配置优先”的工作流程来实现和排查 Hookaido 的问题：首先编辑 `Hookaidofile` 文件，进行验证，然后运行相关服务，检查数据流的流入/流出情况，最后诊断队列的健康状况以及延迟队列（DLQ）的行为。  
对于 Hookaido v2.0.0 的模块化架构，应采取渐进式的采用策略：默认情况下保持现有工作流程不变，仅在模块（如 `postgres`、gRPC 工作器或发布验证）对任务有实质性帮助时才选择使用它们。  
在进行任何更改之前，请确保所做的修改是保守的、可逆的，并在运行时进行验证。

## 工作流程

1. 确认目标架构：包括数据流的流入（HTTP 或 gRPC）、数据的输出（push），以及队列后端（`sqlite`、`memory` 或 `postgres`）。
2. 选择运行时模式，并确保 `hookaido` 已经安装在工具可执行的路径上：
   - **主机二进制模式**：使用 `metadata.openclaw.install` 中提供的安装命令。
   - **主机回退模式**：运行 `bash {baseDir}/scripts/install_hookaido.sh`（该脚本固定为 v2.0.0 版本，并经过 SHA256 验证）。
   - **公共仓库/源代码模式**：如果偏好基于源代码的安装方式，可以通过 `go install github.com/nuetzliches/hookaido/cmd/hookaido@v2.0.0` 来安装。
   - **Docker 沙箱模式**：使用已经包含 `hookaido` 的 Docker 镜像；或者通过 `agents.defaults.sandbox.docker.setupCommand` 在沙箱环境中进行安装。
   - 保留主机安装命令作为回退选项，以满足 `metadata.openclaw.requires.bins` 的要求。
3. 最小限度地检查和更新 `Hookaidofile` 文件。
4. 在启动或重新加载之前，执行格式化和验证操作：
   - `hookaido config fmt --config ./Hookaidofile`
   - `hookaido config validate --config ./Hookaidofile`
   - 如果涉及秘密配置或 Vault 支持的配置文件，请使用 `hookaido config validate --config ./Hookaidofile --strict-secrets`。
5. 启动服务并验证其健康状况：
   - `hookaido run --config ./Hookaidofile --db ./.data/hookaido.db`
   - 如果选择使用 `postgres` 作为队列后端，运行 `hookaido run --config ./Hookaidofile --postgres-dsn "$HOOKAIDO_POSTGRES_DSN"`
   - 使用 `curl http://127.0.0.1:2019/healthz?details=1` 检查服务健康状况。
6. 验证端到端的行为：
   - 确保数据流能够被正确接收并加入队列；
   - 消费者能够执行 `dequeue`、`ack`、`nack` 和 `extend` 操作（支持 HTTP 或 gRPC 模式）。

## 任务剧本

### 配置数据流的流入和消费

1. 定义一个带有明确身份验证和数据流路径的路由（支持 HTTP 或 gRPC 模式）。
2. 将敏感信息存储在环境变量或文件引用中，切勿直接写在代码中。
3. 确保路由配置和全局身份验证设置的一致性。
4. 使用真实的 Webhook 数据进行测试，并验证数据流的流入和消费过程（在需要批量处理时，支持 `ack`/`nack` 操作）。

### 配置数据的输出

1. 仅在服务能够正常接收数据流时才使用数据输出功能。
2. 明确设置超时和重试策略。
3. 由于数据输出至少会被执行一次，因此需要验证下游操作的幂等性。

### 配置队列后端

1. 默认使用 `sqlite` 作为队列后端；除非任务需要临时开发模式或共享的 Postgres 存储。
2. `memory` 和 `postgres` 可以作为可选的扩展模块使用，但不能替代现有的 `sqlite` 队列系统。
3. 在使用 `postgres` 时，记录数据库连接字符串（DSN），并在启动后验证队列的健康状况及队列状态。

### 操作队列和延迟队列（DLQ）

1. 首先查看队列的健康状况和待处理任务的数量。
2. 在重新排队或删除数据之前，先检查延迟队列（DLQ）的状态。
3. 如果需要重新排队大量数据，请说明预期的影响及相应的回滚方案。
4. 对于任何管理操作，必须提供明确的操作原因。

可使用的 API 包括：
- `GET /healthz?details=1`（获取健康状态信息）
- `GET /backlog/trends`（查看队列趋势）
- `GET /dlq`（查询延迟队列信息）
- `POST /dlq/requeue`（重新排队数据）
- `POST /dlq/delete`（删除队列中的数据）

### 使用 MCP 模式进行 AI 操作

1. 诊断时默认使用 `--role read` 权限。
2. 只有在明确表示需要修改数据时，才能启用修改操作：
   - `--enable-mutations --role operate --principal <identity>`
3. 仅允许管理员使用 `--enable-runtime-control` 来执行实时数据操作：
   - `--enable-runtime-control --role admin --pid-file <path>`
4. 对于任何修改操作，必须提供具体的操作原因。

### 验证公共版本

1. 建议使用官方的 Hookaido 公共仓库中的发布版本。
2. 在进行发布之前，验证文件的校验和、签名信息以及来源的真实性。
3. 默认情况下，验证过程是可选的，以避免增加现有工作流程的复杂性；除非任务确实需要验证。

可使用的命令包括：
- `hookaido verify-release --checksums ./hookaido_v2.0.0checksums.txt --require-provenance`（验证发布版本的完整性）

## 验证 checklist

- 在运行或重新加载之前，`hookaido config validate` 必须返回成功结果。
- 当涉及敏感配置或公共版本发布时，必须使用 `hookaido config validate --strict-secrets`。
- 健康检查端点必须能够正常访问，并能正确反映队列后端的状态。
- 消费者可以使用有效的令牌（支持 HTTP 或 gRPC）执行 `dequeue`、`ack`、`nack` 和 `extend` 操作；在需要批量处理时，支持 `ack`/`nack`。
- 对于数据输出模式，必须明确配置超时和重试策略。
- 使用 `--postgres-dsn` 参数来指定 `postgres` 队列后端的连接信息。
- 所有的延迟队列操作都必须有明确的范围、合理的理由，并被记录在日志中。

## 安全规则

- 不要为了通过测试而禁用身份验证机制。
- 在仅进行读取操作时，不得直接修改数据。
- 所有的队列操作都必须保证幂等性；请确保使用幂等的处理逻辑。
- 敏感信息必须存储在环境变量（`env:`）或文件引用（`file:`）中。

## 参考资料

- 有关命令片段和 API 数据格式的详细信息，请参阅 `references/operations.md`。