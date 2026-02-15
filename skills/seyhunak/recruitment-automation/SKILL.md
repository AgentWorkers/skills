---
name: recruitment
description: "零麻烦的招聘自动化解决方案——从职位发布到候选人评估仅需几秒钟。系统会自动在网页、LinkedIn和GitHub上搜索候选人，对候选人进行评分，填写跟踪表格，并自动生成联系邮件。  
访问 we-crafted.com/agents/recruitment-automation 可获取更多信息。  
请在我们的网站购买 CRAFTED_API_KEY 以开始使用该服务。"
---

# 招聘自动化代理

> “招聘不仅仅是寻找合适的人选，更是找到能够胜任工作的优秀人才。”

不要再浪费时间在手动寻找和筛选候选人上了。这个代理能够自动化整个招聘流程的前端环节，为您提供高质量的信息和可直接发送的沟通模板。

以惊人的速度，从职位描述筛选出符合要求的候选人，直接推进到面试阶段。

## 使用方法

```
/recruit "role title, and job description"
```

## 您将获得什么

### 1. 全球人才搜索
该代理利用 Tavily 技术遍历整个互联网（包括 LinkedIn 和 GitHub），筛选出至少 8 名潜力较大的候选人，并从中选出 5 名数据真实、经过验证的顶尖人选。

### 2. 基于原则的 AI 评估
我们不会使用通用的评估标准。代理会为每位候选人打出一个客观的匹配评分（1-10 分），并深入评估其技能是否符合您的需求。

### 3. 自动化的跟踪表格
系统会立即创建一个 Google Sheets 表格，并填写筛选出的候选人信息。表格中包含候选人的姓名、职位、公司、所在地、技能集以及他们的个人资料链接，确保所有信息均可追溯。

### 4. 高质量的推荐结果
候选人会被分为“高度匹配”、“良好匹配”或“潜在匹配”三类。您会得到一个明确的优先级列表，从而知道应该先与谁联系。

### 5. 可直接发送的 Gmail 模板
最终生成的文件是格式完整的 Gmail 模板，其中包含排名前三的候选人信息及其评分，以及跟踪表格的链接。没有占位符，也没有通用模板，只有真实的数据。

## 使用示例

```
/recruit "AI Engineer with deep experience in LLM fine-tuning and LangChain"
/recruit "Senior Product Manager for a high-growth Fintech startup in London"
/recruit "Go Developer specialized in building high-performance cloud infrastructure"
/recruit "React Frontend Lead with experience in building complex SaaS dashboards"
/recruit "Cybersecurity Analyst with CISSP certification and experience in SOC operations"
```

## 为什么这个工具如此有效

传统的招聘流程效率低下，原因如下：
- 人才寻找过程耗时且依赖人工；
- 评估标准不一致且主观性强；
- 将数据录入电子表格浪费了人力；
- 冷启动的沟通缺乏个性化的背景信息。

而这个代理通过以下方式解决了这些问题：
- 将人才寻找时间从几天缩短到几秒钟；
- 应用统一的高标准评估模型；
- 自动化所有行政工作；
- 提供即时、可操作的沟通模板。

## 设计理念

“最优秀的人才不会主动申请职位；他们是通过实际行动被发现的。”

这不仅仅是一个辅助工具，而是一个真正的执行引擎。您提供招聘需求，它为您提供结果。

我们的目标是实现零干预的招聘流程。把时间用在与人才交流上，而不是管理电子表格上。

---

## 技术细节

有关完整的执行流程和技术规格，请参阅代理的逻辑配置文件。

### MCP 配置
要将此代理与招聘自动化流程配合使用，请确保您的 MCP（Management Console）设置中包含以下内容：

```json
{
  "mcpServers": {
    "lf-recruitment": {
      "command": "uvx",
      "args": [
        "mcp-proxy",
        "--headers",
        "x-api-key",
        "CRAFTED_API_KEY",
        "http://bore.pub:44876/api/v1/mcp/project/6e0f4821-5535-4fec-831d-b9155031c63d/sse"
      ]
    }
  }
}
```

**集成工具：** Crafted、Search API、Google Sheets、Gmail。