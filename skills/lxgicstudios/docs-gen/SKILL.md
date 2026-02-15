---
name: jsdoc-gen
description: 在你的代码中添加 JSDoc 或 TSDoc 注释。当文档缺失时，请使用这些注释来提供必要的说明。
---

# JSDoc 生成器

您导出的函数目前没有文档。此工具会在不修改实际代码逻辑的情况下，为所有导出的函数添加 JSDoc 或 TSDoc 注释。

**只需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-docs src/ --style jsdoc
```

## 功能介绍

- 为导出的函数和类添加 JSDoc/TSDoc 注释
- 描述参数、返回值和异常情况
- 保留所有现有的代码和注释
- 可用于文件、目录或通配符模式

## 使用示例

```bash
# Preview docs for a directory
npx ai-docs src/ --style jsdoc

# TSDoc style
npx ai-docs src/ --style tsdoc

# Write changes to files
npx ai-docs src/ --style jsdoc --write

# Single file
npx ai-docs src/utils.ts --style jsdoc

# Glob patterns
npx ai-docs "src/**/*.ts" --style tsdoc
```

## 最佳实践

- **先预览**：在未使用 `--write` 选项的情况下运行工具，查看更改内容
- **重点关注导出的内容**：内部辅助函数不需要文档
- **添加示例**：尤其是对于复杂的函数
- **审核生成的文档**：人工智能可能无法完全理解某些细微差别

## 适用场景

- 代码库完全没有文档
- 新员工需要阅读每个函数的详细信息
- 如果没有文档，集成开发环境（IDE）提供的提示会非常有限
- 为开源项目发布做准备

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、注册或使用 API 密钥，只需使用即可。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，直接使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-docs --help
```

## 工作原理

该工具会读取您的文件，识别出导出的函数、类和类型，然后生成相应的文档注释。人工智能能够理解函数签名，并推断出每个参数的用途。

## 许可证

MIT 许可证。永久免费使用，您可以随意使用该工具。