---
name: "skill-tester"
description: "技能测试器（Skill Tester）"
---
# 技能测试器 (Skill Tester)

---

**名称**: skill-tester  
**级别**: 强大级 (POWERFUL)  
**类别**: 工程质量保证 (Engineering Quality Assurance)  
**依赖项**: 无（仅依赖 Python 标准库）  
**作者**: Claude Skills 工程团队 (Claude Skills Engineering Team)  
**版本**: 1.0.0  
**最后更新**: 2026-02-16  

---

## 描述  

技能测试器 (Skill Tester) 是一个全面的元技能 (meta-skill)，用于验证、测试并评估 claude-skills 生态系统中各项技能的质量。这一强大的质量保证工具通过自动化验证、测试和评分机制，确保所有技能符合 BASIC、STANDARD 和 POWERFUL 级别的严格要求。  

作为技能质量的把关系统，该元技能具备以下三大核心功能：  
1. **结构验证**：确保技能遵循规定的目录结构、文件格式和文档规范。  
2. **脚本测试**：验证 Python 脚本的语法、导入依赖项、功能及输出格式是否符合标准。  
3. **质量评分**：从多个维度对技能进行综合评估，并给出字母等级及改进建议。  

该技能对于维护生态系统的统一性、实现自动化持续集成/持续交付 (CI/CD) 流程，以及支持手动和自动化的质量保证工作流程至关重要。它是预提交钩子 (pre-commit hooks)、拉取请求验证 (pull request validation) 和持续集成流程的基础，有助于保持 claude-skills 仓库的高质量标准。  

## 核心特性  

### 全面技能验证  
- **结构合规性**：验证目录结构、必备文件（SKILL.md、README.md、脚本文件、参考文档、资源文件、预期输出文件等）是否齐全。  
- **文档规范**：检查 SKILL.md 的前置内容、各部分的完整性，以及不同级别所需的最低行数。  
- **文件格式验证**：确保 Markdown 格式正确、YAML 前置内容的语法规范以及文件命名规则符合要求。  

### 高级脚本测试  
- **语法验证**：在执行前编译 Python 脚本以检测语法错误。  
- **导入依赖分析**：仅允许使用标准库，识别外部依赖项。  
- **运行时测试**：使用示例数据执行脚本，验证 `argparse` 的实现方式及 `--help` 功能。  
- **输出格式合规性**：验证输出格式是否支持 JSON 和人类可读格式，并确保错误处理正确。  

### 多维度质量评分  
- **文档质量（25%）**：SKILL.md 的内容深度和完整性、README 的清晰度、参考文档的质量。  
- **代码质量（25%**：脚本的复杂性、错误处理的稳健性、输出格式的一致性。  
- **完整性（25%**：必备文件的齐全性、示例数据的充分性、预期输出的准确性。  
- **可用性（25%**：示例的清晰度、`argparse` 帮助文本的质量、安装的便捷性、用户体验。  

### 级别分类系统  
根据技能的复杂性和功能自动对其进行分类：  

#### BASIC 级别要求  
- SKILL.md 文件至少 100 行。  
- 至少包含 1 个 Python 脚本（代码量 100–300 行）。  
- 基本的 `argparse` 实现。  
- 简单的输入/输出处理。  
- 基本的文档覆盖。  

#### STANDARD 级别要求  
- SKILL.md 文件至少 200 行。  
- 包含 1–2 个 Python 脚本（每个脚本代码量 300–500 行）。  
- 具备子命令的高级 `argparse` 实现。  
- 支持 JSON 和文本两种输出格式。  
- 提供详细的示例和参考文档。  
- 具备错误处理和边缘情况处理能力。  

#### POWERFUL 级别要求  
- SKILL.md 文件至少 300 行。  
- 包含 2–3 个 Python 脚本（每个脚本代码量 500–800 行）。  
- 具备多种模式的复杂 `argparse` 实现。  
- 输出格式和验证机制较为复杂。  
- 提供详尽的文档和参考资料。  
- 具备高级的错误处理和恢复机制。  
- 支持持续集成/持续交付 (CI/CD) 功能。  

