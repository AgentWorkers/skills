---
name: uniswap-v4
description: >
  Swap tokens and read pool state on Uniswap V4 (Base, Ethereum). Use when the agent
  needs to: (1) swap ERC20 tokens or ETH via Uniswap V4, (2) get pool info (price, tick,
  liquidity, fees), (3) find the best pool for a token pair, (4) quote expected swap output
  via the on-chain V4Quoter, (5) set up Permit2 approvals for the Universal Router, or
  (6) execute exact-input swaps with proper slippage protection. Supports Base and Ethereum
  mainnet, plus Base Sepolia testnet. TypeScript with strict types. Write operations
  need a private key via env var.
---

# Uniswap V4 🦄

在 Uniswap V4 中，您可以通过 Universal Router 来交换代币并查看池的状态。

**支持的链：** Base（8453）、Ethereum（1）、Base Sepolia（84532）

| 合同地址                | Base                                           | Ethereum                                     |
|------------------|----------------------------------------------|----------------------------------------------|
| PoolManager            | `0x498581fF718922c3f8e6A244956aF099B2652b2b`          | `0x000000000004444c5dc75cB358380D2e3dE08A90`           |
| UniversalRouter       | `0x6ff5693b99212da76ad316178a184ab56d299b43`          | `0x66a9893cC07D91D95644AEDD05D03f95e1dBA8Af`          |
| Permit2                | `0x000000000022D473030F116dDEE9F6B43aC78BA3`          | `0x000000000022D473030F116dDEE9F6B43aC78BA3`          |
| StateView             | `0xa3c0c9b65bad0b08107aa264b0f3db444b867a71`          | `0x7ffe42c4a5deea5b0fec41c94c136cf115597227`          |
| V4Quoter             | `0x0d5e0f971ed27fbff6c2837bf31316121532048d`          | `0x52f0e24d1c21c8a0cb1e5a5dd6198556bd9e1203`          |

