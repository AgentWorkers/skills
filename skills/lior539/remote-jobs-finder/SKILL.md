---
name: remote-jobs-finder
version: 1.4.0
description: 这是一个基于 Remote Rocketship 提供的精选职位信息的自然语言远程工作查找工具。该工具以对话式的方式引导用户完成注册流程，能够记住用户的偏好设置；用户可以选择使用自己的简历来提高匹配度；同时支持分页功能（例如“显示更多20个职位”），并允许用户安排定期自动检查新职位的功能。
---
# 远程工作搜索助手 × OpenClaw 技能（自然语言求职助手）

每当用户通过常规聊天请求寻找远程工作、浏览职位信息或设置持续的工作搜索时，可以使用此技能。该功能由 Remote Rocketship（https://www.remoterocketship.com）提供支持。

**请勿告知用户使用控制面板或斜杠命令**。整个交互过程应保持对话式：先询问一些基本信息，然后获取职位列表，并根据用户需求继续提供服务（例如：“再给我推送20个职位”）。

## 主要用户体验目标

1. 通过自然语言完成用户引导（简洁、友好、无障碍）。
2. 记录用户的偏好设置（职位名称、工作地点、必备条件、排除项、排序偏好、检查频率）。
3. （可选）基于简历的匹配评分（简历仅保存在助手本地，不会发送到其他地方）。
4. 自动设置API密钥（如果密钥缺失，询问用户如何获取，并让用户将其粘贴到聊天中）。
5. 提供持续监控服务（用户可以选择每小时检查一次；如果用户同意，可以使用定时任务）。
6. 简便的分页功能（默认显示20个职位；用户可重复请求更多职位）。

## 安装与插件设置

1. 安装此技能（在ClawHub中的slug为`remote-jobs-finder`）。
2. 安装配套插件（用于启用相关功能）：
   ```
   openclaw plugins install ./skills/remote-jobs-finder/plugin
   ```
3. 允许使用的工具：
   - **普通用户**：`rr.jobs`, `rr.save_api_key`, `rr.schedule_checks`, `rr.get_last_search`。
   - **可选/敏感操作（需用户明确同意）：`rr.save_session_cookie`, `rr.key_status`, `rr.generate_key`, `rr.rotate_key`, `rr.revoke_key`。
   - 用户也可以请求`rr.clear_api_key`/`rr.clear_session_cookie`以删除已存储的敏感信息。
4. 敏感信息的处理方式：
   - 如果用户粘贴了API密钥，将其保存在本地（切勿再次显示）。
   - 仅在用户明确要求管理密钥时（生成/轮换/撤销/查询状态），才请求或存储`sb-access-token`和`sb-refresh-token`。
5. 在沙箱环境中运行助手时，请确保这些环境变量或`.state`文件夹可被访问。

**辅助脚本**：在您的工作空间根目录下运行`./scripts/install_remote_rocketship_skill.sh`以安装技能和插件，并自动重启代理。

---

## 触发条件

当用户发送以下消息时触发此技能：
- “帮我找一份远程工作”
- “查找远程产品经理职位”
- “显示英国的远程职位”
- “从昨天起有没有新的后端职位？”
- “再给我推送20个职位”
- “设置每小时检查一次”

如果用户的查询与远程工作相关，并且Remote Rocketship的服务能够提供帮助，请使用此技能。

---

## 对话流程

### A) 用户引导（询问以下问题）

当用户首次请求“帮我找一份远程工作”时，询问以下内容：
1. **职位类型**：
   - “您在寻找哪种类型的职位？（职位名称、职能、工作经验要求）”
2. **工作地点**：
   - “您将在哪里工作？（国家/地区）”
3. **必备条件与排除项**：
   - “您有特定的要求吗？（例如薪资范围、是否支持异步工作、行业限制等）”
   - “您希望避免哪些职位？（例如代理公司提供的职位、某些行业、需要随时待命等）”
   - 尽量将这些问题合并为一个问题。
4. **简历（可选）**：
   - “如果您愿意，可以发送简历，我会根据匹配度为您筛选职位。”
   - 隐私声明：“您的简历将仅保存在本地，不会发送到其他地方，仅用于提高匹配效果。”
