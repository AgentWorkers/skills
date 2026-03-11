---
name: pharmaclaw-alphafold-agent
description: 这款AlphaFold代理软件符合相关标准，可用于蛋白质结构检索、ESMFold预测、结合位点检测以及RDKit配体对接等功能。它能够获取公开的PDB/AlphaFold数据库中的结构数据，通过ESMFold（HuggingFace提供）进行蛋白质结构预测，识别蛋白质的结合口袋，并执行基本的分子对接操作。该软件还可以接收来自化学查询系统的SMILES格式结构数据，将其用于后续的IP扩展（IP Expansion）和催化剂设计（Catalyst Design）流程。触发条件包括“alphafold”、“fold”、“PDB”、“docking”、“structure”、“protein”、“binding site”、“pocket”、“UniProt”以及“KRAS”等关键词。
---
# PharmaClaw AlphaFold Agent

## 概述
PharmaClaw AlphaFold Agent 是一个用于药物发现流程的蛋白质结构检索和配体对接工具。它从 RCSB PDB 数据库获取实验结构，从 AlphaFold 数据库获取预测结构，检测结合位点，并使用 RDKit 进行基于构象的配体对接。

## 快速入门

```bash
# Fetch structure and dock a ligand
python scripts/alphafold_agent.py '{"uniprot": "P01116", "smiles": "CC(=O)Nc1ccc(O)cc1"}'

# Structure retrieval only
python scripts/alphafold_agent.py '{"uniprot": "P01116"}'
```

## 功能

| 功能        | 方法                | 数据来源                |
|------------|------------------|----------------------|
| 结构检索      | RCSB 搜索 API + AlphaFold DB    | 公开的 PDB 文件             |
| 结构预测      | 通过 HuggingFace 的 ESMFold 进行   | 序列 → 3D 结构             |
| 结合位点检测    | 基于残基级别的结合口袋检测      |                         |
| 配体对接      | 使用 RDKit 生成构象进行对接     | SMILES → 亲和力评分           |

## 决策流程
- 是否提供了 UniProt ID？→ 从 RCSB PDB 或 AlphaFold DB 获取结构
- 是否提供了 FASTA 序列？→ 使用 ESMFold 进行结构预测
- 是否提供了 SMILES？→ 将配体对接到检测到的结合口袋中
- 未找到结构？→ 回退到使用 ESMFold 进行预测

## 输入格式

```json
{
  "uniprot": "P01116",
  "smiles": "CC(=O)Nc1ccc(O)cc1",
  "fasta": "path/to/sequence.fasta"
}
```

## 输出格式

```json
{
  "pdb": "1abc.pdb",
  "sites": [{"res": "G12", "pocket_vol": 150}],
  "docking": {"affinity": -15.2, "viz": "docked.png"},
  "compliance": "Public AlphaFold 2 DB/ESMFold (commercial OK)"
}
```

## 链接整合
- **输入来源：** 化学查询（用于配体对接的 SMILES 数据）、文献（目标蛋白质信息）
- **输出结果：** 新的结合模式（IP Expansion）、结构引导的合成（Catalyst Design）

## 依赖库
- `rdkit-pypi` — 用于生成分子构象和描述符
- `biopython` — 用于解析 PDB 文件和处理 FASTA 序列
- `requests` — 用于调用 RCSB 和 AlphaFold 数据库的 API

## 合规性
仅使用公开可用的蛋白质结构（RCSB PDB、AlphaFold DB）和开源的预测工具（ESMFold）。所有数据来源均符合商业使用规范，未使用任何专有的 AlphaFold 3 服务器。

## 脚本
- `scripts/alphafold_agent.py` — 主要脚本：负责数据获取、结构预测、结合位点检测和配体对接

## 限制
- 配体对接使用 RDKit 的构象评分方法（而非基于物理原理的 Vina 算法）
- 对于大型蛋白质，ESMFold 的结构预测需要较高的计算资源
- 结合位点检测较为简化；实际应用中建议集成 fpocket 或 P2Rank 等更精确的检测工具