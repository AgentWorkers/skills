---
name: polymarket-sports-live-trader
description: Polymarket的预测市场允许用户进行关于体育锦标赛、比赛结果、最有价值球员（MVP）奖项、转会窗口以及赛季重要节点的投注。当您希望利用联赛排名数据、伤病报告以及Elo评分等信号来从体育市场中获取投资机会时，可以使用这一工具。
metadata:
  author: Diagnostikon
  version: "1.0"
  displayName: Sports & Championships Trader
  difficulty: intermediate
---
# 体育与锦标赛交易系统

> **这是一个模板。**  
> 默认的交易策略基于关键词的市场发现机制，并结合了概率极值检测技术——您可以根据下方“Edge Thesis”中列出的数据源对该策略进行个性化调整。  
> 该系统负责处理所有的交易相关流程（包括市场发现、交易执行和风险控制），而您的代理（agent）则负责提供具体的交易决策（即“alpha”值）。

## 策略概述  

该策略通过分析Elo评分（或类似的游戏排名系统）与市场价格的差异来寻找交易机会。数据来源包括：SofaScore/FotMob API、Elo评分系统、Transfermarkt.com的数据以及ESPN API。

## Edge Thesis（策略核心理念）  

体育预测市场主要由热情的球迷主导，他们往往基于个人情感为支持的球队下注，这导致了市场定价上的系统性效率低下：  
- **球迷忠诚度偏见**：热门球队（如皇家马德里、利物浦、曼城、湖人队）的球迷往往会过度投注，从而造成市场价格的失真；  
- **伤病信息滞后**：官方球队网站通常会在比赛开始前24–48小时才更新伤病信息，而医疗人员往往在比赛临近时才能确认球员的参赛状态；  
- **Elo评分与市场价格的偏差**：当量化评分（如Elo评分）与Polymarket预测的概率偏差超过15%时，就存在交易机会；  
- **DAZN与Polymarket的合作**：由于直播内容的嵌入，高频的实时市场数据变得可获取，尤其是在进球或红牌发生时，市场波动会加剧。  

### 可用的数据源  

- **俱乐部Elo评分**：https://www.clubelo.com/API（免费提供）  
- **NBA球队的Elo评分**：https://projects.fivethirtyeight.com/nba-model/  
- **Transfermarkt API**：提供球员估值和伤病信息  
- **ESPN隐藏API**：`https://site.api.espn.com/apis/site/v2/sports/{sport}/{league}/scoreboard`  

## 风险控制与交易执行模式  

该系统默认采用模拟交易模式（`venue="sim"`）；只有在使用`--live`标志时才会进行真实交易。  

| 模式 | 交易类型 | 财务风险 |
|---|---|---|
| `python trader.py` | 模拟交易 | 无风险 |
| 定时任务（Cron） | 模拟交易 | 无风险 |
| `python trader.py --live` | 实时交易（Polymarket平台） | 使用真实货币（USDC） |

注意：`autostart: false`和`cron: null`的设置意味着在您通过Simmer UI进行配置之前，系统不会自动运行任何交易操作。

## 所需凭证  

| 凭证名称 | 是否必需 | 备注 |
|---|---|---|
| `SIMMER_API_KEY` | 是 | 用于访问交易API，属于高价值凭证。 |

## 可调整参数（风险控制相关）  

所有相关参数均可在`clawhub.json`文件中找到，并通过Simmer UI进行修改：  
| 参数名 | 默认值 | 作用 |
|---|---|---|
| `SIMMER_MAX_POSITION` | 见clawhub.json | 每笔交易的最大资金限额（USDC） |
| `SIMMER_MIN_VOLUME` | 见clawhub.json | 最小交易量限制 |
| `SIMMER_MAX_SPREAD` | 见clawhub.json | 最大买卖价差限制 |
| `SIMMER_MIN_days` | 见clawhub.json | 交易结算的最短等待天数 |
| `SIMMER_MAX_POSITIONS` | 见clawhub.json | 同时持有的最大未平仓头数 |

## 依赖库/工具  

该系统依赖于Simmer Markets（SpartanLabsXyz）提供的`simmer-sdk`：  
- PyPI链接：https://pypi.org/project/simmer-sdk/  
- GitHub仓库：https://github.com/SpartanLabsXyz/simmer-sdk