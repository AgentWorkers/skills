# MCP技能：求职搜索

该技能使AI代理能够使用**JobSpy MCP服务器**在多个招聘网站上搜索职位。JobSpy将来自LinkedIn、Indeed、Glassdoor、ZipRecruiter、Google Jobs、Bayt、Naukri和BDJobs的职位信息汇总到一个统一的界面中。

## 何时使用此技能

当用户要求您执行以下操作时，请使用此技能：
- 根据特定条件（职位类型、地点、公司等）查找职位信息
- 搜索远程或现场职位
- 比较不同平台上的职位机会
- 获取职位的薪资信息
- 查找最近发布的职位（在X小时内）
- 搜索提供“简单申请”功能的职位

## 先决条件

- **Python 3.10+**
- **Node.js 16+**（用于某些服务器实现）
- 已安装并配置了JobSpy MCP服务器

---

## 安装与设置

### 选项1：Python MCP服务器（推荐）

```bash
# Install with pip
pip install mcp>=1.1.0 python-jobspy>=1.1.82 pandas>=2.1.0 pydantic>=2.0.0

# Or install with uv (faster)
uv add mcp python-jobspy pandas pydantic
```

### 选项2：克隆预构建的服务器

```bash
# Clone the jobspy-mcp-server repository
git clone https://github.com/chinpeerapat/jobspy-mcp-server.git
cd jobspy-mcp-server

# Install dependencies
uv sync
# or
pip install -e .
```

### Claude桌面配置

将以下内容添加到您的Claude桌面配置文件中（macOS上的`~/Library/Application Support/Claude/claude_desktop_config.json`）：

```json
{
  "mcpServers": {
    "jobspy": {
      "command": "uv",
      "args": ["run", "jobspy-mcp-server"],
      "env": {}
    }
  }
}
```

**替代配置（Node.js服务器）：**

```json
{
  "mcpServers": {
    "jobspy": {
      "command": "node",
      "args": ["/path/to/jobspy-mcp-server/src/index.js"],
      "env": {
        "ENABLE_SSE": "0"
      }
    }
  }
}
```

---

## MCP工具规范

### 1. `scrape_jobs_tool`（主要工具）

在多个招聘网站上搜索职位，并提供全面的筛选功能。

**参数：**

| 参数 | 类型 | 是否必填 | 默认值 | 描述 |
|-----------|------|----------|---------|-------------|
| `search_term` | 字符串 | ✅ 是 | - | 职位关键词（例如：“软件工程师”、“数据科学家”） |
| `location` | 字符串 | 否 | - | 职位地点（例如：“旧金山，CA”、“远程”） |
| `site_name` | 数组 | 否 | `["indeed", "linkedin", "zip_recruiter", "google"]` | 要搜索的招聘网站 |
| `results_wanted` | 整数 | 否 | 15 | 结果数量（1-1000） |
| `job_type` | 字符串 | 否 | - | 雇用类型：`fulltime`（全职）、`parttime`（兼职）、`internship`（实习）、`contract`（合同） |
| `is_remote` | 布尔值 | 否 | false | 仅筛选远程职位 |
| `hours_old` | 整数 | 否 | - | 按发布时间筛选（以小时为单位） |
| `distance` | 整数 | 否 | 50 | 搜索半径（以英里为单位，1-100） |
| `easy_apply` | 布尔值 | 否 | false | 筛选提供“简单申请”功能的职位 |
| `country_indeed` | 字符串 | 否 | "usa" | Indeed/Glassdoor搜索的国家 |
| `linkedin_fetch_description` | 布尔值 | 否 | false | 获取完整的LinkedIn职位描述（速度较慢） |
| `offset` | 整数 | 否 | 0 | 分页偏移量 |
| `verbose` | 整数 | 否 | 1 | 日志级别（0=错误，1=警告，2=全部） |

