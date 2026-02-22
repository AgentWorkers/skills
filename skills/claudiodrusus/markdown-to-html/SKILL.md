---
name: markdown-to-html
description: 将 Markdown 文本转换为格式美观、结构完整的 HTML 文档，并嵌入 CSS 样式。非常适合用于新闻通讯、文档、报告和电子邮件模板。
triggers:
  - convert markdown to html
  - markdown to html
  - render markdown
  - style markdown
---
# Markdown to HTML 转换器

这是一个完全不依赖外部库的 Python 工具，可以将 Markdown 文件转换为美观且自包含的 HTML 文档，并带有内嵌的 CSS 样式。它仅使用 Python 的标准库。

## 主要特性

- **全面的 Markdown 支持**：支持标题、加粗文本、斜体文本、下划线文本、链接、图片、带有语法提示的代码块、块引用、有序列表、无序列表、水平分隔线以及表格。
- **内置两种主题**：Light（受 GitHub 风格启发）和 Dark 模式，颜色经过精心挑选。
- **自包含的输出**：所有 CSS 都被内嵌在 HTML 文件中，因此无需任何外部依赖即可正常使用。
- **响应式设计**：无论在桌面还是移动设备上，输出效果都非常好。
- **支持标准输入（stdin）**：可以直接将内容通过管道（pipe）传递给该工具，以便在 shell 流程中使用。

## 使用示例

- 使用默认的 Light 主题转换文件：
  ```bash
  ```bash
python main.py README.md -o readme.html
```
  ```

- 使用 Dark 主题制作演示文稿：
  ```bash
  ```bash
python main.py notes.md -o notes.html --theme dark --title "Meeting Notes"
```
  ```

- 从其他命令中获取内容并转换：
  ```bash
  ```bash
cat CHANGELOG.md | python main.py - -o changelog.html
```
  ```

- 在新闻通讯的生成流程中使用该工具：
  ```bash
  ```bash
python main.py issue-42.md --title "Lobster Diary #42" -o issue.html
```
  ```

## 支持的 Markdown 元素

| 元素        | 语法                | 是否支持       |
|-------------|------------------|-------------|
| 标题         | `# H1` 到 `###### H6`       | ✅           |
| 加粗文本       | `**文本**           | ✅           |
| 斜体文本       | `*文本*`           | ✅           |
| 下划线文本       | `~~文本~~`         | ✅           |
| 链接         | `[文本](链接)`         | ✅           |
| 图片          | `![alt](图片链接)`       | ✅           |
| 代码块        | 三重反引号（指定语言）      | ✅           |
| 内联代码       | 单重反引号          | ✅           |
| 块引用        | `> 文本`           | ✅           |
| 无序列表       | `- 条目` 或 `* 条目`       | ✅           |
| 有序列表       | `1. 条目`           | ✅           |
| 水平分隔线       | `---`            | ✅           |

## 命令行选项

- `input`      | Markdown 文件路径（或 `-` 表示从标准输入读取） |
- `-o, --output` | 输出 HTML 文件的路径（默认为标准输出） |
- `--theme`     | 主题（Light 或 Dark，默认为 Light）   |
- `--title`     | HTML 文档的标题（默认为 "Document"） |