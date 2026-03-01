---
name: weave
description: >
  **使用说明：**  
  在使用 Weave CLI 创建 Weave Cash 的加密货币对加密货币类型的发票、生成支付报价，或监控发票的支付状态时，请参考以下说明。
license: AGPL-3.0-or-later
metadata:
  openclaw:
    requires:
      bins:
        - weave
    install:
      - kind: go
        module: github.com/AryanJ-NYC/weave-cash/apps/cli/cmd/weave
        bins:
          - weave
    emoji: "🧶"
    homepage: "https://www.weavecash.com"
  clawdbot:
    requires:
      bins:
        - weave
    install:
      - kind: go
        module: github.com/AryanJ-NYC/weave-cash/apps/cli/cmd/weave
        bins:
          - weave
    emoji: "🧶"
    homepage: "https://www.weavecash.com"
---
# Weave

## 概述

使用 `weave` 可以完成 Weave Cash 发票的整个生命周期管理工作，包括：

1. 创建发票 (`weave create`)
2. 生成付款指令 (`weave quote`)
3. 跟踪结算进度 (`weave status` 或 `weave status --watch`)

## 使用限制

- 仅支持加密货币之间的交易，禁止使用法定货币、法定货币转换或以法定货币计价的功能。
- 优先输出机器可读的 JSON 格式的数据；仅在用户明确要求时才使用 `--human` 选项。
- 绝不要在输出结果中暴露任何敏感信息（如私钥、令牌或 JWT）。
- 将网络/API 调用视为可能出错的操作，并对非零退出代码进行妥善处理。

## 不适用场景

- 严禁将此工具用于处理法定货币发票或法定货币结算相关的工作流程。
- 严禁使用此工具编辑 Weave 的 Web UI 或前端代码。
- 严禁将此工具用于与钱包托管或私钥管理无关的任务。
- 如果用户需要使用非 Weave 支持的支付方式，请勿使用此工具。

## 使用前准备

1. 确认命令行工具 (`CLI`) 是否可用：
```bash
weave --help
```

2. 在选择交易资产之前，先确认运行时环境是否支持相应的令牌和网络：
```bash
weave tokens
```

3. 如果 `weave` 工具未安装，请提供合规的安装指南，并在运行前征求用户同意：
```bash
go install github.com/AryanJ-NYC/weave-cash/apps/cli/cmd/weave@latest
weave --help
```

如果用户环境中没有 Go 语言环境，请引导用户参考官方安装文档，避免使用远程 shell 命令进行安装。

## 安装规范

- 建议使用 `metadata.openclaw.install` 或 `metadata.clawdbot.install` 等包管理工具进行安装。
- 绝不要建议用户直接在 shell 解释器中执行远程下载命令。
- 在安装依赖项时，必须获得用户的明确批准；切勿自动完成依赖项的安装。

## 令牌与网络选择

- 始终以运行时环境生成的 `weave tokens` 作为可信的令牌来源。
- 不要在代码中硬编码令牌或网络列表。
- 仅当需要接收支持多个网络的令牌时，才需要使用 `--receive-network` 选项。
- 如果运行时环境支持，可以使用网络别名（例如 `Ethereum|ETH`、`Solana|SOL`、`Tron|TRX`）。

## 工作流程

### 1) 创建发票

需要收集以下信息：
- `receive-token`
- `amount`（正数字符串）
- `wallet-address`
- `receive-network`（仅在运行时环境要求的场景下使用）
- 可选买家信息（`description`、`buyer-name`、`buyer-email`、`buyer-address`）

命令：
```bash
weave create \
  --receive-token USDC \
  --receive-network Ethereum \
  --amount 25 \
  --wallet-address 0x1111111111111111111111111111111111111111
```

预期的 JSON 格式：
```json
{
  "id": "inv_123",
  "invoiceUrl": "https://www.weavecash.com/invoice/inv_123"
}
```

请记录生成的 `id`，以便后续进行 `quote` 或 `status` 操作。

### 2) 生成付款指令

需要收集以下信息：
- `invoice-id`
- `pay-token`
- `pay-network`
- `refund-address`

命令：
```bash
weave quote inv_123 \
  --pay-token USDT \
  --pay-network Ethereum \
  --refund-address 0x2222222222222222222222222222222222222222
```

预期的输出字段包括：
- `depositAddress`
- `depositMemo`（可选）
- `amountIn`
- `amountOut`
- `timeEstimate`
- `expiresAt`

### 3) 检查结算状态

- 一次性操作：
```bash
weave status inv_123
```

- 监视模式：
```bash
weave status inv_123 --watch --interval-seconds 5 --timeout-seconds 900
```

状态解释：
- 出口代码 `0` 表示操作已完成（`COMPLETED`、`FAILED`、`REFUNDED`、`EXPIRED`）
- 出口代码 `2` 表示监视超时（非命令执行失败）
- 出口代码 `1` 表示命令/API/网络验证失败

## 错误处理

当出现错误时（退出代码为 `1`），请输出结构化的 JSON 错误信息。常见的错误格式如下：
```json
{
  "error": "api message",
  "status": 409,
  "details": {
    "error": "Invoice is not in PENDING status"
  }
}
```

如果监视操作超时（退出代码为 `2`），应视为操作未完成，而非严重故障。建议用户调整 `--timeout-seconds` 参数或重新执行 `weave status <invoice-id>` 命令。

## 运行时环境变化处理

安装的二进制文件和源代码库可能会影响对令牌和网络的支持。在确定有效的令牌/网络组合时，务必使用运行时环境自动生成的列表（`weave tokens`）。