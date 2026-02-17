---
name: chemistry-query
description: >
  **PubChem API 查询的化学代理技能**  
  （用于获取化合物信息/属性、结构/SMILES/图像、合成路线/参考文献；以及 RDKit 化学信息学功能）  
  **功能包括：**  
  - 使用 PubChem API 查询化合物的相关信息（如结构、SMILES、图像等）  
  - 利用 RDKit 进行化学信息学处理：  
    - 将 SMILES 转换为分子属性（如 logP、TPSA 等）  
    - 生成 2D PNG/SVG 图形表示  
    - 计算分子指纹（如 Morgan 指纹）  
    - 进行逆合成分析（如 BRICS 分析）  
    - 制定多步骤合成计划  
  **适用场景：**  
  - 涉及化合物、分子结构、PubChem 数据的化学研究  
  - 使用 RDKit 进行化学信息处理和分析  
  - SMILES 数据的转换与可视化  
  - 合成路线的设计与优化  
  - 逆合成与反应模拟  
  **触发条件：**  
  - 当涉及化学相关操作（如化合物处理、分子结构分析、PubChem 数据查询、RDKit 功能调用等）时，该技能会被自动触发。
---
# Chemistry Query Agent v1.4.0

## 概述

这是一个全栈化学工具包，结合了PubChem数据检索、RDKit分子处理、可视化、分析、逆合成以及合成规划功能。所有输出结果都以结构化的JSON格式提供，便于后续处理。可根据需求生成PNG/SVG格式的分子图像。

**主要功能：**
- PubChem化合物查询（包括信息、结构、合成参考文献、相似性搜索）
- RDKit分子属性分析（分子量、logP值、TPSA、HBD/HBA、可旋转键、芳香环等）
- 2D分子可视化（PNG/SVG格式）
- 支持BRICS逆合成算法，并支持递归深度控制
- 多步合成路线规划
- 使用SMARTS模板进行正向反应模拟
- 提供Morgan指纹图谱以及相似性/子结构搜索功能
- 支持21种常见的化学反应模板（Suzuki、Heck、Grignard、Wittig、Diels-Alder等）

## 快速入门

```bash
# PubChem compound info
exec python scripts/query_pubchem.py --compound "aspirin" --type info

# Molecular properties from SMILES
exec python scripts/rdkit_mol.py --smiles "CC(=O)Oc1ccccc1C(=O)O" --action props

# Retrosynthesis
exec python scripts/rdkit_mol.py --target "CC(=O)Oc1ccccc1C(=O)O" --action retro --depth 2

# Full chain (name → props + draw + retro)
exec python scripts/chain_entry.py --input-json '{"name": "caffeine", "context": "user"}'
```

## 脚本

### `scripts/query_pubchem.py`
通过PubChem REST API进行查询，自动将化合物名称转换为CID（Compound Identifier），并处理超时情况。

```
--compound <name|CID> --type <info|structure|synthesis|similar> [--format smiles|inchi|image|json] [--threshold 80]
```

- **查询结果：** 化合物的信息（公式、分子量、IUPAC名称、InChIKey，以JSON格式返回）
- **分子结构：** SMILES格式的分子结构、InChI代码、分子图像URL或完整的JSON数据
- **合成信息：** 化合物的合成方法及参考文献
- **相似化合物：** 根据Morgan指纹图谱匹配的相似化合物（前20个）

### `scripts/rdkit_mol.py`
基于RDKit的化学信息学引擎，可自动解析化合物名称。

```
--smiles <SMILES> --action <props|draw|fingerprint|similarity|substruct|xyz|react|retro|plan>
```

| 功能 | 描述 | 必需参数 |
|--------|-------------|----------|
| props | 分子量（MW）、logP值、TPSA、HBD、HBA、可旋转键、芳香环数量 | `--smiles` |
| draw | 生成2D分子图像（PNG/SVG，尺寸300×300像素） | `--smiles --output file.png --format png\|svg` |
| retro | 使用BRICS算法进行逆合成 | `--target <SMILES\|name> --depth N` |
| plan | 规划多步合成路线 | `--target <SMILES\|name> --steps N` |
| react | 使用SMARTS模板进行正向反应模拟 | `--reactants "smi1 smi2" --smarts "<SMARTS>"` |
| fingerprint | 计算Morgan指纹图谱 | `--smiles --radius 2` |
| similarity | 使用Tanimoto算法进行相似性比较 | `--query_smiles --target_smiles "smi1,smi2"` |
| substruct | 检查分子结构是否包含指定子结构 | `--query_smiles --target_smiles "smi1,smi2"` |
| xyz | 生成分子的3D坐标（采用MMFF模型优化） | `--smiles` |

