---
name: pharmaclaw-chemistry-query
description: >
  **PubChem API 查询的化学代理技能**  
  （用于获取化合物信息/属性、结构/SMILES/图像、合成路线/参考文献；以及 RDKit 化学信息学功能）  
  该技能支持以下操作：  
  - 通过 PubChem API 查询化合物的详细信息（如结构、SMILES 表示形式、图像等）  
  - 使用 RDKit 进行化学信息学分析：  
    - 将 SMILES 转换为分子属性（如 logP、TPSA 等）  
    - 生成 2D PNG/SVG 图形可视化结果  
    - 计算分子的摩根指纹（Morgan fingerprint）  
    - 执行逆合成（retrosynthesis）分析  
    - 生成多步骤合成计划（multi-step synthesis planning）  
  **应用场景**：  
  适用于涉及化合物、分子结构、PubChem 数据、RDKit 分析、SMILES 处理、合成路线设计、逆合成以及反应模拟的化学任务。  
  **触发条件**：  
  - 当涉及化学相关操作（如化合物处理、分子结构分析、PubChem 数据查询、RDKit 功能使用等）时，该技能会自动被触发。
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
# Chemistry Query Agent v1.4.1

## 概述

这是一个全栈化学工具包，结合了PubChem数据检索、RDKit分子处理、可视化、分析、逆合成以及合成规划功能。所有输出结果都以结构化的JSON格式提供，便于后续处理。可根据需求生成PNG/SVG格式的图像。

**主要功能：**
- 查找PubChem化合物的信息（包括结构、合成参考文献、相似性搜索）
- 使用RDKit获取分子的物理性质（分子量、logP值、TPSA值、氢键/疏水键数量、可旋转键、芳香环数量）
- 2D分子可视化（支持PNG/SVG格式）
- 支持BRICS逆合成算法，并可设置递归深度
- 多步骤合成路线规划
- 使用SMARTS模板进行正向反应模拟
- 计算Morgan指纹图谱，并进行相似性或子结构搜索
- 提供21种常见的化学反应模板（如Suzuki、Heck、Grignard、Wittig、Diels-Alder等）

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
通过PubChem REST API查询化合物信息，自动将名称转换为CID编码，并处理超时情况。

```
--compound <name|CID> --type <info|structure|synthesis|similar> [--format smiles|inchi|image|json] [--threshold 80]
```

- **信息（Info）：** 化合物的分子式、分子量、IUPAC名称、InChIKey（以JSON格式返回）
- **结构（Structure）：** SMILES格式的分子结构、InChI代码、图像URL或完整的JSON数据
- **合成信息（Synthesis）：** 化合物的合成方法及参考文献
- **相似化合物（Similar Compounds）：** 根据2D指纹图谱匹配的相似化合物（前20个）

### `scripts/rdkit_mol.py`
基于RDKit的化学信息学引擎，可自动通过PubChem解析化合物名称。

```
--smiles <SMILES> --action <props|draw|fingerprint|similarity|substruct|xyz|react|retro|plan>
```

| 功能 | 描述 | 关键参数 |
|--------|-------------|----------|
| 获取属性（Props） | 分子的分子量、logP值、TPSA值、氢键/疏水键数量、可旋转键数量、芳香环数量 | `--smiles` |
| 绘制分子结构（Draw） | 生成2D PNG/SVG图像（尺寸300×300像素） | `--smiles --output file.png --format png\|svg` |
| 逆合成（Retro） | 使用BRICS算法进行逆合成 | `--target <SMILES\|name> --depth N` |
| 规划合成路线（Plan） | 进行多步骤逆合成路线规划 | `--target <SMILES\|name> --steps N` |
| 进行正向反应（React） | 使用SMARTS模板进行正向反应模拟 | `--reactants "smi1 smi2" --smarts "<SMARTS>"` |
| 计算指纹图谱（Fingerprint） | 计算Morgan指纹图谱 | `--smiles --radius 2` |
| 检测相似性（Similarity） | 使用Tanimoto相似性评分算法 | `--query_smiles --target_smiles "smi1,smi2"` |
| 子结构匹配（Substruct） | 检查两个分子之间的子结构是否相同 | `--query_smiles --target_smiles "smi1,smi2"` |
| 获取3D坐标（XYZ） | 生成MMFF格式的3D坐标 | `--smiles` |