5. **监控频率**：
   - “您希望我多久检查一次新的匹配结果？（每小时、每6小时、每天还是不检查）”
   - 将用户的答案保存在`pollingCadence`变量中，然后使用该频率调用`rr.schedule_checks`。用户可以随时请求停止监控。

如果用户不愿意回答所有问题，也可以根据现有信息开始获取职位列表。

---

## 用户偏好记录（非常重要）

在内存中维护一个简单的用户档案，以便用户无需重复输入信息：
- `targetTitles`：字符串数组
- `locationFrom`：字符串（国家/地区）
- `seniority`：枚举值（如果已知）
- `employmentType`：枚举值（如果已知）
- `mustHaves`：字符串数组
- `dealBreakers`：字符串数组
- `rankingPreference`：`"best_fit"` 或 `"newest_first`
- `pollingCadence`：例如“每小时”/“每天”/“不检查”
- `lastQueryFilters`：上次使用的搜索条件

如果用户更新了任何信息（例如“实际上我只想要合同制职位”），请更新相应的用户档案。

---

## API密钥与会话cookie的处理流程

- **当用户粘贴API密钥时**，立即使用该密钥调用`rr.save_api_key`。简要确认（例如：“已保存 ✅ — 正在获取职位信息。”），**切勿再次显示密钥**。
- **当需要管理密钥时**（生成/轮换/撤销/查询状态），询问用户`sb-access-token`和`sb-refresh-token`，然后调用`rr.save_session_cookie`。将cookie保存在文件中（切勿再次显示）。
- `rr.jobs`会自动使用保存的API密钥（除非用户另有指定），每次请求最多显示20个职位。如果未保存密钥，工具会返回`{"error": "MISSING_API_KEY"}`，此时可以礼貌地提醒用户重新输入。
- 如果用户请求删除已存储的敏感信息，可以使用`rr.clear_api_key`/`rr.clear_session_cookie`。

## 认证与密钥设置（使用自然语言）

### 先决条件
- 用户必须拥有有效的Remote Rocketship订阅资格并已登录（因此 `/api/openclaw/key` 请求会携带用户的认证cookie）。
- 遵守每日请求限制：每个密钥每天最多1,000次请求，每次请求最多显示50个职位。

### 如果API密钥缺失或无效（401错误）

用简单的语言告知用户：
> “为了获取Remote Rocketship的职位信息，我需要您的API密钥。
> 请访问remoterocketship.com/account，复制您的API密钥，然后粘贴到这里。”

用户粘贴密钥后：
- 立即使用该密钥调用`rr.save_api_key`。
- 确认：“已保存 — 现在可以获取职位信息了。”（切勿再次显示密钥。）

请勿要求用户输入斜杠命令。

### 会话cookie用于密钥自动化

如果用户希望您执行`rr.generate_key`/`rr.rotate_key`/`rr.revoke_key`/`rr.key_status`操作，请询问用户`sb-access-token`和`sb-refresh-token`。将cookie保存在本地（通过`rr.save_session_cookie`）。工具会自动使用该cookie。

### 敏感信息的处理规则（确保WhatsApp聊天安全）

- 绝不要在助手消息中显示任何敏感信息（API密钥、cookie、授权令牌）。
- 如果用户在聊天中提供了敏感信息，确认收到后继续处理。
- 如果需要引用密钥进行故障排除，仅显示密钥的部分内容（例如最后4个字符），并且仅在用户明确请求时显示。

---

## 定时检查（可选）

在完成用户引导后（或首次成功搜索后），询问用户：
> “您希望我按照什么频率检查新的匹配职位？（每小时、每6小时、每天等）”

如果用户同意，可以创建/启用定时任务来定期检查新的职位信息：
- 询问用户希望多久检查一次（每小时、每6小时、每天等）。
- 创建/启用定时任务以重新执行上次保存的搜索条件。
- 仅在新职位出现时通知用户（通过职位ID/URL去重）。
- 通知内容要简洁（例如：“显示前5个职位 + ‘还需要更多吗?’”）。

如果用户拒绝，则不进行任何操作。

---

## 获取职位信息

- **默认行为**：
  - 默认每次请求显示20个职位（`itemsPerPage: 20`）。
  - 如果用户明确要求每次显示更多职位，最多显示50个。

---

## 分页与结果显示（使用自然语言）

维护一个轻量级的对话状态对象：
- `filters`：搜索条件
- `page`：当前页码
- `itemsPerPage`：每页显示的职位数量
- `totalCount`：总职位数量

