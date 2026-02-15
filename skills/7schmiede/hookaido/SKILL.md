---
name: hookaido
description: >
  操作 Hookaido 的入站/出站 Webhook 流程、任务队列管理（queue triage）、MCP 工作流程（MCP workflows），以及基于 gRPC 的数据拉取（gRPC-pull workers）。适用于需要执行以下任务的场景：  
  - 编写 Hookaido 相关文件（Hookaidofile）  
  - 使用 `hookaido` 命令行工具（`run`、`config fmt`、`config validate`、`mcp serve`）  
  - 通过 HTTP 或 gRPC 进行数据拉取操作（`dequeue`/`ack`/`nack`/`extend`）  
  - 管理 Admin API 的待办任务（backlog/DLQ）  
  - 优化 Webhook 的接入与交付流程（production hardening）。
metadata: {"openclaw":{"homepage":"https://github.com/nuetzliches/hookaido","requires":{"bins":["hookaido"]},"install":[{"id":"download-darwin-amd64","kind":"download","os":["darwin"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.5.0/hookaido_v1.5.0_darwin_amd64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v1.5.0 (macOS amd64)"},{"id":"download-darwin-arm64","kind":"download","os":["darwin"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.5.0/hookaido_v1.5.0_darwin_arm64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v1.5.0 (macOS arm64)"},{"id":"download-linux-amd64","kind":"download","os":["linux"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.5.0/hookaido_v1.5.0_linux_amd64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v1.5.0 (Linux amd64)"},{"id":"download-linux-arm64","kind":"download","os":["linux"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.5.0/hookaido_v1.5.0_linux_arm64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v1.5.0 (Linux arm64)"},{"id":"download-windows-amd64","kind":"download","os":["win32"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.5.0/hookaido_v1.5.0_windows_amd64.zip","archive":"zip","extract":true,"targetDir":"~/.openclaw/tools/hookaido","bins":["hookaido"],"label":"Download hookaido v1.5.0 (Windows amd64)"},{"id":"download-windows-arm64","kind":"download","os":["win32"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.5.0/hookaido_v1.5.0_windows_arm64.zip","archive":"zip","extract":true,"targetDir":"~/.openclaw/tools/hookaido","bins":["hookaido"],"label":"Download hookaido v1.5.0 (Windows arm64)"}]}}
---
# Hookaido

## 概述

使用“配置优先”的工作流程来实施和排查 Hookaido 的问题：首先编辑 `Hookaidofile` 文件，进行验证，然后运行相关流程（如 ingress/pull 流），接着诊断队列的健康状况以及 DLQ（Delayed Queue）的行为。在运行时操作之前，应采用保守且可逆的更改方式，并进行验证。

## 工作流程

1. 确认目标拓扑结构：包括入站请求（HTTP 或 gRPC）、出站推送，以及内部队列的配置。
2. 选择运行时模式，并确保 `hookaido` 已经安装在工具执行的环境中：
   - **主机二进制模式**：使用 `metadata.openclaw.install` 中提供的安装命令。
   - **主机回退模式**：运行 `bash {baseDir}/scripts/install_hookaido.sh`（版本固定为 v1.5.0，且已通过 SHA256 验证）。
   - **Docker 沙箱模式**：使用已包含 `hookaido` 的沙箱镜像；或者通过 `agentsdefaults.sandbox.docker.setupCommand` 在沙箱环境中安装。
   - 保留主机安装命令作为回退选项，以满足 `metadata.openclaw.requires.bins` 的要求。
3. 最小限度地检查和更新 `Hookaidofile` 文件的内容。
4. 在启动或重新加载之前，执行格式化和验证操作：
   - `hookaido config fmt --config ./Hookaidofile`
   - `hookaido config validate --config ./Hookaidofile`
5. 启动运行时服务并验证其健康状态：
   - `hookaido run --config ./Hookaidofile --db ./.data/hookaido.db`
   - `curl http://127.0.0.1:2019/healthz?details=1`
6. 验证端到端的行为：
   - 入站请求是否被正确接收并放入队列；
   - 消费者是否能够通过 `dequeue`、`ack`、`nack` 或 `extend` 等操作处理请求（支持 HTTP 拉取，启用 gRPC 拉取时也支持）。

## 任务脚本

### 配置 Ingress 和 Pull 消费

1. 定义一条包含明确身份验证机制和拉取路径的路由（支持 HTTP 拉取，可选 gRPC 拉取）。
2. 将敏感信息存储在环境变量或文件引用中，切勿直接内嵌在代码中。
3. 确保路由配置和全局身份验证设置一致。
4. 使用真实的 Webhook 数据包进行测试，并验证消费端的 `dequeue`/`ack` 功能是否正常工作。

推荐使用以下配置基线：

```hcl
ingress {
  listen :8080
}

pull_api {
  listen :9443
  grpc_listen :9943 # optional gRPC pull-worker listener
  auth token env:HOOKAIDO_PULL_TOKEN
}

/webhooks/github {
  auth hmac env:HOOKAIDO_INGRESS_SECRET
  pull { path /pull/github }
}
```

### 配置 Push 传输

1. 仅在服务能够正常接收入站请求时使用 Push 传输方式。
2. 明确配置超时和重试策略。
3. 由于数据至少会被传输一次，因此需要验证下游处理的幂等性。

```hcl
/webhooks/stripe {
  auth hmac env:STRIPE_SIGNING_SECRET
  deliver "https://billing.internal/stripe" {
    retry exponential max 8 base 2s cap 2m jitter 0.2
    timeout 10s
  }
}
```

### 操作队列和 DLQ

1. 首先查看队列的健康状态和待处理任务列表（backlog）。
2. 在重新排队或删除数据之前，先检查 DLQ 的状态。
3. 如果需要重新排队大量数据，请说明预期的影响及相应的回滚方案。
4. 管理员在进行任何修改操作时，必须提供明确的操作理由。

可使用的 API 包括：
- `GET /healthz?details=1`
- `GET /backlog/trends`
- `GET /dlq`
- `POST /dlq/requeue`
- `POST /dlq/delete`

### 使用 MCP 模式进行 AI 操作

1. 诊断时默认使用 `--role read` 权限。
2. 只有在明确表明操作意图的情况下，才允许进行数据修改：
   - `--enable-mutations --role operate --principal <identity>`
3. 仅允许管理员使用 `--enable-runtime-control` 来执行运行时控制：
   - `--enable-runtime-control --role admin --pid-file <path>`
4. 对于任何数据修改操作，必须提供具体的操作理由。

## 验证检查清单

- 在启动或重新加载服务之前，`hookaido config validate` 的验证必须成功。
- 健康检查端点必须可访问，并能正确报告队列和后端的当前状态。
- 消费者必须能够使用有效的令牌（支持 HTTP 和 gRPC）执行 `dequeue`、`ack`、`nack` 和 `extend` 操作。
- 对于 Push 模式，超时和重试策略必须明确配置。
- 所有的 DLQ 修改操作都必须有明确的范围、合理的理由，并被记录下来。

## 安全规则

- 不得为了通过测试而禁用身份验证机制。
- 在仅用于诊断的阶段，不得直接进行数据修改。
- 队列操作应遵循“至少被处理一次”的原则（at-least-once）；相关处理逻辑必须具备幂等性。
- 敏感信息应存储在 `env:` 或 `file:` 变量中。

## 参考资料

- 请参阅 `references/operations.md` 以获取命令片段和 API 数据包模板。