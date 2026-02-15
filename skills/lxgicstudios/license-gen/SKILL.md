---
name: license-gen
description: 为您的项目选择并生成合适的许可证。在开源许可时，请使用该许可证。
---

# 许可证生成器

选择合适的许可证并不需要法律学位。这个工具会用通俗易懂的语言解释每种许可证的详细内容，并为你生成相应的 LICENSE 文件。

**仅需一个命令，无需任何配置，即可使用。**

## 快速入门

```bash
npx ai-license
```

## 功能介绍

- 提供交互式的许可证选择界面，并附带详细说明
- 生成完整的 LICENSE 文件
- 解释每种许可证的实际含义
- 支持 MIT、Apache、GPL、BSD 等多种许可证类型

## 使用示例

```bash
# Interactive mode
npx ai-license

# Quick MIT license
npx ai-license --type mit --name "Jane Doe"

# Explain a license before choosing
npx ai-license --explain apache-2.0
```

## 最佳实践

- **选择 MIT 许可证（简单易用）**：你可以自由使用代码，只需保留版权信息即可。
- **选择 Apache 许可证（包含专利保护）**：代码会受到专利法的保护。
- **选择 GPL 许可证（遵循开源原则）**：衍生作品也必须保持开源状态。
- **检查依赖关系**：某些许可证可能存在兼容性问题。

## 适用场景

- 开始一个新的开源项目时
- 不确定哪种许可证适合你的需求时
- 需要快速了解许可证的详细规定时
- 需要快速生成 LICENSE 文件时

## 该工具属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥，只需使用相应的命令即可使用这些工具。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装任何软件，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行该工具时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-license --help
```

## 工作原理

该工具会询问你关于代码使用方式的详细要求，然后推荐合适的许可证。它利用 GPT-4o-mini 模型以通俗易懂的语言解释许可证条款，并自动生成完整的 LICENSE 文件。

## 许可证信息

该工具基于 MIT 许可证发布，永久免费。你可以随心所欲地使用该工具。