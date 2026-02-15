# Web Clipper

该工具可以从任何URL中提取可读内容，并将其保存为格式规范的Markdown格式，存储在`memory/clippings/`目录中。非常适合用于研究、文档编写和资料归档。

## 使用方法

```bash
node skills/web-clipper/index.js <url>
```

示例：
```bash
node skills/web-clipper/index.js https://example.com/article
```

## 主要功能

- **可读性优化**：自动去除广告、侧边栏等干扰元素。
- **Markdown转换**：将HTML内容转换为格式规范的Markdown格式。
- **元数据记录**：在文档的开头部分保存标题、作者、日期和来源URL。
- **持久化存储**：将提取的内容长期保存在`memory/clippings/`目录中，便于后续查阅。

## 安装要求

使用该工具需要安装以下依赖库：`axios`、`jsdom`、`@mozilla/readability`和`turndown`。这些依赖库通过`package.json`文件进行管理。请在当前目录中运行`npm install`命令进行安装。