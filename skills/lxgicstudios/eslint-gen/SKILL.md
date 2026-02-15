---
name: eslint-gen
description: 根据您代码库中的模式生成 ESLint 配置文件。在设置代码检查（linting）时可以使用该配置文件。
---

# ESLint 配置生成器

不要再从其他项目中复制 ESLint 配置文件了。这个工具会扫描你的实际代码库，并生成一个与你编码风格相匹配的配置文件。

**只需一个命令，无需手动配置。**  

## 快速入门

```bash
npx ai-eslint-config .
```

## 功能概述

- 扫描你的现有代码，以检测代码中的模式和约定
- 生成与你的编码风格相匹配的 `.eslintrc` 配置文件
- 支持 TypeScript、React、Vue 和 Node.js 项目
- 自动配置解析器和插件设置
- 避免那些会标记你的现有代码为错误的规则

## 使用示例

```bash
# Analyze and generate for current project
npx ai-eslint-config .

# Generate strict config
npx ai-eslint-config . --strict

# Output to specific file
npx ai-eslint-config . -o .eslintrc.json
```

## 最佳实践

- **先在代码质量良好的状态下运行该工具**：在代码库达到标准状态后再生成配置文件
- **审查规则**：虽然 AI 会推荐合理的默认设置，但你需要了解团队的编码习惯
- **扩展而非覆盖**：使用 `extends` 语句来继承现有配置，仅自定义需要的部分
- **逐步添加规则**：开始时设置较宽松的规则，随着时间逐步严格化

## 适用场景

- 新项目启动时需要快速进行代码检查
- 在团队中统一代码风格
- 从 TSLint 或其他过时的代码检查工具迁移
- 通过实际示例学习 ESLint 规则

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无需支付费用、无需注册，也无需 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-eslint-config --help
```

## 工作原理

该工具使用通配符模式来查找源文件，分析代码中的样式规范（如分号、引号和空格的使用），然后生成一个将这些规范转化为可执行规则的 ESLint 配置文件。

## 许可证

MIT 许可证。永久免费使用，你可以随意使用该工具。