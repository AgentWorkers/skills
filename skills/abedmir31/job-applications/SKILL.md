# 自动化求职申请技能

## 概述
这是一个为Abed Mir设计的自动化求职和申请系统。该系统会在Indeed网站上搜索匹配的职位，分析申请者的匹配度，根据职位要求定制简历，并通过ATS（应用跟踪系统）平台（如Greenhouse、Lever、Workday、Indeed Easy Apply）提交申请。

## 目录结构
```
job-applications/
├── config.json              # Search criteria, filters, settings
├── resume-source/
│   ├── resume.json          # Structured resume data (source of truth)
│   └── resume.tex           # LaTeX template
├── scripts/
│   └── tailor_resume.py     # Resume tailoring + LaTeX generation
├── tailored-resumes/        # Generated PDFs per application
├── tracking/
│   └── applications.json    # Application log
└── logs/                    # Run logs
```

## 工作流程（每次运行）

### 1. 搜索职位
- 在浏览器中打开Indeed网站（将页面添加为书签）
- 根据config.json文件中的配置，搜索每个目标职位
- 筛选条件：远程工作或DFW地区混合工作、在最近24小时内发布的职位
- 收集职位的URL、职位名称和公司信息

### 2. 去重
- 检查每个职位是否已经申请过或被跳过

### 3. 分析匹配度
对于每个新找到的职位：
- 访问职位页面，阅读完整描述
- 根据`avoid_industries`和`avoid_keywords`列表判断是否适合申请
- 根据技能匹配度和经验匹配度对职位进行评分
- 优先考虑AI/代理相关的职位

### 4. 定制简历
对于符合匹配条件的职位：
- 以`resume.json`文件为基准
- 重新排列简历中的项目符号内容，将最相关的经验放在前面
- 强调与职位要求匹配的技能和技术
- **严禁伪造经验或技能信息**
- 使用LaTeX编译工具生成PDF格式的简历

### 5. 提交申请
根据职位URL判断使用的ATS平台：
- **Greenhouse**（boards.greenhouse.io）：单页表单——填写姓名、电子邮件、电话号码、上传简历（可选字段）
- **Lever**（jobs.lever.co）：单页表单——与Greenhouse类似
- **Workday**（myworkday*.com）：多步骤向导——创建账户或登录后填写各字段
- **Indeed Easy Apply**：通过Indeed的界面快速提交申请

- 使用config.json文件中的候选人信息填写所有必填字段，并上传定制好的PDF简历。

### 6. 记录日志
将操作记录到`applications.json`文件中：
```json
{
  "id": "uuid",
  "date": "ISO timestamp",
  "company": "Company Name",
  "title": "Job Title",
  "url": "application URL",
  "platform": "greenhouse|lever|workday|indeed",
  "status": "applied|skipped|failed",
  "skip_reason": null,
  "resume_version": "tailored-resumes/company-title.pdf",
  "notes": ""
}
```

## Cron调度
系统每天运行3次：
- 上午8:00（CT时间）——上午批次（抓取夜间发布的职位）
- 中午12:00（CT时间）——中午批次
- 下午5:00（CT时间）——下午批次（抓取当天发布的职位）

## ATS平台填写指南

### Greenhouse
- URL模式：`boards.greenhouse.io/*` 或 `job-boards.greenhouse.io/*`
- 需填写的字段：名字、姓氏、电子邮件、电话号码、简历（文件上传）、工作地点、LinkedIn（可选）、网站（可选）
- 有时会有自定义问题（下拉菜单、文本输入框、复选框）
- 提交按钮通常位于页面底部

### Lever
- URL模式：`jobs.lever.co/*`
- 需填写的字段：全名、电子邮件、电话号码、简历（文件上传）、LinkedIn（可选）、网站（可选）、当前公司（可选）
- 可能会有额外的问题
- 提交按钮位于页面底部

### Workday
- URL模式：`*.myworkdayjobs.com/*` 或 `*.wd5.myworkdayjobs.com/*`
- 多页面流程：登录/创建账户 → 我的信息 → 我的经验 → 申请问题 → 审核 → 提交
- 需要逐页解析并填写信息
- 最为复杂——遇到特殊字段时可能需要人工干预

### Indeed Easy Apply
- 使用abedmir31@gmail.com在openclaw浏览器中登录Indeed账号
- 如果会话过期，导航至https://secure.indeed.com/auth，输入abedmir31@gmail.com，并在#job-applications Discord频道向Abed索取验证码
- 部分字段会自动从Indeed个人资料中填充
- 可能会有额外的筛选问题
- 点击“立即申请”即可完成提交

### 关于Indeed会话的注意事项
- 登录需要使用电子邮件验证码（无需密码）
- 会话信息会在openclaw浏览器中保持
- 如果导航栏显示“登录”而非“欢迎，Abed”，则表示会话已过期

### LinkedIn Easy Apply
- 使用abedmir31@gmail.com在openclaw浏览器中登录LinkedIn账号
- 导航至https://www.linkedin.com/jobs/search/搜索职位
- 根据“Easy Apply”选项、工作地点和发布日期筛选职位
- 点击职位列表上的“Easy Apply”按钮
- LinkedIn Easy Apply页面会自动填充大部分个人资料信息
- 上传简历、回答额外问题后提交申请
- 如果会话过期，导航至https://www.linkedin.com/login并在#job-applications频道向Abed索取登录凭据

### 关于LinkedIn会话的注意事项
- 登录需要使用电子邮件和密码（信息存储在浏览器会话中）
- 会话信息会在openclaw浏览器中保持
- 如果看到登录页面而非职位列表，表示会话已过期

## 重要规则
- **严禁在申请材料中撒谎**——仅允许重新排列或强调现有的工作经验
- 禁止申请与宗教或道德准则相悖的行业（如银行、抵押贷款、赌博等）
- 必须记录遇到的所有职位信息（包括已申请或被跳过的职位及其原因）
- 如果申请过程中出现错误，记录为“失败”并继续下一轮
- 每次运行完成后，务必在#job-applications Discord频道报告操作结果
- **完成申请后务必关闭浏览器标签页**——使用`browser(action="close")`或切换页面，以防止内存占用和标签页混乱