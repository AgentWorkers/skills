---
name: abstract-searcher
description: 通过浏览器查询学术数据库（arXiv、Semantic Scholar、CrossRef）为.bib文件中的条目添加摘要；如果浏览器查询失败，则使用备用方法（fallback method）来获取摘要。
---
# 摘要搜索器

该工具能够自动从 BibTeX 文档中获取并添加论文摘要。

## 使用方法

给定一个 `.bib` 文件，该工具将执行以下操作：
1. 解析每个 BibTeX 条目；
2. 通过多个来源搜索论文摘要：
   - arXiv API（用于 arXiv 论文）
   - Semantic Scholar API
   - CrossRef API
   - OpenAlex API；
3. **如果 API 请求失败**：使用浏览器自动化功能在 Google Scholar 中进行搜索；
4. 为每个条目添加 `abstract={...}` 字段；
5. 返回修改后的完整 `.bib` 文件。

## 快速入门

```bash
# Process a bib file (API-based)
python3 {baseDir}/scripts/add_abstracts.py input.bib > output.bib
```

## API 来源（无需密钥）

1. **arXiv API**：`http://export.arxiv.org/api/query?search_query=...`
2. **Semantic Scholar**：`https://api.semanticscholar.org/graph/v1/paper/search?query=...`
3. **CrossRef**：`https://api.crossref.org/works?query.title=...`
4. **OpenAlex**：`https://api.openalex.org/works?search=...`

## 浏览器回退机制（非常重要！）

当 API 无法找到摘要时，**需要使用 Chrome 浏览器进行手动搜索**：

### 第一步：打开 Chrome 浏览器并创建一个新的标签页
```
# Check if tab is attached
browser action=tabs profile=chrome

# If no tabs, ask user to click the Clawdbot Browser Relay toolbar icon
# Or use mac-control skill to auto-click it
```

### 第二步：在 Google Scholar 中进行搜索
```
browser action=open profile=chrome targetUrl="https://scholar.google.com"
browser action=snapshot profile=chrome

# Type the paper title in search box
browser action=act profile=chrome request={"kind":"type","ref":"search box ref","text":"paper title here"}
browser action=act profile=chrome request={"kind":"press","key":"Enter"}
browser action=snapshot profile=chrome
```

### 第三步：点击搜索结果
```
# Find the paper in results, click to open
browser action=act profile=chrome request={"kind":"click","ref":"paper title link ref"}
browser action=snapshot profile=chrome
```

### 第四步：从页面中提取摘要
- **ScienceDirect**：在页面中查找“Abstract”部分；
- **ACL Anthology**：摘要直接显示在页面顶部；
- **Springer/Wiley**：可能需要点击“Abstract”按钮才能查看摘要；
- **PubMed**：摘要通常可以直接查看。

### 第五步：复制摘要并将其格式化为 BibTeX 格式
```
# Get the abstract text from snapshot
# Clean it: remove newlines, escape special chars
# Add to bib entry: abstract={...},
```

### 提示：
- 使用 `profile=chrome` 选项以确保使用已登录的 Chrome 浏览器；
- Google Scholar 通常不会屏蔽真实的 Chrome 浏览器；
- ScienceDirect 和 IEEE 的资源可能需要机构登录（你的 Chrome 浏览器应已配置相关登录信息）；
- 在复制摘要之前，请务必确认摘要与正确的论文匹配！

## 注意事项：
- API 请求之间有 2 秒的延迟限制；
- 浏览器回退机制应该能够找到几乎所有论文的摘要；
- 提取的摘要会进行格式化处理（删除换行符，并对特殊字符进行转义，以便用于 BibTeX）；
- 在复制摘要之前，请务必确认摘要与对应的论文一致！

## 其他说明：