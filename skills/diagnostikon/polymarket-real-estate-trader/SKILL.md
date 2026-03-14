---
name: polymarket-real-estate-trader
description: Polymarket 的预测市场涵盖了房价、抵押贷款利率、美联储利率决策、房地产市场崩溃情景以及区域房地产市场的重要节点。当您希望利用美联储的会议纪要、Case-Shiller 数据和抵押贷款利率信号来捕捉宏观房地产市场的投资机会时，可以使用这些工具。
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Real Estate & Housing Trader
  difficulty: intermediate
---
# 房地产与住房交易策略

> **这是一个模板。**  
> 默认的交易信号基于关键词的市场发现机制，并结合了概率极值检测技术——您可以根据下方“Edge Thesis”中列出的数据源对其进行调整。  
> 该策略负责处理所有交易相关的流程（市场发现、交易执行、风险控制等），而交易决策则由您自己负责。

## 策略概述  

联邦基金期货（Fed Funds Futures）的价格走势与Polymarket的利率决策市场存在差异。可使用的参考数据源包括：  
- **CME FedWatch工具**  
- **Case-Shiller指数**  
- **Zillow Research API**  
- **FRED经济数据**  

## Edge Thesis（策略核心理念）  

房地产市场和联邦基金利率市场的价格变动主要受散户交易者的影响，这些交易者通常会跟随主流媒体的观点。而能够获取联邦基金期货数据的量化交易者则具有显著的优势：  
- **CME FedWatch vs Polymarket**：联邦基金期货的价格走势往往与Polymarket的利率决策市场存在5%至15%的差异，因为期货市场的数据更为准确。  
- **Case-Shiller指数的发布延迟**：该指数每月发布一次，存在2个月的滞后，这可能导致市场低估实际的价格走势。  
- **地区性差异**：当某些地区的房地产市场（如凤凰城、奥斯汀、迈阿密）已经出现明显变化时，全国性的房地产市场预测可能会失准。  
- **商业房地产市场**：办公室空置率受远程办公（WFH）讨论的影响较大，而CBRE/JLL等机构提供的实际空置率数据能提供更可靠的信息。  

### 可用的数据源及信号生成方法  
- **CME FedWatch**: https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html  
- **FRED API**: https://fred.stlouisfed.org/docs/api/fred/  
- **Zillow Research**: https://www.zillow.com/research/data/  
- **Redfin Data Center**: https://www.redfin.com/news/data-center/  

## 风险控制与交易执行模式  

该策略默认采用模拟交易模式（`venue="sim"`）；只有在使用`--live`标志时才会进行真实交易（使用USDC作为交易货币）。  

| 模式 | 交易类型 | 风险等级 |
|---|---|---|
| `python trader.py` | 模拟交易 | 无风险 |
| 定时任务/自动化脚本 | 模拟交易 | 无风险 |
| `python trader.py --live` | 实时交易（使用Polymarket数据） | 使用真实货币（USDC） |

注意：`autostart: false`和`cron: null`——除非在Simmer UI中配置，否则系统不会自动运行任何交易任务。  

## 所需凭证  

| 凭证名称 | 是否必需 | 备注 |
|---|---|---|
| `SIMMER_API_KEY` | 是 | 用于交易授权，属于高价值凭证。 |

## 可调整参数（风险控制相关）  

所有相关参数均在`clawhub.json`文件中定义为“tunables”，可通过Simmer UI进行修改：  
| 参数名称 | 默认值 | 作用 |
|---|---|---|
| `SIMMER_MAX_POSITION` | 见clawhub.json | 每笔交易的最大持仓量（USDC） |
| `SIMMER_MIN_VOLUME` | 见clawhub.json | 最小交易量阈值 |
| `SIMMER_MAX_SPREAD` | 见clawhub.json | 最大买卖价差 |
| `SIMMER_MIN_days` | 见clawhub.json | 最短等待期（交易完成前需等待的天数） |
| `SIMMER_MAX_POSITIONS` | 见clawhub.json | 同时持有的最大未平仓合约数量 |

## 所需依赖库/工具  

该策略依赖于`simmer-sdk`（由SpartanLabsXyz开发）：  
- PyPI链接：https://pypi.org/project/simmer-sdk/  
- GitHub仓库：https://github.com/SpartanLabsXyz/simmer-sdk