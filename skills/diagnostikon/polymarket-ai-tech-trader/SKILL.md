---
name: polymarket-ai-tech-trader
description: Polymarket的预测市场基于AI模型的发布、科技公司的IPO（首次公开募股）、产品发布、GPU基础设施的重大进展以及AI相关的监管事件进行交易。当您希望利用2026年主导市场趋势——AI与技术——来获取投资机会时，可以使用这一策略。该策略结合了模型基准数据以及科技行业的新闻资讯作为决策依据。
metadata:
  author: Diagnostikon
  version: '1.0'
  displayName: AI & Tech Launch Trader
  difficulty: advanced
---
# AI与科技产品发布交易策略

> **这是一个模板。**  
> 默认的交易信号包括关键词检测以及LMSYS聊天机器人竞技场的排名监控——你可以将其与AI基准测试API（如MMLU、HumanEval）、科技新闻RSS源、SEC EDGAR文件（用于IPO信号）或GitHub的提交活动（作为模型发布的预警信号）相结合使用。  
> 该策略负责处理所有的市场发现、交易执行和风险控制环节；你的代理将负责执行具体的交易操作。

## 战略概述

2026年，AI市场是Polymarket平台上增长最快的领域。2025年上半年，AI投资贡献了美国GDP增长的90%以上。该策略主要关注以下交易机会：  
- **AI模型基准测试**：在特定日期，哪些公司在LMSYS排名中处于领先地位  
- **模型发布**：GPT-5、Claude 4、Gemini Ultra等模型的发布或性能表现  
- **科技IPO**：OpenAI、Databricks、Stripe等公司的IPO公告  
- **产品发布**：Apple Vision Pro 2、Tesla FSD等产品的发布  
- **AI法规**：欧盟的AI法案实施情况以及美国的联邦AI立法  
- **基础设施**：NVIDIA的数据中心收入、H100芯片的部署情况  

**关键洞察**：AI领域的新闻周期非常快，散户投资者往往根据新闻标题进行交易。拥有基准数据的知情投资者将拥有显著的优势。

## 交易信号逻辑

### 默认交易信号：基准测试结果与新闻事件的结合  
1. 在Polymarket平台上发现活跃的AI/科技相关市场  
2. 监控LMSYS聊天机器人竞技场的排名变化  
3. 关注Hugging Face Open LLM排行榜的更新  
4. 比较模型性能数据与市场预期的概率  
5. 当某个模型在基准测试中明显领先但市场价格尚未反映这一变化时，进入交易  
6. 对于IPO市场：监控SEC Form S-1 EDGAR文件作为重要参考指标  

### 可扩展的信号来源  
- **GitHub API**：监控知名AI模型相关项目的提交活动或新仓库的创建  
- **谷歌趋势（Google Trends）**：AI搜索词量的上升可作为市场趋势的信号  
- **HuggingFace API**：模型下载次数可作为模型采用情况的指标  
- **SEC EDGAR**：自动接收IPO市场的S-1文件提交通知  
- **NVIDIA财报电话会议记录**：了解公司的未来展望与市场预期的对比  

## 监控的市场类别  
```python
AI_TECH_KEYWORDS = [
    "AI", "GPT", "Claude", "Gemini", "OpenAI", "Anthropic", "Google",
    "model", "benchmark", "AGI", "ChatGPT", "LLM",
    "IPO", "valuation", "Stripe", "Databricks", "SpaceX IPO",
    "Apple", "Vision Pro", "Tesla FSD", "Optimus", "robot",
    "NVIDIA", "GPU", "H100", "datacenter", "quantum",
    "EU AI Act", "regulation", "congress"
]
```

## 风险参数  

| 参数 | 默认值 | 备注 |
|---------|---------|-------|
| 最大持仓规模 | 40美元 | 流动性较高的市场允许更大的持仓规模 |
| 最小市场成交量 | 10,000美元 | AI市场具有极高的流动性 |
| 最大买卖价差 | 6% | 热门市场的价差通常较小 |
| 最短市场反应时间 | 5天 | 新闻周期变化迅速 |
| 最大同时持仓数量 | 10个 | AI/科技领域涉及的市场范围较广 |

## 交易优势  
### 零售投资者的“新鲜度偏见”  
在重大AI新闻（如GPT-5发布）之后，散户投资者往往会过度关注最新信息，导致相关市场过度波动。此时应在其他平台上减少对该市场的交易。  
### 基准测试结果的滞后  
市场往往根据最新的模型排名进行定价。当新的基准测试结果在午夜左右发布时，市场需要1-4小时才能完全调整价格。通过密切监控可以捕捉到这一时机。  

## 安装与配置  
```bash
clawhub install polymarket-ai-tech-trader
```  
需要设置`SIMMER_API_KEY`环境变量。  

## 定时任务安排  
该策略每5分钟执行一次（`*/5 * * * *`）。由于AI新闻更新频繁，这是所有策略中监控周期最短的。  

## 安全性与交易模式  
**该策略默认为模拟交易（`venue="sim"`）。只有当明确指定`--live`参数时，才会执行真实交易。**  
| 模式 | 交易模式 | 财务风险 |
|--------|---------|----------------|
| `python trader.py` | 模拟交易 | 无风险 |
| 定时任务 | 模拟交易 | 无风险 |
| `python trader.py --live` | 实时交易（Polymarket） | 使用真实USDC进行交易 |

自动执行任务的定时任务默认设置为`null`——你需要通过Simmer UI进行配置才能使其自动运行。`autostart: false`表示安装后不会自动启动。  

## 所需凭证  
| 参数 | 是否必需 | 备注 |
|---------|---------|-------|
| `SIMMER_API_KEY` | 是 | 交易凭证，请保密，切勿将可用于实时交易的密钥放置在可能被自动脚本访问的环境中。 |

## 可调整参数（风险相关）  
所有风险参数都存储在`clawhub.json`文件中，并可通过Simmer UI进行修改，无需修改代码。这些参数前缀为`SIMMER_`，以确保`apply_skill_config()`函数能够安全地加载它们。  
| 参数 | 默认值 | 作用 |
|---------|---------|---------|
| `SIMMER_AITECH_MAX_POSITION` | 40美元 | 每笔交易的最大持仓规模 |
| `SIMMER_AITECH_MIN_VOLUME` | 10,000美元 | 最小市场成交量限制 |
| `SIMMER_AITECH_MAX_SPREAD` | 0.06% | 最大买卖价差（0.10%对应10%的价差） |
| `SIMMER_AITECH_MIN_DAYS` | 5天 | 市场价格调整的最短时间 |
| `SIMMER_AITECH_MAX_POSITIONS` | 10个 | 同时持有的最大持仓数量 |

## 依赖库  
`simmer-sdk`由Simmer Markets发布，可在PyPI上下载：  
- PyPI: https://pypi.org/project/simmer-sdk/  
- GitHub: https://github.com/SpartanLabsXyz/simmer-sdk  
- 发布者：hello@simmer.markets  

在提供实时交易凭证之前，请仔细审查源代码以确保系统的可审计性。