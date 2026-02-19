---
name: pharma-pharmacology-agent
description: >
  **Pharmacology Agent**  
  该工具用于从 SMILES（Simple Molecular Input Line Format）格式的化学结构数据中提取药物候选物的药理学信息，以进行 ADME（吸收、分布、代谢、排泄）和 PK（药代动力学）分析。  
  **主要功能包括：**  
  1. **药物相似性评估**：根据 Lipinski 的 Ro5 和 Veber 规则、QED（Quantitative Estrangement Degree）算法以及 SA（Structure-Area-Activity）评分来评估药物与已知药物的相似性。  
  2. **ADME 预测**：预测药物的生物利用度（Bioavailability, BBB）、水溶性（Aqueous Solubility）、胃肠道吸收（GI Absorption）、CYP3A4 酶的抑制作用、P-gp 转运蛋白的底物特性以及血浆蛋白结合情况。  
  3. **安全性警示**：提供与药物活性相关的 PAINS（Pharmacological Activity Indicators of Safety）警报。  
  4. **化学结构查询**：支持从输入的 SMILES 结构中提取相关的化学信息。  
  5. **多维度分析**：涵盖药物的药理学、ADME、PK/PD（药代动力学/药效学）特性、Lipinski 指数、吸收、分布、代谢、排泄、跨血脑屏障（BBB）能力、溶解度等多个方面。  
  6. **药物优化**：为药物研发提供关键的数据支持，帮助优化候选药物的结构。  
  **应用场景：**  
  适用于药物发现（Drug Discovery）和早期开发阶段，帮助研究人员快速评估新化合物的药理学特性和潜在的药代动力学行为。
---
# Pharma Pharmacology Agent v1.1.0

## 概述

该工具利用RDKit描述符和经过验证的基于规则的启发式方法，对候选药物进行预测性药理学分析。仅需提供一个SMILES字符串，即可获得全面的ADME（吸收、分布、代谢和排泄）评估、药物相似性评分以及风险提示。

**主要功能：**
- **药物相似性评估：** 应用Lipinski五规则和Veber口服生物利用度规则
- **评分指标：** QED（药物相似性定量评估）、SA Score（合成可及性评分）
- **ADME预测：** 血脑屏障（BBB）渗透性、水溶性（ESOL）、胃肠道吸收（Egan模型）、CYP3A4抑制剂风险、P-糖蛋白底物特性、血浆蛋白结合能力
- **安全性评估：** PAINS（多检测干扰）过滤警告
- **风险识别：** 自动识别潜在的药理学问题
- **标准输出格式：** 采用JSON格式，兼容所有后续处理工具

## 快速入门

```bash
# Profile a molecule from SMILES
exec python scripts/chain_entry.py --input-json '{"smiles": "CC(=O)Oc1ccccc1C(=O)O", "context": "user"}'

# Chain from chemistry-query output
exec python scripts/chain_entry.py --input-json '{"smiles": "<canonical_smiles>", "context": "from_chemistry"}'
```

## 脚本

### `scripts/chain_entry.py`
程序的入口文件，接收包含`smiles`字段的JSON输入，并返回完整的药理学分析结果。

**输入数据格式：**
```json
{"smiles": "CN1C=NC2=C1C(=O)N(C(=O)N2C)C", "context": "user"}
```

