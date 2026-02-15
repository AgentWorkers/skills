---
name: code-explain
description: 用简单的英语解释复杂的代码。
---

# 代码解释器

只需粘贴令人困惑的代码，即可获得清晰的解释。支持任何编程语言。

## 快速入门

```bash
npx ai-explain ./src/utils/crypto.ts
```

## 功能介绍

- 逐行解释代码的功能
- 识别代码中的模式和算法
- 解释代码为何采用当前编写方式
- 提出改进建议

## 使用示例

```bash
# Explain a file
npx ai-explain ./src/auth/jwt.ts

# Explain from stdin
cat weird-regex.js | npx ai-explain

# Explain with context
npx ai-explain ./src/api.ts --context "This handles payments"

# Different detail levels
npx ai-explain ./src/algo.ts --detail high
```

## 输出内容

- 高层概述
- 逐步分解代码逻辑
- 解释关键概念
- 指出潜在问题

## 适用场景

- 理解继承来的代码
- 学习新的编程模式
- 代码审查前的准备
- 新员工的入职培训

## 系统要求

- Node.js 18.0 或更高版本
- 需要 OPENAI_API_KEY

## 许可证

MIT 许可证。永久免费使用。

---

**由 LXGIC Studios 开发**

- GitHub: [github.com/lxgicstudios/ai-explain](https://github.com/lxgicstudios/ai-explain)
- Twitter: [@lxgicstudios](https://x.com/lxgicstudios)