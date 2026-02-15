---
name: naming-gen
description: 在改进代码可读性的过程中，建议为变量和函数起更合适的名称。
---

# 命名辅助工具（Naming Gen）

你有一个名为 `data2` 的变量和一个名为 `processStuff` 的函数。这个工具会分析你的代码，并为你提供更合适的变量名和函数名建议。这些名称应该清晰、具有描述性，能够准确反映变量的用途和函数的功能。由于命名是一项复杂的工作，我们希望你能避免因此而感到困扰。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-naming ./src/utils.ts
```

## 工具功能

- 分析代码中的变量名和函数名
- 提出更清晰、更具描述性的替代名称
- 识别像 `temp`、`data`、`result` 这样含义模糊的变量名
- 遵循你的项目命名规范
- 为每个建议提供详细的理由，解释为什么这个名称更合适

## 使用示例

```bash
# Analyze a single file
npx ai-naming ./src/processor.ts

# Analyze all files in a directory
npx ai-naming ./src/

# Only flag the worst offenders
npx ai-naming ./src --threshold 3

# Output suggestions as a checklist
npx ai-naming ./src --format checklist
```

## 最佳实践

- **先修改那些含义模糊的名称**：`data`、`temp`、`result` 是最需要改进的名称
- **考虑变量的使用范围**：对于作用范围较小的变量，可以使用简短的名称；对于作用范围较大的变量，应使用较长的名称
- **保持一致性**：如果在某个地方将某个变量称为 `user`，那么在其他地方也请使用相同的名称
- **避免过度缩写**：使用缩写（如 `usr`）不仅不能节省字符，反而容易引起混淆

## 适用场景

- 在提交代码请求（PR）之前审查代码
- 重构那些变量名难以理解的旧代码
- 学习编写更易读的代码
- 当你发现自己的命名习惯不佳时，用于代码审查前的准备工作

## 该工具属于 LXGIC 开发工具包（LXGIC Dev Toolkit）

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册账号，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。

```bash
npx ai-naming --help
```

## 工作原理

该工具会解析你的源代码，识别所有的变量名和函数名，通过分析它们的使用方式来确定它们的实际功能，然后提出更符合其用途的名称建议。

## 许可证

采用 MIT 许可协议。永久免费，你可以随意使用该工具。