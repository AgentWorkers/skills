---
name: diagram-gen
description: 从您的代码库中生成 Mermaid 图表。当您需要架构可视化时，可以使用这种方法。
---

# 图表生成器

架构图之所以总是过时，是因为没有人去维护它们。这个工具会读取你的代码，并自动生成准确的 Mermaid 图表。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-diagram ./src/
```

## 功能介绍

- 从你的代码中生成 Mermaid 图表
- 支持流程图、类图和序列图
- 从数据库模式创建 ER 图
- 输出符合 Markdown 格式的 Mermaid 代码

## 使用示例

```bash
# Generate flowchart
npx ai-diagram ./src/

# Class diagram
npx ai-diagram ./src/ --type class -o architecture.mmd

# Sequence diagram of function calls
npx ai-diagram ./src/ --type sequence

# Entity relationship diagram
npx ai-diagram ./src/ --type er
```

## 最佳实践

- **选择合适的图表类型**：面向对象编程使用类图，流程处理使用流程图
- **聚焦关键模块**：不要绘制所有内容
- **保持图表更新**：随着代码的更改定期重新生成图表
- **添加到文档中**：Mermaid 图表可以直接在 GitHub 的 Markdown 文档中显示

## 适用场景

- 新团队成员的入职培训
- 无法及时更新的文档
- 理解不熟悉的代码库
- 架构审查和规划

## 作为 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本没有付费门槛、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-diagram --help
```

## 工作原理

该工具会读取你的源代码文件，理解其结构、关系和数据流，然后生成 Mermaid 代码。这些代码可以在 Markdown 编辑器、GitHub 以及文档工具中显示为图表。

## 许可证

MIT 许可证。永久免费。你可以随意使用它。