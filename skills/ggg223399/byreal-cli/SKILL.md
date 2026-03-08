---
name: byreal-cli
description: "Byreal DEX（Solana）一体化命令行工具（CLI）：支持查询资金池、代币信息及总价值（TVL），分析资金池的年化收益率（APR）及风险状况，执行CLMM（Collateralized Loan Management）头寸的开设/关闭/赎回操作，支持代币兑换，以及钱包和余额管理。当用户提及Byreal、LP（Liquidity Provider）、流动性、资金池、DeFi（去中心化金融）头寸、代币兑换或Solana DEX相关操作时，请使用该工具。"
---
# Byreal LP管理

## 获取完整文档

在使用任何功能之前，请务必先运行以下命令，以获取最新、最完整的文档：

```bash
# Complete documentation (commands, parameters, workflows, constraints)
byreal-cli skill

# Structured capability discovery (all capabilities with params)
byreal-cli catalog list

# Detailed parameter info for a specific capability
byreal-cli catalog show <capability-id>
```

## 安装

```bash
# Check if already installed
which byreal-cli && byreal-cli --version

# Install
npm install -g @byreal-io/byreal-cli
```

## 检查更新

```bash
byreal-cli update check
```

如果存在更新：

```bash
byreal-cli update install
```

## 凭据与权限

- **只读命令**（如：pool、token、tvl、stats）：无需钱包
- **写入命令**（如：swap、position open/close/claim）：需要通过 `byreal-cli wallet set` 或 `byreal-cli setup` 设置钱包
- 私钥存储在本地文件 `~/.config/byreal/keys/` 中，并设置严格的文件权限（模式 0600）
- CLI 绝不会通过网络传输私钥——私钥仅用于本地交易签名
- AI 机器人 **绝不应** 要求用户在聊天中输入私钥；应始终引导用户通过 `byreal-cli setup` 以交互方式设置钱包

## 重要规则

1. **`-o json` 仅用于解析数据**——在向用户展示结果时，请省略该参数，让 CLI 的内置表格/图表直接进行渲染。切勿先获取 JSON 数据后再手动绘制图表。
2. **切勿截断链上数据**——始终显示完整的信息：交易签名（txid）、铸造地址、矿池地址、NFT 地址、钱包地址。严禁使用缩写形式（如 `xxx...yyy`）。
3. **切勿显示私钥**——仅显示密钥对的路径。
4. **先使用 `--dry-run` 进行预览，然后再使用 `--confirm` 进行正式操作。
5. **交易金额大于 1000 美元** 时，必须要求用户明确确认。
6. **滑点率超过 200 bps** 时，必须警告用户。
7. **执行写入操作前，请先检查钱包状态**——在任何需要使用钱包的命令之前，请先运行 `wallet address` 命令。