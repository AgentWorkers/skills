---
name: byted-infoquest-search
description: >
  通过 BytePlus InfoQuest API 实现的 AI 优化网页搜索和内容提取功能。该 API 为 AI 代理提供简洁、相关的内容结果，并支持时间过滤及针对特定网站的搜索。API 密钥可从以下链接获取：  
  https://console.byteplus.com/infoquest/infoquests
metadata: {"clawdbot":{"emoji":"🔍","requires":{"bins":["node"],"env":["INFOQUEST_API_KEY"]},"primaryEnv":"INFOQUEST_API_KEY"}}
---
# BytePlus InfoQuest 搜索

利用 BytePlus InfoQuest API 实现的、经过 AI 优化的网页搜索和内容提取功能。可返回简洁、相关的内容，并支持时间过滤和特定网站的搜索。

## 搜索

```bash
node {baseDir}/search.mjs "query"
node {baseDir}/search.mjs "query" -d 7
node {baseDir}/search.mjs "query" -s github.com
```

## 选项

- `-d, --days <数字>`：在过去的 N 天内进行搜索（默认：所有时间）
- `-s, --site <域名>`：在特定网站内进行搜索（例如：`github.com`）

## 从 URL 中提取内容

```bash
node {baseDir}/extract.mjs "https://example.com/article"
```

## 示例

### 最新新闻搜索
```bash
# Search for AI news from last 3 days
node search.mjs "artificial intelligence news" -d 3
```

### 特定网站的研究
```bash
# Search for Python projects on GitHub
node search.mjs "Python machine learning" -s github.com
```

### 内容提取
```bash
# Extract content from a single article
node extract.mjs "https://example.com/article"
```

## 注意事项

### API 访问
- **API 密钥**：请从 [https://console.byteplus.com/infoquest/infoquests](https://console.byteplus.com/infoquest/infoquests) 获取
- **文档**：[https://docs.byteplus.com/en/docs/InfoQuest/What_is_Info_Quest](https://docs.byteplus.com/en/docs/InfoQuest/What_is_Info_Quest)
- **关于 InfoQuest**：InfoQuest 是由 BytePlus 独立开发的、基于 AI 优化的智能搜索和爬虫工具集

### 搜索功能
- **时间过滤**：使用 `-d` 参数在过去的 N 天内进行搜索（例如：`-d 7`）
- **网站过滤**：使用 `-s` 参数在特定网站内进行搜索（例如：`-s github.com`）

## 快速设置

1. **设置 API 密钥：**
   ```bash
   export INFOQUEST_API_KEY="your-api-key-here"
   ```

2. **对于 Node.js 18 及以下版本，安装 fetch 库：**
   ```bash
   # Node.js 18+ includes fetch natively
   # For older versions, install node-fetch
   npm install node-fetch
   ```

3. **测试设置：**
   ```bash
   node search.mjs "test search"
   ```

## 错误处理

API 会返回以 `"Error:"` 开头的错误消息，表示以下情况：
- 认证失败
- 网络超时
- 返回的空响应
- 无效的响应格式