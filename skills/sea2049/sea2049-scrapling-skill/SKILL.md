---
name: scrapling
description: 每当用户请求抓取网站、从网页中提取结构化数据、处理反爬虫/Cloudflare保护页面、爬取多个页面，或明确提到“Scrapling”（数据抓取）时，请使用此技能。该技能提供了一个实用的Scrapling（数据抓取）工作流程：包括安装相关工具、选择合适的数据获取工具、数据提取方法以及爬取策略，从而实现可靠的Python网络数据抓取。
---
# 网页抓取技能

## 目标

使用网页抓取技术来提取网页数据，同时尽量减少选择器失效的情况，并提高抗机器人攻击的能力。  

当用户需要以下功能时，建议使用此技能：  
- 网站抓取  
- 从HTML页面中提取数据  
- 具备抗Cloudflare/反机器人攻击能力的抓取  
- 多页面爬取  
- 将抓取任务转换为可重用的Python脚本  

## 安全性与合法性  

在开始抓取之前，请务必：  
1. 确认目标网站符合用户需求及当地法律法规。  
2. 避免未经授权的访问、绕过登录机制或抓取私人数据。  
3. 遵守目标网站的条款规定，并控制请求频率。  
4. 对于高流量抓取任务，需设置延迟机制或域名级别的请求限制。  

## 默认环境（当前机器）  

所有依赖项应存放于`D:\clawtest`目录下。  

推荐的设置命令：  
```powershell  
python -m venv D:\clawtest\.venv  
D:\clawtest\.venv\Scripts\python -m pip install -U pip  
D:\clawtest\.venv\Scripts\python -m pip install "scrapling[fetchers]"  
D:\clawtest\.venv\Scripts\scrapling install  
```  

**说明：**  
- 如果只是简单的静态HTML数据提取，只需执行`pip install scrapling`即可。  
- 如果需要使用基于浏览器的数据获取工具，需要执行`scraping install`。  

## 选择器使用指南  

根据实际情况选择最合适的工具：  
1. **`Fetcher`**：适用于静态页面，抓取速度较快。  
2. **`StealthyFetcher`**：在存在反机器人机制的情况下为默认选择。  
3. **`DynamicFetcher`**：用于处理由JavaScript渲染的数据。  
4. **`Spider`**：适用于多页面爬取、任务排队、并发处理以及结构化数据输出。  

## 标准工作流程：  
1. 首先确定需要提取的目标字段及数据格式。  
2. 选择合适的抓取工具（从`Fetcher`开始，必要时可升级为`StealthyFetcher`或`DynamicFetcher`）。  
3. 使用CSS/XPath提取数据，并将其转换为JSON格式。  
4. 将数据保存为JSON、JSONL或CSV格式。  
5. 在生产环境中添加重试机制、超时设置以及适当的延迟策略。  

## 代码模板：  

### 1) 单页数据提取（默认使用`StealthyFetcher`）  
```python  
from scrapling.fetchers import StealthyFetcher  

StealthyFetcher.adaptive = True  
url = "https://example.com/products"  
page = StealthyFetcher.fetch(url, headless=True, network_idle=True, timeout=45000)  

items = []  
for card in page.css(".product-card", auto_save=True):  
    items.append({  
        "title": card.css("h2::text").get(default="").strip(),  
        "price": card.css("price::text").get(default="").strip(),  
        "url": card.css("a::attr.href").get(default="")  
    })  
print(items)  
```  

### 2) 应对页面布局变化的情况  
**首次抓取时存储页面特征信息：**  
```python  
products = page.css(".product-card", auto_save=True)  
```  
**后续抓取时根据布局变化重新获取数据：**  
```python  
products = page.css(".product-card", adaptive=True)  
```  

### 3) 使用`Spider`进行多页面爬取  
```python  
from scrapling.spiders import Spider, Response  

class ProductSpider(Spider):  
    name = "product_spider"  
    start_urls = ["https://example.com/catalog"]  

    async def parse(self, response: Response):  
        for card in response.css(".product-card"):  
            yield {  
                "title": card.css("h2::text").get(default="").strip(),  
                "price": card.css("price::text").get(default="").strip()  
            }  
        for href in response.css("a.next::attr(href").all():  
            yield response.follow(href, callback=self.parse)  

if __name__ == "__main__":  
    ProductSpider().start()  
```  

## 辅助工具的输出格式：  
在执行用户任务时，应提供以下信息：  
1. 选择的抓取工具及原因  
2. 为目标网站定制的可执行脚本或代码片段  
3. 适用于当前机器的安装/运行命令  
4. 数据的输出路径及格式  
5. 抗机器人攻击的可靠性说明及备用方案  

## 实用性备用方案：  
如果数据提取失败，可尝试以下方法：  
1. 在新的HTML页面上重新验证选择器的有效性。  
2. 将抓取工具切换为`StealthyFetcher`。  
3. 对于由JavaScript渲染的数据，切换为`DynamicFetcher`。  
4. 启用选择器的自适应功能（`auto_save=True`和`adaptive=True`）。  
5. 增加重试次数、设置延迟机制，并降低请求频率。