---
name: generect-api
description: 搜索B2B潜在客户和公司，通过Generect Live API查找或验证电子邮件地址。适用于用户需要根据职位、公司或行业来查找目标人员，或根据ICP（Internet Content Provider）来搜索公司的场景；同时也可根据姓名+域名生成商务电子邮件地址，或验证电子邮件地址的真实性。该功能涵盖了潜在客户开发、客户信息挖掘以及电子邮件地址查找等业务流程。
---

# Generect Live API

提供来自LinkedIn、Crunchbase的实时B2B数据，以及基于AI的电子邮件发现服务。

**基础URL:** `https://api.generect.com`  
**认证方式:** `Authorization: Token <GENERECT_API_KEY>`  
**文档链接:** https://liveapi.generect.com

## 设置

需要设置`GENERECT_API_KEY`环境变量。您可以在[https://beta.generect.com](https://beta.generect.com)获取API密钥。

## API端点

### 按ICP搜索潜在客户
`POST /api/linkedin/leads/by_icp/`

通过ICP（Industry, Company, Position）过滤器查找目标人群。返回包含工作经历、教育背景和技能的LinkedIn详细信息。

**关键过滤参数：**  
`job_title`（职位名称）、`location`（地理位置）、`industry`（行业）、`company_headcount_range`（公司员工人数范围）、`seniority_level`（职位级别）、`job_function`（职位职能，以数组形式提供）。`company_name`为字符串类型（非数组）。必须至少提供`company_name`、`company_link`或`company_id`中的一个参数。

> **注意：** 此端点会实时查询LinkedIn数据，响应时间可能为15至60秒以上。

**响应格式：**  
`{ "amount": N, "leads": [...] }`  
其中，每个潜在客户的详细信息包括：`full_name`（全名）、`headline`（职位头衔）、`job_title`（职位名称）、`company_name`（公司名称）、`company_website`（公司网站）、`jobs`（工作经历）、`educations`（教育背景）、`skills`（技能列表）。

### 按ICP统计潜在客户数量
`POST /api/linkedin/leads/count/`

根据ICP过滤器统计潜在客户的数量（请求内容与搜索端点相同，不返回具体结果）。

### 按ICP搜索公司
`POST /api/linkedin/companies/by_icp/`

通过ICP过滤器查找公司信息。返回包含公司员工人数、行业、地理位置和融资情况的详细资料。

**关键过滤参数：**  
`industry`（行业）、`location`（地理位置）、`headcount_range`（公司员工人数范围）、`company_type`（公司类型）、`founded_year_min`（成立年份下限）、`founded_year_max`（成立年份上限）、`keyword`（搜索关键词）。

**响应格式：**  
`{ "amount": N, "companies": [...] }`  
其中，每家公司信息包括：`name`（公司名称）、`domain`（域名）、`industry`（行业）、`headcount_range`（员工人数范围）、`headcount_exact`（精确员工人数）、`location`（地理位置）、`description`（公司描述）、`linkedin_link`（LinkedIn公司页面链接）、`website`（公司官网）、`founded_year`（成立年份）。

### 按ICP统计公司数量
`POST /api/linkedin/companies/count/`

根据ICP过滤器统计公司的数量。

### 通过LinkedIn链接获取潜在客户信息
`POST /api/linkedin/leads/by_link/`

**响应格式：**  
返回特定LinkedIn链接对应的潜在客户详细信息。

### 通过LinkedIn链接获取公司信息
`POST /api/linkedin/companies/by_link/`

**响应格式：**  
返回特定LinkedIn公司链接对应的完整公司资料。

### 电子邮件查找器（生成电子邮件地址）
`POST /api/linkedin/email_finder/`

根据姓名和域名自动生成电子邮件地址。生成后的电子邮件地址会经过自动验证。

**响应格式：**  
`{ "email": "...", "result": "valid|risky|invalid", "catch_all": bool, "valid_email": "...", "source": "...", "mx_domain": "..." }`

### 电子邮件验证器
`POST /api/linkedin/email_validator/`

**响应格式：**  
`{ "result": "valid|invalid|risky", "catch_all": bool, "mx_domain": "...", "exist": "yes|no" }`

### 获取用户信息
`GET /api/linkedin/user/me/`

返回当前用户的个人信息和账户余额。

### 获取API使用记录
`GET /api/linkedin/transactions/`

返回所有API使用记录的列表。

## 使用方法（通过curl）

## MCP服务器（备用方案）

Generect还提供了MCP服务器，用于集成AI工具：
- **远程方式：** `mcp-remote https://mcp.generect.com/mcp --header "Authorization: Bearer Token API_KEY"`
- **本地方式：** `npx -y generect-ultimate-mcp@latest`（需设置`GENERECT_API_KEY`环境变量）

可用工具：`search_leads`、`search_companies`、`generate_email`、`get_lead_by_url`、`health`

## 使用提示：
- 响应中的`amount: -1`表示无法获取确切数量；请不断循环查询直到结果为空。
- 潜在客户搜索端点为实时查询，每次请求都会实时查询LinkedIn数据（可能需要5至15秒）。
- 电子邮件生成功能采用AI算法进行地址验证；验证通过的地址可安全使用。
- 可结合潜在客户搜索和电子邮件生成功能，构建完整的潜在客户开发流程。
- 不同API密钥等级有不同的请求频率限制。