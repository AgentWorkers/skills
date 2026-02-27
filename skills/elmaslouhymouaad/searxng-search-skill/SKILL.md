# SearXNG高级搜索技巧

## 创建 `.env` 文件
```bash
# 创建 .env 文件
cat > .env << EOF
SEARXNG_URL=http://localhost:8080
SEARXNG_TIMEOUT=10
SEARXNG_MAX_RETRIES=3
SEARXNG_RETRY_DELAY=1.0
SEARXNG_BACKOFF_FACTOR=2.0
SEARXNG_VERIFY_SSL=true
SEARXNGLANGUAGE=en
EOF
```

## 创建 `config.json` 文件
```bash
# 创建 config.json 文件
cat > config.json << EOF
{
  "instance_url": "http://localhost:8080",
  "default_timeout": 10,
  "max_retries": 3,
  "retry_delay": 1.0,
  "backoff_factor": 2.0,
  "verify_ssl": true,
  "default_language": "en"
}
EOF
```

## 使用 `searxng_skill` 库进行搜索
```python
# 从环境变量中获取配置
config = SearXNGConfig.from_env()
skill = SearXNGSkill(config=config)

# 从文件中获取配置
config = SearXNGConfig.from_file("config.json")
skill = SearXNGSkill(config=config)

# 直接使用实例地址进行搜索
skill = SearXNGSkill(instance_url="http://localhost:8080")
```

## 示例搜索操作
```python
# 搜索“Python编程”相关内容
results = skill.search("Python programming")

# 遍历搜索结果并打印
for result in results["results"][:10]:
    print(f"{result['title']} - {result['url']}")
```

## 分类搜索
```python
# 单一类别搜索
results = skill.search("AI", categories=[SearchCategory.NEWS])

# 多个类别搜索
results = skill.search(
    "climate change",
    categories=[SearchCategory.NEWS, SearchCategory.SCIENCE]
)
```

## 时间范围搜索
```python
# 搜索过去24小时内的新闻
news = skill.news_search("AI breakthrough", time_range=TimeRange.DAY)

# 搜索过去一周的内容
results = skill.search("Python", time_range=TimeRange.WEEK)
```

## 安全搜索
```python
# 搜索“自然摄影”图片（使用严格过滤）
images = skill.image_search(
    "nature photography",
    safesearch=SafeSearch.STRICT
)

# 遍历并打印图片信息
for img in images[:10]:
    print(f"{img['title']}: {img.get('img_src', 'N/A')}")
```

## 高级搜索
```python
# 高级搜索示例
results = skill.advanced_search(
    query="machine learning",
    exact_phrase="deep learning",
    exclude_words=["tutorial", "beginner"],
    site="github.com",
    filetype="pdf"
)
```

## 自动完成搜索
```python
suggestions = skill.autocomplete("artificial int")
```

## 多类别搜索
```python
# 多类别搜索示例
categorized = skill.multi_category_search(
    "climate change",
    categories=[
        SearchCategory.GENERAL,
        SearchCategory.NEWS,
        SearchCategory.SCIENCE
    ]
```

## 并发搜索
```python
queries = ["Python", "JavaScript", "Go", "Rust"]
results = skill.parallel_search(queries, categories=[SearchCategory.IT])

# 获取多页搜索结果
all_results = []
for page in range(1, 4):
    results = skill.search("AI", page=page)
    all_results.extend(results["results"])

# 打印总结果数量
print(f"总结果数量: {len(all_results)}")
```

## 检查 SearXNG 实例状态
```python
if skill.health_check():
    print("✓ SearXNG 实例运行正常")
else:
    print("✗ 实例不可用")
```

## 查看支持的搜索引擎
```python
engines = skill.get_engines_info()
for engine in engines[:10]:
    print(f"{engine.name} - {', '.join(engine.categories)}")
    print(f"  是否启用: {engine.enabled}")
```

## 导出搜索结果
```python
# 将搜索结果导出为 JSON 文件
export_results_json(results, "results.json")

# 将搜索结果导出为 CSV 文件
export_results_csv(results["results"], "results.csv")
```

## 定义搜索类别
```python
SearchCategory.GENERAL      # 通用搜索
SearchCategory.IMAGES       # 图片搜索
SearchCategory.Videos       # 视频搜索
SearchCategory.NEWS         # 新闻文章
SearchCategory.MAP          # 地图
SearchCategory.MUSIC        # 音乐
SearchCategory.IT           # IT/技术
SearchCategory.SCIENCE      # 科学论文
SearchCategory.Files        # 文件搜索
SearchCategory.SOCIAL_MEDIA # 社交媒体
```

## 定义时间范围
```python
TimeRange.DAY    # 过去24小时
TimeRange.WEEK   # 过去7天
TimeRange.MONTH  # 过去30天
TimeRange.YEAR   # 过去一年
TimeRange.ALL    # 所有时间
```

## 设置搜索过滤选项
```python
SafeSearch.NONE     # 无过滤（0）
SafeSearch.MODERATE # 中等过滤（1）
SafeSearch.STRICT   # 严格过滤（2）
```

## 异常处理
```python
# 异常处理示例
try:
    results = skill.search("query", timeout=5)
except TimeoutException:
    print("请求超时 - 请增加超时时间")
except ConnectionException:
    print("无法连接到实例 - 请检查URL和网络连接")
```

## 使用 Docker 运行 SearXNG 服务
```bash
# 使用 Docker 运行 SearXNG 服务
docker run -d -p 8080:8080 searxng/searxng
```

## 验证 SearXNG 服务状态
```bash
# 验证服务状态
curl http://localhost:8080/healthz
```

## 重试策略
```python
# 重试策略示例
strategy = RetryStrategy(
    max_retries=5,
    initial_delay=2.0,
    backoff_factor=1.5,
    max_delay=60.0,
    jitter=True
)

skill = SearXNGSkill(
    instance_url="http://localhost:8080",
    max_retries=5,
    retry_delay=2.0,
    backoff_factor=1.5
)
```

## 限制搜索频率
```python
# 限制搜索频率
for query in ["Python", "Java", "Go", "Rust":
    results = skill.search(query)
    time.sleep(1)  # 每次搜索后等待1秒
```

## 去重搜索结果
```python
# 去重搜索结果
results = skill.search("AI")
unique = deduplicate_results(results["results"], key="url")
```

## 合并搜索结果
```python
# 合并多个搜索结果
r1 = skill.search("Python", engines=["google"])
r2 = skill.search("Python", engines=["duckduckgo"])
merged = merge_search_results([r1, r2])
```

## 日志记录
```python
# 日志记录示例
from logging import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 日志记录搜索过程
logger.info("正在搜索: Python")
results = skill.search("Python")
logger.info(f"找到 {len(results['results']) 条结果")
```

## 其他配置示例
```bash
# 检查实例是否正在运行
curl http://localhost:8080/healthz

# 或者在 Python 中检查实例状态
if not skill.health_check():
    print("实例未运行")
```

## 其他配置选项
```python
# 调整默认超时时间
skill = SearXNGSkill(instance_url="http://localhost:8080", default_timeout=30)

# 按请求设置超时时间
results = skill.search("query", timeout=30)
```

## 查看启用的搜索引擎
```python
# 查看启用的搜索引擎
engines = skill.get_engines_info()
enabled = [e for e in engines if e.enabled]
print(f"启用的引擎数量: {lenenabled)}
```