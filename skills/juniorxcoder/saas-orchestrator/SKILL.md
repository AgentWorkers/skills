---
name: saas-orchestrator
description: 协调 SaaS 工厂的运营流程：创建子代理、跟踪项目进度、管理收入目标，并协调开发工作流程。适用于构建年经常性收入（MRR）超过 10 亿美元的 SaaS 企业。
---
# 🦞 SAAS Orchestration Platform - JUNAI的指挥中心

这是用于管理SAAS开发流程的核心工具。可以将其视为构建盈利性软件产品的“空中交通管制系统”。

## 核心功能

### 1. 子代理管理
创建、监控并协调负责SAAS开发的子代理：
- **市场研究代理**：寻找有盈利潜力的市场细分领域并验证产品创意
- **开发代理**：构建最小可行产品（MVP）并持续优化产品
- **营销代理**：制定产品发布策略和增长计划
- **收入代理**：跟踪月经常性收入（MRR），优化定价策略，寻找收入增长机会

### 2. 项目协调
通过系统化的项目管理确保开发流程顺利进行：
- 跟踪所有活跃的SAAS项目及其进度
- 监控开发过程中的关键节点和潜在障碍
- 协调不同领域的子代理之间的工作
- 确保每个项目都能实现至少1000美元的月经常性收入（MRR）目标

### 3. 收入跟踪与优化
所有SAAS产品都必须达到至少1000美元的月经常性收入才能正式上线：
- 监控所有活跃产品的收入增长情况
- 识别收入优化的机会
- 跟踪客户获取和留存指标
- 标记未达到收入目标的产品

## 使用模式

### 创建新的SAAS项目
```
I want to build a SAAS that [problem description]. Target market: [audience]. Revenue goal: $[amount] MRR.
```

### 检查项目状态
```
What's the status of our SAAS factory? Any projects need attention?
```

### 收入审查
```
Which SAAS products are hitting their MRR targets? Which need work?
```

## 工作流脚本

### spawn-saas-researcher.py
创建一个子代理来研究并验证SAAS产品的创意
- 输入：目标市场细分领域或问题描述
- 输出：市场分析报告、竞争对手分析、收入潜力评估

### spawn-saas-builder.py
创建一个开发子代理来构建最小可行产品（MVP）
- 输入：经过验证的SAAS创意及开发需求
- 输出：具备基本功能的最小可行产品

### spawn-saas-marketer.py
创建一个营销子代理来制定产品增长策略
- 输入：SAAS产品及目标市场
- 输出：产品发布计划、营销渠道及增长策略

### factory-status.py
快速查看所有活跃项目的状态
- 显示：活跃项目、收入情况、所需下一步行动

## 参考资料

- 请参阅 [saas-niches.md](references/saas-niches.md)，了解经过验证的盈利性SAAS市场细分领域
- 请参阅 [revenue-models.md](references/revenue-models.md)，了解有效的定价策略
- 请参阅 [mvp-patterns.md](references/mvp-patterns.md)，了解快速开发的方法

## 成功指标

- **收入目标**：每个SAAS产品的月经常性收入至少达到1000美元
- **开发速度**：在2-4周内完成最小可行产品的开发
- **市场验证**：在正式开发前明确产品的市场定位和解决方案
- **增长率**：活跃产品的月经常性收入每月增长10%以上

请记住：我们正在构建一个庞大的商业帝国，而不仅仅是做一些副业项目。每个上线的产品都必须具备真正的收入潜力。