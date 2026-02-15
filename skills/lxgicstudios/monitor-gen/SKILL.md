---
name: monitor-gen
description: 为 Prometheus 和 Grafana 生成监控和警报配置。在设置可观测性（observability）时使用这些配置。
---

# 监控配置生成器

无需花费数小时阅读文档，即可快速获取 Prometheus 规则和 Grafana 仪表板。只需描述您想要监控的内容，即可立即获得可用于生产环境的配置。

**一个命令，零配置，立即生效。**

## 快速入门

```bash
npx ai-monitoring "node.js api with postgres and redis"
```

## 功能介绍

- 为常见的故障模式生成 Prometheus 警报规则
- 生成可直接导入到 Grafana 的仪表板 JSON 文件
- 支持 CPU、内存、磁盘以及自定义应用程序指标的监控
- 根据行业标准设置合理的阈值
- 包含运行手册链接和警报描述

## 使用示例

```bash
# Monitor a web service
npx ai-monitoring "express api with 99.9% uptime SLA"

# Database monitoring
npx ai-monitoring "postgres primary with 2 replicas"

# Full stack
npx ai-monitoring "kubernetes cluster with 10 nodes running microservices"
```

## 最佳实践

- **调整阈值**：先使用默认值，根据实际流量情况再进行调整
- **仅对可操作的问题发送警报**：避免对无关紧要的问题进行警报
- **添加上下文信息**：在警报注释中包含运行手册的链接
- **测试警报**：故意触发警报以验证其是否能够正确触发

## 适用场景

- 为新服务设置监控系统
- 为现有基础设施添加可观测性功能
- 通过示例学习 Prometheus 查询语法
- 在团队内统一警报设置

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-monitoring --help
```

## 工作原理

该工具能够理解常见的基础设施架构模式，自动生成 PromQL 查询语句和 Grafana 仪表板的定义。它会根据您的描述将需求映射到相应的指标名称，并设置合适的聚合方式和阈值。

## 许可证

采用 MIT 许可协议，永久免费。您可以随意使用该工具。