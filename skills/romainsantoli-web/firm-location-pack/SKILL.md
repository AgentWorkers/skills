---
name: firm-location-pack
version: 1.0.0
description: **选址策略与场地选择工具包**：包含地理经济分析、房地产情报、场地评估、税收优惠优化以及总拥有成本（TCO）模拟等功能。提供5种专业的选址工具。
author: romainsantoli-web
license: MIT
metadata:
  openclaw:
    registry: ClawHub
    requires:
      - mcp-openclaw-extensions >= 3.2.0
tags:
  - location
  - real-estate
  - site-selection
  - geo-economics
  - implantation
---
# firm-location-pack

> ⚠️ 本内容由人工智能生成，使用前需经过人工审核。

## 目的

为公司提供完整的选址策略和工具包。支持结构化的地理经济分析、房地产市场情报、多标准选址评估、税收优惠识别，以及3-5年内的总运营成本模拟。

该工具包旨在生成所有部门都能理解的专业文档：
- CEO（用于制定战略选址决策）
- CFO（用于预测总运营成本）
- HR（用于分析人才库）
- 法律部门（用于了解地域税收影响）
- 运营部门（用于评估物流和基础设施）

## 工具（共5个）

| 工具 | 描述 | 类别 |
|------|-------------|----------|
| `openclaw_location_geo_analysis` | 地理经济分析：人才库、交通状况、生态系统、生活质量 | 战略分析 |
| `openclaw_location_real_estate` | 房地产市场情报：区域内的房源供应、价格走势 | 房地产市场 |
| `openclaw_location_site_score` | 基于20多项标准的多标准选址评估工具（含加权比较矩阵） | 战略分析 |
| `openclaw_location_incentives` | 各地区的税收优惠和援助计划（如ZFU、ZRR、BPI、FEDER） | 财务分析 |
| `openclaw_location_tco_simulate` | 3-5年内的总运营成本模拟 | 财务分析 |

## 使用方法

```yaml
skills:
  - firm-location-pack

# Geo-economic analysis of candidate cities:
openclaw_location_geo_analysis cities='["Paris 13e","Lyon Part-Dieu","Nantes"]' sector="tech" headcount=30

# Real estate search:
openclaw_location_real_estate zone="Île-de-France" property_type="bureau" surface_min=200 budget_max=6000

# Multi-criteria scoring:
openclaw_location_site_score sites='["Saint-Denis","Montreuil","Ivry"]' weights='{"transport":15,"talent":15,"price":20}'

# Tax incentives lookup:
openclaw_location_incentives zone="Saint-Denis Pleyel" company_type="startup" headcount=15

# TCO simulation:
openclaw_location_tco_simulate sites='["Paris 13e","Saint-Denis","Nantes"]' surface=250 horizon_years=3
```

## 跨部门集成

| 部门 | 获得的成果 | 使用的工具 |
|------------|--------------|------|
| **CEO** | 选址评分矩阵及战略建议 | `site_score` |
| **CFO** | 总运营成本模拟及税收优惠影响 | `tco_simulate` + `incentives` |
| **HR** | 人才库分析及生活质量数据 | `geo_analysis` |
| **法律部门** | 地域税收影响信息 | `incentives` |
| **运营部门** | 交通和基础设施评估结果 | `geo_analysis` |

## 系统要求

- 确保系统版本为 `mcp-openclaw-extensions >= 3.2.0`