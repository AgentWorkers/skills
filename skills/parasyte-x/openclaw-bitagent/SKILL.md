---
name: bitagent-skill
description: 通过 CLI 在 BitAgent 的绑定曲线上启动、购买和出售代币。当用户需要创建新的代理代币，或在 BitAgent（BSC 测试网/主网）上交易现有代理代币时，可以使用此功能。
---

# BitAgent 技能

该技能使用 BitAgent SDK 与 BSC（Binance Smart Chain）上的绑定曲线（bonding curves）进行交互。它仅以 **命令行界面（CLI）** 的形式运行：代理必须执行 `scripts/index.ts` 脚本，并将命令的执行结果（stdout）返回给用户。

## 配置（必填）

如果未进行配置，请在 OpenClaw 的 `skills.entries.bitagent-skill.env`（或类似配置文件）中设置相关配置。

- `PRIVATE_KEY` — 钱包的私钥（格式为 0x...）

确保所有依赖项已安装在仓库的根目录下（使用 `npm install` 安装）。

## 运行方式（CLI）

从仓库的根目录运行命令，并设置相应的环境变量。CLI 会将执行结果输出到标准输出（stdout）中。您需要捕获这些输出结果并返回给用户。

| 工具            | 命令                                                                                                      | 结果                                                                                               |
| ------------ | ------------------------------------------------------------------------------------------------------------ | ---------------------------------------------------------------------------------------------------- |
| **launch**   | `npx tsx scripts/index.ts launch --network <bsc\|bscTestnet> --name "<name>" --symbol "<symbol>" --reserve-symbol "<UB\|WBNB\|USD1>"` | 在绑定曲线上部署一个新的代理代币。成功后返回合约地址和 URL。       |
| **buy**      | `npx tsx scripts/index.ts buy --network <bsc\|bscTestnet> --token "<tokenAddress>" --amount "<amount>"`                                  | 购买指定数量的代币。返回交易哈希值。                                          |
| **sell**     | `npx tsx scripts/index.ts sell --network <bsc\|bscTestnet> --token "<tokenAddress>" --amount "<amount>"`                                 | 卖出指定数量的代币。返回交易哈希值。                                         |

## 使用流程

1. **启动代理：** 当用户想要创建代币或代理时，运行 `launch` 命令。如果未提供名称、代币符号或储备代币（UB、WBNB、USD1），则需要用户手动输入这些信息。
2. **交易（买入/卖出）：** 当用户想要进行交易时，可以使用 `buy` 或 `sell` 命令。需要提供代币地址和交易金额。

## 文件结构

- **仓库根目录**：`SKILL.md`、`package.json`
- `scripts/index.ts`：包含 CLI 的实现代码。