---
name: renzo
description: 查询 Renzo 加密货币的流动性重新质押协议：DeFi 保险库的收益、TVL（总价值锁定）、ezETH 的交易汇率、EigenLayer 运营者，以及支持的 Ethereum 和 Solana 区块链网络。
metadata:
  openclaw:
    emoji: "\U0001F7E2"
    requires:
      bins: ["curl", "jq"]
---
# Renzo 协议

该技能用于查询 Renzo 液态重置（liquid restaking）协议的相关数据，包括 ezETH 指标、金库信息、协议统计信息、支持的区块链网络以及运营商详情。

## 使用场景

当用户询问以下内容时，可激活此技能：
- Renzo 协议、ezETH、pzETH、ezSOL 或任何 Renzo 金库代币的相关信息
- Renzo 的液态重置收益、年化收益率（APR）或质押回报
- Renzo 的总锁定价值（TVL）或协议统计数据
- Renzo 金库的详细信息、性能或比较
- Renzo 支持的区块链网络
- 通过 Renzo 委托的 EigenLayer 运营商
- Renzo 上的机构金库管理

## 可用工具

辅助脚本 `renzo-mcp.sh`（位于该技能的目录中）会调用 Renzo MCP 服务器，并返回格式化的 JSON 数据。

| 工具 | 功能 | 参数 |
|------|---------|-----------|
| `get_ezeth_info` | 获取 ezETH 的指标：年化收益率（APR）、供应量、总锁定价值（TVL）、价格、汇率 | 无 |
| `get_protocol_stats` | 获取协议统计信息：总锁定价值（TVL）、年化收益率（APR）、支持的区块链网络数量 | 无 |
| `get_supported_chains` | 列出 Renzo 支持的区块链网络 | 无 |
| `get_vaults` | 列出具有锁定价值（TVL）和年化收益率（APR）的金库 | 可选参数：`{"ecosystem":"eigenlayer"}`（eigenlayer、symbiotic、jito、generic） |
| `get_vault_details` | 获取单个金库的详细信息 | 必需参数：`{"vaultId":"<符号或地址>"}` |
| `get_operators` | 获取协议运营商列表 | 可选参数：`{"product":"ezETH"}`（ezETH、pzETH、ezSOL 等） |

## 使用方法

通过 Bash 工具运行辅助脚本。脚本路径相对于该技能的目录。

```bash
# No arguments
./skills/renzo/renzo-mcp.sh get_ezeth_info
./skills/renzo/renzo-mcp.sh get_protocol_stats
./skills/renzo/renzo-mcp.sh get_supported_chains

# With optional filter
./skills/renzo/renzo-mcp.sh get_vaults '{"ecosystem":"jito"}'
./skills/renzo/renzo-mcp.sh get_operators '{"product":"pzETH"}'

# With required argument
./skills/renzo/renzo-mcp.sh get_vault_details '{"vaultId":"ezREZ"}'
```

## 数据展示规则

为便于阅读，请遵循以下格式规则：
- **年化收益率（APR/APY）**：以百分比形式显示，保留两位小数（例如：“2.84%”）
- **总锁定价值（TVL）**：以美元为单位，使用逗号分隔，并保留两位小数（例如：“$430,813,580.01”）。对于超过 100 万美元的数值，可使用简写形式（例如：“$430.8M”）
- **汇率**：显示 4-6 位小数（例如：“1.0721 ETH 每 ezETH”）
- **代币数量**：保留 2-4 位小数，并显示代币符号
- **表格**：在比较金库或列出多个项目时使用 Markdown 表格
- **说明**：为不熟悉液态重置机制的用户简要解释各项数据的含义

### 示例：ezETH 信息响应

`get_ezeth_info` 工具返回的结果如下：
```json
{
  "token": "ezETH",
  "aprPercent": 2.83,
  "aprAvgPeriodDays": 30,
  "totalSupplyEth": 215986.82,
  "lpTotalSupply": 201461.43,
  "tvlUsd": 430813580.00,
  "ethPriceUsd": 2138.44,
  "exchangeRate": 1.0721
}
```

展示方式如下：
> **ezETH** 当前的年化收益率为 **2.83%**（30 天平均值）。汇率为 **1.0721 ETH 每 ezETH**，总锁定价值为 **$430.8M**，总供应量为 **215,987 ETH**。

### 示例：金库比较

在列出金库信息时，可以使用表格格式：

| 金库 | 基础资产 | 年化收益率（APR） | 总锁定价值（TVL） | 生态系统（Ecosystem） |
|-------|-----------|-----|-----|-----------|
| ezSOL | SOL | 6.41% | $6.4M | Jito |
| ezEIGEN | EIGEN | 18.23% | $329.6K | EigenLayer |
| ezREZ | REZ | 1.64% | $2.5M | EigenLayer |

### 示例：协议概述

对于一般性的关于 Renzo 的问题，可以同时调用 `get_protocol_stats` 和 `get_ezeth_info`，然后进行总结：
> Renzo 是一个液态重置协议，总锁定价值为 **$469.5M**，支持 **8 个区块链网络**。旗舰产品 ezETH 的年化收益率为 **2.84%**，而 pzETH 的年化收益率为 **2.34%**。该协议支持 EVM 系统（Ethereum、Arbitrum、Base、Linea、BNB Chain、Mode、Blast）和 Solana 网络。

## 选择合适的工具

| 用户问题 | 应使用的工具 |
|-------------------|------|
| ezETH 的价格、汇率、收益、年化收益率（APR）、总锁定价值（TVL） | `get_ezeth_info` |
| Renzo 的整体统计信息、总锁定价值（TVL） | `get_protocol_stats` |
| Renzo 支持的区块链网络 | `get_supported_chains` |
| 可用的金库、金库收益、金库比较 | `get_vaults` |
| 特定金库的详细信息（按名称或符号） | `get_vault_details` 并提供相应的金库符号 |
| EigenLayer 运营商、验证者、委托信息 | `get_operators` |
| Renzo 的总体概述 | `get_protocol_stats` + `get_ezeth_info` |
| “我能获得多少收益？” | `get_vaults`（显示所有金库的年化收益率） |

当用户询问特定金库的详细信息时，首先使用 `get_vaults` 查找该金库的符号，然后使用 `get_vault_details` 获取详细信息。

## 错误处理

如果脚本执行过程中出现错误：
- **网络故障**：告知用户 Renzo MCP 服务器无法访问，并建议稍后再试
- **未知的工具**：这可能是技能中的错误，请报告尝试使用的工具名称
- **无效的参数格式**：检查参数格式是否与工具要求一致
- **服务器错误**：展示服务器返回的错误信息

切勿直接向用户显示原始的 JSON 错误输出，应使用简洁的语言总结问题。