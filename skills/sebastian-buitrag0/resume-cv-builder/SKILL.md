---
name: resume-cv-builder
description: 创建专业的简历（Resume）和求职信（CV）。支持生成适用于自动招聘系统（ATS）的格式，优化列表项（bullets），根据具体职位进行定制，并能导出为多种格式（Markdown、HTML、LaTeX、PDF）。
homepage: https://github.com/your-username/resume-builder-skill
metadata: {"clawdbot":{"emoji":"📄","requires":{"bins":["pandoc"],"env":[]}}}
---

# 简历/简历生成工具技能

可以直接使用Clawdbot创建专业的、符合ATS（自动招聘系统）要求的简历和求职信。

## 快速入门

请告诉我：
- “为软件工程师职位创建一份简历”
- “优化我的简历以适应ATS系统”
- “将我的简历转换为PDF格式”
- “根据这份职位描述（[粘贴职位描述]）定制我的简历”

## 简历结构

### 推荐的标准部分顺序

```markdown
# FULL NAME
Contact Info | LinkedIn | GitHub | Portfolio

## PROFESSIONAL SUMMARY
2-3 sentences highlighting key qualifications

## SKILLS
Technical Skills | Soft Skills | Tools | Languages

## EXPERIENCE
Company — Title (Date - Date)
• Achievement-focused bullet points

## EDUCATION
Degree, Major — University (Year)

## PROJECTS (Optional)
## CERTIFICATIONS (Optional)
## PUBLICATIONS (Optional)
```

## 编写指南

### 专业总结的编写格式

```
[Title] with [X years] of experience in [domain]. 
Proven track record of [key achievement]. 
Skilled in [top 3 skills]. Seeking to [goal] at [company type].
```

**示例：**
```
Senior Software Engineer with 7 years of experience in full-stack development. 
Proven track record of reducing system latency by 40% and leading teams of 5+ developers. 
Skilled in Python, React, and AWS. Seeking to drive technical innovation at a growth-stage startup.
```

### 使用项目符号的格式（CAR方法）

```
[Action Verb] + [Task/Project] + [Result with Metrics]
```

**按类别划分的强行动动词：**

| 领导力 | 技术能力 | 成长能力 | 效率 |
|------------|-----------|--------|------------|
| 领导 | 开发 | 提高 | 降低 |
| 指导 | 设计 | 扩展 | 自动化 |
| 管理 | 架构 | 协调 | 整合 |
| 指导 | 实施 | 生成 | 优化 |

**示例：**
```
❌ Weak: "Responsible for managing a team"
✅ Strong: "Led cross-functional team of 8 engineers, delivering 3 major features ahead of schedule"

❌ Weak: "Worked on improving website performance"
✅ Strong: "Optimized database queries reducing page load time by 65%, improving user retention by 23%"

❌ Weak: "Helped with customer support"
✅ Strong: "Resolved 500+ customer tickets monthly with 98% satisfaction rate, reducing escalations by 40%"
```

### 所有内容都要量化

| 例如：**  
| 不要写……** | 要写……** |
|---------------|----------|  
| 管理一个团队 | 管理一个跨3个时区的12名工程师的团队 |
| 提高销售额 | 销售额增加了230万美元（同比增长34%） |
| 提高效率 | 处理时间从4小时缩短到15分钟 |
| 负责预算 | 管理每年50万美元的预算，合规率达到100% |
| 大量用户 | 该平台每天有超过5万名活跃用户 |

## ATS优化

### 应该做的✅
- 使用标准的部分标题（经验、教育背景、技能）
- 包含职位描述中的关键词
- 使用常见的职位名称
- 先写出缩写词的全称：例如“Search Engine Optimization (SEO)”
- 使用标准字体（Arial、Calibri、Times New Roman）
- 保存为.docx或.pdf格式（基于文本的格式，而非图片）

### 不应该做的❌
- 不要使用表格、列或文本框
- 不要添加页眉/页脚（ATS系统可能无法识别这些内容）
- 不要使用图片、标志或图形
- 不要使用创意性的部分名称（例如将“我的经历”改为“经验”）
- 避免使用特殊字符或图标
- 如果简历是从图片或扫描件生成的，不要使用PDF格式

