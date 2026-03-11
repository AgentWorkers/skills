---
name: "prompt-engineer-toolkit"
description: "分析并优化用于生成AI内容的提示语句；创建可重复使用的提示模板，以应用于营销场景（如广告文案、电子邮件活动、社交媒体内容等）；同时构建端到端的AI内容工作流程。适用于用户希望提升AI辅助营销的提示效果、构建提示模板或优化AI内容工作流程的情况。当用户提到“提示工程（Prompt Engineering）”、“改进我的提示（Improve my prompts）”、“AI写作质量（AI Writing Quality）”、“提示模板（Prompt Templates）”或“AI内容工作流程（AI Content Workflow）”时，也可使用该服务。"
license: MIT
metadata:
  version: 1.0.0
  author: Alireza Rezvani
  category: marketing
  updated: 2026-03-06
---
# Prompt Engineer Toolkit

## 概述

该工具用于将提示（prompts）从临时草稿转换为可进行重复测试、版本控制及回归测试的生产环境资产。它强调可量化的质量标准，而非仅依赖直觉。在以下情况下应使用该工具：新的大型语言模型（LLM）功能需要可靠的结果时；模型或指令更改后提示质量下降时；多个团队成员同时编辑提示时需要记录历史变更情况；需要基于证据的提示选择以用于生产环境发布时；或者希望在不同环境中保持提示管理的统一性时。

## 核心功能

- **A/B提示评估**：针对结构化测试用例对提示进行评估。
- **定量评分**：对提示的准确性、相关性和安全性进行检查。
- **提示版本管理**：支持不可变的版本历史记录和变更日志。
- **提示差异对比**：便于审查影响模型行为的修改。
- **可重用的提示模板**：提供提示模板和选择指导。
- **回归测试友好型工作流程**：支持模型和提示的更新过程。

## 关键工作流程

### 1. 运行A/B提示测试

准备JSON测试用例并执行测试：

```bash
python3 scripts/prompt_tester.py \
  --prompt-a-file prompts/a.txt \
  --prompt-b-file prompts/b.txt \
  --cases-file testcases.json \
  --runner-cmd 'my-llm-cli --prompt {prompt} --input {input}' \
  --format text
```

输入数据也可以通过标准输入（stdin）或`--input`参数提供的JSON格式提供。

### 2. 基于证据选择最佳提示

测试人员会对每个测试用例的输出进行评分，并汇总以下指标：
- 预期内容的覆盖情况
- 禁止的内容违规情况
- 正则表达式/格式的合规性
- 输出长度的合理性

选择得分较高的提示作为候选基线版本，然后运行回归测试套件。

### 3. 提示版本管理

```bash
# Add version
python3 scripts/prompt_versioner.py add \
  --name support_classifier \
  --prompt-file prompts/support_v3.txt \
  --author alice

# Diff versions
python3 scripts/prompt_versioner.py diff --name support_classifier --from-version 2 --to-version 3

# Changelog
python3 scripts/prompt_versioner.py changelog --name support_classifier
```

### 4. 回归测试循环

1. 存储基线版本。
2. 提出提示修改建议。
3. 重新运行A/B测试。
4. 仅在得分和安全性指标改善的情况下才推广新版本。

## 脚本接口

- `python3 scripts/prompt_tester.py --help`
  - 从标准输入或`--input`参数读取提示/测试用例。
  - 支持外部运行器命令。
  - 输出文本或JSON格式的测试结果。
- `python3 scripts/prompt_versioner.py --help`
  - 管理提示的历史记录（添加、列出、比较差异、生成变更日志）。
  - 本地存储元数据和内容快照。

## 常见问题、最佳实践及审查清单

**避免以下错误：**
1. 仅根据单个测试用例的结果选择提示——应使用包含多种边缘情况的测试套件。
2. 同时修改提示和模型——务必隔离各个变量。
3. 评估标准中缺少“禁止包含”的检查项。
4. 修改提示时未记录版本元数据、作者或修改理由。
5. 在部署新提示版本前未进行语义差异对比。
6. 优化某个测试指标的同时损害了边缘情况的处理能力——需跟踪整个测试套件的表现。
7. 更换模型后未重新运行基线A/B测试。

**在推广任何提示版本之前，请确认：**
- 任务意图明确且无歧义。
- 输出格式和结构已明确界定。
- 安全性和禁止内容的要求已明确。
- 指令之间没有矛盾。
- 代码中不存在不必要的冗余内容。
- A/B测试的得分有所提升，且违规项数量保持为零。

## 参考资料

- [references/prompt-templates.md](references/prompt-templates.md)
- [references/technique-guide.md](references/technique-guide.md)
- [references/evaluation-rubric.md](references/evaluation-rubric.md)
- [README.md](README.md)

## 评估设计

每个测试用例应定义以下内容：
- `input`：模拟实际生产环境的输入数据。
- `expected_contains`：必须包含的标记或内容。
- `forbidden_contains`：禁止使用的短语或不安全的内容。
- `expected_regex`：必须符合的结构模式。

这样的设计确保了对不同提示版本的评估具有确定性。

## 版本控制策略

- 为每个功能使用唯一的语义提示标识符（如`support_classifier`、`ad_copy_shortform`）。
- 记录每次修改的作者和修改说明。
- 绝不覆盖历史版本。
- 在将新提示推广到生产环境之前，先进行差异对比。

## 推广策略

1. 创建基线提示版本。
2. 提出候选提示版本。
3. 使用相同的测试用例重新运行A/B测试。
4. 仅在候选版本的表现优于基线版本且违规项数量保持为零的情况下才进行推广。
5. 跟踪发布后的用户反馈，并将新的故障情况纳入测试套件中。