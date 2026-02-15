---
name: chaoschain
description: 通过 ERC-8004 标准，在链上注册表中验证 AI 代理的身份和声誉。
user-invocable: true
metadata: {"openclaw": {"emoji": "⛓️", "requires": {"bins": ["python3"]}, "homepage": "https://chaoscha.in", "skillKey": "chaoschain"}}
---

# ChaosChain - 在链上的代理信任与声誉系统

ChaosChain 是为 AI 代理提供的 **信任层**。该工具允许您验证代理的身份，并从 [ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) 注册表中查看代理的链上声誉分数。

## 该工具的功能

✅ **验证** - 检查代理是否在链上注册
✅ **查看声誉** - 查看代理的多维声誉分数
✅ **评估信任** - 在信任其他代理之前做出明智的决策

❌ 该工具不执行工作流程、提交任务或处理支付。
❌ 默认情况下，它仅提供 **只读** 的信任信息可视化功能。

## 命令

### `/chaoschain verify <agent_id_or_address>`

检查代理是否在 ERC-8004 上注册，并查看其基本信息。

**返回内容：**
- 注册状态
- 代理名称和域名（如果存在）
- 所有者地址
- 信任分数摘要

### `/chaoschain reputation <agent_id_or_address>`

查看代理的详细多维声誉分数。

**返回的五个评估维度：**
- 积极性
- 协作性
- 推理能力
- 合规性
- 效率

### `/chaoschain whoami`

检查您的代理钱包是否在链上注册。

**使用说明：**
需要设置 `CHAOSCHAIN_PRIVATE_KEY` 或 `CHAOSCHAIN_ADDRESS`。

### `/chaoschain register` （可选 - 链上操作）

⚠️ **警告：此命令会执行链上交易。**

在 ERC-8004 身份注册表中注册您的代理。

**使用要求：**
- 必须设置 `CHAOSCHAIN_PRIVATE_KEY`
- 钱包中必须有足够的 ETH 作为交易费用（约 0.001 ETH）
- 每个钱包只能注册一次

**安全默认设置**：注册操作默认在 **Sepolia 测试网** 上进行，以防止意外地在主网上进行交易。如需在生产环境中使用，请明确指定 `--network mainnet`。

## 网络默认设置

| 命令 | 默认网络 | 原因 |
|---------|-----------------|--------|
| `verify` | 主网 | 查看生产环境中的声誉数据 |
| `reputation` | 主网 | 查看生产环境中的声誉数据 |
| `whoami` | 主网 | 检查代理是否在主网上注册 |
| `register` | **Sepolia** | 为安全起见，避免在主网上进行交易 |

您可以使用 `--network <network_key>` 来更改网络设置：

## 设置

### 安装后（只需执行一次）

运行设置脚本以安装 Python 依赖项：

**此脚本会创建一个包含 `web3` 及其他依赖项的虚拟环境。**

### 只读模式（默认）

运行 `setup.sh` 后无需额外设置！只需使用 `/chaoschain verify` 和 `/chaoschain reputation` 即可。

### 使用自己的钱包（可选）

若要使用 `/chaoschain whoami` 或 `/chaoschain register`，请将其添加到您的 OpenClaw 配置文件中。

### 注册代理（链上操作）

### 网络选项

**主网地址（所有支持的以太坊主网）：**
- `ethereum_mainnet`
- `base_mainnet`
- `polygon_mainnet`
- `arbitrum_mainnet`
- `celo_mainnet`
- `gnosis_mainnet`
- `scroll_mainnet`
- `taiko_mainnet`
- `monad_mainnet`
- `bsc_mainnet`

**测试网地址（所有支持的以太坊测试网）：**
- `ethereum_sepolia`
- `base_sepolia`
- `polygon_amoy`
- `arbitrum_testnet`
- `celo_testnet`
- `scroll_testnet`
- `monad_testnet`
- `bsc_testnet`
- `optimism_sepolia`
- `linea_sepolia`
- `mode_testnet`

**兼容性说明：**
- `mainnet` 等同 `ethereum_mainnet`
- `sepolia` 等同 `ethereum_sepolia`

## 示例用法

**在信任代理执行任务之前：**

**查看代理的详细声誉信息：**

## 什么是 ERC-8004？

[ERC-8004](https://eips.ethereum.org/EIPS/eip-8004) 是以太坊的 **去中心化代理** 标准。它提供了以下功能：**
- **身份注册表** - 基于 NFT 的代理链上注册
- **声誉注册表** - 代理的反馈和声誉分数
- **验证注册表** - 独立的验证记录

ChaosChain 是 ERC-8004 的参考实现。

## 合同地址

| 网络 | 注册表地址 | 地址 |
|---------|----------|---------|
| 主网（所有支持的主网） | 身份注册表 | `0x8004A169FB4a3325136EB29fA0ceB6D2e539a432` |
| 主网（所有支持的主网） | 声誉注册表 | `0x8004BAa17C55a88189AE136b182e5fdA19dE9b63` |
| 测试网（所有支持的测试网） | 身份注册表 | `0x8004A818BFB912233c491871b3d84c89A494BD9e` |
| 测试网（所有支持的测试网） | 声誉注册表 | `0x8004B663056A597Dffe9eCcC1965A193B7388713` |

## 更多信息

- [ChaosChain 文档](https://docs.chaoscha.in)
- [ERC-8004 规范](https://eips.ethereum.org/EIPS/eip-8004)
- [8004scan.io](https://8004scan.io) - 代理信息查询工具
- [GitHub](https://github.com/ChaosChain/chaoschain)

## 安全注意事项

- 该工具默认为 **只读** 模式
- `/chaoschain register` 是唯一一个会写入链上数据的命令
- 私钥仅用于注册，绝不用于查看信息
- 不会转移任何资金，仅消耗交易费用
- 源代码位于：`{baseDir}/scripts/`