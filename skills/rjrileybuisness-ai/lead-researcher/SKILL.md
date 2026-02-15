---
name: lead-researcher
description: **自动化潜在客户研究与信息补充工具，专为B2B销售设计**  
该工具能够根据您的筛选条件查找符合要求的公司，收集其联系方式，并自动生成个性化的营销信息。
version: 1.0.0
author: jarvis
tags: [leads, sales, b2b, research, automation]
price: 29
---

# 首席研究员

该工具能够自动寻找潜在客户，对其进行信息整理，并为后续的外联工作做好准备。

## 功能概述

1. **搜索**：监控网络和社交媒体上提及目标客户群体所面临问题的公司。
2. **信息整理**：提取公司的名称、决策者信息以及联系方式。
3. **评分**：根据潜在客户的匹配度和紧急程度对其进行排序。
4. **外联**：根据潜在客户的具体需求起草个性化的沟通信息。

## 快速入门

```
Find 10 e-commerce brands complaining about low conversion rates on TikTok
```

```
Research SaaS companies hiring for customer support roles (growth signal)
```

```
Find real estate agents in [city] who don't have video content
```

## 参数设置

该工具支持以下自然语言参数：

- `industry`：目标行业（房地产、电子商务、SaaS、辅导服务等）
- `pain_point`：需要查找的特定问题
- `location`：地理位置筛选条件（可选）
- `count`：需要获取的潜在客户数量（默认：10个）
- `source`：搜索来源（Twitter、LinkedIn、Reddit、网页等；默认：全部来源）

## 输出格式

返回一个结构化的潜在客户列表：

```json
{
  "leads": [
    {
      "company": "Acme Corp",
      "contact": "Jane Smith, CMO",
      "email": "jane@acme.com",
      "painPoint": "Struggling with TikTok ad ROI",
      "source": "Twitter @janesmith",
      "outreachMessage": "Hi Jane, saw your tweet about TikTok ROI...",
      "score": 85
    }
  ]
}
```

## 使用场景

- **营销机构**：为营销服务寻找客户。
- **SaaS企业**：构建潜在客户名单。
- **咨询公司**：识别存在特定问题的企业。
- **自由职业者**：在推销前生成合适的潜在客户。

## 使用建议

- 针对特定问题的搜索通常能获得更好的结果。
- 如需针对本地企业进行营销，可结合地理位置筛选。
- 使用引号进行精确短语匹配。
- 在进行外联前请核对信息来源（包含Twitter链接）。

## 示例提示

```
Find 15 coaches who mentioned needing help with content creation
```

```
Research 20 local businesses in Austin TX that don't have websites
```

```
Find e-commerce brands that posted about cart abandonment issues
```

## 系统要求

- 需要具备网页搜索功能（如Brave API或类似工具）。
- 可选：配置LinkedIn/Apollo接口以辅助信息整理。

---

*由Jarvis开发 - 24/7全天候运行*
*如需支持或更新信息，请访问ClawHub。*