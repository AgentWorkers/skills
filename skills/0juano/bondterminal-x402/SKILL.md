---
name: bondterminal-x402
description: 通过 `btx` CLI 使用 x402 无密钥支付功能查询 BondTerminal API 端点。当用户在没有 API 密钥的情况下请求 BondTerminal 的债券数据时，可以使用此方法。该方法涉及 x402、PAYMENT-SIGNATURE、按次无密钥支付、债券分析、现金流、历史记录、国家风险（riesgo país）以及 ISIN/股票代码（例如 AL30、GD30、US040114HS26）的查询。支持债券列表/详情/分析/现金流/历史记录的查询，以及单只债券的计算功能；同时具备自动处理 402 错误、支付失败和重试的机制。
metadata:
  author: 0juano
  version: "1.0.0"
---
# BondTerminal x402

使用此技能可以通过 x402 按次付费认证方式获取 BondTerminal 数据（无需使用 Bearer API 密钥）。
费用：**基础主网上的每个付费请求费用为 0.01 美元（USDC）**。

## 设置

脚本位置：
- `{baseDir}/scripts/btx`

将其设置为可执行文件：

```bash
chmod +x {baseDir}/scripts/btx
```

安装运行时依赖项（每个工作区只需安装一次）：

```bash
npm install @x402/core @x402/evm viem
```

必需的环境变量（任一名称均可）：

```bash
export X402_PRIVATE_KEY=0x... # EVM private key used to sign x402 payments
# or
export EVM_PRIVATE_KEY=0x...
```

可选的环境变量：

```bash
export BT_API_BASE_URL=https://bondterminal.com/api/v1
# Optional module-resolution override:
# export BTX_MODULE_BASE=/path/to/BondTerminal
```

参考文档：
- `https://bondterminal.com/developers`
- `https://bondterminal.com/developers.md`
- `https://bondterminal.com/api/v1/docs/`

## 资金要求

在付费请求成功结算之前，签名钱包必须满足以下条件：
- 拥有基础网络（Base）上的 USDC（用于支付 0.01 美元）
- 拥有基础网络（Base）上的少量 ETH（用于支付交易手续费）

如果缺少任意一种余额，支付可能会在结算过程中失败。

## 命令

在任意命令后添加 `--json` 选项，以获取机器可读的输出格式。

## 操作说明

- CLI 会首先正常调用相应的 API 端点。
- 如果响应代码为 `402`，则表示需要支付费用，系统会生成已签名的支付请求并自动重试。
- 如果响应代码为 `401`，则可能表示该部署未启用 x402 认证方式。
- `POST /calculate/batch` 命令仅支持 Bearer 认证方式，不属于此技能的范畴。
- 成功完成付费请求后，CLI 会将结算元数据（`payer`、`transaction`、`network`）输出到标准错误流（stderr）中。

## 故障排除

- 必须在 shell 中设置 `X402_PRIVATE_KEY` 或 `EVM_PRIVATE_KEY` 中的一个。
- 私钥格式无效：请确保私钥为 32 字节的十六进制字符串，并以 `0x` 开头。
- 报错信息 `401 Authorization header required` 表示目标 API 路由不支持 x402 认证方式。
- 报错信息 `403 Batch requires API key subscription` 表示 `/calculate/batch` 命令需要 API 密钥。
- 结算或支付失败时，请检查钱包中的 USDC 余额以及基础网络（Base）上的 ETH 手续费余额。