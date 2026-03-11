---
name: "sales-engineer"
description: 分析RFP/RFI（需求提案/询价）的回复，找出其中的覆盖范围缺口；构建具有竞争力的功能对比矩阵；为售前工程团队规划概念验证（POC）项目。适用于以下场景：回复RFP、投标或提案请求；对比产品功能与竞争对手的产品；规划或评估客户的概念验证项目或销售演示；准备技术提案；或进行竞争对手的胜败分析。具体任务包括：“RFP回复”、“投标回复”、“提案回复”、“竞争对手对比”、“功能矩阵编制”、“POC项目规划”、“销售演示准备”以及“售前工程支持”。
---
# 销售工程师技能

## 五阶段工作流程

### 第一阶段：发现与研究

**目标：** 了解客户需求、技术环境及业务驱动因素。

**检查清单：**
- [ ] 与相关方进行技术沟通
- [ ] 映射客户的当前架构和痛点
- [ ] 识别集成需求和限制条件
- [ ] 记录安全性和合规性要求
- [ ] 分析该机会的竞争格局

**工具：** 运行 `rfp_response_analyzer.py` 以评估需求匹配度。

**输出：** 技术发现文档、需求映射图、初步覆盖度评估。

**验证检查点：** 覆盖度得分必须 >50%，且必须满足的需求缺口 ≤3，才能进入第二阶段。请与以下人员确认：  
```bash
python scripts/rfp_response_analyzer.py assets/sample_rfp_data.json --format json | python -c "import sys,json; r=json.load(sys.stdin); print('PROCEED' if r['coverage_score']>50 and r['must_have_gaps']<=3 else 'REVIEW')"
```

---

### 第二阶段：解决方案设计

**目标：** 设计满足客户需求的解决方案架构。

**检查清单：**
- [ ] 将产品功能与客户需求对应起来
- [ ] 设计集成架构
- [ ] 识别定制需求及开发工作量
- [ ] 制定差异化策略
- [ ] 创建解决方案架构图

**工具：** 使用第一阶段的数据运行 `competitive_matrix_builder.py`，以识别差异化点和潜在风险。

**输出：** 解决方案架构、竞争定位、技术差异化策略。

**验证检查点：** 确保每个客户优先事项至少存在一个明显的差异化点，才能进入第三阶段。如果没有找到差异化点，请与产品团队联系（参见“集成点”部分）。

---

### 第三阶段：演示准备与交付

**目标：** 根据相关方的优先级，准备有吸引力的技术演示。

**检查清单：**
- [ ] 构建符合客户用例的演示环境
- [ ] 编写针对不同角色所需的演示脚本
- [ ] 准备应对异议的策略
- [ ] 练习处理失败情况和恢复流程
- [ ] 收集反馈并调整演示内容

**模板：** 使用 `assets/demo_script_template.md` 进行结构化的演示准备。

**输出：** 定制的演示脚本、针对特定相关方的演示内容、反馈记录。

**验证检查点：** 演示脚本必须涵盖 `phase1_rfp_results.json` 中标记的所有必须满足的需求。请与以下人员核对：  
```bash
python -c "import json; rfp=json.load(open('phase1_rfp_results.json')); [print('UNCOVERED:', r) for r in rfp['must_have_requirements'] if r['coverage']=='Gap']"
```

---

### 第四阶段：概念验证（POC）与评估

**目标：** 执行结构化的概念验证，以验证解决方案的有效性。

**检查清单：**
- [ ] 明确 POC 的范围、成功标准和时间表
- [ ] 分配资源并搭建测试环境
- [ ] 分阶段进行测试（核心功能、高级功能、边缘情况）
- [ ] 根据成功标准跟踪进度
- [ ] 生成评估报告

**工具：** 运行 `poc_planner.py` 以制定完整的 POC 计划。

**模板：** 使用 `assets/poc_scorecard_template.md` 进行评估跟踪。

**输出：** POC 计划、评估报告、是否继续进行的建议。

**验证检查点：** POC 的评估得分必须在所有评估维度（功能、性能、集成、可用性、支持）上达到 60% 以上。如果得分低于 60%，请记录差距并返回第二阶段重新设计解决方案。

---

### 第五阶段：提案与收尾

**目标：** 提交支持商业决策的技术提案。

