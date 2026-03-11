---
name: freelancer-bidder
description: 在 Freelancer.com 上搜索符合您技能要求的新项目，起草个性化的投标提案，并跟踪您的投标历史记录。此工具适用于您需要寻找自由职业机会、撰写获胜的投标提案，或监控 Freelancer.com 上的新项目发布时使用。
---
# 自由职业者投标助手

自动扫描 Freelancer.com 上的匹配项目，并生成个性化的投标提案。

## 功能

- 通过关键词或技能搜索活跃的项目
- 按预算、项目类型（固定价格/按小时计费）和项目更新时间进行筛选
- 生成个性化、专业的投标提案
- 跟踪投标历史和中标率
- 根据项目预算建议最佳投标价格

## 使用方法

告知助手：
- 您的技能（例如：“Python、数据抓取、翻译”）
- 预算范围
- 提案的风格（专业/友好/简洁）

## 搜索项目

```
Find Freelancer projects for: [your skills]
Budget: $[min]-$[max]
Posted within: last [N] hours
```

助手将：
1. 通过 Freelancer API 或网络搜索获取匹配的活跃项目
2. 按相关性和预算对项目进行排序
3. 展示前 5–10 个合适的机会

## 生成投标提案

```
Draft a bid for project: [project title / URL]
My background: [brief intro]
Tone: professional
```

助手将生成一份中标几率较高的提案，内容包括：
- 个性化的开场白（针对客户的具体需求）
- 您的相关经验
- 明确的交付时间表
- 行动号召（鼓励客户与您联系）

## 跟踪投标历史

在工作区中维护一个 `bids.md` 日志文件：
```
| Date | Project | Budget | Status |
|------|---------|--------|--------|
```

## 中标的小贴士

1. **快速响应** — 前 5 名投标者获得的浏览量会增加 60%
2. **具体说明** — 提及客户的具体问题
3. **简洁明了** — 固定价格项目的提案长度不超过 150 字
4. **展示成果** — 提供类似过往工作的链接
5. **提出一个问题** — 表示出您的真诚兴趣

## 工作流程示例

```
User: Find Python scraping jobs under $200 posted today
Agent: [returns 8 matching projects with details]

User: Draft bid for project #3
Agent: [generates personalized 120-word proposal]

User: Submit and log it
Agent: [updates bids.md with entry]
```