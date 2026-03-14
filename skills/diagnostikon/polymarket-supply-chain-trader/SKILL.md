---
name: polymarket-supply-chain-trader
description: Polymarket的预测市场专注于供应链中断、港口拥堵、航运延误、商品价格以及物流结果等议题。当您希望捕捉全球贸易流动事件、原材料价格市场以及需求激增的预测机会时，可以使用这些预测市场。
metadata:
  author: Diagnostikon
  version: '1.0'
  displayName: Supply Chain & Logistics Trader
  difficulty: intermediate
---
# 供应链与物流交易策略

> **这是一个模板。**  
> 默认的信号生成方式是基于关键词的市场发现（涉及运输、港口、物流、商品、供应链等领域）——可以结合货运指数API（如波罗的海干货指数）、卫星AIS船舶跟踪数据或实时港口权威数据来进行优化。  
> 该策略负责处理所有的交易流程（包括市场发现、交易执行和风险控制），交易决策由用户自行做出。

## 战略概述

供应链预测市场在Polymarket平台上属于服务相对不足的领域之一。该策略专注于识别并交易以下相关市场：

- **港口拥堵**：如鹿特丹港、苏伊士运河的拥堵情况，以及洛杉矶/长滩港的货物延误  
- **商品价格**：布伦特原油、钢材、锂矿等商品的价格波动  
- **需求激增**：例如GPU/芯片短缺、电动汽车电池供应紧张的情况  
- **公司物流**：特斯拉的交货延迟、马士基公司的航运时间、亚马逊Prime服务的服务水平协议（SLA）  

研究表明，与传统方法相比，预测市场能够将供应链预测的误差降低20%至50%（数据来源：CFTC）。这使得这些市场既具有交易价值，也具有很高的信息参考价值。

## 信号生成逻辑

### 默认信号生成方式：关键词搜索 + 流动性筛选  
1. 在Polymarket平台上搜索包含“供应链”相关关键词的活跃市场  
2. 筛选成交量超过5,000美元且买卖价差小于10%的市场  
3. 应用概率均值回归算法：如果市场价格偏离30天移动平均值的幅度超过15%，则标记为异常信号  
4. 在入场前检查市场是否存在价格反转风险及可能的滑点  
5. 如果市场概率异常低（尽管基本面良好），则选择“否”；否则选择“是”

### 优化策略示例  
- **波罗的海干货指数信号**：当BDI指数周环比涨幅超过15%时，对相关运输延误市场进行买入操作  
- **美国农业部作物报告**：在报告发布前后交易农产品供应市场  
- **港口权威机构的RSS数据**：利用实时拥堵数据作为入场触发条件  
- **卫星AIS跟踪**：通过统计洛杉矶/长滩港的船舶排队数量来获取直接的市场信息  

## 监控的市场类别  
```python
SUPPLY_CHAIN_KEYWORDS = [
    "shipping", "port", "container", "supply chain", "logistics",
    "commodity", "crude oil", "steel price", "lithium", "semiconductor",
    "chip shortage", "delivery delay", "Maersk", "Rotterdam", "Suez",
    "GPU demand", "battery supply", "Amazon Prime"
]
```  

## 风险参数  

| 参数 | 默认值 | 说明 |
|---------|---------|-------|
| 单次最大持仓规模 | 25美元 | 每个市场 |
| 最小市场成交量 | 5,000美元 | 流动性筛选条件 |
| 最大买卖价差 | 10% | 用于控制滑点风险 |
| 最短市场波动周期 | 7天 | 避免受到最后一刻市场波动的影响 |
| 最大同时开仓数量 | 5个 | 限制交易集中度 |

## 安装与配置  

```bash
clawhub install polymarket-supply-chain-trader
```  

需要设置`SIMMER_API_KEY`环境变量。  

## 定时执行计划  

该策略每15分钟执行一次（`*/15 * * * *`）。由于市场波动较为缓慢，因此无需高频交易。  

## 安全性与执行模式  

该策略默认采用模拟交易模式（`venue="sim"`）。只有当明确指定`--live`参数时，才会执行真实交易。  

| 执行方式 | 模式 | 财务风险 |
|---------|------|----------------|
| `python trader.py` | 模拟交易 | 无财务风险 |
| 定时任务/自动化脚本 | 模拟交易 | 无财务风险 |
| `python trader.py --live` | 实时交易（Polymarket平台） | 使用真实美元进行交易 |

自动化脚本的定时任务默认设置为`null`——除非在Simmer用户界面中手动配置，否则不会自动运行。`autostart: false`表示安装后不会自动启动。  

## 所需凭证  

| 凭证 | 是否必需 | 说明 |
|---------|---------|-------|
| `SIMMER_API_KEY` | 是 | 交易授权凭证，请保密；切勿将可用于实时交易的密钥放置在可能被自动化脚本访问的环境中 |

## 可调参数（风险相关）  

所有风险参数均存储在`clawhub.json`文件中，并标记为“tunables”，用户可通过Simmer用户界面进行调整，无需修改代码。这些参数前缀为`SIMMER_`，以确保`apply_skill_config()`函数能够安全地加载配置信息。  

| 参数 | 默认值 | 作用 |
|---------|---------|---------|
| `SIMMER_supply_MAX_POSITION` | 25美元 | 每次交易的最大持仓金额 |
| `SIMMER_supply_MIN_VOLUME` | 5,000美元 | 最小市场成交量阈值 |
| `SIMMER_supply_MAX_SPREAD` | 0.10 | 最大买卖价差（0.10表示10%） |
| `SIMMER_supply_MIN_DAYS` | 7天 | 市场价格稳定所需的最短时间 |
| `SIMMER_supply_MAX_POSITIONS` | 5个 | 同时允许开仓的最大数量 |

## 依赖库  

`simmer-sdk`由Simmer Markets团队发布，可在PyPI上下载：  
- PyPI链接：https://pypi.org/project/simmer-sdk/  
- GitHub链接：https://github.com/SpartanLabsXyz/simmer-sdk  
- 发布者：hello@simmer.markets  

在提供实时交易凭证之前，请务必仔细审查相关代码，以确保系统的可审计性。