## 架构与设计  

### 模块化设计理念  
技能测试器采用模块化架构，每个组件负责特定的验证任务：  
- **skill-validator.py**：核心的结构和文档验证引擎。  
- **script_tester.py**：运行时测试和执行验证框架。  
- **quality_scorer.py**：多维度质量评估和评分系统。  

### 标准执行  
所有验证操作均依据 `references/` 目录中定义的明确标准进行：  
- **技能结构规范**：规定必备和可选的组件。  
- **级别要求矩阵**：详细列出每个级别的要求。  
- **质量评分标准**：全面的评分方法和权重设置。  

### 集成能力  
该工具设计用于无缝集成到现有的开发工作流程中：  
- **预提交钩子**：防止不符合标准的技能被提交。  
- **CI/CD 流程**：在拉取请求过程中自动执行质量检查。  
- **手动验证**：提供交互式的命令行工具用于开发过程中的验证。  
- **批量处理**：能够批量验证和评分现有的技能仓库。  

## 实现细节  

### skill-validator.py 的核心功能  
```python
# Primary validation workflow
validate_skill_structure() -> ValidationReport
check_skill_md_compliance() -> DocumentationReport  
validate_python_scripts() -> ScriptReport
generate_compliance_score() -> float
```  

主要验证内容包括：  
- 解析和验证 SKILL.md 的前置内容。  
- 确保包含必要的章节（如描述、功能、使用方法等）。  
- 检查每个级别所需的最低行数。  
- 验证 Python 脚本的 `argparse` 实现。  
- 确保仅使用标准库进行导入。  
- 验证目录结构是否符合规范。  
- 评估 README.md 的质量。  

### script_tester.py 的测试框架  
```python
# Core testing functions
syntax_validation() -> SyntaxReport
import_validation() -> ImportReport
runtime_testing() -> RuntimeReport
output_format_validation() -> OutputReport
```  

测试功能包括：  
- 基于 Python 解释器抽象树 (AST) 的语法验证。  
- 分析导入语句并检测外部依赖项。  
- 控制脚本的执行过程并设置超时保护。  
- 验证 `argparse` 的 `--help` 功能。  
- 处理示例数据并验证输出结果。  
- 比较实际输出与预期输出并报告差异。  

### quality_scorer.py 的评分系统  
```python
# Multi-dimensional scoring
score_documentation() -> float  # 25% weight
score_code_quality() -> float   # 25% weight
score_completeness() -> float   # 25% weight
score_usability() -> float      # 25% weight
calculate_overall_grade() -> str # A-F grade
```  

评分维度包括：  
- **文档质量**：内容的完整性、清晰度、示例的详细程度、参考文档的质量。  
- **代码质量**：脚本的复杂性、错误处理的稳健性、输出格式的一致性。  
- **完整性**：必备文件的齐全性、示例数据的充分性、预期输出的准确性。  
- **可用性**：帮助文本的质量、示例的清晰度、安装的便捷性。  

## 使用场景  

### 集成到开发工作流程中  
```bash
# Pre-commit hook validation
skill_validator.py path/to/skill --tier POWERFUL --json

# Comprehensive skill testing
script_tester.py path/to/skill --timeout 30 --sample-data

# Quality assessment and scoring
quality_scorer.py path/to/skill --detailed --recommendations
```  

### 集成到 CI/CD 流程中  
```yaml
# GitHub Actions workflow example
- name: "validate-skill-quality"
  run: |
    python skill_validator.py engineering/${{ matrix.skill }} --json | tee validation.json
    python script_tester.py engineering/${{ matrix.skill }} | tee testing.json
    python quality_scorer.py engineering/${{ matrix.skill }} --json | tee scoring.json
```  

### 批量分析仓库  
```bash
# Validate all skills in repository
find engineering/ -type d -maxdepth 1 | xargs -I {} skill_validator.py {}

# Generate repository quality report
quality_scorer.py engineering/ --batch --output-format json > repo_quality.json
```  