**`site_name`的支持值：**
- `linkedin` - 专业社交平台（使用有频率限制） |
- `indeed` - 最大的求职引擎（最可靠） |
- `glassdoor` - 提供公司评价和薪资信息的职位 |
- `zip_recruiter` | 适用于美国/加拿大的职位匹配服务 |
- `google` | 招聘信息汇总平台 |
- `bayt` | 中东地区的招聘门户 |
- `naukri` | 印度的领先招聘门户 |
- `bdjobs` | 孟加拉国的招聘门户 |

**`job_type`的支持值：**
- `fulltime`（全职）
- `parttime`（兼职）
- `internship`（实习）
- `contract`（合同）

### 2. `get_supported_countries`

返回支持职位搜索的所有国家列表。无需参数。

### 3. `get_supported_sites`

返回关于所有支持招聘网站平台的详细信息。无需参数。

### 4. `get_job_search_tips`

返回有效的求职搜索技巧和最佳实践。无需参数。

---

## 职位信息响应规范

当返回职位信息时，每个职位条目包含以下字段：

```typescript
interface JobPost {
  // Core fields (all platforms)
  title: string;                    // Job title
  company: string;                  // Company name
  company_url?: string;             // Company website URL
  job_url: string;                  // Direct link to job posting
  location: {
    country?: string;
    city?: string;
    state?: string;
  };
  is_remote: boolean;               // Whether job is remote
  description?: string;             // Job description (markdown format)
  job_type?: "fulltime" | "parttime" | "internship" | "contract";
  
  // Salary information
  salary?: {
    interval?: "yearly" | "monthly" | "weekly" | "daily" | "hourly";
    min_amount?: number;
    max_amount?: number;
    currency?: string;
    salary_source?: "direct_data" | "description";  // Parsed from posting
  };
  
  date_posted?: string;             // ISO date string
  emails?: string[];                // Contact emails if available
  
  // LinkedIn specific
  job_level?: string;               // Seniority level
  
  // LinkedIn & Indeed specific
  company_industry?: string;
  
  // Indeed specific
  company_country?: string;
  company_addresses?: string[];
  company_employees_label?: string;
  company_revenue_label?: string;
  company_description?: string;
  company_logo?: string;
  
  // Naukri specific
  skills?: string[];
  experience_range?: string;
  company_rating?: number;
  company_reviews_count?: number;
  vacancy_count?: number;
  work_from_home_type?: string;
}
```

---

## 示例提示 → MCP调用 → 输出

### 示例1：基本职位搜索

**用户提示：**
> “在旧金山查找10个软件工程师的职位”

**MCP工具调用：**
```json
{
  "tool": "scrape_jobs_tool",
  "params": {
    "search_term": "software engineer",
    "location": "San Francisco, CA",
    "results_wanted": 10,
    "site_name": ["indeed", "linkedin"]
  }
}
```

**预期输出：**
```json
{
  "jobs": [
    {
      "title": "Software Engineer",
      "company": "TechCorp Inc.",
      "location": { "city": "San Francisco", "state": "CA" },
      "job_url": "https://indeed.com/viewjob?jk=abc123",
      "salary": { "min_amount": 120000, "max_amount": 180000, "interval": "yearly" },
      "job_type": "fulltime",
      "is_remote": false
    }
    // ... more jobs
  ],
  "total_found": 10
}
```

---

### 示例2：远程职位搜索

**用户提示：**
> “在Indeed和ZipRecruiter上搜索远程Python开发人员的职位”

**MCP工具调用：**
```json
{
  "tool": "scrape_jobs_tool",
  "params": {
    "search_term": "Python developer",
    "location": "Remote",
    "is_remote": true,
    "site_name": ["indeed", "zip_recruiter"],
    "results_wanted": 20
  }
}
```

---

### 示例3：带有筛选条件的最近职位

**用户提示：**
> “查找过去24小时内发布的波士顿数据科学家职位”

