---
name: monitoring-gen
description: 生成监控和警报配置。在设置可观测性（observability）时使用此配置。
---

# 监控生成器

建立完善的监控系统意味着需要仪表板、警报机制以及各种监控指标。请描述您的监控设置，并获取 Prometheus、Grafana 或 Datadog 的配置信息。

**一个命令，零配置，即可立即使用。**

## 快速入门

```bash
npx ai-monitoring "node.js app with redis and postgres"
```

## 功能介绍

- 为您的基础设施生成监控配置
- 为常见的故障模式创建警报规则
- 设置仪表板的显示内容
- 支持 Prometheus、Grafana 和 Datadog

## 使用示例

```bash
# Node.js monitoring
npx ai-monitoring "node.js app with redis and postgres"

# Kubernetes metrics
npx ai-monitoring "kubernetes cluster with 3 nodes"

# API monitoring
npx ai-monitoring "REST API with rate limiting alerts"
```

## 最佳实践

- **基于故障症状触发警报**（而非故障原因）
- **避免警报疲劳**（仅对可操作的故障情况发送警报）
- **提供应对方案**（包含当警报触发时应执行的操作步骤）
- **重点展示关键指标**（如延迟、错误率、吞吐量）

## 适用场景

- 为新服务设置监控系统
- 为现有基础设施添加警报功能
- 学习监控最佳实践
- 快速搭建可观测性系统

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。系统需要 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-monitoring --help
```

## 工作原理

该工具会根据您的基础设施信息生成监控配置，包括需要收集的指标、警报阈值以及仪表板的布局。其背后的 AI 系统能够识别不同技术栈的常见监控需求。

## 许可证

采用 MIT 许可协议，永久免费。您可以随意使用该工具。