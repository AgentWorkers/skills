---
name: adi-decision-engine
description: >
  **结构化多标准决策分析（Structured Multi-Criteria Decision Analysis, MCDA）**  
  该工具用于对具有权重、约束条件、置信度的选项进行排序，并提供基于权衡分析的决策建议、敏感性分析以及可解释的决策结果。适用于以下场景：用户需要决策支持、进行多标准决策分析（MCDA）、评分与优先级排序、供应商选择、路线规划、招聘候选人筛选、工具比较、采购决策，或需要可审计的代理决策逻辑（auditable agent decision logic）。  
  **主要功能包括：**  
  1. **权重分配**：为各项标准设定合理的权重，以反映其相对重要性。  
  2. **约束条件处理**：管理各种约束条件，确保决策过程符合实际要求。  
  3. **置信度评估**：对决策结果的可靠性进行量化评估。  
  4. **权衡分析**：在多个标准之间进行综合平衡，找出最佳方案。  
  5. **敏感性分析**：分析不同参数变化对决策结果的影响。  
  6. **可解释性**：提供详细的决策过程和推荐理由，便于理解与沟通。  
  **应用场景示例：**  
  - **供应商选择**：评估不同供应商的性价比、服务质量与技术能力。  
  - **工具比较**：对比多种软件工具的性能与适用场景。  
  - **招聘决策**：根据候选人的技能、经验等因素筛选合适的人选。  
  - **采购决策**：在预算范围内选择最优的采购方案。  
  **优势：**  
  - **灵活性**：支持多种决策模型和评估方法。  
  - **可扩展性**：可根据实际需求定制分析流程和输出格式。  
  - **透明度**：提供清晰、易于理解的决策报告。  
  **适用领域：**  
  - 项目管理  
  - 人力资源管理  
  - 购买与采购  
  - 运营决策  
  - 研发与创新  
  **使用建议：**  
  - 由具备相关专业知识的人员进行数据分析与解读。  
  - 根据具体需求调整分析参数和模型设置。  
  - 定期更新分析方法以适应新情况。
homepage: https://github.com/dimgouso/adi-decision-engine_skill_openclaw
metadata: {"openclaw":{"emoji":"⚖️","requires":{"bins":["python3"],"env":[],"config":[]},"os":["darwin","linux","win32"]}}
---
# ADI 决策引擎

## 核心承诺

将复杂的权衡问题转化为结构化、可审计的多标准决策过程，并提供带有信心和解释的排名建议。

## 何时使用此技能

当用户需要结构化的决策支持而非开放式头脑风暴时，可以使用此技能。典型的应用场景包括：

- 多标准决策分析
- 权重评分或选项排序
- 供应商选择或采购
- 具有明确权衡的路线规划
- 招聘候选人排名
- 工具或平台比较
- 需要政策指导或可审计的代理决策

## 输入模式

此技能支持两种输入模式：

### 1. 结构化模式

用户已经提供了决策请求，其中包含：

- `选项`
- `标准`
- 可选的 `约束条件`
- 可选的 `政策名称`
- 可选的依据、信心度或背景信息

如果请求的质量不确定，请先使用 [scripts/validate_request.py](scripts/validate_request.py) 进行验证，然后使用 [scripts/run_adi.py](scripts/run_adi.py) 执行决策过程。

### 2. 自由格式模式

用户以自然语言描述权衡问题。首先使用 [scripts/normalize_problem.py](scripts/normalize_problem.py) 将问题转化为标准格式的请求框架。如果缺少关键信息，请要求用户补充这些信息，而不是随意设定评分或约束条件。

## 输出内容

如果 ADI 成功运行，最终输出应包括：

- **最佳选项**
- 选择该选项的简要理由
- 排名靠前的备选方案
- 信心度总结
- 约束条件的影响总结（如适用）
- 敏感性或稳定性总结（如适用）
- 明确的假设

如果请求信息不完整，应返回提示让用户补充信息，而不是直接生成排名结果。

## 工作流程

1. 判断用户输入是结构化还是自由格式的。
2. 对于自由格式的输入，使用 [scripts/normalize_problem.py](scripts/normalize_problem.py) 将其转化为标准格式的请求框架。
3. 使用 [scripts/validate_request.py](scripts/validate_request.py) 验证请求的有效性。
4. 使用 [scripts/run_adi.py](scripts/run_adi.py) 执行决策过程。
5. 以清晰、易于理解的方式呈现 ADI 的结果：
   - 首先给出推荐结果
   其次说明最主要的权衡因素
   接着说明需要注意的事项和结果的敏感性

## 决策制定规则

- 未经明确标准定义，不得对选项进行排名。
- 不得擅自设定严格的约束条件。
- 如果标准的方向不明确，请暂停并澄清。
- 在评分前，将模糊的目标转化为具体的标准。
- 优先选择简洁、明确的标准集，而非多个重叠的标准。
- 明确说明所采用的政策导向（例如：平衡性、风险规避或探索性）。

## 输出质量规则

- 首先展示最佳推荐结果。
- 解释选择该选项的原因。
- 提及最主要的权衡因素。
- 说明被排除的选项或违反约束条件的选项。
- 当依据不足时，需说明信心的不确定性。
- 在比较多个选项时，使用简洁的对比表或结构化的列表。

## 安全性和诚信原则

- 不得使用隐藏的数学公式或虚假数据。
- 不得伪造评分结果或证据。
- 如果缺少运行所需的依赖库，不得声称 ADI 已成功运行。
- 不得要求用户提供 API 密钥。
- 核心流程不需要网络访问权限。
- 如果用户提供的信息不足，不得让用户盲目信任排名结果。

## 运行环境要求

- 需要 `python3` 环境。
- 需要可导入的 `adi-decision` 包或系统路径（`PATH`）下的 `adi` 命令行工具。

如果 ADI 的运行环境不可用，应立即给出错误提示，并说明需要安装相应的依赖库。

## 参考资料

- 请求格式规范：[references/request_schema.md](references/request_schema.md)
- 结果解读指南：[references/result_interpretation.md]
- 政策指南：[references/policy_guide.md]
- 应用案例：[references/use_cases.md]

## 示例

- [examples/vendor_selection.json](examples/vendor_selection.json)（供应商选择示例）
- [examples/route_planning.json](examples/route_planning.json)（路线规划示例）
- [examples/hiring_shortlist.json](examples/hiring_shortlist.json)（招聘候选人排名示例）
- [examples/research_methods.json](examples/research_methods.json)（研究方法示例）
- [examples/tool_selection.json](examples/tool_selection.json)（工具选择示例)