规则：
1. 当用户修改搜索条件时，将`page`重置为1并重新获取职位列表。
2. 如果用户请求“更多”、“再给我推送20个职位”或“下一页”，增加`page`值，并使用缓存的搜索条件重新获取职位列表。
3. 如果用户请求“返回上一页”，将`page`值减1并重新获取职位列表。
4. 始终告知用户当前显示的职位数量（例如：“当前显示21–40个职位，共134个”）。

示例状态对象：
```json
{
  "filters": {
    "jobTitleFilters": ["Software Engineer"],
    "locationFilters": ["Worldwide"],
    "itemsPerPage": 20
  },
  "page": 1,
  "totalCount": 134
}
```

**API分页说明**：
- 每次`rrjobs`响应都会包含`pagination`字段：
  `{ page, itemsPerPage, totalCount, totalPages, hasNextPage, hasPreviousPage }`
- 默认值：`page: 1`, `itemsPerPage: 20`（最多50个职位）。
- 仅接受整数；其他值将被忽略。
- 使用`pagination.hasNextPage`来判断是否需要再次获取职位列表，并在响应中显示`pagination.totalCount`。

## 排序选项

询问用户一次并记录偏好：
- “您希望结果按照什么顺序显示？（按匹配度最高排序还是最新发布排序？”

### A) 最新发布排序
  - 按职位发布时间降序排序。

### B) 最适合排序（简单易懂的评分方式）

根据以下因素计算每个职位的匹配度：
- 职位名称匹配度（0–40分）
- 必备条件的符合程度（0–25分）
- 排除项的影响（0–40分）
- 简历关键词的匹配程度（0–35分，仅当用户提供了简历时）

然后：
- 按匹配度降序显示职位列表。
- 如果用户询问“为什么这个职位适合我”，可以简要说明评分依据（2–4条理由）。

简历隐私：简历信息仅保存在助手本地，不会发送给外部服务。

---

## 内部使用的工具

助手可以使用以下工具，但无需用户手动输入：
- **普通用户允许使用的工具**：
  - `rrjobs`
  - `rr.save_api_key`
  - `rr.schedule_checks`
  - `rr.get_last_search`
  - `rr.clear_api_key`
  - `rr.clear_session_cookie`
- **敏感操作（需用户明确同意）**：
  - `rr.save_session_cookie`
  - `rr.key_status`
  - `rr.generate_key`
  - `rr.rotate_key`
  - `rr.revoke_key`

### 工具参数与密钥要求

- `rr.jobs` 需要`filters`和API密钥。如果用户已经提供了密钥，工具会自动使用；否则会返回`{"error": "MISSING_API_KEY"}`，此时可以再次请求用户提供密钥。
- `rr.schedule_checks` 需要`cadence`参数（每小时/每6小时/每天/不检查），并会生成相应的定时任务。成功执行后返回`{"scheduled: true, jobId, systemEvent}`。告知用户检查频率（例如“我将在每6小时检查一次”）。如果传递`cadence: "off"`，则表示取消监控。
- `rr.generate_key`、`rr.rotate_key`、`rr.revoke_key`和`rr.key_status`需要用户的认证cookie。使用`rr.save_session_cookie`保存cookie（询问用户提供`sb-access-token`和`sb-refresh-token`）。
- 所有工具都支持`baseUrl`参数（用于配置测试环境）。

---

## 过滤条件的处理

在调用`/api/openclaw/jobs`之前，对输入数据进行清洗：
- 职位名称：转换为标准格式（不区分大小写，去除空白字符）。
- 地点：仅允许已知的有效值；将常见别名标准化（例如USA/US → United States, UK/Great Britain/England → United Kingdom, UAE → United Arab Emirates）。忽略未知值。
- 枚举类型（如seniority、employmentType、visa、companySize、requiredLanguages、industries）必须与预设选项匹配；忽略无效值。
- `itemsPerPage`默认值为20，最多50个职位；`page`从1开始。

---

## 响应模板（使用Remote Rocketship的语气）

```
**{job.title}** at {job.company.name}
🗓 {timeAgo} · 📍 {location/flag emojis} · 💰 {salaryLabel}{optional chips: ✈️ visa, 🎯 seniority}{optional: ⭐ Fit {fitScore}/100}
{summary line 1}
{summary line 2}
```

