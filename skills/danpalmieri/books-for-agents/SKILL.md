# 为AI代理准备的书籍资源

这是一个开源的知识库，其中包含结构化的书籍摘要，任何AI代理都可以通过MCP访问这些资源。

## 设置

1. 如果您还没有安装`books-for-agents` MCP服务器，请先进行安装：

```
claude mcp add --transport http books-for-agents https://booksforagents.com/mcp
```

或者将其添加到您的MCP配置文件中：

```json
{
  "mcpServers": {
    "books-for-agents": {
      "url": "https://booksforagents.com/mcp"
    }
  }
}
```

2. 安装完成后，您就可以使用以下所有功能了。

## 可以执行的操作

### 搜索书籍

使用`search_books`可以根据主题、关键词或问题来查找书籍。该功能支持混合搜索（全文搜索 + 语义向量嵌入）。

```
search_books({ query: "how to build better habits" })
search_books({ query: "leadership", category: "business" })
search_books({ query: "cognitive biases and decision making", limit: 3 })
```

### 阅读书籍摘要

使用`get_book`可以根据书籍的slug或标题获取其完整的结构化摘要（部分匹配也是支持的）。

```
get_book({ slug: "atomic-habits" })
get_book({ title: "Deep Work" })
```

### 阅读特定章节

使用`get_book_section`可以仅获取书籍的某个章节——当您不需要整个摘要时，这种方法可以节省大量计算资源。可获取的章节包括：`ideas`（想法）、`frameworks`（框架）、`quotes`（名言）、`connections`（关联内容）、`when-to-use`（使用场景）。

```
get_book_section({ slug: "the-lean-startup", section: "frameworks" })
get_book_section({ slug: "clean-code", section: "quotes" })
get_book_section({ slug: "thinking-fast-and-slow", section: "when-to-use" })
```

### 浏览分类

使用`list_categories`可以查看所有可用的分类以及每个分类下包含的书籍数量。

```
list_categories()
```

### 建议新书籍

使用`suggest_book`可以将新书籍添加到待生成的书单中。系统会检查新书籍是否与已发布的书籍或现有书单条目重复。

```
suggest_book({ title: "Thinking in Bets", author: "Annie Duke", category: "psychology" })
```

### 查看待生成的书单

使用`list_backlog`可以查看所有待生成的书籍及其状态。

```
list_backlog()
```

### 生成书籍摘要

使用`generate_book`可以获取生成书籍摘要所需的模板、示例、元数据及说明。您可以指定书籍的标题，也可以让系统自动选择下一个待生成的书籍。

```
generate_book()
generate_book({ title: "Never Split the Difference" })
```

生成内容后，调用`submit_book`将其发布到知识库中。

### 发布书籍摘要

使用`submit_book`将生成的摘要直接发布到知识库中。请在调用`generate_book`生成内容后执行此操作。

```
submit_book({
  slug: "never-split-the-difference",
  title: "Never Split the Difference",
  author: "Chris Voss",
  category: "business",
  content: "---\ntitle: \"Never Split the Difference\"\n..."
})
```

## 提示

- 如果只需要书籍的某个部分，建议使用`get_book_section`，这样可以节省大量计算资源。
- 使用`search_books`时请使用自然语言查询——该功能基于语义理解进行搜索，而不仅仅是关键词匹配。
- 在生成书籍内容时，请严格遵循`generate_book`返回的模板和说明。所有内容都必须使用英文。
- 书籍之间的关联内容应使用`[[slug]]`格式，并且只能引用已存在的书籍。