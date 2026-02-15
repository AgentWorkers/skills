---
name: eslint-config-gen
description: 生成一个与您的代码风格相匹配的 ESLint 配置文件。在设置代码检查（linting）时使用该配置文件。
---

# ESLint 配置生成器

每个团队在 ESLint 规则的使用上都有不同的意见。这款工具会读取你的实际代码，并生成一个与你现有编码风格相匹配的 ESLint 配置文件。

**只需一个命令，无需手动配置，即可立即使用。**

## 快速入门

```bash
npx ai-eslint-config
```

## 功能介绍

- 分析你的现有代码风格
- 生成符合这些风格的 ESLint 配置文件
- 支持扁平化配置文件（flat config）和传统格式的配置文件
- 再也不用为分号的使用等问题争论了

## 使用示例

```bash
# Generate eslint.config.js
npx ai-eslint-config

# Legacy .eslintrc.json format
npx ai-eslint-config --format json

# Analyze specific directory
npx ai-eslint-config --dir ./src
```

## 最佳实践

- **在具有代表性的代码上运行该工具**（而不仅仅是单个文件）
- **查看生成的规则**——这可能会帮助你发现一些不良的编码习惯
- **根据需要添加代码格式化工具（如 `prettier`）**——不要将代码格式化与代码检查混为一谈
- **将生成的配置文件提交到版本控制系统中**——这样所有团队成员都能使用相同的规则

## 适用场景

- 新项目启动时需要设置 ESLint 配置
- 继承了一个没有配置检查机制的项目
- 希望将现有的代码风格规范化
- 需要将配置文件转换为扁平化格式

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本没有付费门槛、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-eslint-config --help
```

## 工作原理

该工具会读取代码库中的示例文件，识别代码中的分号使用方式、引号格式以及缩进规则等模式，然后生成一个能够强制执行这些规则的 ESLint 配置文件。

## 许可证

MIT 许可证。永久免费。你可以自由使用该工具。