---
name: internet-search
description: "如何有效使用 internet_search 工具——包括分类路由、查询构建以及多搜索策略。无论何时需要通过网络搜索（无论是获取时事新闻、研究论文、社区观点，还是超出培训知识范围的任何信息），都可以使用该工具。"
metadata:
  {
    "openclaw":
      {
        "emoji": "🔍"
      }
  }
---
# 网络搜索

该功能用于查询自托管的 SearXNG 实例，该实例集成了多个搜索引擎。

## 分类路由

请始终根据查询的性质来设置 `category`（分类）：

| 分类        | 使用场景                                                         | 支持的搜索引擎                                      |
|------------|---------------------------------------------------------------------|--------------------------------------------------|
| `general`    | 默认分类。包含事实信息、操作指南、产品信息、人物信息以及通用网页内容。                | Brave、Bing、DDG、Startpage、Qwant、Wikipedia 等          |
| `news`      | 最新事件、突发新闻以及任何时效性强的内容。                              | Bing News、DDG News                              |
| `academic`    | 研究论文、学术研究、医学文献、预印本。                               | arXiv、Google Scholar、PubMed                        |
| `social`     | 用户观点、社区推荐内容、“人们对 X 有什么看法”。                            | Reddit                                           |

## 查询格式

请按照搜索引擎的期望来编写查询语句——使用关键词，而非完整的句子：

```
# Bad
"what is the fastest async runtime for rust"

# Good
"rust async runtime benchmarks 2025"
```

- **新闻**：需要指定时间范围，例如：“`OpenAI o3 release 2025`”（而不是仅输入 “`OpenAI o3`”）
- **学术**：使用专业术语，例如：“`transformer attention efficiency survey`”
- **社交**：以社区搜索的形式提出问题，例如：“`reddit best mechanical keyboard 2025`”

## SearXNG 的搜索语法（在 `query` 参数中）

SearXNG 支持多种轻量级的查询修饰符，可以直接嵌入到 `query` 字符串中：

| 语法        | 含义                                      | 示例                                      |
|-------------|-----------------------------------------|-----------------------------------------|
| `!<engine>` / `!<category>` | 选择特定的搜索引擎或分类。支持链式调用；允许使用缩写。                | `!wp paris`、`!wikipedia paris`、`!map paris`、`!map !ddg !wp paris` |
| `:<lang>`      | 语言过滤                      | `:fr !wp Wau Holland`                          |

## 查询结果数量

- `count=5`（默认值）：适用于大多数查询场景
- `count=10`：用于比较多个选项或检查共识
- `count=3`：用于快速核对事实信息

## 多搜索引擎搜索策略

建议执行多个针对性的搜索，而非使用单一的广泛搜索：

```
# Bad: one vague search
internet_search("best way to deploy Node.js")

# Good: three targeted searches
internet_search("Node.js Docker deployment best practices 2025")
internet_search("Node.js PM2 vs Docker production", category="social")
internet_search("Node.js zero-downtime deployment strategies")
```

将 `general` 和 `social` 分类结合使用，以获取更全面的信息（包括事实内容和用户意见）：

```
internet_search("Bun runtime performance vs Node.js benchmarks")
internet_search("Bun runtime production experience", category="social")
```

## 不适用的情况

- 对于已经非常确定的内容
- 对于内容稳定或语法明确的文档（建议使用现有的知识库或官方文档）
- 重复执行已经得到答案的搜索请求

## 常见错误

| 错误类型                | 应对方法                                      |
|-------------------|-----------------------------------------|
| 使用 `general` 分类查询学术论文       | 应使用 `category="academic"`                   |
- 输入 “今天发生了什么”           | 应使用 `category="news"` 并指定具体主题             |
- 对于复杂问题使用单一的广泛搜索       | 应将问题拆分为 2–3 个具体的搜索请求             |
- 机械地重复失败的搜索请求         | 应使用不同的关键词重新构建查询                 |
- 对于简单的事实性问题设置 `count=20`       | 默认的 `count=5` 几乎总是足够的                 |