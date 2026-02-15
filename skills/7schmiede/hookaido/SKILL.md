---
name: hookaido
description: 创建、审查并管理 Hookaido 的 Webhook 队列设置。这些设置适用于以下场景：  
- 涉及 Hookaido 文件的编写；  
- 使用 `hookaido` 命令行工具（`run`、`config fmt`、`config validate`、`mcp serve`）；  
- 采用拉取模式（pull-mode）的消费者（`dequeue`/`ack`/`nack`/`extend`）；  
- 管理 Admin API 队列的状态（如健康检查、待处理任务、延迟队列 DLQ）；  
- 以及为 Hookaido 的数据导入和交付流程进行安全加固（production hardening）。
metadata: {"openclaw":{"homepage":"https://github.com/nuetzliches/hookaido","requires":{"bins":["hookaido"]},"install":[{"id":"download-darwin-amd64","kind":"download","os":["darwin"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.2.0/hookaido_v1.2.0_darwin_amd64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v1.2.0 (macOS amd64)"},{"id":"download-darwin-arm64","kind":"download","os":["darwin"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.2.0/hookaido_v1.2.0_darwin_arm64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v1.2.0 (macOS arm64)"},{"id":"download-linux-amd64","kind":"download","os":["linux"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.2.0/hookaido_v1.2.0_linux_amd64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v1.2.0 (Linux amd64)"},{"id":"download-linux-arm64","kind":"download","os":["linux"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.2.0/hookaido_v1.2.0_linux_arm64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v1.2.0 (Linux arm64)"},{"id":"download-windows-amd64","kind":"download","os":["win32"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.2.0/hookaido_v1.2.0_windows_amd64.zip","archive":"zip","extract":true,"targetDir":"~/.openclaw/tools/hookaido","bins":["hookaido"],"label":"Download hookaido v1.2.0 (Windows amd64)"},{"id":"download-windows-arm64","kind":"download","os":["win32"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.2.0/hookaido_v1.2.0_windows_arm64.zip","archive":"zip","extract":true,"targetDir":"~/.openclaw/tools/hookaido","bins":["hookaido"],"label":"Download hookaido v1.2.0 (Windows arm64)"}]}}
---

# Hookaido

## 概述

使用“配置优先”的工作流程来实现和排查 Hookaido 的问题：首先编辑 `Hookaidofile` 文件，进行验证，然后运行相应的入口（ingress）/拉取（pull）流程，接着诊断队列的健康状况以及延迟队列（DLQ）的行为。在运行时操作之前，应采用保守且可逆的更改方式，并进行充分的验证。

## 工作流程

1. 确认目标拓扑结构：选择拉取模式（pull mode）、推送模式（push mode）、仅限出站（outbound-only）或内部队列（internal queue）。
2. 确保 `hookaido` 可执行文件存在于系统的 `PATH` 环境变量中。
   - 在 OpenClaw 中推荐使用 `metadata.openclaw.install` 中提供的安装命令进行安装。
   - 如果安装失败，可以运行 `bash {baseDir}/scripts/install_hookaido.sh` 从 GitHub 仓库中手动安装。
3. 最小限度地修改 `Hookaidofile` 文件的内容。
4. 在启动或重新加载系统之前，执行格式化和验证操作：
   - `hookaido config fmt --config ./Hookaidofile`
   - `hookaido config validate --config ./Hookaidofile`
5. 启动系统并验证其运行状态：
   - `hookaido run --config ./Hookaidofile --db ./.data/hookaido.db`
   - `curl http://127.0.0.1:2019/healthz?details=1`
6. 验证端到端的行为：
   - 入口请求是否被正确接收并放入队列；
   - 消费者是否能够从队列中取出数据，并且是否能够正确发送 `ack`/`nack` 响应。

## 任务剧本（Task Playbooks）

### 配置入口（Ingress）和拉取消费（Pull Consumption）

1. 定义一个包含明确身份验证（auth）和拉取路径（pull path）的路由规则。
2. 将敏感信息（如密码等）存储在环境变量（env）或文件引用（file refs）中，切勿直接写在代码中。
3. 确保路由规则和全局身份验证设置的一致性。
4. 使用真实的 Webhook 数据包进行测试，并验证数据的拉取及确认（dequeue/ack）流程是否正常工作。

推荐使用以下配置：

```hcl
ingress {
  listen :8080
}

pull_api {
  listen :9443
  auth token env:HOOKAIDO_PULL_TOKEN
}

/webhooks/github {
  auth hmac env:HOOKAIDO_INGRESS_SECRET
  pull { path /pull/github }
}
```

### 配置推送交付（Push Delivery）

1. 仅在服务能够接受外部连接时使用推送模式。
2. 明确配置超时（timeout）和重试（retry）策略。
3. 由于数据至少会被发送一次，因此需要验证下游系统的幂等性（idempotency）。

```hcl
/webhooks/stripe {
  auth hmac env:STRIPE_SIGNING_SECRET
  deliver "https://billing.internal/stripe" {
    retry exponential max 8 base 2s cap 2m jitter 0.2
    timeout 10s
  }
}
```

### 操作队列（Queue Operations）和延迟队列（DLQ）

1. 首先查看系统的运行状态和队列中的积压任务（backlog）。
2. 在重新排队或删除数据之前，先检查延迟队列（DLQ）的情况。
3. 如果需要重新排队大量数据，请提前说明预期的影响，并准备好相应的回滚方案。
4. 对于任何管理操作（admin calls），必须提供明确的操作理由。

可使用的 API 包括：
- `GET /healthz?details=1`
- `GET /backlog/trends`
- `GET /dlq`
- `POST /dlq/requeue`
- `POST /dlq/delete`

### 使用 MCP 模式进行 AI 操作（AI Operations）

1. 诊断时默认使用 `--role read` 权限。
2. 只有在明确表示需要执行修改操作时，才允许使用 `--enable-mutations` 选项：
   - `--enable-mutations --role operate --principal <identity>`
3. 仅允许管理员（admin）使用 `--enable-runtime-control` 选项来控制系统的运行状态：
   - `--enable-runtime-control --role admin --pid-file <path>`
4. 对于任何修改操作，都必须提供具体的操作理由（reason）。

## 验证检查清单（Validation Checklist）

- 在系统启动或重新加载之前，`hookaido config validate` 命令必须返回成功结果。
- 健康检查（health check）端点必须能够正常访问，并且能够正确反映队列和后端系统的状态。
- 拉取数据的消费者必须能够使用有效的令牌（token）来执行 `dequeue`、`ack` 和 `nack` 操作。
- 对于推送模式，超时和重试策略必须经过明确配置。
- 任何对延迟队列（DLQ）的修改都必须有明确的范围、合理的理由，并且要被记录下来。

## 安全规则（Safety Rules）

- 不要为了通过测试而禁用身份验证机制。
- 在进行只读诊断之前，不要尝试直接修改系统配置。
- 将队列操作视为至少会被执行一次（at-least-once），因此需要使用幂等性（idempotent）的处理逻辑。
- 敏感信息必须存储在 `env:` 或 `file:` 变量中。

## 参考资料（References）

- 请参阅 `references/operations.md` 文件，以获取命令片段和 API 数据包模板。