---
name: rxnim
description: 使用 RxnIM 多模态大型语言模型（LLM）将化学反应图像解析为机器可读的数据（反应物、产物和反应条件）。支持通过 Web API（Hugging Face Spaces）进行调用，也支持本地推理。
homepage: https://github.com/CYF2000127/RxnIM
metadata: {"clawdbot":{"emoji":"🔬","requires":{"bins":["python3","curl"]}}}
---
# RxnIM 技能

使用 RxnIM 模型从化学反应图像中提取结构化的反应数据（SMILES、反应条件等）。RxnIM 是一个专为化学反应图像解析设计的多模态大型语言模型，在多种基准测试中实现了 84%-92% 的软匹配 F1 分数。它能够完成三项任务：反应成分提取、反应条件文本识别（OCR）以及反应物角色的识别。

## 特点

- **输入格式**：PNG、JPG 等图像文件。
- **输出格式**：JSON 格式的数据，包含反应物、产物以及反应条件（试剂、溶剂、温度、产率等信息）。
- **两种使用方式**：
  1. **Web API**：通过 Hugging Face Spaces 平台调用该模型（无需安装本地模型）。
  2. **本地推理**：在本地运行完整模型（需要 GPU 和约 14 GB 的磁盘空间）。
- **支持的任务**：
  - 反应成分提取（反应物和产物的 SMILES 表示）。
  - 反应条件文本识别（提取并标注相关文本及角色）。
  - 反应物角色识别（试剂、溶剂、温度、产率）。

## 背景

RxnIM（Reaction Image Multimodal Large Language Model）是首个专门用于将化学反应图像解析为机器可读数据的多模态语言模型。该模型能够将任务指令与图像特征相匹配，并利用基于大型语言模型的解码器来预测反应成分和条件。RxnIM 是在大量合成数据集（Pistachio）以及真实的 ACS（美国化学会）出版物数据上训练而成的。

**主要功能**：
- 高精度地提取反应物和产物的 SMILES 表示。
- 解析文本形式的反应条件（试剂、溶剂、温度、产率等）并为其分配相应角色。
- 输出结构化的 JSON 数据或格式化的反应信息。

**性能表现**：在多个测试集上的软匹配 F1 分数达到 84%-92%，优于之前的方法。

## 快速入门

**Web API 模式（默认方式）**
```bash
node scripts/rxnim.js --image /path/to/reaction.png
```

**本地模式**
1. 首先下载模型检查点文件（详见 RxnIM 仓库：https://github.com/CYF2000127/RxnIM）。
2. 设置环境变量 `RXNIM_MODEL_PATH`：
   ```bash
   export RXNIM_MODEL_PATH=/path/to/RxnIM-7b
   ```
3. 运行命令：
   ```bash
   node scripts/rxnim.js --image /path/to/reaction.png --mode local
   ```

## 安装

**依赖项**
```bash
pip install -r requirements.txt
```
对于本地模式，还需要额外的依赖项（详见 RxnIM 仓库：https://github.com/CYF2000127/RxnIM）。

**模型下载**
- **Web API**：无需下载模型。
- **本地模式**：
  1. 从 Hugging Face 下载模型检查点文件（https://huggingface.co/datasets/CYF200127/RxnIM/blob/main/RxnIM-7b.zip）。
  2. 解压文件并设置 `RXNIM_MODEL_PATH`。

## 使用方法

**命令行**
```bash
node scripts/rxnim.js --image <path> [--mode web|local] [--output json|text]
```

**输出示例**
```json
{
  "reactions": [
    {
      "reactants": ["CC(C)(C)OC(=O)N[C@H]1C=C[C@H](C(=O)O)C1",
      "products": ["CC(C)(C)OC(=O)N[C@@H]1C[C@H]2C(=O)O[C@H]2[C@@H]1Br"],
      "conditions": {
        "reagents": ["Br2", "Pyridine"],
        "solvents": ["DME/H2O"],
        "temperature": "0-5°C",
        "yield": "68%"
      },
      "full_reaction": "CC(C)(C)OC(=O)N[C@H]1C=C[C@H](C(=O)O)C1 >> CC(C)(C)OC(=O)N[C@@H]1C[C@H]2C(=O)O[C@H]2[C@@H]1Br | Br2, Pyridine[reagent], DME/H2O[solvent], 0-5°C[temperature], 68%[yield]"
    }
  ]
}
```

**配置选项**
- `RXNIM_MODE`：指定使用 Web API 还是本地模式（默认为 Web 模式）。
- `RXNIM_MODEL_PATH`：本地模式所需的模型检查点文件路径。
- `RXNIM_API_URL`：自定义的 Web API 端点地址（默认为 Hugging Face Spaces）。

**高级功能（数据生成）**
如需训练或生成合成化学反应图像，请参考原始的 RxnIM 仓库：
1. **数据集**：
  - 合成数据集：Pistachio（https://huggingface.co/datasets/CYF200127/RxnIM/blob/main/reaction_images.zip）
  - 真实化学反应数据集：ACS（https://huggingface.co/datasets/CYF200127/RxnIM/blob/main/reaction_images.zip）
2. **生成代码**：位于仓库的 `data_generation` 目录中。需要使用原始的 Pistachio 数据集。
3. **模型检查点**：下载 RxnIM-7b（https://huggingface.co/datasets/CYF200127/RxnIM/blob/main/RxnIM-7b.zip）以用于本地推理。

**注意事项**
- **Web API**：使用受网络速度限制，需要联网。
- **本地模式**：对计算资源要求较高（需要 GPU 和大量磁盘空间）。
- **模型准确性**：受图像质量和复杂度的影响。

**参考资料**
- RxnIM 项目仓库：https://github.com/CYF2000127/RxnIM
- Hugging Face Spaces 演示页面：https://huggingface.co/spaces/CYF200127/RxnIM
- 相关论文：《利用多模态大型语言模型进行的大规模化学反应图像解析》（https://doi.org/10.1039/D5SC04173B）
- ChemEAGLE（多智能体扩展）：https://github.com/CYF2000127/ChemEagle