**MCP工具调用：**
```json
{
  "tool": "scrape_jobs_tool",
  "params": {
    "search_term": "data scientist",
    "location": "Boston, MA",
    "hours_old": 24,
    "site_name": ["linkedin", "glassdoor", "indeed"],
    "linkedin_fetch_description": true
  }
}
```

---

### 示例4：提供“简单申请”功能的初级职位

**用户提示：**
> “查找纽约提供“简单申请”功能的初级市场营销职位”

**MCP工具调用：**
```json
{
  "tool": "scrape_jobs_tool",
  "params": {
    "search_term": "junior marketing",
    "location": "New York, NY",
    "job_type": "fulltime",
    "easy_apply": true,
    "site_name": ["indeed", "zip_recruiter"],
    "results_wanted": 30
  }
}
```

---

### 示例5：国际职位搜索

**用户提示：**
> “在Indeed上查找德国的软件职位”

**MCP工具调用：**
```json
{
  "tool": "scrape_jobs_tool",
  "params": {
    "search_term": "software developer",
    "location": "Berlin",
    "country_indeed": "germany",
    "site_name": ["indeed"],
    "results_wanted": 15
  }
}
```

---

### 示例6：获取帮助信息

**用户提示：**
> “支持哪些招聘网站？”

**MCP工具调用：**
```json
{
  "tool": "get_supported_sites",
  "params": {}
}
```

**预期输出：**
```json
{
  "sites": [
    { "name": "indeed", "description": "Largest job search engine, most reliable" },
    { "name": "linkedin", "description": "Professional networking platform, rate limited" },
    { "name": "glassdoor", "description": "Jobs with company reviews and salaries" },
    { "name": "zip_recruiter", "description": "Job matching for US/Canada" },
    { "name": "google", "description": "Aggregated job listings" },
    { "name": "bayt", "description": "Middle East job portal" },
    { "name": "naukri", "description": "India's leading job portal" },
    { "name": "bdjobs", "description": "Bangladesh job portal" }
  ]
}
```

---

## 错误处理示例

### 错误1：频率限制

**场景：**LinkedIn返回频率限制错误。

**错误响应：**
```json
{
  "error": "RateLimitError",
  "message": "LinkedIn rate limit exceeded. Try again later or use different sites.",
  "suggestion": "Switch to Indeed or ZipRecruiter which have more lenient rate limits."
}
```

**处理方法：**
- 将`results_wanted`减少到较小的数值（10-15）
- 暂时从`site_name`中移除`linkedin`
- 在搜索之间添加延迟
- 如果可用，使用代理配置

---

### 错误2：未找到结果

**场景：**搜索返回空结果。

**错误响应：**
```json
{
  "jobs": [],
  "total_found": 0,
  "message": "No jobs found matching your criteria"
}
```

**处理方法：**
- 扩大搜索关键词的范围（例如，使用“engineer”而不是“senior principal software engineer”）
- 增加`distance`的搜索半径
- 移除`hours_old`或`job_type`等限制性筛选条件
- 尝试不同的`site_name`选项
- 检查地点拼写是否正确

---

### 错误3：无效的国家代码

**场景：**用户指定了Indeed不支持的国家。

**错误响应：**
```json
{
  "error": "ValidationError",
  "message": "Invalid country_indeed value. Use get_supported_countries to see valid options."
}
```

**处理方法：**
- 调用`get_supported_countries`获取有效的国家代码
- 使用准确的国家名称（例如，使用“usa”而不是“US”，“united kingdom”而不是“UK”）

---

### 错误4：平台特定限制冲突

**场景：**用户尝试使用相互冲突的筛选条件。

**已知限制：**
- **Indeed**：只能使用以下选项中的一个：`hours_old`、`job_type & is_remote`、`easy_apply`
- **LinkedIn**：只能使用以下选项中的一个：`hours_old`、`easy_apply`

**处理方法：**
- 告知用户相关限制
- 优先考虑最重要的筛选条件
- 如果需要多个筛选条件，分别进行搜索

---

## 应避免的做法

