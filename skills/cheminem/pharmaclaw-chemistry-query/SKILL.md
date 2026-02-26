---
name: pharmaclaw-chemistry-query
description: >
  **PubChem API 查询的化学代理技能**  
  （用于获取化合物信息/属性、结构/SMILES/图像、合成路线/参考文献；以及 RDKit 化学信息学功能）  
  **功能概述：**  
  支持使用 PubChem API 查询化合物的相关信息，并结合 RDKit 的化学信息学工具进行处理：  
  - 将 SMILES 格式的化学结构转换为分子属性（如 logP、TPSA 等）  
  - 生成 2D PNG/SVG 格式的分子结构图  
  - 计算分子的摩根指纹（Morgan fingerprint）  
  - 进行逆合成分析（retrosynthesis）  
  - 制定多步骤合成计划（multi-step synthesis planning）  
  **应用场景：**  
  适用于涉及化合物、分子结构、PubChem 数据、RDKit 分析、SMILES 处理、合成路线设计、逆合成以及反应模拟的化学任务。  
  **触发条件：**  
  当涉及到化学相关操作（如化合物处理、分子结构分析、PubChem 数据查询、RDKit 工具应用、SMILES 格式转换、合成路线规划等）时，该技能会被自动触发。
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
- PubChem化合物查询（信息、结构、合成参考文献、相似性搜索）
- RDKit分子属性（分子量、logP值、TPSA值、氢键/疏水键数量、可旋转键、芳香环数量）
- 2D分子可视化（PNG/SVG格式）
- 支持BRICS逆合成算法，并具有递归深度控制功能
- 多步骤合成路线规划
- 使用SMARTS模板进行正向反应模拟
- 提供Morgan指纹图谱以及化合物的相似性/子结构搜索功能
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
使用PubChem REST API进行查询，自动将化合物名称转换为CID（Compound Identifier），并处理超时问题。

```
--compound <name|CID> --type <info|structure|synthesis|similar> [--format smiles|inchi|image|json] [--threshold 80]
```

- **信息：** 化合物的化学式、分子量、IUPAC名称、InChIKey（以JSON格式提供）
- **结构：** SMILES格式的分子结构、InChI字符串、图像URL或完整的JSON结构
- **合成信息：** 化合物的合成方法及参考文献
- **相似性查询：** 根据2D分子指纹图谱查找相似化合物（前20个）

### `scripts/rdkit_mol.py`
基于RDKit的化学信息学引擎，可自动通过PubChem解析化合物名称。

```
--smiles <SMILES> --action <props|draw|fingerprint|similarity|substruct|xyz|react|retro|plan>
```

| 功能 | 描述 | 关键参数 |
|--------|-------------|----------|
| props | 分子的分子量、logP值、TPSA值、氢键数量、疏水键数量、可旋转键数量、芳香环数量 | `--smiles` |
| draw | 生成2D分子图像（PNG/SVG格式，尺寸300×300像素） | `--smiles --output file.png --format png\|svg` |
| retro | 使用BRICS算法进行逆合成 | `--target <SMILES\|name> --depth N` |
| plan | 规划多步骤合成路线 | `--target <SMILES\|name> --steps N` |
| react | 使用SMARTS模板进行正向反应模拟 | `--reactants "smi1 smi2" --smarts "<SMARTS>"` |
| fingerprint | 计算Morgan指纹图谱 | `--smiles --radius 2` |
| similarity | 使用Tanimoto算法进行相似性比较 | `--query_smiles --target_smiles "smi1,smi2"` |
| substruct | 检查两个分子之间的子结构是否匹配 | `--query_smiles --target_smiles "smi1,smi2"` |
| xyz | 生成分子的3D坐标（采用MMFF格式优化） | `--smiles` |

