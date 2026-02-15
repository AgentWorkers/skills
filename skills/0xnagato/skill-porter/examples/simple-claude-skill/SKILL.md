---
name: code-formatter
description: 一个用于演示目的的简单示例技能
subagents:
  - name: reviewer
    description: You are a senior code reviewer.
allowed-tools:
  - Read
  - Write
---

# 代码格式化工具

该工具使用行业标准的工具自动格式化代码文件。

## 功能

- 使用 Prettier 格式化 JavaScript/TypeScript 代码
- 自动修复 ESLint 报告的问题
- 格式化 JSON、YAML 和 Markdown 文件
- 在提交代码之前运行格式化检查

## 使用示例

**格式化单个文件：**
```
"Format the src/index.js file"
```

**格式化整个目录：**
```
"Format all files in the src/ directory"
```

**检查格式化情况（无需进行任何修改）：**
```
"Check if files in src/ are properly formatted"
```

## 配置

请设置以下环境变量以实现自定义配置：
- `PRETTIER_CONFIG`：Prettier 的配置文件路径（默认值：.prettierrc）
- `ESLINT_CONFIG`：ESLint 的配置文件路径（默认值：.eslintrc.js）