### `scripts/chain_entry.py`
标准的代理程序接口，接受`{"smiles": "...", "context": "..."`或`{"name": "...", "context": "..."`格式的输入，并返回包含化合物属性、可视化结果及逆合成信息的统一JSON格式。

```bash
python scripts/chain_entry.py --input-json '{"name": "sotorasib", "context": "user"}'
```

输出数据的结构如下：
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
包含21种常见的化学反应模板，每种模板都配备了SMARTS描述符、预期产率、反应条件及参考文献，例如：Suzuki、Heck、Buchwald-Hartwig、Grignard、Wittig、Diels-Alder等。

## 数据处理流程

1. **通过名称获取完整信息（Name → Full Profile）：** 使用`chain_entry.py`，输入`{"name": "ibuprofen"`，即可获取化合物的详细信息、结构图及逆合成结果。
2. **化学信息 → 药理学分析（Chemistry → Pharmacology）：** 处理后的结果可以直接传递给`pharma-pharmacology-agent`模块。
3. **逆合成 + 可视化（Retro + Viz）：** 首先获取化合物的前体结构，然后分别绘制每个前体的结构图。
4. **Suzuki反应测试（Suzuki Test）：** 使用`--action react --reactants "c1ccccc1Br c1ccccc1B(O)O" --smarts "[c:1][Br:2].[c:3][B]([c:4])(O)O>>[c:1][c:3]"`命令进行Suzuki反应模拟。

## 测试环境

所有功能均已使用RDKit 2024.03+版本进行了端到端的测试：

| 化合物 | SMILES | 测试是否通过 |
|----------|--------|-------------|
| 咖啡因（Caffeine） | `CN1C=NC2=C1C(=O)N(C(=O)N2C)C` | 信息、结构、属性、结构图、逆合成结果、合成路线规划 |
| 阿司匹林（Aspirin） | `CC(=O)Oc1ccccc1C(=O)O` | 信息、结构、属性、结构图、逆合成结果、合成路线规划 |
| Sotorasib | 通过PubChem名称查询化合物信息 | 信息、结构、属性、结构图、逆合成结果、合成路线规划 |
| 布洛芬（Ibuprofen） | 通过PubChem名称查询化合物信息 | 信息、结构、属性、结构图 |
| 无效的SMILES格式 | `XXXINVALID` | 会返回友好的错误提示 |
| 空输入 | `{}` | 会返回友好的错误提示 |

## 资源文档

- `references/api_endpoints.md`：PubChem API的端点信息及使用限制
- `scripts/rdkit_reaction.py`：旧的化学反应处理模块
- `scripts/chembl_query.py`、`scripts/pubmed_search.py`、`scripts/admet_predict.py`：其他查询相关脚本

### `scripts/advanced_chem.py`
高级化学信息学引擎，具备6项核心功能：

```
--action <standardize|descriptors|scaffold|mcs|mmpa|chemspace> --smiles <SMILES> [options]
```

| 功能 | 描述 | 关键参数 |
|--------|-------------|----------|
| 数据标准化（Standardize） | 去除化学式中的盐分、对电荷进行标准化处理、生成标准构象 | `--smiles` |
| 分子描述符（Descriptors） | 提供217种RDKit支持的分子描述符、QED评分、SA评分、Lipinski/Veber规则 | `--smiles --descriptor_set all\|druglike\|physical\|topological` |
| 架构分析（Scaffold） | 提取分子的Murcko骨架、生成通用骨架结构、分析分子多样性、分解R基团 | `--smiles` 或 `--target_smiles "smi1,smi2,..." `--rgroup_core <SMARTS>` |
| 最大公共子结构（MCS） | 找出两个或多个分子之间的最大公共子结构 | `--target_smiles "smi1,smi2,..."` |
| 分子对匹配分析（MMPA） | 分析分子之间的转换关系 | `--target_smiles "smi1,smi2,..."` |
| 化学空间可视化（Chemspace） | 通过PCA/t-SNE/UMAP算法生成化学空间散点图 | `--target_smiles "smi1,smi2,..." --method pca\|tsne\|umap --output plot.png` |

**示例：**
```bash
# Standardize a salt form
python scripts/advanced_chem.py --action standardize --smiles "[Na+].CC(=O)[O-]"

