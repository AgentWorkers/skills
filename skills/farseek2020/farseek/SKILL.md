# Farseek — 人工智能求职 API

通过基于人工智能的搜索技术，从超过 22,700 家企业的招聘信息平台以及 20 多个招聘管理系统（ATS）中找到与您的技能相匹配的职位。

## 功能介绍

Farseek 会实时查询来自 Greenhouse、Lever、Ashby、Workday、SmartRecruiters 等平台的职位信息。它利用 Claude 技术将您的技能转化为搜索关键词，根据相关性对搜索结果进行筛选，并对匹配结果进行分级（从 Tier 1 到 Tier 4）。

## API 端点

```
POST https://farseek.ai/api/v1/search
Content-Type: application/json
```

## 请求参数

```json
{
  "skills": ["Python", "machine learning", "distributed systems"],
  "location": "San Francisco",
  "role": "Senior Software Engineer",
  "titles": ["Software Engineer", "Backend Developer"]
}
```

| 参数名      | 类型       | 是否必填 | 说明                                      |
|------------|------------|---------|--------------------------------------|
| `skills`   | `string[]` | 是       | 需要匹配的技能（最多 50 项）                     |
| `location` | `string`   | 否       | 城市或“远程”（默认值：“远程”）                     |
| `role`     | `string`   | 否       | 当前/期望的职位名称                          |
| `titles`   | `string[]` | 否       | 用于参考的历史职位名称                        |

## 响应数据

```json
{
  "jobs": [
    {
      "title": "ML Engineer",
      "company": "Anthropic",
      "location": "San Francisco, CA",
      "url": "https://boards.greenhouse.io/anthropic/jobs/123",
      "tier": 1,
      "tier_label": "Strong match",
      "haiku_score": 9,
      "broadened": false
    }
  ],
  "meta": {
    "total_results": 25,
    "location": "San Francisco",
    "tokens_used": 15000,
    "cost_usd": 0.003
  }
}
```

## 错误代码及含义

| 错误代码 | 错误含义                                      |
|--------|---------------------------------------------|
| 400     | 技能数组缺失或无效                             |
| 429     | 每分钟请求次数达到限制（10 次）                        |
| 503     | 服务暂时不可用                                  |

错误信息将以 `{"error": {"code": "string", "message": "string"}` 的格式返回。

## 其他说明

- 支持跨源资源共享（CORS）；
- 最多返回 25 个排名靠前的搜索结果；
- Tier 1 表示最佳匹配结果，Tier 4 表示最宽泛的匹配条件；
- 支持查询的招聘平台包括 Greenhouse、Lever、Ashby、Workday、SmartRecruiters、BambooHR、Workable、JazzHR、Teamtailor 等。