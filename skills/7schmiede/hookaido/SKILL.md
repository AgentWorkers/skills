---
name: hookaido
description: 创建、审核并管理 Hookaido 的 Webhook 队列配置。当任务涉及 Hookaidofile 的编写、`hookaido` CLI 命令（`run`、`config fmt`、`config validate`、`mcp serve`）的使用、基于 Pull 模式的消费者（`dequeue`/`ack`/`nack`/`extend`）、管理员 API 队列管理（健康检查、待处理任务、延迟队列 DLQ），或 Hookaido 的生产环境安全加固（如入口控制和数据传输）时，请使用这些配置。
metadata: {"openclaw":{"homepage":"https://github.com/nuetzliches/hookaido","requires":{"bins":["hookaido"]},"install":[{"id":"download-darwin-amd64","kind":"download","os":["darwin"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.3/hookaido_v1.3_darwin_amd64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v1.3 (macOS amd64)"},{"id":"download-darwin-arm64","kind":"download","os":["darwin"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.3/hookaido_v1.3_darwin_arm64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v1.3 (macOS arm64)"},{"id":"download-linux-amd64","kind":"download","os":["linux"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.3/hookaido_v1.3_linux_amd64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v1.3 (Linux amd64)"},{"id":"download-linux-arm64","kind":"download","os":["linux"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.3/hookaido_v1.3_linux_arm64.tar.gz","archive":"tar.gz","extract":true,"stripComponents":1,"targetDir":"~/.local/bin","bins":["hookaido"],"label":"Download hookaido v1.3 (Linux arm64)"},{"id":"download-windows-amd64","kind":"download","os":["win32"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.3/hookaido_v1.3_windows_amd64.zip","archive":"zip","extract":true,"targetDir":"~/.openclaw/tools/hookaido","bins":["hookaido"],"label":"Download hookaido v1.3 (Windows amd64)"},{"id":"download-windows-arm64","kind":"download","os":["win32"],"url":"https://github.com/nuetzliches/hookaido/releases/download/v1.3/hookaido_v1.3_windows_arm64.zip","archive":"zip","extract":true,"targetDir":"~/.openclaw/tools/hookaido","bins":["hookaido"],"label":"Download hookaido v1.3 (Windows arm64)"}]}}
---

# Hookaido

## 概述

使用以配置为中心的工作流程来实现和排查 Hookaido 的问题：首先编辑 `Hookaidofile` 文件，进行验证，然后运行相关流程（如 ingress/pull 流），接着诊断队列的健康状况以及 DLQ（Delayed Queue）的行为。在运行时操作之前，应采用保守且可逆的变更方式，并进行充分的验证。

## 工作流程

1. 确认目标拓扑结构：选择 pull 模式、push 模式、仅限出站消息的模式，或是内部队列模式。
2. 选择运行时模式，并确保 `hookaido` 已经安装在工具执行的环境中：
   - **主机二进制模式**：使用 `metadata.openclaw.install` 中提供的安装命令。
   - **主机回退模式**：运行 `bash {baseDir}/scripts/install_hookaido.sh`（版本固定为 v1.3，且已通过 SHA256 验证）。
   - **Docker 沙箱模式**：使用已经包含 `hookaido` 的沙箱镜像；或者通过 `agents.defaults.sandbox.docker.setupCommand` 在沙箱中安装 `hookaido`。
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
   - 消费者是否能够从队列中取出消息，并正确发送 `ack`/`nack` 响应。

## 任务脚本

### 配置 Ingress 和 Pull 消费

1. 定义一个具有明确身份验证机制和 pull 路径的路由规则。
2. 将敏感信息（如密钥）存储在环境变量或文件引用中，切勿直接写在代码中。
3. 确保路由规则和全局身份验证设置的一致性。
4. 使用真实的 Webhook 数据包进行测试，并验证消息的取出和确认机制是否正常工作。

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

### 配置 Push 传输

1. 仅在服务能够接受入站连接时使用 push 传输方式。
2. 明确设置超时和重试策略。
3. 由于消息至少会被传输一次，因此需要验证下游处理的幂等性。

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

1. 首先查看队列的健康状态和积压消息的数量。
2. 在重新排队或删除消息之前，先检查 DLQ 的状态。
3. 如果需要重新排队大量消息，需说明预期的影响以及相应的回滚方案。
4. 对于任何管理操作，必须提供明确的操作原因说明。

可使用的 API 请求包括：
- `GET /healthz?details=1`
- `GET /backlog/trends`
- `GET /dlq`
- `POST /dlq/requeue`
- `POST /dlq/delete`

### 使用 MCP 模式进行 AI 操作

1. 诊断时默认使用 `--role read` 权限。
2. 只有在明确表示操作意图的情况下，才能允许执行修改操作：
   - `--enable-mutations --role operate --principal <identity>`
3. 仅允许管理员工作流程使用运行时控制功能：
   - `--enable-runtime-control --role admin --pid-file <path>`
4. 对于任何修改操作，必须提供具体的操作原因。

## 验证检查清单

- 在运行开始或重新加载之前，`hookaido config validate` 的验证必须返回成功结果。
- 健康检查端点必须可访问，并能正确反映队列和后端的状态。
- 消费者必须能够使用有效的令牌从队列中取出消息，并发送 `ack`/`nack` 响应。
- 对于 push 模式，超时和重试行为必须经过明确配置。
- 所有的 DLQ 修改操作都必须有明确的范围、合理的理由，并被记录下来。

## 安全规则

- 不要为了“让测试通过”而禁用身份验证机制。
- 在进行仅读诊断之前，不要直接执行修改操作。
- 将队列操作视为至少会被执行一次的操作（即幂等操作），并确保相关处理函数具有幂等性。
- 敏感信息必须存储在 `env:` 或 `file:` 变量中。

## 参考资料

- 请参阅 `references/operations.md` 以获取命令片段和 API 数据包模板。