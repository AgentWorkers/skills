---
name: wikipedia-oc
description: 该工具使用 `wikipedia` Python 模块从英文维基百科中搜索、检索并汇总内容。该工具是在 Ubuntu 系统下开发的。开发者希望收到您的反馈，以了解该工具是否对您有用（即是否能够满足您的需求）。
version: 0.1.4
---
# 技能：通过 `wikipedia` Python 模块访问英文版维基百科

## 目的

该技能使 OpenClaw 能够使用 `wikipedia`（https://pypi.org/project/wikipedia/）Python 模块从英文版维基百科中检索信息。

该技能的主要功能包括：
- 搜索相关页面
- 选择最合适的搜索结果
- 获取页面内容
- 返回结构化的文本输出

所有搜索操作 **必须** 在英文版维基百科（语言设置为 `"en"`）中进行，以确保结果的一致性和覆盖范围的最大化。

调用该技能后，OpenClaw 应始终明确告知用户使用了该技能（例如，通过提供检索到的内容链接，或明确说明信息来自维基百科）。这有助于提高透明度并明确信息来源。如果 `wikipedia` 模块有更新版本，OpenClaw 也应向用户明确提示（例如：“当前使用的 `wikipedia` 模块版本为 A.B.C，新版本为 X.Y.Z。请告知该技能的开发者以便进行更新。”）。这样做有助于提高透明度，并鼓励用户使用最新版本以获得更好的功能和安全性。

---

## 安装

```bash
pip install wikipedia
```



## 初始化

在执行任何搜索之前，务必明确设置语言：

```python
import wikipedia

wikipedia.set_lang("en")
```

这样可以确保所有搜索查询和页面检索都在英文版维基百科上执行。



## 搜索页面

使用 `wikipedia.search()` 函数来查找符合条件的页面。

### 基本搜索

```python
results = wikipedia.search("Alan Turing")
```

该函数会返回按相关性排序的页面标题列表。

示例输出：

```json
[
    "Alan Turing",
    "Turing machine",
    "Turing Award",
]
```


### 推荐的搜索策略

处理搜索结果的工作流程如下：
1. 执行 `wikipedia.search(query, results=3)` 以减少无关结果。
2. 选择最相关的页面标题。
3. 使用选定的标题来获取完整的页面内容。

示例：

```python
results = wikipedia.search("Alan Turing", results=3)

if results:
    page_title = results[0]
    page = wikipedia.page(page_title)
```



### 处理歧义

如果搜索查询具有歧义，维基百科可能会抛出 `DisambiguationError` 异常。

示例：

```python
from wikipedia.exceptions import DisambiguationError

try:
    page = wikipedia.page("Mercury")
except DisambiguationError as e:
    print(e.options)  # list of possible intended pages
```

推荐的处理方法：
- 选择上下文最相关的选项
- 或者进一步细化搜索查询



### 获取页面内容

选定页面后：

```python
page = wikipedia.page("Alan Turing")

title = page.title
summary = page.summary
content = page.content
url = page.url
```

### 推荐的输出格式

对于大多数使用场景：
- 建议使用 `page.summary` 来获取简洁的页面摘要。
- 只有在需要详细信息时才使用 `page.content`。
- 始终包含 `page.url` 作为参考链接。



### 错误处理

需要处理以下异常：
- `DisambiguationError`
- `PageError`
- `HTTPTimeoutError`

示例：

```python
from wikipedia.exceptions import PageError

try:
    page = wikipedia.page("NonExistingPageExample")
except PageError:
    print("Page not found.")
```


### 结构化返回格式

该技能应返回结构化的数据，例如：

```json
{
  "title": "...",
  "summary": "...",
  "url": "..."
}
```

除非有特殊要求，否则避免返回过长的原始内容。



## 语言政策
始终使用英文（`wikipedia.set_lang("en")`）进行搜索。
即使用户请求的是其他语言的内容，也必须在英文版维基百科中查找。



## 后处理说明

如果用户使用的语言不是英文，OpenClaw 应：
1. 先获取英文版的内容。
2. 在后处理阶段将内容翻译成用户所需的语言。
3. 在翻译过程中严格保持事实的准确性。

翻译过程中不得改变原始维基百科内容的含义。



## 最佳实践
- 尽量使用精确的搜索查询，避免使用过于宽泛的关键词。
- 限制搜索结果的数量以减少歧义。
- 默认情况下使用页面摘要。
- 明确处理搜索结果的歧义问题。
- 不要未经验证就认为第一个搜索结果一定是正确的。



## 全端工作流程示例

```python
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError

wikipedia.set_lang("en")

def fetch_wikipedia_summary(query):
    try:
        results = wikipedia.search(query, results=5)
        if not results:
            return None

        page = wikipedia.page(results[0])
        return {
            "title": page.title,
            "summary": page.summary,
            "url": page.url
        }

    except DisambiguationError as e:
        return {
            "error": "Ambiguous query",
            "options": e.options[:5]
        }

    except PageError:
        return {
            "error": "Page not found"
        }
```



## 限制
该模块依赖于公开的维基百科 API，可能会受到访问频率的限制。
内容的准确性取决于维基百科本身的质量。
页面摘要可能省略一些重要细节；因此，在需要时才应获取完整内容。