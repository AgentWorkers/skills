---
name: Avalanche
description: 协助处理Avalanche C-Chain交易、AVAX币的转移、子网（subnets）以及跨链桥（cross-chain bridges）的相关操作。
metadata: {"clawdbot":{"emoji":"🔺","os":["linux","darwin","win32"]}}
---

## 网络架构（关键信息）  
- Avalanche 拥有三条链：X-Chain、P-Chain 和 C-Chain，每条链都有不同的用途：  
  - **C-Chain** 兼容 EVM（以太坊虚拟机），大多数去中心化金融（DeFi）应用和代币都运行在 C-Chain 上，交易费用使用 AVAX；  
  - **X-Chain** 用于快速转账，支持原生 AVAX 转账，但不兼容 EVM；  
  - **P-Chain** 用于质押（staking）和子网（subnet）管理。  

## C-Chain（最常用的链）  
- **兼容性**：C-Chain 兼容 EVM，可以使用 MetaMask 等工具；  
- **交易费用**：所有交易都需要支付 AVAX；  
- **链 ID**：43114；  
- **区块浏览器**：snowtrace.io（用于交易验证）；  
- **主要应用和代币**：Trader Joe、Aave、GMX 等。  

## 跨链转账  
- 在不同链之间转移 AVAX 需要使用 Avalanche 钱包；  
- C-Chain 与 X-Chain 之间的转账通常只需几秒钟，但需要遵循特定的流程；  
- 转账分为“导出”（从某链导出 AVAX）和“导入”（导入到另一链）两个步骤；  
- 可以使用官方的 Core 钱包或 Avalanche 钱包进行跨链转账，这两种钱包都支持所有三条链；  
- MetaMask 仅能访问 C-Chain，无法直接在 C-Chain 与 X-Chain 或 P-Chain 之间转账。  

## 与其他网络的桥接  
- **官方桥接方案**：Avalanche 提供官方桥接服务（bridge.avax.network），可将 ETH 转换为 Avalanche 上的 WETH.e；  
- **其他桥接工具**：LayerZero、Stargate 等，但可能会收取额外费用；  
- **转账时间**：转账到 Ethereum 可能需要一段时间，具体取决于所使用的桥接服务。  

## 交易费用（Gas）  
- **费用模型**：遵循 EIP-1559 后的以太坊标准，包括基础费用和优先级费用；  
- **费用水平**：比以太坊便宜，但高于某些 Layer-2 网络（通常每笔交易 0.01–0.10 美元）；  
- **支付方式**：仅支持使用 AVAX 支付费用；  
- **交易确认速度**：交易几乎立即完成（不到 2 秒）；  
- **失败交易**：失败的交易需要重新支付费用。  

## 代币与去中心化金融（DeFi）  
- **AVAX** 是 Avalanche 的原生交易费用代币，也可以像 ETH 一样进行交易；  
- **WAVAX** 是被包装（wrapped）的 AVAX，某些 DeFi 协议需要使用 WAVAX；  
- **主要交易平台**：Trader Joe、Pangolin 等；  
- **借贷服务**：Aave、Benqi 等平台提供借贷功能；  
- **代币安全性**：请注意可能存在诈骗代币，请在 snowtrace.io 上验证代币的真实性。  

## 子网（Subnets）  
- **定义**：子网是 Avalanche 上的定制区块链，类似于特定应用的专用链；  
- **示例**：DFK Chain（DeFi Kingdoms）、Dexalot 等；  
- **费用机制**：每个子网可能有自己的代币作为交易费用，不一定是 AVAX；  
- **桥接方式**：需要通过官方桥接工具才能访问子网；  
- **安全性**：子网拥有独立的验证器（validators），安全性要求不同。  

## 质押（Staking）  
- **最低要求**：至少需要 25 AVAX 才能开始质押；  
- **质押期限**：至少需要质押 2 周；  
- **奖励**：奖励因验证器的表现而异；  
- **风险**：表现不佳的验证器获得的奖励较少；  
- **流动性**：部分质押方案支持“流动性质押”（如 sAVAX、ggAVAX），可在质押的同时保持资金流动性。  

## 钱包选择  
- **官方钱包**：Core 钱包（支持所有三条链和子网）；  
- **MetaMask**：仅支持 C-Chain，界面熟悉但功能有限；  
- **Ledger**：可通过 Core 或 MetaMask 进行管理；  
- **移动钱包**：Core 钱包提供移动应用版本。  

## 常见问题  
- **资金不足**：在 C-Chain 上进行交易需要足够的 AVAX；  
- **代币错误**：代币可能被错误地转移到了 X-Chain；  
- **代币找不到**：可能是代币位于错误的链上，或需要添加自定义代币；  
- **桥接延迟**：某些桥接服务可能需要 10–30 分钟，请耐心等待；  
- **子网代币显示问题**：可能需要在钱包中添加相应的子网设置。  

## 安全性**  
- **安全性保障**：C-Chain 采用与以太坊相同的 EVM 安全标准；  
- **私钥管理**：一个种子词（seed phrase）即可控制所有链；  
- **地址验证**：C-Chain 的地址以 “X-” 开头；  
- **风险控制**：未使用的权限可以随时撤销；  
- **官方桥接更安全**：第三方桥接可能存在安全风险。