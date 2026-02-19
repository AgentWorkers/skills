---
name: desearch-crawl
description: >
  **功能说明：**  
  能够爬取/抓取任意网页的文本内容，并将其提取为纯文本或原始HTML格式。当您需要获取特定网页的全部内容时，可以使用此功能。  
  **使用场景：**  
  - 用于分析网页的结构和数据  
  - 用于提取网页上的特定信息（如标题、链接、图片等）  
  - 用于自动化处理大量网页  
  **返回结果类型：**  
  - 纯文本（plain text）  
  - 原始HTML（raw HTML）  
  **示例用法：**  
  ```python
  # 使用爬虫库（如requests、BeautifulSoup等）从网页URL获取内容  
  response = requests.get('https://example.com')  
  html_content = response.text  # 获取纯文本内容  
  soup = BeautifulSoup(html_content, 'html.parser')  # 使用BeautifulSoup解析HTML内容  
  # 根据需求选择返回类型：  
  if you_need_pure_text:  
      pure_text = soup.text  # 获取纯文本  
  else:  
      html_content = soup.get_html()  # 获取原始HTML内容  
  ```
metadata: {"clawdbot":{"emoji":"🕷️","homepage":"https://desearch.ai","requires":{"env":["DESEARCH_API_KEY"]}}}
---
# 使用 Desearch 爬取网页

从任意网页 URL 中提取内容。返回纯文本或原始 HTML。

## 设置

1. 从 [https://console.desearch.ai](https://console.desearch.ai) 获取 API 密钥。
2. 设置环境变量：`export DESEARCH_API_KEY='your-key-here'`（将 `your-key-here` 替换为实际的 API 密钥）。

## 使用方法

```bash
# Crawl a webpage (returns clean text by default)
scripts/desearch.py crawl "https://en.wikipedia.org/wiki/Artificial_intelligence"

# Get raw HTML
scripts/desearch.py crawl "https://example.com" --crawl-format html
```


## 选项

| 选项 | 描述 |
|--------|-------------|
| `--crawl-format` | 输出内容格式：`text`（默认）或 `html` |

## 示例

### 阅读文档页面
```bash
scripts/desearch.py crawl "https://docs.python.org/3/tutorial/index.html"
```

### 获取原始 HTML 用于分析
```bash
scripts/desearch.py crawl "https://example.com/page" --crawl-format html
```