---
name: naver-news
description: 使用 Naver Search API 搜索韩国新闻文章。该 API 可用于查找韩国新闻、获取最新的新闻更新、搜索特定主题的新闻，或整理每日新闻摘要。支持按相关性或日期对搜索结果进行排序。
homepage: https://developers.naver.com/docs/serviceapi/search/news/news.md
metadata: {"openclaw":{"emoji":"📰","requires":{"bins":["python3"],"env":["NAVER_CLIENT_ID","NAVER_CLIENT_SECRET"]}}}
---

# Naver 新闻搜索

使用 Naver 搜索 API 搜索韩国新闻文章。

## 快速入门

使用提供的脚本来搜索新闻：

```bash
python scripts/search_news.py "검색어" --display 10 --sort date
```

**选项：**
- `--display N`：每页显示的结果数量（1-100，默认值：10）
- `--start N`：分页的起始位置（1-1000，默认值：1）
- `--sort sim|date`：按相关性（sim）或日期（date）排序（默认值：date）
- `--after DATETIME`：仅显示在该时间之后发布的新闻（ISO 8601 格式，例如：`2026-01-29T09:00:00+09:00`）
- `--min-results N`：需要获取的最小结果数量（启用自动分页）
- `--max-pages N`：自动分页时尝试的最大页面数（默认值：5）
- `--json`：输出原始 JSON 数据而非格式化文本

## 设置

### 环境变量

请从 https://developers.naver.com/ 获取所需的凭据：

```bash
NAVER_CLIENT_ID=your_client_id
NAVER_CLIENT_SECRET=your_client_secret
```

**配置位置：**
- **沙箱环境（默认）：** 添加到 OpenClaw 配置文件中的 `agentsdefaults.sandbox.docker.env`
- **主机环境：** 添加到 OpenClaw 配置文件中的 `env_vars`

### 获取 API 凭据

1. 访问 https://developers.naver.com/
2. 注册一个应用程序
3. 启用“검색”（Search）API
4. 复制客户端 ID（Client ID）和客户端密钥（Client Secret）
5. 将凭据添加到相应的配置部分（见上文）

## 常见用法

### 某主题的最新新闻

```bash
python scripts/search_news.py "AI 인공지능" --display 20 --sort date
```

### 按相关性排序搜索

```bash
python scripts/search_news.py "삼성전자" --sort sim
```

### 按时间过滤（仅显示最新新闻）

```bash
# News published after 9 AM today
python scripts/search_news.py "경제" --display 50 --sort sim --after "2026-01-29T09:00:00+09:00"

# News from the last hour (programmatic use)
python scripts/search_news.py "속보" --after "$(date -u -d '1 hour ago' '+%Y-%m-%dT%H:%M:%S%z')"
```

### 自动分页以确保获取最少结果数量

```bash
# Fetch at least 30 results (automatically requests multiple pages if needed)
python scripts/search_news.py "AI" --sort sim --after "2026-01-29T09:00:00+09:00" --min-results 30 --display 50

# Limit to 3 pages maximum
python scripts/search_news.py "게임" --min-results 50 --max-pages 3
```

**自动分页的工作原理：**
1. 获取第一页的内容（例如，50 条结果）
2. 应用时间过滤条件（例如，剩余 10 条结果）
3. 如果结果数量少于 `--min-results` 指定的数量，自动获取下一页
4. 当达到最小结果数量或达到 `--max-pages` 的限制时停止分页

### 通过分页获取更多结果

```bash
# First 10 results
python scripts/search_news.py "경제" --display 10 --start 1

# Next 10 results
python scripts/search_news.py "경제" --display 10 --start 11
```

## 在 Python 代码中使用

直接导入并使用搜索函数：

```python
from scripts.search_news import search_news

result = search_news(
    query="경제 뉴스",
    display=10,
    sort="date"
)

for item in result["items"]:
    print(item["title"])
    print(item["description"])
    print(item["link"])
```

## API 详情

有关完整的 API 参考信息（包括响应结构、错误代码和速率限制），请参阅：

**[references/api.md](references/api.md)**

## 注意事项

- 搜索查询必须为 UTF-8 编码
- 结果中包含 `<b>` 标签来标记搜索词匹配的部分（在处理文本时需要将其删除）
- 每个应用程序的每日 API 调用限制为 25,000 次
- `link` 字段可能指向 Naver News 或原始新闻来源，具体取决于实际情况