# drug-team

这是一个元技能（meta-skill），用于协调一组专门用于药物设计的AI代理（AI agents）来共同完成任务。

## 概述
- **用途**：在特定目标/适应症（例如：“设计用于止痛的药物，logP<3”）的约束条件下，设计新型药物候选物。
- **代理（Agents）**：
  1. **Chem Synth**（使用chemistry-query技能）：提出分子骨架和合成路线。
  2. **Synth Notebook**（使用synth-notebook技能）：可视化合成路线，优化产率，并检查安全性。
  3. **Lab Inventory**（使用lab-inventory技能）：检查试剂库存，并估算成本。
  4. **ADMET**：使用RDKit/ML代理预测药物的化学性质（如QED、SA、logP、TPSA、pKa）。
  5. **Tox**：检查药物的毒性（PAINS指标）、Brenk警报以及Ames测试结果。
  6. **Pharm**：通过Web工具评估药物与靶点的结合亲和力。
  7. **Patent Scout**（使用patent_scout.py）：扫描现有技术专利，计算新颖性得分，并通过Web搜索检查是否存在阻碍药物开发的专利。
- **协调方式**：代理之间通过迭代式通信（polling and messaging）来不断完善候选药物方案。
- **输出结果**：列出排名前三的分子（包含SMILES结构、合成路线及各项评分），并提供可视化结果（如分子图像）。

## 触发条件（Triggers）
- drug design（药物设计）
- design drug（设计药物）
- painkiller（止痛药）
- drug synthesis（药物合成）
- synth pharm（合成与药物开发）
- design molecule（设计分子）
- “low tox” drug（低毒性的药物）
- inventory-aware design（考虑库存情况的设计）
- design with stock check（在检查库存的情况下进行设计）
- check stock for synthesis（检查合成所需的试剂库存）
- patent（专利相关操作）
- novelty（新颖性评估）
- prior art（现有技术调查）

## 使用方式
当触发相应命令时，会运行`scripts/orchestrate.py \"{user_query}\"`。

## 集成方式（Integration）
- 集成chemistry-query技能以生成初始的分子骨架和合成路线。
- 使用synth-notebook技能进行合成路线的可视化、产率优化及安全性检查。
- 结合lab-inventory技能来检查试剂库存并估算成本。
- 根据产率、安全性（通过SDS扫描确定化学品风险）、以及试剂库存情况对候选药物进行排名。
- 设计完成后，通过专利扫描（patent scouting）将新颖性得分和专利阻碍情况纳入候选药物排名（例如：“高新颖性：无专利阻碍”）。

## 所需依赖项（Dependencies）
- RDKit（已安装）
- chemistry-query技能
- synth-notebook技能
- lab-inventory技能
- Matplotlib/Plotly用于数据可视化
- OpenClaw子代理（用于任务执行）
- beautifulsoup4用于专利信息抓取