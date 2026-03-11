---
name: pharmaclaw-catalyst-design
description: 有机金属催化剂的推荐与新型配体设计，用于药物合成反应。根据精心整理的数据库，为各种反应类型（如铃木反应、赫克反应、布赫瓦尔德-哈特维格反应、金属交换反应、氢化反应、点击化学反应等）推荐合适的催化剂（钯Pd、钌Ru、铑Rh、铱Ir、镍Ni、铜Cu、锆Zr、铁Fe），并对其进行评分。利用RDKit软件设计新型配体变体，包括空间结构修饰、电子结构修饰及生物等效结构修饰。通过化学查询/逆合成方法获取反应类型和底物信息，并将这些数据输入到知识产权（IP）扩展系统中，将新型配体作为可申请专利的发明进行评估。系统会针对催化剂、配体、有机金属种类、交叉偶联反应、反应条件、催化剂选择、配体设计等多个方面进行综合分析。
---
# Catalyst Design Agent v1.0.0

## 概述

该工具可为药物合成步骤推荐有机金属催化剂，并设计新型配体修饰方案。主要包含两个核心工作流程：**推荐**（寻找合适的催化剂）和**设计**（创建新型配体变体）。

## 快速入门

```bash
# Recommend catalysts for a Suzuki coupling
python scripts/catalyst_recommend.py --reaction suzuki

# Recommend with constraints (prefer cheap, earth-abundant)
python scripts/catalyst_recommend.py --reaction "C-N coupling" --constraints '{"prefer_earth_abundant": true, "max_cost": "medium"}'

# Design novel ligand variants from PPh3
python scripts/ligand_designer.py --scaffold PPh3 --strategy all --draw

# Full chain: reaction → catalyst → ligand optimization
python scripts/chain_entry.py --input-json '{"reaction": "suzuki", "context": "retrosynthesis"}'
```

## 脚本

### `scripts/catalyst_recommend.py`
从精心整理的数据库中评估和排名催化剂（包含12种催化剂，28种反应类型）。

评分标准（0-100分）：反应适应性（50分）、成本（15分）、金属偏好（10分）、对映选择性（10分）、负载效率（5分）、优势（5分）、地球丰度（5分）。

### `scripts/ligand_designer.py`
通过以下三种策略生成新型配体变体：
- **空间位阻策略**：在芳香环上添加甲基（methyl）、异丙基（iPr）或叔丁基（tBu）；
- **电子效应策略**：添加氧甲基（OMe）、氟（F）或三氟甲基（CF3）取代基；
- **生物等构策略**：将氮杂环卡宾（NHC）替换为吡啶基（pyridyl），或将膦（phosphine）替换为亚磷酸酯（phosphite）；
该脚本会提供修改后的SMILES结构及其相关性质信息。

```
--scaffold <SMILES|name>       Required. PPh3, NHC_IMes, NHC_IPr, PCy3, dppe, dppp, or raw SMILES
--strategy <type>              steric|electronic|bioisosteric|all (default: all)
--draw                         Generate 2D grid PNG of variants
--output <path>                Save JSON results to file
```

### `scripts/chain_entry.py`
提供标准的PharmaClaw链式接口，支持接收JSON格式的输入数据，可用于推荐催化剂、设计配体或同时进行两者操作。
输入参数包括：`reaction`（反应类型）、`scaffold`/`ligand`（骨架/配体）、`substrate`/`smiles`（底物/SMILES结构）、`constraints`（约束条件）、`enantioselective`（对映选择性要求）、`strategy`（设计策略）、`draw`（是否需要绘图）以及`context`（上下文信息）。
如果仅提供`reaction`参数，系统会自动对排名最高的催化剂所对应的配体进行优化处理。

## 工作流程衔接

| 来源        | 输入                   | 目标                   | 输出                        |
|-------------|-------------------|-------------------|---------------------------|
| 化学查询/逆合成    | 合成步骤所需的反应类型         | **催化剂设计**           | 排名后的催化剂及使用条件              |
| **催化剂设计**     | 推荐的催化剂配体SMILES结构     | **配体设计器**           | 新型配体变体                    |
| **催化剂设计**     | 新型配体SMILES结构         | **知识产权扩展工具**         | 专利信息查询                    |
| **催化剂设计**     | 推荐的使用条件           | **化学查询工具**           | 向前反应模拟                    |

## 数据库

`references/catalyst_database.json`：包含12种催化剂、8种金属、28种反应类型的相关信息。数据库中的数据包括SMILES结构、使用条件、负载范围、成本评估、优势与局限性以及相关文献的DOI链接。
该数据库支持根据现有格式添加新的催化剂条目。

## 配体别名处理

PPh3、PCy3、dppe、dppp、NHC_IMes、NHC_IPr等配体别名会自动转换为对应的SMILES结构。