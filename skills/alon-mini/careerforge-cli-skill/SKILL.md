---
name: careerforge-cv-generator
description: 这款由人工智能驱动的简历生成工具专为求职申请而设计。它可通过 CareerForge CLI 实现自动化的求职流程，帮助用户管理主简历的创建与维护，设置筛选条件（如工作地点、关键词、是否支持远程办公或需要现场面试等），并根据用户需求生成定制化的简历。适用于希望自动化求职过程、创建/更新主简历、配置求职筛选条件，或为特定职位生成简历的用户。
---
# CareerForge CV生成器技能

该技能帮助用户设置并使用CareerForge CLI来自动化求职和简历生成过程。

## 概述

CareerForge是一款基于AI技术的简历生成工具，它利用Google的Gemini 2.5 Pro模型以及Writer+Judge算法，为用户生成符合ATS（ Applicant Tracking System）要求的个性化简历。

## 先决条件

### 第0步：下载CareerForge CLI

在使用该技能之前，请从GitHub下载CareerForge CLI：

```bash
cd /root/.openclaw/workspace
git clone https://github.com/alon-mini/CareerForge-cli.git careerforge-cli
cd careerforge-cli
npm install
```

**仓库地址：** https://github.com/alon-mini/CareerForge-cli

## 设置工作流程

### 第1步：检查/创建主简历

检查用户是否已拥有主简历文件（`CV_Master/master_resume.md`）。

**如果不存在主简历：**
向用户询问以下信息以创建简历：

1. **基本信息：**
   - 全名
   - 职位/头衔
   - 联系方式（电子邮件、电话、LinkedIn、作品集）

2. **职业概述：**
   - 2-3句话描述个人职业背景
   - 自身的核心优势
   - 职业发展方向

3. **核心能力：**
   - 5-8项主要技能（包括技术技能和软技能）

4. **工作经验：**
   - 每个职位的信息：公司名称、职位名称、工作日期、工作地点
   - 每个职位的3-4项主要成就
   - 请用户提供2-4个最相关的职位经历

5. **教育背景：**
   - 拥有的学位、就读机构、毕业时间、相关课程或论文

6. **语言能力：**
   - 使用的语言及熟练程度

**主简历格式：**
请按照以下Markdown结构保存文件：
```markdown
# [Name]

## Contact
- Email: 
- Phone: 
- LinkedIn: 
- Portfolio: 

## Summary
[2-3 sentences]

## Core Competencies
- Skill 1
- Skill 2
...

## Professional Experience

### [Company] | [Title]
*[Dates]*

- Bullet 1
- Bullet 2
...

## Education

### [Degree]
*Institution | Dates*

## Languages
- Language (Proficiency)
```

### 第2步：配置求职筛选条件

向用户询问求职筛选偏好：

1. **工作地点：**（例如：“以色列特拉维夫”）
2. **职位关键词：**（例如：“AI、数据分析师、产品经理”）
3. **工作经验年限：**（默认：2-4年）
4. **工作方式：**（远程/现场/混合办公：默认为仅限现场办公）
5. **需排除的关键词：**（例如：“高级职位、团队领导、销售”）
6. **需排除的公司：**（避免重复投递简历的公司）

### 第3步：配置定时任务

向用户询问定时任务的设置：
- **执行时间：**（默认：以色列时间8:00-18:00）
- **执行频率：**（默认：每周日-周四）
- **时区：**（默认：Asia/Jerusalem）

### 第4步：配置大型语言模型（LLM）参数

向用户索取API密钥：
- **默认选项：** 使用Google Gemini API密钥
- **可选：** 允许用户指定其他语言模型

## 日常工作流程

### 求职执行

定时任务每小时执行一次，具体步骤如下：
1. 搜索符合用户筛选条件的职位信息
2. 将职位信息发送到用户的Telegram群组（每条职位信息单独发送）
3. 每条消息包含：职位名称、公司名称、工作地点、职位链接及使用说明

### 简历生成

当用户回复职位信息并选择“生成简历”时：
1. 从消息中提取职位详细信息
2. 运行CareerForge CLI生成个性化简历
3. 将生成的简历PDF文件发送给用户

## 文件结构

```
workspace/
├── CV_Master/
│   └── master_resume.md          # User's master resume
├── careerforge-cli/              # CLI wrapper (from GitHub)
│   ├── generate_cv_from_json.js
│   ├── package.json
│   └── README.md
├── cvs/                          # Generated CVs output
├── job_search.py                 # Job search script
└── careerforge_config.json       # User's filter settings
```

## 命令说明

### 设置相关配置
```bash
# Download CareerForge CLI from GitHub
git clone https://github.com/alon-mini/CareerForge-cli.git careerforge-cli

# Initialize CareerForge
cd careerforge-cli && npm install

# Create master resume
./scripts/create_master_resume.sh
```

### 日常使用指南
```bash
# Run job search manually
python3 job_search.py

# Generate CV for specific job
node careerforge-cli/generate_cv_from_json.js job.json
```

## 参考资料

- [主简历模板](references/master_resume_template.md)
- [求职配置指南](references/job_search_config.md)
- [CareerForge CLI使用说明](references/cli_usage.md)