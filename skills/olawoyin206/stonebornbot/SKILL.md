---
name: StonebornBot
description: 这是一个专为以太坊（Ethereum）和EVM（Ethereum Virtual Machine）链设计的高速NFT铸造机器人。当用户需要快速抢购NFT、批量铸造NFT集合、设置多钱包铸造脚本、使用预签名交易进行NFT铸造自动化操作，或在多个钱包间实现NFT铸造自动化时，可以使用该工具。该机器人支持ERC721A标准、Archetype合约、Flashbot技术、战争模式（war mode）下的gas费用优化、WebSocket实时监控、内存池（mempool）动态观察，以及支持100多个钱包的批量铸造功能。
---

# NFT铸造机器人

这款NFT铸造机器人能够在100毫秒内完成铸造操作，支持多钱包管理、预签名交易以及多RPC广播功能。

## 快速入门

```bash
# 1. Setup
cd scripts && bash setup.sh && cd ..

# 2. Configure
cp assets/config-template.json scripts/config.json
# Edit scripts/config.json with your RPC URLs, contract, wallets, gas settings

# 3. Run (instant mode — fire immediately)
node scripts/mint-bot.js

# 4. Run (monitor mode — wait for mint to go live)
node scripts/mint-bot.js --mode monitor
```

## 配置概览

请编辑 `scripts/config.json` 文件。主要配置项包括：

- **rpcUrl / rpcUrls**：主RPC端点和备用RPC端点，用于多路广播。
- **wsRpcUrl**：用于订阅区块信息和监控内存池的WebSocket RPC接口。
- **contract**：目标合约地址、铸造函数签名、参数、价格、每个钱包的最大铸造数量以及合约的ABI（应用程序接口）。
- **gas**：EIP-1559相关的Gas设置（`maxFeePerGas`、`maxPriorityFeePerGas`、`gasLimit`）。详情请参阅 [gas-optimization.md](references/gas-optimization.md)。
- **wallets**：一个包含 `{privateKey, label}` 的数组，用于存储钱包信息。详情请参阅 [wallet-management.md](references/wallet-management.md)。
- **monitoring**：操作模式（`instant` 或 `monitor`），以及数据更新间隔和WebSocket/内存池监控选项。
- **archetype**：支持基于邀请（invite-based）的ERC721a合约铸造方式。详情请参阅 [archetype.md](references/archetype.md)。
- **flashbots**：用于提交私密交易的保护机制。
- **bankr**：集成Bankr API以实现钱包的自动化管理。
- **retry**：最大重试次数以及每次尝试之间的延迟时间。

## 操作模式

### 即时模式 (`"mode": "instant"`)
立即执行交易。适用于铸造功能已经上线或已知确切区块编号的情况。

### 监控模式 (`"mode": "monitor"`)
定期向合约发送请求以检测铸造功能是否可用，然后执行交易。支持以下选项：
- **Polling** (`intervalMs`)：通过 `staticCall` 每N毫秒检查一次合约状态。
- **WebSocket blocks** (`useWebSocket: true`)：在新区块生成时立即响应。
- **Mempool watching** (`mempoolWatch: true`)：监控内存池中待处理的铸造相关交易。

您可以将 `mintLiveCheck` 设置为 `"staticCall"`，或使用 `flagFunction` 来指定特定的合约查询函数。

## ERC721a合约支持

对于需要基于邀请和身份验证的ERC721a合约，此机器人提供了相应的支持。详情请参阅 [archetype.md](references/archetype.md)。

## 战时模式（War Mode）下的Gas策略

当 `gas.warMode.enabled` 为 `true` 时，机器人在网络拥堵时会自动增加Gas费用，但费用上限仍受配置值限制。详情请参阅 [gas-optimization.md](references/gas-optimization.md)。

## 多钱包支持

支持200多个钱包，支持批量签名操作。所有交易在广播前都会被预先签名。详情请参阅 [wallet-management.md](references/wallet-management.md)。

## 批量测试

使用 `scripts/batch-test.js` 脚本测试钱包的签名速度和RPC连接稳定性，无需实际发送交易。

## 架构说明

- **预签名交易**：所有交易在广播前都会由相应的钱包进行签名。
- **多RPC广播**：所有签名后的交易会同时发送到所有RPC端点。
- **原始JSON-RPC**：直接使用原生JSON格式进行交易发送，避免 `ethers.js` 的额外开销。
- **纳秒级计时**：使用 `process.hrtime.bigint()` 进行精确的时间测量。
- **可配置的批量处理规模**：允许用户调整并行签名操作的负载。