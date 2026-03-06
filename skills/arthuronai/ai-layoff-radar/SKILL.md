---
name: ai-layoff-radar
description: 从全球新闻中检测由人工智能驱动的裁员事件，并生成结构化的风险报告。
version: 1.0.0
tags:
  - ai
  - layoffs
  - automation
  - news
metadata:
  openclaw:
    requires:
      env:
        - NEWS_API_KEY
    primaryEnv: NEWS_API_KEY
---
# AI 裁员监测工具

该工具用于检测因人工智能（AI）的采用、自动化流程的推行以及基于AI的效率提升计划而引发的全球性裁员事件。

## 适用场景

当用户需要查找、汇总或监控与AI采用相关的裁员信息时，可激活此工具。适用于以下场景：
- 由AI技术导致的裁员
- 由于自动化流程而产生的裁员
- 公司用AI技术替代传统劳动力所引发的裁员
- 为提升效率而实施的裁员计划

## 使用步骤

1. 扫描新闻来源。
2. 提取相关的裁员事件信息。
3. 分析这些裁员事件是否与AI技术有关。
4. 生成结构化的报告。

## 输出格式

返回以下字段的JSON数据：
- `company`（公司名称）
- `date`（裁员发生日期）
- `country`（裁员发生国家）
- `layoff_size`（裁员人数）
- `ai_causality_score`（裁员与AI技术相关的程度评分）
- `summary`（裁员事件的简要概述）

## 示例

用户查询：
`查找最近的AI相关裁员信息`

示例JSON响应：

```json
{
  "summary": {
    "total_events": 2,
    "top_companies": ["Example Corp", "Sample Systems"]
  },
  "detected_events": [
    {
      "company": "Example Corp",
      "date": "2026-03-04T14:20:00+00:00",
      "country": "USA",
      "layoff_size": 1200,
      "ai_causality_score": 88,
      "summary": "Company announced layoffs after AI automation rollout in customer operations."
    },
    {
      "company": "Sample Systems",
      "date": "2026-03-03T09:10:00+00:00",
      "country": "UK",
      "layoff_size": 350,
      "ai_causality_score": 74,
      "summary": "Job cuts tied to AI efficiency program and workflow automation."
    }
  ]
}
```