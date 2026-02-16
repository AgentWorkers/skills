---
name: grc-report
description: 生成合规性报告
user-invocable: true
metadata: {"openclaw":{"requires":{"bins":["python3"]}}}
---# GRC 报告

为特定框架生成合规性报告。

## 操作步骤：
1. 使用 `auditclaw-grc` 技能，询问用户需要为哪个框架生成报告（显示所有可用的框架列表）；
2. 生成相应的 HTML 合规性报告；
3. 报告中应包含合规性得分、控制项的状态分布、证据覆盖情况以及存在的差距（即未满足的控制项）。

### 技术细节：
- `auditclaw-grc` 是一个用于执行 GRC（Governance, Risk, and Compliance）审计的工具；
- 该工具基于 OpenClaw 和 ClawHub 构建，提供了自动化的方式来管理和生成合规性报告；
- 报告中的数据通常来自系统的审计日志和配置信息；
- 报告格式为 HTML，便于阅读和分享。