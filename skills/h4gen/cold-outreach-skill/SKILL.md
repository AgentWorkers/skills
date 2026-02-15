---
name: cold-outreach-hunter
description: **元技能：**  
用于将 Apollo API、LinkedIn API、YC Cold Outreach 和 MachFive Cold Email 集成到一个完整的 B2B 冷拓展（cold outreach）流程中。适用于需要端到端的需求获取（lead sourcing）、数据丰富化（data enrichment）、个性化沟通策略（personalized communication strategies），以及生成即用的拓展序列（generation-ready outreach sequences）的场景，同时确保流程具备严格的质量控制和安全保障机制。
homepage: https://clawhub.ai
user-invocable: true
disable-model-invocation: false
metadata: {"openclaw":{"emoji":"dart","requires":{"bins":["python3","npx"],"env":["MATON_API_KEY","MACHFIVE_API_KEY"],"config":[]},"note":"Requires local installation of apollo-api, linkedin-api, yc-cold-outreach, and cold-email."}}
---

## 目的

执行一个完整的B2B冷启动外联工作流程，从ICP（目标客户群体）定义到生成可发送的邮件序列。

**主要目标：**
- 筛选出符合要求的潜在客户。
- 丰富潜在客户的背景信息，以便进行个性化沟通。
- 生成简洁、非销售性质的邮件内容，以提高回复率。
- 为外部发送/调度系统提供可立即使用的邮件内容。

这是一个协调其他工具的工作流程，它并不替代这些工具的功能。

## 所需安装的技能

- `apollo-api`（最新版本：`1.0.5`）
- `linkedin-api`（最新版本：`1.0.2`）
- `yc-cold-outreach`（最新版本：`1.0.1`）
- `cold-email`（MachFive Cold Email，最新版本：`1.0.5`）

使用ClawHub进行安装/更新：

```bash
npx -y clawhub@latest install apollo-api
npx -y clawhub@latest install linkedin-api
npx -y clawhub@latest install yc-cold-outreach
npx -y clawhub@latest install cold-email
npx -y clawhub@latest update --all
```

**验证是否已安装：**

```bash
npx -y clawhub@latest list
```

如果缺少任何所需的技能，请停止操作并报告具体的安装命令。

## 所需的凭证

- `MATON_API_KEY`（用于`apollo-api`和`linkedin-api`，通过Maton网关访问）
- `MACHFIVE_API_KEY`（用于`cold-email`）

**前置检查：**

```bash
echo "$MATON_API_KEY" | wc -c
echo "$MACHFIVE_API_KEY" | wc -c
```

如果缺少或为空任何凭证，请在处理潜在客户之前停止操作。

## 工作流程模板

在执行前收集以下信息：

- **产品/服务**：要销售的内容（例如：设计服务）
- **ICP标题**：目标职位（例如：首席营销官）
- **ICP行业**：目标行业（例如：SaaS）
- **ICP位置**：目标地点（例如：柏林）
- **目标潜在客户数量**（例如：50个）
- **活动目标**：回复、会议、推荐、审计请求等
- **支持材料**：案例研究、数据指标、社交证明
- **语言风格要求**：使用平实的英语，简洁明了，非销售性质
- **活动ID**：`machfive_campaign`
- **执行模式**：仅生成草稿或生成可发送的邮件

在明确这些信息之前，不要开始编写邮件内容。

## 工具职责

### Apollo API (`apollo-api`)

用于发现潜在客户并对其进行基本信息补充。

**相关操作：**
- 搜索人员：`POST /apollo/v1/mixed_people/api_search`
- 搜索条件包括：
  - `q_person_title`（职位名称）
  - `person_locations`（位置）
  - `q_organization_name`（组织名称）
  - `q_keywords`（关键词）
- 通过电子邮件或LinkedIn链接补充人员信息：`POST /apollo/v1/people/match`
- 支持分页功能（`page`和`per_page`）
- 使用Maton网关，可选`Maton-Connection`头部

