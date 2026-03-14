---
name: authorship-credit-gen
description: >
  **用途：**  
  用于确定研究论文的作者顺序、为CRediT贡献者分配角色以提高透明度、记录个人在协作项目中的贡献，或在多机构研究项目中解决作者身份争议。该工具遵循ICMJE（国际医学期刊编辑委员会）指南和CRediT分类体系，生成公平、透明的作者署名安排。它有助于研究团队记录贡献、解决争议，并确保学术出版物中的贡献得到公正的认可。
allowed-tools: "Read Write Bash Edit"
license: MIT
metadata:
  skill-author: AIPOCH
  version: "1.0"
---
# 研究作者署名与贡献者信用生成工具

## 适用场景

- 确定研究论文中的作者排序  
- 为贡献者分配 CRediT 角色以提高透明度  
- 记录个人在协作项目中的贡献  
- 解决多机构研究中的作者署名争议  
- 为期刊投稿准备贡献者声明  
- 评估研究团队中各成员的贡献比例  

## 快速入门  

```python
from scripts.main import AuthorshipCreditGen

# Initialize the tool
tool = AuthorshipCreditGen()

from scripts.authorship_credit import AuthorshipCreditGenerator

generator = AuthorshipCreditGenerator(guidelines="ICMJEv4")

# Document contributions
contributions = {
    "Dr. Sarah Chen": [
        "Conceptualization",
        "Methodology", 
        "Writing - Original Draft",
        "Supervision"
    ],
    "Dr. Michael Roberts": [
        "Data Curation",
        "Formal Analysis",
        "Writing - Review & Editing"
    ],
    "Dr. Lisa Zhang": [
        "Investigation",
        "Resources",
        "Validation"
    ]
}

# Generate fair authorship order
authorship = generator.determine_order(
    contributions=contributions,
    criteria=["intellectual_input", "execution", "writing", "supervision"],
    weights={"intellectual_input": 0.4, "execution": 0.3, "writing": 0.2, "supervision": 0.1}
)

print(f"First author: {authorship.first_author}")
print(f"Corresponding: {authorship.corresponding_author}")
print(f"Author order: {authorship.ordered_list}")

# Generate CRediT statement
credit_statement = generator.generate_credit_statement(
    contributions=contributions,
    format="journal_submission"
)

# Check for disputes
dispute_check = generator.check_equity_issues(authorship)
if dispute_check.has_issues:
    print(f"Recommendations: {dispute_check.recommendations}")
```  

## 核心功能  

### 1. 生成公平的作者排序  

使用加权标准分析贡献情况，以确定合理的作者排名。  
```python
# Define weighted contribution criteria
weights = {
    "conceptualization": 0.25,
    "methodology_design": 0.20,
    "data_collection": 0.15,
    "analysis": 0.15,
    "manuscript_writing": 0.15,
    "supervision": 0.10
}

# Calculate contribution scores
scores = tool.calculate_contribution_scores(
    contributions=team_contributions,
    weights=weights
)

# Generate ordered author list
authorship_order = tool.generate_author_order(scores)
print(f"Recommended order: {authorship_order}")
```  

### 2. 分配 CRediT 角色  

将贡献者角色与官方的 CRediT 分类标准（Contributor Roles Taxonomy）进行匹配。  
```python
# Map contributions to CRediT roles
credit_roles = tool.assign_credit_roles(
    contributions=contributions,
    version="CRediT_2021"
)

# Generate CRediT statement for journal
statement = tool.generate_credit_statement(
    roles=credit_roles,
    format="JATS_XML"
)

# Validate role assignments
validation = tool.validate_credit_roles(credit_roles)
if validation.is_valid:
    print("CRediT roles properly assigned")
```  

### 3. 识别贡献不均衡问题  

在论文提交前发现潜在的作者署名争议。  
```python
# Analyze contribution distribution
equity_analysis = tool.analyze_equity(
    contributions=contributions,
    thresholds={"min_substantial": 0.15}
)

# Flag potential issues
if equity_analysis.has_inequities:
    for issue in equity_analysis.issues:
        print(f"Warning: {issue.description}")
        print(f"Recommendation: {issue.recommendation}")

# Generate equity report
report = tool.generate_equity_report(equity_analysis)
```  

### 4. 生成符合期刊要求的贡献者声明  

根据不同期刊的要求，生成格式化的贡献者声明。  
```python
# Generate for Nature-style statement
nature_statement = tool.generate_contributor_statement(
    style="Nature",
    include_competing_interests=True
)

# Generate for Science-style statement  
science_statement = tool.generate_contributor_statement(
    style="Science",
    include_author_contributions=True
)

# Export in multiple formats
tool.export_statement(
    statement=nature_statement,
    formats=["docx", "pdf", "txt"]
)
```  

## 命令行使用方法  

```bash
python scripts/main.py --contributions contributions.json --guidelines ICMJE --output authorship_order.json
```  

## 最佳实践  

- 在项目开始时明确作者署名的相关要求  
- 在整个项目过程中持续记录贡献情况  
- 在提交前审查并确定作者排序  
- 将非作者贡献者纳入致谢名单中  

## 质量检查清单  

使用此工具前，请确保：  
- [ ] 明确了解使用目的  
- [ ] 准备并验证了所需的输入数据  
- [ ] 明确了输出格式要求  
- [ ] 查阅了相关文档  

使用此工具后，请确认：  
- [ ] 结果符合质量标准  
- [ ] 输出格式正确  
- [ ] 所有错误或警告均已得到处理  
- [ ] 结果已得到妥善记录  

## 参考资料  

- `references/guide.md` - 完整的用户指南  
- `references/examples/` - 可运行的代码示例  
- `references/api-docs/` - 完整的 API 文档  

---

**技能 ID**: 766 | **版本**: 1.0 | **许可证**: MIT