---
name: Arbitrum
description: 协助处理 Arbitrum One 交易、跨链桥接（bridging）、Gas 资源优化以及 L2（Layer 2）生态系统的导航相关事宜。
metadata: {"clawdbot":{"emoji":"🔵","os":["linux","darwin","win32"]}}
---

## 网络基础  
- Arbitrum One 是一种基于“乐观主义汇总（optimistic rollup）”技术的以太坊 Layer-2 扩容方案。  
- 其执行环境与 Ethereum 的 EVM（以太坊虚拟机）兼容：使用相同的工具、钱包和合约。  
- ETH 是用于支付交易费用的“gas”代币，而非 Arbitrum 的专用代币。  
- ARB 代币是用于治理的代币，不用于支付交易费用。  
- 虽然地址与 Ethereum 相同，但属于不同的网络，因此账户余额也不同。  

## 连接方案（Bridge）  
- 官方连接方案：bridge.arbitrum.io（安全性最高）。  
- 从 Ethereum 向 Arbitrum 存款：大约需要 10 分钟（等待 Ethereum 的确认）。  
- 从 Arbitrum 向 Ethereum 提现：需要等待 7 天（由于“乐观主义汇总”技术的安全机制）。  
- 第三方连接方案（如 Hop、Across、Stargate）虽然速度更快，但存在一定风险。  
- 使用第三方连接方案前，请确保先向 Arbitrum 存入一定数量的 ETH（作为交易费用）。  

## 7 天的提现限制  
- Arbitrum 的“乐观主义汇总”技术假定所有交易都是有效的；在 7 天内，系统会进行欺诈检测。  
- 无法加快通过官方连接方案的提现速度（这是安全要求）。  
- 如果您需要在 7 天内使用资金，请提前做好计划，避免使用第三方连接方案。  
- 第三方连接方案通常依赖外部流动性，因此会收取费用。  
- 提现需在 7 天后才能完成，且需要提供相应的 Ethereum 交易记录作为依据。  

## 交易费用（Gas）  
- Arbitrum 的交易费用远低于 Ethereum 主网，通常低 10 到 50 倍。  
- 交易费用包括两部分：Layer-2 的执行费用和 Layer-1 的数据同步费用。  
- 当 Ethereum 网络拥堵时，Layer-1 的数据同步费用可能会增加。  
- Arbitrum 的交易费用单位与 Ethereum 相同（gwei）。  
- Arbitrum 的区块生成速度较快，大约每 0.25 秒一个区块。  

## ARB 代币  
- ARB 代币用于参与去中心化自治组织（DAO）的治理决策。  
- 交易费用由 ETH 支付，而非 ARB 代币。  
- ARB 代币已向早期用户进行免费发放，目前领取期限已结束。  
- ARB 正在开发 staking（质押）功能。  
- ARB 代币可在主要交易所交易，流动性较高。  

## DeFi 生态系统  
- GMX 是 Arbitrum 上规模最大的去中心化交易所（DEX）。  
- Uniswap、SushiSwap 等也是重要的去中心化交易所。  
- Aave、Radiant 等平台提供借贷服务。  
- Camelot 是专为 Arbitrum 设计的去中心化交易所。  
- Arbitrum 上锁定的资产总价值达数十亿美元。  

## 钱包配置  
- MetaMask 可直接在 Arbitrum 上使用；请通过 chainlist.org 添加 Arbitrum 网络配置。  
- Chain ID：42161；RPC 地址：https://arb1.arbitrum.io/rpc  
- 可使用 arbiscan.io 查看区块信息以验证交易。  
- 钱包的种子短语与 Ethereum 相同，但网络选择需设置为 Arbitrum。  

## Arbitrum Nova  
- Arbitrum Nova 是一个独立的网络，专为游戏和社交应用优化。  
- 其交易费用低于 Arbitrum One，但安全性保障相对较低。  
- 使用不同的连接方案，请注意不要与 Arbitrum One 混淆。  
- Chain ID：42170；请确认自己连接的是正确的网络。  

## 开发工具  
- Arbitrum 支持 Rust、C、C++ 等语言编写的合约，而不仅仅是 Solidity。  
- 执行环境基于 WASM（WebAssembly），与 Ethereum 的 EVM 共享相同的执行引擎。  
- 新功能即将推出，将进一步丰富开发者的选择。  
- Arbitrum 合约的安全性同样得到保障（经过审计）。  

## 常见问题  
- “ETH 不足”：需要 ETH 来支付交易费用，而不仅仅是 ARB 代币。  
- 误选网络：将交易发送到错误的 Ethereum 地址（虽然可以恢复，但过程较为复杂）。  
- 提现延迟：7 天的等待时间属于正常现象，不属于交易失败。  
- 交易被撤销：请检查交易细节（如滑点、确认状态和账户余额）。  
- “网络未找到”：请在钱包中添加 Arbitrum 网络配置。  

## 交易排序机制（Sequencer）  
- 目前 Arbitrum 使用单一的交易排序机制，由 Offchain Labs 运营。  
- 存在中心化风险，但已有去中心化解决方案的规划中。  
- 交易排序机制无法盗取用户资金，仅负责交易顺序的安排。  
- 如果排序机制出现故障，交易会延迟处理但不会丢失，可手动重新提交。  
- 去中心化的交易排序机制正在开发中，将由 DAO（去中心化自治组织）管理。  

## 安全性  
- Arbitrum 的资产安全性与 Ethereum 相同；7 天的挑战期过后，资产将得到充分保护。  
- 智能合约同样存在安全风险，审计结果至关重要。  
- 欺诈检测机制可保护用户免受损失（无效的状态转换会被拒绝）。  
- Arbitrum 的安全依赖于 Ethereum 的基础设施；Layer-1 负责最终的结算。  
- 大额交易请使用官方连接方案，第三方连接方案存在额外风险。