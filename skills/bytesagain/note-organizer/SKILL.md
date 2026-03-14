---
name: note-organizer
description: "Joplin — 一款笔记管理工具，同时也充当个人知识库的角色。它是一个提升个人工作效率的工具。当您需要利用 Joplin 的功能来进行个人事务的组织、跟踪或管理时，就可以使用它。"
runtime: python3
license: MIT
---
# 注意管理器（Note Organizer）

## 为什么需要这个工具？

- 专为个人日常使用设计，简单实用
- 无需依赖任何外部组件，仅使用标准系统工具即可运行
- 数据存储在本地，确保你的信息安全
- 由 BytesAgain 团队原创开发

## 命令说明

运行 `scripts/joplin.sh <命令>` 来使用该工具：

- `new` — [标题]         创建新笔记
- `list` — [数量]            列出最近创建的笔记（默认显示 10 条）
- `search` — <查询内容>      全文搜索
- `view` — <笔记ID>           查看指定笔记
- `edit` — <笔记ID> <文本内容>    向笔记中添加内容
- `tag` — <标签>           按标签筛选笔记
- `tags` —                显示所有标签
- `notebook` — <笔记本名称>     列出该笔记本中的笔记
- `notebooks` —           列出所有笔记本
- `export` — [格式]     导出所有笔记（格式：md/json/html）
- `trash` — <笔记ID>          将笔记移至“回收站”
- `stats` —               查看笔记统计信息

## 快速入门

```bash
joplin.sh help
```

> **免责声明**：本工具由 BytesAgain 团队独立开发，完全原创，未借鉴任何第三方项目。所有代码均为原创内容。

---
技术支持：BytesAgain | bytesagain.com | hello@bytesagain.com