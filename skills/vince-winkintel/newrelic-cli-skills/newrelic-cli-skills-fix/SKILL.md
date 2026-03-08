---
name: newrelic-cli-skills
version: 1.0.2
description: 通过 newrelic CLI 监控、查询和管理 New Relic 的可观测性数据。涵盖 NRQL 查询、APM 性能排查、部署标记、警报管理、基础设施监控以及代理诊断等功能。当用户询问应用程序性能、错误率、交易延迟、部署进度或 New Relic 配置等相关问题时，可以使用该工具。
metadata:
  openclaw:
    purpose: >
      Read-mostly observability skill. Reads APM metrics, NRQL query results, alert
      policies/conditions, and infrastructure host data from the New Relic API.
      Write operations are limited to: creating deployment markers (apm sub-skill)
      and muting/unmuting alert conditions (alerts sub-skill). No data is deleted.
      Scripts execute newrelic CLI commands only; no shell eval or dynamic execution.
    requires:
      env:
        - NEW_RELIC_API_KEY
        - NEW_RELIC_ACCOUNT_ID
      binaries:
        - newrelic
      notes: |
        NEW_RELIC_API_KEY must be a User Key (starts with NRAK-).
        NEW_RELIC_ACCOUNT_ID is the numeric account ID from the NR UI.
        See README.md for CLI installation instructions.
        Use an API key scoped to the minimum required accounts.
tags:
  - newrelic
  - observability
  - apm
  - monitoring
  - performance
  - nrql
---
# New Relic 命令行界面 (CLI) 技能指南

## 快速决策树

- 报告了性能问题？ → [`apm/SKILL.md`](apm/SKILL.md)
- 需要用 NRQL 查询数据？ → [`nrql/SKILL.md`](nrql/SKILL.md)
- 需要记录部署信息？ → [`deployments/SKILL.md`](deployments/SKILL.md)
- 需要管理警报？ → [`alerts/SKILL.md`](alerts/SKILL.md)
- 存在基础设施或主机问题？ → [`infrastructure/SKILL.md`](infrastructure/SKILL.md)
- 代理未报告数据？ → [`diagnostics/SKILL.md`](diagnostics/SKILL.md)

---

## 设置与身份验证

```bash
# Install
curl -Ls https://download.newrelic.com/install/newrelic-cli/scripts/install.sh -o install.sh
bash install.sh && rm install.sh

# Configure profile
newrelic profile add \
  --profile default \
  --apiKey $NEW_RELIC_API_KEY \
  --accountId $NEW_RELIC_ACCOUNT_ID \
  --region US   # or EU

newrelic profile default --profile default

# Verify
newrelic profile list
```

---

## 常用命令

```bash
# Search for an entity by name
newrelic entity search --name "my-app"

# Run a NRQL query
newrelic nrql query --accountId $NEW_RELIC_ACCOUNT_ID \
  --query "SELECT average(duration) FROM Transaction WHERE appName='my-app' SINCE 1 hour ago"

# Record a deployment
newrelic apm deployment create \
  --applicationId <APP_ID> \
  --revision "v1.2.3" \
  --description "Feature: user auth"

# Run diagnostics
newrelic diagnose run
```

---

## 实体引用

查找实体 GUID（用于 API 调用和部署标记）：

```bash
# List all APM apps
newrelic entity search --name "" --type APPLICATION --domain APM

# Get specific entity details
newrelic entity get --guid <GUID>

# List all hosts
newrelic entity search --name "" --type HOST
```

---

## 环境变量

| 变量 | 描述 |
|---|---|
| `NEW_RELIC_API_KEY` | 用户密钥（格式为 NRAK-...） |
| `NEW_RELIC_ACCOUNT_ID` | 数字账户 ID |
| `NEWRELIC_REGION` | `US` 或 `EU` |

---

## 子技能

| 子技能 | 使用场景 |
|---|---|
| [`apm/`](apm/SKILL.md) | 性能问题排查、慢速交易分析、错误诊断 |
| [`nrql/`](nrql/SKILL.md) | 自定义查询、仪表盘构建、数据探索 |
| [`deployments/`](deployments/SKILL.md) | 标记部署事件、关联部署与性能数据 |
| [`alerts/`](alerts/SKILL.md) | 警报策略设置、条件配置、通知渠道管理 |
| [`infrastructure/`](infrastructure/SKILL.md) | 主机指标监控（CPU/内存/进程状态） |
| [`diagnostics/`](diagnostics/SKILL.md) | 代理状态检查、配置验证、连接性测试 |

## 脚本

| 脚本 | 用途 |
|---|---|
| `scripts/check-performance.sh` | 对所有应用程序进行快速健康检查 |
| `scripts/deployment-marker.sh` | 记录部署事件 |
| `scripts/top-slow-transactions.sh` | 查找运行最慢的 10 个交易 |
| `scripts/error-report.sh` | 显示带有堆栈跟踪的最新错误信息 |

## 参考资料

- [`references/nrql-patterns.md`](references/nrql-patterns.md) — 常见的 NRQL 查询模式 |
- [`references/performance-triage.md`](references/performance-triage.md) — 逐步性能问题排查指南 |