**此阶段的主要输出：**  
初始潜在客户列表，包含职位、公司名称及LinkedIn链接（如可用）

### LinkedIn API (`linkedin-api`)

用于获取LinkedIn上的相关背景信息。

**相关操作：**
- 认证后的个人资料/用户信息接口
- 发布内容/帖子的API（`ugcPosts`）以及组织帖子/统计信息API
- 需要`MATON_API_KEY`和LinkedIn协议头部

**重要说明：**  
- 该工具不是用于抓取任意第三方个人资料或最近发布的个人帖子的通用工具。  
- 如果工作流程需要针对每个潜在客户进行深入的个人帖子补充，请标记为“需要额外工具”。

### YC Cold Outreach (`yc-cold-outreach`)

用作编写邮件策略的框架，而非用于发送邮件的工具。

**核心原则：**
- 每封邮件只有一个目标
- 语言风格要自然、亲切
- 个性化内容要真实可靠
- 文章简洁易读，适合移动设备阅读
- 使用清晰、易于理解的呼吁行动（CTA）

### MachFive Cold Email (`cold-email`)

根据准备好的潜在客户信息生成邮件序列。

**相关操作：**
- 需要提供活动ID（`campaign_id`）才能生成邮件序列。
- 单个潜在客户的邮件生成可能需要几分钟；请设置较长的超时时间。
- 批量异步生成（`/generate-batch`）会返回`list_id`；完成后需要查询状态并导出结果。
- 需要提供潜在客户的电子邮件地址。
- 支持按步骤生成结构化的邮件内容，包括主题和正文。

## 标准工作流程

### 第1阶段：构建潜在客户列表（Apollo）

1. 使用Apollo查询符合条件的潜在客户（例如：柏林地区的SaaS行业首席营销官）。
2. 继续搜索，直到达到目标潜在客户数量或达到质量标准。
3. 将每条潜在客户记录转换为所需的格式。
4. 如果要求生成可发送的邮件（MachFive需要电子邮件地址），则丢弃没有电子邮件地址的记录。

**推荐的潜在客户信息格式：**

```json
{
  "lead_id": "apollo-or-derived-id",
  "name": "Anna Example",
  "title": "Chief Marketing Officer",
  "company": "Startup GmbH",
  "location": "Berlin",
  "email": "anna@startup.com",
  "linkedin_url": "https://linkedin.com/in/...",
  "source": "apollo-api"
}
```

### 第2阶段：丰富个性化信息

1. 尝试使用LinkedIn API补充潜在客户的背景信息。
2. 如果无法直接获取个人帖子信息，将该字段标记为`not_available`。
3. 可以根据Apollo提供的信息（公司名称、职位、关键词、行业背景）进一步丰富潜在客户的资料，以避免虚假的个性化内容。

**每个潜在客户的个性化信息对象：**

```json
{
  "icebreaker": "not_available_or_verified_fact",
  "pain_hypothesis": "Likely CRO bottleneck in paid landing pages",
  "proof_hook": "Helped X improve conversion by Y%",
  "confidence": 0.0
}
```

**硬性规则：**
- 不要虚构任何帖子内容、客户兴趣或报价。

### 第3阶段：制定邮件策略（基于YC框架）

在生成邮件内容之前，为每个潜在客户制定策略：

- **问题**：该职位可能面临的具体问题
- **解决方案**：你的产品/服务能解决什么问题
- **证据**：一个具体的数据指标或客户反馈
- **呼吁行动**：下一步该采取的行动

**遵循YC框架的要求：**
- 每封邮件只有一个核心诉求
- 语言简洁，适合移动设备阅读
- 个性化内容要基于真实的信息

### 第4阶段：生成邮件序列（MachFive）

1. 首先获取活动ID（如果未提供，请使用`GET /api/v1/campaigns`）。
2. 提交包含电子邮件地址的潜在客户信息。
- 对于大量潜在客户，建议批量处理；完成后需要查询状态。
3. 将结果导出为JSON格式，并将邮件序列与潜在客户ID关联起来。

