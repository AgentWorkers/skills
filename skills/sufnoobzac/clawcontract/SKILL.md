---
name: clawcontract
description: 这是一个基于人工智能的智能合约生成器、分析工具和部署工具，专为 BNB Chain（BSC/opBNB）设计。当您需要将自然语言转换为 Solidity 代码、进行安全分析、编译并部署智能合约、在 BscScan 或 opBNBScan 上验证合约源代码、与已部署的合约进行交互，或者执行完整的“生成→分析→部署→验证”流程时，都可以使用该工具。该工具支持 BSC 主网（bsc-mainnet）、BSC 测试网（bsc-testnet）以及 opBNB 主网（opbnb-mainnet）和 opBNB 测试网（opbnb-testnet）。
homepage: https://github.com/cvpfus/clawcontract
metadata: {"openclaw":{"requires":{"bins":["clawcontract"],"env":["OPENROUTER_API_KEY"]}}}
---

# ClawContract

通过命令行界面（CLI），在 BNB Chain 上生成、分析、部署和验证智能合约。

**获取与安装：** <https://github.com/cvpfus/clawcontract> — 克隆仓库，然后运行 `pnpm install && pnpm build && npm link`。

## 快速入门

生成智能合约：

    `clawcontract generate "用于点对点交易的托管合约，包含争议解决机制和超时自动释放功能"`

完整流程（生成 → 分析 → 部署 → 验证）：

    `clawcontract full "用于点对点交易的托管合约，包含争议解决机制和超时自动释放功能" --chain bsc-testnet`

部署现有的智能合约：

    `clawcontract deploy ./contracts/VibeToken.sol --chain bsc-testnet`

与已部署的智能合约交互：

    `clawcontract interact 0xABC... name --chain bsc-testnet`

## 设置

非交互式地生成 `.env` 文件：

    `clawcontract setup --openrouter-key <key>`

可选参数：`--private-key`、`--openrouter-key`、`--openrouter-model`、`--bscscan-key`。

## 参考资料

- **完整命令参考（所有参数、示例和说明）：** 请参阅 `{baseDir}/references/commands.md`

## 支持的链

| 关键字 | 链名 | 测试网 |
|-----|-------|---------|
| `bsc-mainnet` | BNB 智能链 | 不支持 |
| `bsc-testnet` | BNB 智能链测试网 | 支持 |
| `opbnb-mainnet` | opBNB | 不支持 |
| `opbnb-testnet` | opBNB 测试网 | 支持 |

默认值：`bsc-testnet`。

## 环境变量

| 变量 | 是否必需 | 用途 |
|----------|----------|---------|
| `OPENROUTER_API_KEY` | 是 | 用于生成智能合约 |
| `PRIVATE_KEY` | 部署时必需 | 用于部署的私钥，需用户提供 |
| `BSCSCAN_API_KEY` | 验证时必需 | 用于在 BscScan/opBNBScan 上验证合约 |
| `OPENROUTER_MODEL` | 可选 | 链模型（默认：anthropic/claude-sonnet-4-20250514） |

## 生成文件

在正常运行过程中，CLI 会在磁盘上生成以下文件：

| 文件路径 | 生成时机 | 文件内容 |
|------|------|----------|
| `contracts/*.sol` | 生成智能合约时 | 生成的 Solidity 源代码 |
| `.env` | 设置环境变量时 | 仅用户手动设置 |
| `.deployments/*.json` | 部署时 | 部署元数据（地址、链名、交易哈希） |

## 安全性注意事项

- **不会自动生成私钥。** 用户必须通过 `setup --private-key` 或直接设置环境变量来提供 `PRIVATE_KEY`。CLI 不会自行生成或保存私钥。
- 部署到主链时会显示额外的确认提示。
- CLI 完全是非交互式的——所有命令均无需用户输入即可执行。
- 对于高严重性的分析问题，CLI 会自动尝试修复（最多尝试 3 次）。
- 使用 `--skip-deploy` 选项可以在部署前查看生成的合约和分析结果。
- 使用 `--skip-fix` 选项可以禁用对高严重性问题的自动修复尝试。
- 初次测试时建议使用测试网和临时生成的密钥。