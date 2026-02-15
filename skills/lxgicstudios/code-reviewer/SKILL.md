# 代码审查工具

这是一个基于人工智能的代码审查工具，专门用于检查待提交的Git变更。它能在您推送代码之前检测出潜在的错误、安全问题以及代码中的不良实践。

## 快速入门

```bash
npx ai-code-review
```

## 功能介绍

- 自动审查您待提交的Git变更
- 识别代码中的错误、逻辑错误以及常见的编程缺陷
- 标记可能存在的安全风险
- 提出具体的改进建议，并附有详细的解释
- 以颜色（红色/黄色/绿色/蓝色）区分审查结果（严重/警告/建议/良好）

## 使用方法

```bash
# Stage your changes first
git add -A

# Run the review
npx ai-code-review
```

## 使用场景

- 在提交Pull Request之前
- 单独工作且没有其他代码审查人员时
- 在深夜编程、头脑疲劳时使用
- 对复杂的代码重构进行快速的质量检查

## 作为LXGIC开发工具包的一部分

该工具是LXGIC Studios提供的110多种免费开发工具之一，完全免费，无需注册或支付任何费用。

**了解更多：**
- GitHub: https://github.com/lxgic-studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 许可协议

MIT许可证。永久免费使用。