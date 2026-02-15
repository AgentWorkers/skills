---
name: remarkable
description: 通过 reMarkable Cloud 将文件和网页文章发送到 reMarkable 电子墨水平板电脑。您可以上传 PDF 或 EPUB 文件，或将网页文章转换为可阅读的电子书并发送到该设备上。同时，您还可以在设备上浏览和管理文件。当用户提到 reMarkable、希望将文章或文档发送到他们的电子阅读器，或需要管理 reMarkable 云端的文件时，可以使用此功能。
---

# reMarkable Cloud

通过云API将文档和网页文章发送到reMarkable平板电脑。使用`rmapi`进行云访问。

## 设置

安装`rmapi`（需要Go语言环境）：
```bash
cd /tmp && git clone --depth 1 https://github.com/ddvk/rmapi.git
cd rmapi && go build -o /usr/local/bin/rmapi .
```

首次运行时，系统会提示您从https://my.remarkable.com/device/browser?showOtp=true获取一次性的验证码。

Python依赖库（用于文章转换）：`readability-lxml`、`ebooklib`、`requests`、`beautifulsoup4`、`lxml`。

## 命令

### 将网页文章发送到设备

```bash
{baseDir}/scripts/remarkable.sh send-article --url "https://example.com/article" --dir /Articles
{baseDir}/scripts/remarkable.sh send-article --url "https://example.com/article" --format pdf --dir /
{baseDir}/scripts/remarkable.sh send-article --url "https://example.com/article" --title "Custom Title" --dir /Articles
```

- 从指定网址获取文章内容
- 提取可阅读的内容
- 将内容转换为EPUB或PDF格式
- 上传到reMarkable云端
- 设备会自动同步内容

### 列出文件

```bash
{baseDir}/scripts/remarkable.sh ls /
{baseDir}/scripts/remarkable.sh ls /Articles
{baseDir}/scripts/remarkable.sh ls "/Book Notes"
```

输出格式：`[f]` 表示文件，`[d]` 表示目录

### 上传文件

```bash
{baseDir}/scripts/remarkable.sh upload --file /path/to/document.pdf --dir /Books
{baseDir}/scripts/remarkable.sh upload --file /path/to/book.epub --dir /
```

### 创建文件夹

```bash
{baseDir}/scripts/remarkable.sh mkdir --path /NewFolder
```

### 搜索文件

```bash
{baseDir}/scripts/remarkable.sh find --name "article title"
```

## 注意事项：

- 建议使用EPUB格式的文件，因为其在电子墨水屏上显示效果更好
- 设备在连接到WiFi时会自动同步内容
- `rmapi`会将认证令牌缓存到`~/.rmapi`文件夹中
- 有些网站会阻止爬虫访问——如果文章获取失败，请尝试其他URL