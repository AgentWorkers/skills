---
name: pharmaclaw-cheminformatics
description: >
  这款高级化学信息学工具适用于3D分子分析、药效团映射、格式转换、RECAP片段化以及立体异构体枚举等任务。它相当于“资深化学信息学家”的升级版本，可进一步用于化学查询（Chemistry Query）相关功能。该工具支持以下应用：  
  - 3D构象体生成与集合（ETKDG + MMFF/UFF方法）；  
  - 药效团特征提取与指纹分析；  
  - 分子格式转换（SMILES/SDF/MOL/InChI/PDB/XYZ格式）；  
  - RECAP逆合成片段化技术（用于库设计）；  
  - 立体异构体枚举（R/S、E/Z类型）；  
  - 化学信息学数据分析。  
  该工具接收来自化学查询（Chemistry Query）的SMILES格式数据，并将其应用于药理学研究、催化剂设计、知识产权（IP）扩展等领域。它能够根据构象体、3D结构、药效团信息、SDF文件、MOL文件格式以及化学信息学数据触发相应的处理流程，包括片段化分析、立体异构体识别、手性分析、对映体检测等。此外，它还支持构建化学库所需的构建模块，并为分子对接（docking）任务提供准备数据。
---
# Cheminformatics Agent v1.0.0

## 概述

这是一个高级的化学信息学工具包，用于3D分子分析和药物开发工作流程。它扩展了原有的“Chemistry Query”功能（该功能主要用于2D分子的查询、属性分析和可视化），并增加了需要3D空间推理能力的预测和结构分析功能。

**Chemistry Query**：用于查询分子的2D结构信息（如分子式、属性等）。
**Cheminformatics**：用于分析分子的3D结构，包括构象变化、药效团识别、分子片段分析以及立体异构体的检测。

## 脚本

### `scripts/conformer_gen.py`
使用ETKDG库和MMFF/UFF算法生成分子的3D构象集合。

```
--smiles <SMILES> --action <generate|ensemble|best> [--num_confs N] [--optimize mmff|uff|none] [--energy_window F] [--prune_rms F] [--output file.sdf]
```

| 功能 | 描述 |
|--------|-------------|
| generate | 生成N个构象，并计算它们的能量及RMSD值（均方根偏差） |
| ensemble | 与generate功能相同，但会生成SDF格式的文件 |
| best | 找到能量最低的构象，并输出其3D坐标 |

**输出内容**：构象的能量（kcal/mol）、构象间的相对能量、收敛状态、RMSD矩阵（前20个构象）以及SDF文件。

### `scripts/format_converter.py`
用于转换不同的分子文件格式。

**支持的格式**：`smiles`、`sdf`、`mol`、`inchi`、`inchikey`、`pdb`、`xyz`。

### `scripts/pharmacophore.py`
用于提取分子的药效团特征，并进行药效团指纹的生成与比较。

**功能**：
- 提取分子的3D药效团特征（如氢键受体/HB、氢键供体、芳香性、疏水性、可电离性等）及其坐标；
- 生成Gobbi 2D药效团指纹图谱；
- 对多个分子进行药效团相似性比较（使用Tanimoto算法）；
- 生成彩色编码的药效团PNG图像（绿色表示供体、红色表示受体、黄色表示芳香基团、蓝色表示疏水基团）。

### `scripts/recap_fragment.py`
用于在可合成连接的键（如酰胺、酯、胺、尿素、醚、烯烃、磺酰胺等）处进行分子片段化分析。

**功能**：
- 生成所有片段化的分子及其元数据；
- 仅保留用于库设计的末端构建块；
- 生成分子的分解层次结构树；
- 提取多个分子中共有的片段（即共同的药效团结构）。

### `scripts/stereoisomers.py`
用于识别和分析分子的立体异构体（包括手性中心的R/S构型以及双键的E/Z构型）。

**功能**：
- 生成所有立体异构体的列表及其构型信息；
- 计算手性中心的数量和立体键的数量，无需逐一列举每个异构体；
- 比较所有立体异构体的性质（对药物开发具有重要意义）。

### `scripts/chain_entry.py`
这是一个标准化的代理程序接口，可以基于SMILES输入文件运行上述所有5个模块。

**输入JSON字段**：
- `smiles`（必填）：输入的SMILES字符串；
- `context`：链结构相关的字符串；
- `actions`：要执行的模块列表（例如`["conformers", "pharmacophore", "recap", "stereoisomers", "formats"]`；
- `output_dir`：输出文件（SDF或PNG格式）的目录。

**输出结构**：

## 数据流

| 输入来源 | 输入内容 | 处理过程 | 输出内容 |
|--------|---------|----------------|-------------------|
| Chemistry Query | SMILES分子结构 | 查询2D属性 | SMILES格式的分子信息 |
| Cheminformatics | SMILES分子结构 | 3D构象信息及药效团特征 | 3D构象数据和药效团信息 |
| Cheminformatics | SMILES分子结构 | 药效团信息及ADME（吸收、分布、代谢、排泄）相关数据 | 药效团信息用于药物开发 |
| Cheminformatics | SMILES分子结构 | 3D构象数据 | 用于催化剂选择的构象数据 |
| Cheminformatics | SMILES分子结构 | 立体异构体信息 | 可申请专利的立体异构体列表 |
| Cheminformatics | SMILES分子结构 | 分子片段信息 | 用于结构安全性的分析数据 |

## 所需依赖库**

- Python ≥ 3.10
- rdkit-pypi
- Pillow（用于生成药效团PNG图像）
- numpy