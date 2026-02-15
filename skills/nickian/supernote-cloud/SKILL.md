---
name: supernote
description: 访问自托管的 Supernote 私有云实例，以浏览文件和文件夹、上传文档（PDF、EPUB 格式）及笔记，将网页文章转换为 EPUB/PDF 格式并发送到设备上，查看存储容量，并导航目录树。当用户提到 Supernote、电子墨水设备文件、希望在 Supernote 云上上传/浏览文档，或希望将文章/URL 发送到电子阅读器时，请使用此功能。
---

# Supernote 私有云

您可以通过其反向工程的 REST API 在自托管的 Supernote 私有云上浏览、上传和管理文件。该系统还支持将网页内容转换为电子书（EPUB 格式），以便发送到设备上。

## 设置

```bash
export SUPERNOTE_URL="http://192.168.50.168:8080"
export SUPERNOTE_USER="your@email.com"
export SUPERNOTE_PASSWORD="your_password"
```

文章转换所需的 Python 库：`readability-lxml`、`ebooklib`、`requests`、`beautifulsoup4`、`lxml`。

## 命令

### 将网页文章发送到设备

```bash
{baseDir}/scripts/supernote.sh send-article --url "https://example.com/article" --format epub --dir-path Document
{baseDir}/scripts/supernote.sh send-article --url "https://example.com/article" --format pdf --dir-path "Document/Articles"
{baseDir}/scripts/supernote.sh send-article --url "https://example.com/article" --title "Custom Title" --dir-path Document
```

1. 获取文章内容。
2. 提取包含图片的可读文本。
3. 将文本转换为格式规范的 EPUB 或 PDF 格式。
4. 将文件上传到指定的文件夹（默认格式：EPUB；默认文件夹：Document）。

### 列出目录内容

```bash
{baseDir}/scripts/supernote.sh ls
{baseDir}/scripts/supernote.sh ls --path Document
{baseDir}/scripts/supernote.sh ls --path "Note/Journal"
{baseDir}/scripts/supernote.sh ls --dir 778507258886619136
```

### 目录结构

```bash
{baseDir}/scripts/supernote.sh tree --depth 2
```

### 通过路径查找目录 ID

```bash
{baseDir}/scripts/supernote.sh find-dir --path "Document/Books"
```

### 上传文件

```bash
{baseDir}/scripts/supernote.sh upload --file /path/to/file.pdf --dir-path Document
{baseDir}/scripts/supernote.sh upload --file /path/to/book.epub --dir-path "Document/Books"
{baseDir}/scripts/supernote.sh upload --file /path/to/file.pdf --dir 778507258773372928 --name "Renamed.pdf"
```

### 检查存储空间

```bash
{baseDir}/scripts/supernote.sh capacity
```

### 手动登录

```bash
{baseDir}/scripts/supernote.sh login
```

## 默认文件夹

| 文件夹 | 用途 |
|--------|---------|
| Note   | 手写笔记（.note 文件） |
| Document | PDF、EPUB 文件及其他文档 |
| Inbox | 收到的文件 |
| Export | 导出的内容 |
| Screenshot | 截图 |
| Mystyle | 自定义样式/模板 |

## 注意事项：

- 建议使用 EPUB 格式存储文章——该格式在电子墨水显示屏上显示效果良好，且文本具有自动排版功能。
- 该 API 是反向工程实现的，属于非官方版本；端点可能会因固件更新而发生变化。
- 目录路径可以使用路径名（例如：“Document/Books”）或数字 ID 来指定。
- 有些网站会阻止爬虫访问；如果请求失败，请尝试使用其他 URL 或缓存/保存的页面。