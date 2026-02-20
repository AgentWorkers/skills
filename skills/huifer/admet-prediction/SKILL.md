---
name: admet-prediction
description: >
  ADMET（吸收、分布、代谢、排泄、毒性）预测  
  用于评估候选药物的相似性、药代动力学（PK）特性以及药物发现早期的安全风险。  
  关键词：ADMET、PK、毒性、药物相似性、药物诱导肝损伤（DILI）、hERG通道、生物利用度
category: DMPK
tags: [admet, pk, toxicity, drug-likeness, safety]
version: 1.0.0
author: Drug Discovery Team
dependencies:
  - rdkit
  - admet-models
---
# ADMET 预测技能

该技能用于预测 ADMET（吸收、分布、代谢、排泄和毒性）属性，以确定化合物的开发优先级。

## 快速入门

```
/admet "CC1=CC=C(C=C1)CNC" --full
/pk-prediction --library compounds.sdf --threshold 0.7
/toxicity-screen CHEMBL210 --include hERG,DILI,Ames
```

## 包含内容

| 属性 | 预测方法 | 模型       |
|--------|-----------|-----------|
| 吸收   | Caco-2、HIA、Pgp | 机器学习/QSAR   |
| 分布   | VDss、PPB、BBB | 机器学习/QSAR   |
| 代谢   | CYP抑制、清除率 | 机器学习/QSAR   |
| 排泄   | 清除率、半衰期 | 机器学习/QSAR   |
| 毒性   | hERG、DILI、Ames、致突变性 | 机器学习/QSAR   |

## 输出结构

```markdown
# ADMET Profile: CHEMBL210 (Osimertinib)

## Summary
| Property | Value | Status |
|----------|-------|--------|
| Drug-likeness | Pass | ✓ |
| Lipinski Ro5 | 0 violations | ✓ |
| VEBER | Pass | ✓ |
| PAINS | 0 alerts | ✓ |
| Brenk | 0 alerts | ✓ |

## Absorption
| Property | Prediction | Confidence |
|----------|------------|-------------|
| HIA | 98% | High |
| Caco-2 | 15.2 × 10⁻⁶ cm/s | High |
| Pgp substrate | Yes | Medium |
| F30% | 65% | Medium |

## Distribution
| Property | Prediction | Confidence |
|----------|------------|-------------|
| VDss | 5.2 L/kg | Medium |
| PPB | 95% | High |
| BBB | Yes | High |
| CNS MPO | 5.5 | Good |

## Metabolism
| Property | Prediction | Confidence |
|----------|------------|-------------|
| CYP3A4 substrate | Yes | High |
| CYP3A4 inhibitor | Yes | Medium |
| CYP2D6 inhibitor | No | High |
| CYP2C9 inhibitor | No | Medium |
| Clearance | 8.5 mL/min/kg | Low |

## Excretion
| Property | Prediction | Confidence |
|----------|------------|-------------|
| Renal clearance | 10% | Medium |
| Half-life | 48 hours | High |

## Toxicity
| Property | Prediction | Confidence |
|----------|------------|-------------|
| hERG inhibition | No | High |
| DILI | Concern | Medium |
| Ames mutagenicity | Negative | High |
| Carcinogenicity | Negative | Medium |
| Respiratory toxicity | No | Low |

## Recommendations
**Strengths**:
- Good oral bioavailability (65%)
- Brain penetration (BBB permeable)
- Low hERG risk

**Concerns**:
- DILI concern - monitor in preclinical studies
- CYP3A4 inhibition - potential DDIs

**Overall**: Good ADMET profile. Progress to in vivo PK.
```

## 属性范围

### 药物相似性评估

| 规则          | 通过标准       |
|--------------|-------------|
| Lipinski Ro5     | 不超过1项违规     |
| Veber        | RotB ≤ 10, PSA ≤ 140 Ų  |
| Egan        | LogP ≤ 5, PSA ≤ 131 Ų  |
| MDDR        | 分子量 ≤ 600, LogP ≤ 5  |

### 吸收

| 属性          | 良好       | 中等       | 差         |
|--------------|-----------|-----------|-----------|
| HIA          | >80%        | 40-80%       | <40%       |
| Caco-2        | >10         | 1-10        | <1         |
| F30%         | >70%        | 30-70%       | <30%       |

### 分布

| 属性          | 良好       | 中等       | 差         |
|--------------|-----------|-----------|-----------|
| VDss         | 0.3-5 L/kg     | <0.3 或 >5     | 极端        |
| PPB          | <90%        | 90-95%       | >95%       |
| BBB          | LogBB > 0.3     | -0.3 至 0.3     | < -0.3      |

### 毒性警报

| 警报类型       | 应对措施       |
|--------------|-------------|
| hERG抑制      | 心脏毒性风险     |
| DILI阳性      | 肝毒性风险     |
| Ames阳性      | 致突变性风险     |
| PAINS        | 测定干扰      |
| 结构警报      | 进一步研究     |

## 运行脚本

```bash
# Full ADMET profile
python scripts/admet_predict.py --smiles "CC1=CC=C..." --full

# Batch prediction
python scripts/admet_predict.py --library compounds.sdf --output results.csv

# Specific properties
python scripts/admet_predict.py --smiles "..." --properties hERG,DILI,CYP

# Filter by criteria
python scripts/admet_filter.py --library compounds.sdf --rules lipinski,veber
```

## 需求

```bash
pip install rdkit

# Optional for advanced models
pip install deepchem admet-x
```

## 参考资料

- [reference/admet-properties.md](reference/admet-properties.md) - 详细的属性参考资料
- [reference/toxicity-alerts.md](reference/toxicity-alerts.md) - 毒性警报参考资料
- [reference/pk-models.md](reference/pk-models.md) - 药物动力学（PK）预测模型

## 最佳实践

1. **使用多种模型**：综合多种模型的预测结果更可靠。
2. **检查预测置信度**：置信度低时需要实验验证。
3. **考虑化合物的化学结构**：新颖结构的预测结果可能不够准确。
4. **迭代设计**：利用预测结果指导化合物的合成过程。
5. **尽早验证**：通过实验确认关键预测结果。

## 常见问题及解决方法

| 问题         | 解决方案       |
|--------------|-------------|
| 过度依赖预测结果   | 需要进行实验验证     |
| 忽视预测置信度     | 检查模型的适用范围     |
| 仅使用单一模型     | 综合多个模型的预测结果   |
| 忽视化合物的化学特性 | 新型化合物的预测结果可能不准确 |
| 在后期进行测试     | 早期进行ADMET筛选可以节省时间 |

## 限制因素

- **模型存在误差**：预测结果可能存在偏差。
- **新颖化学结构**：对于新型化合物，预测结果的可靠性较低。
- **体外与体内实验的差异**：预测结果可能与实际情况不符。
- **物种差异**：人类毒性预测通常基于动物实验数据。
- **复杂的作用机制**：某些毒性效应可能无法被预测。