---
name: polymarket-climate-trader
description: Polymarket的预测市场允许用户对极端天气、气候变化、自然灾害以及农业产出等事件进行交易。当您希望利用气象数据信号来捕捉与温度记录、飓风季节、洪水事件或二氧化碳浓度阈值相关的投资机会时，可以使用这些预测市场。
metadata:
  author: Diagnostikon
  version: '1.0'
  displayName: Climate & Weather Trader
  difficulty: intermediate
---
# 气候与天气交易策略

> **这是一个模板。**  
> 默认的交易信号基于关键词检测以及NOAA天气API数据；你可以将其与ForecastEx的气候预测数据、卫星NDVI农业数据或集合天气模型输出相结合使用。  
> 该策略负责处理所有的交易流程（市场发现、交易执行和风险控制），而你的代理程序则负责提供具体的交易决策。

## 策略概述

气候预测市场是目前增长最快的、但服务仍不完善的领域之一。Polymarket平台上共有151个活跃的气候市场，但大多数都较为基础。本策略能够捕捉到以下方面的投资机会：

- **极端气候事件**：创纪录的高温、热浪、霜冻事件  
- **自然灾害**：飓风数量、地震震级、野火面积  
- **气候关键指标**：二氧化碳浓度阈值、北极海冰最小范围  
- **农业影响**：小麦产量、干旱导致的作物歉收、水资源分配  

气候市场非常适合量化交易：数据来源公开、可验证且结构化程度高（如NOAA、ECMWF、NASA提供的数据）。

## 交易信号逻辑

### 默认交易信号：模型预测结果的分歧

1. 在Polymarket平台上查找活跃的气候/天气市场  
2. 从开放的天气API（如NOAA、Open-Meteo）获取当前的天气预报数据  
3. 比较模型预测的概率与当前市场价格  
4. 如果模型预测结果与市场价格之间的差异超过12%，进一步分析市场情况（例如价格波动、市场趋势变化等）  
5. 根据气象模型的预测结果进行交易  

### 可扩展的交易策略建议：

- **使用ECMWF集合预测模型**：利用欧洲气象中心的15天天气预报作为交易信号  
- **ENSO指数**：通过NOAA的ONI指数进行厄尔尼诺/拉尼娜现象相关的交易  
- **保险相关证券**：利用保险链接证券（ILS）的价差作为概率基准  
- **Copernicus气候数据**：利用欧洲的实时气候服务为本地/区域市场提供交易依据  

## 监控的市场类别  

```python
CLIMATE_KEYWORDS = [
    "temperature", "hurricane", "tornado", "flood", "drought",
    "wildfire", "earthquake", "CO2", "sea ice", "Arctic",
    "El Niño", "La Niña", "snowfall", "rainfall", "heatwave",
    "crop yield", "wheat", "harvest", "water shortage"
]
```

## 风险参数

| 参数 | 默认值 | 说明 |
|---------|---------|-------|
| 单次最大持仓规模 | 20美元 | 每个市场 |
| 最低市场交易量 | 3,000美元 | 气候市场的流动性较低 |
| 最大买卖价差 | 12% | 小众市场允许更大的价差 |
| 最短数据更新周期 | 14天 | 天气数据需要足够的时间来反映市场变化 |
| 同时持有的最大未平仓头寸数 | 8个 | 通过分散投资降低风险 |

## 主要数据来源

- **NOAA气候数据在线**：https://www.ncdc.noaa.gov/cdo-web/  
- **Open-Meteo API**：https://open-meteo.com/（免费，无需注册）  
- **Copernicus C3S**：https://cds.climate.copernicus.eu/  
- **ForecastEx**：https://forecastex.com/  

## 安装与配置

```bash
clawhub install polymarket-climate-trader
```

需要设置`SIMMER_API_KEY`环境变量。可选：`OPENMETEO_API_KEY`。

## 定时任务安排

每30分钟执行一次（`*/30 * * * *`）。天气数据更新频率为1–6小时，无需更频繁地请求数据。

## 安全性与交易模式

**该策略默认为模拟交易模式（`venue="sim"`）。只有在明确指定`--live`参数时才会执行真实交易。**

| 模式 | 交易模式 | 财务风险 |
|---------|---------|----------------|
| `python trader.py` | 模拟交易 | 无财务风险 |
| 定时任务/自动化脚本 | 模拟交易 | 无财务风险 |
| `python trader.py --live` | 实时交易（Polymarket平台） | 使用真实美元进行交易 |

自动化脚本的定时任务默认设置为`null`——你需要在Simmer用户界面中手动配置才能使其运行。`autostart: false`表示安装后不会自动启动。

## 所需凭证

| 凭证 | 必需性 | 说明 |
|---------|---------|-------|
| `SIMMER_API_KEY` | 是 | 用于交易授权，请确保该凭证的安全性，避免将其放置在可能被自动化脚本使用的环境中 |

## 可调整的风险参数

所有风险参数都存储在`clawhub.json`文件中，并标记为`tunables`，可以通过Simmer用户界面进行修改，无需修改代码。这些参数前缀为`SIMMER_`，以便`apply_skill_config()`函数能够安全地加载它们。

| 参数 | 默认值 | 作用 |
|---------|---------|---------|
| `SIMMER_CLIMATE_MAX_POSITION` | 20美元 | 每次交易的最大持仓规模 |
| `SIMMER_CLIMATE_MIN_VOLUME` | 3,000美元 | 最低市场交易量阈值 |
| `SIMMER_CLIMATE_MAX_SPREAD` | 0.12 | 最大买卖价差（0.10表示10%） |
| `SIMMER_CLIMATE_MIN_DAYS` | 14天 | 数据更新的最短周期 |
| `SIMMER_CLIMATE_MAX_POSITIONS` | 8 | 同时持有的最大未平仓头寸数 |

## 依赖库

`simmer-sdk`由Simmer Markets发布，可在PyPI上下载：  
- PyPI：https://pypi.org/project/simmer-sdk/  
- GitHub：https://github.com/SpartanLabsXyz/simmer-sdk  
- 发布者：hello@simmer.markets  

在提供真实交易凭证之前，请仔细审查代码，以确保系统的可审计性。