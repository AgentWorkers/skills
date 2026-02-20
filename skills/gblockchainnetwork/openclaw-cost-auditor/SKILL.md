---
summary: "OpenClaw Cost Auditor: Track API usage, model costs, token burn, and revenue for OpenClaw deployments."
description: "Parse logs, query API metrics, forecast bills, optimize spend with reports & alerts."
triggers:
  - "audit openclaw costs"
  - "openclaw billing"
  - "check API spend"
  - "token usage report"
read_when:
  - "openclaw cost" in message
  - "API auditor" in message
---

# OpenClaw 成本审计器 v1.0.0

## 🎯 功能
- 日/周成本报告
- 按代币数量排序的顶级模型/用户
- 每次查询的成本预测
- 优化建议（量化处理、数据精简）

## 🚀 快速入门
```
!openclaw-cost-auditor --period last7d --format pdf
```

## 文件结构
- `scripts/audit.py`：日志解析器与计算工具
- `templates/report.md`：成本报表模板

## 集成方式
支持与 OpenClaw 日志系统、Grok/xAI API 以及自定义数据提供者的集成。