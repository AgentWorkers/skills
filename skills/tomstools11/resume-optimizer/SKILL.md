---
name: resume-optimizer
description: 这款专业简历生成工具支持PDF导出、自动求职系统（ATS）优化以及简历分析功能。适用于用户需要执行以下操作的场景：  
1. 从零开始创建新的简历；  
2. 根据特定职位需求定制现有简历；  
3. 分析简历并提出改进建议；  
4. 将简历转换为适合自动求职系统（ATS）使用的PDF格式。  
该工具支持按时间顺序、按职能或结合这两种方式展示简历内容的格式。
---

# 简历优化器

生成专业的、符合ATS（ Applicant Tracking System）要求的简历，并支持PDF导出功能。

## 主要功能

1. **创建简历** - 根据用户提供的信息，使用专业的格式生成新的简历。
2. **定制简历** - 根据特定职位或用户需求对现有简历进行个性化修改。
3. **分析简历** - 审查简历并提供可操作的改进建议。
4. **导出为PDF** - 生成适合ATS系统的可下载PDF文件。

## 工作流程决策树

### 创建新简历
1. 收集用户信息（工作经验、教育背景、技能、目标职位）
2. 选择合适的格式（详见下方的格式选择指南）
3. 阅读 `references/templates.md` 以了解所选模板的信息
4. 按照 `references/best-practices.md` 中的指导内容编写简历内容
5. 使用 `scripts/generate_resume_pdf.py` 脚本生成PDF文件

### 定制现有简历
1. 查看提供的简历内容
2. 了解目标职位或用户的具体修改要求
3. 阅读 `references/ats-optimization.md` 以了解关键词整合的方法
4. 按照最佳实践进行修改
5. 生成更新后的PDF文件

### 分析简历
1. 解析简历内容
2. 根据 `references/analysis-checklist.md` 中的标准进行检查
3. 识别简历的优势和需要改进的地方
4. 提出具体、可操作的改进建议
5. （可选）协助用户实施修改

## 格式选择指南

**按时间顺序排列**（最常见）
- 适用场景：在同一领域有连贯的工作经历，职业发展路径清晰
- 最适合：大多数在同一领域持续工作的专业人士
- 参考资料：`references/templates.md` → “按时间顺序排列的模板”部分

**按职能分类**  
- 适用场景：职业转换者、有就业空档的人，需要突出可转移技能的人
- 最适合：重返职场的人或具有跨领域工作经验的人
- 参考资料：`references/templates.md` → “按职能分类的模板”部分

**组合格式**  
- 适用场景：需要在技能和职业发展之间取得平衡的职场人士  
- 最适合：具备多样化技能且有过相关工作经验的职业转换者  
- 参考资料：`references/templates.md` → “组合格式的模板”部分

## PDF生成

使用提供的脚本生成专业的PDF文件：

```bash
python3 scripts/generate_resume_pdf.py \
  --input resume_content.json \
  --output resume.pdf \
  --format chronological
```

该脚本使用 `reportlab` 库生成符合ATS系统的PDF文件，具备以下特点：
- 专业的排版（使用Helvetica字体）
- 合适的页边距和间距（四周均为0.75英寸）
- 清晰的章节标题  
- 项目符号格式  
- 一致的视觉层次结构

## 必读参考资料

在创建任何简历之前，请阅读：
1. `references/best-practices.md` - 简历撰写的基本原则
2. `references/ats-optimization.md` - 符合ATS系统的要求
3. `references/templates.md` - 各格式对应的模板文档

在分析简历之前，请阅读：
1. `references/analysis-checklist.md` - 评估标准和评分方法

## 快速入门示例

**创建简历：**
```
User: "Help me build a resume. I have 5 years in marketing."

Steps:
1. Gather: Current role, key achievements, education, certifications
2. Format: Chronological (clear progression in same field)
3. Build: Use template from references/templates.md
4. Keywords: Integrate from job description per ats-optimization.md
5. Export: Generate PDF to /mnt/user-data/outputs/
```

**针对特定职位进行定制：**
```
User: "Tailor my resume for this job [job description]"

Steps:
1. Parse job description for required skills/keywords
2. Identify gaps between resume and requirements
3. Reorder bullets to lead with relevant achievements
4. Integrate keywords naturally throughout
5. Update summary to mirror key requirements
6. Generate updated PDF
```

**分析简历：**
```
User: "Review my resume and tell me how to improve it"

Steps:
1. Read references/analysis-checklist.md
2. Evaluate each section against criteria
3. Score: Content, Format, ATS-compatibility
4. Identify top 3-5 priority improvements
5. Provide specific rewrite examples
6. Offer to implement changes
```

## 输出要求

所有生成的简历必须满足以下要求：
- 保存在 `/mnt/user-data/outputs/` 目录中，以便用户下载
- 文件名格式为 `FirstName_LastName_Resume.pdf`
- 使用 `computer://` 协议提供下载链接
- 遵循ATS系统的格式要求（不得使用表格、文本框或图形）

## 代码风格规范

在编写用于生成PDF的Python脚本时，请遵循以下规范：
- 使用 `reportlab` 库生成PDF文件
- 保持代码简洁且功能性强
- 优雅地处理错误
- 在交付给用户之前先测试输出结果