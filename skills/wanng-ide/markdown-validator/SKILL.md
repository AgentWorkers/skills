---
name: markdown-validator
description: 用于检查 Markdown 文件中是否存在失效的本地链接（即无法访问的链接）。
---
# Markdown 验证工具

该工具用于检测 Markdown 文件中存在的无效本地链接（即无法访问的链接）。您可以使用此工具来检查内部文档的一致性。

## 使用方法

```bash
# Validate current directory
openclaw exec node skills/markdown-validator/index.js .

# Validate specific file
openclaw exec node skills/markdown-validator/index.js README.md
```

## 主要功能

- 递归扫描整个文档
- 检查相对链接（相对于当前文件的链接）
- 忽略外部 URL（http/https）
- 忽略同一文件内的锚点链接（#anchor）
- 生成包含失效链接及其行号的 JSON 报告

## 示例输出

```json
[
  {
    "file": "/path/to/README.md",
    "valid": false,
    "brokenLinks": [
      {
        "text": "Link Text",
        "url": "./broken-link.md",
        "line": 10
      }
    ]
  }
]
```