**响应指南**：
- 语言简洁友好，使用轻量级的表情符号。
- 如果薪资信息缺失，显示“薪资信息未提供”。
- 如果`requestCountToday`大于800，提醒用户已达到每日请求限制。

`rr_jobs`响应包含`newJobOpenings`（上次请求未显示的新职位）和`stats.newCount`（用于提示有新职位时显示）。

---

## 请求限制与错误处理

| 状态 | 含义 | 助手应对方式 |
| --- | --- | --- |
| 401 | API密钥缺失或无效 | 请用户粘贴密钥，使用`rr.save_api_key`保存后再次调用`rr_jobs`。 |
| 403 | 订阅计划无效 | 告知用户需要激活Remote Rocketship订阅才能获取职位信息。 |
| 429 | 每日请求次数超出限制 | 通知用户每日请求次数限制为1,000次。建议用户稍后再试或更换密钥。 |
| 5xx | 后端错误 | 道歉并尝试重试；如果问题持续，请升级处理。 |

## 允许使用的值

（保留现有的参数列表：jobTitleFilters、locationFilters、seniorityFilters等）

### 监控与日志记录

- 后端会生成`console.warn`事件（用于调试）。
- PostHog会记录`openclaw_jobs_request`日志，包含`email`、`filters`、`jobsReturned`、`requestCountToday`、`techStackFilters`、`industriesFilters`。
- 建议的监控策略：当`requestCountToday`达到800次或5分钟内的错误率超过20%时，通知Remote Rocketship团队。

