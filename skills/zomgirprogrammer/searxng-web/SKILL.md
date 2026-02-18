# searxng-web

searxng-web 提供了一个简单的工具，该工具会将查询请求代理到本地运行的 searxng 实例（地址为 `http://host.docker.internal:8081/search?format=json&q=...`），并返回标准化后的查询结果。

## 功能概述
- 提供的接口：`searxng_search(query, count=5)`
- 执行该接口的脚本：`searxng_search.js`（基于 Node.js）
- 返回的结果格式：JSON 格式，包含以下内容：
  ```json
  {
    "query": "zillow rentals",
    "count": 3,
    "results": [
      {
        "title": "Zillow 租赁信息",
        "url": "https://www.zillow.com/rents/zillow-rents",
        "snippet": "查看 Zillow 上的出租房源",
        "source": "Zillow"
      }
    ]
  }
  ```

## 使用示例

### 简单调用示例
输入：
```json
{
  "query": "zillow rentals",
  "count": 3
}
```

执行命令：
```bash
docker exec -it openclaw sh -lc "searxng_search \"zillow rentals\", 3"
```
这将在容器内执行 `searxng_search.js` 脚本，并输出查询结果。