---
name: claw-skill-hookaido
description: 接收来自外部服务的Webhook请求，并触发自动化流程、集成操作以及基于事件的工作流。管理Hookaido v2的入站/出站/内部Webhook流程、任务队列的优先级分配、MCP工作流、发布验证机制，以及HTTP/GRPC协议下的数据拉取操作。适用于需要执行以下任务的场景：编写Hookaido相关文件、选择任务队列的后端存储方式（`sqlite`、`memory`、`postgres`）、使用`hookaido`命令行工具（`run`、`config fmt`、`config validate`、`mcp serve`）、通过HTTP或gRPC进行数据拉取操作（`dequeue`/`ack`/`nack`/`extend`）、处理Admin API的待办事项或延迟队列（DLQ），以及提升系统的安全性以保障数据的顺利接入和传输。
metadata: {"openclaw":{"homepage":"https://github.com/7schmiede/claw-skill-hookaido","requires":{"bins":["hookaido"]},"install":[{"id":"download-darwin-amd64","kind":"download","os":["darwin"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v2.0.0/hookaido_v2.0.0_darwin_amd64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v2.0.0 (macOS amd64)"},{"id":"download-darwin-arm64","kind":"download","os":["darwin"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v2.0.0/hookaido_v2.0.0_darwin_arm64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v2.0.0 (macOS arm64)"},{"id":"download-linux-amd64","kind":"download","os":["linux"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v2.0.0/hookaido_v2.0.0_linux_amd64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v2.0.0 (Linux amd64)"},{"id":"download-linux-arm64","kind":"download","os":["linux"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v2.0.0/hookaido_v2.0.0_linux_arm64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v2.0.0 (Linux arm64)"},{"id":"download-windows-amd64","kind":"download","os":["win32"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v2.0.0/hookaido_v2.0.0_windows_amd64.zip","archive":"zip","extract":true,"targetDir":"~/.openclaw/tools/hookaido","bins":["hookaido"],"label":"Download hookaido v2.0.0 (Windows amd64)"},{"id":"download-windows-arm64","kind":"download","os":["win32"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v2.0.0/hookaido_v2.0.0_windows_arm64.zip","archive":"zip","extract":true,"targetDir":"~/.openclaw/tools/hookaido","bins":["hookaido"],"label":"Download hookaido v2.0.0 (Windows arm64)"}]}}
---
# Hookaido

## 概述

使用“配置优先”的工作流程来实现和排查 Hookaido 的问题：首先编辑 `Hookaidofile` 文件，进行验证，然后运行相关流程（如数据导入/提取），接着诊断队列的健康状况以及延迟队列（DLQ, Delayed Queue）的行为。在应用 Hookaido v2.0.0 的模块化架构时，应保持现有工作流程的完整性；仅在模块（如 `postgres`、gRPC 工作器或发布验证）对任务有实质性帮助时才选择使用它们。在进行任何更改之前，请确保所做的修改是保守的、可逆的，并在运行时进行验证。

## 工作流程

1. 确认目标架构：包括数据导入/提取（通过 HTTP 或 gRPC）、数据推送以及队列后端（`sqlite`、`memory` 或 `postgres`）。
2. 选择运行模式，并确保 `hookaido` 已安装在工具可执行的位置：
   - **主机二进制模式**：使用 `metadata.openclaw.install` 中提供的安装命令。
   - **主机回退模式**：运行 `bash {baseDir}/scripts/install_hookaido.sh`（该脚本固定为 v2.0.0 版本，并经过 SHA256 验证）。
   - **公共仓库/源代码模式**：如果偏好基于源代码的安装方式，可通过 `go install github.com/nuetzliches/hookaido/cmd/hookaido@v2.0.0` 来安装。
   - **Docker 沙箱模式**：使用已包含 `hookaido` 的 Docker 镜像；或者通过 `agentsdefaults.sandbox.docker.setupCommand` 在沙箱环境中安装。
   - 保留主机安装命令作为回退选项，以满足 `metadata.openclaw.requires.bins` 的要求。
3. 最小限度地检查和更新 `Hookaidofile` 文件。
4. 在启动或重新加载之前执行格式化和验证操作：
   - `hookaido config fmt --config ./Hookaidofile`
   - `hookaido config validate --config ./Hookaidofile`
   - 如果涉及秘密配置或 Vault 支持的配置文件，执行 `hookaido config validate --config ./Hookaidofile --strict-secrets`。
5. 启动服务并验证其健康状况：
   - `hookaido run --config ./Hookaidofile --db ./.data/hookaido.db`
   - 如果选择使用 `postgres` 作为队列后端，执行 `hookaido run --config ./Hookaidofile --postgres-dsn "$HOOKAIDO_POSTGRES_DSN"`
   - 使用 `curl http://127.0.0.1:2019/healthz?details=1` 检查服务健康状况。
6. 验证端到端的行为：
   - 确保数据导入请求能够被正确接收并放入队列；
   - 消费者能够执行 `dequeue`、`ack`、`nack`、`extend` 操作（支持 HTTP 或 gRPC 消息传递方式）。
7. 在遇到问题时，首先检查队列的积压情况（backlog）和延迟队列（DLQ）的状态，然后再进行相应的处理。

## 任务脚本

### 配置数据导入和提取功能

1. 定义一个具有明确身份验证机制和数据提取路径的路由（支持 HTTP 或 gRPC 消费者）。
2. 将敏感信息存储在环境变量或文件引用中，切勿直接写在代码中。
3. 确保路由配置和全局身份验证设置的一致性。
4. 使用真实的 Webhook 数据进行测试，并验证数据提取和确认操作的流程（包括批量处理时的 `ack`/`nack` 操作）。

以下是一个示例配置：

```hcl
ingress {
  listen :8080
}

pull_api {
  listen :9443
  grpc.listen :9943  # 可选：用于 gRPC 消费者
  auth token env:HOOKAIDO_pull_TOKEN
}

/webhooks/github {
  auth hmac env:HOOKAIDO_ingRESS_SECRET
  pull { path /pull/github }
}
```

### 配置数据推送功能

1. 仅在服务能够正常接收数据导入请求时才启用数据推送功能。
2. 明确设置推送操作的超时和重试策略。
3. 由于数据推送至少会执行一次，因此需要验证操作的幂等性（idempotency）。

以下是一个示例配置：

```hcl
/webhooks/stripe {
  auth hmac env:STRIPE_SIGNING_SECRET
  deliver "https://billing.internal/stripe" {
    retry exponential max 8 base 2s cap 2m jitter 0.2
    timeout 10s
  }
}
```

### 配置队列后端

1. 默认使用 `sqlite` 作为队列后端；除非任务需要使用临时性的开发模式或共享的 Postgres 存储。
2. `memory` 和 `postgres` 可视为可选的扩展模块，而非替代现有的 `sqlite` 队列方案。
3. 在使用 `postgres` 时，需记录数据库的连接字符串（DSN），并在服务启动后验证其健康状况及队列状态。

以下是一些常见的队列后端配置示例：

```hcl
queue sqlite
queue memory
queue postgres
```

### 操作队列和延迟队列（DLQ）

1. 在执行任何操作之前，先查看队列的健康状况和积压数据。
2. 在重新排队或删除数据之前，务必检查延迟队列（DLQ）的状态。
3. 如果需要重新排队大量数据，请提前说明可能产生的影响及相应的回滚方案。
4. 管理员进行的任何数据操作都必须提供明确的操作原因。

可使用的 API 路径包括：

- `GET /healthz?details=1`：获取服务健康状态信息。
- `GET /backlog/trends`：查看队列积压趋势。
- `GET /dlq`：查询延迟队列的状态。
- `POST /dlq/requeue`：重新排队数据。
- `POST /dlq/delete`：删除队列中的数据。

### 使用 MCP 模式进行 AI 操作

1. 诊断时默认使用 `--role read` 权限。
2. 只有在明确表示需要执行数据操作时，才能启用修改功能：
  - `--enable-mutations --role operate --principal <identity>`
3. 仅允许管理员使用 `--enable-runtime-control --role admin --pid-file <path>` 来执行实时数据操作。
4. 对于任何数据修改操作，都必须提供详细的操作原因。

### 验证公共版本

1. 建议使用官方的 Hookaido 公共仓库中的版本资源。
2. 在发布新版本之前，务必验证文件的校验和（checksums）、签名信息以及来源的可靠性。
3. 默认情况下，验证过程是可选的，以避免增加现有工作流程的复杂性；除非任务确实需要，否则无需强制进行验证。

以下是一个示例命令：

```hcl
hookaido verify-release --checksums ./hookaido_v2.0.0_checksums.txt --require-provenance
```

## 验证检查清单

- 在运行服务或重新加载之前，`hookaido config validate` 必须返回成功的结果。
- 当涉及秘密配置文件或需要验证公共版本时，必须使用 `hookaido config validate --strict-secrets`。
- 健康状态检查接口能够正常访问，并能准确反映队列后端的实际状态。
- 数据提取消费者能够使用有效的令牌（支持 HTTP 或 gRPC）执行 `dequeue`、`ack`、`nack`、`extend` 操作；批量处理时也支持 `ack`/`nack`。
- 对于数据推送模式，必须明确配置重试和超时策略。
- 使用 `--postgres-dsn` 参数来指定 `postgres` 数据库的连接信息。
- 所有的延迟队列（DLQ）相关操作都必须有明确的范围、合理的理由，并且操作过程会被记录下来。

## 安全规则

- 不得为了“让测试通过”而禁用身份验证机制。
- 在仅用于诊断目的时，不得直接修改系统配置。
- 所有的队列操作都应遵循“至少执行一次”的原则，并确保相关处理函数具有幂等性（idempotent）。
- 敏感信息必须存储在环境变量（`env:`）或文件引用（`file:`）中。

## 参考资料

- 有关命令示例和 API 数据格式的详细信息，请参阅 `references/operations.md` 文件。