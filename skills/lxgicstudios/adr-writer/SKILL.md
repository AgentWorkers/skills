---
name: adr-writer
description: 使用 AI 生成架构决策记录。在记录技术决策时可以使用这种方法。
---

# ADR Writer

编写架构决策记录（Architecture Decision Records, ADR）是大家都知道应该做的事情，但实际上却很少有人真正去执行。因为通常需要编写大量的样板代码，还要花费太多时间考虑文档的格式，而本应把精力集中在决策本身上。这个工具可以解决这些问题。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-adr "switch from REST to GraphQL"
```

## 功能介绍

- 生成符合标准格式的完整 ADR 文档（包含标题、背景信息、决策内容及后果）
- 处理繁琐的文档结构，让你能够专注于决策本身
- 创建一致的文档，方便团队日后查阅
- 适用于各种架构决策，从数据库选择到框架迁移等场景

## 使用示例

```bash
# Database decision
npx ai-adr "use PostgreSQL over MongoDB for transactional data"

# Architecture pattern
npx ai-adr "adopt microservices instead of monolith"

# Framework choice
npx ai-adr "migrate from Express to Fastify"

# Infrastructure
npx ai-adr "move to Kubernetes from Docker Compose"
```

## 最佳实践

- **具体说明决策内容**：例如，“将移动客户端的数据接口从 JSON 更改为 GraphQL”比“更改 API”更具体
- **提供决策背景**：在描述中说明做出该决策的原因
- **审核输出内容**：虽然 AI 可以完成 80% 的工作，但请补充团队特有的背景信息
- **对文档进行版本管理**：将 ADR 文档与所记录的代码一起提交到版本控制系统

## 适用场景

- 在新项目中记录初始的技术选型
- 进行可能引发后续开发者质疑的重大架构变更
- 为新团队成员介绍过去的决策内容
- 满足合规性要求（如需要提供决策文档）

## 属于 LXGIC 开发工具包的一部分

LXGIC Studios 开发了 110 多款免费开发者工具，这款工具就是其中之一。免费版本无需支付费用、无需注册，也不需要 API 密钥，只需简单运行即可使用。

**更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-adr --help
```

## 工作原理

该工具会接收你对架构决策的文字描述，将其发送给优化过的 GPT-4o-mini 模型（该模型专门用于生成 ADR 文档），然后返回结构完整的文档。生成的文档遵循大多数工程团队使用的标准 ADR 模板。

## 许可证

采用 MIT 许可协议，永久免费。你可以随意使用这款工具。