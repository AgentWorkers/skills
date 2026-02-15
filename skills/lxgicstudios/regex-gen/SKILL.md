# 正则表达式生成器（Regex Gen）

根据简单的英文描述生成正则表达式模式。毕竟，没人真的能记住正则表达式的语法吧。

## 快速入门

```bash
npx ai-regex "match email addresses"
```

## 功能介绍

- 将简单的英文描述转换为可使用的正则表达式
- 解释正则表达式各部分的功能
- 提供测试用例以验证生成的表达式是否正确
- 支持常见的正则表达式模式
- 适用于任何编程语言

## 使用方法

```bash
# Generate regex from description
npx ai-regex "match phone numbers with optional country code"

# Get regex for URLs
npx ai-regex "validate URLs including localhost"

# Match dates
npx ai-regex "match dates in YYYY-MM-DD format"
```

## 示例输出

```
Pattern: ^[\w.-]+@[\w.-]+\.\w{2,}$
Explanation:
  ^ - Start of string
  [\w.-]+ - One or more word chars, dots, or hyphens
  @ - Literal @ symbol
  ...
Test cases: ✓ test@example.com ✓ user.name@domain.co.uk
```

## LXGIC 开发工具包的一部分

LXGIC Studios 提供的 110 多款免费开发工具之一。无需付费，也无需注册。

**了解更多：**
- GitHub: https://github.com/lxgic-studios
- Twitter: https://x.com/lxgicstudios
- Substack: https://lxgicstudios.substack.com
- 官网: https://lxgicstudios.com

## 许可证

MIT 许可证。永久免费使用。