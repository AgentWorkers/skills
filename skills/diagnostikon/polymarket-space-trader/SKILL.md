---
name: polymarket-space-trader
description: Polymarket的预测市场涵盖了太空发射、SpaceX的重要里程碑、卫星部署、火星任务以及商业航天飞行的结果等主题。当你希望从这个快速增长（年复合增长率达22%）的太空探索市场中获取投资机会时，可以使用这些预测市场。这些市场的二元决策机制（即只有两种可能的结果：成功或失败）为投资者提供了明确的判断标准。
metadata:
  author: Diagnostikon
  version: '1.0'
  displayName: Space & Launch Trader
  difficulty: intermediate
---
# Space & Launch Trader

> **这是一个模板。**  
> 默认的交易信号是关键词检测与FAA/SpaceX发射计划的匹配结果；您可以根据需要将其与NASA的发射清单API、TLE（Two-Line Element）卫星跟踪数据或SpaceX/Blue Origin的社交媒体动态相结合。  
> 该技能负责处理所有的市场分析、交易执行和风险控制流程，您的代理将负责最终的决策。

## 战略概述

太空预测市场的累计交易量在2020至2025年间超过了1.2亿美元，年复合增长率达到了22%。Polymarket目前列出了106个活跃的太空市场。该技能主要交易的对象包括：  
- **SpaceX的重要里程碑**（如Starship的轨道测试、发射次数、Starlink卫星星座的规模）  
- **火星任务**（NASA或私营企业的任务公告及着陆事件）  
- **商业太空飞行**（Blue Origin、Virgin Galactic、Axiom Space的发射计划）  
- **卫星与电信领域**（轨道拥挤情况、直接面向用户的卫星发射服务）  
- **监管事件**（FAA的批准、国际发射计划的对比）  

**关键洞察**：在发射事件发生前后，市场波动率通常会急剧上升约25%，这为精明的交易者提供了短暂的交易机会。

## 交易信号逻辑

### 默认交易信号：发射计划偏差  
1. 在Polymarket上查找活跃的太空/发射市场  
2. 查询公共发射数据库（如Rocket Watch、Next Spaceflight）以获取即将发生的发射日期  
3. 比较预定的发射日期与当前市场价格  
4. 在发射确认之前，市场往往会对成功发射持悲观态度（零售投资者的谨慎心理）  
5. 在出现异常情况（例如Falcon 9发射失败、天气原因导致发射取消）后，市场可能会过度反应；此时需要及时平仓或调整策略  

### 可扩展的交易信号来源：  
- **Twitter/X平台的情绪分析**：SpaceX的推文活动与交易量峰值有30%的相关性，可作为交易动量信号  
- **FAA的NOTAM文件**：这些公开文件会提前提示即将发生的发射事件  
- **卫星跟踪API**：通过实时轨道数据验证Starlink卫星的实际数量与市场数据是否一致  
- **NASA的API**：https://api.nasa.gov/ 提供实时的任务状态更新  

## 跟踪的市场类别  
```python
SPACE_KEYWORDS = [
    "SpaceX", "Starship", "Starlink", "launch", "rocket",
    "Mars", "NASA", "Blue Origin", "Virgin Galactic", "Axiom",
    "satellite", "orbital", "ISS", "FAA", "Falcon",
    "space station", "lunar", "Artemis", "ESA"
]
```  

## 风险参数  

| 参数 | 默认值 | 备注 |  
|-----------|---------|-------|  
| 单次最大持仓金额 | 30美元 | 太空市场的流动性较好  
| 最低市场交易量 | 2,500美元 | 太空领域的相关投资者较多  
| 最大买卖价差 | 8% | 相比气候市场，太空市场的价差更小  
| 最短等待期 | 3天 | 短期内的发射事件适合交易  
| 最多同时持有的未平仓头寸 | 6个 | 太空事件通常集中在特定的发射窗口期内发生  

## 波动性提示  

太空市场在出现异常消息时波动剧烈。如果发射被取消，价格不会立即飙升。该技能会通过特定的警告机制检测到这种情况，并在高波动期间暂停交易，除非有明确的交易机会。  

## 安装与配置  

```bash
clawhub install polymarket-space-trader
```  

**所需环境变量：** `SIMMER_API_KEY`  

**Cron调度**  
该技能每10分钟执行一次（`*/10 * * * *`）。由于发射事件的不确定性，其执行频率高于其他市场类别。  

## 安全性与交易模式  

**该技能默认采用模拟交易模式（`venue="sim"`）。只有当明确使用`--live`参数时，才会执行真实交易。**  
| 模式 | 交易方式 | 财务风险 |  
|---------|---------|----------------|  
| `python trader.py` | 模拟交易 | 无财务风险 |  
| Cron任务 | 模拟交易 | 无财务风险 |  
| `python trader.py --live` | 实际交易（Polymarket平台） | 使用真实资金 |  

**自动执行设置**：  
Cron任务默认不自动运行，需在Simmer UI中进行配置。`autostart: false`表示安装后不会自动启动。  

## 所需凭证  

| 参数 | 必需性 | 备注 |  
|---------|---------|-------|  
| `SIMMER_API_KEY` | 是 | 用于访问交易API的凭证，需保密；切勿将可执行交易的凭证放置在可能被自动化脚本访问的环境中 |  

## 可调整的风险参数  

所有风险参数都存储在`clawhub.json`文件中，并可通过Simmer UI进行修改，无需修改代码。这些参数前缀为`SIMMER_`，以确保安全加载：  
| 参数 | 默认值 | 作用 |  
|---------|---------|---------|  
| `SIMMER_SPACE_MAX_POSITION` | 30美元 | 每次交易的最大持仓金额 |  
| `SIMMER_SPACE_MIN_VOLUME` | 2,500美元 | 最低市场交易量阈值 |  
| `SIMMER_SPACE_MAX_SPREAD` | 0.08% | 最大买卖价差 |  
| `SIMMER_SPACE_MIN_DAYS` | 3天 | 最短等待期 |  
| `SIMMER_SPACE_MAX_POSITIONS` | 6个 | 同时持有的最大未平仓头寸数 |  

## 依赖库**  
`simmer-sdk`由Simmer Markets团队发布，可在PyPI上获取：  
- PyPI链接：https://pypi.org/project/simmer-sdk/  
- GitHub仓库：https://github.com/SpartanLabsXyz/simmer-sdk  
- 发布者：hello@simmer.markets  

**注意事项**：  
在提供真实交易凭证之前，请务必仔细审查源代码，以确保系统的可审计性。