### 关键词优化

```bash
# Extract keywords from job description
echo "JOB_DESCRIPTION" | tr '[:upper:]' '[:lower:]' | \
  grep -oE '\b[a-z]{3,}\b' | sort | uniq -c | sort -rn | head -20
```

## 模板

### 软件工程师模板

```markdown
# JANE DOE
San Francisco, CA | jane@email.com | linkedin.com/in/janedoe | github.com/janedoe

## PROFESSIONAL SUMMARY
Full-stack Software Engineer with 5+ years building scalable web applications. 
Expert in React, Node.js, and AWS with a track record of improving system performance by 40%+. 
Passionate about clean code and mentoring junior developers.

## TECHNICAL SKILLS
**Languages:** Python, JavaScript/TypeScript, Go, SQL
**Frontend:** React, Next.js, Redux, Tailwind CSS
**Backend:** Node.js, FastAPI, PostgreSQL, Redis
**Cloud/DevOps:** AWS (EC2, S3, Lambda), Docker, Kubernetes, CI/CD
**Tools:** Git, Jira, Figma, DataDog

## EXPERIENCE

**Senior Software Engineer** | TechCorp Inc. | Jan 2022 – Present
• Architected microservices migration reducing deployment time by 70% and enabling independent scaling
• Led team of 5 engineers delivering real-time notification system serving 2M+ users
• Implemented automated testing pipeline increasing code coverage from 45% to 92%
• Mentored 3 junior developers through structured onboarding program

**Software Engineer** | StartupXYZ | Jun 2019 – Dec 2021
• Built React dashboard processing $5M+ monthly transactions with 99.9% uptime
• Optimized PostgreSQL queries reducing API response time by 60%
• Developed CI/CD pipeline cutting release cycles from 2 weeks to 2 days

## EDUCATION
**B.S. Computer Science** | University of California, Berkeley | 2019
GPA: 3.7 | Relevant Coursework: Distributed Systems, Machine Learning, Algorithms

## PROJECTS
**Open Source Contribution** | github.com/project
• Contributed authentication module to popular framework (500+ GitHub stars)
```

### 产品经理模板

```markdown
# ALEX SMITH
New York, NY | alex@email.com | linkedin.com/in/alexsmith

## PROFESSIONAL SUMMARY
Product Manager with 6 years driving B2B SaaS products from concept to scale. 
Led products generating $15M+ ARR with proven expertise in user research, data analysis, and cross-functional leadership. 
MBA from Wharton.

## SKILLS
**Product:** Roadmap Planning, User Research, A/B Testing, PRDs, OKRs
**Analytics:** SQL, Amplitude, Mixpanel, Tableau, Excel
**Tools:** Jira, Figma, Miro, Notion, Productboard
**Methods:** Agile/Scrum, Design Thinking, Jobs-to-be-Done

## EXPERIENCE

**Senior Product Manager** | SaaS Company | Mar 2021 – Present
• Own product roadmap for enterprise platform ($8M ARR, 200+ customers)
• Launched AI-powered feature increasing user engagement by 45% and reducing churn by 20%
• Conducted 100+ customer interviews identifying $3M expansion opportunity
• Collaborated with engineering (12 devs), design, and sales to deliver quarterly releases

**Product Manager** | Tech Startup | Jan 2019 – Feb 2021
• Grew mobile app from 10K to 150K MAU through data-driven feature prioritization
• Reduced onboarding drop-off by 35% via user research and UX improvements
• Defined and tracked KPIs resulting in 25% improvement in activation rate

## EDUCATION
**MBA** | The Wharton School | 2018
**B.A. Economics** | NYU | 2014
```

### 市场经理模板

