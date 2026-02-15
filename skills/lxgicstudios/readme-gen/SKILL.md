---
name: readme-gen
description: 生成精美的 README.md 文件，其中包含徽章、安装说明和 API 文档。在新项目启动时可以使用这些文件。
---

# README 生成器

你的项目可能没有 README 文件，或者更糟糕的是，README 文件里只写着 “TODO: 编写 README”。这个工具可以根据你的代码库自动生成完整的 README 文件，包括徽章、安装步骤、API 文档和使用示例——让人们真正想要使用你的项目。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-readme
```

## 功能介绍

- 根据你的项目结构生成完整的 README 文件
- 添加相应的徽章（如 npm、许可证、构建状态）
- 为你的包管理器生成安装说明
- 根据你的代码中的导出内容生成 API 文档
- 包含来自代码或测试的使用示例

## 使用示例

```bash
# Generate README for current project
npx ai-readme

# Specify output file
npx ai-readme --output README.md

# Include specific sections
npx ai-readme --sections intro,install,api,examples

# Generate for a CLI tool
npx ai-readme --type cli
```

## 最佳实践

- **在项目启动时运行该工具**：这样比之后从头开始编写 README 更容易维护
- **自定义介绍内容**：虽然 AI 可以生成不错的介绍，但你的文字描述会更准确
- **添加真实的示例**：生成的示例通常是通用的，展示你的实际使用场景
- **保持徽章数量适中**：没人需要 15 个徽章，只需选择 3-5 个重要的徽章即可

## 适用场景

- 开始一个新的开源项目
- 将项目发布到 npm
- 你的 README 文件内容过于简陋
- 项目结构发生变更，需要更新文档

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-readme --help
```

## 工作原理

该工具会读取你的 `package.json` 文件，分析源代码中的导出内容及 CLI 命令，检查现有的文档或示例，然后生成一个结构完整的 README 文件，包含一个优秀项目所需的所有部分。

## 许可证

MIT 许可证。永久免费使用，你可以随意使用它。