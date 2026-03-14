---
name: polymarket-biotech-trader
description: Polymarket的预测市场允许用户进行交易，涉及FDA药物审批、生物技术公司的IPO（首次公开募股）、临床试验结果、制药行业的并购以及精准医疗领域的重大进展等主题。当您希望利用PDUFA（药品注册申请）的截止日期、临床试验注册信息以及FDA的官方日程安排来捕捉这些高影响力事件带来的投资机会时，可以使用这些预测市场。
metadata:
  author: Diagnostikon
  version: '1.0'
  displayName: Biotech & FDA Trader
  difficulty: advanced
---
# 生物科技与FDA交易策略

> **这是一个模板。**  
> 默认的交易信号是关键词发现与FDA PDUFA（药品审批决定）日程的匹配；您可以根据需要将其与ClinicalTrials.gov API结合使用，以获取试验状态信息，或利用BioMedTracker数据库分析特定治疗领域的历史批准率，以及生物科技公司的财报电话会议情绪数据。  
> 该策略负责处理所有的市场发现、交易执行和风险控制环节；您的代理将提供具体的交易建议。

## 战略概述

全球生物科技市场的规模在2025年约为1.77万亿美元，并预计到2035年增长至6.34万亿美元（年复合增长率13.6%）。生物科技领域的预测市场具有较高的信息密度：FDA的审批决定具有明确的时间节点（PDUFA），且相关数据已被广泛研究。该策略主要关注以下交易机会：

- **FDA审批**：突破性疗法的认定、CRISPR技术在肿瘤学领域的应用、下一代GLP-1药物的审批。
- **临床试验**：第三阶段的试验结果、试验招募的重要里程碑。
- **生物科技公司的IPO**：2026年的IPO公告及其后续市场表现。
- **制药行业的并购**：肿瘤学领域的大额收购交易、人工智能驱动的药物发现项目。
- **精准医疗**：CAR-T疗法、mRNA疫苗、液体活检技术的进展。

关键洞察：FDA针对不同治疗领域的批准率有详细记录。当Polymarket上的价格与历史基准率出现显著偏离时，就存在交易机会。

## 交易信号逻辑

### 默认信号：PDUFA日期日程 + 历史基准率分析

1. 在Polymarket上查找活跃的生物科技/FDA相关市场。
2. 将这些市场与FDA的PDUFA日程进行匹配（数据公开，每月更新）。
3. 查阅特定药物类别/治疗领域的历史批准率。
4. 将历史基准率（例如，肿瘤学领域的突破性疗法批准率约为85%）与市场价格进行比较。
5. 如果市场价格低于高基准率的70%，则买入（判断为“YES”）。
6. 在重大事件发生前，通过上下文分析避免过度交易某些市场。

### 可扩展的策略思路

- **ClinicalTrials.gov API**：监控试验状态的变化（如从招募阶段到完成阶段）作为重要指标。
- **BioMedTracker / Citeline**：按治疗领域划分的历史批准率数据库。
- **FDA新闻稿**：实时监控FDA的审批或拒绝决定。
- **生物科技公司的Twitter账号**：在PDUFA日期前分析关键意见领袖（KOL）的舆论倾向。
- **空头持仓数据**：在PDUFA日期前，如果某只生物科技公司的空头持仓较高，说明市场预期其申请会被拒绝——据此进行交易决策。

## 监控的市场类别

```python
BIOTECH_KEYWORDS = [
    "FDA", "approval", "CRISPR", "cancer", "oncology", "clinical trial",
    "phase 3", "drug", "therapy", "vaccine", "mRNA", "CAR-T",
    "Alzheimer", "GLP-1", "biotech", "pharma", "M&A",
    "IPO", "diagnostic", "liquid biopsy", "gene editing",
    "sickle cell", "precision medicine", "antibody"
]
```

## 风险参数

| 参数 | 默认值 | 备注 |
|-----------|---------|-------|
| 单次最大持仓规模 | 35美元 | 二元事件需要谨慎控制持仓规模 |
| 最小市场成交量 | 5,000美元 | FDA相关市场通常吸引经验丰富的交易者 |
| 最大买卖价差 | 10% | 稀有疾病相关市场可能允许更大的价差 |
| 最短等待期 | 7天 | 在PDUFA日期前不要入场 |
| 最大同时持有多头头寸数量 | 6个 | 生物科技领域的交易事件往往相互关联 |

## FDA审批基准率（参考数据）

| 治疗领域 | 历史批准率 |
|-----------|--------------------------|
| 肿瘤学（突破性疗法） | 约85% |
| 稀有疾病（孤儿药） | 约70% |
| 中枢神经系统/神经学 | 约55% |
| 一般性药物（第三阶段成功） | 约65% |
| CRISPR/基因疗法（新型技术） | 约45% |

## 主要数据来源

- **FDA PDUFA日程**：https://www.fda.gov/patients/drug-development-process/step-4-fda-drug-review
- **ClinicalTrials.gov API**：https://clinicaltrials.gov/api/
- **SEC EDGAR**（生物科技公司的S-1招股说明书）：https://efts.sec.gov/LATEST/search-index?q=%22biotech%22&dateRange=custom

## 安装与配置

```bash
clawhub install polymarket-biotech-trader
```

需要设置`SIMMER_API_KEY`环境变量。

## 定时任务调度

每20分钟执行一次（`*/20 * * * *`）。FDA的审批决定虽然不频繁，但影响重大；因此适度的数据更新频率即可。

## 安全性与交易模式

**该策略默认采用模拟交易模式（`venue="sim"`）。只有当明确指定`--live`参数时，才会执行真实交易。**

| 模式 | 交易方式 | 财务风险 |
|----------|------|----------------|
| `python trader.py` | 模拟交易 | 无实际财务风险 |
| 定时任务 | 模拟交易 | 无实际财务风险 |
| `python trader.py --live` | 实时交易（Polymarket平台） | 使用真实美元进行交易 |

自动执行任务的定时任务默认设置为`null`——您需要在Simmer用户界面中手动配置它。`autostart: false`表示该任务在安装后不会自动启动。

## 所需凭证

| 参数 | 是否必需 | 备注 |
|----------|----------|-------|
| `SIMMER_API_KEY` | 是 | 用于交易授权的凭证，请保密。切勿将具有实时交易功能的凭证放置在可能被自动化代码访问的环境中。 |

## 可调整参数（风险相关）

所有风险参数都在`clawhub.json`文件中标记为`tunables`，可通过Simmer用户界面进行调整，无需修改代码。这些参数前缀为`SIMMER_`，以便`apply_skill_config()`函数能够安全地加载它们。

| 参数 | 默认值 | 作用 |
|----------|---------|---------|
| `SIMMER_BIOTECH_MAX_POSITION` | 35美元 | 每次交易的最大持仓金额 |
| `SIMMER_BIOTECH_MIN_VOLUME` | 5,000美元 | 最小市场成交量要求 |
| `SIMMER_BIOTECH_MAX_SPREAD` | 0.10 | 最大买卖价差（0.10表示10%） |
| `SIMMER_BIOTECH_MIN_DAYS` | 7天 | 最短等待期 |
| `SIMMER_BIOTECH_MAX_POSITIONS` | 6 | 同时持有的最大多头头寸数量 |

## 依赖库

`simmer-sdk`由Simmer Markets公司在PyPI上发布：
- PyPI链接：https://pypi.org/project/simmer-sdk/
- GitHub链接：https://github.com/SpartanLabsXyz/simmer-sdk
- 发布者：hello@simmer.markets

在提供实时交易凭证之前，请务必仔细审查相关代码，以确保系统的可审计性。