### ❌ **不要**：请求过多的结果

**原因：**同时从太多网站请求过多结果会触发频率限制并导致超时。

**✅ **应该**：**

---

### ❌ **不要**：过度使用LinkedIn

**原因：**LinkedIn的频率限制最为严格。使用`linkedin_fetch_description: true`会增加请求次数。

**✅ **应该**：
- 将LinkedIn作为主要信息来源
- 将LinkedIn的结果数量限制在10-15个以内
- 仅在必要时启用`linkedin_fetch_description`

---

### ❌ **不要**：使用相互冲突的筛选条件

**原因：**Indeed只支持以下选项中的一个：`hours_old`、`job_type & is_remote`或`easy_apply`。

**✅ **应该**：

---

### ❌ **不要**：进行模糊的搜索

**原因：**模糊的搜索会导致结果质量低下，并浪费API调用。

**✅ **应该**：
- 始终包含具体的职位名称或技能要求
- 在知道地点的情况下包含地点信息
- 使用筛选条件来缩小搜索范围

---

### ❌ **不要**：忽略错误响应

**原因：**频率限制、网络问题和无效参数需要适当的处理。

**✅ **应该**：
- 在处理结果之前检查错误响应
- 实现带有重试机制的频率限制处理
- 当搜索失败时向用户提供有用的提示

---

### ❌ **不要**：使用错误的国家代码

**原因：**使用错误的国家代码会导致问题。

**✅ **应该**：
- 使用`get_supported_countries`验证有效的国家代码
- 常见的国家代码包括：“usa”、“united kingdom”、“canada”、“germany”、“india”

---

## 频率限制与最佳实践

### 平台可靠性排名

1. **Indeed** - 最可靠，适合大规模搜索
2. **ZipRecruiter** - 适用于美国/加拿大
3. **Google Jobs** - 招聘信息汇总效果好，稳定性高
4. **Glassdoor** - 提供公司评价和薪资信息
5. **LinkedIn** - 限制最多，使用要谨慎

### 推荐方法

1. **从小规模开始**：先获取10-15个结果以测试筛选条件
2. **优先使用Indeed**：职位数据最可靠
3. **具体明确**：使用针对性的搜索关键词
4. **谨慎筛选**：每次为Indeed/LinkedIn使用一个筛选条件组
5. **分页**：使用`offset`获取更多结果，而不是设置过高的`results_wanted`

---

## 支持的国家

调用`get_supported_countries`获取完整的国家列表。常见国家包括：

| 国家 | `country_indeed`的代码 |
|---------|---------------------------|
| USA | `usa` |
| United Kingdom | `united kingdom` |
| Canada | `canada` |
| Germany | `germany` |
| France | `france` |
| India | `india` |
| Australia | `australia` |
| Singapore | `singapore` |
| Japan | `japan` |
| Netherlands | `netherlands` |

---

## 故障排除

### “浏览器/Chromium未安装”

运行：`playwright install chromium`（某些抓取工具需要Chromium）

### “找不到名为‘jobspy’的模块”

运行：`pip install python-jobspy>=1.1.82`

### “超出频率限制”

- 减少`results_wanted`的数量
- 从`site_name`中移除LinkedIn
- 等待60秒后再尝试
- 考虑使用代理

---

## 快速参考

| 用户意图 | 关键参数 |
|-------------|----------------|
| 在特定城市查找职位 | `search_term`、`location` |
| 仅搜索远程职位 | `is_remote: true` |
| 最新发布的职位 | `hours_old: 24`（或48, 72） |
| 仅限全职职位 | `job_type: "fulltime"` |
| 搜索提供“简单申请”功能的职位 | `easy_apply: true` |
| 搜索特定平台 | `site_name: ["indeed"]` |
| 国际搜索 | `country_indeed: "germany"` |
| 获取更多结果 | `results_wanted: 25` |
| 分页显示结果 | `offset: 25`（在前25个结果之后） |