- **jobTitleFilters`（201个值）：
```json
[
  "2D Artist",
  "3D Artist",
  "AI Engineer",
  "AI Research Scientist",
  "Account Executive",
  "Account Manager",
  "Accountant",
  "Accounting Manager",
  "Accounts Payable",
  "Accounts Receivable",
  "Actuary",
  "Administration",
  "Administrative Assistant",
  "Affiliate Manager",
  "Analyst",
  "Analytics Engineer",
  "Android Engineer",
  "Application Engineer",
  "Appointment Setter",
  "Architect",
  "Art Director",
  "Artificial Intelligence",
  "Attorney",
  "Auditor",
  "Backend Engineer",
  "Bilingual",
  "Billing Specialist",
  "Blockchain Engineer",
  "Bookkeeper",
  "Brand Ambassador",
  "Brand Designer",
  "Brand Manager",
  "Business Analyst",
  "Business Development Rep",
  "Business Intelligence Analyst",
  "Business Intelligence Developer",
  "Business Operations",
  "Call Center Representative",
  "Capture Manager",
  "Chief Marketing Officer",
  "Chief Operating Officer",
  "Chief Technology Officer",
  "Chief of Staff",
  "Civil Engineer",
  "Claims Specialist",
  "Client Partner",
  "Client Services Representative",
  "Clinical Operations",
  "Clinical Research",
  "Cloud Engineer",
  "Collections",
  "Communications",
  "Community Manager",
  "Compliance",
  "Computer Vision Engineer",
  "Consultant",
  "Content Creator",
  "Content Manager",
  "Content Marketing Manager",
  "Content Writer",
  "Controller",
  "Conversion Rate Optimizer",
  "Copywriter",
  "Counselor",
  "Creative Strategist",
  "Crypto",
  "Customer Advocate",
  "Customer Retention Specialist",
  "Customer Success Manager",
  "Customer Support",
  "Data Analyst",
  "Data Engineer",
  "Data Entry",
  "Data Scientist",
  "Database Administrator",
  "DeFi",
  "Designer",
  "DevOps Engineer",
  "Developer Relations",
  "Digital Marketing",
  "Director",
  "Ecommerce",
  "Electrical Engineer",
  "Email Marketing Manager",
  "Engineer",
  "Engineering Manager",
  "Events",
  "Executive Assistant",
  "Field Engineer",
  "Financial Crime",
  "Financial Planning and Analysis",
  "Frontend Engineer",
  "Full-stack Engineer",
  "Game Engineer",
  "General Counsel",
  "Graphics Designer",
  "Growth Marketing",
  "Hardware Engineer",
  "Human Resources",
  "IT Support",
  "Implementation Specialist",
  "Incident Response Analyst",
  "Influencer Marketing",
  "Infrastructure Engineer",
  "Inside Sales",
  "Insurance",
  "Journalist",
  "LLM Engineer",
  "Lead Generation",
  "Learning and Development",
  "Legal Assistant",
  "Machine Learning Engineer",
  "Manager",
  "Marketing",
  "Marketing Analyst",
  "Marketing Operations",
  "Mechanical Engineer",
  "Medical Billing and Coding",
  "Medical Director",
  "Medical Reviewer",
  "Medical writer",
  "NLP Engineer",
  "Network Engineer",
  "Network Operations",
  "Notary",
  "Onboarding Specialist",
  "Operations",
  "Outside Sales",
  "Paralegal",
  "Payroll",
  "People Operations",
  "Performance Marketing",
  "Platform Engineer",
  "Pre-sales Engineer",
  "Pricing Analyst",
  "Procurement",
  "Producer",
  "Product Adoption Specialist",
  "Product Analyst",
  "Product Designer",
  "Product Manager",
  "Product Marketing",
  "Product Operations",
  "Product Specialist",
  "Production Engineer",
  "Program Manager",
  "Project Manager",
  "Proposal Manager",
  "Public Relations",
  "QA Automation Engineer",
  "QA Engineer",
  "Recruitment",
  "Research Analyst",
  "Research Engineer",
  "Research Scientist",
  "Revenue Operations",
  "Risk",
  "Robotics",
  "SAP",
  "SDET",
  "SEO Marketing",
  "Sales",
  "Sales Development Rep",
  "Sales Engineer",
  "Sales Operations Manager",
  "Salesforce Administrator",
  "Salesforce Analyst",
  "Salesforce Consultant",
  "Salesforce Developer",
  "Scrum Master",
  "Security Analyst",
  "Security Engineer",
  "Security Operations",
  "ServiceNow",
  "Smart Contract Engineer",
  "Social Media Manager",
  "Software Engineer",
  "Solutions Engineer",
  "Strategy",
  "Supply Chain",
  "Support Engineer",
  "System Administrator",
  "Systems Engineer",
  "Tax",
  "Technical Account Manager",
  "Technical Customer Success",
  "Technical Product Manager",
  "Technical Program Manager",
  "Technical Project Manager",
  "Technical Recruiter",
  "Technical Writer",
  "Therapist",
  "Threat Intelligence Specialist",
  "Translator",
  "Underwriter",
  "User Researcher",
  "Vice President",
  "Video Editor",
  "Web Designer",
  "Web3",
  "iOS Engineer"
]
```
- **locationFilters**（182个值）：
```json
[
  "Africa",
  "Alabama",
  "Alaska",
  "Albania",
  "Algeria",
  "American Samoa",
  "Argentina",
  "Arizona",
  "Arkansas",
  "Armenia",
  "Aruba",
  "Asia",
  "Australia",
  "Austria",
  "Azerbaijan",
  "Bahamas",
  "Bahrain",
  "Bangladesh",
  "Barbados",
  "Belarus",
  "Belgium",
  "Bermuda",
  "Bosnia and Herzegovina",
  "Brazil",
  "Bulgaria",
  "California",
  "Canada",
  "Cape Verde",
  "Chile",
  "Colombia",
  "Colorado",
  "Connecticut",
  "Costa Rica",
  "Croatia",
  "Curaçao",
  "Cyprus",
  "Czech",
  "Delaware",
  "Denmark",
  "Dominica",
  "Dominican Republic",
  "Ecuador",
  "Egypt",
  "El Salvador",
  "Estonia",
  "Ethiopia",
  "Europe",
  "Finland",
  "Florida",
  "France",
  "Georgia",
  "Germany",
  "Ghana",
  "Gibraltar",
  "Greece",
  "Greenland",
  "Guam",
  "Guatemala",
  "Guernsey",
  "Hawaii",
  "Honduras",
  "Hong Kong",
  "Hungary",
  "Iceland",
  "Idaho",
  "Illinois",
  "India",
  "Indiana",
  "Indonesia",
  "Iowa",
  "Ireland",
  "Isle of Man",
  "Israel",
  "Italy",
  "Jamaica",
  "Japan",
  "Jersey",
  "Jordan",
  "Kansas",
  "Kazakhstan",
  "Kentucky",
  "Kenya",
  "Latin America",
  "Latvia",
  "Lebanon",
  "Lesotho",
  "Libya",
  "Liechtenstein",
  "Lithuania",
  "Louisiana",
  "Luxembourg",
  "Macedonia",
  "Madagascar",
  "Maine",
  "Malaysia",
  "Maldives",
  "Malta",
  "Maryland",
  "Massachusetts",
  "Mauritius",
  "Mexico",
  "Michigan",
  "Middle East",
  "Minnesota",
  "Mississippi",
  "Missouri",
  "Moldova",
  "Monaco",
  "Montana",
  "Montenegro",
  "Morocco",
  "Namibia",
  "Nebraska",
  "Netherlands",
  "Nevada",
  "New Hampshire",
  "New Jersey",
  "New Mexico",
  "New York",
  "New Zealand",
  "Nicaragua",
  "Nigeria",
  "North America",
  "North Carolina",
  "North Dakota",
  "Norway",
  "Oceania",
  "Ohio",
  "Oklahoma",
  "Oman",
  "Oregon",
  "Pakistan",
  "Palau",
  "Palestinian Territory",
  "Panama",
  "Paraguay",
  "Pennsylvania",
  "Peru",
  "Philippines",
  "Poland",
  "Portugal",
  "Puerto Rico",
  "Qatar",
  "Rhode Island",
  "Romania",
  "Russia",
  "Saudi Arabia",
  "Serbia",
  "Seychelles",
  "Singapore",
  "Slovakia",
  "Slovenia",
  "South Africa",
  "South Carolina",
  "South Dakota",
  "South Georgia",
  "South Korea",
  "Spain",
  "Sri Lanka",
  "Suriname",
  "Swaziland",
  "Sweden",
  "Switzerland",
  "Taiwan",
  "Tennessee",
  "Texas",
  "Thailand",
  "Trinidad and Tobago",
  "Turkey",
  "Ukraine",
  "United Arab Emirates",
  "United Kingdom",
  "United States",
  "Uruguay",
  "Utah",
  "Vermont",
  "Virginia",
  "Washington",
  "West Virginia",
  "Wisconsin",
  "Worldwide",
  "Wyoming"
]
```
- **seniorityFilters**（5个值）：
```json
[
  "entry-level",
  "expert",
  "junior",
  "mid",
  "senior"
]
```
- **employmentTypeFilters**（4个值）：
```json
[
  "contract",
  "full-time",
  "internship",
  "part-time"
]
```
- **visaFilter**（2个值）：
```json
[
  "h1b",
  "uk-skilled-worker"
]
```
- **companySizeFilters**（8个值）：
```json
[
  "1,10",
  "10001,",
  "1001,5000",
  "11,50",
  "201,500",
  "5001,10000",
  "501,1000",
  "51,200"
]
```
- **requiredLanguagesFilters**（29个值）：
```json
[
  "ar",
  "cs",
  "da",
  "de",
  "en",
  "es",
  "fi",
  "fr",
  "he",
  "hi",
  "hu",
  "id",
  "is",
  "it",
  "ja",
  "ko",
  "nl",
  "no",
  "pl",
  "pt",
  "ro",
  "ru",
  "sk",
  "sv",
  "th",
  "tr",
  "uk",
  "vi",
  "zh"
]
```
- **industriesFilters**（44个值）：
```json
[
  "API",
  "AR/VR",
  "Aerospace",
  "Agriculture",
  "Artificial Intelligence",
  "B2B",
  "B2C",
  "Banking",
  "Beauty",
  "Biotechnology",
  "Charity",
  "Compliance",
  "Crypto",
  "Cybersecurity",
  "Education",
  "Energy",
  "Enterprise",
  "Fashion",
  "Finance",
  "Fintech",
  "Gambling",
  "Gaming",
  "Government",
  "HR Tech",
  "Hardware",
  "Healthcare Insurance",
  "Marketplace",
  "Media",
  "Non-profit",
  "Pharmaceuticals",
  "Productivity",
  "Real Estate",
  "Recruitment",
  "Retail",
  "SaaS",
  "Science",
  "Security",
  "Social Impact",
  "Sports",
  "Telecommunications",
  "Transport",
  "Web 3",
  "Wellness",
  "eCommerce"
]
```

**注意：`excludeRequiredLanguagesFilters`的使用方式与`requiredLanguagesFilters`相同。**

## 响应模板

```
**{job.title}** at {job.company.name}
🗓 {timeAgo} · 📍 {location/flag emojis} · 💰 {salaryLabel}{optional chips: ✈️ visa, 🎯 seniority}
{summary line 1}
{summary line 2}
```
- 使用Remote Rocketship的语气，语言简洁友好，使用轻量级的表情符号。
- 如果薪资信息缺失，显示“薪资信息未提供”。
- 当`requestCountToday`达到800次时，提醒用户请求次数限制。
- 在定期检查时，显示`stats.newCount`和`newJobOpenings`数组，让用户了解最新情况。

## 请求限制与错误处理

| 状态 | 含义 | 助手应对方式 |
| --- | --- | --- |
| 401 | API密钥缺失或无效 | 请用户粘贴有效的密钥，使用`rr.save_api_key`保存后再次调用`rr_jobs`。 |
| 403 | 订阅计划无效 | 建议用户重新激活Remote Rocketship订阅（通过 `/sign-up`）后再试。 |
| 429 | 每日请求次数超出限制 | 通知用户每日请求次数限制为1,000次。建议用户稍后再试或更换密钥。 |
| 5xx | 后端错误 | 道歉并尝试重试；如果问题持续，建议用户更换密钥。 |

## 使用流程

1. **密钥提供**：如有需要，请求用户粘贴API密钥；收到密钥后，调用`rr.save_api_key`并确认“已保存 ✅”（切勿再次显示密钥）。
2. **获取职位信息**：收集用户输入的搜索条件，调用`rrjobs`，渲染职位列表，并在`requestCountToday`达到800次时提醒用户请求次数限制。
3. **密钥管理**：仅当用户明确请求时，执行密钥的生成/轮换/撤销/查询状态操作：请求用户的认证cookie，使用`rr.save_session_cookie`保存后，根据需要调用`rr.key_status`/`rr.rotate_key`/`rr.revoke_key`。
4. **监控**：当用户请求“每隔X小时检查一次”时，使用`rr.schedule_checks`。用自然语言确认检查频率（例如：“好的 — 我将每6小时检查一次”）。

## 分页与结果显示

**对话式分页提示**：
- 维护一个轻量级的对话状态对象（包含搜索条件、当前页码、每页显示的职位数量）。
- 当用户修改搜索条件时，将`page`重置为1并重新获取职位列表。
- 如果用户请求“更多”，增加`page`值，并使用缓存的搜索条件重新获取职位列表。
- 如果用户请求“返回上一页”，将`page`值减1。
- 始终告知用户当前显示的职位数量（例如：“当前显示21–40个职位，共134个”）。

示例状态对象：
```json
{
  "filters": {
    "jobTitleFilters": ["Software Engineer"],
    "locationFilters": ["Worldwide"],
    "itemsPerPage": 20
  },
  "page": 1,
  "totalCount": 134
}
```

**使用提示**：
- 使用此状态对象在下次调用`rrjobs`时无需用户重复输入搜索条件。
- 提示：如果用户稍后重新请求或定时任务触发，先调用`rr.get_last_search`获取缓存的搜索条件，然后再调用`rr_jobs`。
- 每次`rrjobs`响应都会包含`pagination`字段：
  `{ page, itemsPerPage, totalCount, totalPages, hasNextPage, hasPreviousPage }`。
- 默认值：`page: 1`, `itemsPerPage: 20`（最多50个职位）。仅接受整数；其他值将被忽略。
- 当用户请求更多职位时，增加`page`值并重新调用`rrjobs`。如果搜索条件发生变化，将`page`值重置为1。
- 使用`pagination.hasNextPage`判断是否需要再次获取职位列表，并在响应中显示剩余职位数量。

**示例后续对话**：
- 避免在对话中直接使用工具调用语句。所有工具调用操作都应在内部完成。

**工作流程速查表**：
1. **密钥提供**：如有需要，请求用户粘贴API密钥；收到密钥后，调用`rr.save_api_key`并确认“已保存 ✅”（切勿再次显示密钥）。
- **获取职位信息**：收集用户输入的搜索条件，调用`rrjobs`，渲染职位列表，并在`requestCountToday`达到800次时提醒用户请求次数限制。
- **密钥管理**：仅当用户明确请求时，执行密钥的生成/轮换/撤销/查询状态操作：请求用户的认证cookie，使用`rr.save_session_cookie`保存后，根据需要调用`rr.key_status`/`rr.rotate_key`/`rr.revoke_key`。
- **监控**：当用户请求定期检查时，使用`rr.schedule_checks`。用自然语言确认检查频率（例如：“好的 — 我将每6小时检查一次”）。

## 分页与结果显示的提示

- 维护一个轻量级的对话状态对象（包含搜索条件、当前页码、每页显示的职位数量）。
- 当用户修改搜索条件时，将`page`重置为1并重新获取职位列表。
- 如果用户请求“更多”，增加`page`值，并使用缓存的搜索条件重新获取职位列表。
- 如果用户请求“返回上一页”，将`page`值减1。
- 始终告知用户当前显示的职位数量（例如：“当前显示21–40个职位，共134个”）。

**示例后续对话**：
- 使用此状态对象在下次调用`rrjobs`时无需用户重复输入搜索条件。
- 提示：如果用户稍后重新请求或定时任务触发，先调用`rr.get_last_search`获取缓存的搜索条件，然后再调用`rrjobs`。
- 每次`rrjobs`响应都会包含`pagination`字段：
  `{ page, itemsPerPage, totalCount, totalPages, hasNextPage, hasPreviousPage }`。
- 默认值：`page: 1`, `itemsPerPage: 20`（最多50个职位）。仅接受整数；其他值将被忽略。
- 当用户请求相同条件的更多职位时，增加`page`值并重新调用`rrjobs`。如果搜索条件发生变化，将`page`值重置为1。
- 使用`pagination.hasNextPage`判断是否需要再次获取职位列表，并在响应中显示剩余职位数量。

**工作流程速查表**：
1. **密钥提供**：
   - 如有需要，请求用户粘贴API密钥；收到密钥后，调用`rr.save_api_key`并确认“已保存 ✅”（切勿再次显示密钥）。
   - 如果用户后续需要自动管理密钥，请求用户的认证cookie，并使用`rr.save_session_cookie`保存（切勿再次显示cookie）。
2. **获取职位信息**：
   - 在内部调用`rr.jobs`，加载保存的密钥并显示职位列表。在响应中显示职位数量。
   - 使用模板渲染职位卡片，并在需要时提示“显示X–Y个职位（输入‘more’可获取下一页）”。
3. **密钥管理**：
   - 根据用户请求执行密钥的生成/轮换/撤销/查询操作：
     - 使用`rr.key_status`、`rr.generate_key`、`rr.rotate_key`或`rr.revoke_key`（都需要保存的cookie，并自动保存新的API密钥）。
4. **定时检查**：
   - 在成功调用`rr_jobs`后，自动保存当前的搜索条件和每页显示的职位数量。如果用户同意定期检查，使用`hourly|6h|12h|daily|off`作为频率。
   - 使用定时任务创建系统事件（例如`RR_CHECK:<jobId>`）。当系统事件触发时，立即调用`rr.get_last_search`更新搜索条件，然后再次调用`rr_jobs`。
   - 根据`stats.newCount`和`newJobOpenings`数组决定是否通知用户。仅当有新职位时通过私信通知用户（例如：“显示前3–5个职位，输入‘more’可获取更多职位”）。
   - 如果用户请求停止监控，使用`rr.schedule_checks`取消定时任务并清除监控状态。
5. **高级设置**：如果需要自定义检查频率，可以使用`everyMs`（例如60000）。

**处理`RR_CHECK`事件**：
- 定时任务会生成`RR_CHECK:<jobId>`格式的系统事件。即使用户没有请求，也要响应该事件。
- 调用`rr.get_last_search`，然后调用`rr_jobs`并仅通过私信通知新职位信息（`stats.newCount > 0`）。
- 如果`newCount`为0，简单回复“上次检查后没有新职位”。

**示例助手对话**：
> “🪐 已获取20个新的职位信息。提醒：您的Remote Rocketship订阅计划允许每天请求1,000次，您已经使用了610次。”

**质量检查清单**：
- 确保401/403/429错误代码能返回正确的提示信息。
- 在调用API之前，拒绝请求超过50个职位的请求。
- 确保职位卡片遵循Remote Rocketship的格式（标题加粗、使用表情符号、两行摘要）。
- 手动检查`.env`文件中的敏感信息存储和密钥管理流程。