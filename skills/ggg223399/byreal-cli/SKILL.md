---
name: byreal-cli
description: "Byreal DEX（Solana）数据与分析命令行工具（CLI）：支持查询资金池、代币信息、TVL（总价值锁定）、APR（年化收益率）、K线图、矿工排名、Launchpad项目以及DeFi（去中心化金融）持仓统计等。当用户提及Byreal、LP（锁定池）分析、流动性数据或Solana DEX相关查询时，可使用该工具。"
metadata:
  openclaw:
    homepage: https://github.com/byreal-git/byreal-cli
    requires:
      bins:
        - byreal-cli
    install:
      - kind: node
        package: "@byreal-io/byreal-cli"
        global: true
---
# Byreal DEX 分析工具

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

如果发现有更新可用：

```bash
byreal-cli update install
```

## 凭据与权限

- 大多数命令仅具有 **读取权限**，无需使用钱包；
- 需要写入数据的命令需要通过 `byreal-cli setup` 进行钱包设置（该过程由 CLI 自动完成）；
- AI 机器人 **绝不应** 要求用户在聊天中输入私钥；请始终引导他们使用 `byreal-cli setup` 功能进行设置。

## 重要规则

1. **`-o json` 选项仅用于数据解析** — 在向用户展示结果时，请省略该选项，让 CLI 内置的表格或图表直接生成可视化结果。切勿先获取 JSON 数据后再手动绘制图表。
2. **切勿截断链上数据** — 对于交易签名（txid）、铸造地址、矿池地址、NFT 地址、钱包地址等数据，务必显示完整的内容，严禁使用 `xxx...yyy` 的缩写形式。
3. **先使用 `--dry-run` 选项进行预览，然后再使用 `--confirm` 选项执行实际操作**。
4. **涉及较大金额（>1000）的交易** 需要用户明确确认。
5. **如果交易滑点率超过 200 bp（百万分之一）**，必须向用户发出警告。