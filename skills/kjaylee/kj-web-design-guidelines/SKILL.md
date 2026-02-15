---
name: web-design-guidelines
description: 检查用户界面代码是否符合Web界面设计指南。当收到“审核我的用户界面”、“检查可访问性”、“审计设计”、“评估用户体验”或“根据最佳实践检查我的网站”等请求时，请使用此功能。
metadata:
  author: vercel
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# 网页界面指南

检查文件是否符合网页界面指南的要求。

## 工作原理

1. 从下面的源URL获取最新的指南。
2. 读取指定的文件（或提示用户提供文件或文件模式）。
3. 根据获取的指南中的所有规则进行检查。
4. 以简洁的 `file:line` 格式输出检查结果。

## 指南来源

在每次检查之前，请获取最新的指南：

```
https://raw.githubusercontent.com/vercel-labs/web-interface-guidelines/main/command.md
```

使用 `WebFetch` 命令来检索最新的规则。检索到的内容包含所有的规则以及输出格式的说明。

## 使用方法

当用户提供文件或文件模式作为参数时：
1. 从上面的源URL获取指南。
2. 读取指定的文件。
3. 应用指南中的所有规则。
4. 使用指南中指定的格式输出检查结果。

如果未指定任何文件，请询问用户需要检查哪些文件。