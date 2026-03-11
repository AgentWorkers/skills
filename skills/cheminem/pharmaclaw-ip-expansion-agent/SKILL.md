---
name: pharmaclaw-ip-expansion-agent
description: >
  **知识产权拓展代理（Intellectual Property Expansion Agent）**  
  专为制药公司的药物发现/开发团队提供专业服务。该代理通过以下方式主动管理和拓展公司的知识产权（IP）组合：  
  1. 分析来自其他药物发现/合成团队的 SMILES（结构式分子表示法）数据；  
  2. 利用 RDKit 的相似性检测功能及专利查询 API 进行侵权分析（FTO – Freedom to Operate）；  
  3. 深入挖掘现有文献中的现有技术，为新药分子提供创新性建议（例如生物异构体、衍生物等）；  
  4. 提出具有战略意义的专利申请策略。  
  主要功能包括：  
  - 根据 IP、专利、侵权、新颖性等相关查询，对分子、SMILES 或治疗药物进行深度分析；  
  - 实时跟踪公司的知识产权组合状况；  
  - 与化学研究、毒理学评估及安全性评估团队紧密协作，确保知识产权的有效利用。  
  该服务适用于以下场景：  
  - 评估可申请专利的衍生化合物；  
  - 制定风险管理策略；  
  - 识别潜在的知识产权空白领域；  
  - 监控专利的有效期。
  Intellectual Property Expansion Agent for pharma drug discovery/development teams.
  Proactively manages/expands IP portfolios by analyzing SMILES/molecules from other agents
  (Drug Discovery/Synthesis), performing infringement/FTO analyses via RDKit similarity & patent APIs,
  mining prior art for novelty suggestions (bioisosteres/derivatives), and recommending strategic claims.
  Triggers on: IP/patent/FTO/infringement/novelty/prior art queries for molecules/SMILES/therapeutics;
  portfolio tracking; chaining with chemistry-query/Tox/Safety agents.
  Use for patentable derivative ideas, risk matrices, white space identification, expiration monitoring.
---
# 制药知识产权扩展代理（Pharma IP Expansion Agent）

这是一个专门用于扩展制药团队功能的代理工具（涵盖药物发现、化学合成查询、专利/文献/毒性/安全性分析等）。该代理能够分析输入数据（如SMILES结构、关键词或化合物信息），并提供有价值的知识产权洞察，包括资产管理、侵权风险分析、新颖性评估以及战略扩展建议。输出结果以JSON格式或MD格式呈现，并附带RDKit生成的可视化图表（PNG或SVG格式）。

## 核心功能

该代理遵循以下工作流程：解析输入数据 → 进行分析 → 生成报告 → 将结果记录到资产数据库中：

1. **资产管理**：跟踪专利和应用程序的详细信息，并监控其有效期。可使用`scripts/agent.py track`脚本进行管理。
2. **侵权风险分析**：利用RDKit的Morgan-Franklin（Morgan FP）和Tanimoto相似性算法评估化合物的侵权风险（Tanimoto相似度大于0.8表示高风险）。
3. **自由竞争分析（FTO）**：通过USPTO或PubChem数据库搜索可能构成技术障碍的专利。
4. **现有技术挖掘与新颖性评估**：利用自然语言处理技术提取专利权利要求和化合物信息，推荐具有新颖性的化合物作为研发目标。
5. **战略扩展建议**：根据市场趋势建议进一步的研发方向或化合物的再利用方案。

## 快速启动

运行主代理程序：
```
python3 scripts/agent.py --mode analysis --input '{"smiles": ["CCO"], "from_agent": "synthesis", "therapeutic": "pain"}'
```
程序将生成包含风险分析结果、建议内容及可视化图表的JSON报告，并将其保存到资产数据库中。

### 多代理协同工作（与OpenClaw集成）

在OpenClaw框架下，可以通过启动包含该代理功能的子会话，并将化学合成查询的结果以JSON格式传递给该代理来实现多代理协同工作。

## 工作流程决策树

- 输入数据为JSON或SMILES格式？ → 使用RDKit进行结构解析 → 生成化合物的“指纹”特征 → 与现有专利进行比对（参考`scripts/rdkit_utils.py`）。
- 需要查询资产数据库？ → 使用SQLite进行查询（`self.db`文件）。
- 需要评估侵权风险或现有技术状况？ → 通过API获取相关信息，并利用自然语言处理技术进行解析（参考`references/nlp_patterns.md`）。
- 需要制定战略规划？ → 可结合PubChem提供的市场趋势数据进行分析。
- 需要考虑国际专利或人工智能相关因素？ → 注意潜在的法律风险并进行标记。

输出结果应遵循以下格式：
`{"risks": [...], "suggestions": [...], "viz_path": "report.png", "recommendations": {...}}` + MD格式的报告。

## 多代理集成示例（与OpenClaw结合使用）

- 来自化学合成模块的输入数据：`{"smiles": [...], "reactions": [...]}` → 该代理会自动进行侵权风险检查。
- 该代理会与毒性/安全性分析模块协同工作，结合药物吸收、分布、代谢和排泄（ADMET）数据来优先筛选合适的化合物。
- 可通过`sessions_spawn task="IP expand this SMILES from synth: ..."`命令启动相关任务。
- 该代理支持定期自动执行资产数据库检查。

## 所需资源

### 相关脚本

- `agent.py`：包含所有核心功能的Python代理类，可直接执行或通过导入使用。
- `rdkit_utils.py`：提供分子结构相似性计算和生物异构体分析功能。
- `patent-fetch.py`：用于调用USPTO和PubChem的API。
- `nlp_extract.py`：利用spaCy库提取专利权利要求和化合物名称。

测试命令：`python3 scripts/agent.py --help`

### 参考文档

- `apis.md`：列出了可使用的API接口（包括USPTO、EPO和PubChem）。
- `rdkit_guide.md`：详细介绍了RDKit的分子结构相似性计算方法和Tanimoto相似性阈值。
- `ip_strategies.md`：总结了专利权利要求的相关类型及自由竞争分析的最佳实践。
- `pharma_trends.md`：提供了关于人工智能在知识产权分析中的应用及PCT（专利合作条约）的相关信息。

相关API的详细信息可通过`read references/apis.md`文件获取。

### 数据存储与格式

- 数据库：使用SQLite数据库`ip_portfolio.db`（基于`portfolio_schema.sql`模板进行初始化）。
- 风险阈值：Tanimoto相似度大于0.85表示高风险，可进行配置。
- 可视化结果：以PNG或SVG格式保存在当前目录下。
- 所需依赖库：`pip install rdkit-pypi requests pandas sqlite3 spacy scispacy`（假设已安装相关Python库）。
- 日志记录：所有操作都会被记录到`logs/ip_expansion.log`文件中。
- 在OpenClaw框架中，使用`exec`命令来执行代理程序；报告文件则保存在指定目录下。

如需更新代理功能，请直接修改相应的Python类方法。