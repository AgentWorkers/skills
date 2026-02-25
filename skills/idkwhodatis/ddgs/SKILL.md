# DDGS 网页搜索功能  
该功能通过 DDGS（Dux Distributed Global Search）引擎实现网页搜索，汇总来自多种搜索服务的结果以获取实时信息。  

## 主要特性  
🔍 遵守隐私规定的元搜索工具  
📰 新闻搜索支持  
🖼️ 图片搜索支持  
📹 视频搜索支持  
📚 图书搜索支持  
🌐 免费使用，无需 API 密钥  
🔒 保护用户隐私，不追踪用户行为  
⚡ 支持 MCP（模型上下文协议）和 API 服务器  

## 安装  
```bash  
# 推荐使用 uv 进行安装  
uv pip install ddgs  

# 或者使用 pip 安装  
pip install ddgs  
```  

## 快速入门  

### 1. 文本搜索  
最常用的搜索方式，返回网页结果：  
```python  
python -c """  
from ddgs import DDGS  

query = '你的搜索关键词'  

results = DDGS().text(  
    query,  
    region='wt-wt',        # 地区：cn-zh（中国），us-en（美国），wt-wt（全球）  
    safesearch='moderate',  # 安全搜索：开启/关闭  
    timelimit='m',         # 时间范围：d（天），w（周），m（月），y（年），None（无限制）  
    max_results=10,        # 最大结果数量  
    backend='auto'         # 后端：auto，duckduckgo，brave，bing 等  
)  

for i, r in enumerate(results, 1):  
    print(f\"{i}. {r.get('title')}\")  
    print(f\"   链接: {r.get('href')}\")  
    print(f\"   摘要: {str(r.get('body'))[:100]}...\n")  
"""  
```  

### 2. 新闻搜索  
搜索最新新闻：  
```python  
python -c """  
from ddgs import DDGS  

results = DDGS().news(  
    '人工智能技术',  
    region='wt-wt',  
    safesearch='moderate',  
    timelimit='d',       # d=过去 24 小时，w=过去一周，m=过去一个月  
    max_results=10  
)  

for r in results:  
    print(f\"📰 {r.get('标题')}\")  
    print(f\"   来源: {r.get('source')}\")  
    print(f\"   日期: {r.get('date')}\")  
    print(f\"   链接: {r.get('url')}\")  
"""  
```  

### 3. 图片搜索  
搜索图片资源：  
```python  
python -c """  
from ddgs import DDGS  

results = DDGS().images(  
    '可爱的猫咪',  
    region='wt-wt',  
    safesearch='moderate',  
    size='Medium',       # 小型、中型、大型、壁纸  
    type_image='photo',  # 照片、剪贴画、gif、透明图  
    layout='Square',     # 正方形、高屏、宽屏  
    max_results=10  
)  

for r in results:  
    print(f\"🖼️ {r.get('标题')}\")  
    print(f\"   图片: {r.get('image')}\")  
    print(f\"   缩略图: {r.get('thumbnail')}\")  
    print(f\"   来源: {r.get('source')}\")  
"""  
```  

### 4. 视频搜索  
搜索视频内容：  
```python  
python -c """  
from ddgs import DDGS  

results = DDGS().videos(  
    'Python 编程',  
    region='wt-wt',  
    safesearch='moderate',  
    timelimit='w',       # d、w、m  
    resolution='high',   # 高画质、标准画质  
    duration='medium',   # 短片、中等时长、长片  
    max_results=10  
)  

for r in results:  
    print(f\"📹 {r.get('标题')}\")  
    print(f\"   时长: {r.get('duration', 'N/A')}\")  
    print(f\"   出版商: {r.get('publisher')}\")  
    print(f\"   链接: {r.get('content')}\")  
"""  
```  

### 5. 图书搜索  
搜索书籍：  
```python  
python -c """  
from ddgs import DDGS  

results = DDGS().books(  
    '杰克·伦敦（Jack London）',  
    max_results=5  
)  

for r in results:  
    print(f\"📚 {r.get('标题')}\")  
    print(f\"   作者: {r.get('author')}\")  
    print(f\"   出版商: {r.get('publisher')}\")  
    print(f\"   链接: {r.get('link')}\")  
"""  
```  