**输出数据格式：**
```json
{
  "agent": "pharma-pharmacology",
  "version": "1.1.0",
  "smiles": "<canonical>",
  "status": "success|error",
  "report": {
    "descriptors": {"mw": 194.08, "logp": -1.03, "tpsa": 61.82, "hbd": 0, "hba": 6, "rotb": 0, "arom_rings": 2, "heavy_atoms": 14, "mr": 51.2},
    "lipinski": {"pass": true, "violations": 0, "details": {...}},
    "veber": {"pass": true, "tpsa": {...}, "rotatable_bonds": {...}},
    "qed": 0.5385,
    "sa_score": 2.3,
    "adme": {
      "bbb": {"prediction": "moderate", "confidence": "medium", "rationale": "..."},
      "solubility": {"logS_estimate": -1.87, "class": "high", "rationale": "..."},
      "gi_absorption": {"prediction": "high", "rationale": "..."},
      "cyp3a4_inhibition": {"risk": "low", "rationale": "..."},
      "pgp_substrate": {"prediction": "unlikely", "rationale": "..."},
      "plasma_protein_binding": {"prediction": "moderate-low", "rationale": "..."}
    },
    "pains": {"alert": false}
  },
  "risks": [],
  "recommend_next": ["toxicology", "ip-expansion"],
  "confidence": 0.85,
  "warnings": [],
  "timestamp": "ISO8601"
}
```

## ADME预测规则

| 属性          | 方法                        | 阈值                          |
|----------------|-----------------------------|-----------------------------------|
| 血脑屏障渗透性      | Clark规则（TPSA/logP）                | TPSA<60且logP在1-3之间 = 高风险；TPSA<90 = 中等风险 |
| 水溶性          | ESOL近似值                     | logS > -2 = 高风险；> -4 = 中等风险；否则 = 低风险         |
| 胃肠道吸收        | Egan模型                      | logP<5.6且TPSA<131.6 = 高风险                |
| CYP3A4抑制剂风险    | 基于规则的判断                  | logP>3且分子量（MW）>300 = 高风险                |
| P-糖蛋白底物特性    | 基于规则的判断                  | 分子量（MW）>400且HBD（氢键供体数）>2 = 可能的底物       |
| 血浆蛋白结合能力    | logP相关性                    | logP>3 = 高结合能力（>90%）                    |

## 数据链处理

该工具设计用于接收`chemistry-query`的输出数据：

```
chemistry-query (name→SMILES+props) → pharma-pharmacology (ADME profile) → toxicology / ip-expansion
```

`recommend_next`字段中始终包含`["toxicology", "ip-expansion"]`，以指示后续处理流程。

## 测试情况

所有功能均使用RDKit 2024.03+版本进行了端到端的验证：

| 分子            | 分子量（MW） | logP值       | Lipinski评分 | 主要测试结果                |
|----------------|---------|------------|-----------------|-------------------------|
| 咖啡因           | 194.08     | -1.03       | ✅ 通过（无违规项）                | 高水溶性，中等BBB渗透性，QED评分0.54           |
| 阿司匹林           | 180.04     | 1.31       | ✅ 通过（无违规项）                | 中等水溶性，SA评分1.58（合成易行），QED评分0.55           |
| Sotorasib         | 560.23     | 4.48       | ✅ 通过（1项违规：分子量过大）           | 低水溶性，CYP3A4抑制剂风险，高血浆蛋白结合能力       |
| 二甲双胍           | 129.10     | -1.03       | ✅ 通过（无违规项）                | 高水溶性，低BBB渗透性，QED评分0.25           |
| 无效的SMILES字符串    |           |           |                         | 生成友好的JSON错误信息                 |
| 空输入           |           |           |                         | 生成友好的JSON错误信息                 |

## 错误处理机制
- 无效的SMILES字符串：返回`status: "error"`并附详细警告信息
- 缺少输入数据：显示要求提供`smiles`或`name`的错误提示
- 所有错误情况都会生成有效的JSON响应（程序不会崩溃）

## 参考资源
- `references/api_reference.md` — API及相关方法论的参考文档

## 更新日志

**v1.1.0**（2026-02-14）
- 首次发布版本，包含完整的ADME分析功能
- 新增Lipinski评分、Veber规则、QED评分、SA Score以及PAINS评估
- 支持血脑屏障渗透性、水溶性、胃肠道吸收、CYP3A4抑制剂风险、P-糖蛋白底物特性预测
- 实现自动风险识别功能
- 采用标准化的输出格式（JSON）
- 对多种分子进行了端到端的测试验证