### `scripts/chain_entry.py`
标准的代理程序接口，接受`{"smiles": "...", "context": "..."`或`{"name": "...", "context": "..."`格式的输入，并返回包含化合物属性、可视化结果及逆合成信息的统一JSON格式输出。

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
包含21种常见化学反应的模板，附带相应的SMARTS描述、预期产率、反应条件及参考文献。支持的化学反应模板包括：Suzuki、Heck、Buchwald-Hartwig、Grignard、Wittig、Diels-Alder等。

## 使用流程

1. **通过名称查询化合物信息 → 获取完整化学信息 → 绘制分子结构图 → 进行逆合成分析**
   使用`chain_entry.py`，输入例如`{"name": "ibuprofen"}`，即可依次执行这些操作。

2. **将化学信息传递给药物学分析模块（pharma-pharmacology-agent）**
   逆合成结果可以直接用于后续的药物学分析。

3. **逆合成结果 → 可视化展示**
   可以先获取化合物的前体结构，再分别对每个前体进行可视化展示。

4. **使用Suzuki反应模板进行实验**
   例如：`--action react --reactants "c1ccccc1Br c1ccccc1B(O)O" --smarts "[c:1][Br:2].[c:3][B]([c:4])(O)O>>[c:1][c:3]"`

## 测试情况

所有功能均已使用RDKit 2024.03+版本进行了端到端的测试：

| 化合物 | SMILES | 测试结果 |
|----------|--------|-------------|
| Caffeine | `CN1C=NC2=C1C(=O)N(C(=O)N2C)C` | 成功获取了信息、结构、属性、分子结构图、逆合成结果及合成路线 |
| Aspirin | `CC(=O)Oc1ccccc1C(=O)O` | 成功获取了信息、结构、属性、分子结构图、逆合成结果及合成路线 |
| Sotorasib | 通过PubChem名称成功查询到相关信息 | 成功获取了信息、结构、属性、分子结构图及逆合成结果 |
| Ibuprofen | 通过PubChem名称成功查询到相关信息 | 成功获取了信息、结构及逆合成结果 |
| 无效的SMILES格式 | 显示友好的JSON错误提示 |
| 空输入 | 显示友好的JSON错误提示 |

## 资源文档

- `references/api_endpoints.md`：PubChem API的端点信息及使用限制说明
- `scripts/rdkit_reaction.py`：旧的化学反应处理模块
- `scripts/chembl_query.py`、`scripts/pubmed_search.py`、`scripts/admet_predict.py`：其他查询相关脚本

## 更新日志

**v1.4.1**（2026-02-25）
- 加强了输入数据的安全性处理（对SMILES字符串、化合物名称及输出路径进行清洗）
- 新增了 `_sanitize_input()` 函数，用于限制输入长度并过滤空字节
- 新增了 `_sanitize_output_path()` 函数，防止路径遍历攻击，限制文件扩展名，并阻止任意文件写入
- 在 `resolve_target()` 函数中增加了对shell元字符的过滤
- 在 `chem_ui.py` 中通过RDKit对SMILES字符串进行了验证
- 在 `query_pubchem.py` 中增加了对输入数据的验证（检查长度及是否存在空字节）
- 为 `resolve_target()` 函数中的PubChem子进程调用设置了超时限制
- 解决了VirusTotal工具对参数注入的“可疑”分类问题

**v1.4.0**（2026-02-14）
- 修复了PubChem API中SMILES/InChI数据格式的相关问题
- 修复了`chain_entry.py`中HTML实体显示错误的问题
- 修正了`brics_retro`函数对BRICSDecompose输出的处理方式
- 为所有PubChem相关调用设置了15秒的超时限制
- 对无效的SMILES输入和空输入提供了友好的错误处理机制
- 更新了输出结果的格式和结构
- 完成了全面的端到端测试

**v1.3.0**
- 修复了RDKit相关属性类型的问题，以及对无效SMILES格式的错误处理
- 修复了`React`模块中的相关问题
- 所有使用RDKit的函数现在都支持通过PubChem解析化合物名称

**v1.2.0**
- 新增了BRICS逆合成功能及21种化学反应模板
- 支持多步骤合成路线规划