## 实用脚本  

### 可重用的搜索函数  
```python  
python -c """  
from ddgs import DDGS  

def web_search(query, search_type='text', max_results=5, region='wt-wt', timelimit=None):  
    """  
    执行 DDGS 搜索  

    参数：  
        query: 搜索关键词  
        search_type: 文本、新闻、图片、视频、书籍  
        max_results: 最大结果数量  
        region: 地区（cn-zh、us-en、wt-wt）  
        timelimit: 时间限制（d、w、m、y）  
    """  
    ddgs = DDGS()  
    if search_type == 'text':  
        return list(ddgs.text(query, region=region, timelimit=timelimit, max_results=max_results)  
    elif search_type == 'news':  
        return list(ddgs.news(query, region=region, timelimit=timelimit, max_results=max_results)  
    elif search_type == 'images':  
        return list(ddgs.images(query, region=region, max_results=max_results)  
    elif search_type == 'videos':  
        return list(ddgs/videos(query, region=region, timelimit=timelimit, max_results=max_results)  
    elif search_type == 'books':  
        return list(ddgs.books(query, max_results=max_results)  
    return []  

results = web_search('Python 3.12 新特性', max_results=5)  
print(f'找到了 {len(results)} 条结果')  
"""  
```  

## 参数说明  

### 地区代码（region）  
| 代码 | 地区 |  
|---|---|  
| cn-zh | 中国 |  
| us-en | 美国 |  
| uk-en | 英国 |  
| jp-jp | 日本 |  
| kr-kr | 韩国 |  
| wt-wt | 全球（无地区限制） |  

### 时间限制（timelimit）  
| 值 | 含义 |  
|---|---|  
| d | 过去 24 小时 |  
| w | 过去一周 |  
| m | 过去一个月 |  
| None | 无限制 |  

### 安全搜索（safesearch）  
| 值 | 含义 |  
|---|---|  
| on | 严格过滤 |  
| moderate | 中等过滤（默认） |  
| off | 关闭过滤 |  

## 错误处理与代理设置  

### 基本错误处理  
```python  
python -c """  
from ddgs import DDGS  
from ddgs.exceptions import DDGSException  

try:  
    results = DDGS().text('测试查询', max_results=5)  
    print(f'✅ 搜索成功，找到了 {len(results)} 条结果')  
except DDGSException as e:  
    print(f'❌ 搜索错误: {e}')  
except Exception as e:  
    print(f'❌ 未知错误: {e}')  
"""  
```  

### 使用代理  
```python  
python -c """  
from ddgs import DDGS  

# 设置代理（支持 http/https/socks5）  
proxy = 'http://127.0.0.1:7890'  

results = DDGS(proxy=proxy).text('测试查询', max_results=5)  
print(f'通过代理成功搜索，找到了 {len(results)} 条结果')  
"""  
```  

## 常见问题解答  

**安装失败？**  
```bash  
pip install --upgrade pip  
pip install ddgs  
```  

**未找到结果？**  
- 检查网络连接。  
- 尝试使用代理。  
- 简化搜索关键词。  
- 确认地区设置是否正确。  

**遇到速率限制？**  
- 在多次请求之间添加延迟（例如：`import time; time.sleep(1)`）。  
- 减少每次请求的结果数量。  

## 集成与注意事项  

### 集成示例  
```python  
# 1. 使用 DDGS 进行搜索  
python -c """  
from ddgs import DDGS  
results = DDGS().text('Python 异步教程', max_results=1)  
if results:  
    print(f\"链接: {results[0].get('href')}\")  
"""  

# 2. 使用浏览器或工具打开搜索结果  
browser-use open <搜索结果链接>  
```  

**⚠️ 最佳实践：**  
- **遵守速率限制**：避免在短时间内发送大量请求。  
- **优化结果**：避免在单次查询中请求过多结果。  
- **添加延迟**：执行批量搜索时使用 `time.sleep()`。  
- **处理异常**：始终使用 `try/except` 块来捕获 API 调用中的错误。  
- **尊重版权**：搜索结果仅用于参考，请尊重被索引内容的版权。