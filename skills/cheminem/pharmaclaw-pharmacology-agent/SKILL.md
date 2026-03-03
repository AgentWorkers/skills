---
name: pharmaclaw-pharmacology-agent
description: >
  **Pharmacology Agent**  
  用于从 SMILES 格式的化学结构数据中提取药物候选物的药代动力学（ADME）和药效学（PK）信息。该工具能够计算药物与已知药物的相似性（基于 Lipinski 的 Ro5 和 Veber 规则）、QED 分数、SA 得分，以及进行 ADME 预测（包括血脑屏障（BBB）渗透性、水溶性、胃肠道吸收、CYP3A4 酶的抑制作用、P-gp 转运蛋白的底物特性和血浆蛋白结合情况）。同时，该工具还能生成与药物药理学特性、ADME 表现、PK/PD 参数、Lipinski 指数、吸收、分布、代谢、排泄、血脑屏障穿透性、溶解度等相关的数据报告。适用于药物发现和优化流程，帮助研究人员快速评估新化合物的药学特性。  
  **主要功能包括：**  
  - 计算药物与已知药物的相似性（Lipinski Ro5、Veber 规则等）  
  - 评估药物的化学结构与已知药物的相似程度  
  - 预测药物的 ADME 表现（BBB 渗透性、水溶性、吸收等）  
  - 分析药物的代谢和排泄途径  
  - 评估药物的生物利用度（Bioavailability）  
  - 提供关于药物相互作用（PAINS）的警示信息  
  **输入格式：**  
  输入数据以 SMILES 格式提供，该格式用于描述分子的化学结构。  
  **应用场景：**  
  - 药物发现（Drug Discovery）  
  - 药物优化（Drug Optimization）  
  - 药物安全性评估（Safety Assessment）  
  - 药物疗效预测（Efficacy Prediction）  
  **技术支持：**  
  - 使用化学查询（Chemistry Query）功能从 SMILES 数据中提取相关信息  
  - 支持多种药理学和药代动力学参数的计算  
  **注意事项：**  
  - 请确保输入的 SMILES 数据格式正确，以便工具能够准确解析化学结构信息。
---
# Pharma Pharmacology Agent v2.0.0

## 概述

本工具专注于对候选药物进行预测性药理学分析。它结合了ADMETlab 3.0的机器学习预测结果（如可用）与RDKit提供的基于描述符的模型，能够从SMILES字符串出发，提供全面的ADME（吸收、分布、代谢、排泄）评估、毒性风险分析、药物相似性评分以及风险提示。

**主要功能：**
- **药物相似性评估：**遵循Lipinski五规则和Veber口服生物利用度规则
- **评分指标：**QED（药物相似性定量评估）、SA Score（合成可及性评分）
- **ADME预测：**血脑屏障（BBB）渗透性、水溶性（ESOL）、胃肠道吸收（Egan模型）、CYP3A4酶抑制风险、P-糖蛋白底物特性、血浆蛋白结合能力
- **安全性评估：**PAINS（多检测干扰）过滤器警报
- **风险识别：**自动识别潜在的药理学问题
- **标准输出格式：**符合所有下游工具的JSON格式

## 快速入门

```bash
# Profile a molecule from SMILES
exec python scripts/chain_entry.py --input-json '{"smiles": "CC(=O)Oc1ccccc1C(=O)O", "context": "user"}'

# Chain from chemistry-query output
exec python scripts/chain_entry.py --input-json '{"smiles": "<canonical_smiles>", "context": "from_chemistry"}'
```

## 脚本

### `scripts/chain_entry.py`
程序的主要入口点。接收包含`smiles`字段的JSON数据，并返回完整的药理学分析结果。

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