**生成邮件内容所需的信息：**
- 包括`name`（姓名）、`title`（职位）、`company`（公司名称）、`email`（电子邮件地址）
- 如果可用，包括`linkedin_url`（LinkedIn链接）和`company_website`（公司网站）
- 有意识地设置`email_count`（通常为3条）
- 使用与活动目标一致的可批准呼吁行动（CTA）

### 第5阶段：质量检查和决策

在宣布邮件内容准备好之前，验证每个邮件序列：
- 确认个性化信息的真实性
- 检查是否符合YC框架的要求（语言自然、简洁、只有一个呼吁行动）
- 检查使用的信息是否真实（姓名/公司/职位正确）
- 确认没有虚假的宣传内容

任何失败的邮件序列都必须标记为“需要修订”。

### 第6阶段：调度和发送

这个流程仅输出可发送的邮件建议，不自动执行发送操作。

如果用户要求优化发送时间（例如：周二10:00），则将其作为调度建议返回。

**示例发送建议对象：**

```json
{
  "lead_id": "...",
  "sequence_status": "approved",
  "suggested_send_time_local": "Tuesday 10:00",
  "timezone": "Europe/Berlin",
  "send_system": "external",
  "notes": "Timing is recommendation-only; execution tool must schedule/send."
}
```

## 因果链（场景映射）

以“向初创公司的营销负责人销售设计服务”为例：

1. Apollo返回目标潜在客户列表（例如：柏林地区的50位首席营销官）。
2. 使用LinkedIn API补充每个潜在客户的背景信息。
3. YC框架将潜在客户的信息转化为清晰的“问题→解决方案→证据→呼吁行动”结构。
4. MachFive根据验证后的信息生成多步骤的邮件序列。
5. 代理输出：
  - 经过审核的邮件序列
  - 每条邮件的质量评分
  - 发送建议（例如：周二10:00）

## 输出内容

始终返回以下信息：

- **潜在客户总结**：
  - 提交的潜在客户数量与符合条件的潜在客户数量
  - 被拒绝的原因（缺少电子邮件地址、不符合条件、重复）

- **信息补充总结**：
  - 成功补充的信息字段
  - 无法补充的信息字段及其原因

- **邮件序列包**：
  - 每个潜在客户对应的邮件序列，包含每一步的主题和正文
  - 质量检查状态（“已批准”或“需要修订”）

- **执行计划**：
  - 发送时间建议
  - 所需的外部发送工具/调度系统
  - 需要解决的障碍（例如：缺少活动ID、API密钥、缺少电子邮件地址）

## 安全准则

- 绝不要虚构个性化信息。
- 除非有来源和可验证的证据，否则不要声称潜在客户发布了某些内容。
- 在未确定活动ID之前，不要开始生成邮件序列。
- 如果呼吁行动不明确或存在多个诉求，不要将邮件序列标记为“已批准”。
- 语言要自然，符合外联政策。

## 故障处理**

- 如果缺少`MATON_API_KEY`，停止使用Apollo/LinkedIn相关操作。
- 如果缺少`MACHFIVE_API_KEY`，停止邮件生成流程，并返回仅生成草稿的方案。
- 如果缺少活动ID，列出所有可用的活动并请求用户明确选择。
- 如果批量处理超时或部分内容生成失败，继续通过查询状态和导出功能进行恢复。
- 如果潜在客户质量不足，返回质量较高的潜在客户列表，而不是强行生成大量邮件。

## 来自上游工具的已知限制

- `linkedin-api`的功能有限，不能随意抓取个人用户的全部信息。
- `cold-email`可以生成邮件序列，但不保证邮件的发送和调度。
- `apollo-api`提供搜索和信息补充功能；电子邮件是否能够成功送达可能需要额外的工具。

在规划和报告中请将这些限制作为明确的约束条件。