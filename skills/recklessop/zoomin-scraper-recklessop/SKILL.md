---
name: zoomin-scraper
description: 使用 Playwright 浏览器自动化工具从 Zoomin Software 的门户网站中抓取文档内容，以处理动态内容的加载问题。当使用标准的网络请求方法（如 requests 和 BeautifulSoup）无法获取到有效的数据，或者无法捕获到文档的主体内容时，可以采用此方法。
---
# Zoomin Scraper 技能

该技能提供了一种从由 Zoomin Software 提供支持的文档门户中高效抓取内容的机制。它利用 Playwright 启动一个无头 Chromium 浏览器，执行 JavaScript 代码，等待动态内容加载完成后，再从主文章主体中提取渲染出的文本。

## 使用方法

要使用此技能，您需要提供一个包含 URL 列表的文件（每行一个 URL）。技能会处理每个 URL，并将提取的内容保存到指定的输出目录中。

### 先决条件（手动设置）

此技能依赖于 Playwright。首次在新系统上使用此技能之前，您必须通过运行以下命令在终端中手动安装 Playwright 及其浏览器二进制文件：

```bash
pip install playwright
playwright install chromium
```
这些命令应在您计划用于该技能的虚拟环境中执行。

### 运行抓取器

要运行抓取器，请调用 `run_scraper.sh` 脚本（该脚本位于技能的 `scripts/` 目录中）。此脚本会在执行主要的 Python Playwright 脚本之前激活您指定的 Python 虚拟环境。

**`run_scraper.sh` 的参数：**

*   **`urls_file`**：包含要抓取的 URL 的文本文件的路径（每行一个 URL）。
*   **`output_directory`**（可选）：保存抓取内容的目录。如果未提供，默认为 `scraped_docs_output`。
*   **`venv_path`**：您的 Python 虚拟环境的绝对路径（例如：`/home/justin/scraper/.env`）。

**示例：**

假设您的 URL 列表位于 `path/to/urls.txt` 文件中，您希望将输出结果保存到 `my_scraped_docs/` 目录中，并且您的虚拟环境位于 `path/to/my_venv`：

```bash
zoomin-scraper urls_file="path/to/urls.txt" output_directory="my_scraped_docs" venv_path="path/to/my_venv"
```

脚本将启动一个无头 Chromium 浏览器，访问每个 URL，等待主要内容加载（具体目标是 `<article id="zDocsContent">`），然后保存提取的文本。脚本会设置用户代理以模拟普通浏览器，并在请求之间添加短暂的延迟，以减少对服务器的负担。