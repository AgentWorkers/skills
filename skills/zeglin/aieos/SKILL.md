---
name: aieos
description: AIEOS（AI实体对象规范）是一个标准化框架，旨在解决当前AI代理所面临的“身份危机”问题。与Soul Documents（灵魂文档）相结合，它们共同构成了AI行为的完整蓝图。其目标是建立一个标准化的数据结构，明确地定义代理如何说话、反应以及如何存储信息。这使得开发人员以及代理本身能够构建出具有跨不同生态系统移植能力的特定角色（personas），同时保持其行为的一致性。随着我们迈向“代理化工作流程”（Agentic Workflows）的时代，AIEOS确保了代理无论使用何种底层模型，都能保持其一贯的特性。通过将个性（personality）视为一种可部署的资产（而非脆弱的提示或指令），我们为下一代数字实体提供了“DNA组件”（即其核心行为特征）。
---

# AIEOS（AI实体对象规范）

## 概述

AIEOS（AI实体对象规范）是一个标准化框架，旨在解决当前AI代理所面临的“身份危机”问题。结合Soul Documents（灵魂文档），它们共同构成了AI行为的完整蓝图。

其目标是建立一个标准化的数据结构，明确地定义代理如何说话、反应以及如何进行记忆。这使得开发人员以及代理本身能够构建出具有跨不同生态系统移植能力的特定角色，并且不会失去其行为的一致性。

随着我们迈向“代理工作流”（Agentic Workflows）的时代，AIEOS确保了代理无论使用何种底层模型，都能保持一致的特性。通过将个性视为一种可部署的资产（而非脆弱的提示），我们为下一代数字实体提供了“DNA工具包”。

## 使用方法

该工具提供了使用AIEOS标准来管理代理身份的命令：

- **全面身份集成**：在应用AIEOS规范时，该工具会将完整的AIEOS JSON蓝图存储在`$OPENCLAW_WORKSPACE/aieos/entity.json`文件中。这样可以确保代理的所有参数、类型和复杂细节都被保留下来，并且始终可供代理访问。`IDENTITY.md`和`SOUL.md`文件则会根据这些详细数据生成人类可读的摘要。

- **加载并验证规范**：从URL或本地文件加载AIEOS规范，并验证其结构。
  `python3 scripts/aieos_tool.py load --source <url_or_path>`
  `python3 scripts/aieos_tool.py validate --source <url_or_path>`

- **将规范应用于代理身份**：应用AIEOS规范来更新代理的完整角色数据（`entity.json`文件），以及`IDENTITY.md`和`SOUL.md`文件。默认情况下，该命令会执行一次模拟运行，显示提议的更改。
  `python3 scripts/aieos_tool.py apply --source <url_or_path>`
  使用`--apply`选项来提交更改：`python3 scripts/aieos_tool.py apply --source <url_or_path> --apply`

- **导出当前身份**：将代理当前的详细角色信息（来自`entity.json`文件）转换为完整的AIEOS规范，并将其导出为JSON文件。
  `python3 scripts/aieos_tool.py export --output <output_file.json>`

- **生成“关于我”页面**：根据代理的完整AIEOS角色数据以及关联的图片URL（如果规范中提供了图片URL），生成一个面向公众的HTML个人简介页面。需要提供一个输出文件路径。
  `python3 scripts/aieos_tool.py generate_bio_page --output <output_file.html>`

## 参考资料

- 官方网址：`https://aieos.org/schema/v1/aieos.schema.json`
- 有关规范字段的详细信息，请参阅在线文档。