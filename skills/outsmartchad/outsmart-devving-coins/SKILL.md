---
name: outsmart-devving-coins
description: "在 Solana 的 LaunchPads 上发布代币。适用场景：当用户询问如何创建代币、开发新币种、发起代币发行活动（如 PumpFun、LaunchLab、Jupiter Studio 等）、设置代币的绑定曲线（bonding curve）或部署代币时。不适用场景：购买现有代币（请使用交易功能），以及在现有流动性池（LP pools）中进行代币 farming 操作。"
homepage: https://github.com/outsmartchad/outsmart-cli
metadata: { "openclaw": { "requires": { "bins": ["outsmart"], "env": ["PRIVATE_KEY", "MAINNET_ENDPOINT"] }, "install": [{ "id": "node", "kind": "node", "package": "outsmart", "bins": ["outsmart"], "label": "Install outsmart CLI (npm)" }] } }
---
# 开发代币（Developing Coins）

在合适的时机推出代币。尽早抓住市场趋势，创建代币，并在代币“毕业”后通过绑定曲线（bonding curve）费用和锁定份额（LP）来获取收益。

## 适用场景

- **推出表情包代币（memecoin）**  
- **为当前的市场趋势开发代币**  
- **在 PumpFun 平台上创建代币**  
- **如何在 Solana 上进行代币发行？**  

## 不适用场景

- **购买现有代币** — 使用去中心化交易所（dex-trading）  
- **将代币投入现有份额池（LP pools）** — 使用专门的份额 farming 工具  
- **在缺乏市场热度的时期推出代币**  

## 发行平台（Launchpads）

### PumpFun（最受欢迎）

- **默认选择**：拥有最广泛的受众群体和最高的关注度。  
- **费用**：约 0.02 SOL。  
- **代币“毕业”后会被转移到 PumpSwap 平台。**  

**所有代币的特点**：  
- 小数点后有 6 位；总供应量为 10 亿枚；  
- 禁用代币的铸造（mint）和冻结（freeze）功能。  

### Jupiter Studio

- **基于 Meteora DBC 架构构建**：  
- 使用 USDC 作为结算货币；  
- 具有防止代币被恶意抢购（anti-sniping）的功能；  
- 支持开发者对代币进行逐步释放（vesting）设置。  
- **代币“毕业”后会被转移到 DAMM v2 平台。**  
- **预设发行方案**：  
  - 表情包类代币（Meme）：价格区间 $16,000 至 $69,000；  
  - 独立类代币（Indie）：价格区间 $32,000 至 $240,000；  
  - 支持自定义发行方案。  

### Raydium LaunchLab

- **代币“毕业”后会被转移到 Raydium CPMM 平台**。  
- 虽然不太适合推出表情包类代币，但可为其他发行平台提供支持（如 american.fun）。  

### Meteora DBC

- **无需许可即可使用**：提供便捷的代币绑定曲线（bonding curve）功能；  
- Jupiter Studio 以及许多 AI 自动化发行平台都基于此平台进行操作。  
- **代币“毕业”后同样会被转移到 DAMM v2 平台。**  

## 选择哪个发行平台？

| 你的需求 | 适用平台 | 原因 |
|---------|---------|------|
| 最大关注度，快速推出表情包代币 | PumpFun | 最广泛的受众群体 |
| 使用 USDC 曲线，防止恶意抢购，支持逐步释放 | Jupiter Studio | 内置安全保护机制 |
| 需要自动化发行流程 | PumpFun | 通过单一 CLI 命令即可完成发行。 |

## 抓住市场趋势（Catching the Narrative）

创建代币只是一个交易过程，关键在于知道该推出什么代币以及何时推出：

- **CT/X 社区**：同一主题的账户数量超过 5 个时，说明市场趋势正在形成；  
- **Telegram 群组**：新代币信息通常会首先在这些群组中泄露；  
- **DexScreener 热门榜单**：可以查看当前哪些代币正在上涨；  
- **新闻事件**：速度至关重要，第一个使用正确 ticker 的代币往往能获得成功。  

**最佳时机是市场趋势形成的初期（第 1-2 阶段）**；到了第 3 阶段，就已经太晚了。  

## 代币“毕业”后的收益计算  

**从发行到代币完全锁定为份额（LP）的总成本**：约 0.25 SOL。  

## 成为优秀的开发者（Be a Good Dev）

- **不要立即抛售你的代币**：所有交易都会被 GMGN（Global Market Gateway Network）监控到；  
- **不要一次性锁定所有份额**：否则会影响代币价格；  
- **不要在发行时启用代币的铸造/冻结功能**：这会立即引起怀疑；  
- **不要通过备用钱包购买大部分代币**：GMGN 能检测到批量购买行为；  
- **不要在缺乏市场热度的时期推出代币**。