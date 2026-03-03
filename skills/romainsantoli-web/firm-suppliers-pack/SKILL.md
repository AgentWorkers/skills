---
name: firm-suppliers-pack
version: 1.0.0
description: 采购与供应商管理套件：包括供应商寻源、多标准评估、总拥有成本（TCO）分析、合同管理以及供应链风险监控功能。包含5款采购工具。
author: romainsantoli-web
license: MIT
metadata:
  openclaw:
    registry: ClawHub
    requires:
      - mcp-openclaw-extensions >= 3.2.0
tags:
  - procurement
  - suppliers
  - sourcing
  - supply-chain
  - vendor-management
---
# firm-suppliers-pack

> ⚠️ 本内容由人工智能生成，使用前需经过人工审核。

## 目的

为该公司提供一套完整的采购和供应商管理工具包。  
支持结构化的供应商寻源（包括SaaS产品、服务及工业产品），采用多标准评估机制（含评分矩阵），进行总拥有成本（TCO）分析，提供合同条款建议，并实现持续的供应链风险监控。

该工具包旨在生成所有部门都能理解的专业文档：  
- 首席执行官（CEO）：用于制定战略采购决策  
- 财务总监（CFO）：用于评估采购预算和总拥有成本  
- 技术总监（CTO）：用于选择技术供应商  
- 法律部门：用于审查合同条款  
- 运营部门：用于获取供应链风险预警  

## 工具（共5个）

| 工具 | 描述 | 类别 |
|------|-------------|----------|
| `openclawupplier_search` | 全范围供应商搜索——识别、筛选、入围 | 采购 |
| `openclawupplier_evaluate` | 基于15项以上加权标准的供应商多标准评估 | 采购 |
| `openclawupplier_tco_analyze` | 对3-5年内的总拥有成本（包括隐性成本）进行分析 | 财务 |
| `openclawupplier_contract_check` | 合同条款审核——服务水平协议（SLA）、罚款条款、合同可撤销性、合规性 | 法律 |
| `openclawupplier_risk_monitor` | 持续监控供应商风险——包括财务风险、依赖关系及地缘政治风险 | 采购 |

## 使用方法

```yaml
skills:
  - firm-suppliers-pack

# Search for SaaS project management tools:
openclaw_supplier_search category="SaaS project management" budget_max=1000 users=50

# Evaluate shortlisted suppliers:
openclaw_supplier_evaluate suppliers='["Monday.com","ClickUp","Notion"]' criteria='{"price":20,"features":25,"support":15}'

# TCO analysis:
openclaw_supplier_tco_analyze suppliers='["Monday.com","ClickUp"]' volume=50 horizon_years=3

# Contract clause check:
openclaw_supplier_contract_check supplier="ClickUp" contract_type="SaaS" requirements='["SLA 99.9%","RGPD DPA","reversibility"]'

# Risk monitoring:
openclaw_supplier_risk_monitor action="add" supplier="ClickUp" watch='["financial","service_level","security"]'
```

## 跨部门集成

| 部门 | 获得的资源 | 使用的工具 |
|------------|--------------|------|
| **CEO** | 战略采购建议 | `supplier_evaluate` |
| **CFO** | 总拥有成本分析、预算预测 | `supplier_tco_analyze` |
| **CTO** | 技术供应商评估与对比 | `supplier_search` + `supplier_evaluate` |
| **法律部门** | 合同条款建议 | `supplier_contract_check` |
| **运营部门** | 供应链风险警报 | `supplier_risk_monitor` |

## 系统要求  

- 确保系统版本为 `mcp-openclaw-extensions >= 3.2.0`