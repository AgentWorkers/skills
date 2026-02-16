---
name: grc-score
description: 快速合规性评分检查及趋势分析
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---# GRC 评分

显示所有活跃框架的当前合规性评分。

## 操作步骤
使用 `auditclaw-grc` 技能，计算并显示所有活跃框架的合规性评分。包括以下内容：
- 总加权评分
- 各框架的详细评分情况（包括健康状态分布）
- 评分趋势（与上次计算结果相比）
- 任何评分变化的警报