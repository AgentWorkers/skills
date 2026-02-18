---
name: markdown-linter
description: 用于检查工作区中的 Markdown 文件是否存在失效的本地链接、缺失的文件引用以及基本语法错误。该工具有助于维护文档的完整性，避免 MEMORY.md 或 SKILL.md 文件中出现引用错误的问题。
---
# Markdown Linter

这是一个轻量级的工具，用于验证工作区中的 Markdown 文件。它主要关注确保文件内容的一致性，特别是检查是否存在失效的链接和缺失的引用。

## 功能

- **链接验证**：检查 `[link](path)` 引用，确保目标文件在本地存在。
- **标题检查**：验证标题是否遵循逻辑层次结构（例如，H1 -> H2）。
- **代码块检查**：确保代码块在适当的位置包含语言标识符。

## 使用方法

```javascript
const linter = require('./index');
const results = await linter.scan('.'); // Scans current directory recursively
console.log(JSON.stringify(results, null, 2));
```

## 输出格式

```json
{
  "totalFiles": 15,
  "brokenLinks": [
    {
      "file": "docs/README.md",
      "line": 10,
      "link": "./missing-image.png",
      "error": "File not found"
    }
  ],
  "syntaxErrors": []
}
```