## 输出格式与报告  

### 双重输出支持  
所有工具均提供人类可读和机器可解析的输出格式：  

#### 人类可读格式  
```
=== SKILL VALIDATION REPORT ===
Skill: engineering/example-skill
Tier: STANDARD
Overall Score: 85/100 (B)

Structure Validation: ✓ PASS
├─ SKILL.md: ✓ EXISTS (247 lines)
├─ README.md: ✓ EXISTS  
├─ scripts/: ✓ EXISTS (2 files)
└─ references/: ⚠ MISSING (recommended)

Documentation Quality: 22/25 (88%)
Code Quality: 20/25 (80%)
Completeness: 18/25 (72%)
Usability: 21/25 (84%)

Recommendations:
• Add references/ directory with documentation
• Improve error handling in main.py
• Include more comprehensive examples
```  

#### JSON 格式  
```json
{
  "skill_path": "engineering/example-skill",
  "timestamp": "2026-02-16T16:41:00Z",
  "validation_results": {
    "structure_compliance": {
      "score": 0.95,
      "checks": {
        "skill_md_exists": true,
        "readme_exists": true,
        "scripts_directory": true,
        "references_directory": false
      }
    },
    "overall_score": 85,
    "letter_grade": "B",
    "tier_recommendation": "STANDARD",
    "improvement_suggestions": [
      "Add references/ directory",
      "Improve error handling",
      "Include comprehensive examples"
    ]
  }
}
```  

## 质量保证标准  

### 代码质量要求  
- **仅使用标准库**：不允许使用外部依赖包（如 pip 包）。  
- **错误处理**：具备详细的异常处理机制和有意义的错误信息。  
- **输出一致性**：输出格式统一，采用标准化的 JSON 格式。  
- **性能**：验证算法高效，执行时间合理。  
- **可维护性**：代码结构清晰，适当添加类型提示。  

### 测试标准  
- **自我测试**：技能测试器能够自我验证（元验证）。  
- **样本数据覆盖**：涵盖边缘情况和错误条件的全面测试用例。  
- **预期输出验证**：所有样本运行都能产生可验证、可复制的输出结果。  
- **超时保护**：对可能存在问题的脚本设置超时限制，确保安全执行。  

### 文档标准  
- **全面覆盖**：所有函数、类和模块都有相应的文档说明。  
- **使用示例**：为所有用例提供清晰、实用的示例。  
- **集成指南**：提供详细的 CI/CD 和工作流程集成步骤。  
- **参考资料**：包含标准和要求的完整规范文档。  

## 集成示例  

### 预提交钩子设置  
```bash
#!/bin/bash
# .git/hooks/pre-commit
echo "Running skill validation..."
python engineering/skill-tester/scripts/skill_validator.py engineering/new-skill --tier STANDARD
if [ $? -ne 0 ]; then
    echo "Skill validation failed. Commit blocked."
    exit 1
fi
echo "Validation passed. Proceeding with commit."
```  

### GitHub Actions 工作流程  
```yaml
name: "skill-quality-gate"
on:
  pull_request:
    paths: ['engineering/**']

jobs:
  validate-skills:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: "setup-python"
        uses: actions/setup-python@v4
        with:
          python-version: '3.11'
      - name: "validate-changed-skills"
        run: |
          changed_skills=$(git diff --name-only ${{ github.event.before }} | grep -E '^engineering/[^/]+/' | cut -d'/' -f1-2 | sort -u)
          for skill in $changed_skills; do
            echo "Validating $skill..."
            python engineering/skill-tester/scripts/skill_validator.py $skill --json
            python engineering/skill-tester/scripts/script_tester.py $skill
            python engineering/skill-tester/scripts/quality_scorer.py $skill --minimum-score 75
          done
```  

### 持续质量监控  
```bash
#!/bin/bash
# Daily quality report generation
echo "Generating daily skill quality report..."
timestamp=$(date +"%Y-%m-%d")
python engineering/skill-tester/scripts/quality_scorer.py engineering/ \
  --batch --json > "reports/quality_report_${timestamp}.json"

echo "Quality trends analysis..."
python engineering/skill-tester/scripts/trend_analyzer.py reports/ \
  --days 30 > "reports/quality_trends_${timestamp}.md"
```  