> 合同地址来源于 [docs.uniswap.org/contracts/v4/deployments](https://docs.uniswap.org/contracts/v4/deployments)，验证日期：2026-02-08。

## 决策树

1. **查看池状态？** → `src/pool-info.ts`（免费，无需 gas，无需密钥）
2. **获取交换报价？** → `src/quote.ts`（免费，使用链上的 V4Quoter）
3. **批准代币交易？** → `src/approve.ts`（需要写入数据，约 100K gas，需要 `PRIVATE_KEY`）
4. **执行交换操作？** → `src/swap.ts`（需要写入数据，约 300-350K gas，需要 `PRIVATE_KEY`）
5. **如果是第一次使用 ERC20 代币？** → 先运行 `approve` 函数，或使用 `--auto-approve` 参数执行交换操作

## 脚本参考

所有脚本位于 `src/` 目录下。使用 `npx tsx` 命令运行这些脚本。输入 `--help` 可查看使用说明。

### pool-info.ts — 查看池状态（免费）

返回池 ID、sqrtPriceX96、tick 值、流动性、费用以及代币的符号和小数位数。
系统会自动根据流动性选择最佳池（或您可以通过 `--fee`/`--tick-spacing` 参数进行自定义选择）。

```bash
npx tsx src/pool-info.ts --token0 ETH --token1 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 --chain base --rpc $BASE_RPC_URL
```

**环境变量：** `BASE_RPC_URL` 或 `ETH_RPC_URL`（或使用 `--rpc` 参数）

### quote.ts — 获取交换报价（免费）

通过链上的 V4Quoter 合同获取精确的输入金额报价（仅用于模拟，不生成交易）。
返回预期的输出金额和所需 gas 量。

```bash
npx tsx src/quote.ts \
  --token-in ETH \
  --token-out 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --amount 10000000000000000 \
  --chain base \
  --rpc $BASE_RPC_URL
```

**环境变量：** `BASE_RPC_URL` 或 `ETH_RPC_URL`

### approve.ts — 设置代币交易批准权限（需要写入数据）

采用两步流程：首先使用 Permit2 合同，然后再使用 Universal Router 合同。
如果代币已经获得批准，则跳过此步骤。此功能仅适用于 ERC20 代币（不适用于 ETH）。

```bash
PRIVATE_KEY=0x... npx tsx src/approve.ts \
  --token 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --chain base \
  --rpc $BASE_RPC_URL \
  --json
```

**环境变量：** `PRIVATE_KEY`（必需），`BASE_RPC_URL`

### swap.ts — 执行交换操作（需要写入数据）

通过 Universal Router 执行精确输入的交换操作。首先获取报价，然后应用滑点设置，最后发送交易。

```bash
PRIVATE_KEY=0x... npx tsx src/swap.ts \
  --token-in ETH \
  --token-out 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --amount 10000000000000000 \
  --slippage 50 \
  --chain base \
  --rpc $BASE_RPC_URL \
  --json
```

如果启用自动批准功能（需要设置 Permit2 权限），则执行以下步骤：
```bash
PRIVATE_KEY=0x... npx tsx src/swap.ts \
  --token-in 0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913 \
  --token-out ETH \
  --amount 25000000 \
  --slippage 100 \
  --auto-approve \
  --chain base \
  --rpc $BASE_RPC_URL
```

**可选参数：** `--slippage <bps>`（默认值为 50%，即 0.5%），`--recipient <addr>`，`--auto-approve`，`--json`
**环境变量：** `PRIVATE_KEY`（必需），`BASE_RPC_URL`

## 代币输入

- `ETH` 或 `eth`：表示 V4 中的原生 ETH 代币（地址为 0）
- 合同地址：表示 ERC20 代币的地址
- 常见的 Base 代币示例：USDC（`0x833589fCD6eDb6E08f4c7C32D4f71b54bdA02913`）、WETH（`0x4200000000000000000000000000000000000006`）

## 环境变量

| 变量                          | 使用场景          | 是否必需 | 说明                                      |
|-----------------------------|----------------|---------|-----------------------------------------|
| `PRIVATE_KEY`        | approve、swap       | 是         | 钱包私钥（切勿通过 CLI 传递！）                         |
| `BASE_RPC_URL`       | 所有功能        | 否        | Base 主网的 RPC 地址                             |
| `ETH_RPC_URL`       | Ethereum 相关功能    | 否        | Ethereum 主网的 RPC 地址                             |
| `BASE_SEPOLIA_RPC_URL`    | 测试网相关功能    | 否        | Base Sepolia 测试网的 RPC 地址                             |

* **注意：** `PRIVATE_KEY` 仅在进行写入操作时必需。读取操作（如 pool-info、quote）不需要该密钥。

## V4 架构说明

- **Singleton PoolManager**：所有池的信息都存储在一个合约中。
- **状态数据**：通过 StateView 合同读取（该合约封装了 PoolManager 的存储数据）。
- **交换操作**：通过 `V4_SWAP` 命令在 Universal Router 和 PoolManager 之间进行。
- **权限批准**：ERC20 代币的交易需要经过 Permit2 和 Universal Router 两个步骤的批准。
- **池 ID**：`keccak256(abi.encode(currency0, currency1, fee, tickSpacing, hooks)` 的计算结果。
- **货币排序规则**：`currency0 < currency1`（按照数值大小排序，ETH 对应地址 0）。
- **操作顺序**：`SWAP_EXACT_IN_SINGLE (0x06) + SETTLE_ALL (0x0c) + TAKE_ALL (0x0f)`。
- 有关完整的编码规范，请参阅 `references/v4-encoding.md`。

## 错误处理

| 错误类型                        | 原因                                      | 解决方案                                      |
|------------------------------|--------------------------------------------|----------------------------------------|
| 未找到对应的 V4 池        | 该代币对未在 V4 中列出                   | 请检查输入的代币地址                         |
| 获取报价失败                | 池存在但无法执行交换操作                   | 请检查输入金额，池可能流动性不足                     |
| 需要 `PRIVATE_KEY`        | 缺少执行写入操作所需的环境变量                | 请在脚本中设置 `PRIVATE_KEY` 的值                   |
| 未配置 RPC 地址         | 未配置 RPC 连接信息                         | 请使用 `--rpc` 参数或设置相应的环境变量                 |
| 交易失败                         | 账户余额不足、交易超时或滑点设置不当                 | 请检查账户余额或调整滑点设置                     |
| 输入金额超出限制         | 输入的金额超过 V4 的处理上限                   | 请减少输入金额                         |

## 安全注意事项

- `PRIVATE_KEY` 必须通过环境变量或秘密管理工具进行传递。
- **严禁** 在聊天框中输入或发送 `PRIVATE_KEY`。
- **严禁** 将 `PRIVATE_KEY` 或 `.env` 文件提交到 Git 仓库。
- **注意：** `stdout` 和 `stderr` 的输出会被视为公开日志（包括在持续集成（CI）和终端界面中）。CI 测试会确保 `PRIVATE_KEY` 的值不会被显示。
- **严禁** 通过 CLI 参数传递私钥（所有脚本都会拒绝此类操作）。
- 私钥仅通过 `PRIVATE_KEY` 环境变量传递。
- 所有输入数据都会经过验证：地址格式、金额范围（使用 `BigInt` 类型）、滑点设置（0-10000%）。
- 代码中禁止使用 `eval()`、`exec()` 等函数，以及 Shell 命令；所有计算都使用纯 TypeScript 完成。
- 代币金额一律使用 `BigInt` 类型表示（避免浮点数和溢出问题）。

## 测试说明

```bash
npm run test:unit      # Unit tests (no network)
npm run test:fork      # Fork tests (needs: anvil --fork-url https://mainnet.base.org)
npm run test:testnet   # Testnet reads (Base Sepolia)
npm run test:mainnet   # Mainnet smoke tests (read-only)
npm run security       # Security scan
```

## 参考资料

- V4 编码规范：`references/v4-encoding.md`
- 合同地址列表：`references/addresses.md`
- V4 架构文档：`references/v4-architecture.md`