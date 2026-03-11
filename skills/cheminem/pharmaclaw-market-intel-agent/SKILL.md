---
name: pharmaclaw-market-intel-agent
description: >
  从 openFDA API 获取并分析 FDA 不良事件报告系统（FAERS）的数据。  
  支持输入药物名称或 SMILES（通过 PubChem 进行解析）。  
  生成以下输出：  
  - 事件列表  
  - 年度趋势统计（事件数量）  
  - 最常见的反应/结果（以 JSON 格式呈现）  
  - 以及相应的 matplotlib 条形图（以 PNG 格式保存）。
triggers: ['faers', 'adverse event', 'safety report', 'drug side effect', 'post-market surveillance', 'reaction trend', 'clinical trial', 'clinicaltrials', 'trial pipeline', 'recruiting trial']
---
# 制药市场情报代理 - FAERS查询功能

## 概述
该功能用于查询药物的真实世界上市后安全数据，有助于获取药物的安全性概况、潜在风险及竞争对手分析等市场情报。

**主要输出结果：**
- JSON格式的汇总数据（包含数据趋势及最常见的不良反应/结果）
- PNG格式的条形图（年度报告，显示最常见的10种不良反应/结果）
- 最近发生的事件示例

**请求速率限制**：openFDA接口的请求速率为约240次/分钟。数据更新较快，但无法获取全部详细信息。

## 化学结构查询
用户输入的查询语句会被解析并传递给该模型，以实现标准化的处理流程：

```python
from dataclasses import dataclass
from typing import List, Optional

@dataclass
class ChemistryQuery:
    drug: str  # Drug name or SMILES
    query_type: str = 'faers'  # 'faers', 'pubchem', etc.
    metrics: Optional[List[str]] = None  # ['yearly_trends', 'top_reactions', 'top_outcomes', 'events']
    limit_events: int = 20
```

**示例：**
```json
{
  \"drug\": \"aspirin\",  // or \"CC(=O)OC1=CC=CC=C1C(=O)O\"
  \"query_type\": \"faers\",
  \"metrics\": [\"yearly_trends\", \"top_reactions\"]
}
```

## 快速入门/工作流程

### 1. 基本查询（所有指标）
```
exec skills/pharma-market-intel-agent/scripts/query_faers.py --drug aspirin --output ./aspirin_faers
```
- 生成文件：`aspirin_faers/aspirin_summary.json`
- 生成PNG格式的图表
- 提供最近发生的事件信息（以JSON格式）

### 2. 使用SMILES格式输入
```
exec ... --drug \"CC(=O)OC1=CC=CC=C1C(=O)O\"  # Aspirin SMILES
```
系统会通过PubChem自动将SMILES格式的输入转换为对应的药物名称。

### 3. 自定义请求限制
```
exec ... --drug ozempic --limit-events 50 --output ozempic_analysis
```

## 查询流程示例：
- **结合化学结构查询**：先解析/验证SMILES格式的输入，再查询FAERS数据。
- **pharma-tox-agent**：根据查询结果预测药物的安全性风险。
- **pharma-ip-expansion-agent**：检查目标药物的安全性信息。
- **traction-agent**：根据FAERS数据对药物的市场风险进行评估。

```
# Agent workflow:
1. Parse ChemistryQuery
2. Resolve SMILES if needed (pubchempy or query_faers handles)
3. Run query_faers.py
4. Read PNGs/JSONs into response
5. Chain if metrics require
```

---

## 与ClinicalTrials.gov的集成
该功能支持通过ClinicalTrials.gov API v2查询临床试验数据，支持按药物名称、疾病类型、试验阶段和试验状态进行搜索。无需API密钥。

### 快速入门
```bash
# Search by drug
exec skills/pharma-market-intel-agent/scripts/query_trials.py --drug "sotorasib" --output ./sotorasib_trials

# Search by condition + filters
exec ... --condition "breast cancer" --phase PHASE3 --status RECRUITING --limit 10 --output ./bc_trials

# Search by both
exec ... --drug "pembrolizumab" --condition "NSCLC" --output ./pembro_trials

# SMILES input (auto-resolves via PubChem)
exec ... --drug "CC(=O)OC1=CC=CC=C1C(=O)O" --output ./aspirin_trials
```

**输出结果：**
- `{drug}_trials_summary.json`：包含试验列表和汇总统计信息的完整结构化文件
- `{drug}_trials_by_phase.png`：按试验阶段划分的条形图
- `{drug}_trials_by_status.png`：按试验状态划分的条形图
- `{drug}_trials_timeline.png`：试验启动时间的时间线图表

### JSON格式的汇总数据结构
```json
{
  "drug": "sotorasib",
  "total_found": 45,
  "trials": [{"nct_id": "NCT...", "title": "...", "phase": "PHASE3", "sponsor": "Amgen", ...}],
  "stats": {"by_phase": {...}, "by_status": {...}, "top_sponsors": [...], "top_conditions": [...]}
}
```

**查询流程示例：**
- **化学结构查询 → 市场情报分析**：先解析SMILES格式的输入，再查询相关临床试验数据以了解市场竞争情况。
- **FAERS + 临床试验**：同时运行这两个查询，以获取药物的安全性概况和研发进度信息。
- **chain_entry.py**：通过`--metrics trials`或`--metrics faers,trials`参数一次性执行这两个查询。

---

## 参考资料
- [faers_fields.md](./references/faers_fields.md)：FAERS数据的关键字段及查询语法
- [clinicaltrials_fields.md](./references/clinicaltrials_fields.md)：ClinicalTrials.gov API的相关字段及枚举类型
- [openFDA药物事件API](https://open.fda.gov/apis/drug/event/)
- [ClinicalTrials.gov API v2](https://clinicaltrials.gov/data-api/api)
- [PubChem PUG REST](https://pubchem.ncbi.nlm.nih.gov/docs/pug-rest)

## 资源文件：
- **scripts/query_faers.py**：用于查询FAERS数据的脚本
- **scripts/query_trials.py**：用于查询ClinicalTrials.gov数据的脚本
- **scripts/chain_entry.py**：用于统一执行FAERS和临床试验数据查询的入口脚本
- **assets/**：用于存储生成的PNG图表文件，便于后续使用