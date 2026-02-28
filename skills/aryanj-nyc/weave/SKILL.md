---
name: weave
description: >
  **使用说明：**  
  在通过 `weave CLI` 创建 Weave Cash 的加密货币对加密货币类型的发票、生成支付报价，或监控发票支付状态时，请使用以下方法。
license: AGPL-3.0-or-later
metadata:
  openclaw:
    requires:
      bins:
        - weave
    emoji: "🧶"
    homepage: "https://www.weavecash.com"
  clawdbot:
    requires:
      bins:
        - weave
    emoji: "🧶"
    homepage: "https://www.weavecash.com"
---
# Weave

## 概述

使用 `weave` 可以完成 Weave Cash 发票的完整生命周期管理工作，包括：

1. 创建发票 (`weave create`)
2. 生成支付指令 (`weave quote`)
3. 跟踪结算进度 (`weave status` 或 `weave status --watch`)

## 规范要求：

- 仅支持加密货币之间的交易，禁止使用法定货币、法定货币转换或以法定货币计价的功能。
- 输出格式应采用机器可读的 JSON 格式；仅在用户明确要求时才使用 `--human` 选项。
- 绝不要在输出中泄露任何敏感信息（如私钥、令牌、JWT 等）。
- 将网络/API 调用视为可能出错的操作，并对非零退出码进行妥善处理。

## 不适用场景：

- 严禁将此工具用于处理法定货币发票或法定货币结算相关的工作流程。
- 严禁使用此工具编辑 Weave 的 Web UI 或前端代码。
- 严禁将此工具用于与钱包保管或私钥管理无关的任务。
- 当用户需要使用非 Weave 支付方式时，严禁使用此工具。

## 使用前的准备工作：

1. 确保命令行工具 (`CLI`) 可用：
   ```bash
weave --help
```

2. 在选择交易资产之前，先确认运行时环境是否支持相应的令牌和网络：
   ```bash
weave tokens
```

3. 如果 `weave` 工具未安装，请指导用户进行安装（不要自动执行安装过程）：
   ```bash
curl -fsSL --proto '=https' --tlsv1.2 https://www.weavecash.com/install.sh | bash
```

## 安装流程：

```bash
curl -fsSL --proto '=https' --tlsv1.2 -o /tmp/weave-install.sh https://www.weavecash.com/install.sh
less /tmp/weave-install.sh
bash /tmp/weave-install.sh
```

## 令牌与网络的选择：

- 始终使用运行时环境生成的 `weave tokens` 作为有效令牌来源。
- 不要在代码中硬编码令牌或网络列表。
- 仅当需要接收支持多个网络的令牌时，才使用 `--receive-network` 选项。
- 运行时环境支持的情况下，可以使用网络别名（例如 `Ethereum|ETH`、`Solana|SOL`、`Tron|TRX`）。

## 工作流程：

### 1) 创建发票

需要收集以下信息：
- `receive-token`
- `amount`（正数字符串）
- `wallet-address`
- 根据运行时环境的要求，可能需要提供 `receive-network`
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

请记录发票的 `id`，以便后续进行 `quote` 或 `status` 操作。

### 2) 生成支付指令

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

预期的输出字段：
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

- 监控模式：
   ```bash
weave status inv_123 --watch --interval-seconds 5 --timeout-seconds 900
```

状态解释：
- 出口码 `0` 表示操作已完成（`COMPLETED`、`FAILED`、`REFUNDED`、`EXPIRED`）
- 出口码 `2` 表示监控超时（非命令失败）
- 出口码 `1` 表示命令或网络验证失败

## 错误处理：

当出现错误（退出码为 `1`）时，应输出结构化的 JSON 错误信息。常见的 API 错误格式如下：
```json
{
  "error": "api message",
  "status": 409,
  "details": {
    "error": "Invoice is not in PENDING status"
  }
}
```

如果监控超时（退出码为 `2`），应视为操作未完成，而非致命错误。建议增加 `--timeout-seconds` 参数来延长监控时间，或重新执行 `weave status <invoice-id>` 命令。

## 运行时环境的变化：

已安装的二进制文件和源代码库中的令牌支持配置可能会发生变化。在确定有效的令牌/网络组合时，务必使用运行时环境提供的信息（`weave tokens`）。