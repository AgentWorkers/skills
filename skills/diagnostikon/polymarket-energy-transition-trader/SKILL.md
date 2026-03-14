---
name: polymarket-energy-transition-trader
description: Polymarket的预测市场涵盖了电动汽车（EV）的普及里程碑、太阳能/风能发电容量、核能项目的重启情况、石油价格阈值以及能源政策相关事件。这些预测工具可用于利用国际能源署（IEA）的数据、公用事业公司的公开报告以及商品期货市场的信号，来捕捉能源转型过程中的投资机会（即“alpha收益”）。
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Energy Transition Trader
  difficulty: intermediate
---
# 能源转型交易者（Energy Transition Trader）

> **这是一个模板。**  
> 默认的交易策略基于关键词进行市场分析，并结合概率极值检测机制；您可以根据下方“Edge Thesis”中列出的数据源对这一策略进行进一步调整。  
> 该工具负责处理所有的交易流程（市场分析、交易执行及风险控制），而您的代理（agent）则负责提供具体的交易策略（alpha strategy）。

## 策略概述  
国际能源署（IEA）的月度数据与市场预期中的采用率之间存在差异；具体数据来源包括：IEA的每周石油报告、BloombergNEF的能源转型数据以及IRENA的产能统计信息。

## Edge Thesis  
能源市场既受到长期结构性趋势的影响，也受到政策变化的驱动：  
- **电动汽车（EV）的采用情况**：IEA每月发布电动汽车销售数据。然而，市场对电动汽车普及速度的预期往往滞后于IEA的预测（通常滞后1–2个月）。  
- **欧佩克（OPEC）的意外减产**：自2022年以来，欧佩克+组织的减产决策在石油市场中经常被低估；该组织70%以上的减产行动都出乎市场预期。  
- **核能重启市场**：欧洲的核能重启计划相关信息可通过监管文件获取，但美国零售投资者对欧洲的能源政策了解不足。  
- **太阳能发电能力**：IEA和IRENA每季度发布新增太阳能发电能力的数据；尽管有这些数据，市场对“到某年将安装多少吉瓦（GW）的太阳能发电设施”的预期往往偏低。

### 数据源建议  
- **国际能源署数据**：https://www.iea.org/data-and-statistics  
- **IEA每周石油报告**：https://www.eia.gov/petroleum/  
- **IRENA统计数据**：https://www.irena.org/Statistics  
- **OilPrice.com API**：布伦特原油（Brent）和西德克萨斯中质原油（WTI）的实时价格数据  

## 安全性与执行模式  
该工具默认采用模拟交易模式（`venue="sim"`）；只有在使用`--live`标志时才会进行真实交易（使用USDC作为交易货币）。  

| 模式 | 执行方式 | 金融风险 |
|---|---|---|
| `python trader.py` | 模拟交易 | 无金融风险 |
| Cron/自动化脚本 | 模拟交易 | 无金融风险 |
| `python trader.py --live` | 实时交易（多市场模式） | 使用真实USDC进行交易 |

注意：`autostart: false`和`cron: null`——除非在Simmer UI中配置，否则所有操作都不会自动执行。

## 所需凭证  
- **SIMMER_API_KEY**：必需凭证，用于访问交易相关服务。请将其视为高价值敏感信息。  

## 可调参数（风险控制参数）  
所有相关参数均可在`clawhub.json`文件中设置，并通过Simmer UI进行调整：  
| 参数 | 默认值 | 作用 |
|---|---|---|
| `SIMMER_MAX_POSITION` | 见clawhub.json | 每笔交易的最大USDC金额限制 |
| `SIMMER_MIN_VOLUME` | 见clawhub.json | 最小交易量限制 |
| `SIMMER_MAX_SPREAD` | 见clawhub.json | 最大买卖价差限制 |
| `SIMMER_MIN_DAYS` | 见clawhub.json | 最短结算周期（天数） |
| `SIMMER_MAX_POSITIONS` | 见clawhub.json | 同时持有的最大未平仓头寸数量 |

## 依赖库  
该工具依赖于Simmer Markets（SpartanLabsXyz）提供的`simmer-sdk`库：  
- PyPI链接：https://pypi.org/project/simmer-sdk/  
- GitHub仓库：https://github.com/SpartanLabsXyz/simmer-sdk