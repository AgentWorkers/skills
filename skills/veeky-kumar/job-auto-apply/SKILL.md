---
name: job-auto-apply
description: Clawdbot的自动化求职与申请系统：当用户希望搜索符合自己条件的职位并自动提交申请时，可以使用该系统。该系统支持在LinkedIn、Indeed、Glassdoor、ZipRecruiter和Wellfound等招聘平台上进行职位搜索，能够自动生成个性化的求职信、填写申请表格，并实时跟踪申请进度。适用于用户提出以下需求的情况：“查找并申请职位”、“自动申请[职位名称]”、“搜索[职位类型]的职位并提交申请”，或“帮我自动申请多个职位”。
---

# 自动申请职位技能

使用Clawdbot自动化在多个求职平台上搜索和提交职位申请。

## 概述

该技能实现了职位搜索和申请流程的自动化。它能够根据用户设定的条件搜索职位，分析职位与用户资格的匹配度，自动生成定制的求职信，并在用户确认后自动提交申请。

**支持的平台：**
- LinkedIn（包括Easy Apply功能）
- Indeed
- Glassdoor
- ZipRecruiter
- Wellfound（AngelList）

## 快速入门

### 1. 设置用户资料

首先，使用提供的模板创建用户资料：

```bash
# Copy the profile template
cp profile_template.json ~/job_profile.json

# Edit with user's information
# Fill in: name, email, phone, resume path, skills, preferences
```

### 2. 运行职位搜索和申请

```bash
# Basic usage - search and apply (dry run)
python job_search_apply.py \
  --title "Software Engineer" \
  --location "San Francisco, CA" \
  --remote \
  --max-applications 10 \
  --dry-run

# With profile file
python job_search_apply.py \
  --profile ~/job_profile.json \
  --title "Backend Engineer" \
  --platforms linkedin,indeed \
  --auto-apply

# Production mode (actual applications)
python job_search_apply.py \
  --profile ~/job_profile.json \
  --title "Senior Developer" \
  --no-dry-run \
  --require-confirmation
```

## 工作流程步骤

### 第1步：配置用户资料

从模板中加载用户资料，或通过编程方式创建用户资料：

```python
from job_search_apply import ApplicantProfile

profile = ApplicantProfile(
    full_name="Jane Doe",
    email="jane@example.com",
    phone="+1234567890",
    resume_path="~/Documents/resume.pdf",
    linkedin_url="https://linkedin.com/in/janedoe",
    years_experience=5,
    authorized_to_work=True,
    requires_sponsorship=False
)
```

### 第2步：定义搜索参数

```python
from job_search_apply import JobSearchParams, JobPlatform

search_params = JobSearchParams(
    title="Software Engineer",
    location="Remote",
    remote=True,
    experience_level="mid",
    job_type="full-time",
    salary_min=100000,
    platforms=[JobPlatform.LINKEDIN, JobPlatform.INDEED]
)
```

### 第3步：自动提交申请

```python
from job_search_apply import auto_apply_workflow

results = auto_apply_workflow(
    search_params=search_params,
    profile=profile,
    max_applications=10,
    min_match_score=0.75,
    dry_run=False,
    require_confirmation=True
)
```

## 与Clawdbot的集成

### 作为Clawdbot工具使用

将该技能安装到Clawdbot后，可以通过自然语言指令来使用它：

**示例指令：**
- “在旧金山查找并申请Python开发人员的职位”
- “搜索远程后端工程师职位，并申请排名前5的职位”
- “自动申请薪资超过10万美元的高级软件工程师职位”
- “申请Wellfound平台上科技初创公司的职位”

该技能将：
1. 解析用户的指令并提取搜索参数
2. 从已保存的配置中加载用户资料
3. 在指定的平台上进行搜索
4. 分析职位与用户资格的匹配度
5. 生成定制的求职信
6. 自动提交申请（如用户启用确认功能）
7. 报告搜索结果并跟踪申请进度

### 在Clawdbot中的配置

将该技能添加到Clawdbot的配置文件中：

```json
{
  "skills": {
    "job-auto-apply": {
      "enabled": true,
      "profile_path": "~/job_profile.json",
      "default_platforms": ["linkedin", "indeed"],
      "max_daily_applications": 10,
      "require_confirmation": true,
      "dry_run": false
    }
  }
}
```

## 功能特点

### 1. 多平台搜索
- 覆盖所有主要的求职平台
- 在支持API的平台使用官方API
- 在没有API的平台使用网页抓取技术

### 2. 智能匹配
- 分析职位描述以判断用户资格是否符合要求
- 计算职位匹配度得分
- 根据最低匹配阈值筛选职位

### 3. 申请个性化
- 为每个职位生成定制的求职信
- 根据职位要求调整简历的重点内容
- 处理各平台特有的申请表格

### 4. 安全功能
- **试运行模式**：在不提交申请的情况下进行测试
- **手动确认**：在提交前审核每个申请
- **速率限制**：防止过度占用平台资源
- **申请记录**：记录所有申请信息以供参考

### 5. 表单自动化
- 自动填写常见的申请字段：
  - 个人信息
  - 工作授权状态
  - 教育背景和工作经验
  - 技能和认证
  - 筛选问题（必要时使用人工智能）

## 高级用法

### 定制求职信模板

创建包含占位符的求职信模板：

```text
Dear Hiring Manager at {company},

I am excited to apply for the {position} role. With {years} years of 
experience in {skills}, I believe I would be an excellent fit.

{custom_paragraph}

I look forward to discussing how I can contribute to {company}'s success.

Best regards,
{name}
```

### 申请跟踪

搜索结果会以JSON格式自动保存，其中包含每个申请的详细信息，如提交时间、匹配度得分和申请状态。

## 配套资源

### 脚本
- `job_search_apply.py`：包含搜索、匹配和申请逻辑的主要自动化脚本

### 参考文档
- `platform_integration.md`：关于API集成、网页抓取、表单自动化和平台特定细节的技术文档

### 资源文件
- `profile_template.json`：包含所有必填和可选字段的完整用户资料模板

## 安全与道德规范

### 重要提示

1. **诚实守信**：切勿夸大自己的资格或工作经验
2. **真诚申请**：仅申请你真正感兴趣的职位
3. **遵守平台限制**：遵守各平台的使用条款和限制
4. **手动审核**：为确保申请质量，可启用确认功能
5. **保护隐私**：妥善保管个人资料和密码

### 最佳实践

- 先使用试运行模式验证功能
- 设置合理的申请频率（每天5-10次）
- 设置较高的匹配度阈值（0.75以上）
- 对重要申请启用确认功能
- 跟踪申请结果以优化申请策略