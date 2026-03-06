---
name: byreal-cli
description: "Byreal DEX（Solana）一体化命令行工具（CLI）：支持查询资金池、代币信息及总价值（TVL），分析资金池的年化收益率（APR）及风险状况，执行CLMM头寸的开设、关闭和赎回操作，支持代币兑换，以及钱包和余额管理。当用户提及Byreal、流动性池（LP）、去中心化金融（DeFi）头寸、代币兑换或Solana DEX相关操作时，可使用该工具。"
---
# Byreal LP Management

## 获取完整文档

请始终先运行以下命令，以获取完整且最新的文档：

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

# Install (one-time)
npm install -g https://github.com/byreal-git/byreal-cli/releases/latest/download/byreal-cli.tgz
```

## 检查更新

```bash
byreal-cli update check
```

如果有更新可用：

```bash
byreal-cli update install
```

## 硬性规定

1. **`-o json` 仅用于解析数据** — 在向用户展示结果时，请**省略该选项**，让 CLI 内置的表格/图表直接进行渲染。切勿先获取 JSON 数据后再手动绘制图表。
2. **切勿截断链上数据** — 对于交易签名（txid）、铸造地址、矿池地址、NFT 地址、钱包地址等，务必显示完整的字符串；严禁使用 `xxx...yyy` 的缩写形式。
3. **切勿显示私钥** — 仅使用密钥对路径。
4. **先使用 `--dry-run` 进行预览，然后再使用 `--confirm` 进行确认操作。
5. **交易金额大于 1000 美元** 时，必须获得用户的明确确认。
6. **滑点率超过 200 bps** 时，必须向用户发出警告。
7. **在执行写入操作前，请先检查钱包状态** — 在执行任何需要使用钱包的命令之前，务必先运行 `wallet address` 命令。