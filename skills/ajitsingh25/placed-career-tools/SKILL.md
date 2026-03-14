---
name: placed-career-tools
description: >
  当用户需要执行以下操作时，应使用此技能：  
  - “跟踪职位申请”  
  - “将简历与职位匹配”  
  - “生成求职信”  
  - “根据职位要求优化简历”  
  - “获取公司的面试问题”  
  - “创建领英个人资料”  
  - “提交职位申请”  
  - “查询申请状态”  
  - “了解薪资信息”  
  - “协商薪资”  
  - “调研公司情况”  
  - “分析简历中的不足之处”  
  - 或者希望使用 Placed 平台（placed.exidian.tech）提供的 AI 职业发展工具。
version: 1.0.0
homepage: https://placed.exidian.tech
metadata: {"openclaw":{"emoji":"🧭","homepage":"https://placed.exidian.tech","requires":{"env":["PLACED_API_KEY"]},"primaryEnv":"PLACED_API_KEY"}}
---
# Placed Career Tools

Placed Career Tools 提供了一套全面的人工智能职业发展工具，涵盖求职全过程：职位跟踪、简历与职位匹配、求职信生成、LinkedIn个人资料优化、薪资信息查询、谈判策略制定以及公司信息研究——所有这些功能均通过 Placed MCP 服务器实现。

## 概述

Placed Career Tools 覆盖了求职的整个流程。您可以通过该工具跟踪申请进度、将简历与职位描述进行匹配、生成定制的求职信、研究公司信息、对比薪资水平，并准备谈判策略——所有这些操作都由人工智能助手完成。

## 先决条件

1. 在 https://placed.exidian.tech 上创建一个账户。
2. 从“设置”（Settings）→“API 密钥”（API Keys）中获取您的 API 密钥。
3. 安装 Placed MCP 服务器：

```json
{
  "mcpServers": {
    "placed": {
      "command": "npx",
      "args": ["-y", "@exidian/placed-mcp"],
      "env": {
        "PLACED_API_KEY": "your-api-key-here",
        "PLACED_BASE_URL": "https://placed.exidian.tech"
      }
    }
  }
}
```

## 可用工具

### 职位跟踪

| 工具                        | 功能描述                                      |
| --------------------------- | ----------------------------------------- |
| `add_job_application`       | 向跟踪系统添加新的职位申请                   |
| `list_job_applications`     | 查看您的所有申请进度                         |
| `update_job_status`         | 将申请状态更新至新的阶段                         |
| `get_application_analytics` | 查看申请流程的详细分析和转化率                   |

### 人工智能职业发展工具

| 工具                           | 功能描述                                      |
| ------------------------------ | ---------------------------------------------------- |
| `match_job`                    | 评估您的简历与职位描述的匹配程度                   |
| `analyze_resume_gaps`          | 查找目标职位所需的关键词和技能                   |
| `generate_cover_letter`        | 生成个性化的求职信                         |
| `optimize.resume_for_job`      | 根据职位要求优化简历内容                     |
| `generate_interview_questions` | 生成针对该公司/职位的面试问题                   |
| `generate_linkedin_profile`    | 生成优化后的 LinkedIn 个人资料标题和简介部分           |

### 薪资与谈判

| 工具                          | 功能描述                                       |
| ----------------------------- | ------------------------------------------------- |
| `get_salary_insights`         | 提供按职位、公司和地区划分的薪资市场数据             |
| `generate_negotiation_script` | 生成个性化的薪资谈判策略                     |

### 公司研究

| 工具               | 功能描述                                         |
| ------------------ | --------------------------------------------------- |
| `research_company` | 提供公司概况、企业文化、新闻及面试技巧                   |

## 快速入门

### 跟踪职位申请

```
add_job_application(
  company="Stripe",
  role="Senior Software Engineer",
  job_url="https://stripe.com/jobs/...",
  status="applied",
  resume_id="res_abc123"
)
```

### 匹配简历与职位

```
match_job(
  resume_id="res_abc123",
  job_description="Senior Software Engineer at Stripe — distributed systems, Go, Kubernetes..."
)
# Returns: match score, matched keywords, missing keywords, recommendations
```

### 生成求职信

```
generate_cover_letter(
  resume_id="res_abc123",
  company="Airbnb",
  role="Staff Engineer",
  job_description="...",
  tone="professional"
)
```

### 获取薪资信息

```
get_salary_insights(
  role="Senior Software Engineer",
  company="Google",
  location="San Francisco, CA",
  years_experience=6
)
# Returns: salary range, percentiles, bonus, equity, total comp
```

### 生成谈判策略

```
generate_negotiation_script(
  current_offer=200000,
  target_salary=240000,
  role="Senior Software Engineer",
  company="Stripe",
  justifications=[
    "6 years distributed systems experience",
    "Led 3 high-impact projects at previous company",
    "Market rate for this role in SF is $230-260K"
  ]
)
```

### 研究公司

```
research_company(
  company_name="Databricks",
  include_interview_tips=true
)
# Returns: culture, recent news, funding, employee ratings, interview style
```

## 申请流程阶段

`update_job_status` 的标准阶段包括：

- `wishlist` — 保存以备后续处理
- `applied` — 申请已提交
- `phone_screen` — 初步面试电话
- `technical` — 技术面试环节
- `onsite` — 现场面试或最终面试
- `offer` — 收到录用通知
- `negotiating` — 谈判阶段
- `accepted` — 接受录用通知
- `rejected` — 申请被拒绝
- `withdrawn` — 申请被撤回

## 常见工作流程

**申请新职位：**
1. 使用 `research_company` 了解公司文化和面试风格。
2. 使用 `match_job` 评估简历与职位的匹配程度。
3. 使用 `analyze_resume_gaps` 查找简历中缺失的关键词和技能。
4. 使用 `optimize_resume_for_job` 优化简历内容。
5. 使用 `generate_cover_letter` 生成求职信。
6. 使用 `add_job_application` 追踪申请进度。

**准备面试：**
1. 使用 `research_company` 了解公司文化和近期新闻。
2. 使用 `generate_interview_questions` 生成可能的面试问题。
3. 可以使用 `placed-interview-coach` 进行模拟面试练习。

**谈判录用通知：**
1. 使用 `get_salary_insights` 获取薪资参考数据。
2. 根据实际情况选择合适的谈判策略（保守型、平衡型或激进型）。
3. 使用 `generate_negotiation_script` 准备谈判内容。

**跟踪申请进度：**
1. 使用 `list_job_applications` 查看所有申请情况。
2. 随着申请进展更新 `update_job_status`。
3. 使用 `get_application_analytics` 分析申请转化率并找出瓶颈。

## 提示：

- 提交申请后立即添加相关记录——完整的申请信息有助于更有效地进行跟踪。
- 在申请前先使用 `match_job` 评估简历的匹配度，优先处理匹配度高的职位。
- 确保简历信息更新完成后再使用 `generate_linkedin_profile`。
- 指定公司、地区和工作经验年限后，`get_salary_insights` 可提供更准确的薪资数据。
- 在使用 `optimize_resume_for_job` 之前，先使用 `analyze_resume_gaps` 了解简历的不足之处。

## 额外资源

- **`references/api-guide.md`** — 完整的 API 参考文档，包含所有参数和响应格式。
- **Placed Job Tracker** — https://placed.exidian.tech/jobs
- **Placed Career Hub** — https://placed.exidian.tech/career