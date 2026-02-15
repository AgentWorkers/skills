---
name: code-formatter
description: 使用 `prettier` 和 `eslint` 对代码文件进行格式化。当用户需要格式化代码、修复代码检查（linting）问题或优化代码风格时，可以使用这些工具。
allowed-tools:
  - Read
  - Write
  - Bash
---

# 代码格式化工具

该工具使用行业标准的工具自动格式化代码文件。

## 功能

- 使用 Prettier 格式化 JavaScript/TypeScript 代码
- 自动修复 ESLint 规则引发的错误
- 格式化 JSON、YAML 和 Markdown 文件
- 在提交代码之前执行格式化检查

## 使用示例

**格式化单个文件：**
```
"Format the src/index.js file"
```

**格式化整个目录：**
```
"Format all files in the src/ directory"
```

**检查代码格式（无需进行任何修改）：**
```
"Check if files in src/ are properly formatted"
```

## 配置

请设置以下环境变量以实现自定义配置：
- `PRETTIER_CONFIG`：Prettier 配置文件的路径（默认值：.prettierrc）
- `ESLINT_CONFIG`：ESLint 配置文件的路径（默认值：.eslintrc.js）