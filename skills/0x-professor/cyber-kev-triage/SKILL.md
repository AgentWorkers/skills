---
name: cyber-kev-triage
description: 根据 KEV（Kubernetes Exploitation Vulnerability）模型的评估标准，结合资产的重要性和脆弱性的严重程度，优先处理漏洞修复工作。该模型可用于漏洞的优先级排序（CVE triage）、补丁的部署顺序决策以及漏洞修复情况的报告。
---
# 网络安全漏洞分类（Cyber KEV Triage）

## 概述

通过结合漏洞的严重程度、利用状态以及受影响资产的业务关键性，制定补丁优先级计划。

## 工作流程

1. 收集包含 CVE（Common Vulnerability Enumeration）、CVSS（Common Vulnerability Scoring System）评分、利用指标以及受影响资产的漏洞信息。
2. 将每个漏洞与资产的关键性进行关联。
3. 对漏洞进行评分，并将其划分为不同的补丁优先级等级。
4. 生成简洁的修复方案摘要和相应的修复截止时间指导。

## 使用捆绑资源

- 运行 `scripts/kev_triage.py` 命令以获得明确的漏洞分类结果。
- 阅读 `references/triage-method.md` 文件，了解评分依据和审查流程。

## 注意事项

- 确保输出内容仅用于防御目的和修复工作，不得生成用于攻击的载荷或执行步骤。