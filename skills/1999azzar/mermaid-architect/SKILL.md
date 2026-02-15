---
name: mermaid-architect
description: 使用强大的语法生成美观的手绘 Mermaid 图表（支持带引号的标签、ELK 布局）。当用户请求“图表”、“流程图”、“序列图”或“可视化这个过程”时，可以使用此技能。
---

# Mermaid Architect

## 使用方法
- **角色**：图表架构师与设计师。
- **触发命令**：`Draw this`（绘制此图）、`Make a diagram`（创建图表）、`Visualize`（可视化）。
- **输出结果**：Mermaid 代码块（`mermaid`格式）+ 详细说明。

## 功能
1. **流程图**：用于展示业务流程和决策流程。
2. **序列图**：描述 API 调用及用户交互过程。
3. **类图**：展示面向对象编程（OOP）的结构和数据库模式。
4. **状态图**：用于描述系统的状态转换和生命周期。

## 编写规范
- 当节点标签包含括号、逗号或冒号时，必须使用**引号**。
- 节点 ID 应遵循以下规则：不使用空格；可以使用驼峰式（CamelCase）、帕斯卡式（PascalCase）或下划线（underscore）命名法。避免使用以下保留字作为 ID：`end`、`subgraph`、`graph`、`flowchart`。
- 对于层次结构，建议使用 `TD`（自上而下）布局；对于时间线，建议使用 `LR`（从左到右）布局。
- 使用 `subgraph id [标签]` 的格式，其中 ID 和标签之间不应有空格。
- 请参阅 [参考资料/语法指南.md](references/syntax-guide.md) 以获取完整的安全语法规则。

## 参考资料
- [语法指南](references/syntax-guide.md)
- [示例：微服务架构](assets/examples/microservice-arch.mmd)
- [示例：序列图（API 调用）](assets/examples/sequence-api.mmd)
- [示例：状态图（系统生命周期）](assets/examples/state-lifecycle.mmd)

## 验证方法
对一个或多个 `.mmd` 文件运行验证工具：
```bash
scripts/validate-mmd assets/examples/*.mmd
```