```markdown
# SARAH JOHNSON
Los Angeles, CA | sarah@email.com | linkedin.com/in/sarahjohnson

## PROFESSIONAL SUMMARY
Digital Marketing Manager with 5+ years driving growth for DTC and B2B brands. 
Managed $2M+ annual ad spend with 4x ROAS. Expert in paid acquisition, SEO, and marketing automation.

## SKILLS
**Channels:** Google Ads, Meta Ads, LinkedIn, TikTok, SEO/SEM
**Tools:** HubSpot, Marketo, Google Analytics, SEMrush, Klaviyo
**Skills:** Marketing Automation, Content Strategy, CRO, Email Marketing
**Analytics:** SQL, Looker, Excel, Attribution Modeling

## EXPERIENCE

**Marketing Manager** | E-commerce Brand | Jun 2021 – Present
• Manage $150K/month paid media budget achieving 4.2x ROAS (vs. 2.5x benchmark)
• Grew organic traffic by 180% YoY through SEO content strategy (50+ articles)
• Built email automation flows generating $500K incremental revenue
• Led rebrand project increasing brand awareness by 60% (measured via surveys)

**Digital Marketing Specialist** | Agency | Aug 2019 – May 2021
• Managed campaigns for 8 clients with combined $1M annual spend
• Achieved average 35% reduction in CAC across client portfolio
• Created reporting dashboards saving team 10 hours/week

## EDUCATION
**B.S. Marketing** | USC Marshall | 2019

## CERTIFICATIONS
Google Ads Certified | HubSpot Inbound Marketing | Meta Blueprint
```

## 导出命令

### 将Markdown转换为HTML
```bash
pandoc resume.md -o resume.html --standalone --css=style.css
```

### 将Markdown转换为PDF
```bash
pandoc resume.md -o resume.pdf --pdf-engine=xelatex
```

### 将Markdown转换为DOCX
```bash
pandoc resume.md -o resume.docx
```

### 自定义样式

```bash
# Create styled HTML
pandoc resume.md -o resume.html --standalone \
  --metadata title="Resume" \
  --css="https://cdn.jsdelivr.net/npm/water.css@2/out/water.css"
```

## 根据具体职位进行定制

### 分步流程

1. **从职位描述中提取关键词**
2. **匹配技能**——确保你的技能部分符合职位要求
3. **重新排序项目符号**——将最相关的经验放在前面
4. **使用与职位描述相同的语言**  
5. **自定义总结**——提及公司名称和具体职位

### 定制示例

**职位描述示例：**
> “寻找具有React、TypeScript和AWS经验的候选人。需要具备团队领导经验。”

**修改前的项目符号内容：**
```
• Developed web applications using various technologies
```

**修改后的项目符号内容：**
```
• Led team of 4 engineers building React/TypeScript applications deployed on AWS, serving 50K users
```

## 需避免的常见错误

| 错误 | 修正方法 |
|---------|-----|
| 包含“如需可提供推荐信” | 删除该内容——招聘方通常会默认提供 |
| 使用个人代词（我、我的） | 用行动动词开头 |
| 列出工作职责而非成果 | 重点介绍成果和影响 |
| 使用过时的技能（jQuery、Flash） | 保持技能的时效性和相关性 |
| 简历超过2页 | 经验不足10年的简历不超过1页，超过10年的简历最多2页 |
| 使用泛泛的求职目标 | 用具体的目标来替代 |
| 格式不一致 | 使用统一的日期格式和项目符号样式 |
| 拼写和语法错误 | 多次校对

## 快速检查清单

```
□ Contact info is current and professional
□ Email is professional (not coolboy99@...)
□ Summary is tailored to target role
□ All bullets start with action verbs
□ Achievements include metrics/numbers
□ Skills match job description keywords
□ Education includes relevant details only
□ No typos or grammatical errors
□ Consistent formatting throughout
□ Saved in ATS-friendly format
□ File named professionally (FirstName_LastName_Resume.pdf)
```

## 资源

- [哈佛大学简历指南](https://careerservices.fas.harvard.edu/resources/resume-guide/)
- [Google XYZ公式](https://www.inc.com/bill-murphy-jr/google-recruiters-say-these-5-resume-tips-including-x-y-z-formula-will-improve-your-odds-of-getting-hired-at-google.html)
- [ATS简历测试工具](https://www.jobscan.co/)