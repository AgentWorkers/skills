---
name: refactor-assist
description: 获取带有颜色差异显示的重构建议。在提升代码质量时可以使用此功能。
---

# 代码重构助手（Code Refactor Assistant）

在其他人进行代码审查之前，先自己先进行一次代码审查。只需将此工具指向目标文件，它就会提供具体的重构建议及相应的代码差异（diffs）。

**仅需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-refactor src/utils.ts
```

## 功能简介

- 分析代码中的优化点
- 以彩色差异的形式显示建议的修改内容
- 重点关注代码的可读性和编程模式
- 可自动应用修改建议

## 使用示例

```bash
# See suggestions
npx ai-refactor src/utils.ts

# Apply changes directly
npx ai-refactor src/utils.ts --apply

# Focus on specific area
npx ai-refactor src/api.ts --focus "error handling"
```

## 最佳实践

- **应用修改前先进行审查**：确保建议合理可行
- **先提交代码**：确保代码处于一个干净的状态，便于后续对比差异
- **一次专注于一项重构任务**：不要一次性重构所有内容
- **修改后运行测试**：确保代码功能正常

## 适用场景

- 代码审查前的准备工作
- 清理旧代码
- 学习更好的编程模式
- 技术债务清理（Technical Debt Management）

## 本工具属于 LXGIC 开发工具包（LXGIC Dev Toolkit）的一部分

这是 LXGIC Studios 开发的 110 多款免费开发者工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多信息：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgic.dev

## 系统要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行此工具需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-refactor --help
```

## 工作原理

该工具会读取你的代码文件，将其发送给 GPT-4o-mini 进行分析，并以代码差异的形式展示重构建议。分析内容涵盖代码的可读性、重复代码、现代编程模式、性能以及类型安全性等方面。

## 许可证

采用 MIT 许可协议，永久免费。你可以随心所欲地使用该工具。