# Full descriptors (217+)
python scripts/advanced_chem.py --action descriptors --smiles "CC(=O)Oc1ccccc1C(=O)O" --descriptor_set all

# Scaffold diversity of a set
python scripts/advanced_chem.py --action scaffold --target_smiles "CC(=O)Oc1ccccc1C(=O)O,CN1C=NC2=C1C(=O)N(C(=O)N2C)C,CC(C)Cc1ccc(cc1)C(C)C(=O)O"

# MCS of aspirin and salicylic acid
python scripts/advanced_chem.py --action mcs --target_smiles "CC(=O)Oc1ccccc1C(=O)O,c1ccccc1C(=O)O"

# Matched molecular pairs
python scripts/advanced_chem.py --action mmpa --target_smiles "c1ccc(CC(=O)O)cc1,c1ccc(CCC(=O)O)cc1"

# Chemical space PCA plot
python scripts/advanced_chem.py --action chemspace --target_smiles "CC(=O)Oc1ccccc1C(=O)O,CN1C=NC2=C1C(=O)N(C(=O)N2C)C,c1ccccc1" --method pca --output space.png
```

## 更新日志

**v2.0.0**（2026-02-28）
- 新增`advanced_chem.py`模块，提供6项高级化学信息学功能：
  - 分子标准化与构象优化
  - 扩展了分子描述符集（217种RDKit描述符、QED评分、SA评分、Lipinski/Veber规则）
  - 架构分析（Murcko骨架、通用骨架、多样性分析）
  - 最大公共子结构检测
  - 分子对匹配分析
  - 化学空间可视化（支持PCA/t-SNE/UMAP图）
- 依赖库更新：添加了scikit-learn和matplotlib

**v1.4.1**（2026-02-25）
- 加强了安全性：
  - 对所有子进程调用（包括SMILES处理、化合物名称处理、输出路径处理）进行了安全优化
- 新增 `_sanitize_input()` 函数，用于检查用户输入的长度和是否存在空字节
- 新增 `_sanitize_output_path()` 函数，防止路径遍历攻击和任意文件写入
- 在 `resolve_target()` 函数中增加了对shell元字符的过滤
- 在 `chem_ui.py` 中通过RDKit验证SMILES格式的有效性
- 在 `query_pubchem.py` 中增加了对化合物输入的有效性检查（包括长度和空字节检查）
- 为 `resolve_target()` 中的PubChem子进程调用设置了超时限制
- 修复了VirusTotal对参数注入的检测问题

**v1.4.0**（2026-02-14）
- 修复了PubChem API端点的部分问题（如属性/CanonicalSMILES/TXT格式）
- 修复了`chain_entry.py`中的HTML实体损坏问题
- 修正了`brics_retro`函数，使其能正确处理BRICSDecompose函数的输出结果
- 为所有PubChem调用设置了15秒的超时限制
- 对无效的SMILES格式和空输入提供了友好的错误处理
- 更新了输出数据的格式和结构
- 完成了全面的端到端测试

**v1.3.0**
- 修复了RDKit相关属性类型的错误处理问题
- 修复了与反应相关的代码问题
- 所有使用RDKit的功能现在都支持通过PubChem进行名称解析

**v1.2.0**
- 新增了BRICS逆合成功能及21种化学反应模板
- 支持多步骤合成路线规划