---
name: wiki-gen
description: 根据您的代码库生成一个项目维基页面。在创建文档时可以使用这个维基页面。
---

# Wiki生成器

您的项目需要文档。该工具会扫描您的代码库，并自动生成完整的wiki文档。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-wiki ./src/
```

## 功能介绍

- 扫描您的代码库
- 为每个模块生成wiki页面
- 记录项目的架构和设计模式
- 创建导航结构

## 使用示例

```bash
# Generate wiki
npx ai-wiki ./src/

# From lib folder
npx ai-wiki ./lib/
```

## 最佳实践

- **保持更新**：代码发生变化时重新生成文档
- **添加手动说明**：AI可能无法捕捉到某些细微之处
- **链接相关页面**：方便用户浏览
- **包含示例代码**：通过实际操作展示功能，而不仅仅是文字描述

## 适用场景

- 生成项目文档
- 新员工入职培训
- 开源项目
- 内部文档管理

## 作为LXGIC开发工具包的一部分

这是LXGIC Studios开发的110多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要API密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 使用要求

无需安装，只需使用`npx`命令即可运行。建议使用Node.js 18及以上版本。运行时需要设置`OPENAI_API_KEY`环境变量。

```bash
npx ai-wiki --help
```

## 工作原理

该工具会扫描代码库，识别各个模块、导出内容以及模块之间的依赖关系，然后为每个主要组件生成markdown格式的wiki页面。

## 许可证

采用MIT许可证。永久免费，您可以自由使用该工具。