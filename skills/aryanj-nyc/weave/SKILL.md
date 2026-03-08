---
name: weave
description: Use when creating crypto or stablecoin invoices, generating payment quotes, or tracking invoice payment status with the Weave CLI.
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
      - id: node
        kind: node
        package: weave-cash-cli
        label: Fallback: Install Weave CLI (npm)
        bins:
          - weave
    emoji: '🧶'
    homepage: 'https://www.weavecash.com'
  clawdbot:
    requires:
      bins:
        - weave
    install:
      - kind: go
        module: github.com/AryanJ-NYC/weave-cash/apps/cli/cmd/weave
        bins:
          - weave
      - id: node
        kind: node
        package: weave-cash-cli
        label: Fallback: Install Weave CLI (npm)
        bins:
          - weave
    emoji: '🧶'
    homepage: 'https://www.weavecash.com'
---

# Weave

Weave 是一个用于处理加密货币发票和跨链支付工作流的命令行工具（CLI）。当您需要创建比特币、以太坊、Solana、USDC 或 USDT 发票、生成支付报价，以及监控 Base、Tron 和 Zcash 等支持网络中的结算情况时，可以使用这个工具。

## 概述

使用 `weave` 可以完成整个 Weave Cash 发票生命周期的工作流程：
1. 创建发票（`weave create`）
2. 生成支付指令（`weave quote`）
3. 跟踪结算状态（`weave status` 或 `weave status --watch`）

## 使用注意事项：

- 仅支持加密货币之间的交易，禁止使用法定货币、法定货币转换或以法定货币计价的功能。
- 优先输出机器可读的 JSON 格式的数据；仅在用户明确要求时使用 `--human` 选项。
- 绝不要在输出中暴露任何敏感信息（如私钥、代币或 JWT）。
- 要意识到网络/API 调用可能存在失败风险，并妥善处理非零退出码。

## 不适用场景：

- 请勿将此工具用于处理法定货币发票或法定货币结算相关的工作流程。
- 请勿使用此工具编辑 Weave 的 Web UI 或前端代码。
- 请勿将此工具用于与钱包托管或私钥管理无关的任务。
- 如果用户需要使用非 Weave 的支付解决方案，请勿使用此工具。

## 使用前准备：

1. 确认命令行工具是否可用：
```bash
weave --help
```

2. 在选择资产之前，先了解运行时环境支持的代币和网络：
```bash
weave tokens
```

3. 如果 `weave` 未安装，请提供合规的安装指南，并在运行前询问用户是否需要安装：
```bash
go install github.com/AryanJ-NYC/weave-cash/apps/cli/cmd/weave@latest
weave --help
```

如果 Go 语言不可用，可以使用 npm 作为替代方案：
```bash
npm i -g weave-cash-cli
weave --help
```

如果 Go 和 npm 都不可用，请报告缺失的依赖项。

## 安装规范：

- 建议使用 `metadata.openclaw.install` 或 `metadata.clawdbot.install` 这样的包管理器进行安装。
- 严禁直接将远程下载命令通过管道传递给 Shell 解释器。
- 在用户明确同意之前，切勿自动安装依赖项。

## 代币和网络选择：

- 始终以运行时环境输出的 `weave tokens` 为准。
- 不要在代码中硬编码代币或网络列表。
- 只有在需要接收支持多个网络的代币时，才需要使用 `--receive-network` 选项。
- 如果运行时环境支持，可以使用网络别名（例如 `Ethereum|ETH`、`Solana|SOL`、`Tron|TRX`）。

## 工作流程：

### 1) 创建发票

所需输入：
- `receive-token`（接收代币的命令）
- `amount`（正数字符串，表示金额）
- `wallet-address`（接收方钱包地址）
- `receive-network`（仅在运行时环境要求的代币/网络映射中需要提供）
- 可选字段：`buyer-name`（买家名称）、`buyer-email`（买家邮箱）、`buyer-address`（买家地址）

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

### 2) 生成支付报价

所需输入：
- `invoice-id`（发票 ID）
- `pay-token`（支付代币）
- `pay-network`（支付网络）
- `refund-address`（退款地址）

命令：
```bash
weave quote inv_123 \
  --pay-token USDT \
  --pay-network Ethereum \
  --refund-address 0x2222222222222222222222222222222222222222
```

预期的输出字段：
- `depositAddress`（存款地址）
- `depositMemo`（可选备注）
- `amountIn`（输入金额）
- `amountOut`（输出金额）
- `timeEstimate`（预计完成时间）
- `expiresAt`（到期时间）

### 3) 检查结算状态

**一次性操作：**
```bash
weave status inv_123
```

**监控模式：**
```bash
weave status inv_123 --watch --interval-seconds 5 --timeout-seconds 900
```

状态解释：
- 出口码 `0`：表示操作已完成（`COMPLETED`）、失败（`FAILED`）、已退款（`REFUNDED`）或已过期（`EXPIRED`）
- 出口码 `2`：表示监控超时（非命令失败）
- 出口码 `1`：表示命令/API/网络验证失败

## 错误处理：

当退出码为 `1` 时，如果存在错误信息，请以结构化的 JSON 格式显示出来。常见的错误信息格式如下：
```json
{
  "error": "api message",
  "status": 409,
  "details": {
    "error": "Invoice is not in PENDING status"
  }
}
```

如果监控超时（退出码 `2`），视为操作未完成，并非致命错误。建议增加 `--timeout-seconds` 参数或重新执行 `weave status <invoice-id>` 命令。

## 运行时环境变化规则：

安装的二进制文件和源代码库中的代币支持信息可能会发生变化。在确定有效的代币/网络组合时，始终使用运行时环境提供的 `weave tokens` 功能进行判断。