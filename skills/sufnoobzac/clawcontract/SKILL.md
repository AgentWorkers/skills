---
name: clawcontract
description: 这是一个基于人工智能的智能合约生成器、分析工具和部署工具，专为 BNB Chain（BSC/opBNB）平台设计。当您需要将自然语言文本转换为 Solidity 代码、进行安全分析、编译并部署智能合约、在 BscScan 或 opBNBScan 上验证合约代码、与已部署的合约进行交互，或者执行完整的“生成→分析→部署→验证”流程时，都可以使用该工具。该工具支持 BSC 主网（bsc-mainnet）、BSC 测试网（bsc-testnet）以及 opBNB 主网（opbnb-mainnet）和 opBNB 测试网（opbnb-testnet）。
homepage: https://github.com/cvpfus/clawcontract
metadata: {"openclaw":{"requires":{"bins":["clawcontract"],"env":["CLAWCONTRACT_OPENROUTER_API_KEY","CLAWCONTRACT_PRIVATE_KEY","CLAWCONTRACT_BSCSCAN_API_KEY"]},"install":[{"id":"clawcontract","kind":"node","package":"clawcontract","bins":["clawcontract"],"label":"Install clawcontract (npm)"}]}}
---
# ClawContract

通过命令行界面（CLI）在 BNB 链上生成、分析、部署和验证智能合约。

**来源与安装：** <https://github.com/cvpfus/clawcontract> — 克隆仓库，然后运行 `pnpm install && pnpm build && npm link`。

## 快速入门

生成一个合约：

    `clawcontract generate "用于点对点交易的托管合约，包含争议解决机制和超时自动释放功能"`

完整的流程（生成 → 分析 → 部署 → 验证）：

    `clawcontract full "用于点对点交易的托管合约，包含争议解决机制和超时自动释放功能" --chain bsc-testnet`

部署一个现有的合约：

    `clawcontract deploy ./contracts/VibeToken.sol --chain bsc-testnet`

与已部署的合约交互：

    `clawcontract interact 0xABC... name --chain bsc-testnet`

列出部署记录：

    `clawcontract list`
    `clawcontract list --chain bsc-testnet`

删除部署记录：

    `clawcontract delete 0xABC...def`

## 参考资料

- **完整命令参考（所有参数、示例和说明）：** 请参阅 `{baseDir}/references/commands.md`

## 支持的链

| 关键参数 | 链 | 测试网 |
|-----|-------|---------|
| `bsc-mainnet` | BNB 智能链 | 不支持 |
| `bsc-testnet` | BNB 智能链测试网 | 支持 |
| `opbnb-mainnet` | opBNB | 不支持 |
| `opbnb-testnet` | opBNB 测试网 | 支持 |

默认值：`bsc-testnet`。

## 环境变量

可以通过 `docker-compose.yml` 配置，或直接在环境中设置。

| 变量 | 是否必填 | 用途 |
|----------|----------|---------|
| `CLAWCONTRACT_OPENROUTER_API_KEY` | 是 | 用于生成智能合约 |
| `CLAWCONTRACT_PRIVATE_KEY` | 部署时需要 | 用于部署的钱包密钥 — 必须由用户提供 |
| `CLAWCONTRACT_BSCSCAN_API_KEY` | 验证时需要 | 用于在 BscScan/opBNBScan 上验证合约 |
| `CLAWCONTRACT_OPENROUTER_MODEL` | 可选 | 模型覆盖（默认值：anthropic/claude-sonnet-4-20250514） |

## 生成文件

在正常运行过程中，CLI 会在磁盘上生成以下文件：

| 文件路径 | 生成时机 | 文件内容 |
|------|------|----------|
| `contracts/*.sol` | 生成合约时 | 生成的 Solidity 源代码 |
| `.deployments/*.json` | 部署时 | 部署元数据（地址、链、交易哈希） |

## 安全性注意事项

- **不会自动生成密钥。** `CLAWCONTRACT_PRIVATE_KEY` 必须通过环境变量由用户明确提供。CLI 不会自行生成或保存私钥。
- **关于主网的警告（非阻塞式操作）。** 部署到主网时会显示关于实际费用的警告，但不会阻止操作继续进行 — 这是设计上的考虑：CLI 主要用于代理驱动的自动化流程，这些流程可能无法使用标准输入（stdin）。用户可以通过 `--chain` 参数显式选择部署目标（默认为 `bsc-testnet`）。
- **删除操作会显示确认提示。** `delete` 是唯一的交互式命令，它会显示部署详情并询问用户是否要删除该合约（y/N）。可以使用 `--force` 参数跳过此提示（更适用于自动化流程）。这样做是安全的，因为 `delete` 命令仅删除本地元数据，不会影响链上的状态。
- **自动修复机制。** 在执行 `full` 命令时，如果发现严重问题，AI 会尝试修复并重新分析合约（最多进行 3 次尝试）。这意味着代理可以在部署前修改生成的源代码。相应的应对措施包括：
  - 使用 `--skip-fix` 参数完全禁用自动修复功能。
  - 使用 `--skip-deploy` 参数在执行任何链上操作之前查看最终的源代码和分析结果。
  - 修复操作仅针对 `contracts/` 目录下的文件，不会修改其他文件。
- **意外部署到主网的风险。** 由于部署需要 `CLAWCONTRACT_PRIVATE_KEY`，且默认链为 `bsc-testnet`，因此如果意外将合约部署到主网，用户必须同时设置主网密钥，并明确指定 `--chain bsc-mainnet` 或 `--chain opbnb-mainnet`。这两种操作都不能在后台默默完成。
- **建议在初期测试时使用测试网和临时生成的密钥。**