### `scripts/chain_entry.py`
标准的代理程序接口，接受`{"smiles": "...", "context": "..."}`或`{"name": "...", "context": "..."}`格式的输入，并返回包含分子属性、可视化结果及逆合成信息的统一JSON数据。

```bash
python scripts/chain_entry.py --input-json '{"name": "sotorasib", "context": "user"}'
```

### 输出数据格式
```json
{
  "agent": "chemistry-query",
  "version": "1.4.0",
  "smiles": "<canonical>",
  "status": "success|error",
  "report": {"props": {...}, "draw": {...}, "retro": {...}},
  "risks": [],
  "viz": ["path/to/image.png"],
  "recommend_next": ["pharmacology", "toxicology"],
  "confidence": 0.95,
  "warnings": [],
  "timestamp": "ISO8601"
}
```

### `scripts/templates.json`
包含21种常见的化学反应模板，每种模板都配有SMARTS描述、预期产率、反应条件及参考文献。支持的模板包括：Suzuki、Heck、Buchwald-Hartwig、Grignard、Wittig、Diels-Alder等。

## 数据处理流程

1. **名称查询 → 获取完整信息：** 使用`chain_entry.py`，输入`{"name": "ibuprofen"`，即可获取化合物的详细信息、结构图及逆合成结果。
2. **化学信息 → 药理学分析：** 将处理结果直接传递给`pharma-pharmacology-agent`模块。
3. **逆合成 → 可视化：** 获取化合物的前体结构后，分别绘制每个前体的结构图。
4. **Suzuki反应测试：** 使用`--action react --reactants "c1ccccc1Br c1ccccc1B(O)O" --smarts "[c:1][Br:2].[c:3][B]([c:4])(O)O>>[c:1][c:3]"`命令进行测试。

## 测试情况

所有功能均已使用RDKit 2024.03+版本进行了端到端的测试：

| 化合物 | SMILES | 测试结果 |
|----------|--------|-------------|
| Caffeine | `CN1C=NC2=C1C(=O)N(C(=O)N2C)C` | 成功获取信息、结构、属性、结构图、逆合成结果及合成路线 |
| Aspirin | `CC(=O)Oc1ccccc1C(=O)O` | 成功获取信息、结构、属性、结构图、逆合成结果及合成路线 |
| Sotorasib | 通过PubChem名称查询到相应化合物信息 | 成功获取信息、结构、属性、结构图及逆合成结果 |
| Ibuprofen | 通过PubChem名称查询到相应化合物信息 | 成功获取信息、结构、属性及逆合成结果 |
| 无效的SMILES格式 | 返回友好的JSON错误提示 |
| 空输入 | 返回友好的JSON错误提示 |

## 相关资源

- `references/api_endpoints.md`：PubChem API的端点信息及使用限制说明
- `scripts/rdkit_reaction.py`：旧的化学反应处理模块
- `scripts/chembl_query.py`、`scripts/pubmed_search.py`、`scripts/admet_predict.py`：其他查询相关脚本

## 更新记录

**v1.4.0**（2026-02-14）
- 修复了PubChem API中SMILES/InChI数据的处理问题
- 修复了`chain_entry.py`中HTML实体显示错误
- 修正了`brics_retro`函数对BRICSDecompose输出字符串的处理方式
- 为所有PubChem相关请求设置了15秒的超时限制
- 对无效的SMILES格式和空输入提供了友好的错误处理机制
- 更新了输出数据的格式和结构
- 完成了全面的端到端测试

**v1.3.0**
- 修复了RDKit相关属性类型为`NoneType`时的问题
- 优化了无效SMILES格式的错误处理
- 修正了`React`函数中的相关代码

**v1.2.0**
- 新增了BRICS逆合成功能及21种化学反应模板
- 支持多步合成路线规划