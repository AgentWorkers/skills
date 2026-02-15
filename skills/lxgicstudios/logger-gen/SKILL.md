---
name: logger-gen
description: 为任何框架设置结构化的日志记录功能。在配置日志记录时使用此功能。
---

# 日志生成器

虽然结构化日志记录非常重要，但正确配置它需要花费时间。这个工具可以为 pino、winston 或 bunyan 生成可用于生产环境的日志配置。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-logger pino
```

## 功能介绍

- 为常用库生成日志配置
- 包含请求跟踪信息和关联 ID
- 设置日志轮换和格式化规则
- 开发模式下提供美观的日志输出，生产模式下提供 JSON 格式的日志

## 使用示例

```bash
# Pino setup
npx ai-logger pino

# Winston to file
npx ai-logger winston -o lib/logger.ts

# Edge runtime compatible
npx ai-logger bunyan -e edge
```

## 最佳实践

- **使用结构化日志**：JSON 格式的日志更易于搜索
- **包含请求 ID**：便于跨服务追踪请求
- **在适当的级别记录日志**：不要在所有情况下都记录详细信息
- **隐藏敏感数据**：切勿记录密码或令牌

## 适用场景

- 在新项目中设置合适的日志记录机制
- 用正式的日志记录系统替换 console.log
- 配置日志聚合功能
- 调试生产环境中的问题

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、注册或使用 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-logger --help
```

## 工作原理

该工具会为所选库生成完整的日志配置，包括传输方式（transport）、格式化规则（formatter）以及用于请求记录的中间件（middleware），并自动处理与环境相关的配置设置。

## 许可证

采用 MIT 许可协议，永久免费。您可以自由使用该工具。