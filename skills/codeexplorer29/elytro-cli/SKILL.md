---
name: elytro-skills
description: Elytro钱包技能的入口点，以及精心挑选的DeFi子技能。在加载任何特定的协议技能之前，请先从这里开始。
user-invocable: false
disable-model-invocation: false
---
# Elytro 技能包

欢迎使用！`elytro` 命令行界面（CLI）会在执行 `elytro --help` 时显示此 URL，确保用户在使用钱包之前能够先查看官方指南。请阅读本文档，然后开始学习下面的子技能。

> 在 `elytro --help` 中显示的原始链接：`https://raw.githubusercontent.com/Elytro-eth/skills/main/SKILL.md`

**需要交换代币吗？** 请安装 `defi/uniswap/SKILL.md`（位于 `./defi/uniswap` 目录下）。  
**需要执行其他去中心化金融（DeFi）协议的操作吗？** 请同时安装 해당协议的文件夹（例如 `defi/pendle/SKILL.md`）以及 `defi/elytro/SKILL.md`。

## 开始使用

1. **安装 Elytro CLI**：`npm install -g @elytro/cli`（建议使用 Node.js 24 及更高版本）。大多数操作都需要使用 CLI 命令，因此请确保已安装该工具。
2. **加载 `elytro` 钱包相关的技能**：该技能文件位于 `elytro/SKILL.md`。它涵盖了账户管理、内联按钮的用户界面规则以及 Elytro 特有的安全指南。
3. **选择合适的 DeFi 协议**：请查看 `defi/SKILL.md`。该文件会链接到各个 DeFi 协议的详细说明（目前主要是 Uniswap，未来还会添加更多协议）以及执行相关的指南（`defi/elytro/SKILL.md`）。
4. **按需组合使用技能**：进行代币交换时，通常需要同时加载以下三个技能：
   - `elytro`：钱包用户界面、菜单功能及账户安全设置。
   - `defi`：负责路由管理和操作流程的脚本。
   - `defi/uniswap`：提供 Uniswap 的智能合约操作提示。

## 技能结构图

| 路径                | 描述                                                                 | 使用场景                                                                 |
|------------------|---------------------------------------------------------------------------|------------------------------------------------------------------------------------|
| `elytro/`           | Elytro 钱包的核心技能，包括内联按钮规则和菜单功能。                          | 与 Elytro 智能合约相关的所有操作（如查看余额、发送交易、部署合约、确保账户安全）。           |
| `defi/`            | 用于处理 DeFi 操作的通用技能，会链接到具体的协议技能。                      | 当用户请求执行 DeFi 操作但尚未选择具体协议时使用。                          |
| `defi/elytro/`         | 将智能合约的指令/数据传递给 Elytro 智能合约的执行桥梁。                    | 负责执行 Uniswap 的智能合约指令、传递相关数据、模拟交易并发送交易请求。                |
| `defi/uniswap/`        | 提供 Uniswap 的智能合约操作提示和安全保障机制。                        | 用于代币交换、管理流动性池（LP）以及在执行前提供分析数据。                         |
| `payroll/`          | 用于管理 Elytro 智能合约的工资发放流程。                          | 每个支付周期会手动批准 ETH/USDC 的定期支付。                         |

你可以在 `defi/` 目录下创建更多子文件夹（格式为 `defi/<协议>/SKILL.md`），系统会自动将这些文件夹链接到技能包中。

## 安装指南

```bash
# Install the whole pack (skills CLI)
npx skills add Elytro-eth/skills

# Focus on the Elytro wallet skill
npx skills add Elytro-eth/skills --skill elytro

# Uniswap planner only
npx skills add Elytro-eth/skills --skill defi/uniswap
```

Clawhub 用户只需添加一次仓库，然后根据工作需求启用相应的文件夹即可。无需重新打包文件；Clawhub 会自动保持文件夹结构（如 `<folder>/SKILL.md`）的格式。