---
name: grc-risks
description: 按严重程度划分的风险登记册汇总
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---# GRC 风险管理

显示风险登记册的摘要。

## 操作步骤
使用 `auditclaw-grc` 技能，展示以下内容：
- 按严重程度（严重/高/中/低）分类的风险列表
- 风险热图摘要（风险发生的可能性与影响程度的分布）
- 评分最高的 5 个风险及其应对措施
- 到期未进行风险审查的风险