**检查清单：**
- [ ] 整理 POC 结果和成功指标
- [ ] 编写包含实施计划的技术提案
- [ ] 用证据回应未解决的问题
- [ ] 协助定价和包装方案的讨论
- [ ] 在决策后进行胜败分析

**模板：** 使用 `assets/technical_proposal_template.md` 编写提案文档。

**输出：** 技术提案、实施时间表、风险缓解计划。

---

## Python 自动化工具

### 1. RFP 响应分析器

**脚本：`scripts/rfp_response_analyzer.py`

**用途：** 解析 RFP/RFI 的需求，评估覆盖度，识别差距，并生成是否投标的建议。

**覆盖度分类：** 完全满足（100%）、部分满足（50%）、计划中（25%）、有差距（0%）。
**优先级权重：** 必须满足的需求 3 倍权重，应该满足的需求 2 倍权重，可选需求 1 倍权重。

**投标/不投标逻辑：**
- **投标：** 覆盖度 >70% 且必须满足的需求缺口 ≤3
- **条件性投标：** 覆盖度 50–70% 或必须满足的需求缺口 2–3
- **不投标：** 覆盖度 <50% 或必须满足的需求缺口 >3

**使用方法：**
```bash
python scripts/rfp_response_analyzer.py assets/sample_rfp_data.json            # human-readable
python scripts/rfp_response_analyzer.py assets/sample_rfp_data.json --format json  # JSON output
python scripts/rfp_response_analyzer.py --help
```

**输入格式：** 详见 `assets/sample_rfp_data.json` 的完整格式说明。

---

### 2. 竞争矩阵构建器

**脚本：`scripts/competitive_matrix_builder.py`

**用途：** 生成功能对比矩阵，计算竞争分数，识别差异化点和潜在风险。

**功能评分标准：** 完全满足（3 分）、部分满足（2 分）、有限满足（1 分）、未满足（0 分）。

**使用方法：**
```bash
python scripts/competitive_matrix_builder.py competitive_data.json              # human-readable
python scripts/competitive_matrix_builder.py competitive_data.json --format json  # JSON output
```

**输出内容：** 功能对比矩阵、加权竞争分数、差异化点、潜在风险及获胜策略。

---

### 3. POC 规划器

**脚本：`scripts/poc_planner.py**

**用途：** 制定包含时间表、资源分配、成功标准和评估报告的结构化 POC 计划。

**默认阶段划分：**
- **第 1 周：** 环境搭建、数据迁移、配置
- **第 2–3 周：** 核心功能测试
- **第 4 周：** 高级功能测试、性能测试、安全性测试
- **第 5 周：** 评估、生成评估报告、决策

**使用方法：**
```bash
python scripts/poc_planner.py poc_data.json              # human-readable
python scripts/poc_planner.py poc_data.json --format json  # JSON output
```

**输出内容：** 分阶段的 POC 计划、资源分配、成功标准、风险登记册以及是否继续进行的建议框架。

---

## 参考知识库

| 参考文档 | 说明 |
|-----------|-------------|
| `references/rfp-response-guide.md` | RFP/RFI 回应的最佳实践、合规性矩阵、投标/不投标框架 |
| `references/competitive-positioning-framework.md` | 竞争分析方法、竞争分析报告的编写、异议处理 |
| `references/poc-best-practices.md` | POC 规划方法、成功标准、评估框架 |

## 资产模板

| 模板 | 用途 |
|----------|---------|
| `assets/technical_proposal_template.md` | 包含执行摘要、解决方案架构、实施计划的技术提案 |
| `assets/demo_script_template.md` | 包含议程、演示要点、异议处理方式的演示脚本 |
| `assets/poc_scorecard_template.md` | 带有加权评分的 POC 评估报告 |
| `assets/sample_rfp_data.json` | 用于测试分析器的示例 RFP 数据 |
| `assets/expected_output.json` | `rfp_response_analyzer.py` 的预期输出格式 |

## 集成要点

- **市场营销技能**：利用来自 `../../marketing-skill/` 的竞争情报和信息传递框架
- **产品团队**：协调 RFP 分析中标记为“计划中”的项目
- **高层顾问**：处理需要高层参与的战略性交易
- **客户成功团队**：将 POC 结果和成功标准移交给 CSM

---

**最后更新时间：** 2026 年 2 月
**状态：** 已准备好投入生产
**使用的工具：** 3 个 Python 自动化脚本
**参考文档：** 3 份知识库文档
**模板：** 5 个资产文件