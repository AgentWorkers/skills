---
name: polymarket-food-agriculture-trader
description: Polymarket的预测市场允许用户交易与食品商品价格、农作物产量、干旱导致的供应冲击、替代蛋白质技术的发展里程碑以及农业政策事件相关的合约。当您希望利用美国农业部（USDA）的农作物报告、期货价格曲线以及天气与农业之间的相关性信号来获取食品市场的投资机会时，可以使用这些工具。
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Food & Agriculture Trader
  difficulty: intermediate
---
# 食品与农业交易策略

> **这是一个模板。**  
> 默认的交易策略基于关键词进行市场发现，并结合概率极端值检测机制——您可以根据下方“Edge Thesis”中列出的数据源对这一策略进行定制。  
> 该策略负责处理所有的市场发现、交易执行及风险控制等环节；具体的交易决策由您的代理（agent）来做出。

## 策略概述  
该策略主要关注美国农业部（USDA）的WASDE报告与期货价格曲线之间的差异，并结合其他数据源进行综合分析：  
- **USDA NASS作物生长进度报告**  
- **联合国粮食及农业组织（FAO）食品价格指数**  
- **芝加哥商品交易所（CME）的农产品期货价格结构**  
- **世界银行的商品价格数据**  

## Edge Thesis（策略核心理念）  
农业市场的走势受实际数据（如USDA报告、卫星作物监测数据）的影响，但交易行为往往受到散户投资者的情绪和新闻报道的驱动：  
- **USDA WASDE报告**：WASDE报告每月在固定日期发布，市场在报告发布前常常对作物产量预期产生误判，而此时卫星数据早已预示了市场走势。  
- **咖啡/可可供应集中度**：70%的可可产量来自科特迪瓦和加纳，西非地区的任何天气事件都会对可可价格产生重大影响；散户投资者往往低估了供应冲击的可能性。  
- **厄尔尼诺现象对农业的影响**：NOAA的ENSO预测能够提前3–6个月预警主要农作物种植区的天气状况，但市场很少能准确反映这些信息。  
- **替代蛋白产品的监管政策**：实验室培育肉类的审批流程信息可通过FDA/USDA的官方文件获取，市场常常根据这些监管信息错误地判断价格走势。  

### 数据源与信号生成建议  
- **USDA NASS**：[https://www.nass.usda.gov/Data_and_Statistics/](https://www.nass.usda.gov/Data_and_Statistics/) – 提供免费的作物生长进度数据API  
- **FAO食品价格指数**：[https://www.fao.org/worldfoodsituation/foodpricesindex/](https://www.fao.org/worldfoodsituation/foodpricesindex/)  
- **世界银行商品价格数据**：[https://www.worldbank.org/en/research/commodity-markets](https://www.worldbank.org/en/research/commodity-markets)  
- **Planet Labs作物监测**：提供主要农作物种植区的卫星NDVI数据（需付费，但数据质量较高）  

## 安全性与交易执行模式  
该策略默认采用模拟交易模式（`venue="sim"`）；只有在使用`--live`标志时才会进行真实交易（使用USDC作为交易货币）。  

| 模式 | 交易方式 | 风险等级 |
|---|---|---|
| `python trader.py` | 模拟交易 | 无风险 |
| 定时任务/自动化脚本 | 模拟交易 | 无风险 |
| `python trader.py --live` | 实时交易（多市场模式） | 使用真实USDC进行交易 |

注意：`autostart: false`和`cron: null`——除非在Simmer UI中进行配置，否则所有任务都不会自动执行。  

## 所需凭证  
- **SIMMER_API_KEY**：必需凭证，用于访问交易相关API；请妥善保管。  

## 可调参数（风险控制相关）  
所有相关参数均可在`clawhub.json`文件中设置，并通过Simmer UI进行调整：  
| 参数 | 默认值 | 作用 |
|---|---|---|
| `SIMMER_MAX_POSITION` | 见clawhub.json | 每次交易的最大USDC持仓量 |
| `SIMMER_MIN_VOLUME` | 见clawhub.json | 最小市场交易量限制 |
| `SIMMER_MAX_SPREAD` | 见clawhub.json | 最大买卖价差限制 |
| `SIMMER_MIN_days` | 见clawhub.json | 最短等待决策的天数 |
| `SIMMER_MAX_POSITIONS` | 见clawhub.json | 同时持有的最大开仓数量 |

## 依赖库/工具  
该策略依赖于Simmer Markets（SpartanLabsXyz）提供的`simmer-sdk`：  
- PyPI仓库：[https://pypi.org/project/simmer-sdk/](https://pypi.org/project/simmer-sdk/)  
- GitHub仓库：[https://github.com/SpartanLabsXyz/simmer-sdk](https://github.com/SpartanLabsXyz/simmer-sdk)