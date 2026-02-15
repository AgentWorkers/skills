---
name: husky-gen
description: 为您的项目设置定制的 Git 钩子（git hooks）。在添加文件到仓库之前，可以使用预提交钩子（pre-commit hooks）来执行特定的操作。
---

# Husky Generator

Git 钩子功能强大，但设置起来却相当麻烦。这款工具会分析你的项目，并为你的工作流程自动生成所需的 Git 钩子。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-husky
```

## 功能介绍

- 安装并配置 Husky
- 为待提交的文件生成代码检查（linting）钩子
- 为推送操作生成测试执行钩子
- 为常规提交生成提交信息（commit-message）钩子

## 使用示例

```bash
# Install git hooks
npx ai-husky

# Preview without installing
npx ai-husky --dry-run
```

## 最佳实践

- **仅对待提交的文件进行代码检查**：避免对整个代码库进行扫描
- **在推送时执行测试**：在提交 Pull Request（PR）之前发现问题
- **保持钩子的执行效率**：过慢的钩子可能会被忽略
- **设置可选的跳过选项**：在紧急情况下可以使用 `--no-verify` 参数

## 适用场景

- 为新项目设置 Git 钩子
- 为现有项目添加代码质量检查机制
- 强制执行统一的提交信息格式
- 标准化提交前的工作流程

## 属于 LXGIC 开发工具包的一部分

Husky 是 LXGIC Studios 开发的 110 多款免费开发者工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需额外安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-husky --help
```

## 工作原理

该工具会解析你的 `package.json` 文件，以确定你使用的代码检查工具（linters）、代码格式化工具（formatters）和测试工具（test runners），然后自动生成相应的 Husky 钩子，确保它们在合适的时间执行相应的命令。

## 许可证

采用 MIT 许可协议，永久免费。你可以随意使用该工具。