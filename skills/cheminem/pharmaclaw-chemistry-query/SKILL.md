---
name: pharmaclaw-chemistry-query
description: >
  **PubChem API 查询的化学代理技能**  
  （用于获取化合物信息/属性、结构/SMILES/图像、合成路线/参考文献；以及 RDKit 化学信息学功能）  
  该技能支持以下操作：  
  - 通过 PubChem API 查询化合物的信息和属性  
  - 获取化合物的结构数据（包括 SMILES 表示形式）及相关图像  
  - 提供合成路线和参考文献  
  - 利用 RDKit 进行化学信息学分析：  
    - 将 SMILES 转换为分子属性（如 logP、TPSA 等）  
    - 生成 2D 图形（PNG 或 SVG 格式）  
    - 计算分子的特征值（如 Morgan 指纹）  
    - 进行逆合成分析（Retrosynthesis）  
    - 制定多步骤合成方案  
  **应用场景**：  
  - 处理与化合物、分子、结构相关的化学任务  
  - 查询和解析 PubChem 数据  
  - 进行 SMILES 数据的处理与分析  
  - 设计合成路线  
  - 进行逆合成研究  
  - 模拟化学反应过程  
  **触发条件**：  
  - 当涉及化学相关操作（如化合物处理、分子结构分析、PubChem 数据查询、RDKit 功能使用等）时，该技能会被自动触发。
type: code
dependencies:
  python: ">=3.10"
  python-packages:
    - rdkit
    - gradio
    - pandas
    - Pillow
  system:
    - java (JRE 8+ for OPSIN, optional — only needed for IUPAC name→SMILES conversion)
  external-apis:
    - PubChem REST API (public, no key required)
    - ChEMBL API (public, no key required)
    - PubMed/NCBI E-utilities (public, no key required)
  notes: >
    OPSIN JAR (13.8MB) is auto-downloaded on first use of IUPAC name conversion
    with pinned SHA-256 checksum verification (d25bc08f...). All other functionality
    works without Java/OPSIN.
---
# Chemistry Query Agent v1.4.0

## 概述

这是一个全栈化学工具包，结合了PubChem数据检索、RDKit分子处理、可视化、分析、逆合成以及合成规划功能。所有输出都以结构化的JSON格式提供，便于后续处理。可根据需求生成PNG/SVG图像。

**主要功能：**
- PubChem化合物查询（信息、结构、合成参考文献、相似性搜索）
- RDKit分子属性（分子量、logP值、TPSA值、氢键/疏水键数量、可旋转键、芳香环信息）
- 2D分子可视化（PNG/SVG格式）
- 支持BRICS逆合成算法，并可设置递归深度
- 多步骤合成路线规划
- 使用SMARTS模板进行正向反应模拟
- 提供Morgan指纹图谱以及相似性/子结构搜索功能
- 支持21种常见的化学反应模板（如Suzuki、Heck、Grignard、Wittig、Diels-Alder等）

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
使用PubChem REST API进行查询，自动将化合物名称转换为CID（Compound Identifier），并处理超时问题。

```
--compound <name|CID> --type <info|structure|synthesis|similar> [--format smiles|inchi|image|json] [--threshold 80]
```

- **信息：** 化合物的化学式、分子量、IUPAC名称、InChIKey（以JSON格式提供）
- **结构：** SMILES格式的分子结构、InChI代码、图像URL或完整的JSON结构
- **合成信息：** 化合物的别名及合成参考文献
- **相似化合物：** 根据2D指纹图谱查找相似化合物（前20个）

### `scripts/rdkit_mol.py`
RDKit化学信息学引擎，可自动通过PubChem解析化合物名称。

```
--smiles <SMILES> --action <props|draw|fingerprint|similarity|substruct|xyz|react|retro|plan>
```

