---
name: interview-gen
description: 根据你的代码库生成面试问题，用于招聘开发人员。
---

# 面试生成器

通用的面试问题并不能真正反映候选人的技术能力。这款工具会分析你的代码库，生成与你的项目相关的技术问题，从而测试候选人的实际技能。

**只需一个命令，无需任何配置，即可立即使用。**

## 快速入门

```bash
npx ai-interview ./src/
```

## 功能介绍

- 分析你的代码库中使用的技术和编程模式
- 生成相关的技术问题
- 支持不同级别的技术难度（初级、中级、高级）
- 专注于你实际使用的开发技术栈

## 使用示例

```bash
# Generate mid-level questions
npx ai-interview ./src/

# Senior-level questions
npx ai-interview ./src/ --level senior --count 15

# Save to file
npx ai-interview ./src/ -o questions.md

# Junior level
npx ai-interview ./src/ --level junior
```

## 最佳实践

- **问题要与职位匹配**：不要用高级问题来测试初级候选人
- **结合理论与实践**：两者都很重要
- **设置跟进问题**：好的面试问题能够引发深入的讨论
- **定期更新问题库**：随着你的技术栈的更新，问题库也需要相应更新

## 适用场景

- 为候选人准备面试
- 标准化技术面试流程
- 为团队建立题库
- 帮助面试官了解你的代码库

## 属于 LXGIC 开发工具包的一部分

这是 LXGIC Studios 开发的 110 多个免费开发者工具之一。免费版本无需支付费用、无需注册，也不需要 API 密钥。这些工具都能直接使用。

**了解更多：**
- GitHub: https://github.com/LXGIC-Studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 使用要求

无需安装，只需使用 `npx` 命令即可运行。建议使用 Node.js 18 及更高版本。运行时需要设置 `OPENAI_API_KEY` 环境变量。

```bash
npx ai-interview --help
```

## 工作原理

该工具会扫描你的代码库，识别其中使用的技术、编程模式以及代码的复杂性，然后生成针对这些内容的面试问题，以评估候选人能否胜任你的项目。

## 许可证

采用 MIT 许可协议，永久免费。你可以自由使用该工具。