## 性能与可扩展性  

### 执行性能  
- **快速验证**：每个技能的验证耗时少于 1 秒。  
- **高效测试**：脚本测试具有超时保护功能（可配置，默认超时时间为 30 秒）。  
- **批量处理**：支持并行处理，适用于大规模仓库的分析。  
- **内存效率**：适用于大型仓库分析，占用内存极少。  

### 可扩展性考虑  
- **仓库规模**：适用于包含 100 多个技能的仓库。  
- **并发执行**：线程安全的实现支持并行验证。  
- **资源管理**：自动清理临时文件和子进程资源。  
- **配置灵活性**：可配置超时时间、内存限制和验证严格程度。  

## 安全性与安全性  

### 安全执行环境  
- **沙箱测试**：脚本在受控环境中执行，并具有超时保护。  
- **资源限制**：监控内存和 CPU 使用情况，防止资源耗尽。  
- **输入验证**：所有输入在处理前都经过清洗和验证。  
- **无网络访问**：离线操作，避免外部依赖或网络调用。  

### 安全最佳实践  
- **无代码注入**：仅进行静态分析，不生成动态代码。  
- **路径遍历保护**：通过路径验证确保文件系统访问的安全性。  
- **最小权限**：以最低权限运行，仅访问必要的文件系统资源。  
- **审计日志**：记录详细的日志，便于安全监控和故障排查。  

## 故障排除与支持  

### 常见问题及解决方法  

#### 验证失败  
- **文件缺失**：检查目录结构是否符合级别要求。  
- **导入错误**：确保仅使用标准库的导入依赖项。  
- **文档问题**：验证 SKILL.md 的前置内容和各部分的完整性。  

#### 脚本测试问题  
- **超时错误**：增加超时限制或优化脚本性能。  
- **执行失败**：检查脚本的语法和导入语句的正确性。  
- **输出格式问题**：确保输出格式正确且支持双重输出。  

#### 评分差异  
- **评分过低**：重新查看评分标准和改进建议。  
- **级别分类错误**：根据级别要求重新验证技能的复杂性。  
- **结果不一致**：检查质量标准或评分权重的最新变更。  

### 调试支持  
- **详细日志**：提供详细的日志记录和执行跟踪信息。  
- **干运行模式**：提供无需执行的调试模式。  
- **调试输出**：提供包含文件位置和改进建议的详细错误报告。  

## 未来改进计划  

### 计划中的功能  
- **机器学习质量预测**：利用历史数据进行智能质量评估。  
- **性能基准测试**：跟踪各技能的执行时间和资源使用情况。  
- **依赖项分析**：自动检测和验证技能之间的依赖关系。  
- **质量趋势分析**：跟踪历史质量变化和异常情况。  

### 集成路线图  
- **集成到 IDE 中**：在流行的开发环境中实现实时验证。  
- **Web 仪表板**：提供集中式的质量监控和报告界面。  
- **API 接口**：提供 RESTful API 用于外部集成和自动化。  
- **通知系统**：在质量下降或验证失败时自动发送警报。  

## 结论  

技能测试器是维护 claude-skills 生态系统高质量标准的关键基础设施组件。它通过提供全面的验证、测试和评分功能，确保所有技能符合或超过各自级别的严格要求。  

该元技能不仅充当质量把关的角色，还指导技能开发者遵循最佳实践，并帮助维护整个仓库的一致性。凭借其集成能力和全面的报告功能，它支持手动和自动化的质量保证工作流程，能够随着 claude-skills 生态系统的不断发展而持续进化。  

结构验证、运行时测试和多维度质量评分的结合，为技能质量提供了无与伦比的透明度，同时保持了应对不同技能类型和复杂性的灵活性。随着 claude-skills 仓库的持续增长，技能测试器将继续作为质量保证和生态系统完整性的基石。