| 功能 | 描述 | 关键参数 |
|--------|-------------|----------|
| props | 分子的分子量、logP值、TPSA值、氢键/疏水键数量、可旋转键数量、芳香环数量 | `--smiles` |
| draw | 生成2D PNG/SVG图像（300×300像素） | `--smiles --output file.png --format png\|svg` |
| retro | 使用BRICS算法进行逆合成 | `--target <SMILES\|name> --depth N` |
| plan | 规划多步骤合成路线 | `--target <SMILES\|name> --steps N` |
| react | 使用SMARTS模板进行正向反应模拟 | `--reactants "smi1 smi2" --smarts "<SMARTS>"` |
| fingerprint | 计算Morgan指纹图谱 | `--smiles --radius 2` |
| similarity | 使用Tanimoto算法进行相似性比较 | `--query_smiles --target_smiles "smi1,smi2"` |
| substruct | 检查分子结构是否包含指定子结构 | `--query_smiles --target_smiles "smi1,smi2"` |
| xyz | 输出分子的3D坐标（采用MMFF格式优化） | `--smiles` |

### `scripts/chain_entry.py`
标准的代理链接口，接受`{"smiles": "...", "context": "..."`或`{"name": "...", "context": "..."`格式的输入，并返回包含分子属性、可视化结果及逆合成信息的统一JSON格式。

```bash
python scripts/chain_entry.py --input-json '{"name": "sotorasib", "context": "user"}'
```

**输出格式：**
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
包含21种常见化学反应的模板，每种模板都附带SMARTS描述、预期产率、反应条件及参考文献，支持以下反应类型：Suzuki、Heck、Buchwald-Hartwig、Grignard、Wittig、Diels-Alder等。

## 使用流程

1. **通过名称查询化合物信息 → 获取完整化学信息 → 绘制分子结构 → 进行逆合成分析**
   使用 `chain_entry.py` 和 `{"name": "ibuprofen"}` 进行查询。

2. **将化学信息传递给药物学分析模块（pharma-pharmacology-agent）**
   化学信息可以直接用于后续的药物学分析。

3. **逆合成结果 → 可视化展示**
   根据逆合成结果获取前体分子，并分别绘制它们的结构图。

4. **使用Suzuki反应模板进行实验**
   例如：`--action react --reactants "c1ccccc1Br c1ccccc1B(O)O" --smarts "[c:1][Br:2].[c:3][B]([c:4])(O)O>>[c:1][c:3]"`

## 测试情况

所有功能均已使用RDKit 2024.03+版本进行了端到端的测试：

| 化合物 | SMILES | 测试结果 |
|----------|--------|-------------|
| Caffeine | `CN1C=NC2=C1C(=O)N(C(=O)N2C)C` | 成功获取信息、结构、属性、结构图、逆合成结果及合成路线 |
| Aspirin | `CC(=O)Oc1ccccc1C(=O)O` | 成功获取信息、结构、属性、结构图、逆合成结果及合成路线 |
| Sotorasib | 通过PubChem名称成功查询化合物信息 | 成功获取信息、结构、属性、结构图、逆合成结果及合成路线 |
| Ibuprofen | 通过PubChem名称成功查询化合物信息 | 成功获取信息、结构、属性及合成路线 |
| 无效的SMILES格式 | 返回友好的JSON错误信息 |
| 空输入 | 返回友好的JSON错误信息 |

## 资源文档

- `references/api_endpoints.md`：PubChem API的端点信息及使用限制说明
- `scripts/rdkit_reaction.py`：旧的化学反应处理模块
- `scripts/chembl_query.py`、`scripts/pubmed_search.py`、`scripts/admet_predict.py`：其他查询相关脚本

## 更新日志

**v1.4.0**（2026-02-14）
- 修复了PubChem SMILES/InChI数据格式的问题
- 修复了`chain_entry.py`中HTML实体显示错误
- 修正了`brics_retro`函数对BRICSDecompose输出的处理方式
- 为所有PubChem API调用设置了15秒的超时限制
- 对无效的SMILES格式和空输入提供了友好的错误处理机制
- 更新了输出格式和结构
- 完成了全面的端到端测试

**v1.3.0**
- 修复了RDKit相关属性类型的问题，以及对无效SMILES格式的友好错误处理
- 修正了`React`模块中的`ReactionFromSmarts`函数
- 所有RDKit相关操作均通过PubChem进行名称解析

**v1.2.0**
- 新增了BRICS逆合成功能及21种化学反应模板
- 支持多步骤合成路线规划