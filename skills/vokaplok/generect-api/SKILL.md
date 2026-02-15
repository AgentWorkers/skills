---
name: generect-api
description: 搜索B2B潜在客户和公司，通过Generect Live API查找或验证电子邮件地址。适用于用户需要根据职位、公司名称或行业来查找目标人员，或根据ICP（互联网内容提供商）信息来搜索公司的场景；同时支持从用户名+域名组合生成商务联系邮箱，以及验证电子邮件地址的功能。该服务涵盖潜在客户开发、市场开拓、信息补充（enrichment）以及电子邮件地址发现（email discovery）等业务流程。
---

# Generect Live API

提供来自LinkedIn、Crunchbase的实时B2B数据，以及基于AI的电子邮件发现服务。

**基础URL:** `https://api.generect.com`  
**认证方式:** `Authorization: Token <GENERECT_API_KEY>`

## 设置

需要设置`GENERECT_API_KEY`环境变量。您可以在 [https://beta.generect.com](https://beta.generect.com) 获取API密钥。

## 端点（Endpoints）

### 搜索潜在客户（Search Leads）
`POST /api/v1/leads/by_icp/`

通过ICP（Industry, Company, Position）过滤器查找潜在客户。返回包含工作经历、教育背景和技能的LinkedIn完整个人资料。

```json
{
  "job_title": ["CEO", "CTO"],
  "location": ["United States"],
  "industry": ["Software Development"],
  "company_headcount_range": ["11-50", "51-200"],
  "page": 1,
  "per_page": 10
}
```

**关键过滤参数:** `job_title`（职位名称）、`location`（位置）、`industry`（行业）、`company_headcount_range`（公司员工人数范围）、`company_name`（公司名称）、`seniority_level`（职位级别）、`job_function`（职位职能）。所有参数均支持数组形式。

**响应格式:** `{ "amount": N, "leads": [...] }` — 每条潜在客户信息包含 `full_name`（全名）、`headline`（职位头衔）、`job_title`（职位名称）、`company_name`（公司名称）、`company_website`（公司网站）、`jobs`（工作经历）、`educations`（教育背景）、`skills`（技能）。

### 搜索公司（Search Companies）
`POST /api/v1/companies/by_icp/`

通过ICP过滤器查找公司信息。返回包含员工人数、行业、位置和融资情况的公司资料。

```json
{
  "industry": ["Software Development"],
  "location": ["San Francisco"],
  "headcount_range": ["51-200"],
  "page": 1,
  "per_page": 10
}
```

**关键过滤参数:** `industry`（行业）、`location`（位置）、`headcount_range`（员工人数范围）、`company_type`（公司类型）、`founded_year_min`（成立年份下限）、`founded_year_max`（成立年份上限）、`keyword`（关键词）。

**响应格式:** `{ "amount": N, "companies": [...] }` — 每家公司信息包含 `name`（公司名称）、`domain`（域名）、`industry`（行业）、`headcount_range`（员工人数范围）、`headcount_exact`（确切员工人数）、`location`（位置）、`description`（公司描述）、`linkedin_link`（LinkedIn链接）、`website`（公司网站）、`founded_year`（成立年份）。

### 根据LinkedIn URL获取潜在客户信息（Get Lead by LinkedIn URL）
`POST /api/v1/leads/by_url/`

根据特定的LinkedIn URL获取对应的潜在客户完整资料。

```json
{ "url": "https://www.linkedin.com/in/username/" }
```

### 生成电子邮件（Generate Email）
`POST /api/v1/email_generator/`

根据姓名和域名生成基于AI的电子邮件地址。

**响应格式:** `{ "email": "...", "result": "valid|risky|invalid", "catch_all": bool }`

### 验证电子邮件地址（Validate Email）
`POST /api/v1/email-validator/`

**响应格式:** `{ "result": "valid|invalid|risky", "catch_all": bool, "mx_domain": "...", "exist": "yes|no" }`

## 通过curl使用API

```bash
curl -X POST https://api.generect.com/api/v1/leads/by_icp/ \
  -H "Authorization: Token $GENERECT_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"job_title":["VP Sales"],"location":["United States"],"per_page":5}'
```

## MCP服务器（替代方案）

Generect还提供MCP服务器，用于AI工具的集成：
- **远程方式:** `mcp-remote https://mcp.generect.com/mcp --header "Authorization: Bearer Token API_KEY"`
- **本地方式:** `npx -y generect-ultimate-mcp@latest`（需设置`GENERECT_API_KEY`环境变量）

可用工具：`search_leads`、`search_companies`、`generate_email`、`get_lead_by_url`、`health`

## 使用提示：

- 如果响应中的`amount`参数值为 `-1`，表示无法获取确切数量；请不断迭代请求直到结果为空。
- 潜在客户搜索端点为实时请求（可能需要5-15秒）。
- 电子邮件生成功能使用AI算法生成并验证地址；标记为`valid`的地址可以安全发送。
- 结合潜在客户搜索和电子邮件生成功能，可构建完整的潜在客户开发流程。
- 每个API密钥的使用频率受到限制（遵循相应的速率限制规则）。