| 属性 | 预测方法 | 阈值 |
|----------|--------|-----------|
| 血脑屏障渗透性 | Clark规则（TPSA/logP） | TPSA<60且logP在1-3区间 = 高风险；TPSA<90 = 中等风险 |
| 水溶性 | ESOL模型 | logP > -2 = 高风险；> -4 = 中等风险；否则 = 低风险 |
| 胃肠道吸收 | Egan模型 | logP<5.6且TPSA<131.6 = 高风险 |
| CYP3A4酶抑制 | 基于规则的判断 | logP>3且分子量（MW）>300 = 高风险 |
| P-糖蛋白底物 | 基于规则的判断 | MW>400且HBD>2 = 很可能是P-糖蛋白底物 |
| 血浆蛋白结合 | logP相关性 | logP>3 = 高结合率（>90%） |

## 数据流设计

本工具设计为接收来自`chemistry-query`的输出数据：

```
chemistry-query (name→SMILES+props) → pharma-pharmacology (ADME profile) → toxicology / ip-expansion
```

`recommend_next`字段始终包含`["toxicology", "ip-expansion"]`，以指示后续处理流程。

## 测试情况

所有功能均使用RDKit 2024.03+版本进行了端到端的验证：

| 分子 | 分子量（MW） | logP值 | Lipinski评分 | 主要测试结果 |
|----------|---------|---------|-----------------|-------------------|
| 咖啡因 | 194.08 | -1.03 | ✅ 通过（无违规项） | 高水溶性，中等BBB穿透性，QED评分0.54 |
| 阿司匹林 | 180.04 | 1.31 | ✅ 通过（无违规项） | 中等水溶性，SA评分1.58（合成易得），QED评分0.55 |
| Sotorasib | 560.23 | 4.48 | ✅ 通过（1项违规：分子量过大） | 低水溶性，CYP3A4酶抑制风险，高血浆蛋白结合率 |
| 二甲双胍 | 129.10 | -1.03 | ✅ 通过（无违规项） | 高水溶性，低BBB穿透性，QED评分0.25 |
| 无效的SMILES格式 | — | — | — | 会返回友好的JSON错误信息 |
| 空输入 | — | — | — | 会返回友好的JSON错误信息 |

## 错误处理机制

- 无效的SMILES格式：返回`status: "error"`并附带详细错误提示
- 缺少输入数据：会提示用户提供`smiles`或`name`字段
- 所有错误情况都会生成有效的JSON响应（程序不会崩溃）

### `scripts/admetlab3.py`
该脚本增强了ADME/毒性预测功能：首先尝试使用ADMETlab 3.0的API进行预测，若失败则转而使用RDKit的全面模型。

**输出内容包括：**
- **物理化学性质：**分子量（MW）、logP值、TPSA、logS（ESOL模型）、溶解度分类、CSP3分数、摩尔折射率
- **吸收特性：**Lipinski评分、Veber规则、Egan模型结果、Caco-2细胞渗透性、P-糖蛋白底物特性、口服生物利用度
- **分布特性：**血脑屏障穿透性（Clark模型）、血浆蛋白结合能力
- **代谢特性：**CYP3A4酶抑制风险
- **毒性评估：**hERG效应风险、Ames致突变性、DILI（药物诱导肝损伤）评估、结构相关警示（如硝基基团、芳香胺结构）
- **药物相似性评估：**QED评分、SA Score、药物相似性分类

## 参考资源

- `references/api_reference.md` — API及相关方法论的参考文档

## 更新日志

**v2.0.0**（2026-02-18）
- 集成ADMETlab 3.0的机器学习预测功能（自动切换至RDKit模型）
- 改进了RDKit的ADME预测模型（包括Caco-2渗透性、Egan模型、hERG效应、Ames致突变性评估）
- 新增了通过ESOL模型计算水溶性的功能
- 引入了药物相似性分类（lead-like/drug-like）
- 增加了对特定结构基团（如硝基、芳香胺）的警示功能

**v1.1.0**（2026-02-14）
- 首次发布版本，包含完整的ADME分析功能
- 支持Lipinski评分、Veber规则、QED评分、SA Score
- 提供了血脑屏障穿透性、水溶性、胃肠道吸收、CYP3A4酶抑制、P-糖蛋白底物等参数的预测
- 实现了自动风险评估
- 优化了输出数据的格式和错误处理机制
- 使用多种分子进行了端到端的测试验证