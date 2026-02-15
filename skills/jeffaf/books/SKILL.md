---
name: books
version: 1.0.0
description: "这是一个用于AI代理的命令行工具（CLI），帮助它们为人类用户搜索和查找书籍。该工具使用了Open Library API，且无需进行身份验证（无需登录）。"
homepage: https://openlibrary.org
metadata:
  openclaw:
    emoji: "📚"
    requires:
      bins: ["bash", "curl", "jq"]
    tags: ["books", "reading", "open-library", "literature", "cli"]
---

# 书籍查询功能

这是一个用于AI代理的命令行工具（CLI），帮助用户为其人类用户搜索和查找书籍。例如：“那个关于魔法大学的奇幻系列小说叫什么名字？”——现在你的AI代理可以为你解答这个问题。

该工具使用了Open Library API，无需注册账户或API密钥。

## 使用方法

```
"Search for books called The Name of the Wind"
"Find books by Patrick Rothfuss"
"Tell me about work ID OL27448W"
"Who is author OL23919A?"
```

## 命令列表

| 功能 | 命令                |
|--------|-------------------|
| 搜索书籍 | `books search "查询内容"`     |
| 查看书籍详情 | `books info <书籍ID>`     |
| 查看作者信息 | `books author <作者ID>`     |

### 使用示例

```bash
books search "the name of the wind"     # Find books by title
books search "author:brandon sanderson" # Search by author
books info OL27448W                     # Get full details by work ID
books author OL23919A                   # Get author bio and works
```

## 输出结果

**搜索结果：**
```
[OL27448W] The Name of the Wind — Patrick Rothfuss, 2007, ⭐ 4.5
```

**书籍详情：**
```
📚 The Name of the Wind
   Work ID: OL27448W
   First Published: March 27, 2007
   Subjects: Fantasy, Magic, Coming of Age

📖 Description:
[Full description text]

🖼️ Cover: https://covers.openlibrary.org/b/id/12345-L.jpg
```

**作者信息：**
```
👤 Patrick Rothfuss
   Born: June 6, 1973
   Author ID: OL23919A

📖 Bio:
[Author biography]

=== Works ===
[OL27448W] The Name of the Wind, 2007
[OL16313124W] The Wise Man's Fear, 2011
```

## 注意事项

- 该工具基于Open Library API（网址：openlibrary.org）运行。
- 无需进行身份验证。
- 书籍的ID格式为：OL27448W
- 作者的ID格式为：OL23919A
- 搜索支持使用前缀 `author:`、`title:` 和 `subject:` 来指定搜索条件。
- 书籍封面图片提供S、M、L三种尺寸可供选择。

---

## 代理实现说明

**脚本位置：** `{skill_folder}/books`（实际脚本位于 `scripts/books` 文件夹中）

**当用户询问书籍相关信息时：**
1. 运行 `./books search "书名或作者名"` 来获取书籍的ID。
2. 运行 `./books info <书籍ID>` 来查看书籍的详细信息。
3. 运行 `./books author <作者ID>` 来查看作者的信息及参考文献。

**搜索提示：**
- 使用 `author:作者名` 可以根据作者名称进行精确搜索。
- 使用 `title:书名` 可以根据书名进行精确搜索。
- 使用 `subject:主题` 可以根据书籍的类型或主题进行搜索。

**不适用场景：**
- 该工具不适用于电子书、有声书的查询，也不支持购买书籍或阅读书籍的实际内容。