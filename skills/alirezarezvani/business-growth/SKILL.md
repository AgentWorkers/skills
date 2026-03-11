---
name: "business-growth-skills"
description: "4项具备生产环境适用性的业务与成长技能：  
- **客户成功经理**：负责客户满意度评估（健康评分）及客户流失预测；  
- **销售工程师**：擅长处理销售请求（RFP）的分析；  
- **收入运营专员**：负责管理销售流程（sales pipeline）及市场推广策略（GTM, Growth Marketing）相关的指标；  
- **合同与提案撰写专家**：负责起草正式的合同文件及销售提案。  
**使用的Python工具**：仅限于Python的标准库（stdlib）。  
**协作工具**：  
- **Claude Code**：用于代码编写与协作；  
- **Codex CLI**：提供命令行界面，便于自动化操作；  
- **OpenClaw**：用于数据处理与分析。"
version: 1.1.0
author: Alireza Rezvani
license: MIT
tags:
  - business
  - customer-success
  - sales
  - revenue-operations
  - growth
agents:
  - claude-code
  - codex-cli
  - openclaw
---
# 商业与成长技能

以下是4项适用于客户成功、销售和收入运营的、具备生产环境使用能力的技能。

## 快速入门

### Claude Code
```
/read business-growth/customer-success-manager/SKILL.md
```

### Codex CLI
```bash
npx agent-skills-cli add alirezarezvani/claude-skills/business-growth
```

## 技能概述

| 技能 | 所在文件夹 | 重点 |
|-------|--------|-------|
| 客户成功经理 | `customer-success-manager/` | 客户健康状况评估、流失预测、业务扩展 |
| 销售工程师 | `sales-engineer/` | 商业需求书（RFP）分析、竞争分析、概念验证（PoC）规划 |
| 收入运营 | `revenue-operations/` | 销售流程分析、预测准确性、销售管理（GTM）指标 |
| 合同与提案撰写 | `contract-and-proposal-writer/` | 提案撰写、合同模板设计 |

## Python工具

共有9个脚本，全部使用Python的标准库实现：

```bash
python3 customer-success-manager/scripts/health_score_calculator.py --help
python3 revenue-operations/scripts/pipeline_analyzer.py --help
```

## 规则

- 仅加载您需要的特定技能对应的SKILL.md文件。
- 使用Python工具进行评分和指标计算，避免手动估算。