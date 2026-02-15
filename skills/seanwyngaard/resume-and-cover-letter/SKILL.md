---
name: resume-and-cover-letter
description: 生成针对特定职位描述优化的 ATS（ Applicant Tracking System）格式简历和定制的求职信。适用于制作简历、个人简历（CV）、求职信或职业相关文件时使用。
argument-hint: "[job-description-or-url]"
allowed-tools: Read, Write, Edit, Grep, Glob, Bash
---

# 简历与求职信生成器

该工具能够生成符合特定职位要求的、经过ATS（ Applicant Tracking System）优化过的简历和定制化的求职信。简历会突出显示相关的工作经验，使用恰当的关键词，并支持多种输出格式。

## 使用方法

```
/resume-and-cover-letter "Senior Frontend Developer at Stripe — React, TypeScript, 5+ years..."
/resume-and-cover-letter job-posting.txt --profile my-experience.md
/resume-and-cover-letter "Product Manager role" --resume existing-resume.md --tailor
```

请提供以下信息：
1. 职位描述（直接粘贴或提供文件路径）
2. 您的工作经验/个人资料（直接粘贴、提供文件路径，或上传现有的简历以供生成）

如果未提供个人资料或简历，系统会交互式地询问您所需的关键信息。

## 简历生成流程

### 第一步：解析职位描述

提取以下内容：
- **职位名称**及职位级别（初级、中级、高级、主管、总监）
- **必备技能**（硬性要求与加分项）
- **主要职责**
- **行业/领域相关的关键词**
- **公司价值观及企业文化**
- **ATS系统中使用的关键词**（需与职位描述完全一致）

### 第二步：收集候选人信息

如果未提供相关信息，系统会要求您提供以下内容：
- 姓名、联系方式、所在地区、LinkedIn个人主页链接
- 工作经验（公司名称、职位、工作时长、取得的成就）
- 教育背景
- 技术技能
- 持有的证书
- 代表性的项目经历

### 第三步：关键词匹配

将候选人的工作经验与职位要求进行对比：

```
KEYWORD MATCH REPORT
═══════════════════
✅ Matched (use these prominently):
   - React (mentioned 3x in JD, candidate has 4 years)
   - TypeScript (required, candidate proficient)
   - REST APIs (mentioned 2x, candidate built several)

⚠️ Partial Match (reframe experience):
   - GraphQL (required, candidate has basic experience)
   - CI/CD (mentioned, candidate has "deployment automation" experience)

❌ Gap (address in cover letter):
   - Kubernetes (nice-to-have, candidate hasn't used directly)

📊 Overall Match: 78%
```

### 第四步：生成简历

简历采用以下结构（按时间倒序排列，符合ATS系统的格式）：

```
[FULL NAME]
[City, State] | [Email] | [Phone] | [LinkedIn URL] | [Portfolio URL]

═══════════════════════════════════════════
PROFESSIONAL SUMMARY
═══════════════════════════════════════════
[2-3 sentences: years of experience + key skills + biggest achievement
 Mirror the job title and top 3 keywords from the JD]

═══════════════════════════════════════════
EXPERIENCE
═══════════════════════════════════════════
[Job Title] | [Company Name]
[Start Date] – [End Date] | [Location]

• [Achievement verb] + [what you did] + [quantified result]
• [Achievement verb] + [what you did] + [quantified result]
• [Achievement verb] + [what you did] + [quantified result]
• [Achievement verb] + [what you did] + [quantified result]

[Repeat for each role — max 3-4 roles, most recent first]

═══════════════════════════════════════════
SKILLS
═══════════════════════════════════════════
Languages: [list]
Frameworks: [list]
Tools: [list]
Other: [list]

═══════════════════════════════════════════
EDUCATION
═══════════════════════════════════════════
[Degree] in [Field] | [University] | [Year]

═══════════════════════════════════════════
CERTIFICATIONS (if applicable)
═══════════════════════════════════════════
[Certification Name] | [Issuer] | [Year]
```

**简历撰写规则**：
1. 每个项目描述都以强烈的动词开头（例如：构建、领导、减少、提高、设计、实施、自动化、优化、发布）
2. 所有数据均需量化：例如：“将加载时间减少了40%”，“管理了一个8人的团队”，“每天处理超过1000万条记录”
3. 严格遵循职位描述中的语言表述：如果职位描述中使用了“跨部门协作”这样的表述，简历中也必须使用相同的表达
4. 避免使用代词：“I” —— 简历中的项目描述通常以第三人称形式呈现
5. 根据重要性对成就进行排序：每个职位下应先列出最相关的成就
6. **篇幅要求**：工作经验不足10年的简历不超过1页；高级职位的简历最多不超过2页
7. 简历中不得包含图形、表格、列或页眉/页脚——这些内容ATS系统无法识别
8. 使用标准的项目名称：例如使用“工作经验”而非“职业历程”，“技能”而非“工具集”

### 第五步：生成求职信

```
[Your Name]
[Your Email] | [Your Phone]
[Date]

[Hiring Manager Name or "Hiring Team"]
[Company Name]

Dear [Name/Hiring Team],

PARAGRAPH 1 — THE HOOK (2-3 sentences)
[Why you're excited about THIS specific role at THIS specific company.
Reference something specific: a product feature, company value, recent news.
Don't be generic.]

PARAGRAPH 2 — THE PROOF (3-5 sentences)
[Your most relevant achievement that directly maps to their top requirement.
Use the STAR format: Situation, Task, Action, Result.
Include a quantified result.]

PARAGRAPH 3 — THE FIT (2-3 sentences)
[Why you're a match for their culture/team.
Address any secondary requirements.
Show you understand their challenges.]

PARAGRAPH 4 — THE CLOSE (2 sentences)
[Express enthusiasm. Suggest next step.
"I'd welcome the chance to discuss how my experience with [X]
can help [Company] achieve [Y]. I'm available for a call at your convenience."]

Sincerely,
[Your Name]
```

**求职信撰写规则**：
- 字数控制在350字以内（约3/4页）
- 求职信内容不应与简历重复，应重点阐述1-2项突出的成就
- 在求职信中提及公司名称及具体细节，以证明您不是发送通用模板
- 如被询问，需诚实地说明职业空白期（如跳槽或失业期）
- 保持与公司的沟通风格一致（初创公司采用非正式语气，大型企业则采用正式语气）

### 第六步：输出结果

将生成的文件保存到 `output/career-docs/` 目录下：

```
output/career-docs/
  resume.md               # Clean Markdown
  resume.html             # Print-ready HTML with clean styling
  resume.tex              # LaTeX source (optional, for PDF generation)
  cover-letter.md         # Markdown
  cover-letter.html       # Print-ready HTML
  keyword-match-report.md # Gap analysis
  README.md               # Notes on customization
```

生成的HTML文件应具备以下特点：
- 简洁专业的设计风格（无颜色、设计元素极少）
- 适合打印的CSS样式（使用 `@media print` 规则）
- 使用标准字体（Georgia、Arial或系统默认字体）
- 打印时保持适当的页边距（四周0.75英寸）

### 第七步：向用户展示结果

向用户展示以下内容：
1. 关键词匹配报告（哪些内容与职位描述匹配，哪些需要改进）
- 简历预览（前几部分内容）
- 求职信预览
- 文件存放位置
- 改进建议（建议补充哪些技能或证书）