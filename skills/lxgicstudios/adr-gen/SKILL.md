---
name: adr-gen
description: 使用 AI 生成架构决策记录。在记录技术决策时可以使用这种方法。
---

# ADR 生成器（ADR Generator）

“我们为什么选择使用 Redis 而不是 Memcached？”六个月后，没人能记得这个原因了。这个工具可以根据你的决策背景生成架构决策记录（Architecture Decision Records，简称 ADR）。它记录了决策内容、考虑过的替代方案以及决策的理由。未来的你会感谢现在的自己。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-adr "We chose PostgreSQL over MongoDB for our user data"
```

## 功能介绍

- 生成格式规范的 ADR 文档
- 记录决策的背景及需要解决的问题
- 列出所有被考虑过的替代方案
- 解释决策的理由及其影响
- 记录决策所带来的后果和权衡因素

## 使用示例

```bash
# Generate an ADR from a decision
npx ai-adr "Switching from REST to GraphQL for our public API"

# Include context about your constraints
npx ai-adr "Using Kafka for event streaming" --context "High throughput, multi-consumer"

# Output to your docs folder
npx ai-adr "Adopting TypeScript" --output docs/adr/001-typescript.md
```

## 最佳实践

- **在做出决策时立即编写 ADR**——而不是六个月后才想起来原因
- **务必包含所有替代方案**——你还考虑过哪些方案？为什么没有选择它们？
- **如实记录权衡因素**——每个决策都有缺点，必须将其记录下来
- **为 ADR 文件编号**——例如：001-database-choice.md、002-auth-provider.md 等

## 适用场景

- 在做出重大技术决策时
- 新团队成员入职时需要了解决策背景时
- 为架构评审做准备时
- 建立技术选型的知识库时

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-adr --help
```

## 工作原理

该工具会获取你的决策内容，研究该技术选择常见的替代方案及权衡因素，然后按照标准格式（标题、状态、背景、决策内容、后果）生成结构化的 ADR 文档。

## 许可证

采用 MIT 许可协议，永久免费。你可以随意使用该工具。