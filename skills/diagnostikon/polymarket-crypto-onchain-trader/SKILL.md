---
name: polymarket-crypto-onchain-trader
description: 在 Polymarket 预测市场中，通过比特币（Bitcoin）、以太坊（Ethereum）和索拉纳（Solana）的价格里程碑、ETF 流入量、减半事件（halving events）以及去中心化金融（DeFi）协议的里程碑等数据来进行交易决策。这些数据主要基于链上（on-chain）信息获取。当你希望结合 Polymarket 提供的概率分析与实时的区块链指标来获取投资机会（即“捕获阿尔法收益”alpha returns）时，可以使用这种方法。
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Crypto & On-Chain Trader
  difficulty: advanced
---
# 加密货币与链上交易策略

> **这是一个模板。**  
> 默认的交易信号基于关键词的市场检测机制，结合了概率极值检测技术——您可以根据下方“Edge Thesis”中列出的数据源对其进行调整。该策略负责处理所有的交易流程（市场检测、交易执行及风险控制），而您的代理程序则负责生成具体的交易指令（即“alpha”信号）。

## 策略概述  
链上数据通常会提前2至12小时预示价格走势。可使用的数据源包括：Glassnode的免费服务（SOPR、NUPL、交易所流量数据）、CoinGlass的ETF流量追踪工具、Dune Analytics的仪表盘以及Arkham Intelligence的钱包追踪功能。

## Edge Thesis（策略依据）  
加密货币市场拥有所有资产类别中最完善的链上数据基础设施——然而，Polymarket平台的散户用户却很少利用这些数据：  
- **交易所资金流动**：大量BTC从交易所流出通常预示着价格上涨；大量资金流入则可能预示着抛售压力。Glassnode提供24小时延迟的数据，且完全免费。  
- **ETF流量数据**：BlackRock/Fidelity发行的BTC ETF的每日流入量数据由CoinGlass提前发布，这些数据会在Polymarket重新调整价格阈值之前被公开。  
- **恐惧与贪婪指数**：历史数据显示，当恐惧指数（<20）或贪婪指数（>80）达到极端值时，市场往往存在系统性定价错误。  
- **融资利率**：Binance和Bybit平台上的永续合约融资利率可以反映市场的过度杠杆化情况；当融资利率为正值且数值极高时，市场可能面临多头挤压风险，此时应考虑减少持仓或平仓。

### 可用的数据源  
- **Glassnode**: https://glassnode.com/（免费服务）  
- **CoinGlass ETF流量**: https://www.coinglass.com/bitcoin-etf  
- **Alternative.me恐惧与贪婪指数**: https://api.alternative.me/fng/  
- **Dune Analytics**: https://dune.com/（支持自定义链上数据查询）

## 安全性与交易模式  
该策略默认采用模拟交易模式（`venue="sim"`）；只有在使用`--live`标志时才会进行真实交易（使用Polymarket平台）。  

| 模式 | 交易类型 | 财务风险 |
|---|---|---|
| `python trader.py` | 模拟交易 | 无风险 |
| 定时任务/自动化脚本 | 模拟交易 | 无风险 |
| `python trader.py --live` | 实时交易（Polymarket平台） | 使用真实USDC进行交易 |

注意：`autostart: false`和`cron: null`——除非在Simmer UI中配置，否则所有交易都不会自动执行。

## 所需凭证  
- `SIMMER_API_KEY`：必需凭证，用于访问交易相关API；请将其视为高价值敏感信息。  

## 可调整参数（风险控制相关）  
所有相关参数均在`clawhub.json`文件中标记为“tunables”，可通过Simmer UI进行修改：  
| 参数 | 默认值 | 作用 |
|---|---|---|
| `SIMMER_MAX_POSITION` | 见clawhub.json | 每笔交易的最大USDC持仓量 |
| `SIMMER_MIN_VOLUME` | 见clawhub.json | 最小市场成交量阈值 |
| `SIMMER_MAX_SPREAD` | 见clawhub.json | 最大买卖价差 |
| `SIMMER_MIN_days` | 见clawhub.json | 最短等待天数（用于确认交易信号） |
| `SIMMER_MAX_POSITIONS` | 见clawhub.json | 同时持有的最大未平仓头寸数量 |

## 所需依赖库/工具  
- `simmer-sdk`：由Simmer Markets（SpartanLabsXyz开发）提供  
  - PyPI链接：https://pypi.org/project/simmer-sdk/  
  - GitHub仓库：https://github.com/SpartanLabsXyz/simmer-sdk