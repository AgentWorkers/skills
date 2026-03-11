---
name: pharmaclaw-tox-agent
description: 该工具是一款用于药物安全性评估的毒理学分析软件，能够处理SMILES格式的化学结构数据。它能够计算RDKit中的ADMET参数（如logP、TPSA、分子量、HBD、HBA、可旋转键等），检测Lipinski规则五项指标的违反情况，进行Veber规则检查，以及计算QED药物相似性得分，并提供PAINS（Potentially Active Indications, Safety, and Efficacy Issues）子结构警报。该工具会输出风险等级（低/中/高）以及详细的属性报告。它接收化学结构的SMILES格式数据，将其用于后续的IP（Intellectual Property）扩展工作，以生成更安全的药物衍生物。其触发条件涉及毒理学、安全性、ADMET参数、肝毒性、致癌性、风险评估、PAINS指标、药物安全性、Lipinski规则、Veber规则以及QED（Quantitative Estimation of Drug Efficacy）等多个方面。
---
# PharmaClaw 毒理学分析工具

## 概述
PharmaClaw 毒理学分析工具是用于药物发现流程中的预测性毒理学和药物安全性评估工具。该工具通过 RDKit 描述符、基于规则的筛选条件（如 Lipinski Ro5、Veber 规则）、QED 评分以及 PAINS 警报来识别候选药物中的潜在安全风险，从而在药物发现早期阶段就发现潜在问题。

## 快速入门

```bash
# Analyze a compound
python scripts/tox_agent.py "CC(=O)Nc1ccc(O)cc1"

# Default (ethanol)
python scripts/tox_agent.py
```

## 功能特性

| 检查项目 | 方法 | 阈值 |
|---------|------|------|
| Lipinski Ro5 | 分子量 (MW)、LogP 值、HBD 值、HBA 值 | MW > 500, LogP > 5, HBD > 5, HBA > 10 |
| Veber 规则 | TPSA 值、可旋转键的数量 | TPSA > 140, 可旋转键数量 > 10 |
| QED 评分 | RDKit 的 QED 模块 | 分数范围 0-1（分数越高，越具有药物特性） |
| PAINS 警报 | 子结构匹配 | 与已知检测干扰模式的匹配 |
| 环结构分析 | 芳香环/总环数 | 用于评估化合物的复杂性 |

## 决策流程
- **输入格式：** SMILES 表达式 |
- **处理流程：** 使用 RDKit 计算描述符 → 基于规则的筛选 |
- **结果判断：**
  - **无 Lipinski 规则违反且无 PAINS 警报** → 风险等级：低 |
  - **存在任何违反规则或 PAINS 警报** → 风险等级：中等/高 |
- **高风险** → 建议通过化学查询或化合物结构扩展（IP Expansion）来寻找替代化合物 |

## 输出格式

```json
{
  "lipinski_viol": 0,
  "veber_viol": 0,
  "qed": 0.737,
  "pains": 0,
  "risk": "Low",
  "props": {
    "mw": 151.2,
    "logp": 1.02,
    "tpsa": 49.3,
    "hbd": 2,
    "hba": 2,
    "rotb": 1,
    "rings": 1,
    "arom": 1
  }
}
```

## 风险分类
- **低风险：** 无 Lipinski 规则违反，无 PAINS 警报，QED 评分 > 0.5 |
- **中等风险：** 1-2 项 Lipinski 规则违反或 QED 评分较低 |
- **高风险：** 3 项以上 Lipinski 规则违反，存在 PAINS 警报，或多项 Veber 规则违反 |

## 系统集成
- **数据来源：** 化学查询（SMILES 数据）、药理学数据（ADME 信息） |
- **数据输出：** 化合物结构扩展建议（更安全的衍生物设计）、合成建议（避免使用有毒中间体） |
- **交叉参考：** 类似化合物的市场不良反应数据（FAERS）

## 所需依赖库/工具
- `rdkit-pypi` — 提供分子描述符计算、QED 评分及子结构匹配功能 |

## 相关脚本
- `scripts/tox_agent.py` — 主要处理脚本，包含 `analyze(smiles)` 方法用于执行毒理学分析

## 限制条件
- PAINS 筛选使用的是简化的子结构集（实际生产环境中应使用完整的 PAINS 数据库） |
- 该工具不提供 Ames 致突变性评估或 hERG 通道预测功能（计划通过其他方法实现） |
- LD50 值估算功能尚未实现（未来版本将加入 QSAR 模型）