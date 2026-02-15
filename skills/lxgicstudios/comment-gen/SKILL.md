---
name: comment-gen
description: 为复杂的代码添加有意义的内联注释。当文档不足时，请使用这种方法。
---

# 评论生成器

好的注释应该解释“为什么”（the reason），而不是“做什么”（what）。这个工具会读取你的代码，理解其背后的意图，并添加真正有助于未来读者的注释。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-comment ./src/algorithm.ts
```

## 功能介绍

- 为复杂代码添加内联注释，解释其背后的逻辑
- 重点说明代码“为什么”执行某个操作，而非“具体做什么”
- 支持多种注释详细程度，以满足不同读者的需求
- 保留你原有的代码格式

## 使用示例

```bash
# Add concise comments
npx ai-comment ./src/algorithm.ts

# More detailed explanations
npx ai-comment ./src/utils.js --style detailed

# For junior developer onboarding
npx ai-comment ./src/parser.ts --style beginner

# Preview without changing files
npx ai-comment ./src/complex.ts --dry-run
```

## 最佳实践

- **不要过度注释**——简单的代码不需要注释
- **重点关注复杂逻辑**——业务规则、边缘情况、解决方法
- **审核生成的注释**——确保注释的准确性
- **代码更新时及时更新注释**——过时的注释比没有注释更糟糕

## 适用场景

- 继承了没有文档的代码库
- 新团队成员的入职培训
- 需要解释的复杂算法
- 在休假前，以便他人能够维护你的代码

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥。这些工具都能正常使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-comment --help
```

## 工作原理

该工具会读取你的代码文件，将其发送给 GPT-4o-mini，然后接收带有完整内联注释的代码。AI 会分析代码的控制流程、业务逻辑及边缘情况，从而生成解释性注释。

## 许可证

采用 MIT 许可协议，永久免费。你可以随意使用该工具。